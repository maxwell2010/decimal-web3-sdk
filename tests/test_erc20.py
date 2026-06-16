from __future__ import annotations

from decimal import Decimal

from decimal_web3_sdk import SystemContracts, format_units, parse_units


def test_token_unit_helpers() -> None:
    assert format_units(123450000, 6) == Decimal("123.45")
    assert parse_units("123.45", 6) == 123450000


def test_system_contracts_include_decimal_core_addresses() -> None:
    contracts = SystemContracts()

    assert contracts.delegation.startswith("0x")
    assert contracts.multicall == "0x7b23eb47587ca6482fc16cb3d9d426ec64d4b5fc"

