# validator_operations

[Index](../api.md)

Сигнатуры сформированы из кода релиза. Обязательные поля не имеют значения по умолчанию.

## ValidatorDescription

Публичная операция/свойство SDK. Ниже приведены точные типы, значения по умолчанию и тип результата; контекст использования дан в руководстве раздела.

```python
ValidatorDescription(moniker: 'str', identity: 'str' = '', website: 'str' = '', security_contact: 'str' = '', details: 'str' = '') -> None
```

- `moniker`: `str`; required.
- `identity`: `str`; ''.
- `website`: `str`; ''.
- `security_contact`: `str`; ''.
- `details`: `str`; ''.

## ValidatorMetadata

Публичная операция/свойство SDK. Ниже приведены точные типы, значения по умолчанию и тип результата; контекст использования дан в руководстве раздела.

```python
ValidatorMetadata(operator_address: 'str', reward_address: 'str', consensus_pubkey: 'str', description: 'ValidatorDescription', commission: 'str') -> None
```

- `operator_address`: `str`; required.
- `reward_address`: `str`; required.
- `consensus_pubkey`: `str`; required.
- `description`: `ValidatorDescription`; required.
- `commission`: `str`; required.

### from_dict

Публичная операция/свойство SDK. Ниже приведены точные типы, значения по умолчанию и тип результата; контекст использования дан в руководстве раздела.

```python
from_dict(value: 'dict') -> "'ValidatorMetadata'"
```

### to_json

Публичная операция/свойство SDK. Ниже приведены точные типы, значения по умолчанию и тип результата; контекст использования дан в руководстве раздела.

```python
to_json(self) -> 'str'
```

## AddValidatorTokenRequest

Публичная операция/свойство SDK. Ниже приведены точные типы, значения по умолчанию и тип результата; контекст использования дан в руководстве раздела.

```python
AddValidatorTokenRequest(metadata: 'ValidatorMetadata', token: 'str', amount_raw: 'int', *, private_key: 'str') -> None
```

- `private_key`: `str`; use from_mnemonic; technical field, hidden in repr.
- `metadata`: `ValidatorMetadata`; required.
- `token`: `str`; required.
- `amount_raw`: `int`; required.

### from_mnemonic

Локально получить технический ключ подписи; поля запроса передаются именованными аргументами.

```python
from_mnemonic(*, mnemonic: 'str', passphrase: 'str' = '', account_path: 'str' = "m/44'/60'/0'/0/0", account_index: 'int | None' = None, **kwargs) -> 'T'
```

### to_contract_call

Публичная операция/свойство SDK. Ниже приведены точные типы, значения по умолчанию и тип результата; контекст использования дан в руководстве раздела.

```python
to_contract_call(self, client)
```

## AddValidatorDelRequest

Публичная операция/свойство SDK. Ниже приведены точные типы, значения по умолчанию и тип результата; контекст использования дан в руководстве раздела.

```python
AddValidatorDelRequest(metadata: 'ValidatorMetadata', amount_del: 'Decimal | str | int', *, private_key: 'str') -> None
```

- `private_key`: `str`; use from_mnemonic; technical field, hidden in repr.
- `metadata`: `ValidatorMetadata`; required.
- `amount_del`: `Decimal | str | int`; required.

### from_mnemonic

Локально получить технический ключ подписи; поля запроса передаются именованными аргументами.

```python
from_mnemonic(*, mnemonic: 'str', passphrase: 'str' = '', account_path: 'str' = "m/44'/60'/0'/0/0", account_index: 'int | None' = None, **kwargs) -> 'T'
```

### to_contract_call

Публичная операция/свойство SDK. Ниже приведены точные типы, значения по умолчанию и тип результата; контекст использования дан в руководстве раздела.

```python
to_contract_call(self, client)
```

## RemoveValidatorRequest

Публичная операция/свойство SDK. Ниже приведены точные типы, значения по умолчанию и тип результата; контекст использования дан в руководстве раздела.

```python
RemoveValidatorRequest(validator: 'str', *, private_key: 'str') -> None
```

- `private_key`: `str`; use from_mnemonic; technical field, hidden in repr.
- `validator`: `str`; required.

### from_mnemonic

Локально получить технический ключ подписи; поля запроса передаются именованными аргументами.

```python
from_mnemonic(*, mnemonic: 'str', passphrase: 'str' = '', account_path: 'str' = "m/44'/60'/0'/0/0", account_index: 'int | None' = None, **kwargs) -> 'T'
```

### to_contract_call

Публичная операция/свойство SDK. Ниже приведены точные типы, значения по умолчанию и тип результата; контекст использования дан в руководстве раздела.

```python
to_contract_call(self, client)
```

## UpdateValidatorMetadataRequest

Публичная операция/свойство SDK. Ниже приведены точные типы, значения по умолчанию и тип результата; контекст использования дан в руководстве раздела.

```python
UpdateValidatorMetadataRequest(metadata: 'ValidatorMetadata', *, private_key: 'str') -> None
```

- `private_key`: `str`; use from_mnemonic; technical field, hidden in repr.
- `metadata`: `ValidatorMetadata`; required.

### from_mnemonic

Локально получить технический ключ подписи; поля запроса передаются именованными аргументами.

```python
from_mnemonic(*, mnemonic: 'str', passphrase: 'str' = '', account_path: 'str' = "m/44'/60'/0'/0/0", account_index: 'int | None' = None, **kwargs) -> 'T'
```

### to_contract_call

Публичная операция/свойство SDK. Ниже приведены точные типы, значения по умолчанию и тип результата; контекст использования дан в руководстве раздела.

```python
to_contract_call(self, client)
```

## ValidatorOperations

Публичная операция/свойство SDK. Ниже приведены точные типы, значения по умолчанию и тип результата; контекст использования дан в руководстве раздела.

### add_validator_del

Публичная операция/свойство SDK. Ниже приведены точные типы, значения по умолчанию и тип результата; контекст использования дан в руководстве раздела.

```python
async add_validator_del(self, request: 'AddValidatorDelRequest', broadcast: 'bool' = False, wait_receipt: 'bool' = False) -> 'TransactionResult'
```

### add_validator_token

Публичная операция/свойство SDK. Ниже приведены точные типы, значения по умолчанию и тип результата; контекст использования дан в руководстве раздела.

```python
async add_validator_token(self, request: 'AddValidatorTokenRequest', broadcast: 'bool' = False, wait_receipt: 'bool' = False) -> 'TransactionResult'
```

### remove_validator

Публичная операция/свойство SDK. Ниже приведены точные типы, значения по умолчанию и тип результата; контекст использования дан в руководстве раздела.

```python
async remove_validator(self, request: 'RemoveValidatorRequest', broadcast: 'bool' = False, wait_receipt: 'bool' = False) -> 'TransactionResult'
```

### update_validator_metadata

Публичная операция/свойство SDK. Ниже приведены точные типы, значения по умолчанию и тип результата; контекст использования дан в руководстве раздела.

```python
async update_validator_metadata(self, request: 'UpdateValidatorMetadataRequest', broadcast: 'bool' = False, wait_receipt: 'bool' = False) -> 'TransactionResult'
```
