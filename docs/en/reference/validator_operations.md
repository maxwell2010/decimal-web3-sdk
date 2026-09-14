# validator_operations

[Index](../api.md)

Signatures are generated from the release source. Required fields have no default.

## ValidatorDescription

Validatordescription; types, defaults and return value are specified below.

```python
ValidatorDescription(moniker: 'str', identity: 'str' = '', website: 'str' = '', security_contact: 'str' = '', details: 'str' = '') -> None
```

- `moniker`: `str`; required.
- `identity`: `str`; ''.
- `website`: `str`; ''.
- `security_contact`: `str`; ''.
- `details`: `str`; ''.

## ValidatorMetadata

Validatormetadata; types, defaults and return value are specified below.

```python
ValidatorMetadata(operator_address: 'str', reward_address: 'str', consensus_pubkey: 'str', description: 'ValidatorDescription', commission: 'str') -> None
```

- `operator_address`: `str`; required.
- `reward_address`: `str`; required.
- `consensus_pubkey`: `str`; required.
- `description`: `ValidatorDescription`; required.
- `commission`: `str`; required.

### from_dict

From dict; types, defaults and return value are specified below.

```python
from_dict(value: 'dict') -> "'ValidatorMetadata'"
```

### to_json

To json; types, defaults and return value are specified below.

```python
to_json(self) -> 'str'
```

## AddValidatorTokenRequest

Addvalidatortokenrequest; types, defaults and return value are specified below.

```python
AddValidatorTokenRequest(metadata: 'ValidatorMetadata', token: 'str', amount_raw: 'int', *, private_key: 'str') -> None
```

- `private_key`: `str`; use from_mnemonic; technical field, hidden in repr.
- `metadata`: `ValidatorMetadata`; required.
- `token`: `str`; required.
- `amount_raw`: `int`; required.

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

## AddValidatorDelRequest

Addvalidatordelrequest; types, defaults and return value are specified below.

```python
AddValidatorDelRequest(metadata: 'ValidatorMetadata', amount_del: 'Decimal | str | int', *, private_key: 'str') -> None
```

- `private_key`: `str`; use from_mnemonic; technical field, hidden in repr.
- `metadata`: `ValidatorMetadata`; required.
- `amount_del`: `Decimal | str | int`; required.

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

## RemoveValidatorRequest

Removevalidatorrequest; types, defaults and return value are specified below.

```python
RemoveValidatorRequest(validator: 'str', *, private_key: 'str') -> None
```

- `private_key`: `str`; use from_mnemonic; technical field, hidden in repr.
- `validator`: `str`; required.

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

## UpdateValidatorMetadataRequest

Updatevalidatormetadatarequest; types, defaults and return value are specified below.

```python
UpdateValidatorMetadataRequest(metadata: 'ValidatorMetadata', *, private_key: 'str') -> None
```

- `private_key`: `str`; use from_mnemonic; technical field, hidden in repr.
- `metadata`: `ValidatorMetadata`; required.

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

## ValidatorOperations

Validatoroperations; types, defaults and return value are specified below.

### add_validator_del

Add validator del; types, defaults and return value are specified below.

```python
async add_validator_del(self, request: 'AddValidatorDelRequest', broadcast: 'bool' = False, wait_receipt: 'bool' = False) -> 'TransactionResult'
```

### add_validator_token

Add validator token; types, defaults and return value are specified below.

```python
async add_validator_token(self, request: 'AddValidatorTokenRequest', broadcast: 'bool' = False, wait_receipt: 'bool' = False) -> 'TransactionResult'
```

### remove_validator

Remove validator; types, defaults and return value are specified below.

```python
async remove_validator(self, request: 'RemoveValidatorRequest', broadcast: 'bool' = False, wait_receipt: 'bool' = False) -> 'TransactionResult'
```

### update_validator_metadata

Update validator metadata; types, defaults and return value are specified below.

```python
async update_validator_metadata(self, request: 'UpdateValidatorMetadataRequest', broadcast: 'bool' = False, wait_receipt: 'bool' = False) -> 'TransactionResult'
```
