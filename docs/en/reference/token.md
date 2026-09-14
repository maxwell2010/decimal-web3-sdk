# token

[Index](../api.md)

Signatures are generated from the release source. Required fields have no default.

## BuyTokenRequest

Buytokenrequest; types, defaults and return value are specified below.

```python
BuyTokenRequest(token: 'str', amount_del: 'Decimal | str | int', private_key: 'str', min_amount_out_raw: 'int' = 0) -> None
```

- `token`: `str`; required.
- `amount_del`: `Decimal | str | int`; required.
- `private_key`: `str`; use from_mnemonic; technical field, hidden in repr.
- `min_amount_out_raw`: `int`; 0.

### from_mnemonic

Derive the technical signing key locally; pass request fields as keyword arguments.

```python
from_mnemonic(*, mnemonic: 'str', passphrase: 'str' = '', account_path: 'str' = "m/44'/60'/0'/0/0", account_index: 'int | None' = None, **kwargs) -> 'T'
```

## SellTokenRequest

Selltokenrequest; types, defaults and return value are specified below.

```python
SellTokenRequest(token: 'str', amount: 'Decimal | str | int', private_key: 'str', min_amount_del_out_wei: 'int' = 1, decimals: 'int | None' = None) -> None
```

- `token`: `str`; required.
- `amount`: `Decimal | str | int`; required.
- `private_key`: `str`; use from_mnemonic; technical field, hidden in repr.
- `min_amount_del_out_wei`: `int`; 1.
- `decimals`: `int | None`; None.

### from_mnemonic

Derive the technical signing key locally; pass request fields as keyword arguments.

```python
from_mnemonic(*, mnemonic: 'str', passphrase: 'str' = '', account_path: 'str' = "m/44'/60'/0'/0/0", account_index: 'int | None' = None, **kwargs) -> 'T'
```

## ConvertTokenRequest

Converttokenrequest; types, defaults and return value are specified below.

```python
ConvertTokenRequest(token_in: 'str', token_out: 'str', amount_in: 'Decimal | str | int', min_amount_out: 'Decimal | str | int', private_key: 'str', token_in_decimals: 'int | None' = None, token_out_decimals: 'int | None' = None, auto_approve: 'bool' = True, prefer_permit: 'bool' = True, permit_deadline: 'int' = 115792089237316195423570985008687907853269984665640564039457584007913129639935) -> None
```

- `token_in`: `str`; required.
- `token_out`: `str`; required.
- `amount_in`: `Decimal | str | int`; required.
- `min_amount_out`: `Decimal | str | int`; required.
- `private_key`: `str`; use from_mnemonic; technical field, hidden in repr.
- `token_in_decimals`: `int | None`; None.
- `token_out_decimals`: `int | None`; None.
- `auto_approve`: `bool`; True.
- `prefer_permit`: `bool`; True.
- `permit_deadline`: `int`; 115792089237316195423570985008687907853269984665640564039457584007913129639935.

### from_mnemonic

Derive the technical signing key locally; pass request fields as keyword arguments.

```python
from_mnemonic(*, mnemonic: 'str', passphrase: 'str' = '', account_path: 'str' = "m/44'/60'/0'/0/0", account_index: 'int | None' = None, **kwargs) -> 'T'
```

## BurnTokenRequest

Burntokenrequest; types, defaults and return value are specified below.

```python
BurnTokenRequest(token: 'str', amount: 'Decimal | str | int', private_key: 'str', decimals: 'int | None' = None) -> None
```

- `token`: `str`; required.
- `amount`: `Decimal | str | int`; required.
- `private_key`: `str`; use from_mnemonic; technical field, hidden in repr.
- `decimals`: `int | None`; None.

### from_mnemonic

Derive the technical signing key locally; pass request fields as keyword arguments.

```python
from_mnemonic(*, mnemonic: 'str', passphrase: 'str' = '', account_path: 'str' = "m/44'/60'/0'/0/0", account_index: 'int | None' = None, **kwargs) -> 'T'
```

## MintTokenRequest

Minttokenrequest; types, defaults and return value are specified below.

```python
MintTokenRequest(token: 'str', to: 'str', amount: 'Decimal | str | int', private_key: 'str', decimals: 'int | None' = None) -> None
```

- `token`: `str`; required.
- `to`: `str`; required.
- `amount`: `Decimal | str | int`; required.
- `private_key`: `str`; use from_mnemonic; technical field, hidden in repr.
- `decimals`: `int | None`; None.

### from_mnemonic

Derive the technical signing key locally; pass request fields as keyword arguments.

```python
from_mnemonic(*, mnemonic: 'str', passphrase: 'str' = '', account_path: 'str' = "m/44'/60'/0'/0/0", account_index: 'int | None' = None, **kwargs) -> 'T'
```

## UpdateTokenDetailsRequest

Updatetokendetailsrequest; types, defaults and return value are specified below.

```python
UpdateTokenDetailsRequest(token: 'str', identity: 'str', max_total_supply_raw: 'int', private_key: 'str') -> None
```

- `token`: `str`; required.
- `identity`: `str`; required.
- `max_total_supply_raw`: `int`; required.
- `private_key`: `str`; use from_mnemonic; technical field, hidden in repr.

### from_mnemonic

Derive the technical signing key locally; pass request fields as keyword arguments.

```python
from_mnemonic(*, mnemonic: 'str', passphrase: 'str' = '', account_path: 'str' = "m/44'/60'/0'/0/0", account_index: 'int | None' = None, **kwargs) -> 'T'
```

## CreateReservelessTokenRequest

Createreservelesstokenrequest; types, defaults and return value are specified below.

```python
CreateReservelessTokenRequest(name: 'str', symbol: 'str', mintable: 'bool', burnable: 'bool', initial_mint_raw: 'int', cap_raw: 'int', identity: 'str', private_key: 'str') -> None
```

- `name`: `str`; required.
- `symbol`: `str`; required.
- `mintable`: `bool`; required.
- `burnable`: `bool`; required.
- `initial_mint_raw`: `int`; required.
- `cap_raw`: `int`; required.
- `identity`: `str`; required.
- `private_key`: `str`; use from_mnemonic; technical field, hidden in repr.

### from_mnemonic

Derive the technical signing key locally; pass request fields as keyword arguments.

```python
from_mnemonic(*, mnemonic: 'str', passphrase: 'str' = '', account_path: 'str' = "m/44'/60'/0'/0/0", account_index: 'int | None' = None, **kwargs) -> 'T'
```

## CreateTokenRequest

Createtokenrequest; types, defaults and return value are specified below.

```python
CreateTokenRequest(name: 'str', symbol: 'str', initial_mint_raw: 'int', min_total_supply_raw: 'int', max_total_supply_raw: 'int', crr: 'int', identity: 'str', private_key: 'str', reserve_value_wei: 'int | None' = None, creator: 'str | None' = None) -> None
```

- `name`: `str`; required.
- `symbol`: `str`; required.
- `initial_mint_raw`: `int`; required.
- `min_total_supply_raw`: `int`; required.
- `max_total_supply_raw`: `int`; required.
- `crr`: `int`; required.
- `identity`: `str`; required.
- `private_key`: `str`; use from_mnemonic; technical field, hidden in repr.
- `reserve_value_wei`: `int | None`; None.
- `creator`: `str | None`; None.

### from_mnemonic

Derive the technical signing key locally; pass request fields as keyword arguments.

```python
from_mnemonic(*, mnemonic: 'str', passphrase: 'str' = '', account_path: 'str' = "m/44'/60'/0'/0/0", account_index: 'int | None' = None, **kwargs) -> 'T'
```

## TokenService

Tokenservice; types, defaults and return value are specified below.

### burn

Burn; types, defaults and return value are specified below.

```python
async burn(self, request: 'BurnTokenRequest', broadcast: 'bool' = False, wait_receipt: 'bool' = False) -> 'TransactionResult'
```

### buy

Buy; types, defaults and return value are specified below.

```python
async buy(self, request: 'BuyTokenRequest', broadcast: 'bool' = False, wait_receipt: 'bool' = False) -> 'TransactionResult'
```

### convert

Convert; types, defaults and return value are specified below.

```python
async convert(self, request: 'ConvertTokenRequest', broadcast: 'bool' = False, wait_receipt: 'bool' = False) -> 'DecimalWorkflowResult'
```

### create

Create; types, defaults and return value are specified below.

```python
async create(self, request: 'CreateTokenRequest', broadcast: 'bool' = False, wait_receipt: 'bool' = False) -> 'TransactionResult'
```

### create_reserveless

Create reserveless; types, defaults and return value are specified below.

```python
async create_reserveless(self, request: 'CreateReservelessTokenRequest', broadcast: 'bool' = False, wait_receipt: 'bool' = False) -> 'TransactionResult'
```

### mint

Mint; types, defaults and return value are specified below.

```python
async mint(self, request: 'MintTokenRequest', broadcast: 'bool' = False, wait_receipt: 'bool' = False) -> 'TransactionResult'
```

### sell

Sell; types, defaults and return value are specified below.

```python
async sell(self, request: 'SellTokenRequest', broadcast: 'bool' = False, wait_receipt: 'bool' = False) -> 'TransactionResult'
```

### token_address_by_symbol

Token address by symbol; types, defaults and return value are specified below.

```python
async token_address_by_symbol(self, symbol: 'str') -> 'str | None'
```

### update_details

Update details; types, defaults and return value are specified below.

```python
async update_details(self, request: 'UpdateTokenDetailsRequest', broadcast: 'bool' = False, wait_receipt: 'bool' = False) -> 'TransactionResult'
```

## token_creation_commission_del

Token creation commission del; types, defaults and return value are specified below.

```python
token_creation_commission_del(symbol: 'str') -> 'Decimal'
```

## token_creation_commission_wei

Token creation commission wei; types, defaults and return value are specified below.

```python
token_creation_commission_wei(symbol: 'str') -> 'int'
```

## token_creation_required_reserve_del

Token creation required reserve del; types, defaults and return value are specified below.

```python
token_creation_required_reserve_del(symbol: 'str', extra_reserve_del: 'Decimal | str | int' = 0) -> 'Decimal'
```

## token_creation_required_reserve_wei

Token creation required reserve wei; types, defaults and return value are specified below.

```python
token_creation_required_reserve_wei(symbol: 'str', extra_reserve_wei: 'int' = 0) -> 'int'
```
