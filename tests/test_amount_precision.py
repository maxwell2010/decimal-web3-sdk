from decimal import Decimal

import pytest

from decimal_web3_sdk import (
    DecimalClient,
    NetworkConfig,
    TokenBalance,
    TokenInfo,
    format_units,
    format_units_string,
    parse_units,
)
from decimal_web3_sdk.client import _json_loads_exact


TOKEN = "0x1000000000000000000000000000000000000001"
OWNER = "0x2000000000000000000000000000000000000002"


def test_base_units_are_formatted_without_rounding_or_float_conversion() -> None:
    raw = 100_000_000_000_000_000

    assert format_units(raw, 18) == Decimal("0.1")
    assert format_units_string(raw, 18) == "0.1"
    assert parse_units("0.1", 18) == raw


def test_large_amount_round_trip_preserves_every_base_unit() -> None:
    raw = 123_456_789_012_345_678_901_234_567_890
    formatted = format_units(raw, 18)

    assert str(formatted) == "123456789012.34567890123456789"
    assert parse_units(formatted, 18) == raw


def test_parse_units_rejects_precision_that_cannot_fit_token_decimals() -> None:
    with pytest.raises(ValueError, match="more than 18 decimal places"):
        parse_units("0.0000000000000000001", 18)


def test_token_balance_json_shape_keeps_raw_and_formatted_as_strings() -> None:
    balance = TokenBalance(
        token=TokenInfo(address=TOKEN, name="Example", symbol="EXAMPLE", decimals=18),
        owner=OWNER,
        raw=100_000_000_000_000_000,
        formatted=Decimal("0.1"),
    )

    payload = balance.as_dict()

    assert payload["raw"] == "100000000000000000"
    assert payload["formatted"] == "0.1"
    assert payload["token"]["decimals"] == 18


@pytest.mark.asyncio
async def test_native_del_balance_is_decimal_not_float(monkeypatch: pytest.MonkeyPatch) -> None:
    client = DecimalClient(NetworkConfig.mainnet())

    async def balance_wei(_address: str) -> int:
        return 100_000_000_000_000_000

    monkeypatch.setattr(client, "balance_wei", balance_wei)

    balance = await client.balance_del(OWNER)

    assert balance == Decimal("0.1")
    assert isinstance(balance, Decimal)


def test_rest_json_parser_keeps_integer_raw_and_decimal_literal_exact() -> None:
    payload = _json_loads_exact(
        '{"raw":100000000000000000,"formatted":0.100000000000000001}'
    )

    assert payload["raw"] == 100_000_000_000_000_000
    assert payload["formatted"] == Decimal("0.100000000000000001")
