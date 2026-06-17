from __future__ import annotations

from typing import TypeVar

from .wallet import DEFAULT_DERIVATION_PATH, mnemonic_to_private_key


T = TypeVar("T", bound="FromMnemonicMixin")


class FromMnemonicMixin:
    @classmethod
    def from_mnemonic(
        cls: type[T],
        *,
        mnemonic: str,
        passphrase: str = "",
        account_path: str = DEFAULT_DERIVATION_PATH,
        **kwargs,
    ) -> T:
        if "private_key" in kwargs:
            raise ValueError("Pass mnemonic or private_key, not both")
        return cls(
            private_key=mnemonic_to_private_key(
                mnemonic,
                passphrase=passphrase,
                account_path=account_path,
            ),
            **kwargs,
        )
