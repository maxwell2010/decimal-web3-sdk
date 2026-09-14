# transactions

[Index](../api.md)

Сигнатуры сформированы из кода релиза. Обязательные поля не имеют значения по умолчанию.

## MemoCapability

Публичная операция/свойство SDK. Ниже приведены точные типы, значения по умолчанию и тип результата; контекст использования дан в руководстве раздела.

```python
MemoCapability(transaction_type: 'str', supported: 'bool', request_field: 'str | None', transport: 'str', notes: 'str') -> None
```

- `transaction_type`: `str`; required.
- `supported`: `bool`; required.
- `request_field`: `str | None`; required.
- `transport`: `str`; required.
- `notes`: `str`; required.

## memo_capabilities

Публичная операция/свойство SDK. Ниже приведены точные типы, значения по умолчанию и тип результата; контекст использования дан в руководстве раздела.

```python
memo_capabilities() -> 'tuple[MemoCapability, ...]'
```

## memo_supported_for

Публичная операция/свойство SDK. Ниже приведены точные типы, значения по умолчанию и тип результата; контекст использования дан в руководстве раздела.

```python
memo_supported_for(transaction_type: 'str') -> 'bool'
```

## encode_memo_data

Публичная операция/свойство SDK. Ниже приведены точные типы, значения по умолчанию и тип результата; контекст использования дан в руководстве раздела.

```python
encode_memo_data(memo: 'str | None') -> 'str'
```

## decode_memo_data

Публичная операция/свойство SDK. Ниже приведены точные типы, значения по умолчанию и тип результата; контекст использования дан в руководстве раздела.

```python
decode_memo_data(data: 'str | None') -> 'str | None'
```

## NativeTransferRequest

Публичная операция/свойство SDK. Ниже приведены точные типы, значения по умолчанию и тип результата; контекст использования дан в руководстве раздела.

```python
NativeTransferRequest(to: 'str', amount_del: 'Decimal | str | int', private_key: 'str', memo: 'str | None' = None, gas: 'int | None' = None, gas_price_wei: 'int | None' = None) -> None
```

- `to`: `str`; required.
- `amount_del`: `Decimal | str | int`; required.
- `private_key`: `str`; use from_mnemonic; technical field, hidden in repr.
- `memo`: `str | None`; None.
- `gas`: `int | None`; None.
- `gas_price_wei`: `int | None`; None.

### from_mnemonic

Локально получить технический ключ подписи; поля запроса передаются именованными аргументами.

```python
from_mnemonic(*, to: 'str', amount_del: 'Decimal | str | int', mnemonic: 'str', passphrase: 'str' = '', account_path: 'str' = "m/44'/60'/0'/0/0", account_index: 'int | None' = None, memo: 'str | None' = None, gas: 'int | None' = None, gas_price_wei: 'int | None' = None) -> "'NativeTransferRequest'"
```

## ContractCallRequest

Публичная операция/свойство SDK. Ниже приведены точные типы, значения по умолчанию и тип результата; контекст использования дан в руководстве раздела.

```python
ContractCallRequest(contract: 'str', private_key: 'str', data: 'str', value_wei: 'int' = 0, gas: 'int | None' = None, gas_price_wei: 'int | None' = None) -> None
```

- `contract`: `str`; required.
- `private_key`: `str`; use from_mnemonic; technical field, hidden in repr.
- `data`: `str`; required.
- `value_wei`: `int`; 0.
- `gas`: `int | None`; None.
- `gas_price_wei`: `int | None`; None.

### from_mnemonic

Локально получить технический ключ подписи; поля запроса передаются именованными аргументами.

```python
from_mnemonic(*, contract: 'str', data: 'str', mnemonic: 'str', passphrase: 'str' = '', account_path: 'str' = "m/44'/60'/0'/0/0", account_index: 'int | None' = None, value_wei: 'int' = 0, gas: 'int | None' = None, gas_price_wei: 'int | None' = None) -> "'ContractCallRequest'"
```

## Erc20TransferRequest

Публичная операция/свойство SDK. Ниже приведены точные типы, значения по умолчанию и тип результата; контекст использования дан в руководстве раздела.

```python
Erc20TransferRequest(token: 'str', to: 'str', amount: 'Decimal | str | int', private_key: 'str', decimals: 'int | None' = None, gas: 'int | None' = None, gas_price_wei: 'int | None' = None) -> None
```

- `token`: `str`; required.
- `to`: `str`; required.
- `amount`: `Decimal | str | int`; required.
- `private_key`: `str`; use from_mnemonic; technical field, hidden in repr.
- `decimals`: `int | None`; None.
- `gas`: `int | None`; None.
- `gas_price_wei`: `int | None`; None.

### from_mnemonic

Локально получить технический ключ подписи; поля запроса передаются именованными аргументами.

```python
from_mnemonic(*, token: 'str', to: 'str', amount: 'Decimal | str | int', mnemonic: 'str', passphrase: 'str' = '', account_path: 'str' = "m/44'/60'/0'/0/0", account_index: 'int | None' = None, decimals: 'int | None' = None, gas: 'int | None' = None, gas_price_wei: 'int | None' = None) -> "'Erc20TransferRequest'"
```

## Erc20ApproveRequest

Публичная операция/свойство SDK. Ниже приведены точные типы, значения по умолчанию и тип результата; контекст использования дан в руководстве раздела.

```python
Erc20ApproveRequest(token: 'str', spender: 'str', amount: 'Decimal | str | int', private_key: 'str', decimals: 'int | None' = None, gas: 'int | None' = None, gas_price_wei: 'int | None' = None) -> None
```

- `token`: `str`; required.
- `spender`: `str`; required.
- `amount`: `Decimal | str | int`; required.
- `private_key`: `str`; use from_mnemonic; technical field, hidden in repr.
- `decimals`: `int | None`; None.
- `gas`: `int | None`; None.
- `gas_price_wei`: `int | None`; None.

### from_mnemonic

Локально получить технический ключ подписи; поля запроса передаются именованными аргументами.

```python
from_mnemonic(*, token: 'str', spender: 'str', amount: 'Decimal | str | int', mnemonic: 'str', passphrase: 'str' = '', account_path: 'str' = "m/44'/60'/0'/0/0", account_index: 'int | None' = None, decimals: 'int | None' = None, gas: 'int | None' = None, gas_price_wei: 'int | None' = None) -> "'Erc20ApproveRequest'"
```

## Erc20TransferFromRequest

Публичная операция/свойство SDK. Ниже приведены точные типы, значения по умолчанию и тип результата; контекст использования дан в руководстве раздела.

```python
Erc20TransferFromRequest(token: 'str', owner: 'str', to: 'str', amount: 'Decimal | str | int', private_key: 'str', decimals: 'int | None' = None, gas: 'int | None' = None, gas_price_wei: 'int | None' = None) -> None
```

- `token`: `str`; required.
- `owner`: `str`; required.
- `to`: `str`; required.
- `amount`: `Decimal | str | int`; required.
- `private_key`: `str`; use from_mnemonic; technical field, hidden in repr.
- `decimals`: `int | None`; None.
- `gas`: `int | None`; None.
- `gas_price_wei`: `int | None`; None.

### from_mnemonic

Локально получить технический ключ подписи; поля запроса передаются именованными аргументами.

```python
from_mnemonic(*, token: 'str', owner: 'str', to: 'str', amount: 'Decimal | str | int', mnemonic: 'str', passphrase: 'str' = '', account_path: 'str' = "m/44'/60'/0'/0/0", account_index: 'int | None' = None, decimals: 'int | None' = None, gas: 'int | None' = None, gas_price_wei: 'int | None' = None) -> "'Erc20TransferFromRequest'"
```

## TransactionDraft

Публичная операция/свойство SDK. Ниже приведены точные типы, значения по умолчанию и тип результата; контекст использования дан в руководстве раздела.

```python
TransactionDraft(tx: 'dict[str, Any]', from_address: 'str', to_address: 'str', value_wei: 'int', gas: 'int | None' = None, estimated_gas: 'int | None' = None, gas_limit: 'int | None' = None, gas_price_wei: 'int | None' = None, oracle_gas_price_wei: 'int | None' = None, fee_wei: 'int | None' = None, estimated_fee_wei: 'int | None' = None, preflight: "'FeePreflight | None'" = None, raw_tx: 'bytes | None' = None, tx_hash: 'str | None' = None, receipt: 'dict[str, Any] | None' = None, timings_ms: 'dict[str, float]' = <factory>) -> None
```

- `tx`: `dict[str, Any]`; required.
- `from_address`: `str`; required.
- `to_address`: `str`; required.
- `value_wei`: `int`; required.
- `gas`: `int | None`; None.
- `estimated_gas`: `int | None`; None.
- `gas_limit`: `int | None`; None.
- `gas_price_wei`: `int | None`; None.
- `oracle_gas_price_wei`: `int | None`; None.
- `fee_wei`: `int | None`; None.
- `estimated_fee_wei`: `int | None`; None.
- `preflight`: `'FeePreflight | None'`; None.
- `raw_tx`: `bytes | None`; None.
- `tx_hash`: `str | None`; None.
- `receipt`: `dict[str, Any] | None`; None.
- `timings_ms`: `dict[str, float]`; factory: dict.

### fee_del

Публичная операция/свойство SDK. Ниже приведены точные типы, значения по умолчанию и тип результата; контекст использования дан в руководстве раздела.

```python
fee_del: Decimal | None
```

## TransactionResult

Публичная операция/свойство SDK. Ниже приведены точные типы, значения по умолчанию и тип результата; контекст использования дан в руководстве раздела.

```python
TransactionResult(success: 'bool', tx_hash: 'str | None' = None, status: 'str | None' = None, block_number: 'int | None' = None, transaction_index: 'int | None' = None, gas_used: 'int | None' = None, effective_gas_price_wei: 'int | None' = None, oracle_gas_price_wei: 'int | None' = None, effective_fee_wei: 'int | None' = None, effective_fee_del: 'Decimal | None' = None, fee_wei: 'int | None' = None, fee_del: 'Decimal | None' = None, gas: 'int | None' = None, raw_tx_hex: 'str | None' = None, receipt: 'dict[str, Any] | None' = None, events: 'dict[str, Any] | None' = None, token_address: 'str | None' = None, hold_timestamp: 'int | None' = None, hold_time: 'str | None' = None, error: 'str | None' = None, user_message: 'str | None' = None, native_balance_wei: 'int | None' = None, required_wei: 'int | None' = None, missing_wei: 'int | None' = None, token_balance_raw: 'int | None' = None, token_required_raw: 'int | None' = None, token_missing_raw: 'int | None' = None, token_allowance_raw: 'int | None' = None, token_allowance_required_raw: 'int | None' = None, token_allowance_missing_raw: 'int | None' = None) -> None
```

- `success`: `bool`; required.
- `tx_hash`: `str | None`; None.
- `status`: `str | None`; None.
- `block_number`: `int | None`; None.
- `transaction_index`: `int | None`; None.
- `gas_used`: `int | None`; None.
- `effective_gas_price_wei`: `int | None`; None.
- `oracle_gas_price_wei`: `int | None`; None.
- `effective_fee_wei`: `int | None`; None.
- `effective_fee_del`: `Decimal | None`; None.
- `fee_wei`: `int | None`; None.
- `fee_del`: `Decimal | None`; None.
- `gas`: `int | None`; None.
- `raw_tx_hex`: `str | None`; None.
- `receipt`: `dict[str, Any] | None`; None.
- `events`: `dict[str, Any] | None`; None.
- `token_address`: `str | None`; None.
- `hold_timestamp`: `int | None`; None.
- `hold_time`: `str | None`; None.
- `error`: `str | None`; None.
- `user_message`: `str | None`; None.
- `native_balance_wei`: `int | None`; None.
- `required_wei`: `int | None`; None.
- `missing_wei`: `int | None`; None.
- `token_balance_raw`: `int | None`; None.
- `token_required_raw`: `int | None`; None.
- `token_missing_raw`: `int | None`; None.
- `token_allowance_raw`: `int | None`; None.
- `token_allowance_required_raw`: `int | None`; None.
- `token_allowance_missing_raw`: `int | None`; None.

### is_confirmed

Публичная операция/свойство SDK. Ниже приведены точные типы, значения по умолчанию и тип результата; контекст использования дан в руководстве раздела.

```python
is_confirmed: bool
```

### is_pending

Публичная операция/свойство SDK. Ниже приведены точные типы, значения по умолчанию и тип результата; контекст использования дан в руководстве раздела.

```python
is_pending: bool
```

### is_successful

Публичная операция/свойство SDK. Ниже приведены точные типы, значения по умолчанию и тип результата; контекст использования дан в руководстве раздела.

```python
is_successful: bool
```

## FeePreflight

Публичная операция/свойство SDK. Ниже приведены точные типы, значения по умолчанию и тип результата; контекст использования дан в руководстве раздела.

```python
FeePreflight(ok: 'bool', from_address: 'str', native_balance_wei: 'int', value_wei: 'int', fee_wei: 'int', required_wei: 'int', missing_wei: 'int' = 0, gas: 'int | None' = None, estimated_gas: 'int | None' = None, gas_price_wei: 'int | None' = None, oracle_gas_price_wei: 'int | None' = None, estimated_fee_wei: 'int | None' = None, gas_limit: 'int | None' = None, gas_limit_fee_wei: 'int | None' = None, exact: 'bool' = False) -> None
```

- `ok`: `bool`; required.
- `from_address`: `str`; required.
- `native_balance_wei`: `int`; required.
- `value_wei`: `int`; required.
- `fee_wei`: `int`; required.
- `required_wei`: `int`; required.
- `missing_wei`: `int`; 0.
- `gas`: `int | None`; None.
- `estimated_gas`: `int | None`; None.
- `gas_price_wei`: `int | None`; None.
- `oracle_gas_price_wei`: `int | None`; None.
- `estimated_fee_wei`: `int | None`; None.
- `gas_limit`: `int | None`; None.
- `gas_limit_fee_wei`: `int | None`; None.
- `exact`: `bool`; False.

### estimated_fee_del

Публичная операция/свойство SDK. Ниже приведены точные типы, значения по умолчанию и тип результата; контекст использования дан в руководстве раздела.

```python
estimated_fee_del: Decimal | None
```

### fee_del

Публичная операция/свойство SDK. Ниже приведены точные типы, значения по умолчанию и тип результата; контекст использования дан в руководстве раздела.

```python
fee_del: Decimal
```

### gas_limit_fee_del

Публичная операция/свойство SDK. Ниже приведены точные типы, значения по умолчанию и тип результата; контекст использования дан в руководстве раздела.

```python
gas_limit_fee_del: Decimal | None
```

### minimum_fee_del

Публичная операция/свойство SDK. Ниже приведены точные типы, значения по умолчанию и тип результата; контекст использования дан в руководстве раздела.

```python
minimum_fee_del: Decimal
```

### minimum_fee_wei

Публичная операция/свойство SDK. Ниже приведены точные типы, значения по умолчанию и тип результата; контекст использования дан в руководстве раздела.

```python
minimum_fee_wei: int
```

### missing_del

Публичная операция/свойство SDK. Ниже приведены точные типы, значения по умолчанию и тип результата; контекст использования дан в руководстве раздела.

```python
missing_del: Decimal
```

### native_balance_del

Публичная операция/свойство SDK. Ниже приведены точные типы, значения по умолчанию и тип результата; контекст использования дан в руководстве раздела.

```python
native_balance_del: Decimal
```

### required_del

Публичная операция/свойство SDK. Ниже приведены точные типы, значения по умолчанию и тип результата; контекст использования дан в руководстве раздела.

```python
required_del: Decimal
```

### value_del

Публичная операция/свойство SDK. Ниже приведены точные типы, значения по умолчанию и тип результата; контекст использования дан в руководстве раздела.

```python
value_del: Decimal
```

## TransactionService

Публичная операция/свойство SDK. Ниже приведены точные типы, значения по умолчанию и тип результата; контекст использования дан в руководстве раздела.

### approve_erc20

Публичная операция/свойство SDK. Ниже приведены точные типы, значения по умолчанию и тип результата; контекст использования дан в руководстве раздела.

```python
async approve_erc20(self, request: 'Erc20ApproveRequest', broadcast: 'bool' = False, wait_receipt: 'bool' = False) -> 'TransactionResult'
```

### broadcast

Отправить подписанную транзакцию; расходует средства. Сначала изучите комиссии и ограничения.

```python
async broadcast(self, draft: 'TransactionDraft') -> 'TransactionDraft'
```

### broadcast_with_fee_retry

Отправить подписанную транзакцию; расходует средства. Сначала изучите комиссии и ограничения.

```python
async broadcast_with_fee_retry(self, draft: 'TransactionDraft', private_key: 'str') -> 'TransactionDraft'
```

### build_contract_call

Подготовка calldata/черновика без отправки. Единицы и ограничения ABI описаны в руководстве раздела.

```python
async build_contract_call(self, request: 'ContractCallRequest') -> 'TransactionDraft'
```

### build_erc20_approve

Подготовка calldata/черновика без отправки. Единицы и ограничения ABI описаны в руководстве раздела.

```python
async build_erc20_approve(self, request: 'Erc20ApproveRequest') -> 'TransactionDraft'
```

### build_erc20_transfer

Подготовка calldata/черновика без отправки. Единицы и ограничения ABI описаны в руководстве раздела.

```python
async build_erc20_transfer(self, request: 'Erc20TransferRequest') -> 'TransactionDraft'
```

### build_erc20_transfer_from

Подготовка calldata/черновика без отправки. Единицы и ограничения ABI описаны в руководстве раздела.

```python
async build_erc20_transfer_from(self, request: 'Erc20TransferFromRequest') -> 'TransactionDraft'
```

### build_native_transfer

Подготовка calldata/черновика без отправки. Единицы и ограничения ABI описаны в руководстве раздела.

```python
async build_native_transfer(self, request: 'NativeTransferRequest') -> 'TransactionDraft'
```

### calculate_fee

Публичная операция/свойство SDK. Ниже приведены точные типы, значения по умолчанию и тип результата; контекст использования дан в руководстве раздела.

```python
async calculate_fee(self, draft: 'TransactionDraft', *, exact: 'bool' = False) -> 'FeePreflight'
```

### estimate

Публичная операция/свойство SDK. Ниже приведены точные типы, значения по умолчанию и тип результата; контекст использования дан в руководстве раздела.

```python
async estimate(self, draft: 'TransactionDraft', *, exact: 'bool' = False) -> 'TransactionDraft'
```

### estimate_fee_for_contract_call

Расчет gas и необходимого баланса без подписи; RPC-симуляция может завершиться revert.

```python
async estimate_fee_for_contract_call(self, request: 'ContractCallRequest', *, exact: 'bool' = False) -> 'FeePreflight'
```

### estimate_fee_for_erc20_approve

Расчет gas и необходимого баланса без подписи; RPC-симуляция может завершиться revert.

```python
async estimate_fee_for_erc20_approve(self, request: 'Erc20ApproveRequest', *, exact: 'bool' = False) -> 'FeePreflight'
```

### estimate_fee_for_erc20_transfer

Расчет gas и необходимого баланса без подписи; RPC-симуляция может завершиться revert.

```python
async estimate_fee_for_erc20_transfer(self, request: 'Erc20TransferRequest', *, exact: 'bool' = False) -> 'FeePreflight'
```

### estimate_fee_for_erc20_transfer_from

Расчет gas и необходимого баланса без подписи; RPC-симуляция может завершиться revert.

```python
async estimate_fee_for_erc20_transfer_from(self, request: 'Erc20TransferFromRequest', *, exact: 'bool' = False) -> 'FeePreflight'
```

### estimate_fee_for_native_transfer

Расчет gas и необходимого баланса без подписи; RPC-симуляция может завершиться revert.

```python
async estimate_fee_for_native_transfer(self, request: 'NativeTransferRequest', *, exact: 'bool' = False) -> 'FeePreflight'
```

### preflight_fee

Публичная операция/свойство SDK. Ниже приведены точные типы, значения по умолчанию и тип результата; контекст использования дан в руководстве раздела.

```python
async preflight_fee(self, draft: 'TransactionDraft') -> 'FeePreflight'
```

### send_del

Публичная операция/свойство SDK. Ниже приведены точные типы, значения по умолчанию и тип результата; контекст использования дан в руководстве раздела.

```python
async send_del(self, request: 'NativeTransferRequest', broadcast: 'bool' = False, wait_receipt: 'bool' = False) -> 'TransactionResult'
```

### send_draft

Публичная операция/свойство SDK. Ниже приведены точные типы, значения по умолчанию и тип результата; контекст использования дан в руководстве раздела.

```python
async send_draft(self, draft: 'TransactionDraft', private_key: 'str', broadcast: 'bool', wait_receipt: 'bool') -> 'TransactionResult'
```

### send_erc20

Публичная операция/свойство SDK. Ниже приведены точные типы, значения по умолчанию и тип результата; контекст использования дан в руководстве раздела.

```python
async send_erc20(self, request: 'Erc20TransferRequest', broadcast: 'bool' = False, wait_receipt: 'bool' = False) -> 'TransactionResult'
```

### sign

Создать локальную подпись без автоматической отправки. Подписанные данные являются чувствительными.

```python
async sign(self, draft: 'TransactionDraft', private_key: 'str') -> 'TransactionDraft'
```

### transfer_from_erc20

Публичная операция/свойство SDK. Ниже приведены точные типы, значения по умолчанию и тип результата; контекст использования дан в руководстве раздела.

```python
async transfer_from_erc20(self, request: 'Erc20TransferFromRequest', broadcast: 'bool' = False, wait_receipt: 'bool' = False) -> 'TransactionResult'
```

### wait_receipt

Публичная операция/свойство SDK. Ниже приведены точные типы, значения по умолчанию и тип результата; контекст использования дан в руководстве раздела.

```python
async wait_receipt(self, draft: 'TransactionDraft', timeout_seconds: 'float' = 7.0, poll_seconds: 'float' = 3.0) -> 'TransactionDraft'
```

## user_message_from_error

Публичная операция/свойство SDK. Ниже приведены точные типы, значения по умолчанию и тип результата; контекст использования дан в руководстве раздела.

```python
user_message_from_error(error: 'str | None') -> 'str | None'
```
