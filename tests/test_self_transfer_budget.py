import importlib.util
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import AsyncMock

import pytest


spec = importlib.util.spec_from_file_location(
    "self_transfer_checks", Path(__file__).resolve().parents[1] / "scripts/run_self_transfer_checks.py",
)
checks = importlib.util.module_from_spec(spec)
spec.loader.exec_module(checks)


def planned_transaction():
    return {
        "chainId": 75, "nonce": 7, "from": "0x" + "11" * 20,
        "to": "0x" + "11" * 20, "value": 1, "data": "0x",
        "gas": 21000, "gasPrice": 10,
    }


def test_exact_budget_includes_fee_and_value():
    planned = planned_transaction()
    draft = SimpleNamespace(tx=dict(planned))
    assert checks.check_signing_budget(draft, planned, 100, 210101) == 210001
    with pytest.raises(ValueError, match="budget"):
        checks.check_signing_budget(draft, planned, 100, 210100)


def test_fee_retry_must_pass_budget_again():
    planned = planned_transaction()
    draft = SimpleNamespace(tx={**planned, "gasPrice": 100})
    with pytest.raises(ValueError, match="budget"):
        checks.check_signing_budget(draft, planned, 0, 210001)


@pytest.mark.parametrize("field,value", [
    ("chainId", 202020), ("nonce", 8), ("value", 2),
    ("from", "0x" + "22" * 20), ("to", "0x" + "22" * 20), ("data", "0xff"),
])
def test_signing_guard_rejects_unapproved_transaction(field, value):
    planned = planned_transaction()
    draft = SimpleNamespace(tx={**planned, field: value})
    with pytest.raises(ValueError, match="differs"):
        checks.check_signing_budget(draft, planned, 0, 10**18)


def test_legacy_receipt_without_effective_price_uses_confirmed_transaction():
    assert checks.receipt_fee({"gasUsed": 21000}, {"gas": 23100, "gasPrice": 1190475000000, "type": 0}) == (24999975000000000, 1190475000000)


def test_effective_price_takes_precedence_over_transaction_price():
    assert checks.receipt_fee({"gasUsed": 21000, "effectiveGasPrice": 10}, {"gas": 23100, "gasPrice": 20, "type": 2}) == (210000, 10)


def test_missing_dynamic_effective_price_must_not_be_guessed():
    with pytest.raises(ValueError, match="Dynamic-fee"):
        checks.receipt_fee({"gasUsed": 21000}, {"gas": 23100, "gasPrice": 20, "type": 2})


@pytest.mark.asyncio
async def test_reconcile_recounts_confirmed_fee_without_resending():
    planned = planned_transaction()
    tx = {**planned, "input": planned["data"], "type": 0}
    client = SimpleNamespace(
        transaction_receipt=AsyncMock(return_value={"status": 1, "gasUsed": 21000, "blockNumber": 123}),
        rpc=SimpleNamespace(call=AsyncMock(return_value=tx)),
    )
    build, send = AsyncMock(return_value=SimpleNamespace(tx=planned)), AsyncMock()
    report = {"spent_fee_wei": "999", "budget_consumed_wei": "999", "cases": [{
        "name": "send_del", "nonce": 7,
        "signed_attempts": [{"tx_hash": "0x123", "gas_limit": 21000, "gas_price_wei": "10"}],
    }]}
    assert await checks.reconcile(client, report, [("send_del", build, send)]) == 210001
    assert report["spent_fee_wei"] == "210000"
    assert report["cases"][0]["status"] == "confirmed"
    send.assert_not_awaited()
    assert await checks.reconcile(client, report, [("send_del", build, send)]) == 210001
    assert report["spent_fee_wei"] == "210000"


@pytest.mark.asyncio
@pytest.mark.parametrize("receipt", [None, {"status": 0}])
async def test_resume_never_resends_unresolved_or_reverted_case(receipt):
    client = SimpleNamespace(transaction_receipt=AsyncMock(return_value=receipt))
    build, send = AsyncMock(), AsyncMock()
    report = {"cases": [{"name": "send_del", "signed_attempts": [{"tx_hash": "0x123"}]}]}
    with pytest.raises(ValueError, match="will not resend"):
        await checks.reconcile(client, report, [("send_del", build, send)])
    build.assert_not_awaited()
    send.assert_not_awaited()


@pytest.mark.parametrize("field,value", [("network", "testnet"), ("chain_id", 202020), ("address", "0x" + "22" * 20), ("limit_del", "5"), ("token", "0x" + "22" * 20)])
def test_resume_rejects_different_wallet_network_budget_or_token(field, value):
    address, token = "0x" + "11" * 20, "0x" + "33" * 20
    report = {"network": "mainnet", "chain_id": 75, "address": address, "limit_del": "0.25", "token": token}
    report[field] = value
    with pytest.raises(ValueError, match="does not match"):
        checks.validate_resume(report, "mainnet", 75, address, 25 * 10**16, token)
