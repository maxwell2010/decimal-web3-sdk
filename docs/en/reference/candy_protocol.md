# candy_protocol

[Index](../api.md)

Signatures are generated from the release source. Required fields have no default.

## load_candy_profile

Load candy profile; types, defaults and return value are specified below.

```python
load_candy_profile() -> 'dict[str, Any]'
```

## build_unsigned_candy_burn

Build transaction data/draft without broadcasting. See units and ABI constraints in the module guide.

```python
build_unsigned_candy_burn(*, owner: 'str', amount_base: 'int', token_address: 'str | None' = None, chain_id: 'int' = 75) -> 'dict[str, Any]'
```

## build_unsigned_candy_call

Build transaction data/draft without broadcasting. See units and ABI constraints in the module guide.

```python
build_unsigned_candy_call(*, owner: 'str', contract_type: 'str', signature: 'str', args: 'list[Any]', address: 'str | None' = None, value_wei: 'int' = 0, chain_id: 'int' = 75) -> 'dict[str, Any]'
```
