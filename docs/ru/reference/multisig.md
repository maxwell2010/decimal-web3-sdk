# multisig

[Index](../api.md)

Сигнатуры сформированы из кода релиза. Обязательные поля не имеют значения по умолчанию.

## WeightedOwner

Публичная операция/свойство SDK. Ниже приведены точные типы, значения по умолчанию и тип результата; контекст использования дан в руководстве раздела.

```python
WeightedOwner(owner: 'str', weight: 'int' = 1) -> None
```

- `owner`: `str`; required.
- `weight`: `int`; 1.

## SafeTransaction

Публичная операция/свойство SDK. Ниже приведены точные типы, значения по умолчанию и тип результата; контекст использования дан в руководстве раздела.

```python
SafeTransaction(to: 'str', nonce: 'int', value_wei: 'int' = 0, data: 'str' = '0x', operation: 'Literal[0, 1]' = 0, safe_tx_gas: 'int' = 0, base_gas: 'int' = 0, gas_price_wei: 'int' = 0, gas_token: 'str' = '0x0000000000000000000000000000000000000000', refund_receiver: 'str' = '0x0000000000000000000000000000000000000000') -> None
```

- `to`: `str`; required.
- `nonce`: `int`; required.
- `value_wei`: `int`; 0.
- `data`: `str`; '0x'.
- `operation`: `Literal[0, 1]`; 0.
- `safe_tx_gas`: `int`; 0.
- `base_gas`: `int`; 0.
- `gas_price_wei`: `int`; 0.
- `gas_token`: `str`; '0x0000000000000000000000000000000000000000'.
- `refund_receiver`: `str`; '0x0000000000000000000000000000000000000000'.

### values

Публичная операция/свойство SDK. Ниже приведены точные типы, значения по умолчанию и тип результата; контекст использования дан в руководстве раздела.

```python
values(self) -> 'tuple'
```

## safe_typed_data

Публичная операция/свойство SDK. Ниже приведены точные типы, значения по умолчанию и тип результата; контекст использования дан в руководстве раздела.

```python
safe_typed_data(safe: 'str', chain_id: 'int', transaction: 'SafeTransaction')
```

## safe_transaction_hash

Публичная операция/свойство SDK. Ниже приведены точные типы, значения по умолчанию и тип результата; контекст использования дан в руководстве раздела.

```python
safe_transaction_hash(safe: 'str', chain_id: 'int', transaction: 'SafeTransaction') -> 'str'
```

## SafeSignature

Публичная операция/свойство SDK. Ниже приведены точные типы, значения по умолчанию и тип результата; контекст использования дан в руководстве раздела.

```python
SafeSignature(signer: 'str', data: 'str', kind: "Literal['eip712', 'eth_sign', 'approved_hash', 'contract']" = 'eip712') -> None
```

- `signer`: `str`; required.
- `data`: `str`; required.
- `kind`: `Literal['eip712', 'eth_sign', 'approved_hash', 'contract']`; 'eip712'.

### preapproved

Публичная операция/свойство SDK. Ниже приведены точные типы, значения по умолчанию и тип результата; контекст использования дан в руководстве раздела.

```python
preapproved(signer: 'str') -> "'SafeSignature'"
```

## SignSafeTransactionRequest

Публичная операция/свойство SDK. Ниже приведены точные типы, значения по умолчанию и тип результата; контекст использования дан в руководстве раздела.

```python
SignSafeTransactionRequest(safe: 'str', chain_id: 'int', transaction: 'SafeTransaction', private_key: 'str') -> None
```

- `safe`: `str`; required.
- `chain_id`: `int`; required.
- `transaction`: `SafeTransaction`; required.
- `private_key`: `str`; use from_mnemonic; technical field, hidden in repr.

### from_mnemonic

Локально получить технический ключ подписи; поля запроса передаются именованными аргументами.

```python
from_mnemonic(*, mnemonic: 'str', passphrase: 'str' = '', account_path: 'str' = "m/44'/60'/0'/0/0", account_index: 'int | None' = None, **kwargs) -> 'T'
```

## sign_safe_transaction

Публичная операция/свойство SDK. Ниже приведены точные типы, значения по умолчанию и тип результата; контекст использования дан в руководстве раздела.

```python
sign_safe_transaction(request: 'SignSafeTransactionRequest') -> 'SafeSignature'
```

## pack_safe_signatures

Публичная операция/свойство SDK. Ниже приведены точные типы, значения по умолчанию и тип результата; контекст использования дан в руководстве раздела.

```python
pack_safe_signatures(safe: 'str', chain_id: 'int', transaction: 'SafeTransaction', signatures: 'tuple[SafeSignature, ...]') -> 'bytes'
```

## CreateMultisigRequest

Публичная операция/свойство SDK. Ниже приведены точные типы, значения по умолчанию и тип результата; контекст использования дан в руководстве раздела.

```python
CreateMultisigRequest(owners: 'tuple[WeightedOwner, ...]', weight_threshold: 'int', salt_nonce: 'int', fallback_handler: 'str' = '0x0000000000000000000000000000000000000000', *, private_key: 'str') -> None
```

- `private_key`: `str`; use from_mnemonic; technical field, hidden in repr.
- `owners`: `tuple[WeightedOwner, ...]`; required.
- `weight_threshold`: `int`; required.
- `salt_nonce`: `int`; required.
- `fallback_handler`: `str`; '0x0000000000000000000000000000000000000000'.

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

## ApproveMultisigTransactionRequest

Публичная операция/свойство SDK. Ниже приведены точные типы, значения по умолчанию и тип результата; контекст использования дан в руководстве раздела.

```python
ApproveMultisigTransactionRequest(safe: 'str', transaction: 'SafeTransaction', *, private_key: 'str') -> None
```

- `private_key`: `str`; use from_mnemonic; technical field, hidden in repr.
- `safe`: `str`; required.
- `transaction`: `SafeTransaction`; required.

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

## ExecuteMultisigTransactionRequest

Публичная операция/свойство SDK. Ниже приведены точные типы, значения по умолчанию и тип результата; контекст использования дан в руководстве раздела.

```python
ExecuteMultisigTransactionRequest(safe: 'str', transaction: 'SafeTransaction', signatures: 'tuple[SafeSignature, ...]', *, private_key: 'str') -> None
```

- `private_key`: `str`; use from_mnemonic; technical field, hidden in repr.
- `safe`: `str`; required.
- `transaction`: `SafeTransaction`; required.
- `signatures`: `tuple[SafeSignature, ...]`; required.

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

## MultisigState

Публичная операция/свойство SDK. Ниже приведены точные типы, значения по умолчанию и тип результата; контекст использования дан в руководстве раздела.

```python
MultisigState(nonce: 'int', owners: 'tuple[WeightedOwner, ...]', weight_threshold: 'int', block_number: 'int') -> None
```

- `nonce`: `int`; required.
- `owners`: `tuple[WeightedOwner, ...]`; required.
- `weight_threshold`: `int`; required.
- `block_number`: `int`; required.

## MultisigService

Публичная операция/свойство SDK. Ниже приведены точные типы, значения по умолчанию и тип результата; контекст использования дан в руководстве раздела.

### approve_transaction

Публичная операция/свойство SDK. Ниже приведены точные типы, значения по умолчанию и тип результата; контекст использования дан в руководстве раздела.

```python
async approve_transaction(self, request: 'ApproveMultisigTransactionRequest', broadcast: 'bool' = False, wait_receipt: 'bool' = False) -> 'TransactionResult'
```

### build_operation

Подготовка calldata/черновика без отправки. Единицы и ограничения ABI описаны в руководстве раздела.

```python
async build_operation(self, request: 'ContractOperationRequest') -> 'TransactionDraft'
```

### build_transaction

Подготовка calldata/черновика без отправки. Единицы и ограничения ABI описаны в руководстве раздела.

```python
async build_transaction(self, safe: 'str', call: 'ContractCallRequest | TransactionDraft', *, nonce: 'int | None' = None) -> 'SafeTransaction'
```

### check_execution_result

Публичная операция/свойство SDK. Ниже приведены точные типы, значения по умолчанию и тип результата; контекст использования дан в руководстве раздела.

```python
check_execution_result(self, safe: 'str', transaction: 'SafeTransaction', result: 'TransactionResult') -> 'TransactionResult'
```

### create

Публичная операция/свойство SDK. Ниже приведены точные типы, значения по умолчанию и тип результата; контекст использования дан в руководстве раздела.

```python
async create(self, request: 'CreateMultisigRequest', broadcast: 'bool' = False, wait_receipt: 'bool' = False) -> 'TransactionResult'
```

### execute

Публичная операция/свойство SDK. Ниже приведены точные типы, значения по умолчанию и тип результата; контекст использования дан в руководстве раздела.

```python
async execute(self, request: 'ExecuteMultisigTransactionRequest', broadcast: 'bool' = False, wait_receipt: 'bool' = False) -> 'TransactionResult'
```

### state

Публичная операция/свойство SDK. Ниже приведены точные типы, значения по умолчанию и тип результата; контекст использования дан в руководстве раздела.

```python
async state(self, safe: 'str') -> 'MultisigState'
```
