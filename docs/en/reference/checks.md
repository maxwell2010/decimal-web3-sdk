# checks

[Index](../api.md)

Signatures are generated from the release source. Required fields have no default.

## CreateChecksDelRequest

Createchecksdelrequest; types, defaults and return value are specified below.

```python
CreateChecksDelRequest(contract: 'str', signers: 'list[str]', amount_wei: 'int', due_block: 'int', private_key: 'str', nonce: 'int | None' = None) -> None
```

- `contract`: `str`; required.
- `signers`: `list[str]`; required.
- `amount_wei`: `int`; required.
- `due_block`: `int`; required.
- `private_key`: `str`; use from_mnemonic; technical field, hidden in repr.
- `nonce`: `int | None`; None.

### from_mnemonic

Derive the technical signing key locally; pass request fields as keyword arguments.

```python
from_mnemonic(*, mnemonic: 'str', passphrase: 'str' = '', account_path: 'str' = "m/44'/60'/0'/0/0", account_index: 'int | None' = None, **kwargs) -> 'T'
```

## CreateChecksTokenRequest

Createcheckstokenrequest; types, defaults and return value are specified below.

```python
CreateChecksTokenRequest(contract: 'str', token: 'str', signers: 'list[str]', amount_raw: 'int', due_block: 'int', private_key: 'str', nonce: 'int | None' = None, permit: 'PermitSignature | None' = None) -> None
```

- `contract`: `str`; required.
- `token`: `str`; required.
- `signers`: `list[str]`; required.
- `amount_raw`: `int`; required.
- `due_block`: `int`; required.
- `private_key`: `str`; use from_mnemonic; technical field, hidden in repr.
- `nonce`: `int | None`; None.
- `permit`: `PermitSignature | None`; None.

### from_mnemonic

Derive the technical signing key locally; pass request fields as keyword arguments.

```python
from_mnemonic(*, mnemonic: 'str', passphrase: 'str' = '', account_path: 'str' = "m/44'/60'/0'/0/0", account_index: 'int | None' = None, **kwargs) -> 'T'
```

## RedeemChecksRequest

Redeemchecksrequest; types, defaults and return value are specified below.

```python
RedeemChecksRequest(contract: 'str', signatures: 'list[str]', checks: 'list[str]', private_key: 'str') -> None
```

- `contract`: `str`; required.
- `signatures`: `list[str]`; required.
- `checks`: `list[str]`; required.
- `private_key`: `str`; use from_mnemonic; technical field, hidden in repr.

### from_mnemonic

Derive the technical signing key locally; pass request fields as keyword arguments.

```python
from_mnemonic(*, mnemonic: 'str', passphrase: 'str' = '', account_path: 'str' = "m/44'/60'/0'/0/0", account_index: 'int | None' = None, **kwargs) -> 'T'
```

## ChecksService

Checksservice; types, defaults and return value are specified below.

### create_del

Create del; types, defaults and return value are specified below.

```python
async create_del(self, request: 'CreateChecksDelRequest', broadcast: 'bool' = False, wait_receipt: 'bool' = False) -> 'TransactionResult'
```

### create_token

Create token; types, defaults and return value are specified below.

```python
async create_token(self, request: 'CreateChecksTokenRequest', broadcast: 'bool' = False, wait_receipt: 'bool' = False) -> 'TransactionResult'
```

### redeem

Redeem; types, defaults and return value are specified below.

```python
async redeem(self, request: 'RedeemChecksRequest', broadcast: 'bool' = False, wait_receipt: 'bool' = False) -> 'TransactionResult'
```
