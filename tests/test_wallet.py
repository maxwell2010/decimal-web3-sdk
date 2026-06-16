from __future__ import annotations

import pytest

from decimal_web3_sdk.wallet import (
    DEFAULT_DERIVATION_PATH,
    generate_mnemonic_account,
    mnemonic_to_account,
    mnemonic_to_private_key,
)


MNEMONIC = "test test test test test test test test test test test junk"
PRIVATE_KEY = "0xac0974bec39a17e36ba4a6b4d238ff944bacb478cbed5efcae784d7bf4f2ff80"
ADDRESS = "0xf39Fd6e51aad88F6F4ce6aB8827279cffFb92266"


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
