from __future__ import annotations

from dataclasses import dataclass
from types import SimpleNamespace

import pytest
from web3 import Web3

from decimal_web3_sdk import (
    DelegateDelRequest,
    DelegateErc20Request,
    HoldDelRequest,
    HoldErc20Request,
    HoldStakeWithResetRequest,
    MultisendDelRequest,
    MultisendErc20Recipient,
    MultisendErc20Request,
    MultisendRecipient,
    ResetStakeHoldRequest,
    StakeTokenToHoldRequest,
    TransferStakeErc20Request,
    TransferStakeWithResetRequest,
    UnbondDelRequest,
    UnbondErc20Request,
    ValidatorPauseRequest,
    ValidatorSelfPauseRequest,
    WithdrawStakeWithResetRequest,
    WithdrawHoldErc20Request,
)
from decimal_web3_sdk.decimal import DecimalService
from decimal_web3_sdk.transactions import TransactionResult, TransactionService


PRIVATE_KEY = "0x" + "1" * 64
VALIDATOR = "0x" + "3" * 40
RECIPIENT = "0x" + "4" * 40
TOKEN = "0x" + "5" * 40


class FakeDecimalClient:
    def __init__(
        self,
        balance_wei: int = 10**21,
        token_balance_raw: int = 10**21,
        allowance_raw: int = 10**21,
    ) -> None:
        self.web3 = Web3()
        self.config = SimpleNamespace(
            chain_id=75,
            contracts=SimpleNamespace(
                delegation="0xa16c34ed1c0601c0e749e17ebef19752a15faa01",
                del_token="0x16049a46126d69211de7c042465122badefa360c",
                master_validator="0x630B03FF9EeD4C4A468dA9f481DF23F542070Aa4",
                multicall="0x7b23eb47587ca6482fc16cb3d9d426ec64d4b5fc",
            ),
        )
        self.tx = TransactionService(self)
        self.balance = balance_wei
        self.token_balance_raw = token_balance_raw
        self.allowance_raw = allowance_raw
        self.erc20 = SimpleNamespace(
            info=self._token_info,
            balance=self._token_balance,
            allowance=self._allowance,
            permit_signature=self._permit_signature,
            build_approve_data=lambda token, spender, amount_raw: "0x095ea7b3" + "00" * 64,
            build_permit_data=lambda token, owner, spender, value, permit: "0xd505accf" + "00" * 64,
            build_transfer_from_data=lambda token, owner, to, amount_raw: "0x23b872dd" + "00" * 96,
        )
        self.permit = None

    async def transaction_count(self, address: str) -> int:
        return 1

    async def gas_price(self) -> int:
        return 1_000_000_000

    async def estimate_gas(self, tx: dict) -> int:
        assert tx["data"].startswith("0x")
        return 100_000

    async def balance_wei(self, address: str) -> int:
        return self.balance

    async def send_raw_transaction(self, raw_tx: bytes) -> str:
        return "0x" + "b" * 64

    async def transaction_receipt(self, tx_hash: str) -> dict | None:
        return None

    async def _token_info(self, token: str):
        return SimpleNamespace(decimals=18)

    async def _token_balance(self, token: str, owner: str):
        return SimpleNamespace(raw=self.token_balance_raw)

    async def _allowance(self, token: str, owner: str, spender: str):
        return self.allowance_raw

    async def _permit_signature(self, *args):
        return self.permit


@dataclass(frozen=True)
class FakePermit:
    deadline: int = 2**256 - 1
    v: int = 27
    r: bytes = b"\x01" * 32
    s: bytes = b"\x02" * 32


@pytest.mark.asyncio
async def test_delegate_del_dry_run_checks_value_plus_fee() -> None:
    client = FakeDecimalClient()
    service = DecimalService(client)

    result = await service.delegate_del(
        DelegateDelRequest(validator=VALIDATOR, amount_del="1", private_key=PRIVATE_KEY)
    )

    assert result.success is True
    assert result.required_wei == 1_000_100_000_000_000_000
    assert result.raw_tx_hex is not None


@pytest.mark.asyncio
async def test_delegate_del_reports_insufficient_fee_before_signing() -> None:
    client = FakeDecimalClient(balance_wei=1)
    service = DecimalService(client)

    result = await service.delegate_del(
        DelegateDelRequest(validator=VALIDATOR, amount_del="1", private_key=PRIVATE_KEY),
        broadcast=True,
    )

    assert result.success is False
    assert "Insufficient DEL" in str(result.error)
    assert result.raw_tx_hex is None


@pytest.mark.asyncio
async def test_hold_and_unbond_del_build_transactions() -> None:
    client = FakeDecimalClient()
    service = DecimalService(client)

    hold = await service.hold_del(
        HoldDelRequest(validator=VALIDATOR, amount_del="0.5", hold_timestamp=123, private_key=PRIVATE_KEY)
    )
    unbond = await service.unbond_del(
        UnbondDelRequest(validator=VALIDATOR, amount_del="0.5", private_key=PRIVATE_KEY)
    )

    assert hold.success is True
    assert unbond.success is True


@pytest.mark.asyncio
async def test_multisend_del_builds_total_value_preflight() -> None:
    client = FakeDecimalClient()
    service = DecimalService(client)

    result = await service.multisend_del(
        MultisendDelRequest(
            recipients=[MultisendRecipient(to=RECIPIENT, amount_del="0.1")],
            private_key=PRIVATE_KEY,
            memo="hello",
        )
    )

    assert result.success is True
    assert result.required_wei == 100_100_000_000_000_000


@pytest.mark.asyncio
async def test_delegate_erc20_uses_single_step_when_allowance_is_enough() -> None:
    client = FakeDecimalClient(allowance_raw=10**21)
    service = DecimalService(client)

    result = await service.delegate_erc20(
        DelegateErc20Request(
            token=TOKEN,
            validator=VALIDATOR,
            amount="1",
            private_key=PRIVATE_KEY,
            decimals=18,
        )
    )

    assert result.success is True
    assert result.steps == ("delegate_erc20",)
    assert result.extra_steps_required is False


@pytest.mark.asyncio
async def test_delegate_erc20_plans_approve_when_allowance_is_low() -> None:
    client = FakeDecimalClient(allowance_raw=0)
    service = DecimalService(client)

    result = await service.delegate_erc20(
        DelegateErc20Request(
            token=TOKEN,
            validator=VALIDATOR,
            amount="1",
            private_key=PRIVATE_KEY,
            decimals=18,
        )
    )

    assert result.success is True
    assert result.steps == ("approve_erc20", "delegate_erc20")
    assert result.actual_steps == 2
    assert result.extra_steps_required is True
    assert result.requires_secondary_transaction is True
    assert result.one_transaction is False
    assert result.transaction_count == 2
    assert result.total_fee_del is not None


@pytest.mark.asyncio
async def test_delegate_erc20_uses_permit_when_available() -> None:
    client = FakeDecimalClient(allowance_raw=0)
    client.permit = FakePermit()
    service = DecimalService(client)

    result = await service.delegate_erc20(
        DelegateErc20Request(
            token=TOKEN,
            validator=VALIDATOR,
            amount="1",
            private_key=PRIVATE_KEY,
            decimals=18,
        )
    )

    assert result.success is True
    assert result.steps == ("delegate_erc20_by_permit",)
    assert result.actual_steps == 1
    assert result.extra_steps_required is False
    assert result.requires_secondary_transaction is False
    assert result.one_transaction is True
    assert result.transaction_count == 1


@pytest.mark.asyncio
async def test_delegate_erc20_reports_insufficient_token_balance() -> None:
    client = FakeDecimalClient(token_balance_raw=1, allowance_raw=10**21)
    service = DecimalService(client)

    result = await service.delegate_erc20(
        DelegateErc20Request(
            token=TOKEN,
            validator=VALIDATOR,
            amount="1",
            private_key=PRIVATE_KEY,
            decimals=18,
        )
    )

    assert result.success is False
    assert "Insufficient ERC20" in str(result.error)
    assert result.actual_steps == 0


@pytest.mark.asyncio
async def test_hold_erc20_plans_approve_when_allowance_is_low() -> None:
    client = FakeDecimalClient(allowance_raw=0)
    service = DecimalService(client)

    result = await service.hold_erc20(
        HoldErc20Request(
            token=TOKEN,
            validator=VALIDATOR,
            amount="1",
            hold_timestamp=123,
            private_key=PRIVATE_KEY,
            decimals=18,
        )
    )

    assert result.success is True
    assert result.steps == ("approve_erc20", "hold_erc20")
    assert result.extra_steps_required is True


@pytest.mark.asyncio
async def test_hold_erc20_uses_permit_when_available() -> None:
    client = FakeDecimalClient(allowance_raw=0)
    client.permit = FakePermit()
    service = DecimalService(client)

    result = await service.hold_erc20(
        HoldErc20Request(
            token=TOKEN,
            validator=VALIDATOR,
            amount="1",
            hold_timestamp=123,
            private_key=PRIVATE_KEY,
            decimals=18,
        )
    )

    assert result.success is True
    assert result.steps == ("hold_erc20_by_permit",)
    assert result.actual_steps == 1


@pytest.mark.asyncio
async def test_multisend_erc20_single_step_when_allowance_is_enough() -> None:
    client = FakeDecimalClient(allowance_raw=10**21)
    service = DecimalService(client)

    result = await service.multisend_erc20(
        MultisendErc20Request(
            token=TOKEN,
            recipients=[MultisendErc20Recipient(to=RECIPIENT, amount="1")],
            private_key=PRIVATE_KEY,
            decimals=18,
        )
    )

    assert result.success is True
    assert result.steps == ("multisend_erc20",)
    assert result.extra_steps_required is False


@pytest.mark.asyncio
async def test_multisend_erc20_adds_memo_as_final_aggregate_call() -> None:
    client = FakeDecimalClient(allowance_raw=10**21)
    service = DecimalService(client)
    captured: dict[str, str] = {}

    async def capture_send_contract(private_key, contract, data, value_wei, broadcast, wait_receipt):
        captured["data"] = data
        return TransactionResult(success=True, status="dry_run", gas=100_000, fee_wei=100_000_000_000_000)

    service._send_contract = capture_send_contract

    result = await service.multisend_erc20(
        MultisendErc20Request(
            token=TOKEN,
            recipients=[MultisendErc20Recipient(to=RECIPIENT, amount="1")],
            private_key=PRIVATE_KEY,
            decimals=18,
            memo="hello",
        )
    )

    assert result.success is True
    assert result.steps == ("multisend_erc20",)
    decoded = service._multicall_contract().decode_function_input(captured["data"])[1]["calls"]
    assert decoded[-1]["target"] == "0x0000000000000000000000000000000000000000"
    assert decoded[-1]["value"] == 0
    assert decoded[-1]["callData"] == b"hello"


@pytest.mark.asyncio
async def test_multisend_erc20_uses_permit_inside_aggregate() -> None:
    client = FakeDecimalClient(allowance_raw=0)
    client.permit = FakePermit()
    service = DecimalService(client)

    result = await service.multisend_erc20(
        MultisendErc20Request(
            token=TOKEN,
            recipients=[MultisendErc20Recipient(to=RECIPIENT, amount="1")],
            private_key=PRIVATE_KEY,
            decimals=18,
        )
    )

    assert result.success is True
    assert result.steps == ("permit_erc20", "multisend_erc20")
    assert result.actual_steps == 2
    assert result.extra_steps_required is False


@pytest.mark.asyncio
async def test_multisend_erc20_falls_back_to_approve_when_permit_missing() -> None:
    client = FakeDecimalClient(allowance_raw=0)
    service = DecimalService(client)

    result = await service.multisend_erc20(
        MultisendErc20Request(
            token=TOKEN,
            recipients=[MultisendErc20Recipient(to=RECIPIENT, amount="1")],
            private_key=PRIVATE_KEY,
            decimals=18,
        )
    )

    assert result.success is True
    assert result.steps == ("approve_erc20", "multisend_erc20")
    assert result.extra_steps_required is True


@pytest.mark.asyncio
async def test_unbond_and_withdraw_hold_erc20_build_single_step() -> None:
    client = FakeDecimalClient()
    service = DecimalService(client)

    unbond = await service.unbond_erc20(
        UnbondErc20Request(token=TOKEN, validator=VALIDATOR, amount="1", private_key=PRIVATE_KEY, decimals=18)
    )
    withdraw = await service.withdraw_hold_erc20(
        WithdrawHoldErc20Request(
            token=TOKEN,
            validator=VALIDATOR,
            amount="1",
            hold_timestamp=123,
            private_key=PRIVATE_KEY,
            decimals=18,
        )
    )

    assert unbond.success is True
    assert unbond.steps == ("unbond_erc20",)
    assert withdraw.success is True
    assert withdraw.steps == ("withdraw_hold_erc20",)


@pytest.mark.asyncio
async def test_transfer_stake_erc20_builds_single_step() -> None:
    client = FakeDecimalClient()
    service = DecimalService(client)

    result = await service.transfer_stake_erc20(
        TransferStakeErc20Request(
            token=TOKEN,
            validator=VALIDATOR,
            new_validator=RECIPIENT,
            amount="1",
            private_key=PRIVATE_KEY,
            decimals=18,
        )
    )

    assert result.success is True
    assert result.steps == ("transfer_stake_erc20",)


@pytest.mark.asyncio
async def test_transfer_hold_stake_erc20_builds_single_step() -> None:
    service = DecimalService(FakeDecimalClient())

    result = await service.transfer_stake_erc20(
        TransferStakeErc20Request(
            token=TOKEN,
            validator=VALIDATOR,
            new_validator=RECIPIENT,
            amount="1",
            hold_timestamp=123,
            private_key=PRIVATE_KEY,
            decimals=18,
        )
    )

    assert result.success is True
    assert result.steps == ("transfer_hold_stake_erc20",)


@pytest.mark.asyncio
async def test_stake_hold_reset_workflows_build_transactions() -> None:
    service = DecimalService(FakeDecimalClient())

    to_hold = await service.stake_token_to_hold(
        StakeTokenToHoldRequest(
            token=TOKEN,
            validator=VALIDATOR,
            amount="1",
            old_hold_timestamp=111,
            new_hold_timestamp=222,
            private_key=PRIVATE_KEY,
            decimals=18,
        )
    )
    reset = await service.reset_stake_hold(
        ResetStakeHoldRequest(
            validator=VALIDATOR,
            delegator=RECIPIENT,
            token=TOKEN,
            hold_timestamp=111,
            private_key=PRIVATE_KEY,
        )
    )
    reset_del = await service.reset_stake_hold(
        ResetStakeHoldRequest(
            validator=VALIDATOR,
            delegator=RECIPIENT,
            hold_timestamp=111,
            private_key=PRIVATE_KEY,
        )
    )

    assert to_hold.success is True
    assert reset.success is True
    assert reset_del.success is True


@pytest.mark.asyncio
async def test_with_reset_stake_workflows_build_transactions() -> None:
    service = DecimalService(FakeDecimalClient())

    withdraw = await service.withdraw_stake_with_reset(
        WithdrawStakeWithResetRequest(
            token=TOKEN,
            validator=VALIDATOR,
            amount="1",
            hold_timestamps_to_reset=[1, 2],
            private_key=PRIVATE_KEY,
            decimals=18,
        )
    )
    transfer = await service.transfer_stake_with_reset(
        TransferStakeWithResetRequest(
            token=TOKEN,
            old_validator=VALIDATOR,
            new_validator=RECIPIENT,
            amount="1",
            hold_timestamps_to_reset=[1, 2],
            private_key=PRIVATE_KEY,
            decimals=18,
        )
    )
    hold = await service.hold_stake_with_reset(
        HoldStakeWithResetRequest(
            token=TOKEN,
            validator=VALIDATOR,
            amount="1",
            new_hold_timestamp=333,
            hold_timestamps_to_reset=[1, 2],
            private_key=PRIVATE_KEY,
            decimals=18,
        )
    )

    assert withdraw.success is True
    assert transfer.success is True
    assert hold.success is True


@pytest.mark.asyncio
async def test_validator_self_toggle_workflows_build_transactions() -> None:
    service = DecimalService(FakeDecimalClient())

    offline = await service.pause_self_validator(ValidatorSelfPauseRequest(private_key=PRIVATE_KEY))
    online = await service.unpause_self_validator(ValidatorSelfPauseRequest(private_key=PRIVATE_KEY))

    assert offline.success is True
    assert offline.steps == ("pause_self_validator",)
    assert online.success is True
    assert online.steps == ("unpause_self_validator",)


@pytest.mark.asyncio
async def test_validator_address_toggle_workflows_build_transactions() -> None:
    service = DecimalService(FakeDecimalClient())

    offline = await service.pause_validator(
        ValidatorPauseRequest(validator=VALIDATOR, private_key=PRIVATE_KEY)
    )
    online = await service.unpause_validator(
        ValidatorPauseRequest(validator=VALIDATOR, private_key=PRIVATE_KEY)
    )

    assert offline.success is True
    assert offline.steps == ("pause_validator",)
    assert online.success is True
    assert online.steps == ("unpause_validator",)
