# nft_operations

[Index](../api.md)

Signatures are generated from the release source. Required fields have no default.

## CreateReservelessNftCollectionRequest

Createreservelessnftcollectionrequest; types, defaults and return value are specified below.

```python
CreateReservelessNftCollectionRequest(kind: "Literal['erc721', 'erc1155']", creator: 'str', symbol: 'str', name: 'str', contract_uri: 'str', burnable: 'bool' = True, *, private_key: 'str') -> None
```

- `private_key`: `str`; use from_mnemonic; technical field, hidden in repr.
- `kind`: `Literal['erc721', 'erc1155']`; required.
- `creator`: `str`; required.
- `symbol`: `str`; required.
- `name`: `str`; required.
- `contract_uri`: `str`; required.
- `burnable`: `bool`; True.

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

## AddTokenReserveNftRequest

Addtokenreservenftrequest; types, defaults and return value are specified below.

```python
AddTokenReserveNftRequest(nft: 'str', token_id: 'int', reserve_amount_raw: 'int', permit: 'PermitSignature | None' = None, *, private_key: 'str') -> None
```

- `private_key`: `str`; use from_mnemonic; technical field, hidden in repr.
- `nft`: `str`; required.
- `token_id`: `int`; required.
- `reserve_amount_raw`: `int`; required.
- `permit`: `PermitSignature | None`; None.

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

## NftStakeOperationRequest

Nftstakeoperationrequest; types, defaults and return value are specified below.

```python
NftStakeOperationRequest(validator: 'str', nft: 'str', token_id: 'int', *, private_key: 'str') -> None
```

- `private_key`: `str`; use from_mnemonic; technical field, hidden in repr.
- `validator`: `str`; required.
- `nft`: `str`; required.
- `token_id`: `int`; required.

### from_mnemonic

Derive the technical signing key locally; pass request fields as keyword arguments.

```python
from_mnemonic(*, mnemonic: 'str', passphrase: 'str' = '', account_path: 'str' = "m/44'/60'/0'/0/0", account_index: 'int | None' = None, **kwargs) -> 'T'
```

## StakeNftToHoldRequest

Stakenfttoholdrequest; types, defaults and return value are specified below.

```python
StakeNftToHoldRequest(validator: 'str', nft: 'str', token_id: 'int', amount: 'int', old_hold_timestamp: 'int', new_hold_timestamp: 'int', *, private_key: 'str') -> None
```

- `private_key`: `str`; use from_mnemonic; technical field, hidden in repr.
- `validator`: `str`; required.
- `nft`: `str`; required.
- `token_id`: `int`; required.
- `amount`: `int`; required.
- `old_hold_timestamp`: `int`; required.
- `new_hold_timestamp`: `int`; required.

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

## ResetNftStakeHoldRequest

Resetnftstakeholdrequest; types, defaults and return value are specified below.

```python
ResetNftStakeHoldRequest(validator: 'str', nft: 'str', token_id: 'int', delegator: 'str', hold_timestamp: 'int', *, private_key: 'str') -> None
```

- `private_key`: `str`; use from_mnemonic; technical field, hidden in repr.
- `validator`: `str`; required.
- `nft`: `str`; required.
- `token_id`: `int`; required.
- `delegator`: `str`; required.
- `hold_timestamp`: `int`; required.

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

## ResetNftStakeHoldsRequest

Resetnftstakeholdsrequest; types, defaults and return value are specified below.

```python
ResetNftStakeHoldsRequest(validator: 'str', nft: 'str', token_id: 'int', delegator: 'str', hold_timestamps: 'tuple[int, ...]', *, private_key: 'str') -> None
```

- `private_key`: `str`; use from_mnemonic; technical field, hidden in repr.
- `validator`: `str`; required.
- `nft`: `str`; required.
- `token_id`: `int`; required.
- `delegator`: `str`; required.
- `hold_timestamps`: `tuple[int, ...]`; required.

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

## WithdrawNftWithResetRequest

Withdrawnftwithresetrequest; types, defaults and return value are specified below.

```python
WithdrawNftWithResetRequest(validator: 'str', nft: 'str', token_id: 'int', amount: 'int', hold_timestamps_to_reset: 'tuple[int, ...]', *, private_key: 'str') -> None
```

- `private_key`: `str`; use from_mnemonic; technical field, hidden in repr.
- `validator`: `str`; required.
- `nft`: `str`; required.
- `token_id`: `int`; required.
- `amount`: `int`; required.
- `hold_timestamps_to_reset`: `tuple[int, ...]`; required.

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

## TransferNftWithResetRequest

Transfernftwithresetrequest; types, defaults and return value are specified below.

```python
TransferNftWithResetRequest(validator: 'str', nft: 'str', token_id: 'int', amount: 'int', hold_timestamps_to_reset: 'tuple[int, ...]', new_validator: 'str', *, private_key: 'str') -> None
```

- `private_key`: `str`; use from_mnemonic; technical field, hidden in repr.
- `validator`: `str`; required.
- `nft`: `str`; required.
- `token_id`: `int`; required.
- `amount`: `int`; required.
- `hold_timestamps_to_reset`: `tuple[int, ...]`; required.
- `new_validator`: `str`; required.

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

## HoldNftWithResetRequest

Holdnftwithresetrequest; types, defaults and return value are specified below.

```python
HoldNftWithResetRequest(validator: 'str', nft: 'str', token_id: 'int', amount: 'int', hold_timestamps_to_reset: 'tuple[int, ...]', new_hold_timestamp: 'int', *, private_key: 'str') -> None
```

- `private_key`: `str`; use from_mnemonic; technical field, hidden in repr.
- `validator`: `str`; required.
- `nft`: `str`; required.
- `token_id`: `int`; required.
- `amount`: `int`; required.
- `hold_timestamps_to_reset`: `tuple[int, ...]`; required.
- `new_hold_timestamp`: `int`; required.

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

## CompleteNftStakeRequest

Completenftstakerequest; types, defaults and return value are specified below.

```python
CompleteNftStakeRequest(indexes: 'tuple[int, ...]', *, private_key: 'str') -> None
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

## NftStake

Nftstake; types, defaults and return value are specified below.

```python
NftStake(validator: 'str', delegator: 'str', token: 'str', amount_raw: 'int', token_id: 'int', token_type: 'int', hold_timestamp: 'int', block_number: 'int | None' = None) -> None
```

- `validator`: `str`; required.
- `delegator`: `str`; required.
- `token`: `str`; required.
- `amount_raw`: `int`; required.
- `token_id`: `int`; required.
- `token_type`: `int`; required.
- `hold_timestamp`: `int`; required.
- `block_number`: `int | None`; None.

### amount

Amount; types, defaults and return value are specified below.

```python
amount(self, decimals: 'int' = 0)
```

### amount_string

Amount string; types, defaults and return value are specified below.

```python
amount_string(self, decimals: 'int' = 0) -> 'str'
```

### as_dict

As dict; types, defaults and return value are specified below.

```python
as_dict(self, decimals: 'int' = 0) -> 'dict'
```

## FrozenNftStake

Frozennftstake; types, defaults and return value are specified below.

```python
FrozenNftStake(index: 'int', stake: 'NftStake', freeze_status: 'int', freeze_type: 'int', unfreeze_timestamp: 'int') -> None
```

- `index`: `int`; required.
- `stake`: `NftStake`; required.
- `freeze_status`: `int`; required.
- `freeze_type`: `int`; required.
- `unfreeze_timestamp`: `int`; required.

### as_dict

As dict; types, defaults and return value are specified below.

```python
as_dict(self) -> 'dict'
```

## NftOperations

Nftoperations; types, defaults and return value are specified below.

### add_token_reserve

Add token reserve; types, defaults and return value are specified below.

```python
async add_token_reserve(self, request: 'AddTokenReserveNftRequest', broadcast: 'bool' = False, wait_receipt: 'bool' = False) -> 'TransactionResult'
```

### complete_stake

Complete stake; types, defaults and return value are specified below.

```python
async complete_stake(self, request: 'CompleteNftStakeRequest', broadcast: 'bool' = False, wait_receipt: 'bool' = False) -> 'TransactionResult'
```

### create_reserveless_collection

Create reserveless collection; types, defaults and return value are specified below.

```python
async create_reserveless_collection(self, request: 'CreateReservelessNftCollectionRequest', broadcast: 'bool' = False, wait_receipt: 'bool' = False) -> 'TransactionResult'
```

### get_freeze_time

Get freeze time; types, defaults and return value are specified below.

```python
async get_freeze_time(self, freeze_type: 'Literal[1, 2]', *, block_identifier='latest') -> 'int'
```

### get_frozen_stake

Get frozen stake; types, defaults and return value are specified below.

```python
async get_frozen_stake(self, index: 'int', *, block_identifier='latest') -> 'FrozenNftStake'
```

### get_frozen_stakes

Get frozen stakes; types, defaults and return value are specified below.

```python
async get_frozen_stakes(self, indexes: 'tuple[int, ...]', *, block_identifier='latest') -> 'tuple[FrozenNftStake, ...]'
```

### get_hold_stake

Get hold stake; types, defaults and return value are specified below.

```python
async get_hold_stake(self, validator: 'str', delegator: 'str', nft: 'str', token_id: 'int', hold_timestamp: 'int', *, block_identifier='latest') -> 'NftStake'
```

### get_stake

Get stake; types, defaults and return value are specified below.

```python
async get_stake(self, validator: 'str', delegator: 'str', nft: 'str', token_id: 'int', *, block_identifier='latest') -> 'NftStake'
```

### get_stake_id

Get stake id; types, defaults and return value are specified below.

```python
async get_stake_id(self, validator: 'str', delegator: 'str', nft: 'str', token_id: 'int', *, block_identifier='latest') -> 'str'
```

### hold_with_reset

Hold with reset; types, defaults and return value are specified below.

```python
async hold_with_reset(self, request: 'HoldNftWithResetRequest', broadcast: 'bool' = False, wait_receipt: 'bool' = False) -> 'TransactionResult'
```

### reset_stake_hold

Reset stake hold; types, defaults and return value are specified below.

```python
async reset_stake_hold(self, request: 'ResetNftStakeHoldRequest', broadcast: 'bool' = False, wait_receipt: 'bool' = False) -> 'TransactionResult'
```

### reset_stake_holds

Reset stake holds; types, defaults and return value are specified below.

```python
async reset_stake_holds(self, request: 'ResetNftStakeHoldsRequest', broadcast: 'bool' = False, wait_receipt: 'bool' = False) -> 'TransactionResult'
```

### stake_to_hold

Stake to hold; types, defaults and return value are specified below.

```python
async stake_to_hold(self, request: 'StakeNftToHoldRequest', broadcast: 'bool' = False, wait_receipt: 'bool' = False) -> 'TransactionResult'
```

### transfer_with_reset

Transfer with reset; types, defaults and return value are specified below.

```python
async transfer_with_reset(self, request: 'TransferNftWithResetRequest', broadcast: 'bool' = False, wait_receipt: 'bool' = False) -> 'TransactionResult'
```

### withdraw_with_reset

Withdraw with reset; types, defaults and return value are specified below.

```python
async withdraw_with_reset(self, request: 'WithdrawNftWithResetRequest', broadcast: 'bool' = False, wait_receipt: 'bool' = False) -> 'TransactionResult'
```
