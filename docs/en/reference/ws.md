# ws

[Index](../api.md)

Signatures are generated from the release source. Required fields have no default.

## WsMessage

Wsmessage; types, defaults and return value are specified below.

```python
WsMessage(raw: 'str', data: 'dict[str, Any] | list[Any] | str | None') -> None
```

- `raw`: `str`; required.
- `data`: `dict[str, Any] | list[Any] | str | None`; required.

## DecimalWsClient

Decimalwsclient; types, defaults and return value are specified below.

### close

Close; types, defaults and return value are specified below.

```python
async close(self) -> 'None'
```

### connect

Connect; types, defaults and return value are specified below.

```python
async connect(self) -> 'bool'
```

### connected

Connected; types, defaults and return value are specified below.

```python
connected: bool
```

### receive_once

Receive once; types, defaults and return value are specified below.

```python
async receive_once(self, timeout_seconds: 'float' = 5.0) -> 'WsMessage | None'
```

### subscribe

Subscribe; types, defaults and return value are specified below.

```python
async subscribe(self, query: 'str') -> 'dict[str, Any]'
```

### unsubscribe

Unsubscribe; types, defaults and return value are specified below.

```python
async unsubscribe(self, query: 'str') -> 'dict[str, Any]'
```
