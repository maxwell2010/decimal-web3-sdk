# policy

[Index](../api.md)

Сигнатуры сформированы из кода релиза. Обязательные поля не имеют значения по умолчанию.

## TransactionPolicy

Публичная операция/свойство SDK. Ниже приведены точные типы, значения по умолчанию и тип результата; контекст использования дан в руководстве раздела.

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

Публичная операция/свойство SDK. Ниже приведены точные типы, значения по умолчанию и тип результата; контекст использования дан в руководстве раздела.

```python
fast() -> "'TransactionPolicy'"
```

### validate

Публичная операция/свойство SDK. Ниже приведены точные типы, значения по умолчанию и тип результата; контекст использования дан в руководстве раздела.

```python
validate(self) -> 'None'
```
