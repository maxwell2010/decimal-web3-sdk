from __future__ import annotations

from decimal import Decimal

from decimal_web3_sdk.test_harness import TxTrainingJournal, _record, _test_private_key_from_env, _training_config
from decimal_web3_sdk.transactions import TransactionResult
from decimal_web3_sdk.wallet import generate_mnemonic_account


def test_training_journal_writes_csv(tmp_path) -> None:
    journal = TxTrainingJournal(tmp_path / "tx_training.csv")
    record = _record(
        "send_del",
        "DEL",
        TransactionResult(success=True, gas=21_000, fee_wei=1, fee_del=Decimal("0.1")),
        elapsed_ms=12.3,
        broadcast=False,
        expected_steps=1,
        actual_steps=1,
    )

    journal.append(record)

    text = (tmp_path / "tx_training.csv").read_text(encoding="utf-8")
    assert "send_del" in text
    assert "extra_steps_required" in text


def test_training_private_key_can_come_from_mnemonic(monkeypatch) -> None:
    account = generate_mnemonic_account()
    monkeypatch.delenv("DECIMAL_TEST_PRIVATE_KEY", raising=False)
    monkeypatch.setenv("DECIMAL_TEST_MNEMONIC", account.mnemonic or "")

    assert _test_private_key_from_env() == account.private_key


def test_training_private_key_takes_precedence_over_mnemonic(monkeypatch) -> None:
    account = generate_mnemonic_account()
    monkeypatch.setenv("DECIMAL_TEST_PRIVATE_KEY", "0x" + "1" * 64)
    monkeypatch.setenv("DECIMAL_TEST_MNEMONIC", account.mnemonic or "")

    assert _test_private_key_from_env() == "0x" + "1" * 64


def test_training_config_defaults_to_testnet(monkeypatch) -> None:
    monkeypatch.delenv("DECIMAL_TEST_NETWORK", raising=False)

    config = _training_config()

    assert config.name == "decimal-testnet"
    assert config.chain_id == 202020
