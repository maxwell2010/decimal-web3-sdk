from __future__ import annotations

import asyncio
from dataclasses import dataclass, field
from decimal import Decimal, ROUND_CEILING
from typing import Any

from eth_account import Account
from hexbytes import HexBytes
from web3 import Web3

from .wallet import DEFAULT_DERIVATION_PATH, checksum, mnemonic_to_private_key, normalize_private_key, private_key_to_address


@dataclass(frozen=True)
class MemoCapability:
    transaction_type: str
    supported: bool
    request_field: str | None
    transport: str
    notes: str


MEMO_CAPABILITY_MATRIX: tuple[MemoCapability, ...] = (
    MemoCapability(
        transaction_type="native_del_transfer",
        supported=True,
        request_field="NativeTransferRequest.memo",
        transport="EVM transaction data",
        notes="UTF-8 memo is encoded into native DEL transaction data; gas estimation includes the payload.",
    ),
    MemoCapability(
        transaction_type="multisend_del",
        supported=True,
        request_field="MultisendDelRequest.memo",
        transport="Decimal multicall aggregate",
        notes="One UTF-8 memo for the whole DEL batch is encoded as the final zero-value call to 0x0.",
    ),
    MemoCapability(
        transaction_type="multisend_erc20",
        supported=True,
        request_field="MultisendErc20Request.memo",
        transport="Decimal multicall aggregate",
        notes="One UTF-8 memo for the whole ERC20 batch is encoded as the final zero-value call to 0x0.",
    ),
    MemoCapability(
        transaction_type="erc20_transfer",
        supported=False,
        request_field=None,
        transport="ERC20 transfer calldata",
        notes="ERC20 transfer/approve/transferFrom calldata is occupied by ABI arguments and has no generic memo.",
    ),
    MemoCapability(
        transaction_type="contract_call",
        supported=False,
        request_field=None,
        transport="Contract calldata",
        notes="Use a contract-specific argument if that contract explicitly supports a note/message field.",
    ),
    MemoCapability(
        transaction_type="staking_token_nft_checks_bridge",
        supported=False,
        request_field=None,
        transport="Decimal system contracts",
        notes="No generic memo field is exposed by current request classes.",
    ),
)

_MEMO_TRANSACTION_ALIASES = {
    "send_del": "native_del_transfer",
    "del_transfer": "native_del_transfer",
    "native_transfer": "native_del_transfer",
    "erc20": "erc20_transfer",
    "erc20_transfer_from": "erc20_transfer",
    "erc20_approve": "erc20_transfer",
}


def memo_capabilities() -> tuple[MemoCapability, ...]:
    return MEMO_CAPABILITY_MATRIX


def memo_supported_for(transaction_type: str) -> bool:
    normalized = transaction_type.strip().lower().replace("-", "_")
    normalized = _MEMO_TRANSACTION_ALIASES.get(normalized, normalized)
    return any(item.transaction_type == normalized and item.supported for item in MEMO_CAPABILITY_MATRIX)


def encode_memo_data(memo: str | None) -> str:
    if not memo:
        return "0x"
    return "0x" + memo.encode("utf-8").hex()


def decode_memo_data(data: str | None) -> str | None:
    if not data or data == "0x":
        return None
    hex_data = data[2:] if data.startswith("0x") else data
    try:
        return bytes.fromhex(hex_data).decode("utf-8")
    except (ValueError, UnicodeDecodeError) as exc:
        raise ValueError("Transaction data is not a UTF-8 memo") from exc


@dataclass(frozen=True)
class NativeTransferRequest:
    to: str
    amount_del: Decimal | str | int | float
    private_key: str
    memo: str | None = None
    gas: int | None = None
    gas_price_wei: int | None = None

    @classmethod
    def from_mnemonic(
        cls,
        *,
        to: str,
        amount_del: Decimal | str | int | float,
        mnemonic: str,
        passphrase: str = "",
        account_path: str = DEFAULT_DERIVATION_PATH,
        memo: str | None = None,
        gas: int | None = None,
        gas_price_wei: int | None = None,
    ) -> "NativeTransferRequest":
        return cls(
            to=to,
            amount_del=amount_del,
            private_key=mnemonic_to_private_key(mnemonic, passphrase=passphrase, account_path=account_path),
            memo=memo,
            gas=gas,
            gas_price_wei=gas_price_wei,
        )


@dataclass(frozen=True)
class ContractCallRequest:
    contract: str
    private_key: str
    data: str
    value_wei: int = 0
    gas: int | None = None
    gas_price_wei: int | None = None

    @classmethod
    def from_mnemonic(
        cls,
        *,
        contract: str,
        data: str,
        mnemonic: str,
        passphrase: str = "",
        account_path: str = DEFAULT_DERIVATION_PATH,
        value_wei: int = 0,
        gas: int | None = None,
        gas_price_wei: int | None = None,
    ) -> "ContractCallRequest":
        return cls(
            contract=contract,
            private_key=mnemonic_to_private_key(mnemonic, passphrase=passphrase, account_path=account_path),
            data=data,
            value_wei=value_wei,
            gas=gas,
            gas_price_wei=gas_price_wei,
        )


@dataclass(frozen=True)
class Erc20TransferRequest:
    token: str
    to: str
    amount: Decimal | str | int | float
    private_key: str
    decimals: int | None = None
    gas: int | None = None
    gas_price_wei: int | None = None

    @classmethod
    def from_mnemonic(
        cls,
        *,
        token: str,
        to: str,
        amount: Decimal | str | int | float,
        mnemonic: str,
        passphrase: str = "",
        account_path: str = DEFAULT_DERIVATION_PATH,
        decimals: int | None = None,
        gas: int | None = None,
        gas_price_wei: int | None = None,
    ) -> "Erc20TransferRequest":
        return cls(
            token=token,
            to=to,
            amount=amount,
            private_key=mnemonic_to_private_key(mnemonic, passphrase=passphrase, account_path=account_path),
            decimals=decimals,
            gas=gas,
            gas_price_wei=gas_price_wei,
        )


@dataclass(frozen=True)
class Erc20ApproveRequest:
    token: str
    spender: str
    amount: Decimal | str | int | float
    private_key: str
    decimals: int | None = None
    gas: int | None = None
    gas_price_wei: int | None = None

    @classmethod
    def from_mnemonic(
        cls,
        *,
        token: str,
        spender: str,
        amount: Decimal | str | int | float,
        mnemonic: str,
        passphrase: str = "",
        account_path: str = DEFAULT_DERIVATION_PATH,
        decimals: int | None = None,
        gas: int | None = None,
        gas_price_wei: int | None = None,
    ) -> "Erc20ApproveRequest":
        return cls(
            token=token,
            spender=spender,
            amount=amount,
            private_key=mnemonic_to_private_key(mnemonic, passphrase=passphrase, account_path=account_path),
            decimals=decimals,
            gas=gas,
            gas_price_wei=gas_price_wei,
        )


@dataclass(frozen=True)
class Erc20TransferFromRequest:
    token: str
    owner: str
    to: str
    amount: Decimal | str | int | float
    private_key: str
    decimals: int | None = None
    gas: int | None = None
    gas_price_wei: int | None = None

    @classmethod
    def from_mnemonic(
        cls,
        *,
        token: str,
        owner: str,
        to: str,
        amount: Decimal | str | int | float,
        mnemonic: str,
        passphrase: str = "",
        account_path: str = DEFAULT_DERIVATION_PATH,
        decimals: int | None = None,
        gas: int | None = None,
        gas_price_wei: int | None = None,
    ) -> "Erc20TransferFromRequest":
        return cls(
            token=token,
            owner=owner,
            to=to,
            amount=amount,
            private_key=mnemonic_to_private_key(mnemonic, passphrase=passphrase, account_path=account_path),
            decimals=decimals,
            gas=gas,
            gas_price_wei=gas_price_wei,
        )


@dataclass
class TransactionDraft:
    tx: dict[str, Any]
    from_address: str
    to_address: str
    value_wei: int
    gas: int | None = None
    gas_price_wei: int | None = None
    fee_wei: int | None = None
    preflight: "FeePreflight | None" = None
    raw_tx: bytes | None = None
    tx_hash: str | None = None
    receipt: dict[str, Any] | None = None
    timings_ms: dict[str, float] = field(default_factory=dict)

    @property
    def fee_del(self) -> Decimal | None:
        if self.fee_wei is None:
            return None
        return Decimal(self.fee_wei) / Decimal(10**18)


@dataclass(frozen=True)
class TransactionResult:
    success: bool
    tx_hash: str | None = None
    status: str | None = None
    block_number: int | None = None
    transaction_index: int | None = None
    gas_used: int | None = None
    effective_gas_price_wei: int | None = None
    effective_fee_wei: int | None = None
    effective_fee_del: Decimal | None = None
    fee_wei: int | None = None
    fee_del: Decimal | None = None
    gas: int | None = None
    raw_tx_hex: str | None = None
    receipt: dict[str, Any] | None = None
    events: dict[str, Any] | None = None
    token_address: str | None = None
    error: str | None = None
    user_message: str | None = None
    native_balance_wei: int | None = None
    required_wei: int | None = None
    missing_wei: int | None = None
    token_balance_raw: int | None = None
    token_required_raw: int | None = None
    token_missing_raw: int | None = None
    token_allowance_raw: int | None = None
    token_allowance_required_raw: int | None = None
    token_allowance_missing_raw: int | None = None

    @property
    def is_confirmed(self) -> bool:
        return self.receipt is not None

    @property
    def is_successful(self) -> bool:
        return self.status == "success"

    @property
    def is_pending(self) -> bool:
        return self.status == "pending"


@dataclass(frozen=True)
class FeePreflight:
    ok: bool
    from_address: str
    native_balance_wei: int
    value_wei: int
    fee_wei: int
    required_wei: int
    missing_wei: int = 0
    gas: int | None = None
    gas_price_wei: int | None = None

    @property
    def fee_del(self) -> Decimal:
        return Decimal(self.fee_wei) / Decimal(10**18)

    @property
    def native_balance_del(self) -> Decimal:
        return Decimal(self.native_balance_wei) / Decimal(10**18)

    @property
    def value_del(self) -> Decimal:
        return Decimal(self.value_wei) / Decimal(10**18)

    @property
    def required_del(self) -> Decimal:
        return Decimal(self.required_wei) / Decimal(10**18)

    @property
    def missing_del(self) -> Decimal:
        return Decimal(self.missing_wei) / Decimal(10**18)


class TransactionService:
    def __init__(self, client) -> None:
        self._client = client

    async def build_native_transfer(self, request: NativeTransferRequest) -> TransactionDraft:
        private_key = normalize_private_key(request.private_key)
        from_address = private_key_to_address(private_key)
        to_address = checksum(request.to)
        value_wei = Web3.to_wei(Decimal(str(request.amount_del)), "ether")
        data = encode_memo_data(request.memo)
        nonce = await self._client.transaction_count(from_address)
        gas_price = request.gas_price_wei or await self._client.gas_price()
        tx: dict[str, Any] = {
            "chainId": self._client.config.chain_id,
            "from": from_address,
            "to": to_address,
            "value": int(value_wei),
            "nonce": nonce,
            "gasPrice": int(gas_price),
            "data": data,
        }
        if request.gas is not None:
            tx["gas"] = request.gas
        return TransactionDraft(
            tx=tx,
            from_address=from_address,
            to_address=to_address,
            value_wei=int(value_wei),
            gas=request.gas,
            gas_price_wei=int(gas_price),
        )

    async def build_contract_call(self, request: ContractCallRequest) -> TransactionDraft:
        private_key = normalize_private_key(request.private_key)
        from_address = private_key_to_address(private_key)
        contract_address = checksum(request.contract)
        nonce = await self._client.transaction_count(from_address)
        gas_price = request.gas_price_wei or await self._client.gas_price()
        tx: dict[str, Any] = {
            "chainId": self._client.config.chain_id,
            "from": from_address,
            "to": contract_address,
            "value": int(request.value_wei),
            "nonce": nonce,
            "gasPrice": int(gas_price),
            "data": request.data,
        }
        if request.gas is not None:
            tx["gas"] = request.gas
        return TransactionDraft(
            tx=tx,
            from_address=from_address,
            to_address=contract_address,
            value_wei=int(request.value_wei),
            gas=request.gas,
            gas_price_wei=int(gas_price),
        )

    async def build_erc20_transfer(self, request: Erc20TransferRequest) -> TransactionDraft:
        decimals = request.decimals
        if decimals is None:
            decimals = (await self._client.erc20.info(request.token)).decimals
        amount_raw = _parse_units(request.amount, decimals)
        data = self._client.erc20.build_transfer_data(request.token, request.to, amount_raw)
        return await self.build_contract_call(
            ContractCallRequest(
                contract=request.token,
                private_key=request.private_key,
                data=data,
                gas=request.gas,
                gas_price_wei=request.gas_price_wei,
            )
        )

    async def build_erc20_approve(self, request: Erc20ApproveRequest) -> TransactionDraft:
        decimals = request.decimals
        if decimals is None:
            decimals = (await self._client.erc20.info(request.token)).decimals
        amount_raw = _parse_units(request.amount, decimals)
        data = self._client.erc20.build_approve_data(request.token, request.spender, amount_raw)
        return await self.build_contract_call(
            ContractCallRequest(
                contract=request.token,
                private_key=request.private_key,
                data=data,
                gas=request.gas,
                gas_price_wei=request.gas_price_wei,
            )
        )

    async def build_erc20_transfer_from(self, request: Erc20TransferFromRequest) -> TransactionDraft:
        decimals = request.decimals
        if decimals is None:
            decimals = (await self._client.erc20.info(request.token)).decimals
        amount_raw = _parse_units(request.amount, decimals)
        data = self._client.erc20.build_transfer_from_data(
            request.token,
            request.owner,
            request.to,
            amount_raw,
        )
        return await self.build_contract_call(
            ContractCallRequest(
                contract=request.token,
                private_key=request.private_key,
                data=data,
                gas=request.gas,
                gas_price_wei=request.gas_price_wei,
            )
        )

    async def estimate(self, draft: TransactionDraft) -> TransactionDraft:
        estimated_gas = int(await self._client.estimate_gas(draft.tx))
        gas = _apply_gas_limit_multiplier(estimated_gas, _gas_limit_multiplier(self._client))
        draft.gas = int(gas)
        draft.tx["gas"] = int(gas)
        gas_price = int(draft.tx["gasPrice"])
        draft.gas_price_wei = gas_price
        draft.fee_wei = int(gas) * gas_price
        return draft

    async def preflight_fee(self, draft: TransactionDraft) -> FeePreflight:
        if draft.fee_wei is None:
            raise ValueError("Estimate transaction before fee preflight")
        balance = int(await self._client.balance_wei(draft.from_address))
        required = int(draft.value_wei) + int(draft.fee_wei)
        missing = max(0, required - balance)
        preflight = FeePreflight(
            ok=missing == 0,
            from_address=draft.from_address,
            native_balance_wei=balance,
            value_wei=int(draft.value_wei),
            fee_wei=int(draft.fee_wei),
            required_wei=required,
            missing_wei=missing,
            gas=draft.gas,
            gas_price_wei=draft.gas_price_wei,
        )
        draft.preflight = preflight
        return preflight

    async def calculate_fee(self, draft: TransactionDraft) -> FeePreflight:
        """Estimate gas/fee and check native DEL balance without signing."""
        if draft.gas is None and draft.tx.get("gas") is not None:
            draft.gas = int(draft.tx["gas"])
        if draft.fee_wei is None and draft.gas is None:
            draft = await self.estimate(draft)
        elif draft.fee_wei is None:
            gas_price = int(draft.tx["gasPrice"])
            draft.tx["gas"] = int(draft.gas)
            draft.gas_price_wei = gas_price
            draft.fee_wei = int(draft.gas) * gas_price
        return await self.preflight_fee(draft)

    async def estimate_fee_for_native_transfer(
        self,
        request: NativeTransferRequest,
    ) -> FeePreflight:
        draft = await self.build_native_transfer(request)
        return await self.calculate_fee(draft)

    async def estimate_fee_for_contract_call(
        self,
        request: ContractCallRequest,
    ) -> FeePreflight:
        draft = await self.build_contract_call(request)
        return await self.calculate_fee(draft)

    async def estimate_fee_for_erc20_transfer(
        self,
        request: Erc20TransferRequest,
    ) -> FeePreflight:
        draft = await self.build_erc20_transfer(request)
        return await self.calculate_fee(draft)

    async def estimate_fee_for_erc20_approve(
        self,
        request: Erc20ApproveRequest,
    ) -> FeePreflight:
        draft = await self.build_erc20_approve(request)
        return await self.calculate_fee(draft)

    async def estimate_fee_for_erc20_transfer_from(
        self,
        request: Erc20TransferFromRequest,
    ) -> FeePreflight:
        draft = await self.build_erc20_transfer_from(request)
        return await self.calculate_fee(draft)

    async def sign(self, draft: TransactionDraft, private_key: str) -> TransactionDraft:
        signable_tx = {key: value for key, value in draft.tx.items() if key != "from"}
        signed = Account.sign_transaction(signable_tx, normalize_private_key(private_key))
        raw = getattr(signed, "raw_transaction", None) or getattr(signed, "rawTransaction")
        draft.raw_tx = bytes(raw)
        return draft

    async def broadcast(self, draft: TransactionDraft) -> TransactionDraft:
        if draft.raw_tx is None:
            raise ValueError("Transaction must be signed before broadcast")
        tx_hash = await self._client.send_raw_transaction(draft.raw_tx)
        draft.tx_hash = _hex(tx_hash)
        return draft

    async def wait_receipt(
        self,
        draft: TransactionDraft,
        timeout_seconds: float = 1.0,
        poll_seconds: float = 0.2,
    ) -> TransactionDraft:
        if draft.tx_hash is None:
            raise ValueError("Transaction hash is required")
        deadline = asyncio.get_running_loop().time() + timeout_seconds
        while asyncio.get_running_loop().time() < deadline:
            receipt = await self._client.transaction_receipt(draft.tx_hash)
            if receipt is not None:
                draft.receipt = receipt
                return draft
            await asyncio.sleep(poll_seconds)
        return draft

    async def send_del(
        self,
        request: NativeTransferRequest,
        broadcast: bool = False,
        wait_receipt: bool = False,
    ) -> TransactionResult:
        try:
            draft = await self.build_native_transfer(request)
            native_balance = int(await self._client.balance_wei(draft.from_address))
            if int(draft.value_wei) > native_balance:
                return _native_value_preflight_failure(draft, native_balance)
            preflight = await self.calculate_fee(draft)
            if not preflight.ok:
                return _preflight_failure(draft, preflight)
            draft = await self.sign(draft, request.private_key)
            if broadcast:
                draft = await self.broadcast(draft)
                if wait_receipt:
                    timeout_seconds, poll_seconds = _receipt_wait_settings(self._client)
                    draft = await self.wait_receipt(
                        draft,
                        timeout_seconds=timeout_seconds,
                        poll_seconds=poll_seconds,
                    )
            return _result_from_draft(
                draft,
                preflight,
                broadcast=broadcast,
                native_balance_wei=preflight.native_balance_wei,
                required_wei=preflight.required_wei,
                missing_wei=preflight.missing_wei,
            )
        except Exception as exc:
            return _exception_failure(exc)

    async def send_erc20(
        self,
        request: Erc20TransferRequest,
        broadcast: bool = False,
        wait_receipt: bool = False,
    ) -> TransactionResult:
        try:
            decimals = request.decimals
            if decimals is None:
                decimals = (await self._client.erc20.info(request.token)).decimals
            amount_raw = _parse_units(request.amount, decimals)
            owner = private_key_to_address(request.private_key)
            balance = await self._client.erc20.balance(request.token, owner)
            if int(balance.raw) < amount_raw:
                return _token_preflight_failure(int(balance.raw), amount_raw)
            request = Erc20TransferRequest(
                token=request.token,
                to=request.to,
                amount=request.amount,
                private_key=request.private_key,
                decimals=decimals,
                gas=request.gas,
                gas_price_wei=request.gas_price_wei,
            )
            draft = await self.build_erc20_transfer(request)
            return await self.send_draft(draft, request.private_key, broadcast, wait_receipt)
        except Exception as exc:
            return _exception_failure(exc)

    async def approve_erc20(
        self,
        request: Erc20ApproveRequest,
        broadcast: bool = False,
        wait_receipt: bool = False,
    ) -> TransactionResult:
        try:
            draft = await self.build_erc20_approve(request)
            return await self.send_draft(draft, request.private_key, broadcast, wait_receipt)
        except Exception as exc:
            return _exception_failure(exc)

    async def transfer_from_erc20(
        self,
        request: Erc20TransferFromRequest,
        broadcast: bool = False,
        wait_receipt: bool = False,
    ) -> TransactionResult:
        try:
            decimals = request.decimals
            if decimals is None:
                decimals = (await self._client.erc20.info(request.token)).decimals
            amount_raw = _parse_units(request.amount, decimals)
            spender = private_key_to_address(request.private_key)
            balance = await self._client.erc20.balance(request.token, request.owner)
            if int(balance.raw) < amount_raw:
                return _token_preflight_failure(int(balance.raw), amount_raw)
            allowance = await self._client.erc20.allowance(request.token, request.owner, spender)
            if int(allowance) < amount_raw:
                return _allowance_preflight_failure(int(allowance), amount_raw)
            request = Erc20TransferFromRequest(
                token=request.token,
                owner=request.owner,
                to=request.to,
                amount=request.amount,
                private_key=request.private_key,
                decimals=decimals,
                gas=request.gas,
                gas_price_wei=request.gas_price_wei,
            )
            draft = await self.build_erc20_transfer_from(request)
            return await self.send_draft(draft, request.private_key, broadcast, wait_receipt)
        except Exception as exc:
            return _exception_failure(exc)

    async def send_draft(
        self,
        draft: TransactionDraft,
        private_key: str,
        broadcast: bool,
        wait_receipt: bool,
    ) -> TransactionResult:
        try:
            if not await self._contract_code_is_present(draft):
                return _missing_contract_code_failure(draft)
            preflight = await self.calculate_fee(draft)
            if not preflight.ok:
                return _preflight_failure(draft, preflight)
            draft = await self.sign(draft, private_key)
            if broadcast:
                draft = await self.broadcast(draft)
                if wait_receipt:
                    timeout_seconds, poll_seconds = _receipt_wait_settings(self._client)
                    draft = await self.wait_receipt(
                        draft,
                        timeout_seconds=timeout_seconds,
                        poll_seconds=poll_seconds,
                    )
            return _result_from_draft(
                draft,
                preflight,
                broadcast=broadcast,
                native_balance_wei=preflight.native_balance_wei,
                required_wei=preflight.required_wei,
                missing_wei=preflight.missing_wei,
            )
        except Exception as exc:
            return _exception_failure(exc)

    async def _contract_code_is_present(self, draft: TransactionDraft) -> bool:
        data = draft.tx.get("data")
        to_address = draft.tx.get("to")
        if not to_address or not data or data == "0x":
            return True
        rpc = getattr(self._client, "rpc", None)
        if rpc is None:
            return True
        try:
            code = await rpc.call(lambda w3: w3.eth.get_code(checksum(to_address)))
        except Exception:
            return True
        return bool(code)


def _hex(value: Any) -> str:
    if isinstance(value, HexBytes):
        return value.hex()
    if isinstance(value, bytes):
        return "0x" + value.hex()
    text = str(value)
    if len(text) == 64 and all(char in "0123456789abcdefABCDEF" for char in text):
        return "0x" + text
    return text


def _receipt_wait_settings(client) -> tuple[float, float]:
    safety = getattr(getattr(client, "config", None), "safety", None)
    timeout = getattr(safety, "receipt_wait_timeout_seconds", 7.0) or 7.0
    poll = getattr(safety, "receipt_poll_seconds", 3.0) or 3.0
    return float(timeout), float(poll)


def _receipt_get(receipt: dict[str, Any], *keys: str) -> Any:
    for key in keys:
        if key in receipt:
            return receipt[key]
    return None


def _int_or_none(value: Any) -> int | None:
    if value is None:
        return None
    if isinstance(value, HexBytes):
        return int(value.hex(), 16)
    if isinstance(value, bytes):
        return int.from_bytes(value, "big")
    if isinstance(value, str):
        return int(value, 16) if value.startswith("0x") else int(value)
    return int(value)


def _receipt_details(receipt: dict[str, Any] | None) -> dict[str, Any]:
    if not receipt:
        return {
            "status": None,
            "block_number": None,
            "transaction_index": None,
            "gas_used": None,
            "effective_gas_price_wei": None,
            "effective_fee_wei": None,
            "effective_fee_del": None,
        }
    raw_status = _int_or_none(_receipt_get(receipt, "status"))
    gas_used = _int_or_none(_receipt_get(receipt, "gasUsed", "gas_used"))
    effective_gas_price = _int_or_none(_receipt_get(receipt, "effectiveGasPrice", "effective_gas_price"))
    effective_fee = gas_used * effective_gas_price if gas_used is not None and effective_gas_price is not None else None
    return {
        "status": "success" if raw_status == 1 else "failed" if raw_status == 0 else None,
        "block_number": _int_or_none(_receipt_get(receipt, "blockNumber", "block_number")),
        "transaction_index": _int_or_none(_receipt_get(receipt, "transactionIndex", "transaction_index")),
        "gas_used": gas_used,
        "effective_gas_price_wei": effective_gas_price,
        "effective_fee_wei": effective_fee,
        "effective_fee_del": Decimal(effective_fee) / Decimal(10**18) if effective_fee is not None else None,
    }


def _result_from_draft(
    draft: TransactionDraft,
    preflight: FeePreflight,
    *,
    broadcast: bool,
    **kwargs,
) -> TransactionResult:
    details = _receipt_details(draft.receipt)
    effective_gas_price_wei = details["effective_gas_price_wei"]
    if effective_gas_price_wei is None and details["gas_used"] is not None:
        effective_gas_price_wei = draft.gas_price_wei
    effective_fee_wei = details["effective_fee_wei"]
    if effective_fee_wei is None and details["gas_used"] is not None and effective_gas_price_wei is not None:
        effective_fee_wei = int(details["gas_used"]) * int(effective_gas_price_wei)
    status = details["status"] or ("pending" if broadcast else "dry_run")
    success = status != "failed"
    return TransactionResult(
        success=success,
        tx_hash=draft.tx_hash,
        status=status,
        block_number=details["block_number"],
        transaction_index=details["transaction_index"],
        gas_used=details["gas_used"],
        effective_gas_price_wei=effective_gas_price_wei,
        effective_fee_wei=effective_fee_wei,
        effective_fee_del=Decimal(effective_fee_wei) / Decimal(10**18) if effective_fee_wei is not None else None,
        fee_wei=draft.fee_wei,
        fee_del=draft.fee_del,
        gas=draft.gas,
        raw_tx_hex="0x" + draft.raw_tx.hex() if draft.raw_tx else None,
        receipt=draft.receipt,
        **kwargs,
    )


def _preflight_failure(draft: TransactionDraft, preflight: FeePreflight) -> TransactionResult:
    user_message = (
        "Недостаточно DEL для суммы и комиссии."
        if int(draft.value_wei) > 0
        else "Недостаточно DEL для комиссии."
    )
    return TransactionResult(
        success=False,
        fee_wei=draft.fee_wei,
        fee_del=draft.fee_del,
        gas=draft.gas,
        error=(
            "Insufficient DEL for transaction value and fee: "
            f"balance={preflight.native_balance_del} DEL, "
            f"required={preflight.required_del} DEL, "
            f"missing={preflight.missing_del} DEL"
        ),
        user_message=user_message,
        native_balance_wei=preflight.native_balance_wei,
        required_wei=preflight.required_wei,
        missing_wei=preflight.missing_wei,
    )


def _native_value_preflight_failure(draft: TransactionDraft, native_balance_wei: int) -> TransactionResult:
    missing = max(0, int(draft.value_wei) - int(native_balance_wei))
    return TransactionResult(
        success=False,
        error=(
            "Insufficient DEL for transaction value: "
            f"balance={Decimal(native_balance_wei) / Decimal(10**18)} DEL, "
            f"required={Decimal(draft.value_wei) / Decimal(10**18)} DEL, "
            f"missing={Decimal(missing) / Decimal(10**18)} DEL"
        ),
        user_message="Недостаточно DEL на балансе.",
        native_balance_wei=int(native_balance_wei),
        required_wei=int(draft.value_wei),
        missing_wei=missing,
    )


def _missing_contract_code_failure(draft: TransactionDraft) -> TransactionResult:
    return TransactionResult(
        success=False,
        error=f"Contract address has no bytecode: {draft.to_address}",
        user_message="Контракт сети недоступен. Проверьте сеть или адрес контракта.",
    )


def _token_preflight_failure(balance_raw: int, required_raw: int) -> TransactionResult:
    missing = max(0, required_raw - balance_raw)
    return TransactionResult(
        success=False,
        error=(
            "Insufficient ERC20 token balance: "
            f"balance_raw={balance_raw}, required_raw={required_raw}, missing_raw={missing}"
        ),
        user_message="Недостаточно токенов на балансе.",
        token_balance_raw=balance_raw,
        token_required_raw=required_raw,
        token_missing_raw=missing,
    )


def _allowance_preflight_failure(allowance_raw: int, required_raw: int) -> TransactionResult:
    missing = max(0, required_raw - allowance_raw)
    return TransactionResult(
        success=False,
        error=(
            "Insufficient ERC20 allowance: "
            f"allowance_raw={allowance_raw}, required_raw={required_raw}, missing_raw={missing}"
        ),
        user_message="Нужно разрешение на списание токена.",
        token_allowance_raw=allowance_raw,
        token_allowance_required_raw=required_raw,
        token_allowance_missing_raw=missing,
    )


def _exception_failure(exc: Exception) -> TransactionResult:
    return TransactionResult(success=False, error=str(exc), user_message=user_message_from_error(str(exc)))


def user_message_from_error(error: str | None) -> str | None:
    if not error:
        return None
    lowered = error.lower()
    if "insufficient del" in lowered or "insufficient funds" in lowered:
        if "fee" in lowered or "gas" in lowered:
            return "Недостаточно DEL для комиссии."
        return "Недостаточно DEL на балансе."
    if "insufficient erc20 token balance" in lowered or "insufficient token" in lowered:
        return "Недостаточно токенов на балансе."
    if "insufficient erc20 allowance" in lowered or "allowance" in lowered:
        return "Нужно разрешение на списание токена."
    if "memo is not supported" in lowered:
        return "Memo не поддерживается для этого типа транзакции."
    if "all decimal web3 rpc endpoints failed" in lowered or "rpc" in lowered:
        return "Не удалось получить данные сети. Попробуйте позже."
    if "estimate gas" in lowered or "execution reverted" in lowered or "revert" in lowered:
        return "Транзакция не может быть выполнена. Проверьте данные и баланс."
    if "private key" in lowered or "mnemonic" in lowered:
        return "Ошибка доступа к кошельку."
    return "Не удалось выполнить транзакцию. Попробуйте позже."


def _parse_units(value: Decimal | str | int | float, decimals: int) -> int:
    return int(Decimal(str(value)) * (Decimal(10) ** int(decimals)))


def _gas_limit_multiplier(client) -> float:
    safety = getattr(getattr(client, "config", None), "safety", None)
    value = getattr(safety, "gas_limit_multiplier", 1.0)
    try:
        multiplier = float(value)
    except (TypeError, ValueError):
        return 1.0
    if multiplier < 1.0:
        return 1.0
    return multiplier


def _apply_gas_limit_multiplier(estimated_gas: int, multiplier: float) -> int:
    value = Decimal(int(estimated_gas)) * Decimal(str(multiplier))
    return int(value.to_integral_value(rounding=ROUND_CEILING))
