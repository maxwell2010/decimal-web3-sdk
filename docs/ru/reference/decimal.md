# decimal

[Index](../api.md)

Сигнатуры сформированы из кода релиза. Обязательные поля не имеют значения по умолчанию.

## DelegateDelRequest

Публичная операция/свойство SDK. Ниже приведены точные типы, значения по умолчанию и тип результата; контекст использования дан в руководстве раздела.

```python
DelegateDelRequest(validator: 'str', amount_del: 'Decimal | str | int', private_key: 'str') -> None
```

- `validator`: `str`; required.
- `amount_del`: `Decimal | str | int`; required.
- `private_key`: `str`; use from_mnemonic; technical field, hidden in repr.

### from_mnemonic

Локально получить технический ключ подписи; поля запроса передаются именованными аргументами.

```python
from_mnemonic(*, mnemonic: 'str', passphrase: 'str' = '', account_path: 'str' = "m/44'/60'/0'/0/0", account_index: 'int | None' = None, **kwargs) -> 'T'
```

## HoldDelRequest

Публичная операция/свойство SDK. Ниже приведены точные типы, значения по умолчанию и тип результата; контекст использования дан в руководстве раздела.

```python
HoldDelRequest(validator: 'str', amount_del: 'Decimal | str | int', hold_timestamp: 'int', private_key: 'str') -> None
```

- `validator`: `str`; required.
- `amount_del`: `Decimal | str | int`; required.
- `hold_timestamp`: `int`; required.
- `private_key`: `str`; use from_mnemonic; technical field, hidden in repr.

### from_mnemonic

Локально получить технический ключ подписи; поля запроса передаются именованными аргументами.

```python
from_mnemonic(*, mnemonic: 'str', passphrase: 'str' = '', account_path: 'str' = "m/44'/60'/0'/0/0", account_index: 'int | None' = None, **kwargs) -> 'T'
```

## UnbondDelRequest

Публичная операция/свойство SDK. Ниже приведены точные типы, значения по умолчанию и тип результата; контекст использования дан в руководстве раздела.

```python
UnbondDelRequest(validator: 'str', amount_del: 'Decimal | str | int', private_key: 'str') -> None
```

- `validator`: `str`; required.
- `amount_del`: `Decimal | str | int`; required.
- `private_key`: `str`; use from_mnemonic; technical field, hidden in repr.

### from_mnemonic

Локально получить технический ключ подписи; поля запроса передаются именованными аргументами.

```python
from_mnemonic(*, mnemonic: 'str', passphrase: 'str' = '', account_path: 'str' = "m/44'/60'/0'/0/0", account_index: 'int | None' = None, **kwargs) -> 'T'
```

## WithdrawHoldDelRequest

Публичная операция/свойство SDK. Ниже приведены точные типы, значения по умолчанию и тип результата; контекст использования дан в руководстве раздела.

```python
WithdrawHoldDelRequest(validator: 'str', amount_del: 'Decimal | str | int', hold_timestamp: 'int', private_key: 'str') -> None
```

- `validator`: `str`; required.
- `amount_del`: `Decimal | str | int`; required.
- `hold_timestamp`: `int`; required.
- `private_key`: `str`; use from_mnemonic; technical field, hidden in repr.

### from_mnemonic

Локально получить технический ключ подписи; поля запроса передаются именованными аргументами.

```python
from_mnemonic(*, mnemonic: 'str', passphrase: 'str' = '', account_path: 'str' = "m/44'/60'/0'/0/0", account_index: 'int | None' = None, **kwargs) -> 'T'
```

## MultisendRecipient

Публичная операция/свойство SDK. Ниже приведены точные типы, значения по умолчанию и тип результата; контекст использования дан в руководстве раздела.

```python
MultisendRecipient(to: 'str', amount_del: 'Decimal | str | int') -> None
```

- `to`: `str`; required.
- `amount_del`: `Decimal | str | int`; required.

## MultisendDelRequest

Публичная операция/свойство SDK. Ниже приведены точные типы, значения по умолчанию и тип результата; контекст использования дан в руководстве раздела.

```python
MultisendDelRequest(recipients: 'list[MultisendRecipient]', private_key: 'str', memo: 'str | None' = None) -> None
```

- `recipients`: `list[MultisendRecipient]`; required.
- `private_key`: `str`; use from_mnemonic; technical field, hidden in repr.
- `memo`: `str | None`; None.

### from_mnemonic

Локально получить технический ключ подписи; поля запроса передаются именованными аргументами.

```python
from_mnemonic(*, mnemonic: 'str', passphrase: 'str' = '', account_path: 'str' = "m/44'/60'/0'/0/0", account_index: 'int | None' = None, **kwargs) -> 'T'
```

## MultisendErc20Recipient

Публичная операция/свойство SDK. Ниже приведены точные типы, значения по умолчанию и тип результата; контекст использования дан в руководстве раздела.

```python
MultisendErc20Recipient(to: 'str', amount: 'Decimal | str | int') -> None
```

- `to`: `str`; required.
- `amount`: `Decimal | str | int`; required.

## MultisendErc20Request

Публичная операция/свойство SDK. Ниже приведены точные типы, значения по умолчанию и тип результата; контекст использования дан в руководстве раздела.

```python
MultisendErc20Request(token: 'str', recipients: 'list[MultisendErc20Recipient]', private_key: 'str', decimals: 'int | None' = None, memo: 'str | None' = None, auto_approve: 'bool' = True, prefer_permit: 'bool' = True, permit_deadline: 'int' = 115792089237316195423570985008687907853269984665640564039457584007913129639935) -> None
```

- `token`: `str`; required.
- `recipients`: `list[MultisendErc20Recipient]`; required.
- `private_key`: `str`; use from_mnemonic; technical field, hidden in repr.
- `decimals`: `int | None`; None.
- `memo`: `str | None`; None.
- `auto_approve`: `bool`; True.
- `prefer_permit`: `bool`; True.
- `permit_deadline`: `int`; 115792089237316195423570985008687907853269984665640564039457584007913129639935.

### from_mnemonic

Локально получить технический ключ подписи; поля запроса передаются именованными аргументами.

```python
from_mnemonic(*, mnemonic: 'str', passphrase: 'str' = '', account_path: 'str' = "m/44'/60'/0'/0/0", account_index: 'int | None' = None, **kwargs) -> 'T'
```

## DelegateErc20Request

Публичная операция/свойство SDK. Ниже приведены точные типы, значения по умолчанию и тип результата; контекст использования дан в руководстве раздела.

```python
DelegateErc20Request(token: 'str', validator: 'str', amount: 'Decimal | str | int', private_key: 'str', decimals: 'int | None' = None, auto_approve: 'bool' = True, prefer_permit: 'bool' = True, permit_deadline: 'int' = 115792089237316195423570985008687907853269984665640564039457584007913129639935) -> None
```

- `token`: `str`; required.
- `validator`: `str`; required.
- `amount`: `Decimal | str | int`; required.
- `private_key`: `str`; use from_mnemonic; technical field, hidden in repr.
- `decimals`: `int | None`; None.
- `auto_approve`: `bool`; True.
- `prefer_permit`: `bool`; True.
- `permit_deadline`: `int`; 115792089237316195423570985008687907853269984665640564039457584007913129639935.

### from_mnemonic

Локально получить технический ключ подписи; поля запроса передаются именованными аргументами.

```python
from_mnemonic(*, mnemonic: 'str', passphrase: 'str' = '', account_path: 'str' = "m/44'/60'/0'/0/0", account_index: 'int | None' = None, **kwargs) -> 'T'
```

## HoldErc20Request

Публичная операция/свойство SDK. Ниже приведены точные типы, значения по умолчанию и тип результата; контекст использования дан в руководстве раздела.

```python
HoldErc20Request(token: 'str', validator: 'str', amount: 'Decimal | str | int', hold_timestamp: 'int', private_key: 'str', decimals: 'int | None' = None, auto_approve: 'bool' = True, prefer_permit: 'bool' = True, permit_deadline: 'int' = 115792089237316195423570985008687907853269984665640564039457584007913129639935) -> None
```

- `token`: `str`; required.
- `validator`: `str`; required.
- `amount`: `Decimal | str | int`; required.
- `hold_timestamp`: `int`; required.
- `private_key`: `str`; use from_mnemonic; technical field, hidden in repr.
- `decimals`: `int | None`; None.
- `auto_approve`: `bool`; True.
- `prefer_permit`: `bool`; True.
- `permit_deadline`: `int`; 115792089237316195423570985008687907853269984665640564039457584007913129639935.

### from_mnemonic

Локально получить технический ключ подписи; поля запроса передаются именованными аргументами.

```python
from_mnemonic(*, mnemonic: 'str', passphrase: 'str' = '', account_path: 'str' = "m/44'/60'/0'/0/0", account_index: 'int | None' = None, **kwargs) -> 'T'
```

## UnbondErc20Request

Публичная операция/свойство SDK. Ниже приведены точные типы, значения по умолчанию и тип результата; контекст использования дан в руководстве раздела.

```python
UnbondErc20Request(token: 'str', validator: 'str', amount: 'Decimal | str | int', private_key: 'str', decimals: 'int | None' = None) -> None
```

- `token`: `str`; required.
- `validator`: `str`; required.
- `amount`: `Decimal | str | int`; required.
- `private_key`: `str`; use from_mnemonic; technical field, hidden in repr.
- `decimals`: `int | None`; None.

### from_mnemonic

Локально получить технический ключ подписи; поля запроса передаются именованными аргументами.

```python
from_mnemonic(*, mnemonic: 'str', passphrase: 'str' = '', account_path: 'str' = "m/44'/60'/0'/0/0", account_index: 'int | None' = None, **kwargs) -> 'T'
```

## WithdrawHoldErc20Request

Публичная операция/свойство SDK. Ниже приведены точные типы, значения по умолчанию и тип результата; контекст использования дан в руководстве раздела.

```python
WithdrawHoldErc20Request(token: 'str', validator: 'str', amount: 'Decimal | str | int', hold_timestamp: 'int', private_key: 'str', decimals: 'int | None' = None) -> None
```

- `token`: `str`; required.
- `validator`: `str`; required.
- `amount`: `Decimal | str | int`; required.
- `hold_timestamp`: `int`; required.
- `private_key`: `str`; use from_mnemonic; technical field, hidden in repr.
- `decimals`: `int | None`; None.

### from_mnemonic

Локально получить технический ключ подписи; поля запроса передаются именованными аргументами.

```python
from_mnemonic(*, mnemonic: 'str', passphrase: 'str' = '', account_path: 'str' = "m/44'/60'/0'/0/0", account_index: 'int | None' = None, **kwargs) -> 'T'
```

## TransferStakeErc20Request

Публичная операция/свойство SDK. Ниже приведены точные типы, значения по умолчанию и тип результата; контекст использования дан в руководстве раздела.

```python
TransferStakeErc20Request(token: 'str', validator: 'str', new_validator: 'str', amount: 'Decimal | str | int', private_key: 'str', decimals: 'int | None' = None, hold_timestamp: 'int | None' = None) -> None
```

- `token`: `str`; required.
- `validator`: `str`; required.
- `new_validator`: `str`; required.
- `amount`: `Decimal | str | int`; required.
- `private_key`: `str`; use from_mnemonic; technical field, hidden in repr.
- `decimals`: `int | None`; None.
- `hold_timestamp`: `int | None`; None.

### from_mnemonic

Локально получить технический ключ подписи; поля запроса передаются именованными аргументами.

```python
from_mnemonic(*, mnemonic: 'str', passphrase: 'str' = '', account_path: 'str' = "m/44'/60'/0'/0/0", account_index: 'int | None' = None, **kwargs) -> 'T'
```

## TransferStakeDelRequest

Публичная операция/свойство SDK. Ниже приведены точные типы, значения по умолчанию и тип результата; контекст использования дан в руководстве раздела.

```python
TransferStakeDelRequest(validator: 'str', new_validator: 'str', amount_del: 'Decimal | str | int', private_key: 'str', hold_timestamp: 'int | None' = None) -> None
```

- `validator`: `str`; required.
- `new_validator`: `str`; required.
- `amount_del`: `Decimal | str | int`; required.
- `private_key`: `str`; use from_mnemonic; technical field, hidden in repr.
- `hold_timestamp`: `int | None`; None.

### from_mnemonic

Локально получить технический ключ подписи; поля запроса передаются именованными аргументами.

```python
from_mnemonic(*, mnemonic: 'str', passphrase: 'str' = '', account_path: 'str' = "m/44'/60'/0'/0/0", account_index: 'int | None' = None, **kwargs) -> 'T'
```

## StakeTokenToHoldRequest

Публичная операция/свойство SDK. Ниже приведены точные типы, значения по умолчанию и тип результата; контекст использования дан в руководстве раздела.

```python
StakeTokenToHoldRequest(token: 'str', validator: 'str', amount: 'Decimal | str | int', old_hold_timestamp: 'int', new_hold_timestamp: 'int', private_key: 'str', decimals: 'int | None' = None) -> None
```

- `token`: `str`; required.
- `validator`: `str`; required.
- `amount`: `Decimal | str | int`; required.
- `old_hold_timestamp`: `int`; required.
- `new_hold_timestamp`: `int`; required.
- `private_key`: `str`; use from_mnemonic; technical field, hidden in repr.
- `decimals`: `int | None`; None.

### from_mnemonic

Локально получить технический ключ подписи; поля запроса передаются именованными аргументами.

```python
from_mnemonic(*, mnemonic: 'str', passphrase: 'str' = '', account_path: 'str' = "m/44'/60'/0'/0/0", account_index: 'int | None' = None, **kwargs) -> 'T'
```

## ResetStakeHoldRequest

Публичная операция/свойство SDK. Ниже приведены точные типы, значения по умолчанию и тип результата; контекст использования дан в руководстве раздела.

```python
ResetStakeHoldRequest(validator: 'str', delegator: 'str', private_key: 'str', hold_timestamp: 'int', token: 'str | None' = None) -> None
```

- `validator`: `str`; required.
- `delegator`: `str`; required.
- `private_key`: `str`; use from_mnemonic; technical field, hidden in repr.
- `hold_timestamp`: `int`; required.
- `token`: `str | None`; None.

### from_mnemonic

Локально получить технический ключ подписи; поля запроса передаются именованными аргументами.

```python
from_mnemonic(*, mnemonic: 'str', passphrase: 'str' = '', account_path: 'str' = "m/44'/60'/0'/0/0", account_index: 'int | None' = None, **kwargs) -> 'T'
```

## WithdrawStakeWithResetRequest

Публичная операция/свойство SDK. Ниже приведены точные типы, значения по умолчанию и тип результата; контекст использования дан в руководстве раздела.

```python
WithdrawStakeWithResetRequest(token: 'str', validator: 'str', amount: 'Decimal | str | int', hold_timestamps_to_reset: 'list[int]', private_key: 'str', decimals: 'int | None' = None) -> None
```

- `token`: `str`; required.
- `validator`: `str`; required.
- `amount`: `Decimal | str | int`; required.
- `hold_timestamps_to_reset`: `list[int]`; required.
- `private_key`: `str`; use from_mnemonic; technical field, hidden in repr.
- `decimals`: `int | None`; None.

### from_mnemonic

Локально получить технический ключ подписи; поля запроса передаются именованными аргументами.

```python
from_mnemonic(*, mnemonic: 'str', passphrase: 'str' = '', account_path: 'str' = "m/44'/60'/0'/0/0", account_index: 'int | None' = None, **kwargs) -> 'T'
```

## WithdrawDelStakeWithResetRequest

Публичная операция/свойство SDK. Ниже приведены точные типы, значения по умолчанию и тип результата; контекст использования дан в руководстве раздела.

```python
WithdrawDelStakeWithResetRequest(validator: 'str', amount_del: 'Decimal | str | int', hold_timestamps_to_reset: 'list[int]', private_key: 'str') -> None
```

- `validator`: `str`; required.
- `amount_del`: `Decimal | str | int`; required.
- `hold_timestamps_to_reset`: `list[int]`; required.
- `private_key`: `str`; use from_mnemonic; technical field, hidden in repr.

### from_mnemonic

Локально получить технический ключ подписи; поля запроса передаются именованными аргументами.

```python
from_mnemonic(*, mnemonic: 'str', passphrase: 'str' = '', account_path: 'str' = "m/44'/60'/0'/0/0", account_index: 'int | None' = None, **kwargs) -> 'T'
```

## TransferStakeWithResetRequest

Публичная операция/свойство SDK. Ниже приведены точные типы, значения по умолчанию и тип результата; контекст использования дан в руководстве раздела.

```python
TransferStakeWithResetRequest(token: 'str', old_validator: 'str', new_validator: 'str', amount: 'Decimal | str | int', hold_timestamps_to_reset: 'list[int]', private_key: 'str', decimals: 'int | None' = None) -> None
```

- `token`: `str`; required.
- `old_validator`: `str`; required.
- `new_validator`: `str`; required.
- `amount`: `Decimal | str | int`; required.
- `hold_timestamps_to_reset`: `list[int]`; required.
- `private_key`: `str`; use from_mnemonic; technical field, hidden in repr.
- `decimals`: `int | None`; None.

### from_mnemonic

Локально получить технический ключ подписи; поля запроса передаются именованными аргументами.

```python
from_mnemonic(*, mnemonic: 'str', passphrase: 'str' = '', account_path: 'str' = "m/44'/60'/0'/0/0", account_index: 'int | None' = None, **kwargs) -> 'T'
```

## TransferDelStakeWithResetRequest

Публичная операция/свойство SDK. Ниже приведены точные типы, значения по умолчанию и тип результата; контекст использования дан в руководстве раздела.

```python
TransferDelStakeWithResetRequest(old_validator: 'str', new_validator: 'str', amount_del: 'Decimal | str | int', hold_timestamps_to_reset: 'list[int]', private_key: 'str') -> None
```

- `old_validator`: `str`; required.
- `new_validator`: `str`; required.
- `amount_del`: `Decimal | str | int`; required.
- `hold_timestamps_to_reset`: `list[int]`; required.
- `private_key`: `str`; use from_mnemonic; technical field, hidden in repr.

### from_mnemonic

Локально получить технический ключ подписи; поля запроса передаются именованными аргументами.

```python
from_mnemonic(*, mnemonic: 'str', passphrase: 'str' = '', account_path: 'str' = "m/44'/60'/0'/0/0", account_index: 'int | None' = None, **kwargs) -> 'T'
```

## HoldStakeWithResetRequest

Публичная операция/свойство SDK. Ниже приведены точные типы, значения по умолчанию и тип результата; контекст использования дан в руководстве раздела.

```python
HoldStakeWithResetRequest(token: 'str', validator: 'str', amount: 'Decimal | str | int', new_hold_timestamp: 'int', hold_timestamps_to_reset: 'list[int]', private_key: 'str', decimals: 'int | None' = None) -> None
```

- `token`: `str`; required.
- `validator`: `str`; required.
- `amount`: `Decimal | str | int`; required.
- `new_hold_timestamp`: `int`; required.
- `hold_timestamps_to_reset`: `list[int]`; required.
- `private_key`: `str`; use from_mnemonic; technical field, hidden in repr.
- `decimals`: `int | None`; None.

### from_mnemonic

Локально получить технический ключ подписи; поля запроса передаются именованными аргументами.

```python
from_mnemonic(*, mnemonic: 'str', passphrase: 'str' = '', account_path: 'str' = "m/44'/60'/0'/0/0", account_index: 'int | None' = None, **kwargs) -> 'T'
```

## ValidatorSelfPauseRequest

Публичная операция/свойство SDK. Ниже приведены точные типы, значения по умолчанию и тип результата; контекст использования дан в руководстве раздела.

```python
ValidatorSelfPauseRequest(private_key: 'str') -> None
```

- `private_key`: `str`; use from_mnemonic; technical field, hidden in repr.

### from_mnemonic

Локально получить технический ключ подписи; поля запроса передаются именованными аргументами.

```python
from_mnemonic(*, mnemonic: 'str', passphrase: 'str' = '', account_path: 'str' = "m/44'/60'/0'/0/0", account_index: 'int | None' = None, **kwargs) -> 'T'
```

## ValidatorPauseRequest

Публичная операция/свойство SDK. Ниже приведены точные типы, значения по умолчанию и тип результата; контекст использования дан в руководстве раздела.

```python
ValidatorPauseRequest(validator: 'str', private_key: 'str') -> None
```

- `validator`: `str`; required.
- `private_key`: `str`; use from_mnemonic; technical field, hidden in repr.

### from_mnemonic

Локально получить технический ключ подписи; поля запроса передаются именованными аргументами.

```python
from_mnemonic(*, mnemonic: 'str', passphrase: 'str' = '', account_path: 'str' = "m/44'/60'/0'/0/0", account_index: 'int | None' = None, **kwargs) -> 'T'
```

## DelegationTokenType

Публичная операция/свойство SDK. Ниже приведены точные типы, значения по умолчанию и тип результата; контекст использования дан в руководстве раздела.

## DelegationStake

Публичная операция/свойство SDK. Ниже приведены точные типы, значения по умолчанию и тип результата; контекст использования дан в руководстве раздела.

```python
DelegationStake(validator: 'str', delegator: 'str', token: 'str', amount_raw: 'int', token_id: 'int', token_type: 'int', hold_timestamp: 'int', block_number: 'int | None' = None) -> None
```

- `validator`: `str`; required.
- `delegator`: `str`; required.
- `token`: `str`; required.
- `amount_raw`: `int`; required.
- `token_id`: `int`; required.
- `token_type`: `int`; required.
- `hold_timestamp`: `int`; required.
- `block_number`: `int | None`; None.

### amount

Публичная операция/свойство SDK. Ниже приведены точные типы, значения по умолчанию и тип результата; контекст использования дан в руководстве раздела.

```python
amount(self, decimals: 'int' = 18) -> 'Decimal'
```

### amount_string

Публичная операция/свойство SDK. Ниже приведены точные типы, значения по умолчанию и тип результата; контекст использования дан в руководстве раздела.

```python
amount_string(self, decimals: 'int' = 18) -> 'str'
```

### as_dict

Публичная операция/свойство SDK. Ниже приведены точные типы, значения по умолчанию и тип результата; контекст использования дан в руководстве раздела.

```python
as_dict(self, decimals: 'int' = 18) -> 'dict[str, object]'
```

### exists

Публичная операция/свойство SDK. Ниже приведены точные типы, значения по умолчанию и тип результата; контекст использования дан в руководстве раздела.

```python
exists: bool
```

### hold_time

Публичная операция/свойство SDK. Ниже приведены точные типы, значения по умолчанию и тип результата; контекст использования дан в руководстве раздела.

```python
hold_time: str | None
```

### is_hold

Публичная операция/свойство SDK. Ниже приведены точные типы, значения по умолчанию и тип результата; контекст использования дан в руководстве раздела.

```python
is_hold: bool
```

### is_matured

Публичная операция/свойство SDK. Ниже приведены точные типы, значения по умолчанию и тип результата; контекст использования дан в руководстве раздела.

```python
is_matured(self, now_timestamp: 'int | None' = None) -> 'bool'
```

### is_native_del

Публичная операция/свойство SDK. Ниже приведены точные типы, значения по умолчанию и тип результата; контекст использования дан в руководстве раздела.

```python
is_native_del: bool
```

### token_type_enum

Публичная операция/свойство SDK. Ниже приведены точные типы, значения по умолчанию и тип результата; контекст использования дан в руководстве раздела.

```python
token_type_enum: DelegationTokenType
```

## DelegationStakeSnapshot

Публичная операция/свойство SDK. Ниже приведены точные типы, значения по умолчанию и тип результата; контекст использования дан в руководстве раздела.

```python
DelegationStakeSnapshot(block_number: 'int', regular: 'DelegationStake', holds: 'tuple[DelegationStake, ...]' = (), missing_hold_timestamps: 'tuple[int, ...]' = ()) -> None
```

- `block_number`: `int`; required.
- `regular`: `DelegationStake`; required.
- `holds`: `tuple[DelegationStake, ...]`; ().
- `missing_hold_timestamps`: `tuple[int, ...]`; ().

### as_dict

Публичная операция/свойство SDK. Ниже приведены точные типы, значения по умолчанию и тип результата; контекст использования дан в руководстве раздела.

```python
as_dict(self, decimals: 'int' = 18) -> 'dict[str, object]'
```

### held_amount

Публичная операция/свойство SDK. Ниже приведены точные типы, значения по умолчанию и тип результата; контекст использования дан в руководстве раздела.

```python
held_amount(self, decimals: 'int' = 18) -> 'Decimal'
```

### held_amount_raw

Публичная операция/свойство SDK. Ниже приведены точные типы, значения по умолчанию и тип результата; контекст использования дан в руководстве раздела.

```python
held_amount_raw: int
```

### matured_holds

Публичная операция/свойство SDK. Ниже приведены точные типы, значения по умолчанию и тип результата; контекст использования дан в руководстве раздела.

```python
matured_holds(self, now_timestamp: 'int | None' = None) -> 'tuple[DelegationStake, ...]'
```

### regular_amount

Публичная операция/свойство SDK. Ниже приведены точные типы, значения по умолчанию и тип результата; контекст использования дан в руководстве раздела.

```python
regular_amount(self, decimals: 'int' = 18) -> 'Decimal'
```

### regular_amount_raw

Публичная операция/свойство SDK. Ниже приведены точные типы, значения по умолчанию и тип результата; контекст использования дан в руководстве раздела.

```python
regular_amount_raw: int
```

### total_amount

Публичная операция/свойство SDK. Ниже приведены точные типы, значения по умолчанию и тип результата; контекст использования дан в руководстве раздела.

```python
total_amount(self, decimals: 'int' = 18) -> 'Decimal'
```

### total_amount_raw

Публичная операция/свойство SDK. Ниже приведены точные типы, значения по умолчанию и тип результата; контекст использования дан в руководстве раздела.

```python
total_amount_raw: int
```

## DecimalWorkflowResult

Публичная операция/свойство SDK. Ниже приведены точные типы, значения по умолчанию и тип результата; контекст использования дан в руководстве раздела.

```python
DecimalWorkflowResult(success: 'bool', name: 'str', steps: 'tuple[str, ...]', expected_steps: 'int', actual_steps: 'int', extra_steps_required: 'bool', primary: 'TransactionResult | None' = None, secondary: 'TransactionResult | None' = None, error: 'str | None' = None, user_message: 'str | None' = None) -> None
```

- `success`: `bool`; required.
- `name`: `str`; required.
- `steps`: `tuple[str, ...]`; required.
- `expected_steps`: `int`; required.
- `actual_steps`: `int`; required.
- `extra_steps_required`: `bool`; required.
- `primary`: `TransactionResult | None`; None.
- `secondary`: `TransactionResult | None`; None.
- `error`: `str | None`; None.
- `user_message`: `str | None`; None.

### fee_del

Публичная операция/свойство SDK. Ниже приведены точные типы, значения по умолчанию и тип результата; контекст использования дан в руководстве раздела.

```python
fee_del: Decimal | None
```

### fee_wei

Публичная операция/свойство SDK. Ниже приведены точные типы, значения по умолчанию и тип результата; контекст использования дан в руководстве раздела.

```python
fee_wei: int | None
```

### gas

Публичная операция/свойство SDK. Ниже приведены точные типы, значения по умолчанию и тип результата; контекст использования дан в руководстве раздела.

```python
gas: int | None
```

### hold_time

Публичная операция/свойство SDK. Ниже приведены точные типы, значения по умолчанию и тип результата; контекст использования дан в руководстве раздела.

```python
hold_time: str | None
```

### hold_timestamp

Публичная операция/свойство SDK. Ниже приведены точные типы, значения по умолчанию и тип результата; контекст использования дан в руководстве раздела.

```python
hold_timestamp: int | None
```

### one_transaction

Публичная операция/свойство SDK. Ниже приведены точные типы, значения по умолчанию и тип результата; контекст использования дан в руководстве раздела.

```python
one_transaction: bool
```

### requires_secondary_transaction

Публичная операция/свойство SDK. Ниже приведены точные типы, значения по умолчанию и тип результата; контекст использования дан в руководстве раздела.

```python
requires_secondary_transaction: bool
```

### total_fee_del

Публичная операция/свойство SDK. Ниже приведены точные типы, значения по умолчанию и тип результата; контекст использования дан в руководстве раздела.

```python
total_fee_del: Decimal | None
```

### total_fee_wei

Публичная операция/свойство SDK. Ниже приведены точные типы, значения по умолчанию и тип результата; контекст использования дан в руководстве раздела.

```python
total_fee_wei: int | None
```

### transaction_count

Публичная операция/свойство SDK. Ниже приведены точные типы, значения по умолчанию и тип результата; контекст использования дан в руководстве раздела.

```python
transaction_count: int
```

### tx_hash

Публичная операция/свойство SDK. Ниже приведены точные типы, значения по умолчанию и тип результата; контекст использования дан в руководстве раздела.

```python
tx_hash: str | None
```

## DecimalService

Публичная операция/свойство SDK. Ниже приведены точные типы, значения по умолчанию и тип результата; контекст использования дан в руководстве раздела.

### build_multisend_del

Подготовка calldata/черновика без отправки. Единицы и ограничения ABI описаны в руководстве раздела.

```python
async build_multisend_del(self, request: 'MultisendDelRequest') -> 'TransactionDraft'
```

### delegate_del

Публичная операция/свойство SDK. Ниже приведены точные типы, значения по умолчанию и тип результата; контекст использования дан в руководстве раздела.

```python
async delegate_del(self, request: 'DelegateDelRequest', broadcast: 'bool' = False, wait_receipt: 'bool' = False) -> 'TransactionResult'
```

### delegate_erc20

Публичная операция/свойство SDK. Ниже приведены точные типы, значения по умолчанию и тип результата; контекст использования дан в руководстве раздела.

```python
async delegate_erc20(self, request: 'DelegateErc20Request', broadcast: 'bool' = False, wait_receipt: 'bool' = False) -> 'DecimalWorkflowResult'
```

### estimate_fee_for_delegate_del

Расчет gas и необходимого баланса без подписи; RPC-симуляция может завершиться revert.

```python
async estimate_fee_for_delegate_del(self, request: 'DelegateDelRequest', *, exact: 'bool' = False) -> 'FeePreflight'
```

### estimate_fee_for_hold_del

Расчет gas и необходимого баланса без подписи; RPC-симуляция может завершиться revert.

```python
async estimate_fee_for_hold_del(self, request: 'HoldDelRequest', *, exact: 'bool' = False) -> 'FeePreflight'
```

### estimate_fee_for_multisend_del

Расчет gas и необходимого баланса без подписи; RPC-симуляция может завершиться revert.

```python
async estimate_fee_for_multisend_del(self, request: 'MultisendDelRequest', *, exact: 'bool' = False) -> 'FeePreflight'
```

### estimate_fee_for_transfer_del_stake_with_reset

Расчет gas и необходимого баланса без подписи; RPC-симуляция может завершиться revert.

```python
async estimate_fee_for_transfer_del_stake_with_reset(self, request: 'TransferDelStakeWithResetRequest', *, exact: 'bool' = False) -> 'FeePreflight'
```

### estimate_fee_for_transfer_stake_del

Расчет gas и необходимого баланса без подписи; RPC-симуляция может завершиться revert.

```python
async estimate_fee_for_transfer_stake_del(self, request: 'TransferStakeDelRequest', *, exact: 'bool' = False) -> 'FeePreflight'
```

### estimate_fee_for_transfer_stake_erc20

Расчет gas и необходимого баланса без подписи; RPC-симуляция может завершиться revert.

```python
async estimate_fee_for_transfer_stake_erc20(self, request: 'TransferStakeErc20Request', *, exact: 'bool' = False) -> 'FeePreflight'
```

### estimate_fee_for_transfer_stake_with_reset

Расчет gas и необходимого баланса без подписи; RPC-симуляция может завершиться revert.

```python
async estimate_fee_for_transfer_stake_with_reset(self, request: 'TransferStakeWithResetRequest', *, exact: 'bool' = False) -> 'FeePreflight'
```

### estimate_fee_for_unbond_del

Расчет gas и необходимого баланса без подписи; RPC-симуляция может завершиться revert.

```python
async estimate_fee_for_unbond_del(self, request: 'UnbondDelRequest', *, exact: 'bool' = False) -> 'FeePreflight'
```

### estimate_fee_for_unbond_erc20

Расчет gas и необходимого баланса без подписи; RPC-симуляция может завершиться revert.

```python
async estimate_fee_for_unbond_erc20(self, request: 'UnbondErc20Request', *, exact: 'bool' = False) -> 'FeePreflight'
```

### estimate_fee_for_withdraw_del_stake_with_reset

Расчет gas и необходимого баланса без подписи; RPC-симуляция может завершиться revert.

```python
async estimate_fee_for_withdraw_del_stake_with_reset(self, request: 'WithdrawDelStakeWithResetRequest', *, exact: 'bool' = False) -> 'FeePreflight'
```

### estimate_fee_for_withdraw_hold_del

Расчет gas и необходимого баланса без подписи; RPC-симуляция может завершиться revert.

```python
async estimate_fee_for_withdraw_hold_del(self, request: 'WithdrawHoldDelRequest', *, exact: 'bool' = False) -> 'FeePreflight'
```

### estimate_fee_for_withdraw_hold_erc20

Расчет gas и необходимого баланса без подписи; RPC-симуляция может завершиться revert.

```python
async estimate_fee_for_withdraw_hold_erc20(self, request: 'WithdrawHoldErc20Request', *, exact: 'bool' = False) -> 'FeePreflight'
```

### estimate_fee_for_withdraw_stake_with_reset

Расчет gas и необходимого баланса без подписи; RPC-симуляция может завершиться revert.

```python
async estimate_fee_for_withdraw_stake_with_reset(self, request: 'WithdrawStakeWithResetRequest', *, exact: 'bool' = False) -> 'FeePreflight'
```

### get_hold_stake

Публичная операция/свойство SDK. Ниже приведены точные типы, значения по умолчанию и тип результата; контекст использования дан в руководстве раздела.

```python
async get_hold_stake(self, validator: 'str', delegator: 'str', token: 'str', hold_timestamp: 'int', *, block_identifier: 'int | str | None' = None) -> 'DelegationStake'
```

### get_stake

Публичная операция/свойство SDK. Ниже приведены точные типы, значения по умолчанию и тип результата; контекст использования дан в руководстве раздела.

```python
async get_stake(self, validator: 'str', delegator: 'str', token: 'str', *, block_identifier: 'int | str | None' = None) -> 'DelegationStake'
```

### get_stake_snapshot

Публичная операция/свойство SDK. Ниже приведены точные типы, значения по умолчанию и тип результата; контекст использования дан в руководстве раздела.

```python
async get_stake_snapshot(self, validator: 'str', delegator: 'str', token: 'str', hold_timestamps: 'list[int] | tuple[int, ...]' = (), *, block_number: 'int | None' = None, max_hold_entries: 'int' = 100) -> 'DelegationStakeSnapshot'
```

### hold_del

Публичная операция/свойство SDK. Ниже приведены точные типы, значения по умолчанию и тип результата; контекст использования дан в руководстве раздела.

```python
async hold_del(self, request: 'HoldDelRequest', broadcast: 'bool' = False, wait_receipt: 'bool' = False) -> 'TransactionResult'
```

### hold_erc20

Публичная операция/свойство SDK. Ниже приведены точные типы, значения по умолчанию и тип результата; контекст использования дан в руководстве раздела.

```python
async hold_erc20(self, request: 'HoldErc20Request', broadcast: 'bool' = False, wait_receipt: 'bool' = False) -> 'DecimalWorkflowResult'
```

### hold_stake_with_reset

Публичная операция/свойство SDK. Ниже приведены точные типы, значения по умолчанию и тип результата; контекст использования дан в руководстве раздела.

```python
async hold_stake_with_reset(self, request: 'HoldStakeWithResetRequest', broadcast: 'bool' = False, wait_receipt: 'bool' = False) -> 'DecimalWorkflowResult'
```

### multisend_del

Публичная операция/свойство SDK. Ниже приведены точные типы, значения по умолчанию и тип результата; контекст использования дан в руководстве раздела.

```python
async multisend_del(self, request: 'MultisendDelRequest', broadcast: 'bool' = False, wait_receipt: 'bool' = False) -> 'TransactionResult'
```

### multisend_erc20

Публичная операция/свойство SDK. Ниже приведены точные типы, значения по умолчанию и тип результата; контекст использования дан в руководстве раздела.

```python
async multisend_erc20(self, request: 'MultisendErc20Request', broadcast: 'bool' = False, wait_receipt: 'bool' = False) -> 'DecimalWorkflowResult'
```

### pause_self_validator

Публичная операция/свойство SDK. Ниже приведены точные типы, значения по умолчанию и тип результата; контекст использования дан в руководстве раздела.

```python
async pause_self_validator(self, request: 'ValidatorSelfPauseRequest', broadcast: 'bool' = False, wait_receipt: 'bool' = False) -> 'DecimalWorkflowResult'
```

### pause_validator

Публичная операция/свойство SDK. Ниже приведены точные типы, значения по умолчанию и тип результата; контекст использования дан в руководстве раздела.

```python
async pause_validator(self, request: 'ValidatorPauseRequest', broadcast: 'bool' = False, wait_receipt: 'bool' = False) -> 'DecimalWorkflowResult'
```

### reset_stake_hold

Публичная операция/свойство SDK. Ниже приведены точные типы, значения по умолчанию и тип результата; контекст использования дан в руководстве раздела.

```python
async reset_stake_hold(self, request: 'ResetStakeHoldRequest', broadcast: 'bool' = False, wait_receipt: 'bool' = False) -> 'DecimalWorkflowResult'
```

### stake_token_to_hold

Публичная операция/свойство SDK. Ниже приведены точные типы, значения по умолчанию и тип результата; контекст использования дан в руководстве раздела.

```python
async stake_token_to_hold(self, request: 'StakeTokenToHoldRequest', broadcast: 'bool' = False, wait_receipt: 'bool' = False) -> 'DecimalWorkflowResult'
```

### transfer_del_stake_with_reset

Публичная операция/свойство SDK. Ниже приведены точные типы, значения по умолчанию и тип результата; контекст использования дан в руководстве раздела.

```python
async transfer_del_stake_with_reset(self, request: 'TransferDelStakeWithResetRequest', broadcast: 'bool' = False, wait_receipt: 'bool' = False) -> 'DecimalWorkflowResult'
```

### transfer_stake_del

Публичная операция/свойство SDK. Ниже приведены точные типы, значения по умолчанию и тип результата; контекст использования дан в руководстве раздела.

```python
async transfer_stake_del(self, request: 'TransferStakeDelRequest', broadcast: 'bool' = False, wait_receipt: 'bool' = False) -> 'DecimalWorkflowResult'
```

### transfer_stake_erc20

Публичная операция/свойство SDK. Ниже приведены точные типы, значения по умолчанию и тип результата; контекст использования дан в руководстве раздела.

```python
async transfer_stake_erc20(self, request: 'TransferStakeErc20Request', broadcast: 'bool' = False, wait_receipt: 'bool' = False) -> 'DecimalWorkflowResult'
```

### transfer_stake_with_reset

Публичная операция/свойство SDK. Ниже приведены точные типы, значения по умолчанию и тип результата; контекст использования дан в руководстве раздела.

```python
async transfer_stake_with_reset(self, request: 'TransferStakeWithResetRequest', broadcast: 'bool' = False, wait_receipt: 'bool' = False) -> 'DecimalWorkflowResult'
```

### unbond_del

Публичная операция/свойство SDK. Ниже приведены точные типы, значения по умолчанию и тип результата; контекст использования дан в руководстве раздела.

```python
async unbond_del(self, request: 'UnbondDelRequest', broadcast: 'bool' = False, wait_receipt: 'bool' = False) -> 'TransactionResult'
```

### unbond_erc20

Публичная операция/свойство SDK. Ниже приведены точные типы, значения по умолчанию и тип результата; контекст использования дан в руководстве раздела.

```python
async unbond_erc20(self, request: 'UnbondErc20Request', broadcast: 'bool' = False, wait_receipt: 'bool' = False) -> 'DecimalWorkflowResult'
```

### unpause_self_validator

Публичная операция/свойство SDK. Ниже приведены точные типы, значения по умолчанию и тип результата; контекст использования дан в руководстве раздела.

```python
async unpause_self_validator(self, request: 'ValidatorSelfPauseRequest', broadcast: 'bool' = False, wait_receipt: 'bool' = False) -> 'DecimalWorkflowResult'
```

### unpause_validator

Публичная операция/свойство SDK. Ниже приведены точные типы, значения по умолчанию и тип результата; контекст использования дан в руководстве раздела.

```python
async unpause_validator(self, request: 'ValidatorPauseRequest', broadcast: 'bool' = False, wait_receipt: 'bool' = False) -> 'DecimalWorkflowResult'
```

### validator_is_active

Публичная операция/свойство SDK. Ниже приведены точные типы, значения по умолчанию и тип результата; контекст использования дан в руководстве раздела.

```python
async validator_is_active(self, validator: 'str') -> 'bool'
```

### validator_is_member

Публичная операция/свойство SDK. Ниже приведены точные типы, значения по умолчанию и тип результата; контекст использования дан в руководстве раздела.

```python
async validator_is_member(self, validator: 'str') -> 'bool'
```

### validator_status

Публичная операция/свойство SDK. Ниже приведены точные типы, значения по умолчанию и тип результата; контекст использования дан в руководстве раздела.

```python
async validator_status(self, validator: 'str') -> 'int'
```

### withdraw_del_stake_with_reset

Публичная операция/свойство SDK. Ниже приведены точные типы, значения по умолчанию и тип результата; контекст использования дан в руководстве раздела.

```python
async withdraw_del_stake_with_reset(self, request: 'WithdrawDelStakeWithResetRequest', broadcast: 'bool' = False, wait_receipt: 'bool' = False) -> 'DecimalWorkflowResult'
```

### withdraw_hold_del

Публичная операция/свойство SDK. Ниже приведены точные типы, значения по умолчанию и тип результата; контекст использования дан в руководстве раздела.

```python
async withdraw_hold_del(self, request: 'WithdrawHoldDelRequest', broadcast: 'bool' = False, wait_receipt: 'bool' = False) -> 'TransactionResult'
```

### withdraw_hold_erc20

Публичная операция/свойство SDK. Ниже приведены точные типы, значения по умолчанию и тип результата; контекст использования дан в руководстве раздела.

```python
async withdraw_hold_erc20(self, request: 'WithdrawHoldErc20Request', broadcast: 'bool' = False, wait_receipt: 'bool' = False) -> 'DecimalWorkflowResult'
```

### withdraw_stake_with_reset

Публичная операция/свойство SDK. Ниже приведены точные типы, значения по умолчанию и тип результата; контекст использования дан в руководстве раздела.

```python
async withdraw_stake_with_reset(self, request: 'WithdrawStakeWithResetRequest', broadcast: 'bool' = False, wait_receipt: 'bool' = False) -> 'DecimalWorkflowResult'
```
