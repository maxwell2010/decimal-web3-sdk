# wallet

[Index](../api.md)

Signatures are generated from the release source. Required fields have no default.

## WalletAccount

Walletaccount; types, defaults and return value are specified below.

```python
WalletAccount(address: 'str', private_key: 'str', mnemonic: 'str | None' = None, derivation_path: 'str' = "m/44'/60'/0'/0/0") -> None
```

- `address`: `str`; required.
- `private_key`: `str`; use from_mnemonic; technical field, hidden in repr.
- `mnemonic`: `str | None`; None.
- `derivation_path`: `str`; "m/44'/60'/0'/0/0".

## normalize_private_key

Normalize private key; types, defaults and return value are specified below.

```python
normalize_private_key(private_key: 'str') -> 'str'
```

## private_key_to_address

Private key to address; types, defaults and return value are specified below.

```python
private_key_to_address(private_key: 'str') -> 'str'
```

## derivation_path_for_index

Derivation path for index; types, defaults and return value are specified below.

```python
derivation_path_for_index(index: 'int', *, account: 'int' = 0, change: 'int' = 0) -> 'str'
```

## mnemonic_to_private_key

Mnemonic to private key; types, defaults and return value are specified below.

```python
mnemonic_to_private_key(mnemonic: 'str', *, passphrase: 'str' = '', account_path: 'str' = "m/44'/60'/0'/0/0", account_index: 'int | None' = None) -> 'str'
```

## mnemonic_to_account

Mnemonic to account; types, defaults and return value are specified below.

```python
mnemonic_to_account(mnemonic: 'str', *, passphrase: 'str' = '', account_path: 'str' = "m/44'/60'/0'/0/0", account_index: 'int | None' = None, include_mnemonic: 'bool' = False) -> 'WalletAccount'
```

## mnemonic_to_accounts

Mnemonic to accounts; types, defaults and return value are specified below.

```python
mnemonic_to_accounts(mnemonic: 'str', *, start_index: 'int' = 0, count: 'int' = 10, passphrase: 'str' = '', account: 'int' = 0, change: 'int' = 0) -> 'tuple[WalletAccount, ...]'
```

## generate_mnemonic_account

Generate mnemonic account; types, defaults and return value are specified below.

```python
generate_mnemonic_account(*, num_words: 'int' = 12, passphrase: 'str' = '', account_path: 'str' = "m/44'/60'/0'/0/0") -> 'WalletAccount'
```

## checksum

Checksum; types, defaults and return value are specified below.

```python
checksum(address: 'str') -> 'str'
```
