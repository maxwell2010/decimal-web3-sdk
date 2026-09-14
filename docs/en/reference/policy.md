# policy

[Index](../api.md)

Signatures are generated from the release source. Required fields have no default.

## TransactionPolicy

Transactionpolicy; types, defaults and return value are specified below.

```python
TransactionPolicy(target_total_seconds: 'float' = 5.0, build_timeout_seconds: 'float' = 1.0, estimate_timeout_seconds: 'float' = 1.5, broadcast_timeout_seconds: 'float' = 1.5, receipt_poll_seconds: 'float' = 1.0, max_rpc_attempts: 'int' = 2) -> None
```

- `target_total_seconds`: `float`; 5.0.
- `build_timeout_seconds`: `float`; 1.0.
- `estimate_timeout_seconds`: `float`; 1.5.
- `broadcast_timeout_seconds`: `float`; 1.5.
- `receipt_poll_seconds`: `float`; 1.0.
- `max_rpc_attempts`: `int`; 2.

### fast

Fast; types, defaults and return value are specified below.

```python
fast() -> "'TransactionPolicy'"
```

### validate

Validate; types, defaults and return value are specified below.

```python
validate(self) -> 'None'
```
