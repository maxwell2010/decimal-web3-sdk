from __future__ import annotations

from dataclasses import dataclass, field

from .erc20 import PermitSignature
from .mnemonic import FromMnemonicMixin
from .transactions import ContractCallRequest, TransactionResult
from .wallet import checksum


CHECKS_ABI = [
    {
        "inputs": [],
        "name": "nonces",
        "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
        "stateMutability": "view",
        "type": "function",
    },
    {
        "inputs": [
            {"internalType": "address[]", "name": "signers", "type": "address[]"},
            {"internalType": "uint256", "name": "amount", "type": "uint256"},
            {"internalType": "uint256", "name": "dueBlock", "type": "uint256"},
            {"internalType": "uint256", "name": "nonce", "type": "uint256"},
        ],
        "name": "createChecksDEL",
        "outputs": [{"internalType": "bytes32[]", "name": "", "type": "bytes32[]"}],
        "stateMutability": "payable",
        "type": "function",
    },
    {
        "inputs": [
            {"internalType": "address[]", "name": "signers", "type": "address[]"},
            {"internalType": "uint256", "name": "amount", "type": "uint256"},
            {"internalType": "uint256", "name": "dueBlock", "type": "uint256"},
            {"internalType": "uint256", "name": "nonce", "type": "uint256"},
            {"internalType": "address", "name": "token", "type": "address"},
        ],
        "name": "createChecksToken",
        "outputs": [{"internalType": "bytes32[]", "name": "", "type": "bytes32[]"}],
        "stateMutability": "nonpayable",
        "type": "function",
    },
    {
        "inputs": [
            {"internalType": "address[]", "name": "signers", "type": "address[]"},
            {"internalType": "uint256", "name": "amount", "type": "uint256"},
            {"internalType": "uint256", "name": "dueBlock", "type": "uint256"},
            {"internalType": "uint256", "name": "nonce", "type": "uint256"},
            {"internalType": "address", "name": "token", "type": "address"},
            {"internalType": "uint256", "name": "deadline", "type": "uint256"},
            {"internalType": "uint8", "name": "v", "type": "uint8"},
            {"internalType": "bytes32", "name": "r", "type": "bytes32"},
            {"internalType": "bytes32", "name": "s", "type": "bytes32"},
        ],
        "name": "createChecksTokenByPermit",
        "outputs": [{"internalType": "bytes32[]", "name": "", "type": "bytes32[]"}],
        "stateMutability": "nonpayable",
        "type": "function",
    },
    {
        "inputs": [
            {"internalType": "bytes[]", "name": "signatures", "type": "bytes[]"},
            {"internalType": "bytes32[]", "name": "checks", "type": "bytes32[]"},
        ],
        "name": "redeemChecks",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function",
    },
]


@dataclass(frozen=True)
class CreateChecksDelRequest(FromMnemonicMixin):
    contract: str
    signers: list[str]
    amount_wei: int
    due_block: int
    private_key: str = field(repr=False)
    nonce: int | None = None


@dataclass(frozen=True)
class CreateChecksTokenRequest(FromMnemonicMixin):
    contract: str
    token: str
    signers: list[str]
    amount_raw: int
    due_block: int
    private_key: str = field(repr=False)
    nonce: int | None = None
    permit: PermitSignature | None = None


@dataclass(frozen=True)
class RedeemChecksRequest(FromMnemonicMixin):
    contract: str
    signatures: list[str]
    checks: list[str]
    private_key: str = field(repr=False)


class ChecksService:
    def __init__(self, client) -> None:
        self._client = client

    async def create_del(
        self,
        request: CreateChecksDelRequest,
        broadcast: bool = False,
        wait_receipt: bool = False,
    ) -> TransactionResult:
        nonce = await self._nonce(request.contract) if request.nonce is None else int(request.nonce)
        signers = [checksum(item) for item in request.signers]
        data = self._contract(request.contract).functions.createChecksDEL(
            signers,
            int(request.amount_wei),
            int(request.due_block),
            nonce,
        )._encode_transaction_data()
        value = len(signers) * int(request.amount_wei)
        return await self._send(request.private_key, request.contract, data, value, broadcast, wait_receipt)

    async def create_token(
        self,
        request: CreateChecksTokenRequest,
        broadcast: bool = False,
        wait_receipt: bool = False,
    ) -> TransactionResult:
        nonce = await self._nonce(request.contract) if request.nonce is None else int(request.nonce)
        signers = [checksum(item) for item in request.signers]
        contract = self._contract(request.contract)
        if request.permit is None:
            data = contract.functions.createChecksToken(
                signers,
                int(request.amount_raw),
                int(request.due_block),
                nonce,
                checksum(request.token),
            )._encode_transaction_data()
        else:
            data = contract.functions.createChecksTokenByPermit(
                signers,
                int(request.amount_raw),
                int(request.due_block),
                nonce,
                checksum(request.token),
                int(request.permit.deadline),
                int(request.permit.v),
                request.permit.r,
                request.permit.s,
            )._encode_transaction_data()
        return await self._send(request.private_key, request.contract, data, 0, broadcast, wait_receipt)

    async def redeem(
        self,
        request: RedeemChecksRequest,
        broadcast: bool = False,
        wait_receipt: bool = False,
    ) -> TransactionResult:
        data = self._contract(request.contract).functions.redeemChecks(
            [bytes.fromhex(item[2:] if item.startswith("0x") else item) for item in request.signatures],
            request.checks,
        )._encode_transaction_data()
        return await self._send(request.private_key, request.contract, data, 0, broadcast, wait_receipt)

    async def _nonce(self, contract_address: str) -> int:
        contract = self._contract(contract_address)
        return int(await self._client.rpc.call(lambda _w3: contract.functions.nonces().call()))

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
        return self._client.web3.eth.contract(address=checksum(contract_address), abi=CHECKS_ABI)
