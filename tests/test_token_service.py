from __future__ import annotations

from types import SimpleNamespace

import pytest
from web3 import Web3

from decimal_web3_sdk.token import (
    BurnTokenRequest,
    BuyTokenRequest,
    ConvertTokenRequest,
    CreateReservelessTokenRequest,
    SellTokenRequest,
    TokenService,
)
from decimal_web3_sdk.transactions import TransactionService


PRIVATE_KEY = "0x" + "1" * 64
TOKEN_IN = "0x" + "5" * 40
TOKEN_OUT = "0x" + "6" * 40
TOKEN_CENTER = "0x" + "7" * 40


class FakeTokenClient:
    def __init__(
        self,
        balance_wei: int = 10**21,
        token_balance_raw: int = 10**21,
        allowance_raw: int = 10**21,
    ) -> None:
        self.web3 = Web3()
        self.config = SimpleNamespace(
            chain_id=75,
            contracts=SimpleNamespace(token_center=TOKEN_CENTER),
        )
        self.tx = TransactionService(self)
        self.balance = balance_wei
        self.token_balance_raw = token_balance_raw
        self.allowance_raw = allowance_raw
        self.erc20 = SimpleNamespace(
            info=self._token_info,
            balance=self._token_balance,
            allowance=self._allowance,
            build_approve_data=lambda token, spender, amount_raw: "0x095ea7b3" + "00" * 64,
        )

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


@pytest.mark.asyncio
async def test_buy_token_checks_value_plus_fee() -> None:
    service = TokenService(FakeTokenClient())

    result = await service.buy(BuyTokenRequest(token=TOKEN_IN, amount_del="1", private_key=PRIVATE_KEY))

    assert result.success is True
    assert result.required_wei == 1_000_100_000_000_000_000
    assert result.raw_tx_hex is not None


@pytest.mark.asyncio
async def test_sell_token_reports_insufficient_token_balance() -> None:
    service = TokenService(FakeTokenClient(token_balance_raw=1))

    result = await service.sell(SellTokenRequest(token=TOKEN_IN, amount="1", private_key=PRIVATE_KEY))

    assert result.success is False
    assert "Insufficient ERC20" in str(result.error)
    assert result.token_missing_raw == 10**18 - 1


@pytest.mark.asyncio
async def test_burn_token_builds_contract_call_after_token_preflight() -> None:
    service = TokenService(FakeTokenClient(token_balance_raw=10**21))

    result = await service.burn(BurnTokenRequest(token=TOKEN_IN, amount="2", private_key=PRIVATE_KEY))

    assert result.success is True
    assert result.gas == 100_000


@pytest.mark.asyncio
async def test_convert_token_single_step_when_allowance_is_enough() -> None:
    service = TokenService(FakeTokenClient(allowance_raw=10**21))

    result = await service.convert(
        ConvertTokenRequest(
            token_in=TOKEN_IN,
            token_out=TOKEN_OUT,
            amount_in="1",
            min_amount_out="0.9",
            private_key=PRIVATE_KEY,
        )
    )

    assert result.success is True
    assert result.steps == ("convert_erc20",)
    assert result.extra_steps_required is False


@pytest.mark.asyncio
async def test_convert_token_plans_approve_when_allowance_is_low() -> None:
    service = TokenService(FakeTokenClient(allowance_raw=0))

    result = await service.convert(
        ConvertTokenRequest(
            token_in=TOKEN_IN,
            token_out=TOKEN_OUT,
            amount_in="1",
            min_amount_out="0.9",
            private_key=PRIVATE_KEY,
        )
    )

    assert result.success is True
    assert result.steps == ("approve_erc20", "convert_erc20")
    assert result.actual_steps == 2
    assert result.extra_steps_required is True


@pytest.mark.asyncio
async def test_create_reserveless_token_builds_token_center_call() -> None:
    service = TokenService(FakeTokenClient())

    result = await service.create_reserveless(
        CreateReservelessTokenRequest(
            name="Training",
            symbol="TRN",
            mintable=True,
            burnable=True,
            initial_mint_raw=1000,
            cap_raw=10_000,
            identity="sdk-test",
            private_key=PRIVATE_KEY,
        )
    )

    assert result.success is True
    assert result.gas == 100_000
