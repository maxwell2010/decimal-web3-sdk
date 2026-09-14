# orchestrator

[Index](../api.md)

Сигнатуры сформированы из кода релиза. Обязательные поля не имеют значения по умолчанию.

## OrchestratorResult

Публичная операция/свойство SDK. Ниже приведены точные типы, значения по умолчанию и тип результата; контекст использования дан в руководстве раздела.

```python
OrchestratorResult(success: 'bool', results: 'tuple[AgentResult, ...]', timings: 'tuple[Timing, ...]', metrics: 'dict[str, float | int]' = <factory>) -> None
```

- `success`: `bool`; required.
- `results`: `tuple[AgentResult, ...]`; required.
- `timings`: `tuple[Timing, ...]`; required.
- `metrics`: `dict[str, float | int]`; factory: dict.

## AgentOrchestrator

Публичная операция/свойство SDK. Ниже приведены точные типы, значения по умолчанию и тип результата; контекст использования дан в руководстве раздела.

### add

Публичная операция/свойство SDK. Ниже приведены точные типы, значения по умолчанию и тип результата; контекст использования дан в руководстве раздела.

```python
add(self, agent: 'DecimalAgent') -> 'None'
```

### run_parallel

Публичная операция/свойство SDK. Ниже приведены точные типы, значения по умолчанию и тип результата; контекст использования дан в руководстве раздела.

```python
async run_parallel(self, context: 'AgentContext', timeout_seconds: 'float | None' = None) -> 'OrchestratorResult'
```

### run_sequential

Публичная операция/свойство SDK. Ниже приведены точные типы, значения по умолчанию и тип результата; контекст использования дан в руководстве раздела.

```python
async run_sequential(self, context: 'AgentContext', timeout_seconds: 'float | None' = None, stop_on_error: 'bool' = True) -> 'OrchestratorResult'
```
