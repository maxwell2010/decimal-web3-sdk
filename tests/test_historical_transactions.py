"""Rebuild mined calldata offline; never load credentials, sign or broadcast."""

from collections import Counter
import copy
import importlib.util
import json
from pathlib import Path
import socket
from types import SimpleNamespace
from unittest.mock import AsyncMock

from eth_abi import decode
from eth_account import Account
from hexbytes import HexBytes
import pytest
import requests
from web3 import Web3

from decimal_web3_sdk import decimal as decimal_module, transactions as tx_module
from decimal_web3_sdk.config import NetworkConfig
from decimal_web3_sdk.decimal import (
    DecimalService, MultisendDelRequest, MultisendErc20Request,
    MultisendErc20Recipient, MultisendRecipient, WithdrawDelStakeWithResetRequest,
)
from decimal_web3_sdk.erc20 import Erc20Service, PermitSignature, format_units_string
from decimal_web3_sdk.transactions import (
    Erc20ApproveRequest, Erc20TransferRequest, NativeTransferRequest,
    TransactionDraft, TransactionResult, TransactionService, _result_from_draft,
)


ROOT = Path(__file__).resolve().parents[1]
CORPUS = json.loads((ROOT / "tests/fixtures/mined_mainnet_transactions.json").read_text())
CASES = {case["name"]: case for case in CORPUS["cases"]}
spec = importlib.util.spec_from_file_location("collect_fixtures", ROOT / "scripts/collect_transaction_fixtures.py")
collector = importlib.util.module_from_spec(spec)
spec.loader.exec_module(collector)


def forbidden(*args, **kwargs):
    pytest.fail("Historical regression attempted network access or signing")


@pytest.fixture(autouse=True)
def no_network_or_signatures(monkeypatch):
    # Windows asyncio creates a loopback socketpair when setting up its event loop.
    monkeypatch.setattr(socket, "getaddrinfo", forbidden)
    monkeypatch.setattr(requests.Session, "request", forbidden)
    monkeypatch.setattr(Web3.HTTPProvider, "make_request", forbidden)
    monkeypatch.setattr(Account, "sign_transaction", forbidden)
    monkeypatch.setattr(Account, "sign_message", forbidden)


@pytest.fixture
def offline_client(monkeypatch):
    def create(case_name):
        tx = CASES[case_name]["transaction"]
        # The key is ephemeral and never used to sign. Only the historical sender is substituted.
        key = "0x" + bytes(Account.create().key).hex()
        monkeypatch.setattr(tx_module, "private_key_to_address", lambda _: tx["from"])
        monkeypatch.setattr(decimal_module, "private_key_to_address", lambda _: tx["from"])
        client = SimpleNamespace(
            config=NetworkConfig.mainnet(), web3=Web3(),
            transaction_count=AsyncMock(return_value=tx["nonce"]),
            gas_price=AsyncMock(return_value=int(tx["gasPrice"])), captured=[],
            send_raw_transaction=AsyncMock(side_effect=forbidden),
            rpc=SimpleNamespace(call=AsyncMock(side_effect=forbidden)),
        )
        client.tx = TransactionService(client)
        client.erc20 = Erc20Service(client)
        client.decimal = DecimalService(client)
        client.erc20.info = AsyncMock(return_value=SimpleNamespace(decimals=18))
        client.erc20.balance = AsyncMock(return_value=SimpleNamespace(raw=10**30))
        client.erc20.allowance = AsyncMock(return_value=10**30)
        client.erc20.permit_signature = AsyncMock(side_effect=forbidden)
        client.tx.sign = AsyncMock(side_effect=forbidden)

        async def capture(draft, private_key, broadcast, wait_receipt):
            assert not broadcast and not wait_receipt
            client.captured.append(draft)
            return TransactionResult(success=True, status="dry_run")

        client.tx.send_draft = capture
        return client, key
    return create


def assert_payload(draft, case_name):
    expected = CASES[case_name]["transaction"]
    assert draft.tx["chainId"] == expected["chainId"]
    assert draft.from_address.lower() == expected["from"].lower()
    assert draft.to_address.lower() == expected["to"].lower()
    assert draft.value_wei == int(expected["value"])
    assert HexBytes(draft.tx["data"]) == HexBytes(expected["input"])
    assert draft.raw_tx is None


def aggregate_calls(case_name):
    raw = HexBytes(CASES[case_name]["transaction"]["input"])
    assert raw[:4] == Web3.keccak(text="aggregate((address,uint256,bytes)[])")[:4]
    return decode(["(address,uint256,bytes)[]"], raw[4:])[0]


@pytest.mark.parametrize("entrypoint", ["native", "single_recipient_multisend"])
async def test_direct_native_memo_matches_previous_mined_transaction(offline_client, entrypoint):
    client, key = offline_client("sdk_del_memo")
    tx = CASES["sdk_del_memo"]["transaction"]
    amount, memo = format_units_string(int(tx["value"]), 18), bytes(HexBytes(tx["input"])).decode()
    if entrypoint == "native":
        draft = await client.tx.build_native_transfer(NativeTransferRequest(to=tx["to"], amount_del=amount, memo=memo, private_key=key))
    else:
        draft = await client.decimal.build_multisend_del(MultisendDelRequest(recipients=[MultisendRecipient(tx["to"], amount)], memo=memo, private_key=key))
    assert_payload(draft, "sdk_del_memo")


async def test_native_multisend_matches_mined_payload_without_approve(offline_client):
    client, key = offline_client("sdk_del_multisend")
    calls = aggregate_calls("sdk_del_multisend")
    draft = await client.decimal.build_multisend_del(MultisendDelRequest(
        recipients=[MultisendRecipient(to, format_units_string(value, 18)) for to, value, _ in calls[:-1]],
        memo=calls[-1][2].decode(), private_key=key,
    ))
    assert_payload(draft, "sdk_del_multisend")
    client.erc20.allowance.assert_not_awaited()
    client.erc20.permit_signature.assert_not_awaited()


async def test_withdraw_with_reset_matches_previous_success(offline_client):
    client, key = offline_client("sdk_withdraw_with_reset")
    tx = CASES["sdk_withdraw_with_reset"]["transaction"]
    validator, token, amount, holds = decode(["address", "address", "uint256", "uint256[]"], HexBytes(tx["input"])[4:])
    assert token.lower() == client.config.contracts.wdel.lower()
    result = await client.decimal.withdraw_del_stake_with_reset(WithdrawDelStakeWithResetRequest(
        validator=validator, amount_del=format_units_string(amount, 18),
        hold_timestamps_to_reset=list(holds), private_key=key,
    ), broadcast=False)
    assert result.success and result.one_transaction
    assert len(client.captured) == 1
    assert_payload(client.captured[0], "sdk_withdraw_with_reset")


async def test_approve_matches_service_transaction_exactly(offline_client):
    client, key = offline_client("service_erc20_approve")
    tx = CASES["service_erc20_approve"]["transaction"]
    spender, amount = decode(["address", "uint256"], HexBytes(tx["input"])[4:])
    draft = await client.tx.build_erc20_approve(Erc20ApproveRequest(
        token=tx["to"], spender=spender, amount=format_units_string(amount, 18), decimals=18, private_key=key,
    ))
    assert_payload(draft, "service_erc20_approve")


async def test_transfer_matches_mined_payload_and_event(offline_client):
    client, key = offline_client("sdk_erc20_transfer")
    tx = CASES["sdk_erc20_transfer"]["transaction"]
    to, amount = decode(["address", "uint256"], HexBytes(tx["input"])[4:])
    draft = await client.tx.build_erc20_transfer(Erc20TransferRequest(
        token=tx["to"], to=to, amount=format_units_string(amount, 18), decimals=18, private_key=key,
    ))
    assert_payload(draft, "sdk_erc20_transfer")
    assert transfer_events("sdk_erc20_transfer") == Counter({(tx["to"].lower(), tx["from"].lower(), to.lower(), amount): 1})


def transfer_events(case_name):
    topic = Web3.keccak(text="Transfer(address,address,uint256)")
    result = Counter()
    for log in CASES[case_name]["receipt"]["logs"]:
        if len(log["topics"]) == 3 and HexBytes(log["topics"][0]) == topic:
            owner, to = ("0x" + bytes(HexBytes(item))[-20:].hex() for item in log["topics"][1:])
            result[(log["address"].lower(), owner, to, int.from_bytes(HexBytes(log["data"]), "big"))] += 1
    return result


@pytest.mark.parametrize("route", ["allowance", "approve", "permit"])
async def test_erc20_multisend_routes_match_mined_examples(offline_client, route):
    case_name = "reference_permit_multisend" if route == "permit" else "service_erc20_multisend"
    client, key = offline_client(case_name)
    calls = aggregate_calls(case_name)
    transfers = calls[1:-1] if route == "permit" else calls[:-1]
    recipients, expected_events = [], Counter()
    for token, value, data in transfers:
        assert value == 0 and data[:4] == Web3.keccak(text="transferFrom(address,address,uint256)")[:4]
        owner, to, amount = decode(["address", "address", "uint256"], data[4:])
        recipients.append(MultisendErc20Recipient(to, format_units_string(amount, 18)))
        expected_events[(token.lower(), owner.lower(), to.lower(), amount)] += 1
    assert transfer_events(case_name) == expected_events
    assert len(recipients) == (26 if route == "permit" else 17)
    deadline = 2**256 - 1
    if route in ("approve", "permit"):
        client.erc20.allowance.return_value = 0
    if route == "permit":
        owner, spender, total, deadline, v, r, s = decode(["address", "address", "uint256", "uint256", "uint8", "bytes32", "bytes32"], calls[0][2][4:])
        client.erc20.permit_signature = AsyncMock(return_value=PermitSignature(deadline, v, r, s))
    result = await client.decimal.multisend_erc20(MultisendErc20Request(
        token=transfers[0][0], recipients=recipients, decimals=18, memo=calls[-1][2].decode(),
        private_key=key, prefer_permit=route == "permit", auto_approve=route == "approve", permit_deadline=deadline,
    ), broadcast=False)
    assert result.success, result.error
    assert_payload(client.captured[-1], case_name)
    assert result.transaction_count == len(client.captured) == (2 if route == "approve" else 1)
    assert result.one_transaction == (route != "approve")
    if route == "approve":
        assert_payload(client.captured[0], "service_erc20_approve")
    elif route == "permit":
        client.erc20.permit_signature.assert_awaited_once_with(transfers[0][0], CASES[case_name]["transaction"]["from"], client.config.contracts.multicall, total, deadline, key)
    else:
        client.erc20.permit_signature.assert_not_awaited()


@pytest.mark.parametrize("case_name", CASES)
def test_mined_receipts_keep_hash_block_status_without_guessing_dynamic_fee(case_name):
    row = CASES[case_name]
    tx, receipt = row["transaction"], row["receipt"]
    draft = TransactionDraft(
        tx={**tx, "value": int(tx["value"]), "gasPrice": int(tx["gasPrice"])},
        from_address=tx["from"], to_address=tx["to"], value_wei=int(tx["value"]),
        gas=tx["gas"], gas_price_wei=int(tx["gasPrice"]), tx_hash=row["hash"], receipt=receipt,
    )
    result = _result_from_draft(draft, None, broadcast=True)
    assert result.success and result.status == "success"
    assert result.tx_hash == row["hash"] and result.block_number == receipt["blockNumber"]
    if tx["type"] == 2 and receipt.get("effectiveGasPrice") is None:
        assert result.effective_gas_price_wei is None
        assert result.effective_fee_wei is None and result.effective_fee_del is None
        return
    price = int(receipt.get("effectiveGasPrice", tx["gasPrice"]))
    assert result.effective_fee_wei == receipt["gasUsed"] * price
    assert str(result.effective_fee_del) == format_units_string(receipt["gasUsed"] * price, 18)
    assert result.raw_tx_hex is None


def test_sources_and_corpus_match_and_exclude_credentials():
    sources = json.loads((ROOT / "tests/fixtures/transaction_sources.json").read_text())
    assert [(r["name"], r["source"], r["hash"]) for r in sources["cases"]] == [(r["name"], r["source"], r["hash"]) for r in CORPUS["cases"]]
    assert not CORPUS["signed"] and not CORPUS["broadcast"] and not CORPUS["secrets_loaded"]
    assert {r["source"] for r in CORPUS["cases"]} == {"sdk", "service", "protocol_reference"}
    def visit(value):
        if isinstance(value, dict):
            assert not {"private_key", "mnemonic", "seed", "raw_tx", "r", "s", "v"}.intersection(value)
            for item in value.values():
                visit(item)
        elif isinstance(value, list):
            for item in value:
                visit(item)
    visit(CORPUS)


@pytest.mark.parametrize("tx_fields,receipt_fields", [
    ({"type": "0x2"}, {}), ({"type": 3}, {}), ({"type": "unknown"}, {}),
    ({}, {"type": "0x2"}), ({"type": 0}, {"type": 2}),
    ({"maxFeePerGas": 999}, {}), ({"maxPriorityFeePerGas": 0}, {}),
])
def test_dynamic_or_unknown_fee_never_uses_legacy_fallback(tx_fields, receipt_fields):
    tx = {"gasPrice": 999, **tx_fields}
    draft = TransactionDraft(
        tx=tx, from_address="0x" + "11" * 20, to_address="0x" + "22" * 20,
        value_wei=0, gas_price_wei=999, receipt={"status": 1, "gasUsed": 21000, **receipt_fields},
    )
    result = _result_from_draft(draft, None, broadcast=True)
    assert result.success and result.effective_fee_wei is None


@pytest.mark.parametrize("tx_type", [None, 0, 1, "0x0", "0x1"])
def test_fixed_fee_types_keep_legacy_fallback(tx_type):
    draft = TransactionDraft(
        tx={"type": tx_type}, from_address="0x" + "11" * 20, to_address="0x" + "22" * 20,
        value_wei=0, gas_price_wei=10, receipt={"status": 1, "gasUsed": 21000},
    )
    assert _result_from_draft(draft, None, broadcast=True).effective_fee_wei == 210000


def test_dynamic_fee_uses_explicit_receipt_price_not_maximum():
    draft = TransactionDraft(
        tx={"type": 2, "maxFeePerGas": 999}, from_address="0x" + "11" * 20,
        to_address="0x" + "22" * 20, value_wei=0, gas_price_wei=999,
        receipt={"status": "0x1", "gasUsed": "0x5208", "effectiveGasPrice": "0xa"},
    )
    assert _result_from_draft(draft, None, broadcast=True).effective_fee_wei == 210000


@pytest.mark.parametrize("method", ["eth_sendRawTransaction", "eth_sendTransaction", "eth_sign", "personal_sign", "eth_signTypedData_v4", "eth_call"])
def test_fixture_collector_rejects_non_lookup_rpc(method):
    with pytest.raises(RuntimeError, match="only reads"):
        collector.FixtureProvider("https://example.invalid").make_request(method, [])


def test_fixture_collector_rejects_batch_rpc():
    with pytest.raises(RuntimeError, match="batch"):
        collector.FixtureProvider("https://example.invalid").make_batch_request([])


@pytest.mark.parametrize("field,value", [("status", 0), ("transactionHash", "0x" + "ff" * 32), ("blockNumber", 0), ("blockHash", "0x" + "ff" * 32)])
def test_fixture_collector_rejects_mismatched_or_failed_receipts(field, value):
    row = CASES["sdk_del_memo"]
    receipt = copy.deepcopy(row["receipt"])
    tx = {**row["transaction"], "hash": row["hash"], "blockNumber": receipt["blockNumber"], "blockHash": receipt["blockHash"]}
    receipt[field] = value
    with pytest.raises(ValueError, match="did not match"):
        collector.snapshot(row["name"], row["source"], row["hash"], tx, receipt, b"")
