# staking_operations

[Index](../api.md)

Signatures are generated from the release source. Required fields have no default.

## CompleteStakeRequest

Completestakerequest; types, defaults and return value are specified below.

```python
CompleteStakeRequest(indexes: 'tuple[int, ...]', *, private_key: 'str') -> None
```

- `private_key`: `str`; use from_mnemonic; technical field, hidden in repr.
- `indexes`: `tuple[int, ...]`; required.

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

## ApplyStakePenaltyRequest

Applystakepenaltyrequest; types, defaults and return value are specified below.

```python
ApplyStakePenaltyRequest(validator: 'str', delegator: 'str', token: 'str', allow_legacy: 'bool' = False, *, private_key: 'str') -> None
```

- `private_key`: `str`; use from_mnemonic; technical field, hidden in repr.
- `validator`: `str`; required.
- `delegator`: `str`; required.
- `token`: `str`; required.
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

## ApplyStakePenaltiesRequest

Applystakepenaltiesrequest; types, defaults and return value are specified below.

```python
ApplyStakePenaltiesRequest(validator: 'str', delegator: 'str', token: 'str', allow_legacy: 'bool' = False, *, private_key: 'str') -> None
```

- `private_key`: `str`; use from_mnemonic; technical field, hidden in repr.
- `validator`: `str`; required.
- `delegator`: `str`; required.
- `token`: `str`; required.
- `allow_legacy`: `bool`; False.

### from_mnemonic

Derive the technical signing key locally; pass request fields as keyword arguments.

```python
from_mnemonic(*, mnemonic: 'str', passphrase: 'str' = '', account_path: 'str' = "m/44'/60'/0'/0/0", account_index: 'int | None' = None, **kwargs) -> 'T'
```

## StakingOperations

Stakingoperations; types, defaults and return value are specified below.

### apply_stake_penalties

Apply stake penalties; types, defaults and return value are specified below.

```python
async apply_stake_penalties(self, request: 'ApplyStakePenaltiesRequest', broadcast: 'bool' = False, wait_receipt: 'bool' = False) -> 'TransactionResult'
```

### apply_stake_penalty

Apply stake penalty; types, defaults and return value are specified below.

```python
async apply_stake_penalty(self, request: 'ApplyStakePenaltyRequest', broadcast: 'bool' = False, wait_receipt: 'bool' = False) -> 'TransactionResult'
```

### complete_stake

Complete stake; types, defaults and return value are specified below.

```python
async complete_stake(self, request: 'CompleteStakeRequest', broadcast: 'bool' = False, wait_receipt: 'bool' = False) -> 'TransactionResult'
```
