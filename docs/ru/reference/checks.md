# checks

[Index](../api.md)

Сигнатуры сформированы из кода релиза. Обязательные поля не имеют значения по умолчанию.

## CreateChecksDelRequest

Публичная операция/свойство SDK. Ниже приведены точные типы, значения по умолчанию и тип результата; контекст использования дан в руководстве раздела.

```python
CreateChecksDelRequest(contract: 'str', signers: 'list[str]', amount_wei: 'int', due_block: 'int', private_key: 'str', nonce: 'int | None' = None) -> None
```

- `contract`: `str`; required.
- `signers`: `list[str]`; required.
- `amount_wei`: `int`; required.
- `due_block`: `int`; required.
- `private_key`: `str`; use from_mnemonic; technical field, hidden in repr.
- `nonce`: `int | None`; None.

### from_mnemonic

Локально получить технический ключ подписи; поля запроса передаются именованными аргументами.

```python
from_mnemonic(*, mnemonic: 'str', passphrase: 'str' = '', account_path: 'str' = "m/44'/60'/0'/0/0", account_index: 'int | None' = None, **kwargs) -> 'T'
```

## CreateChecksTokenRequest

Публичная операция/свойство SDK. Ниже приведены точные типы, значения по умолчанию и тип результата; контекст использования дан в руководстве раздела.

```python
CreateChecksTokenRequest(contract: 'str', token: 'str', signers: 'list[str]', amount_raw: 'int', due_block: 'int', private_key: 'str', nonce: 'int | None' = None, permit: 'PermitSignature | None' = None) -> None
```

- `contract`: `str`; required.
- `token`: `str`; required.
- `signers`: `list[str]`; required.
- `amount_raw`: `int`; required.
- `due_block`: `int`; required.
- `private_key`: `str`; use from_mnemonic; technical field, hidden in repr.
- `nonce`: `int | None`; None.
- `permit`: `PermitSignature | None`; None.

### from_mnemonic

Локально получить технический ключ подписи; поля запроса передаются именованными аргументами.

```python
from_mnemonic(*, mnemonic: 'str', passphrase: 'str' = '', account_path: 'str' = "m/44'/60'/0'/0/0", account_index: 'int | None' = None, **kwargs) -> 'T'
```

## RedeemChecksRequest

Публичная операция/свойство SDK. Ниже приведены точные типы, значения по умолчанию и тип результата; контекст использования дан в руководстве раздела.

```python
RedeemChecksRequest(contract: 'str', signatures: 'list[str]', checks: 'list[str]', private_key: 'str') -> None
```

- `contract`: `str`; required.
- `signatures`: `list[str]`; required.
- `checks`: `list[str]`; required.
- `private_key`: `str`; use from_mnemonic; technical field, hidden in repr.

### from_mnemonic

Локально получить технический ключ подписи; поля запроса передаются именованными аргументами.

```python
from_mnemonic(*, mnemonic: 'str', passphrase: 'str' = '', account_path: 'str' = "m/44'/60'/0'/0/0", account_index: 'int | None' = None, **kwargs) -> 'T'
```

## ChecksService

Публичная операция/свойство SDK. Ниже приведены точные типы, значения по умолчанию и тип результата; контекст использования дан в руководстве раздела.

### create_del

Публичная операция/свойство SDK. Ниже приведены точные типы, значения по умолчанию и тип результата; контекст использования дан в руководстве раздела.

```python
async create_del(self, request: 'CreateChecksDelRequest', broadcast: 'bool' = False, wait_receipt: 'bool' = False) -> 'TransactionResult'
```

### create_token

Публичная операция/свойство SDK. Ниже приведены точные типы, значения по умолчанию и тип результата; контекст использования дан в руководстве раздела.

```python
async create_token(self, request: 'CreateChecksTokenRequest', broadcast: 'bool' = False, wait_receipt: 'bool' = False) -> 'TransactionResult'
```

### redeem

Публичная операция/свойство SDK. Ниже приведены точные типы, значения по умолчанию и тип результата; контекст использования дан в руководстве раздела.

```python
async redeem(self, request: 'RedeemChecksRequest', broadcast: 'bool' = False, wait_receipt: 'bool' = False) -> 'TransactionResult'
```
