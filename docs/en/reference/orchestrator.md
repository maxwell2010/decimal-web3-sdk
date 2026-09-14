# orchestrator

[Index](../api.md)

Signatures are generated from the release source. Required fields have no default.

## OrchestratorResult

Orchestratorresult; types, defaults and return value are specified below.

```python
OrchestratorResult(success: 'bool', results: 'tuple[AgentResult, ...]', timings: 'tuple[Timing, ...]', metrics: 'dict[str, float | int]' = <factory>) -> None
```

- `success`: `bool`; required.
- `results`: `tuple[AgentResult, ...]`; required.
- `timings`: `tuple[Timing, ...]`; required.
- `metrics`: `dict[str, float | int]`; factory: dict.

## AgentOrchestrator

Agentorchestrator; types, defaults and return value are specified below.

### add

Add; types, defaults and return value are specified below.

```python
add(self, agent: 'DecimalAgent') -> 'None'
```

### run_parallel

Run parallel; types, defaults and return value are specified below.

```python
async run_parallel(self, context: 'AgentContext', timeout_seconds: 'float | None' = None) -> 'OrchestratorResult'
```

### run_sequential

Run sequential; types, defaults and return value are specified below.

```python
async run_sequential(self, context: 'AgentContext', timeout_seconds: 'float | None' = None, stop_on_error: 'bool' = True) -> 'OrchestratorResult'
```
