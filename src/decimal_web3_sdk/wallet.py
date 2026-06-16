from __future__ import annotations

from dataclasses import dataclass

from eth_account import Account
from web3 import Web3

DEFAULT_DERIVATION_PATH = "m/44'/60'/0'/0/0"


@dataclass(frozen=True)
class WalletAccount:
    address: str
    private_key: str
    mnemonic: str | None = None
    derivation_path: str = DEFAULT_DERIVATION_PATH


def normalize_private_key(private_key: str) -> str:
    key = private_key.strip()
    if not key.startswith("0x"):
        key = f"0x{key}"
    if len(key) != 66:
        raise ValueError("Private key must be 32 bytes hex")
    return key


def private_key_to_address(private_key: str) -> str:
    account = Account.from_key(normalize_private_key(private_key))
    return Web3.to_checksum_address(account.address)


def mnemonic_to_private_key(
    mnemonic: str,
    *,
    passphrase: str = "",
    account_path: str = DEFAULT_DERIVATION_PATH,
) -> str:
    Account.enable_unaudited_hdwallet_features()
    account = Account.from_mnemonic(
        mnemonic.strip(),
        passphrase=passphrase,
        account_path=account_path,
    )
    return normalize_private_key(account.key.hex())


def mnemonic_to_account(
    mnemonic: str,
    *,
    passphrase: str = "",
    account_path: str = DEFAULT_DERIVATION_PATH,
    include_mnemonic: bool = False,
) -> WalletAccount:
    private_key = mnemonic_to_private_key(
        mnemonic,
        passphrase=passphrase,
        account_path=account_path,
    )
    return WalletAccount(
        address=private_key_to_address(private_key),
        private_key=private_key,
        mnemonic=mnemonic.strip() if include_mnemonic else None,
        derivation_path=account_path,
    )


def generate_mnemonic_account(
    *,
    num_words: int = 12,
    passphrase: str = "",
    account_path: str = DEFAULT_DERIVATION_PATH,
) -> WalletAccount:
    if num_words not in (12, 15, 18, 21, 24):
        raise ValueError("num_words must be one of 12, 15, 18, 21, 24")
    Account.enable_unaudited_hdwallet_features()
    account, mnemonic = Account.create_with_mnemonic(
        passphrase=passphrase,
        num_words=num_words,
        account_path=account_path,
    )
    private_key = normalize_private_key(account.key.hex())
    return WalletAccount(
        address=private_key_to_address(private_key),
        private_key=private_key,
        mnemonic=mnemonic,
        derivation_path=account_path,
    )


def checksum(address: str) -> str:
    return Web3.to_checksum_address(address)
