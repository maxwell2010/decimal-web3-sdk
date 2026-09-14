# nft

[Index](../api.md)

Signatures are generated from the release source. Required fields have no default.

## CreateNftCollectionRequest

Createnftcollectionrequest; types, defaults and return value are specified below.

```python
CreateNftCollectionRequest(kind: 'NftKind', symbol: 'str', name: 'str', contract_uri: 'str', private_key: 'str', refundable: 'bool' = False, creator: 'str | None' = None) -> None
```

- `kind`: `NftKind`; required.
- `symbol`: `str`; required.
- `name`: `str`; required.
- `contract_uri`: `str`; required.
- `private_key`: `str`; use from_mnemonic; technical field, hidden in repr.
- `refundable`: `bool`; False.
- `creator`: `str | None`; None.

### from_mnemonic

Derive the technical signing key locally; pass request fields as keyword arguments.

```python
from_mnemonic(*, mnemonic: 'str', passphrase: 'str' = '', account_path: 'str' = "m/44'/60'/0'/0/0", account_index: 'int | None' = None, **kwargs) -> 'T'
```

## MintNftRequest

Mintnftrequest; types, defaults and return value are specified below.

```python
MintNftRequest(kind: 'NftKind', nft: 'str', to: 'str', token_uri: 'str', private_key: 'str', token_id: 'int | None' = None, amount: 'int' = 1, reserve_amount_raw: 'int' = 0, reserve_token: 'str' = '0x0000000000000000000000000000000000000000', value_wei: 'int' = 0) -> None
```

- `kind`: `NftKind`; required.
- `nft`: `str`; required.
- `to`: `str`; required.
- `token_uri`: `str`; required.
- `private_key`: `str`; use from_mnemonic; technical field, hidden in repr.
- `token_id`: `int | None`; None.
- `amount`: `int`; 1.
- `reserve_amount_raw`: `int`; 0.
- `reserve_token`: `str`; '0x0000000000000000000000000000000000000000'.
- `value_wei`: `int`; 0.

### from_mnemonic

Derive the technical signing key locally; pass request fields as keyword arguments.

```python
from_mnemonic(*, mnemonic: 'str', passphrase: 'str' = '', account_path: 'str' = "m/44'/60'/0'/0/0", account_index: 'int | None' = None, **kwargs) -> 'T'
```

## NftTransferRequest

Nfttransferrequest; types, defaults and return value are specified below.

```python
NftTransferRequest(kind: 'NftKind', nft: 'str', to: 'str', token_id: 'int', private_key: 'str', amount: 'int' = 1, data: 'bytes' = b'') -> None
```

- `kind`: `NftKind`; required.
- `nft`: `str`; required.
- `to`: `str`; required.
- `token_id`: `int`; required.
- `private_key`: `str`; use from_mnemonic; technical field, hidden in repr.
- `amount`: `int`; 1.
- `data`: `bytes`; b''.

### from_mnemonic

Derive the technical signing key locally; pass request fields as keyword arguments.

```python
from_mnemonic(*, mnemonic: 'str', passphrase: 'str' = '', account_path: 'str' = "m/44'/60'/0'/0/0", account_index: 'int | None' = None, **kwargs) -> 'T'
```

## NftBatchTransferRequest

Nftbatchtransferrequest; types, defaults and return value are specified below.

```python
NftBatchTransferRequest(nft: 'str', to: 'str', token_ids: 'list[int]', amounts: 'list[int]', private_key: 'str', data: 'bytes' = b'') -> None
```

- `nft`: `str`; required.
- `to`: `str`; required.
- `token_ids`: `list[int]`; required.
- `amounts`: `list[int]`; required.
- `private_key`: `str`; use from_mnemonic; technical field, hidden in repr.
- `data`: `bytes`; b''.

### from_mnemonic

Derive the technical signing key locally; pass request fields as keyword arguments.

```python
from_mnemonic(*, mnemonic: 'str', passphrase: 'str' = '', account_path: 'str' = "m/44'/60'/0'/0/0", account_index: 'int | None' = None, **kwargs) -> 'T'
```

## NftApprovalRequest

Nftapprovalrequest; types, defaults and return value are specified below.

```python
NftApprovalRequest(kind: 'NftKind', nft: 'str', operator: 'str', approved: 'bool', private_key: 'str') -> None
```

- `kind`: `NftKind`; required.
- `nft`: `str`; required.
- `operator`: `str`; required.
- `approved`: `bool`; required.
- `private_key`: `str`; use from_mnemonic; technical field, hidden in repr.

### from_mnemonic

Derive the technical signing key locally; pass request fields as keyword arguments.

```python
from_mnemonic(*, mnemonic: 'str', passphrase: 'str' = '', account_path: 'str' = "m/44'/60'/0'/0/0", account_index: 'int | None' = None, **kwargs) -> 'T'
```

## NftApproveRequest

Nftapproverequest; types, defaults and return value are specified below.

```python
NftApproveRequest(nft: 'str', to: 'str', token_id: 'int', private_key: 'str') -> None
```

- `nft`: `str`; required.
- `to`: `str`; required.
- `token_id`: `int`; required.
- `private_key`: `str`; use from_mnemonic; technical field, hidden in repr.

### from_mnemonic

Derive the technical signing key locally; pass request fields as keyword arguments.

```python
from_mnemonic(*, mnemonic: 'str', passphrase: 'str' = '', account_path: 'str' = "m/44'/60'/0'/0/0", account_index: 'int | None' = None, **kwargs) -> 'T'
```

## BurnNftRequest

Burnnftrequest; types, defaults and return value are specified below.

```python
BurnNftRequest(kind: 'NftKind', nft: 'str', token_id: 'int', private_key: 'str', amount: 'int' = 1) -> None
```

- `kind`: `NftKind`; required.
- `nft`: `str`; required.
- `token_id`: `int`; required.
- `private_key`: `str`; use from_mnemonic; technical field, hidden in repr.
- `amount`: `int`; 1.

### from_mnemonic

Derive the technical signing key locally; pass request fields as keyword arguments.

```python
from_mnemonic(*, mnemonic: 'str', passphrase: 'str' = '', account_path: 'str' = "m/44'/60'/0'/0/0", account_index: 'int | None' = None, **kwargs) -> 'T'
```

## DisableMintNftRequest

Disablemintnftrequest; types, defaults and return value are specified below.

```python
DisableMintNftRequest(kind: 'NftKind', nft: 'str', private_key: 'str') -> None
```

- `kind`: `NftKind`; required.
- `nft`: `str`; required.
- `private_key`: `str`; use from_mnemonic; technical field, hidden in repr.

### from_mnemonic

Derive the technical signing key locally; pass request fields as keyword arguments.

```python
from_mnemonic(*, mnemonic: 'str', passphrase: 'str' = '', account_path: 'str' = "m/44'/60'/0'/0/0", account_index: 'int | None' = None, **kwargs) -> 'T'
```

## SetTokenUriNftRequest

Settokenurinftrequest; types, defaults and return value are specified below.

```python
SetTokenUriNftRequest(kind: 'NftKind', nft: 'str', token_id: 'int', token_uri: 'str', private_key: 'str') -> None
```

- `kind`: `NftKind`; required.
- `nft`: `str`; required.
- `token_id`: `int`; required.
- `token_uri`: `str`; required.
- `private_key`: `str`; use from_mnemonic; technical field, hidden in repr.

### from_mnemonic

Derive the technical signing key locally; pass request fields as keyword arguments.

```python
from_mnemonic(*, mnemonic: 'str', passphrase: 'str' = '', account_path: 'str' = "m/44'/60'/0'/0/0", account_index: 'int | None' = None, **kwargs) -> 'T'
```

## AddDelReserveNftRequest

Adddelreservenftrequest; types, defaults and return value are specified below.

```python
AddDelReserveNftRequest(kind: 'NftKind', nft: 'str', token_id: 'int', reserve_wei: 'int', private_key: 'str') -> None
```

- `kind`: `NftKind`; required.
- `nft`: `str`; required.
- `token_id`: `int`; required.
- `reserve_wei`: `int`; required.
- `private_key`: `str`; use from_mnemonic; technical field, hidden in repr.

### from_mnemonic

Derive the technical signing key locally; pass request fields as keyword arguments.

```python
from_mnemonic(*, mnemonic: 'str', passphrase: 'str' = '', account_path: 'str' = "m/44'/60'/0'/0/0", account_index: 'int | None' = None, **kwargs) -> 'T'
```

## DelegateNftRequest

Delegatenftrequest; types, defaults and return value are specified below.

```python
DelegateNftRequest(kind: 'NftKind', nft: 'str', validator: 'str', token_id: 'int', private_key: 'str', amount: 'int' = 1, auto_approve: 'bool' = True) -> None
```

- `kind`: `NftKind`; required.
- `nft`: `str`; required.
- `validator`: `str`; required.
- `token_id`: `int`; required.
- `private_key`: `str`; use from_mnemonic; technical field, hidden in repr.
- `amount`: `int`; 1.
- `auto_approve`: `bool`; True.

### from_mnemonic

Derive the technical signing key locally; pass request fields as keyword arguments.

```python
from_mnemonic(*, mnemonic: 'str', passphrase: 'str' = '', account_path: 'str' = "m/44'/60'/0'/0/0", account_index: 'int | None' = None, **kwargs) -> 'T'
```

## HoldNftRequest

Holdnftrequest; types, defaults and return value are specified below.

```python
HoldNftRequest(kind: 'NftKind', nft: 'str', validator: 'str', token_id: 'int', hold_timestamp: 'int', private_key: 'str', amount: 'int' = 1, auto_approve: 'bool' = True) -> None
```

- `kind`: `NftKind`; required.
- `nft`: `str`; required.
- `validator`: `str`; required.
- `token_id`: `int`; required.
- `hold_timestamp`: `int`; required.
- `private_key`: `str`; use from_mnemonic; technical field, hidden in repr.
- `amount`: `int`; 1.
- `auto_approve`: `bool`; True.

### from_mnemonic

Derive the technical signing key locally; pass request fields as keyword arguments.

```python
from_mnemonic(*, mnemonic: 'str', passphrase: 'str' = '', account_path: 'str' = "m/44'/60'/0'/0/0", account_index: 'int | None' = None, **kwargs) -> 'T'
```

## TransferNftStakeRequest

Transfernftstakerequest; types, defaults and return value are specified below.

```python
TransferNftStakeRequest(nft: 'str', validator: 'str', new_validator: 'str', token_id: 'int', private_key: 'str', amount: 'int' = 1, hold_timestamp: 'int | None' = None) -> None
```

- `nft`: `str`; required.
- `validator`: `str`; required.
- `new_validator`: `str`; required.
- `token_id`: `int`; required.
- `private_key`: `str`; use from_mnemonic; technical field, hidden in repr.
- `amount`: `int`; 1.
- `hold_timestamp`: `int | None`; None.

### from_mnemonic

Derive the technical signing key locally; pass request fields as keyword arguments.

```python
from_mnemonic(*, mnemonic: 'str', passphrase: 'str' = '', account_path: 'str' = "m/44'/60'/0'/0/0", account_index: 'int | None' = None, **kwargs) -> 'T'
```

## WithdrawNftRequest

Withdrawnftrequest; types, defaults and return value are specified below.

```python
WithdrawNftRequest(nft: 'str', validator: 'str', token_id: 'int', private_key: 'str', amount: 'int' = 1, hold_timestamp: 'int | None' = None) -> None
```

- `nft`: `str`; required.
- `validator`: `str`; required.
- `token_id`: `int`; required.
- `private_key`: `str`; use from_mnemonic; technical field, hidden in repr.
- `amount`: `int`; 1.
- `hold_timestamp`: `int | None`; None.

### from_mnemonic

Derive the technical signing key locally; pass request fields as keyword arguments.

```python
from_mnemonic(*, mnemonic: 'str', passphrase: 'str' = '', account_path: 'str' = "m/44'/60'/0'/0/0", account_index: 'int | None' = None, **kwargs) -> 'T'
```

## NftService

Nftservice; types, defaults and return value are specified below.

### add_del_reserve

Add del reserve; types, defaults and return value are specified below.

```python
async add_del_reserve(self, request: 'AddDelReserveNftRequest', broadcast: 'bool' = False, wait_receipt: 'bool' = False) -> 'TransactionResult'
```

### approve

Approve; types, defaults and return value are specified below.

```python
async approve(self, request: 'NftApproveRequest', broadcast: 'bool' = False, wait_receipt: 'bool' = False) -> 'TransactionResult'
```

### balance_of

Balance of; types, defaults and return value are specified below.

```python
async balance_of(self, nft: 'str', owner: 'str', token_id: 'int | None' = None, kind: 'NftKind' = 'erc721') -> 'int'
```

### build_operation

Build transaction data/draft without broadcasting. See units and ABI constraints in the module guide.

```python
async build_operation(self, request: 'ContractOperationRequest | WithdrawNftRequest | TransferNftStakeRequest') -> 'TransactionDraft'
```

### build_transfer_stake

Build transaction data/draft without broadcasting. See units and ABI constraints in the module guide.

```python
async build_transfer_stake(self, request: 'TransferNftStakeRequest') -> 'TransactionDraft'
```

### build_withdraw

Build transaction data/draft without broadcasting. See units and ABI constraints in the module guide.

```python
async build_withdraw(self, request: 'WithdrawNftRequest') -> 'TransactionDraft'
```

### burn

Burn; types, defaults and return value are specified below.

```python
async burn(self, request: 'BurnNftRequest', broadcast: 'bool' = False, wait_receipt: 'bool' = False) -> 'TransactionResult'
```

### create_collection

Create collection; types, defaults and return value are specified below.

```python
async create_collection(self, request: 'CreateNftCollectionRequest', broadcast: 'bool' = False, wait_receipt: 'bool' = False) -> 'TransactionResult'
```

### delegate

Delegate; types, defaults and return value are specified below.

```python
async delegate(self, request: 'DelegateNftRequest', broadcast: 'bool' = False, wait_receipt: 'bool' = False) -> 'DecimalWorkflowResult'
```

### disable_mint

Disable mint; types, defaults and return value are specified below.

```python
async disable_mint(self, request: 'DisableMintNftRequest', broadcast: 'bool' = False, wait_receipt: 'bool' = False) -> 'TransactionResult'
```

### hold

Hold; types, defaults and return value are specified below.

```python
async hold(self, request: 'HoldNftRequest', broadcast: 'bool' = False, wait_receipt: 'bool' = False) -> 'DecimalWorkflowResult'
```

### is_approved_for_all

Is approved for all; types, defaults and return value are specified below.

```python
async is_approved_for_all(self, kind: 'NftKind', nft: 'str', owner: 'str', operator: 'str') -> 'bool'
```

### mint

Mint; types, defaults and return value are specified below.

```python
async mint(self, request: 'MintNftRequest', broadcast: 'bool' = False, wait_receipt: 'bool' = False) -> 'TransactionResult'
```

### owner_of

Owner of; types, defaults and return value are specified below.

```python
async owner_of(self, nft: 'str', token_id: 'int') -> 'str'
```

### set_approval_for_all

Set approval for all; types, defaults and return value are specified below.

```python
async set_approval_for_all(self, request: 'NftApprovalRequest', broadcast: 'bool' = False, wait_receipt: 'bool' = False) -> 'TransactionResult'
```

### set_token_uri

Set token uri; types, defaults and return value are specified below.

```python
async set_token_uri(self, request: 'SetTokenUriNftRequest', broadcast: 'bool' = False, wait_receipt: 'bool' = False) -> 'TransactionResult'
```

### transfer

Transfer; types, defaults and return value are specified below.

```python
async transfer(self, request: 'NftTransferRequest', broadcast: 'bool' = False, wait_receipt: 'bool' = False) -> 'TransactionResult'
```

### transfer_batch_erc1155

Transfer batch erc1155; types, defaults and return value are specified below.

```python
async transfer_batch_erc1155(self, request: 'NftBatchTransferRequest', broadcast: 'bool' = False, wait_receipt: 'bool' = False) -> 'TransactionResult'
```

### transfer_stake

Transfer stake; types, defaults and return value are specified below.

```python
async transfer_stake(self, request: 'TransferNftStakeRequest', broadcast: 'bool' = False, wait_receipt: 'bool' = False) -> 'TransactionResult'
```

### withdraw

Withdraw; types, defaults and return value are specified below.

```python
async withdraw(self, request: 'WithdrawNftRequest', broadcast: 'bool' = False, wait_receipt: 'bool' = False) -> 'TransactionResult'
```
