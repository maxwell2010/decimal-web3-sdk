from __future__ import annotations

from dataclasses import dataclass, field

from eth_account import Account
from eth_account.messages import encode_defunct
from hexbytes import HexBytes
from web3 import Web3

from .erc20 import PermitSignature
from .mnemonic import FromMnemonicMixin
from .transactions import ContractCallRequest, TransactionResult
from .wallet import checksum, mnemonic_to_private_key


CHECKS_ABI = [
    {
        "anonymous": False,
        "inputs": [
            {"indexed": False, "name": "checkHash", "type": "bytes32"},
            {"indexed": False, "name": "check", "type": "tuple", "components": [
                {"name": "checkDetails", "type": "bytes32"},
                {"name": "signer", "type": "address"},
                {"name": "status", "type": "uint8"},
            ]},
        ],
        "name": "CreatedCheck",
        "type": "event",
    },
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

    def created_check_hashes(
        self, receipt: dict, *, contract: str | None = None,
    ) -> tuple[str, ...]:
        status = receipt.get("status")
        if (int(status, 0) if isinstance(status, str) else status) != 1:
            raise ValueError("A successful receipt is required")
        target = checksum(contract or self._client.config.contracts.checks)
        event = self._client.web3.eth.contract(abi=CHECKS_ABI).events.CreatedCheck()
        topic = Web3.keccak(text="CreatedCheck(bytes32,(bytes32,address,uint8))")
        hashes = []
        for log in receipt.get("logs", []):
            if checksum(log["address"]) != target or not log.get("topics"):
                continue
            if HexBytes(log["topics"][0]) != topic:
                continue
            normalized = {key: receipt.get(key) for key in (
                "blockHash", "blockNumber", "transactionHash", "transactionIndex",
            )}
            normalized.update(log)
            normalized.setdefault("logIndex", 0)
            hashes.append(Web3.to_hex(event.process_log(normalized)["args"]["checkHash"]))
        return tuple(hashes)

    @staticmethod
    def sign_redemption(
        check_hash: str, redeemer: str, mnemonic: str, *,
        account_index: int = 0, passphrase: str = "",
    ) -> str:
        check = HexBytes(check_hash)
        if len(check) != 32:
            raise ValueError("check_hash must be 32 bytes")
        digest = Web3.solidity_keccak(["bytes32", "address"], [check, checksum(redeemer)])
        private_key = mnemonic_to_private_key(
            mnemonic, passphrase=passphrase, account_index=account_index,
        )
        signature = Account.sign_message(encode_defunct(primitive=digest), private_key).signature
        return Web3.to_hex(signature)

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
        return int(await self._client.rpc.call(lambda w3: self._contract(contract_address, w3).functions.nonces().call()))

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

    def _contract(self, contract_address: str, web3=None):
        return (web3 or self._client.web3).eth.contract(address=checksum(contract_address), abi=CHECKS_ABI)
