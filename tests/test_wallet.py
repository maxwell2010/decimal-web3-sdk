from __future__ import annotations

import pytest

from decimal_web3_sdk.wallet import (
    DEFAULT_DERIVATION_PATH,
    generate_mnemonic_account,
    mnemonic_to_account,
    mnemonic_to_private_key,
)


TEST_ACCOUNT = generate_mnemonic_account()
MNEMONIC = TEST_ACCOUNT.mnemonic or ""
PRIVATE_KEY = TEST_ACCOUNT.private_key
ADDRESS = TEST_ACCOUNT.address


def test_mnemonic_to_private_key_uses_evm_default_path() -> None:
    assert mnemonic_to_private_key(MNEMONIC) == PRIVATE_KEY


def test_mnemonic_to_account_returns_address_and_path_without_seed_by_default() -> None:
    account = mnemonic_to_account(MNEMONIC)

    assert account.address == ADDRESS
    assert account.private_key == PRIVATE_KEY
    assert account.mnemonic is None
    assert account.derivation_path == DEFAULT_DERIVATION_PATH


def test_mnemonic_to_account_can_include_seed_for_explicit_export() -> None:
    account = mnemonic_to_account(MNEMONIC, include_mnemonic=True)

    assert account.mnemonic == MNEMONIC


def test_generate_mnemonic_account_validates_word_count() -> None:
    with pytest.raises(ValueError):
        generate_mnemonic_account(num_words=13)
