"""Decimal weighted Safe: creation, owner approval and execution."""

from __future__ import annotations

from dataclasses import dataclass, field, replace
from typing import Literal

from eth_account import Account
from eth_account.messages import encode_defunct, encode_typed_data
from hexbytes import HexBytes
from web3 import Web3
from web3.logs import DISCARD

from ._contract_operations import (
    ContractOperationRequest,
    ContractOperations,
    ZERO_ADDRESS,
    address,
    uint,
)
from .mnemonic import FromMnemonicMixin
from .transactions import ContractCallRequest, TransactionDraft, TransactionResult
from .wallet import checksum, private_key_to_address


@dataclass(frozen=True)
class WeightedOwner:
    owner: str
    weight: int = 1


@dataclass(frozen=True)
class SafeTransaction:
    to: str
    nonce: int
    value_wei: int = 0
    data: str = "0x"
    operation: Literal[0, 1] = 0
    safe_tx_gas: int = 0
    base_gas: int = 0
    gas_price_wei: int = 0
    gas_token: str = ZERO_ADDRESS
    refund_receiver: str = ZERO_ADDRESS

    def values(self) -> tuple:
        if type(self.operation) is not int or self.operation not in (0, 1):
            raise ValueError("operation must be 0 (call) or 1 (delegatecall)")
        return (
            checksum(self.to),
            uint(self.value_wei, "value_wei"),
            _data(self.data),
            self.operation,
            uint(self.safe_tx_gas, "safe_tx_gas"),
            uint(self.base_gas, "base_gas"),
            uint(self.gas_price_wei, "gas_price_wei"),
            checksum(self.gas_token),
            checksum(self.refund_receiver),
            uint(self.nonce, "nonce"),
        )


def _data(value: str) -> bytes:
    if not isinstance(value, str) or not value.startswith("0x") or len(value) % 2:
        raise ValueError("data must be even-length 0x-prefixed hexadecimal")
    return bytes.fromhex(value[2:])


def safe_typed_data(safe: str, chain_id: int, transaction: SafeTransaction):
    names = (
        "to",
        "value",
        "data",
        "operation",
        "safeTxGas",
        "baseGas",
        "gasPrice",
        "gasToken",
        "refundReceiver",
        "nonce",
    )
    types = (
        "address",
        "uint256",
        "bytes",
        "uint8",
        "uint256",
        "uint256",
        "uint256",
        "address",
        "address",
        "uint256",
    )
    return encode_typed_data(
        full_message={
            "types": {
                "EIP712Domain": [
                    {"name": "chainId", "type": "uint256"},
                    {"name": "verifyingContract", "type": "address"},
                ],
                "SafeTx": [{"name": name, "type": kind} for name, kind in zip(names, types)],
            },
            "primaryType": "SafeTx",
            "domain": {
                "chainId": uint(chain_id, "chain_id", positive=True),
                "verifyingContract": address(safe),
            },
            "message": dict(zip(names, transaction.values())),
        }
    )


def safe_transaction_hash(safe: str, chain_id: int, transaction: SafeTransaction) -> str:
    message = safe_typed_data(safe, chain_id, transaction)
    return "0x" + Web3.keccak(b"\x19" + message.version + message.header + message.body).hex()


@dataclass(frozen=True)
class SafeSignature:
    signer: str
    data: str = field(repr=False)
    kind: Literal["eip712", "eth_sign", "approved_hash", "contract"] = "eip712"

    @classmethod
    def preapproved(cls, signer: str) -> "SafeSignature":
        signer = address(signer)
        data = int(signer, 16).to_bytes(32, "big") + bytes(32) + b"\x01"
        return cls(signer, "0x" + data.hex(), "approved_hash")


@dataclass(frozen=True)
class SignSafeTransactionRequest(FromMnemonicMixin):
    safe: str
    chain_id: int
    transaction: SafeTransaction
    private_key: str = field(repr=False)


def sign_safe_transaction(request: SignSafeTransactionRequest) -> SafeSignature:
    """Sign EIP-712 data locally; this is not an on-chain transaction."""
    message = safe_typed_data(request.safe, request.chain_id, request.transaction)
    signed = Account.sign_message(message, request.private_key)
    return SafeSignature(private_key_to_address(request.private_key), "0x" + signed.signature.hex())


def pack_safe_signatures(
    safe: str, chain_id: int, transaction: SafeTransaction, signatures: tuple[SafeSignature, ...]
) -> bytes:
    if not signatures:
        raise ValueError("At least one Safe signature is required")
    ordered = sorted(signatures, key=lambda item: address(item.signer).lower())
    if len({address(item.signer) for item in ordered}) != len(ordered):
        raise ValueError("Duplicate Safe signature owner")
    static, dynamic = bytearray(), bytearray()
    for signature in ordered:
        signer, data = address(signature.signer), _data(signature.data)
        if signature.kind == "contract":
            if not data:
                raise ValueError("Contract signature cannot be empty")
            offset = len(ordered) * 65 + len(dynamic)
            static.extend(
                int(signer, 16).to_bytes(32, "big") + offset.to_bytes(32, "big") + b"\x00"
            )
            dynamic.extend(len(data).to_bytes(32, "big") + data)
            continue
        if len(data) != 65:
            raise ValueError("ECDSA and approved-hash signatures must be 65 bytes")
        if signature.kind == "approved_hash":
            if data != _data(SafeSignature.preapproved(signer).data):
                raise ValueError("Invalid approved-hash signature")
        elif signature.kind in ("eip712", "eth_sign"):
            message = safe_typed_data(safe, chain_id, transaction)
            recover_data = data
            if signature.kind == "eth_sign":
                if data[-1] not in (31, 32):
                    raise ValueError("Safe eth_sign v must be 31 or 32")
                message = encode_defunct(
                    primitive=HexBytes(safe_transaction_hash(safe, chain_id, transaction))
                )
                recover_data = data[:-1] + bytes([data[-1] - 4])
            elif data[-1] not in (27, 28):
                raise ValueError("Safe EIP-712 v must be 27 or 28")
            recovered = Account.recover_message(message, signature=recover_data)
            if checksum(recovered) != signer:
                raise ValueError(
                    "Safe signature does not match its owner, chain, Safe or transaction"
                )
        else:
            raise ValueError("Unsupported Safe signature kind")
        static.extend(data)
    return bytes(static + dynamic)


@dataclass(frozen=True)
class CreateMultisigRequest(ContractOperationRequest):
    owners: tuple[WeightedOwner, ...]
    weight_threshold: int
    salt_nonce: int
    fallback_handler: str = ZERO_ADDRESS
    domain = "multisig"

    def to_contract_call(self, client):
        if not self.owners or not all(isinstance(item, WeightedOwner) for item in self.owners):
            raise ValueError("A nonempty tuple of WeightedOwner values is required")
        owners = [
            (address(item.owner), uint(item.weight, "weight", positive=True))
            for item in self.owners
        ]
        if len({owner for owner, _ in owners}) != len(owners):
            raise ValueError("Duplicate Safe owner")
        if any(weight > 1000 or int(owner, 16) == 1 for owner, weight in owners):
            raise ValueError("Invalid Safe owner or weight; weights must be between 1 and 1000")
        threshold = uint(self.weight_threshold, "weight_threshold", positive=True)
        if threshold > sum(weight for _, weight in owners):
            raise ValueError("weight_threshold exceeds total owner weight")
        safe = client.web3.eth.contract(
            address=address(client.config.contracts.safe), abi=client.abi.load("safe")
        )
        initializer = safe.encode_abi(
            "setup",
            args=[
                owners,
                threshold,
                ZERO_ADDRESS,
                b"",
                checksum(self.fallback_handler),
                ZERO_ADDRESS,
                0,
                ZERO_ADDRESS,
            ],
        )
        return self._encode(
            client,
            "safe_factory",
            client.config.contracts.safe_factory,
            "createProxyWithNonce",
            [safe.address, _data(initializer), uint(self.salt_nonce, "salt_nonce")],
        )


@dataclass(frozen=True)
class ApproveMultisigTransactionRequest(ContractOperationRequest):
    safe: str
    transaction: SafeTransaction
    domain = "multisig"

    def to_contract_call(self, client):
        return self._encode(client, "safe", self.safe, "approveHash", [self.transaction.values()])


@dataclass(frozen=True)
class ExecuteMultisigTransactionRequest(ApproveMultisigTransactionRequest):
    signatures: tuple[SafeSignature, ...]

    def to_contract_call(self, client):
        signatures = pack_safe_signatures(
            self.safe, client.config.chain_id, self.transaction, self.signatures
        )
        return self._encode(
            client,
            "safe",
            self.safe,
            "execTransaction",
            [*self.transaction.values()[:-1], signatures],
        )


@dataclass(frozen=True)
class MultisigState:
    nonce: int
    owners: tuple[WeightedOwner, ...]
    weight_threshold: int
    block_number: int


class MultisigService(ContractOperations):
    _operation_domain = "multisig"

    def __init__(self, client):
        self._client = client

    async def state(self, safe: str) -> MultisigState:
        target, abi = address(safe), self._client.abi.load("safe")

        def read(w3):
            block = w3.eth.block_number
            contract = w3.eth.contract(address=target, abi=abi)
            nonce = contract.functions.nonce().call(block_identifier=block)
            owners = contract.functions.getOwnersWithWeights().call(block_identifier=block)
            threshold = contract.functions.getWeightThreshold().call(block_identifier=block)
            return MultisigState(
                int(nonce), tuple(WeightedOwner(*owner) for owner in owners), int(threshold), block
            )

        return await self._client.rpc.call(read)

    async def build_transaction(
        self, safe: str, call: ContractCallRequest | TransactionDraft, *, nonce: int | None = None
    ) -> SafeTransaction:
        """Wrap an unsigned SDK call for the Safe, including new NFT operations."""
        address(safe)
        if nonce is None:
            nonce = (await self.state(safe)).nonce
        if isinstance(call, ContractCallRequest):
            result = SafeTransaction(call.contract, nonce, call.value_wei, call.data)
        elif isinstance(call, TransactionDraft):
            if call.raw_tx or call.tx_hash:
                raise ValueError("Use an unsigned draft to build a Safe transaction")
            result = SafeTransaction(
                call.tx["to"], nonce, call.tx.get("value", 0), call.tx.get("data", "0x")
            )
        else:
            raise TypeError("An unsigned ContractCallRequest or TransactionDraft is required")
        result.values()
        return result

    async def build_operation(self, request: ContractOperationRequest) -> TransactionDraft:
        draft = await super().build_operation(request)
        if isinstance(request, CreateMultisigRequest) and not await self._singleton_has_code():
            raise ValueError("The configured Safe implementation has no contract code")
        if isinstance(request, ApproveMultisigTransactionRequest):
            state = await self.state(request.safe)
            if state.nonce != request.transaction.nonce:
                raise ValueError(
                    "Safe nonce changed; rebuild the transaction and collect signatures again"
                )
            owner = private_key_to_address(request.private_key)
            weights = {checksum(item.owner): item.weight for item in state.owners}
            if isinstance(request, ExecuteMultisigTransactionRequest):
                signed_weight = sum(
                    weights.get(checksum(sig.signer), 0) for sig in request.signatures
                )
                if state.weight_threshold <= 0 or signed_weight < state.weight_threshold:
                    raise ValueError("Insufficient Safe signature weight")
                if not await self._simulate_execution(request, draft):
                    raise ValueError("The Safe simulation reports failure of the inner transaction")
            elif checksum(owner) not in weights:
                raise ValueError("Only a Safe owner can approve the transaction")
        return draft

    async def _singleton_has_code(self) -> bool:
        target = address(self._client.config.contracts.safe)
        return bool(await self._client.rpc.call(lambda w3: w3.eth.get_code(target)))

    async def _simulate_execution(self, request, draft) -> bool:
        # execTransaction can return false without reverting the outer transaction.
        abi, target = self._client.abi.load("safe"), address(request.safe)

        def simulate(w3):
            contract = w3.eth.contract(address=target, abi=abi)
            function, args = contract.decode_function_input(draft.tx["data"])
            return function(**args).call({"from": draft.tx["from"]})

        return bool(await self._client.rpc.call(simulate))

    async def create(
        self, request: CreateMultisigRequest, broadcast: bool = False, wait_receipt: bool = False
    ) -> TransactionResult:
        result = await self._send_operation(
            request, broadcast, wait_receipt, request_type=CreateMultisigRequest
        )
        if result.receipt and result.success:
            contract = self._client.web3.eth.contract(
                address=address(self._client.config.contracts.safe_factory),
                abi=self._client.abi.load("safe_factory"),
            )
            events = contract.events.ProxyCreation().process_receipt(result.receipt, errors=DISCARD)
            events = [event for event in events if checksum(event["address"]) == contract.address]
            if len(events) == 1:
                result = replace(
                    result,
                    events={**(result.events or {}), "safe_address": events[0]["args"]["proxy"]},
                )
        return result

    async def approve_transaction(
        self,
        request: ApproveMultisigTransactionRequest,
        broadcast: bool = False,
        wait_receipt: bool = False,
    ) -> TransactionResult:
        return await self._send_operation(
            request, broadcast, wait_receipt, request_type=ApproveMultisigTransactionRequest
        )

    async def execute(
        self,
        request: ExecuteMultisigTransactionRequest,
        broadcast: bool = False,
        wait_receipt: bool = False,
    ) -> TransactionResult:
        result = await self._send_operation(
            request, broadcast, wait_receipt, request_type=ExecuteMultisigTransactionRequest
        )
        if result.success:
            result = replace(
                result,
                events={
                    **(result.events or {}),
                    "safe_transaction_hash": safe_transaction_hash(
                        request.safe, self._client.config.chain_id, request.transaction
                    ),
                },
            )
        if result.receipt and result.success:
            return self.check_execution_result(request.safe, request.transaction, result)
        return result

    def check_execution_result(
        self, safe: str, transaction: SafeTransaction, result: TransactionResult
    ) -> TransactionResult:
        """Check the inner outcome after a receipt, even when outer status is 1."""
        if not result.receipt or not result.success:
            return result
        tx_hash = HexBytes(safe_transaction_hash(safe, self._client.config.chain_id, transaction))
        target = address(safe)
        contract = self._client.web3.eth.contract(address=target, abi=self._client.abi.load("safe"))

        def matching(event):
            return [
                item
                for item in event().process_receipt(result.receipt, errors=DISCARD)
                if checksum(item["address"]) == target
                and HexBytes(item["args"]["txHash"]) == tx_hash
            ]

        failure = matching(contract.events.ExecutionFailure)
        success = matching(contract.events.ExecutionSuccess)
        if failure or not success:
            error = (
                "Safe inner execution failed"
                if failure
                else "Safe execution outcome was not confirmed by an event"
            )
            result = replace(
                result,
                success=False,
                status="failed" if failure else "unknown",
                error=error,
                user_message=error,
            )
        return result
