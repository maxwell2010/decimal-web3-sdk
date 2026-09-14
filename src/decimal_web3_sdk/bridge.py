from __future__ import annotations

from dataclasses import dataclass, field

from .mnemonic import FromMnemonicMixin
from .transactions import ContractCallRequest, TransactionResult
from .wallet import checksum


BRIDGE_V2_ABI = [
    {
        "inputs": [
            {"internalType": "bytes32", "name": "recipient", "type": "bytes32"},
            {"internalType": "uint16", "name": "toChainId", "type": "uint16"},
            {"internalType": "uint256", "name": "nonce", "type": "uint256"},
            {"internalType": "uint256", "name": "serviceFee", "type": "uint256"},
        ],
        "name": "wrapAndTransferETH",
        "outputs": [],
        "stateMutability": "payable",
        "type": "function",
    },
    {
        "inputs": [
            {"internalType": "address", "name": "token", "type": "address"},
            {"internalType": "bytes32", "name": "recipient", "type": "bytes32"},
            {"internalType": "uint256", "name": "amount", "type": "uint256"},
            {"internalType": "uint16", "name": "toChainId", "type": "uint16"},
            {"internalType": "uint256", "name": "nonce", "type": "uint256"},
        ],
        "name": "transferTokens",
        "outputs": [],
        "stateMutability": "payable",
        "type": "function",
    },
    {
        "inputs": [
            {"internalType": "bytes", "name": "encodedVM", "type": "bytes"},
            {"internalType": "bool", "name": "unwrapWETH", "type": "bool"},
        ],
        "name": "completeTransfer",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function",
    },
]


@dataclass(frozen=True)
class BridgeTransferNativeRequest(FromMnemonicMixin):
    contract: str
    to: str
    amount_wei: int
    service_fee_wei: int
    to_chain_id: int
    nonce: int
    private_key: str = field(repr=False)


@dataclass(frozen=True)
class BridgeTransferTokenRequest(FromMnemonicMixin):
    contract: str
    token: str
    to: str
    amount_raw: int
    service_fee_wei: int
    to_chain_id: int
    nonce: int
    private_key: str = field(repr=False)


@dataclass(frozen=True)
class BridgeCompleteTransferRequest(FromMnemonicMixin):
    contract: str
    encoded_vm: str
    unwrap_weth: bool
    private_key: str = field(repr=False)


class BridgeService:
    def __init__(self, client) -> None:
        self._client = client

    async def transfer_native(
        self,
        request: BridgeTransferNativeRequest,
        broadcast: bool = False,
        wait_receipt: bool = False,
    ) -> TransactionResult:
        data = self._contract(request.contract).functions.wrapAndTransferETH(
            _address_to_bytes32(request.to),
            int(request.to_chain_id),
            int(request.nonce),
            int(request.service_fee_wei),
        )._encode_transaction_data()
        value = int(request.amount_wei) + int(request.service_fee_wei)
        return await self._send(request.private_key, request.contract, data, value, broadcast, wait_receipt)

    async def transfer_token(
        self,
        request: BridgeTransferTokenRequest,
        broadcast: bool = False,
        wait_receipt: bool = False,
    ) -> TransactionResult:
        data = self._contract(request.contract).functions.transferTokens(
            checksum(request.token),
            _address_to_bytes32(request.to),
            int(request.amount_raw),
            int(request.to_chain_id),
            int(request.nonce),
        )._encode_transaction_data()
        return await self._send(
            request.private_key,
            request.contract,
            data,
            int(request.service_fee_wei),
            broadcast,
            wait_receipt,
        )

    async def complete_transfer(
        self,
        request: BridgeCompleteTransferRequest,
        broadcast: bool = False,
        wait_receipt: bool = False,
    ) -> TransactionResult:
        encoded_vm = bytes.fromhex(request.encoded_vm[2:] if request.encoded_vm.startswith("0x") else request.encoded_vm)
        data = self._contract(request.contract).functions.completeTransfer(
            encoded_vm,
            bool(request.unwrap_weth),
        )._encode_transaction_data()
        return await self._send(request.private_key, request.contract, data, 0, broadcast, wait_receipt)

    async def _send(
        self,
        private_key: str,
        contract: str,
        data: str,
        value_wei: int,
        broadcast: bool,
        wait_receipt: bool,
    ) -> TransactionResult:
        draft = await self._client.tx.build_contract_call(
            ContractCallRequest(contract=contract, private_key=private_key, data=data, value_wei=value_wei)
        )
        return await self._client.tx.send_draft(draft, private_key, broadcast, wait_receipt)

    def _contract(self, contract_address: str):
        return self._client.web3.eth.contract(address=checksum(contract_address), abi=BRIDGE_V2_ABI)


def _address_to_bytes32(address: str) -> bytes:
    checked = checksum(address)
    return bytes.fromhex(checked[2:].rjust(64, "0"))
