# monitoring

[Index](../api.md)

Signatures are generated from the release source. Required fields have no default.

## MonitorSnapshot

Monitorsnapshot; types, defaults and return value are specified below.

```python
MonitorSnapshot(healthy: 'bool', result: 'OrchestratorResult') -> None
```

- `healthy`: `bool`; required.
- `result`: `OrchestratorResult`; required.

## DecimalMonitor

Decimalmonitor; types, defaults and return value are specified below.

### snapshot

Snapshot; types, defaults and return value are specified below.

```python
async snapshot(self) -> 'MonitorSnapshot'
```
