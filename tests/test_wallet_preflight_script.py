import importlib.util
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import AsyncMock, Mock

from eth_account import Account
import pytest
from web3 import Web3

from decimal_web3_sdk.transactions import FeePreflight


spec = importlib.util.spec_from_file_location(
    "wallet_preflight", Path(__file__).resolve().parents[1] / "scripts/check_wallet_preflight.py",
)
audit = importlib.util.module_from_spec(spec)
spec.loader.exec_module(audit)


@pytest.mark.parametrize("method", ["eth_sendRawTransaction", "eth_sendTransaction", "eth_sign", "personal_sign"])
def test_audit_blocks_writes_before_http(method, monkeypatch):
    send = Mock(side_effect=AssertionError("Network must not be reached"))
    monkeypatch.setattr(Web3.HTTPProvider, "make_request", send)
    with pytest.raises(RuntimeError, match="forbids"):
        audit.ReadOnlyProvider().make_request(method, [])
    send.assert_not_called()


def test_audit_blocks_batch_bypass():
    with pytest.raises(RuntimeError, match="batch"):
        audit.ReadOnlyProvider().make_batch_request([("eth_sendRawTransaction", [])])


def test_audit_errors_never_contain_secrets_or_endpoints():
    error = RuntimeError("secret-value https://private-node.invalid/?key=secret-value")
    assert "secret-value" not in str(audit.failure(error))
    assert "private-node" not in str(audit.failure(error))


def test_audit_requires_network_specific_wallet():
    with pytest.raises(ValueError, match="Dedicated"):
        audit.wallet_config({"SEED": "not used"}, "testnet")


def test_audit_rejects_wrong_expected_address(monkeypatch):
    account = Account.create()
    monkeypatch.setattr(audit, "mnemonic_to_account", lambda *args, **kwargs: account)
    with pytest.raises(ValueError, match="mismatch"):
        audit.wallet_config({
            "DECIMAL_TESTNET_TEST_MNEMONIC": "not used by the stub",
            "DECIMAL_TESTNET_TEST_EXPECTED_ADDRESS": "0x" + "11" * 20,
        }, "testnet")


def test_audit_fee_records_do_not_round_or_claim_actual_fees():
    fee = FeePreflight(
        ok=True, from_address="0x" + "11" * 20,
        native_balance_wei=10**18, value_wei=1,
        fee_wei=100000000000000001, required_wei=100000000000000002,
        gas_price_wei=1, estimated_gas=100000000000000001,
        estimated_fee_wei=100000000000000001,
        gas_limit=110000000000000002, gas_limit_fee_wei=110000000000000002,
    )
    record = audit.fee_record(fee)
    assert record["estimated_fee_del"] == "0.100000000000000001"
    assert record["gas_limit_fee_del"] == "0.110000000000000002"
    assert record["actual_fee_del"] is None


async def test_audit_base_cases_never_sign(monkeypatch):
    account = Account.create()
    wallet = SimpleNamespace(address=account.address, private_key=account.key.hex())
    config = audit.NetworkConfig.testnet()
    monkeypatch.setattr(audit, "dotenv_values", lambda *a, **k: {})
    monkeypatch.setattr(audit, "wallet_config", lambda *a: (wallet, config))
    fee = FeePreflight(
        ok=True, from_address=account.address, native_balance_wei=10**18, value_wei=1,
        fee_wei=23100, required_wei=23101, estimated_gas=21000, gas_limit=23100,
        gas_price_wei=1, estimated_fee_wei=21000, gas_limit_fee_wei=23100,
    )
    rpc = SimpleNamespace(call=AsyncMock(return_value=10**18))
    client = SimpleNamespace(
        rpc=rpc, block_number=AsyncMock(return_value=100), balance_wei=AsyncMock(return_value=10**18),
        tx=SimpleNamespace(estimate_fee_for_native_transfer=AsyncMock(return_value=fee)),
        decimal=SimpleNamespace(estimate_fee_for_multisend_del=AsyncMock(return_value=fee)),
        multisig=SimpleNamespace(estimate_fee_for_operation=AsyncMock(return_value=fee)),
        nft=SimpleNamespace(estimate_fee_for_operation=AsyncMock(return_value=fee)),
        close=AsyncMock(),
    )
    monkeypatch.setattr(audit, "DecimalClient", lambda *a: client)
    monkeypatch.setattr(audit, "AuditRpc", lambda *a, **k: rpc)
    signing = Mock(side_effect=AssertionError("Signing is forbidden"))
    monkeypatch.setattr(Account, "sign_transaction", signing)
    monkeypatch.setattr(Account, "sign_message", signing)
    report = await audit.audit(SimpleNamespace(env_file="unused", network="testnet", token=None, validator=None))
    assert "error" not in report
    assert len(report["checks"]) == 6
    assert report["signed"] is False and report["broadcast"] is False
    assert wallet.private_key not in str(report)
    signing.assert_not_called()
