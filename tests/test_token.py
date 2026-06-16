from __future__ import annotations

from decimal import Decimal

import pytest

from decimal_web3_sdk import (
    token_creation_commission_del,
    token_creation_commission_wei,
    token_creation_required_reserve_del,
    token_creation_required_reserve_wei,
)


@pytest.mark.parametrize(
    ("symbol", "commission"),
    [
        ("ABC", Decimal("2500000")),
        ("ABCD", Decimal("250000")),
        ("ABCDE", Decimal("25000")),
        ("ABCDEF", Decimal("2500")),
        ("ABCDEFG", Decimal("250")),
        ("MINTCANDY", Decimal("250")),
    ],
)
def test_token_creation_commission_matches_decimal_go_sdk_rules(symbol: str, commission: Decimal) -> None:
    assert token_creation_commission_del(symbol) == commission


def test_token_creation_required_reserve_adds_minimum_reserve_and_commission() -> None:
    assert token_creation_required_reserve_del("MINTCANDY") == Decimal("1250")
    assert token_creation_required_reserve_wei("MINTCANDY") == 1250 * 10**18
    assert token_creation_commission_wei("ABC") == 2_500_000 * 10**18


def test_token_creation_commission_rejects_empty_symbol() -> None:
    with pytest.raises(ValueError, match="Token symbol is required"):
        token_creation_commission_del(" ")
