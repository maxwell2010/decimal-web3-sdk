# wallet

[Index](../api.md)

Сигнатуры сформированы из кода релиза. Обязательные поля не имеют значения по умолчанию.

## WalletAccount

Публичная операция/свойство SDK. Ниже приведены точные типы, значения по умолчанию и тип результата; контекст использования дан в руководстве раздела.

```python
WalletAccount(address: 'str', private_key: 'str', mnemonic: 'str | None' = None, derivation_path: 'str' = "m/44'/60'/0'/0/0") -> None
```

- `address`: `str`; required.
- `private_key`: `str`; use from_mnemonic; technical field, hidden in repr.
- `mnemonic`: `str | None`; None.
- `derivation_path`: `str`; "m/44'/60'/0'/0/0".

## normalize_private_key

Публичная операция/свойство SDK. Ниже приведены точные типы, значения по умолчанию и тип результата; контекст использования дан в руководстве раздела.

```python
normalize_private_key(private_key: 'str') -> 'str'
```

## private_key_to_address

Публичная операция/свойство SDK. Ниже приведены точные типы, значения по умолчанию и тип результата; контекст использования дан в руководстве раздела.

```python
private_key_to_address(private_key: 'str') -> 'str'
```

## derivation_path_for_index

Публичная операция/свойство SDK. Ниже приведены точные типы, значения по умолчанию и тип результата; контекст использования дан в руководстве раздела.

```python
derivation_path_for_index(index: 'int', *, account: 'int' = 0, change: 'int' = 0) -> 'str'
```

## mnemonic_to_private_key

Публичная операция/свойство SDK. Ниже приведены точные типы, значения по умолчанию и тип результата; контекст использования дан в руководстве раздела.

```python
mnemonic_to_private_key(mnemonic: 'str', *, passphrase: 'str' = '', account_path: 'str' = "m/44'/60'/0'/0/0", account_index: 'int | None' = None) -> 'str'
```

## mnemonic_to_account

Публичная операция/свойство SDK. Ниже приведены точные типы, значения по умолчанию и тип результата; контекст использования дан в руководстве раздела.

```python
mnemonic_to_account(mnemonic: 'str', *, passphrase: 'str' = '', account_path: 'str' = "m/44'/60'/0'/0/0", account_index: 'int | None' = None, include_mnemonic: 'bool' = False) -> 'WalletAccount'
```

## mnemonic_to_accounts

Публичная операция/свойство SDK. Ниже приведены точные типы, значения по умолчанию и тип результата; контекст использования дан в руководстве раздела.

```python
mnemonic_to_accounts(mnemonic: 'str', *, start_index: 'int' = 0, count: 'int' = 10, passphrase: 'str' = '', account: 'int' = 0, change: 'int' = 0) -> 'tuple[WalletAccount, ...]'
```

## generate_mnemonic_account

Публичная операция/свойство SDK. Ниже приведены точные типы, значения по умолчанию и тип результата; контекст использования дан в руководстве раздела.

```python
generate_mnemonic_account(*, num_words: 'int' = 12, passphrase: 'str' = '', account_path: 'str' = "m/44'/60'/0'/0/0") -> 'WalletAccount'
```

## checksum

Публичная операция/свойство SDK. Ниже приведены точные типы, значения по умолчанию и тип результата; контекст использования дан в руководстве раздела.

```python
checksum(address: 'str') -> 'str'
```
