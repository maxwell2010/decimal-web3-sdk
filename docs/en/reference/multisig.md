# multisig

[Index](../api.md)

Signatures are generated from the release source. Required fields have no default.

## WeightedOwner

Weightedowner; types, defaults and return value are specified below.

```python
WeightedOwner(owner: 'str', weight: 'int' = 1) -> None
```

- `owner`: `str`; required.
- `weight`: `int`; 1.

## SafeTransaction

Safetransaction; types, defaults and return value are specified below.

```python
SafeTransaction(to: 'str', nonce: 'int', value_wei: 'int' = 0, data: 'str' = '0x', operation: 'Literal[0, 1]' = 0, safe_tx_gas: 'int' = 0, base_gas: 'int' = 0, gas_price_wei: 'int' = 0, gas_token: 'str' = '0x0000000000000000000000000000000000000000', refund_receiver: 'str' = '0x0000000000000000000000000000000000000000') -> None
```

- `to`: `str`; required.
- `nonce`: `int`; required.
- `value_wei`: `int`; 0.
- `data`: `str`; '0x'.
- `operation`: `Literal[0, 1]`; 0.
- `safe_tx_gas`: `int`; 0.
- `base_gas`: `int`; 0.
- `gas_price_wei`: `int`; 0.
- `gas_token`: `str`; '0x0000000000000000000000000000000000000000'.
- `refund_receiver`: `str`; '0x0000000000000000000000000000000000000000'.

### values

Values; types, defaults and return value are specified below.

```python
values(self) -> 'tuple'
```

## safe_typed_data

Safe typed data; types, defaults and return value are specified below.

```python
safe_typed_data(safe: 'str', chain_id: 'int', transaction: 'SafeTransaction')
```

## safe_transaction_hash

Safe transaction hash; types, defaults and return value are specified below.

```python
safe_transaction_hash(safe: 'str', chain_id: 'int', transaction: 'SafeTransaction') -> 'str'
```

## SafeSignature

Safesignature; types, defaults and return value are specified below.

```python
SafeSignature(signer: 'str', data: 'str', kind: "Literal['eip712', 'eth_sign', 'approved_hash', 'contract']" = 'eip712') -> None
```

- `signer`: `str`; required.
- `data`: `str`; required.
- `kind`: `Literal['eip712', 'eth_sign', 'approved_hash', 'contract']`; 'eip712'.

### preapproved

Preapproved; types, defaults and return value are specified below.

```python
preapproved(signer: 'str') -> "'SafeSignature'"
```

## SignSafeTransactionRequest

Signsafetransactionrequest; types, defaults and return value are specified below.

```python
SignSafeTransactionRequest(safe: 'str', chain_id: 'int', transaction: 'SafeTransaction', private_key: 'str') -> None
```

- `safe`: `str`; required.
- `chain_id`: `int`; required.
- `transaction`: `SafeTransaction`; required.
- `private_key`: `str`; use from_mnemonic; technical field, hidden in repr.

### from_mnemonic

Derive the technical signing key locally; pass request fields as keyword arguments.

```python
from_mnemonic(*, mnemonic: 'str', passphrase: 'str' = '', account_path: 'str' = "m/44'/60'/0'/0/0", account_index: 'int | None' = None, **kwargs) -> 'T'
```

## sign_safe_transaction

Sign safe transaction; types, defaults and return value are specified below.

```python
sign_safe_transaction(request: 'SignSafeTransactionRequest') -> 'SafeSignature'
```

## pack_safe_signatures

Pack safe signatures; types, defaults and return value are specified below.

```python
pack_safe_signatures(safe: 'str', chain_id: 'int', transaction: 'SafeTransaction', signatures: 'tuple[SafeSignature, ...]') -> 'bytes'
```

## CreateMultisigRequest

Createmultisigrequest; types, defaults and return value are specified below.

```python
CreateMultisigRequest(owners: 'tuple[WeightedOwner, ...]', weight_threshold: 'int', salt_nonce: 'int', fallback_handler: 'str' = '0x0000000000000000000000000000000000000000', *, private_key: 'str') -> None
```

- `private_key`: `str`; use from_mnemonic; technical field, hidden in repr.
- `owners`: `tuple[WeightedOwner, ...]`; required.
- `weight_threshold`: `int`; required.
- `salt_nonce`: `int`; required.
- `fallback_handler`: `str`; '0x0000000000000000000000000000000000000000'.

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

## ApproveMultisigTransactionRequest

Approvemultisigtransactionrequest; types, defaults and return value are specified below.

```python
ApproveMultisigTransactionRequest(safe: 'str', transaction: 'SafeTransaction', *, private_key: 'str') -> None
```

- `private_key`: `str`; use from_mnemonic; technical field, hidden in repr.
- `safe`: `str`; required.
- `transaction`: `SafeTransaction`; required.

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

## ExecuteMultisigTransactionRequest

Executemultisigtransactionrequest; types, defaults and return value are specified below.

```python
ExecuteMultisigTransactionRequest(safe: 'str', transaction: 'SafeTransaction', signatures: 'tuple[SafeSignature, ...]', *, private_key: 'str') -> None
```

- `private_key`: `str`; use from_mnemonic; technical field, hidden in repr.
- `safe`: `str`; required.
- `transaction`: `SafeTransaction`; required.
- `signatures`: `tuple[SafeSignature, ...]`; required.

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

## MultisigState

Multisigstate; types, defaults and return value are specified below.

```python
MultisigState(nonce: 'int', owners: 'tuple[WeightedOwner, ...]', weight_threshold: 'int', block_number: 'int') -> None
```

- `nonce`: `int`; required.
- `owners`: `tuple[WeightedOwner, ...]`; required.
- `weight_threshold`: `int`; required.
- `block_number`: `int`; required.

## MultisigService

Multisigservice; types, defaults and return value are specified below.

### approve_transaction

Approve transaction; types, defaults and return value are specified below.

```python
async approve_transaction(self, request: 'ApproveMultisigTransactionRequest', broadcast: 'bool' = False, wait_receipt: 'bool' = False) -> 'TransactionResult'
```

### build_operation

Build transaction data/draft without broadcasting. See units and ABI constraints in the module guide.

```python
async build_operation(self, request: 'ContractOperationRequest') -> 'TransactionDraft'
```

### build_transaction

Build transaction data/draft without broadcasting. See units and ABI constraints in the module guide.

```python
async build_transaction(self, safe: 'str', call: 'ContractCallRequest | TransactionDraft', *, nonce: 'int | None' = None) -> 'SafeTransaction'
```

### check_execution_result

Check execution result; types, defaults and return value are specified below.

```python
check_execution_result(self, safe: 'str', transaction: 'SafeTransaction', result: 'TransactionResult') -> 'TransactionResult'
```

### create

Create; types, defaults and return value are specified below.

```python
async create(self, request: 'CreateMultisigRequest', broadcast: 'bool' = False, wait_receipt: 'bool' = False) -> 'TransactionResult'
```

### execute

Execute; types, defaults and return value are specified below.

```python
async execute(self, request: 'ExecuteMultisigTransactionRequest', broadcast: 'bool' = False, wait_receipt: 'bool' = False) -> 'TransactionResult'
```

### state

State; types, defaults and return value are specified below.

```python
async state(self, safe: 'str') -> 'MultisigState'
```
