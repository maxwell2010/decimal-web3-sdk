# rpc

[Index](../api.md)

Signatures are generated from the release source. Required fields have no default.

## RpcPool

Rpcpool; types, defaults and return value are specified below.

### call

Call; types, defaults and return value are specified below.

```python
async call(self, fn: 'Callable[[Web3], T]') -> 'T'
```

### connect

Connect; types, defaults and return value are specified below.

```python
async connect(self) -> 'bool'
```

### current_url

Current url; types, defaults and return value are specified below.

```python
current_url: str
```

### rotate

Rotate; types, defaults and return value are specified below.

```python
rotate(self) -> 'None'
```

### web3

Web3; types, defaults and return value are specified below.

```python
web3: Web3
```
