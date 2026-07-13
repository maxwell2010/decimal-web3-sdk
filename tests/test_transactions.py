from __future__ import annotations

from decimal import Decimal
from types import SimpleNamespace

import pytest

from decimal_web3_sdk import (
    AgentContext,
    AgentOrchestrator,
    BroadcastTransactionAgent,
    BuildNativeTransferAgent,
    ContractCallRequest,
    Erc20TransferFromRequest,
    EstimateGasAgent,
    NativeTransferRequest,
    ReceiptPollAgent,
    SignTransactionAgent,
    TransactionService,
    decode_memo_data,
    encode_memo_data,
    memo_supported_for,
)
from decimal_web3_sdk.transactions import _retry_gas_price_from_minimum_fee_error
from decimal_web3_sdk.limits import SafetyLimits
from decimal_web3_sdk.wallet import generate_mnemonic_account


PRIVATE_KEY = "0x" + "1" * 64
TO_ADDRESS = "0x" + "2" * 40
TEST_ACCOUNT = generate_mnemonic_account()
TEST_MNEMONIC = TEST_ACCOUNT.mnemonic or ""
TEST_MNEMONIC_PRIVATE_KEY = TEST_ACCOUNT.private_key


class FakeTxClient:
    def __init__(
        self,
        balance_wei: int = 10**21,
        token_balance_raw: int = 10**21,
        token_allowance_raw: int = 10**21,
        safety: SafetyLimits | None = None,
        gas_price_wei: int = 1_000_000_000,
    ) -> None:
        self.config = SimpleNamespace(chain_id=75, safety=safety)
        self.tx = TransactionService(self)
        self.sent_raw: bytes | None = None
        self.balance = balance_wei
        self.gas_price_wei = gas_price_wei
        self.estimate_calls = 0
        self.sent_raws: list[bytes] = []
        self.erc20 = SimpleNamespace(
            info=self._token_info,
            balance=self._token_balance,
            allowance=self._token_allowance,
            build_transfer_data=lambda token, to, amount_raw: "0xa9059cbb" + "00" * 64,
            build_transfer_from_data=lambda token, owner, to, amount_raw: "0x23b872dd" + "00" * 96,
        )
        self.token_balance_raw = token_balance_raw
        self.token_allowance_raw = token_allowance_raw
        self.rpc = None

    async def transaction_count(self, address: str) -> int:
        return 7

    async def gas_price(self) -> int:
        return self.gas_price_wei

    async def balance_wei(self, address: str) -> int:
        return self.balance

    async def estimate_gas(self, tx: dict) -> int:
        assert "value" in tx
        self.estimate_calls += 1
        return 21_000

    async def send_raw_transaction(self, raw_tx: bytes) -> str:
        self.sent_raw = raw_tx
        self.sent_raws.append(raw_tx)
        return "0x" + "a" * 64

    async def transaction_receipt(self, tx_hash: str) -> dict | None:
        return {"transactionHash": tx_hash, "status": 1}

    async def _token_info(self, token: str):
        return SimpleNamespace(decimals=18)

    async def _token_balance(self, token: str, owner: str):
        return SimpleNamespace(raw=self.token_balance_raw)

    async def _token_allowance(self, token: str, owner: str, spender: str) -> int:
        return self.token_allowance_raw


@pytest.mark.asyncio
async def test_send_del_dry_run_builds_signed_transaction() -> None:
    client = FakeTxClient()
    request = NativeTransferRequest(to=TO_ADDRESS, amount_del=Decimal("1"), private_key=PRIVATE_KEY)

    result = await client.tx.send_del(request, broadcast=False)

    assert result.success is True
    assert result.tx_hash is None
    assert result.gas == 21_000
    assert result.fee_wei == 21_000_000_000_000
    assert result.raw_tx_hex is not None
    assert result.native_balance_wei == 10**21
    assert result.required_wei == 1_000_021_000_000_000_000
    assert result.missing_wei == 0
    assert result.status == "dry_run"
    assert result.is_confirmed is False


@pytest.mark.asyncio
async def test_send_del_broadcast_result_exposes_receipt_summary() -> None:
    client = FakeTxClient()

    async def transaction_receipt(tx_hash: str) -> dict:
        return {
            "transactionHash": tx_hash,
            "status": 1,
            "blockNumber": 123,
            "transactionIndex": 4,
            "gasUsed": 21_000,
            "effectiveGasPrice": 1_000_000_000,
        }

    client.transaction_receipt = transaction_receipt  # type: ignore[method-assign]
    request = NativeTransferRequest(to=TO_ADDRESS, amount_del=Decimal("1"), private_key=PRIVATE_KEY)

    result = await client.tx.send_del(request, broadcast=True, wait_receipt=True)

    assert result.success is True
    assert result.status == "success"
    assert result.is_successful is True
    assert result.is_confirmed is True
    assert result.tx_hash == "0x" + "a" * 64
    assert result.block_number == 123
    assert result.transaction_index == 4
    assert result.gas_used == 21_000
    assert result.effective_gas_price_wei == 1_000_000_000
    assert result.effective_fee_wei == 21_000_000_000_000
    assert result.effective_fee_del == Decimal("0.000021")


@pytest.mark.asyncio
async def test_send_del_retries_with_minimum_global_fee_from_broadcast_error() -> None:
    client = FakeTxClient(gas_price_wei=2_380_950_000_000)
    attempts = 0

    async def send_raw_transaction(raw_tx: bytes) -> str:
        nonlocal attempts
        attempts += 1
        client.sent_raws.append(raw_tx)
        if attempts == 1:
            raise ValueError("provided fee 420000000000000 is less than minimum global fee 1000000000000000")
        return "0x" + "d" * 64

    client.send_raw_transaction = send_raw_transaction  # type: ignore[method-assign]
    request = NativeTransferRequest(to=TO_ADDRESS, amount_del=Decimal("1"), private_key=PRIVATE_KEY)

    result = await client.tx.send_del(request, broadcast=True, wait_receipt=False)

    assert result.success is True
    assert result.tx_hash == "0x" + "d" * 64
    assert attempts == 2
    assert len(client.sent_raws) == 2
    assert result.gas == 21_000
    assert result.fee_wei == 1_000_000_000_020_000
    assert result.fee_del == Decimal("0.00100000000002")
    assert result.required_wei == 1_001_000_000_000_020_000


@pytest.mark.asyncio
async def test_send_del_does_not_block_minimum_global_fee_above_local_cap() -> None:
    client = FakeTxClient(gas_price_wei=2_380_950_000_000)
    attempts = 0

    async def send_raw_transaction(raw_tx: bytes) -> str:
        nonlocal attempts
        attempts += 1
        client.sent_raws.append(raw_tx)
        if attempts == 1:
            raise ValueError("minimum global fee too high: 0.180144 DEL > limit 0.020000 DEL")
        return "0x" + "f" * 64

    client.send_raw_transaction = send_raw_transaction  # type: ignore[method-assign]
    request = NativeTransferRequest(to=TO_ADDRESS, amount_del=Decimal("1"), private_key=PRIVATE_KEY, gas=100_000)

    result = await client.tx.send_del(request, broadcast=True, wait_receipt=False)

    assert result.success is True
    assert result.tx_hash == "0x" + "f" * 64
    assert attempts == 2
    assert result.gas == 100_000
    assert result.fee_wei == 180_144_000_000_000_000
    assert result.fee_del == Decimal("0.180144")
    assert result.required_wei == 1_180_144_000_000_000_000


def test_minimum_global_fee_retry_parser() -> None:
    assert (
        _retry_gas_price_from_minimum_fee_error(
            "provided fee 420000000000000 is less than minimum global fee 1000000000000000",
            21_000,
        )
        == 47_619_047_620
    )
    assert (
        _retry_gas_price_from_minimum_fee_error("minimum global fee: 0.002 DEL", 100_000)
        == 20_000_000_000
    )
    assert (
        _retry_gas_price_from_minimum_fee_error(
            "minimum global fee too high: 0.180144 DEL > limit 0.020000 DEL",
            100_000,
        )
        == 1_801_440_000_000
    )
    assert _retry_gas_price_from_minimum_fee_error("insufficient funds", 21_000) is None


@pytest.mark.asyncio
async def test_broadcast_normalizes_hash_without_prefix() -> None:
    client = FakeTxClient()

    async def send_raw_transaction(raw_tx: bytes) -> str:
        return "a" * 64

    client.send_raw_transaction = send_raw_transaction  # type: ignore[method-assign]
    request = NativeTransferRequest(to=TO_ADDRESS, amount_del=Decimal("1"), private_key=PRIVATE_KEY)

    result = await client.tx.send_del(request, broadcast=True)

    assert result.tx_hash == "0x" + "a" * 64


@pytest.mark.asyncio
async def test_contract_call_to_empty_address_fails_before_signing() -> None:
    class EmptyCodeRpc:
        async def call(self, fn):
            return b""

    client = FakeTxClient()
    client.rpc = EmptyCodeRpc()
    request = ContractCallRequest(
        contract=TO_ADDRESS,
        private_key=PRIVATE_KEY,
        data="0x12345678",
    )

    draft = await client.tx.build_contract_call(request)
    result = await client.tx.send_draft(draft, PRIVATE_KEY, broadcast=True, wait_receipt=False)

    assert result.success is False
    assert result.raw_tx_hex is None
    assert client.sent_raw is None
    assert result.user_message == "Контракт сети недоступен. Проверьте сеть или адрес контракта."


@pytest.mark.asyncio
async def test_send_del_broadcast_uses_draft_gas_price_when_receipt_has_no_effective_price() -> None:
    client = FakeTxClient()

    async def transaction_receipt(tx_hash: str) -> dict:
        return {
            "transactionHash": tx_hash,
            "status": 1,
            "blockNumber": 123,
            "transactionIndex": 4,
            "gasUsed": 21_000,
        }

    client.transaction_receipt = transaction_receipt  # type: ignore[method-assign]
    request = NativeTransferRequest(to=TO_ADDRESS, amount_del=Decimal("1"), private_key=PRIVATE_KEY)

    result = await client.tx.send_del(request, broadcast=True, wait_receipt=True)

    assert result.status == "success"
    assert result.effective_gas_price_wei == 1_000_000_000
    assert result.effective_fee_wei == 21_000_000_000_000
    assert result.effective_fee_del == Decimal("0.000021")


@pytest.mark.asyncio
async def test_send_del_broadcast_without_receipt_is_pending() -> None:
    client = FakeTxClient()

    async def transaction_receipt(tx_hash: str) -> None:
        return None

    client.transaction_receipt = transaction_receipt  # type: ignore[method-assign]
    request = NativeTransferRequest(to=TO_ADDRESS, amount_del=Decimal("1"), private_key=PRIVATE_KEY)

    result = await client.tx.send_del(request, broadcast=True, wait_receipt=True)

    assert result.success is True
    assert result.status == "pending"
    assert result.is_pending is True
    assert result.tx_hash == "0x" + "a" * 64
    assert result.block_number is None


@pytest.mark.asyncio
async def test_send_del_wait_receipt_uses_configured_timeout() -> None:
    client = FakeTxClient(safety=SafetyLimits(receipt_wait_timeout_seconds=7, receipt_poll_seconds=2))
    seen: dict[str, float] = {}
    original_wait = client.tx.wait_receipt

    async def wait_receipt(draft, timeout_seconds: float = 1.0, poll_seconds: float = 0.2):
        seen["timeout"] = timeout_seconds
        seen["poll"] = poll_seconds
        return await original_wait(draft, timeout_seconds=timeout_seconds, poll_seconds=poll_seconds)

    client.tx.wait_receipt = wait_receipt  # type: ignore[method-assign]
    request = NativeTransferRequest(to=TO_ADDRESS, amount_del=Decimal("1"), private_key=PRIVATE_KEY)

    await client.tx.send_del(request, broadcast=True, wait_receipt=True)

    assert seen == {"timeout": 7, "poll": 2}


def test_native_transfer_request_can_be_created_from_mnemonic() -> None:
    request = NativeTransferRequest.from_mnemonic(
        to=TO_ADDRESS,
        amount_del="1",
        mnemonic=TEST_MNEMONIC,
    )

    assert request.private_key == TEST_MNEMONIC_PRIVATE_KEY
    assert request.to == TO_ADDRESS


@pytest.mark.asyncio
async def test_native_transfer_memo_is_utf8_transaction_data() -> None:
    client = FakeTxClient()
    request = NativeTransferRequest(
        to=TO_ADDRESS,
        amount_del="1",
        private_key=PRIVATE_KEY,
        memo="optional",
    )

    draft = await client.tx.build_native_transfer(request)

    assert draft.tx["data"] == encode_memo_data("optional")
    assert decode_memo_data(draft.tx["data"]) == "optional"


def test_memo_support_matrix_matches_transaction_types() -> None:
    assert memo_supported_for("native_del_transfer") is True
    assert memo_supported_for("send-del") is True
    assert memo_supported_for("multisend_del") is True
    assert memo_supported_for("multisend_erc20") is True
    assert memo_supported_for("multisend-erc20") is True
    assert memo_supported_for("erc20_transfer") is False
    assert memo_supported_for("contract_call") is False


def test_decode_memo_data_rejects_non_utf8_payload() -> None:
    with pytest.raises(ValueError, match="UTF-8 memo"):
        decode_memo_data("0xff")


def test_erc20_transfer_request_can_be_created_from_mnemonic() -> None:
    from decimal_web3_sdk import Erc20TransferRequest

    request = Erc20TransferRequest.from_mnemonic(
        token=TO_ADDRESS,
        to=TO_ADDRESS,
        amount="1",
        mnemonic=TEST_MNEMONIC,
        decimals=18,
    )

    assert request.private_key == TEST_MNEMONIC_PRIVATE_KEY
    assert request.decimals == 18


def test_contract_call_request_can_be_created_from_mnemonic() -> None:
    request = ContractCallRequest.from_mnemonic(
        contract=TO_ADDRESS,
        data="0x12345678",
        mnemonic=TEST_MNEMONIC,
        value_wei=123,
    )

    assert request.private_key == TEST_MNEMONIC_PRIVATE_KEY
    assert request.value_wei == 123


@pytest.mark.asyncio
async def test_calculate_fee_estimates_without_signing() -> None:
    client = FakeTxClient()
    request = NativeTransferRequest(to=TO_ADDRESS, amount_del=Decimal("1"), private_key=PRIVATE_KEY)

    draft = await client.tx.build_native_transfer(request)
    quote = await client.tx.calculate_fee(draft)

    assert quote.ok is True
    assert quote.gas == 21_000
    assert quote.gas_price_wei == 1_000_000_000
    assert quote.fee_wei == 21_000_000_000_000
    assert quote.required_wei == 1_000_021_000_000_000_000
    assert draft.raw_tx is None
    assert client.sent_raw is None


@pytest.mark.asyncio
async def test_calculate_fee_reports_missing_del_without_signing() -> None:
    client = FakeTxClient(balance_wei=1)
    request = NativeTransferRequest(to=TO_ADDRESS, amount_del=Decimal("1"), private_key=PRIVATE_KEY)

    quote = await client.tx.estimate_fee_for_native_transfer(request)

    assert quote.ok is False
    assert quote.missing_wei == 1_000_020_999_999_999_999
    assert quote.fee_del == Decimal("0.000021")
    assert client.sent_raw is None


@pytest.mark.asyncio
async def test_calculate_fee_applies_configured_gas_limit_multiplier() -> None:
    client = FakeTxClient(safety=SafetyLimits(gas_limit_multiplier=1.10))
    request = NativeTransferRequest(to=TO_ADDRESS, amount_del=Decimal("1"), private_key=PRIVATE_KEY)

    quote = await client.tx.estimate_fee_for_native_transfer(request)

    assert quote.gas == 23_100
    assert quote.fee_wei == 23_100_000_000_000


@pytest.mark.asyncio
async def test_calculate_fee_uses_explicit_gas_without_estimating() -> None:
    client = FakeTxClient()
    request = NativeTransferRequest(
        to=TO_ADDRESS,
        amount_del=Decimal("1"),
        private_key=PRIVATE_KEY,
        gas=30_000,
    )

    quote = await client.tx.estimate_fee_for_native_transfer(request)

    assert quote.gas == 30_000
    assert quote.fee_wei == 30_000_000_000_000
    assert client.estimate_calls == 0


@pytest.mark.asyncio
async def test_calculate_fee_caps_network_gas_price_by_default() -> None:
    client = FakeTxClient(gas_price_wei=2_380_950_000_000)
    request = NativeTransferRequest(
        to=TO_ADDRESS,
        amount_del=Decimal("1"),
        private_key=PRIVATE_KEY,
    )

    quote = await client.tx.estimate_fee_for_native_transfer(request)

    assert quote.oracle_gas_price_wei == 2_380_950_000_000
    assert quote.gas_price_wei == 20_000_000_000
    assert quote.minimum_fee_wei == 420_000_000_000_000
    assert quote.minimum_fee_del == Decimal("0.00042")


@pytest.mark.asyncio
async def test_calculate_fee_caps_user_gas_price_when_above_limit() -> None:
    client = FakeTxClient(gas_price_wei=2_000_000_000)
    request = NativeTransferRequest(
        to=TO_ADDRESS,
        amount_del=Decimal("1"),
        private_key=PRIVATE_KEY,
        gas_price_wei=50_000_000_000,
    )

    quote = await client.tx.estimate_fee_for_native_transfer(request)

    assert quote.oracle_gas_price_wei == 2_000_000_000
    assert quote.gas_price_wei == 20_000_000_000
    assert quote.minimum_fee_wei == 420_000_000_000_000


@pytest.mark.asyncio
async def test_calculate_fee_can_disable_gas_price_cap() -> None:
    client = FakeTxClient(
        gas_price_wei=2_380_950_000_000,
        safety=SafetyLimits(max_gas_price_wei=None),
    )
    request = NativeTransferRequest(to=TO_ADDRESS, amount_del=Decimal("1"), private_key=PRIVATE_KEY)

    quote = await client.tx.estimate_fee_for_native_transfer(request)

    assert quote.oracle_gas_price_wei == 2_380_950_000_000
    assert quote.gas_price_wei == 2_380_950_000_000


@pytest.mark.asyncio
async def test_transaction_agent_pipeline_broadcasts_and_polls_receipt() -> None:
    client = FakeTxClient()
    request = NativeTransferRequest(to=TO_ADDRESS, amount_del="1", private_key=PRIVATE_KEY)
    context = AgentContext(client=client, data={"request": request})
    orchestrator = AgentOrchestrator(
        [
            BuildNativeTransferAgent(),
            EstimateGasAgent(),
            SignTransactionAgent(),
            BroadcastTransactionAgent(),
            ReceiptPollAgent(),
        ],
        default_timeout_seconds=1,
    )

    result = await orchestrator.run_sequential(context)
    draft = context.data["draft"]

    assert result.success is True
    assert draft.tx_hash == "0x" + "a" * 64
    assert draft.receipt == {"transactionHash": draft.tx_hash, "status": 1}
    assert client.sent_raw is not None


@pytest.mark.asyncio
async def test_transaction_agent_pipeline_retries_minimum_global_fee() -> None:
    client = FakeTxClient(gas_price_wei=2_380_950_000_000)
    attempts = 0

    async def send_raw_transaction(raw_tx: bytes) -> str:
        nonlocal attempts
        attempts += 1
        client.sent_raws.append(raw_tx)
        if attempts == 1:
            raise ValueError("provided fee 420000000000000 is less than minimum global fee 1000000000000000")
        return "0x" + "e" * 64

    client.send_raw_transaction = send_raw_transaction  # type: ignore[method-assign]
    request = NativeTransferRequest(to=TO_ADDRESS, amount_del="1", private_key=PRIVATE_KEY)
    context = AgentContext(client=client, data={"request": request})
    orchestrator = AgentOrchestrator(
        [
            BuildNativeTransferAgent(),
            EstimateGasAgent(),
            SignTransactionAgent(),
            BroadcastTransactionAgent(),
        ],
        default_timeout_seconds=1,
    )

    result = await orchestrator.run_sequential(context)
    draft = context.data["draft"]

    assert result.success is True
    assert attempts == 2
    assert draft.tx_hash == "0x" + "e" * 64
    assert draft.gas_price_wei == 47_619_047_620
    assert draft.fee_wei == 1_000_000_000_020_000


@pytest.mark.asyncio
async def test_contract_call_dry_run_uses_explicit_calldata() -> None:
    client = FakeTxClient()
    request = ContractCallRequest(
        contract=TO_ADDRESS,
        private_key=PRIVATE_KEY,
        data="0x12345678",
    )

    draft = await client.tx.build_contract_call(request)
    result = await client.tx.send_draft(draft, PRIVATE_KEY, broadcast=False, wait_receipt=False)

    assert result.success is True
    assert draft.tx["to"] == TO_ADDRESS
    assert draft.tx["data"] == "0x12345678"
    assert result.raw_tx_hex is not None


@pytest.mark.asyncio
async def test_send_del_stops_before_sign_when_native_balance_cannot_cover_fee() -> None:
    client = FakeTxClient(balance_wei=1)
    request = NativeTransferRequest(to=TO_ADDRESS, amount_del=Decimal("1"), private_key=PRIVATE_KEY)

    result = await client.tx.send_del(request, broadcast=True)

    assert result.success is False
    assert "Insufficient DEL" in str(result.error)
    assert result.user_message == "Недостаточно DEL на балансе."
    assert result.raw_tx_hex is None
    assert result.missing_wei is not None
    assert client.estimate_calls == 0
    assert client.sent_raw is None


@pytest.mark.asyncio
async def test_send_erc20_stops_before_estimate_when_token_balance_is_low() -> None:
    client = FakeTxClient(token_balance_raw=1)

    from decimal_web3_sdk import Erc20TransferRequest

    result = await client.tx.send_erc20(
        Erc20TransferRequest(
            token=TO_ADDRESS,
            to=TO_ADDRESS,
            amount=Decimal("1"),
            private_key=PRIVATE_KEY,
            decimals=18,
        ),
        broadcast=True,
    )

    assert result.success is False
    assert "Insufficient ERC20" in str(result.error)
    assert result.user_message == "Недостаточно токенов на балансе."
    assert result.token_balance_raw == 1
    assert result.token_required_raw == 10**18
    assert client.sent_raw is None


@pytest.mark.asyncio
async def test_transfer_from_erc20_dry_run_checks_balance_and_allowance() -> None:
    client = FakeTxClient()

    result = await client.tx.transfer_from_erc20(
        Erc20TransferFromRequest(
            token=TO_ADDRESS,
            owner="0x" + "3" * 40,
            to=TO_ADDRESS,
            amount=Decimal("1"),
            private_key=PRIVATE_KEY,
            decimals=18,
        ),
        broadcast=False,
    )

    assert result.success is True
    assert result.gas == 21_000
    assert result.raw_tx_hex is not None


@pytest.mark.asyncio
async def test_transfer_from_erc20_stops_when_allowance_is_low() -> None:
    client = FakeTxClient(token_allowance_raw=1)

    result = await client.tx.transfer_from_erc20(
        Erc20TransferFromRequest(
            token=TO_ADDRESS,
            owner="0x" + "3" * 40,
            to=TO_ADDRESS,
            amount=Decimal("1"),
            private_key=PRIVATE_KEY,
            decimals=18,
        ),
        broadcast=True,
    )

    assert result.success is False
    assert "Insufficient ERC20 allowance" in str(result.error)
    assert result.user_message == "Нужно разрешение на списание токена."
    assert result.token_allowance_raw == 1
    assert result.token_allowance_required_raw == 10**18
    assert client.sent_raw is None
