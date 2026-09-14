# bridge

[Index](../api.md)

Signatures are generated from the release source. Required fields have no default.

## BridgeTransferNativeRequest

Bridgetransfernativerequest; types, defaults and return value are specified below.

```python
BridgeTransferNativeRequest(contract: 'str', to: 'str', amount_wei: 'int', service_fee_wei: 'int', to_chain_id: 'int', nonce: 'int', private_key: 'str') -> None
```

- `contract`: `str`; required.
- `to`: `str`; required.
- `amount_wei`: `int`; required.
- `service_fee_wei`: `int`; required.
- `to_chain_id`: `int`; required.
- `nonce`: `int`; required.
- `private_key`: `str`; use from_mnemonic; technical field, hidden in repr.

### from_mnemonic

Derive the technical signing key locally; pass request fields as keyword arguments.

```python
from_mnemonic(*, mnemonic: 'str', passphrase: 'str' = '', account_path: 'str' = "m/44'/60'/0'/0/0", account_index: 'int | None' = None, **kwargs) -> 'T'
```

## BridgeTransferTokenRequest

Bridgetransfertokenrequest; types, defaults and return value are specified below.

```python
BridgeTransferTokenRequest(contract: 'str', token: 'str', to: 'str', amount_raw: 'int', service_fee_wei: 'int', to_chain_id: 'int', nonce: 'int', private_key: 'str') -> None
```

- `contract`: `str`; required.
- `token`: `str`; required.
- `to`: `str`; required.
- `amount_raw`: `int`; required.
- `service_fee_wei`: `int`; required.
- `to_chain_id`: `int`; required.
- `nonce`: `int`; required.
- `private_key`: `str`; use from_mnemonic; technical field, hidden in repr.

### from_mnemonic

Derive the technical signing key locally; pass request fields as keyword arguments.

```python
from_mnemonic(*, mnemonic: 'str', passphrase: 'str' = '', account_path: 'str' = "m/44'/60'/0'/0/0", account_index: 'int | None' = None, **kwargs) -> 'T'
```

## BridgeCompleteTransferRequest

Bridgecompletetransferrequest; types, defaults and return value are specified below.

```python
BridgeCompleteTransferRequest(contract: 'str', encoded_vm: 'str', unwrap_weth: 'bool', private_key: 'str') -> None
```

- `contract`: `str`; required.
- `encoded_vm`: `str`; required.
- `unwrap_weth`: `bool`; required.
- `private_key`: `str`; use from_mnemonic; technical field, hidden in repr.

### from_mnemonic

Derive the technical signing key locally; pass request fields as keyword arguments.

```python
from_mnemonic(*, mnemonic: 'str', passphrase: 'str' = '', account_path: 'str' = "m/44'/60'/0'/0/0", account_index: 'int | None' = None, **kwargs) -> 'T'
```

## BridgeService

Bridgeservice; types, defaults and return value are specified below.

### complete_transfer

Complete transfer; types, defaults and return value are specified below.

```python
async complete_transfer(self, request: 'BridgeCompleteTransferRequest', broadcast: 'bool' = False, wait_receipt: 'bool' = False) -> 'TransactionResult'
```

### transfer_native

Transfer native; types, defaults and return value are specified below.

```python
async transfer_native(self, request: 'BridgeTransferNativeRequest', broadcast: 'bool' = False, wait_receipt: 'bool' = False) -> 'TransactionResult'
```

### transfer_token

Transfer token; types, defaults and return value are specified below.

```python
async transfer_token(self, request: 'BridgeTransferTokenRequest', broadcast: 'bool' = False, wait_receipt: 'bool' = False) -> 'TransactionResult'
```
