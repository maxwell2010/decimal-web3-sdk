# limits

[Index](../api.md)

Сигнатуры сформированы из кода релиза. Обязательные поля не имеют значения по умолчанию.

## SafetyLimits

Публичная операция/свойство SDK. Ниже приведены точные типы, значения по умолчанию и тип результата; контекст использования дан в руководстве раздела.

```python
SafetyLimits(rest_max_limit: 'int' = 100, rest_min_interval_seconds: 'float' = 0.15, rpc_min_interval_seconds: 'float' = 0.05, gas_limit_multiplier: 'float' = 1.1, max_gas_price_wei: 'int | None' = None, receipt_wait_timeout_seconds: 'float' = 7.0, receipt_poll_seconds: 'float' = 3.0, ws_max_subscriptions: 'int' = 16, ws_ping_interval_seconds: 'float' = 30.0, ws_reconnect_min_delay_seconds: 'float' = 2.0, integration_tests_enabled: 'bool' = False) -> None
```

- `rest_max_limit`: `int`; 100.
- `rest_min_interval_seconds`: `float`; 0.15.
- `rpc_min_interval_seconds`: `float`; 0.05.
- `gas_limit_multiplier`: `float`; 1.1.
- `max_gas_price_wei`: `int | None`; None.
- `receipt_wait_timeout_seconds`: `float`; 7.0.
- `receipt_poll_seconds`: `float`; 3.0.
- `ws_max_subscriptions`: `int`; 16.
- `ws_ping_interval_seconds`: `float`; 30.0.
- `ws_reconnect_min_delay_seconds`: `float`; 2.0.
- `integration_tests_enabled`: `bool`; False.

## AsyncRateLimiter

Публичная операция/свойство SDK. Ниже приведены точные типы, значения по умолчанию и тип результата; контекст использования дан в руководстве раздела.

### wait

Публичная операция/свойство SDK. Ниже приведены точные типы, значения по умолчанию и тип результата; контекст использования дан в руководстве раздела.

```python
async wait(self) -> 'None'
```
