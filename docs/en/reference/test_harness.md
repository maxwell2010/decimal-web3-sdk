# test_harness

[Index](../api.md)

Signatures are generated from the release source. Required fields have no default.

## TxTrainingCase

Txtrainingcase; types, defaults and return value are specified below.

```python
TxTrainingCase(name: 'str', kind: 'str', expected_steps: 'int', broadcast: 'bool' = False) -> None
```

- `name`: `str`; required.
- `kind`: `str`; required.
- `expected_steps`: `int`; required.
- `broadcast`: `bool`; False.

## TxTrainingRecord

Txtrainingrecord; types, defaults and return value are specified below.

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

Txtrainingjournal; types, defaults and return value are specified below.

### append

Append; types, defaults and return value are specified below.

```python
append(self, record: 'TxTrainingRecord') -> 'None'
```

## run_env_training

Run env training; types, defaults and return value are specified below.

```python
async run_env_training(journal: 'TxTrainingJournal | None' = None) -> 'list[TxTrainingRecord]'
```
