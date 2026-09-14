# bridge

[Index](../api.md)

Сигнатуры сформированы из кода релиза. Обязательные поля не имеют значения по умолчанию.

## BridgeTransferNativeRequest

Публичная операция/свойство SDK. Ниже приведены точные типы, значения по умолчанию и тип результата; контекст использования дан в руководстве раздела.

```python
BridgeTransferNativeRequest(contract: 'str', to: 'str', amount_wei: 'int', service_fee_wei: 'int', to_chain_id: 'int', nonce: 'int', private_key: 'str') -> None
```

- `contract`: `str`; required.
- `to`: `str`; required.
- `amount_wei`: `int`; required.
- `service_fee_wei`: `int`; required.
- `to_chain_id`: `int`; required.
- `nonce`: `int`; required.
- `private_key`: `str`; use from_mnemonic; technical field, hidden in repr.

### from_mnemonic

Локально получить технический ключ подписи; поля запроса передаются именованными аргументами.

```python
from_mnemonic(*, mnemonic: 'str', passphrase: 'str' = '', account_path: 'str' = "m/44'/60'/0'/0/0", account_index: 'int | None' = None, **kwargs) -> 'T'
```

## BridgeTransferTokenRequest

Публичная операция/свойство SDK. Ниже приведены точные типы, значения по умолчанию и тип результата; контекст использования дан в руководстве раздела.

```python
BridgeTransferTokenRequest(contract: 'str', token: 'str', to: 'str', amount_raw: 'int', service_fee_wei: 'int', to_chain_id: 'int', nonce: 'int', private_key: 'str') -> None
```

- `contract`: `str`; required.
- `token`: `str`; required.
- `to`: `str`; required.
- `amount_raw`: `int`; required.
- `service_fee_wei`: `int`; required.
- `to_chain_id`: `int`; required.
- `nonce`: `int`; required.
- `private_key`: `str`; use from_mnemonic; technical field, hidden in repr.

### from_mnemonic

Локально получить технический ключ подписи; поля запроса передаются именованными аргументами.

```python
from_mnemonic(*, mnemonic: 'str', passphrase: 'str' = '', account_path: 'str' = "m/44'/60'/0'/0/0", account_index: 'int | None' = None, **kwargs) -> 'T'
```

## BridgeCompleteTransferRequest

Публичная операция/свойство SDK. Ниже приведены точные типы, значения по умолчанию и тип результата; контекст использования дан в руководстве раздела.

```python
BridgeCompleteTransferRequest(contract: 'str', encoded_vm: 'str', unwrap_weth: 'bool', private_key: 'str') -> None
```

- `contract`: `str`; required.
- `encoded_vm`: `str`; required.
- `unwrap_weth`: `bool`; required.
- `private_key`: `str`; use from_mnemonic; technical field, hidden in repr.

### from_mnemonic

Локально получить технический ключ подписи; поля запроса передаются именованными аргументами.

```python
from_mnemonic(*, mnemonic: 'str', passphrase: 'str' = '', account_path: 'str' = "m/44'/60'/0'/0/0", account_index: 'int | None' = None, **kwargs) -> 'T'
```

## BridgeService

Публичная операция/свойство SDK. Ниже приведены точные типы, значения по умолчанию и тип результата; контекст использования дан в руководстве раздела.

### complete_transfer

Публичная операция/свойство SDK. Ниже приведены точные типы, значения по умолчанию и тип результата; контекст использования дан в руководстве раздела.

```python
async complete_transfer(self, request: 'BridgeCompleteTransferRequest', broadcast: 'bool' = False, wait_receipt: 'bool' = False) -> 'TransactionResult'
```

### transfer_native

Публичная операция/свойство SDK. Ниже приведены точные типы, значения по умолчанию и тип результата; контекст использования дан в руководстве раздела.

```python
async transfer_native(self, request: 'BridgeTransferNativeRequest', broadcast: 'bool' = False, wait_receipt: 'bool' = False) -> 'TransactionResult'
```

### transfer_token

Публичная операция/свойство SDK. Ниже приведены точные типы, значения по умолчанию и тип результата; контекст использования дан в руководстве раздела.

```python
async transfer_token(self, request: 'BridgeTransferTokenRequest', broadcast: 'bool' = False, wait_receipt: 'bool' = False) -> 'TransactionResult'
```
