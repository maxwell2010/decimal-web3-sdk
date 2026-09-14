from decimal import Decimal, localcontext
from types import SimpleNamespace
from unittest.mock import AsyncMock

import pytest
from web3.exceptions import TransactionNotFound

from decimal_web3_sdk import DecimalClient, NetworkConfig, format_units, format_units_string, parse_units
from decimal_web3_sdk.candy_protocol import load_candy_profile
from decimal_web3_sdk.config import SystemContracts, _env_optional_gas_price_wei
from decimal_web3_sdk.erc20 import _sum_amounts
from decimal_web3_sdk.rest import WalletStakeHold, normalize_wallet_stake_withdrawals
from decimal_web3_sdk.rpc import RpcPool
from decimal_web3_sdk.transactions import FeePreflight, _apply_gas_limit_multiplier, _retry_gas_price_from_minimum_fee_error


def test_fees_and_aggregation_ignore_decimal_context():
    raw = 10**60 + 123456789123456789
    with localcontext() as context:
        context.prec = 3
        quote = FeePreflight(True, "account", raw, raw, raw, raw, raw,
                             estimated_fee_wei=raw, gas_limit_fee_wei=raw)
        for name in ("fee_del", "native_balance_del", "value_del", "required_del", "missing_del", "estimated_fee_del", "gas_limit_fee_del"):
            assert format(getattr(quote, name), "f") == format_units_string(raw, 18)
        assert _sum_amounts([format_units(raw, 18), Decimal("0.000000000000000001")]) == format_units(raw + 1, 18)
        assert _apply_gas_limit_multiplier(1234567, 1.10) == 1358024
        message = f"provided fee < minimum global fee (1 < {raw})"
        price = _retry_gas_price_from_minimum_fee_error(message, 1234567)
        assert price * 1234567 >= raw
        assert (price - 1) * 1234567 < raw


@pytest.mark.parametrize("value", [True, 0.1, float("nan"), float("inf")])
def test_float_and_bool_amounts_rejected(value):
    with pytest.raises(TypeError):
        parse_units(value, 18)


@pytest.mark.parametrize("places", [True, 18.5, -1, 256, "18"])
def test_invalid_decimals_rejected(places):
    with pytest.raises(ValueError):
        parse_units("1", places)


def test_gwei_override_is_exact(monkeypatch):
    monkeypatch.delenv("DECIMAL_MAX_GAS_PRICE_WEI", raising=False)
    monkeypatch.setenv("DECIMAL_MAX_GAS_PRICE_GWEI", "123456789.123456789")
    assert _env_optional_gas_price_wei() == 123456789123456789


async def test_wrong_chain_is_never_used_and_fallback_checked(monkeypatch):
    wrong = SimpleNamespace(eth=SimpleNamespace(chain_id=1))
    right = SimpleNamespace(eth=SimpleNamespace(chain_id=75))
    pool = RpcPool(["wrong", "right"], min_interval_seconds=0, chain_id=75)
    monkeypatch.setattr(pool, "_create_web3", lambda url: wrong if url == "wrong" else right)
    visited = []
    assert await pool.call(lambda w3: visited.append(w3) or "ok") == "ok"
    assert visited == [right]


async def test_receipt_not_found_is_not_rpc_outage(monkeypatch):
    client = DecimalClient(NetworkConfig.custom(web3_urls=["https://rpc.example.invalid"]))
    def absent(_):
        raise TransactionNotFound("pending")
    fake = SimpleNamespace(eth=SimpleNamespace(get_transaction_receipt=absent))
    async def call(fn):
        return fn(fake)
    monkeypatch.setattr(client.rpc, "call", call)
    assert await client.transaction_receipt("hash") is None
    monkeypatch.setattr(client.rpc, "call", AsyncMock(side_effect=RuntimeError("unavailable")))
    with pytest.raises(RuntimeError):
        await client.transaction_receipt("hash")


def test_mature_withdrawal_is_not_completed_and_raw_amount_is_exact():
    owner = "0x" + "11" * 20
    rows = normalize_wallet_stake_withdrawals(owner, now_timestamp=2000000000,
        txs_payload={"data": [{"from_address": owner, "transaction_type": "withdraw_with_reset",
            "amount": "0.100000000000000001", "token_symbol": "DEL", "timestamp": 1000000000}]})
    assert len(rows) == 1
    assert rows[0].amount_raw == "100000000000000001"
    assert rows[0].is_matured and not rows[0].is_completed
    assert rows[0].completion_estimated


def test_hold_start_is_not_contract_hold_key():
    hold = WalletStakeHold(Decimal(1), str(10**18), hold_start_time=100)
    assert hold.contract_hold_timestamp is None


def test_nft_defaults_match_reviewed_profile():
    profile = load_candy_profile()
    config = SystemContracts()
    assert config.nft_center == profile["nftCenter"]
    assert config.delegation_nft == profile["nftDelegation"]
    assert config.nft_center != config.token_center


def test_cli_defaults_to_mainnet_and_does_not_require_a_key_argument():
    from decimal_web3_sdk.cli import _build_parser
    args = _build_parser().parse_args(["send-del", "--to", "0x" + "11" * 20, "--amount", "0.1"])
    assert args.network == "mainnet"
    assert args.private_key is None


@pytest.mark.parametrize("network", ["mainnet", "testnet", "devnet"])
def test_cli_network_can_be_selected_explicitly(network):
    from decimal_web3_sdk.cli import _build_parser
    args = _build_parser().parse_args(["--network", network, "block-number"])
    assert args.network == network


def test_default_client_uses_official_mainnet(monkeypatch):
    for name in ("DECIMAL_WEB3_URLS", "DECIMAL_NETWORK_NAME"):
        monkeypatch.delenv(name, raising=False)
    client = DecimalClient()
    assert client.config.chain_id == 75
    assert client.config.name == "decimal-mainnet"
    assert client.config.web3_urls == ["https://node.decimalchain.com/web3/"]


async def test_connect_falls_back_when_disconnected(monkeypatch):
    pool = RpcPool(["offline", "online"], min_interval_seconds=0)
    monkeypatch.setattr(pool, "_create_web3", lambda url: SimpleNamespace(is_connected=lambda: url == "online"))
    assert await pool.connect()
    assert pool.current_url == "online"
