# telemetry

[Index](../api.md)

Signatures are generated from the release source. Required fields have no default.

## Timing

Timing; types, defaults and return value are specified below.

```python
Timing(name: 'str', duration_ms: 'float', success: 'bool', tags: 'dict[str, str]' = <factory>) -> None
```

- `name`: `str`; required.
- `duration_ms`: `float`; required.
- `success`: `bool`; required.
- `tags`: `dict[str, str]`; factory: dict.

## MetricsCollector

Metricscollector; types, defaults and return value are specified below.

### observe

Observe; types, defaults and return value are specified below.

```python
observe(self, name: 'str', started_at: 'float', success: 'bool', tags: 'dict[str, str] | None' = None) -> 'Timing'
```

### summary

Summary; types, defaults and return value are specified below.

```python
summary(self) -> 'dict[str, float | int]'
```

### timings

Timings; types, defaults and return value are specified below.

```python
timings: tuple[Timing, ...]
```

## Stopwatch

Stopwatch; types, defaults and return value are specified below.

### elapsed_ms

Elapsed ms; types, defaults and return value are specified below.

```python
elapsed_ms: float
```
