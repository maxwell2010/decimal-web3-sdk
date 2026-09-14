# token_operations

[Index](../api.md)

Signatures are generated from the release source. Required fields have no default.

## BuyExactTokenRequest

Buyexacttokenrequest; types, defaults and return value are specified below.

```python
BuyExactTokenRequest(token: 'str', recipient: 'str', amount_out_raw: 'int', max_amount_del: 'Decimal | str | int', *, private_key: 'str') -> None
```

- `private_key`: `str`; use from_mnemonic; technical field, hidden in repr.
- `token`: `str`; required.
- `recipient`: `str`; required.
- `amount_out_raw`: `int`; required.
- `max_amount_del`: `Decimal | str | int`; required.

### from_mnemonic

Derive the technical signing key locally; pass request fields as keyword arguments.

```python
from_mnemonic(*, mnemonic: 'str', passphrase: 'str' = '', account_path: 'str' = "m/44'/60'/0'/0/0", account_index: 'int | None' = None, **kwargs) -> 'T'
```

### to_contract_call

To contract call; types, defaults and return value are specified below.

```python
to_contract_call(self, client)
```

## SellForExactDelRequest

Sellforexactdelrequest; types, defaults and return value are specified below.

```python
SellForExactDelRequest(token: 'str', recipient: 'str', amount_out_del: 'Decimal | str | int', max_amount_in_raw: 'int', *, private_key: 'str') -> None
```

- `private_key`: `str`; use from_mnemonic; technical field, hidden in repr.
- `token`: `str`; required.
- `recipient`: `str`; required.
- `amount_out_del`: `Decimal | str | int`; required.
- `max_amount_in_raw`: `int`; required.

### from_mnemonic

Derive the technical signing key locally; pass request fields as keyword arguments.

```python
from_mnemonic(*, mnemonic: 'str', passphrase: 'str' = '', account_path: 'str' = "m/44'/60'/0'/0/0", account_index: 'int | None' = None, **kwargs) -> 'T'
```

### to_contract_call

To contract call; types, defaults and return value are specified below.

```python
to_contract_call(self, client)
```

## ConvertToDelRequest

Converttodelrequest; types, defaults and return value are specified below.

```python
ConvertToDelRequest(owner: 'str', token: 'str', amount_raw: 'int', estimated_gas: 'int', permit: 'PermitSignature', *, private_key: 'str') -> None
```

- `private_key`: `str`; use from_mnemonic; technical field, hidden in repr.
- `owner`: `str`; required.
- `token`: `str`; required.
- `amount_raw`: `int`; required.
- `estimated_gas`: `int`; required.
- `permit`: `PermitSignature`; required.

### from_mnemonic

Derive the technical signing key locally; pass request fields as keyword arguments.

```python
from_mnemonic(*, mnemonic: 'str', passphrase: 'str' = '', account_path: 'str' = "m/44'/60'/0'/0/0", account_index: 'int | None' = None, **kwargs) -> 'T'
```

### to_contract_call

To contract call; types, defaults and return value are specified below.

```python
to_contract_call(self, client)
```

## UpdateTokenMinSupplyRequest

Updatetokenminsupplyrequest; types, defaults and return value are specified below.

```python
UpdateTokenMinSupplyRequest(token: 'str', min_total_supply_raw: 'int', allow_legacy: 'bool' = False, *, private_key: 'str') -> None
```

- `private_key`: `str`; use from_mnemonic; technical field, hidden in repr.
- `token`: `str`; required.
- `min_total_supply_raw`: `int`; required.
- `allow_legacy`: `bool`; False.

### from_mnemonic

Derive the technical signing key locally; pass request fields as keyword arguments.

```python
from_mnemonic(*, mnemonic: 'str', passphrase: 'str' = '', account_path: 'str' = "m/44'/60'/0'/0/0", account_index: 'int | None' = None, **kwargs) -> 'T'
```

### to_contract_call

To contract call; types, defaults and return value are specified below.

```python
to_contract_call(self, client)
```

## TokenOperations

Tokenoperations; types, defaults and return value are specified below.

### buy_exact

Buy exact; types, defaults and return value are specified below.

```python
async buy_exact(self, request: 'BuyExactTokenRequest', broadcast: 'bool' = False, wait_receipt: 'bool' = False) -> 'TransactionResult'
```

### convert_to_del

Convert to del; types, defaults and return value are specified below.

```python
async convert_to_del(self, request: 'ConvertToDelRequest', broadcast: 'bool' = False, wait_receipt: 'bool' = False) -> 'TransactionResult'
```

### sell_for_exact_del

Sell for exact del; types, defaults and return value are specified below.

```python
async sell_for_exact_del(self, request: 'SellForExactDelRequest', broadcast: 'bool' = False, wait_receipt: 'bool' = False) -> 'TransactionResult'
```

### update_min_supply

Update min supply; types, defaults and return value are specified below.

```python
async update_min_supply(self, request: 'UpdateTokenMinSupplyRequest', broadcast: 'bool' = False, wait_receipt: 'bool' = False) -> 'TransactionResult'
```
