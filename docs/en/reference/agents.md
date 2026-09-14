# agents

[Index](../api.md)

Signatures are generated from the release source. Required fields have no default.

## AgentContext

Agentcontext; types, defaults and return value are specified below.

```python
AgentContext(client: 'Any | None' = None, data: 'dict[str, Any]' = <factory>, policy: 'TransactionPolicy' = <factory>) -> None
```

- `client`: `Any | None`; None.
- `data`: `dict[str, Any]`; factory: dict.
- `policy`: `TransactionPolicy`; factory: fast.

## AgentResult

Agentresult; types, defaults and return value are specified below.

```python
AgentResult(name: 'str', success: 'bool', payload: 'dict[str, Any]' = <factory>, error: 'str | None' = None) -> None
```

- `name`: `str`; required.
- `success`: `bool`; required.
- `payload`: `dict[str, Any]`; factory: dict.
- `error`: `str | None`; None.

## DecimalAgent

Decimalagent; types, defaults and return value are specified below.

### run

Run; types, defaults and return value are specified below.

```python
async run(self, context: 'AgentContext') -> 'AgentResult'
```

## HealthCheckAgent

Healthcheckagent; types, defaults and return value are specified below.

### run

Run; types, defaults and return value are specified below.

```python
async run(self, context: 'AgentContext') -> 'AgentResult'
```

## LatestBlockAgent

Latestblockagent; types, defaults and return value are specified below.

### run

Run; types, defaults and return value are specified below.

```python
async run(self, context: 'AgentContext') -> 'AgentResult'
```

## RestLatencyAgent

Restlatencyagent; types, defaults and return value are specified below.

### run

Run; types, defaults and return value are specified below.

```python
async run(self, context: 'AgentContext') -> 'AgentResult'
```

## TransactionSlaAgent

Transactionslaagent; types, defaults and return value are specified below.

### run

Run; types, defaults and return value are specified below.

```python
async run(self, context: 'AgentContext') -> 'AgentResult'
```
