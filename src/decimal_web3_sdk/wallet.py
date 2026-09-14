from __future__ import annotations

from dataclasses import dataclass, field

from eth_account import Account
from web3 import Web3

DEFAULT_DERIVATION_PATH = "m/44'/60'/0'/0/0"
DEFAULT_DERIVATION_PATH_TEMPLATE = "m/44'/60'/{account}'/{change}/{index}"


@dataclass(frozen=True)
class WalletAccount:
    address: str
    private_key: str = field(repr=False)
    mnemonic: str | None = field(default=None, repr=False)
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


def derivation_path_for_index(index: int, *, account: int = 0, change: int = 0) -> str:
    """Build the Decimal EVM BIP-44 path for one address in a mnemonic sequence."""
    values = {"account": account, "change": change, "index": index}
    for name, value in values.items():
        if not isinstance(value, int) or isinstance(value, bool) or value < 0:
            raise ValueError(f"{name} must be a non-negative integer")
    return DEFAULT_DERIVATION_PATH_TEMPLATE.format(**values)


def _resolved_account_path(account_path: str, account_index: int | None) -> str:
    if account_index is None:
        return account_path
    if account_path != DEFAULT_DERIVATION_PATH:
        raise ValueError("Pass account_path or account_index, not both")
    return derivation_path_for_index(account_index)


def mnemonic_to_private_key(
    mnemonic: str,
    *,
    passphrase: str = "",
    account_path: str = DEFAULT_DERIVATION_PATH,
    account_index: int | None = None,
) -> str:
    account_path = _resolved_account_path(account_path, account_index)
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
    account_index: int | None = None,
    include_mnemonic: bool = False,
) -> WalletAccount:
    account_path = _resolved_account_path(account_path, account_index)
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


def mnemonic_to_accounts(
    mnemonic: str,
    *,
    start_index: int = 0,
    count: int = 10,
    passphrase: str = "",
    account: int = 0,
    change: int = 0,
) -> tuple[WalletAccount, ...]:
    """Derive a deterministic address sequence from one mnemonic (0..9 by default)."""
    if not isinstance(start_index, int) or isinstance(start_index, bool) or start_index < 0:
        raise ValueError("start_index must be a non-negative integer")
    if not isinstance(count, int) or isinstance(count, bool) or count < 1:
        raise ValueError("count must be a positive integer")
    return tuple(
        mnemonic_to_account(
            mnemonic,
            passphrase=passphrase,
            account_path=derivation_path_for_index(index, account=account, change=change),
        )
        for index in range(start_index, start_index + count)
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
