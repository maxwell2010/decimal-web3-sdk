# test_harness

[Index](../api.md)

Сигнатуры сформированы из кода релиза. Обязательные поля не имеют значения по умолчанию.

## TxTrainingCase

Публичная операция/свойство SDK. Ниже приведены точные типы, значения по умолчанию и тип результата; контекст использования дан в руководстве раздела.

```python
TxTrainingCase(name: 'str', kind: 'str', expected_steps: 'int', broadcast: 'bool' = False) -> None
```

- `name`: `str`; required.
- `kind`: `str`; required.
- `expected_steps`: `int`; required.
- `broadcast`: `bool`; False.

## TxTrainingRecord

Публичная операция/свойство SDK. Ниже приведены точные типы, значения по умолчанию и тип результата; контекст использования дан в руководстве раздела.

```python
TxTrainingRecord(timestamp: 'str', name: 'str', kind: 'str', success: 'bool', broadcast: 'bool', chain_id: 'int | None', account: 'str | None', balance_before_del: 'str | None', balance_after_del: 'str | None', nonce_before: 'int | None', nonce_after: 'int | None', preflight_fee_wei: 'int | None', preflight_fee_del: 'str | None', preflight_required_del: 'str | None', preflight_missing_del: 'str | None', tx_hash: 'str | None', status: 'str | None', block_number: 'int | None', gas: 'int | None', fee_wei: 'int | None', fee_del: 'str | None', effective_fee_del: 'str | None', elapsed_ms: 'float', expected_steps: 'int', actual_steps: 'int', extra_steps_required: 'bool', error: 'str | None') -> None
```

- `timestamp`: `str`; required.
- `name`: `str`; required.
- `kind`: `str`; required.
- `success`: `bool`; required.
- `broadcast`: `bool`; required.
- `chain_id`: `int | None`; required.
- `account`: `str | None`; required.
- `balance_before_del`: `str | None`; required.
- `balance_after_del`: `str | None`; required.
- `nonce_before`: `int | None`; required.
- `nonce_after`: `int | None`; required.
- `preflight_fee_wei`: `int | None`; required.
- `preflight_fee_del`: `str | None`; required.
- `preflight_required_del`: `str | None`; required.
- `preflight_missing_del`: `str | None`; required.
- `tx_hash`: `str | None`; required.
- `status`: `str | None`; required.
- `block_number`: `int | None`; required.
- `gas`: `int | None`; required.
- `fee_wei`: `int | None`; required.
- `fee_del`: `str | None`; required.
- `effective_fee_del`: `str | None`; required.
- `elapsed_ms`: `float`; required.
- `expected_steps`: `int`; required.
- `actual_steps`: `int`; required.
- `extra_steps_required`: `bool`; required.
- `error`: `str | None`; required.

## TxTrainingJournal

Публичная операция/свойство SDK. Ниже приведены точные типы, значения по умолчанию и тип результата; контекст использования дан в руководстве раздела.

### append

Публичная операция/свойство SDK. Ниже приведены точные типы, значения по умолчанию и тип результата; контекст использования дан в руководстве раздела.

```python
append(self, record: 'TxTrainingRecord') -> 'None'
```

## run_env_training

Публичная операция/свойство SDK. Ниже приведены точные типы, значения по умолчанию и тип результата; контекст использования дан в руководстве раздела.

```python
async run_env_training(journal: 'TxTrainingJournal | None' = None) -> 'list[TxTrainingRecord]'
```
