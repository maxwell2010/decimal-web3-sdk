# erc20

[Index](../api.md)

Signatures are generated from the release source. Required fields have no default.

## TokenInfo

Tokeninfo; types, defaults and return value are specified below.

```python
TokenInfo(address: 'str', name: 'str | None', symbol: 'str | None', decimals: 'int') -> None
```

- `address`: `str`; required.
- `name`: `str | None`; required.
- `symbol`: `str | None`; required.
- `decimals`: `int`; required.

## TokenBalance

Tokenbalance; types, defaults and return value are specified below.

```python
TokenBalance(token: 'TokenInfo', owner: 'str', raw: 'int', formatted: 'Decimal') -> None
```

- `token`: `TokenInfo`; required.
- `owner`: `str`; required.
- `raw`: `int`; required.
- `formatted`: `Decimal`; required.

### as_dict

As dict; types, defaults and return value are specified below.

```python
as_dict(self) -> 'dict[str, object]'
```

### formatted_string

Formatted string; types, defaults and return value are specified below.

```python
formatted_string: str
```

### raw_string

Raw string; types, defaults and return value are specified below.

```python
raw_string: str
```

## PermitSignature

Permitsignature; types, defaults and return value are specified below.

```python
PermitSignature(deadline: 'int', v: 'int', r: 'bytes', s: 'bytes') -> None
```

- `deadline`: `int`; required.
- `v`: `int`; required.
- `r`: `bytes`; required.
- `s`: `bytes`; required.

## Erc20Service

Erc20service; types, defaults and return value are specified below.

### allowance

Allowance; types, defaults and return value are specified below.

```python
async allowance(self, token_address: 'str', owner: 'str', spender: 'str') -> 'int'
```

### balance

Balance; types, defaults and return value are specified below.

```python
async balance(self, token_address: 'str', owner: 'str') -> 'TokenBalance'
```

### build_approve_data

Build transaction data/draft without broadcasting. See units and ABI constraints in the module guide.

```python
build_approve_data(self, token_address: 'str', spender: 'str', amount_raw: 'int') -> 'str'
```

### build_permit_data

Build transaction data/draft without broadcasting. See units and ABI constraints in the module guide.

```python
build_permit_data(self, token_address: 'str', owner: 'str', spender: 'str', value_raw: 'int', permit: 'PermitSignature') -> 'str'
```

### build_transfer_data

Build transaction data/draft without broadcasting. See units and ABI constraints in the module guide.

```python
build_transfer_data(self, token_address: 'str', to: 'str', amount_raw: 'int') -> 'str'
```

### build_transfer_from_data

Build transaction data/draft without broadcasting. See units and ABI constraints in the module guide.

```python
build_transfer_from_data(self, token_address: 'str', owner: 'str', to: 'str', amount_raw: 'int') -> 'str'
```

### info

Info; types, defaults and return value are specified below.

```python
async info(self, token_address: 'str') -> 'TokenInfo'
```

### permit_signature

Create a local signature. Treat the returned payload as sensitive; no automatic network broadcast.

```python
async permit_signature(self, token_address: 'str', owner: 'str', spender: 'str', value_raw: 'int', deadline: 'int', private_key: 'str') -> 'PermitSignature | None'
```

## format_units_string

Format units string; types, defaults and return value are specified below.

```python
format_units_string(value: 'int', decimals: 'int') -> 'str'
```

## format_units

Format units; types, defaults and return value are specified below.

```python
format_units(value: 'int', decimals: 'int') -> 'Decimal'
```

## parse_units

Parse units; types, defaults and return value are specified below.

```python
parse_units(value: 'Decimal | str | int', decimals: 'int') -> 'int'
```
