"""Exercise every public transaction entry point offline with real ABI encoding."""
import importlib.util
import json
import os
import time
from decimal import Decimal
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import AsyncMock

import pytest
from eth_account import Account
from web3 import Web3

import decimal_web3_sdk as sdk
from decimal_web3_sdk.erc20 import TokenBalance, TokenInfo

SPEC = importlib.util.spec_from_file_location("reference", Path(__file__).parents[1] / "scripts/generate_reference.py")
reference = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(reference)
CASES = reference.transaction_catalog()


@pytest.fixture
def account():
    Account.enable_unaudited_hdwallet_features()
    account, mnemonic = Account.create_with_mnemonic()
    return account, mnemonic


@pytest.fixture
def offline_client(account):
    owner = account[0].address
    client = sdk.DecimalClient(sdk.NetworkConfig.custom(web3_urls=["https://rpc.example.invalid"]))
    client.rpc._web3 = Web3()
    client.rpc.call = AsyncMock(side_effect=AssertionError("Unexpected RPC in offline test"))
    client.transaction_count = AsyncMock(return_value=0)
    client.gas_price = AsyncMock(return_value=20 * 10**9)
    client.estimate_gas = AsyncMock(return_value=120000)
    client.balance_wei = AsyncMock(return_value=10**36)
    client.send_raw_transaction = AsyncMock(side_effect=AssertionError("Broadcast forbidden"))
    client.tx._contract_code_is_present = AsyncMock(return_value=True)
    info = TokenInfo("0x" + "11" * 20, "Example", "EXAMPLE", 18)
    client.erc20.info = AsyncMock(return_value=info)
    client.erc20.balance = AsyncMock(return_value=TokenBalance(info, owner, 10**36, Decimal("1e18")))
    client.erc20.allowance = AsyncMock(return_value=10**36)
    client.erc20.permit_signature = AsyncMock(return_value=None)
    client.nft.owner_of = AsyncMock(return_value=owner)
    client.nft.balance_of = AsyncMock(return_value=100)
    client.nft.is_approved_for_all = AsyncMock(return_value=True)
    client.checks._nonce = AsyncMock(return_value=1)
    return client


def make_request(row, account, monkeypatch):
    owner, mnemonic = account
    for key in ("VALIDATOR", "OLD_VALIDATOR", "NEW_VALIDATOR", "TOKEN", "TOKEN_IN", "TOKEN_OUT", "NFT", "CONTRACT", "OPERATOR", "SPENDER"):
        monkeypatch.setenv(key, "0x" + ("22" if key in {"TOKEN_OUT", "NEW_VALIDATOR"} else "11") * 20)
    for key in ("HOLD_TIMESTAMP", "OLD_HOLD_TIMESTAMP", "NEW_HOLD_TIMESTAMP", "DUE_BLOCK", "NONCE", "TO_CHAIN_ID", "CRR", "TOKEN_ID"):
        monkeypatch.setenv(key, "1800000000" if "TIMESTAMP" in key else "1")
    for key in ("TOKEN_URI", "CONTRACT_URI", "IDENTITY"):
        monkeypatch.setenv(key, "https://example.org/metadata.json")
    monkeypatch.setenv("HOLD_TIMESTAMPS_TO_RESET", "[1700000000]")
    monkeypatch.setenv("ENCODED_VM", "0x01")
    monkeypatch.setenv("CHECKS", json.dumps(["0x" + "12" * 32]))
    monkeypatch.setenv("SIGNATURES", json.dumps(["0x" + "12" * 65]))
    context = {**vars(sdk), "os": os, "json": json, "time": time, "wallet": owner}
    # Only evaluate our generated fixed expressions, never runtime user input.
    kwargs = {name: eval(expr, context) for name, expr in reference.request_arguments(row["request"]).items()}
    if row["request"] == "MintNftRequest":
        kwargs["token_id"] = 1
    return getattr(sdk, row["request"]).from_mnemonic(mnemonic=mnemonic, **kwargs)


@pytest.mark.parametrize("row", CASES, ids=lambda row: row["method"])
async def test_every_transaction_builds_signs_and_never_broadcasts(row, offline_client, account, monkeypatch):
    request = make_request(row, account, monkeypatch)
    service, method = row["method"].split(".")
    result = await getattr(getattr(offline_client, service), method)(request, broadcast=False)
    assert result.success, result.user_message or result.error
    primary = result.primary if isinstance(result, sdk.DecimalWorkflowResult) else result
    assert primary is not None
    assert primary.raw_tx_hex
    assert primary.tx_hash is None
    assert primary.fee_wei > 0
    assert Account.recover_transaction(primary.raw_tx_hex).lower() == account[0].address.lower()
    offline_client.send_raw_transaction.assert_not_called()
    offline_client.rpc.call.assert_not_called()


def test_all_transaction_examples_compile():
    for row in CASES:
        compile(reference.example(row), row["method"], "exec")


def test_every_public_request_hides_the_key(account, monkeypatch):
    for row in CASES:
        request = make_request(row, account, monkeypatch)
        assert request.private_key not in repr(request)


def test_documentation_is_in_sync():
    root = Path(__file__).parents[1]
    for name, content in reference.generated_files().items():
        assert (root / name).read_text(encoding="utf-8") == content, name
