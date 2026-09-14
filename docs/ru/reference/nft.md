# nft

[Index](../api.md)

Сигнатуры сформированы из кода релиза. Обязательные поля не имеют значения по умолчанию.

## CreateNftCollectionRequest

Публичная операция/свойство SDK. Ниже приведены точные типы, значения по умолчанию и тип результата; контекст использования дан в руководстве раздела.

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

Локально получить технический ключ подписи; поля запроса передаются именованными аргументами.

```python
from_mnemonic(*, mnemonic: 'str', passphrase: 'str' = '', account_path: 'str' = "m/44'/60'/0'/0/0", account_index: 'int | None' = None, **kwargs) -> 'T'
```

## MintNftRequest

Публичная операция/свойство SDK. Ниже приведены точные типы, значения по умолчанию и тип результата; контекст использования дан в руководстве раздела.

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

Локально получить технический ключ подписи; поля запроса передаются именованными аргументами.

```python
from_mnemonic(*, mnemonic: 'str', passphrase: 'str' = '', account_path: 'str' = "m/44'/60'/0'/0/0", account_index: 'int | None' = None, **kwargs) -> 'T'
```

## NftTransferRequest

Публичная операция/свойство SDK. Ниже приведены точные типы, значения по умолчанию и тип результата; контекст использования дан в руководстве раздела.

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

Локально получить технический ключ подписи; поля запроса передаются именованными аргументами.

```python
from_mnemonic(*, mnemonic: 'str', passphrase: 'str' = '', account_path: 'str' = "m/44'/60'/0'/0/0", account_index: 'int | None' = None, **kwargs) -> 'T'
```

## NftBatchTransferRequest

Публичная операция/свойство SDK. Ниже приведены точные типы, значения по умолчанию и тип результата; контекст использования дан в руководстве раздела.

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

Локально получить технический ключ подписи; поля запроса передаются именованными аргументами.

```python
from_mnemonic(*, mnemonic: 'str', passphrase: 'str' = '', account_path: 'str' = "m/44'/60'/0'/0/0", account_index: 'int | None' = None, **kwargs) -> 'T'
```

## NftApprovalRequest

Публичная операция/свойство SDK. Ниже приведены точные типы, значения по умолчанию и тип результата; контекст использования дан в руководстве раздела.

```python
NftApprovalRequest(kind: 'NftKind', nft: 'str', operator: 'str', approved: 'bool', private_key: 'str') -> None
```

- `kind`: `NftKind`; required.
- `nft`: `str`; required.
- `operator`: `str`; required.
- `approved`: `bool`; required.
- `private_key`: `str`; use from_mnemonic; technical field, hidden in repr.

### from_mnemonic

Локально получить технический ключ подписи; поля запроса передаются именованными аргументами.

```python
from_mnemonic(*, mnemonic: 'str', passphrase: 'str' = '', account_path: 'str' = "m/44'/60'/0'/0/0", account_index: 'int | None' = None, **kwargs) -> 'T'
```

## NftApproveRequest

Публичная операция/свойство SDK. Ниже приведены точные типы, значения по умолчанию и тип результата; контекст использования дан в руководстве раздела.

```python
NftApproveRequest(nft: 'str', to: 'str', token_id: 'int', private_key: 'str') -> None
```

- `nft`: `str`; required.
- `to`: `str`; required.
- `token_id`: `int`; required.
- `private_key`: `str`; use from_mnemonic; technical field, hidden in repr.

### from_mnemonic

Локально получить технический ключ подписи; поля запроса передаются именованными аргументами.

```python
from_mnemonic(*, mnemonic: 'str', passphrase: 'str' = '', account_path: 'str' = "m/44'/60'/0'/0/0", account_index: 'int | None' = None, **kwargs) -> 'T'
```

## BurnNftRequest

Публичная операция/свойство SDK. Ниже приведены точные типы, значения по умолчанию и тип результата; контекст использования дан в руководстве раздела.

```python
BurnNftRequest(kind: 'NftKind', nft: 'str', token_id: 'int', private_key: 'str', amount: 'int' = 1) -> None
```

- `kind`: `NftKind`; required.
- `nft`: `str`; required.
- `token_id`: `int`; required.
- `private_key`: `str`; use from_mnemonic; technical field, hidden in repr.
- `amount`: `int`; 1.

### from_mnemonic

Локально получить технический ключ подписи; поля запроса передаются именованными аргументами.

```python
from_mnemonic(*, mnemonic: 'str', passphrase: 'str' = '', account_path: 'str' = "m/44'/60'/0'/0/0", account_index: 'int | None' = None, **kwargs) -> 'T'
```

## DisableMintNftRequest

Публичная операция/свойство SDK. Ниже приведены точные типы, значения по умолчанию и тип результата; контекст использования дан в руководстве раздела.

```python
DisableMintNftRequest(kind: 'NftKind', nft: 'str', private_key: 'str') -> None
```

- `kind`: `NftKind`; required.
- `nft`: `str`; required.
- `private_key`: `str`; use from_mnemonic; technical field, hidden in repr.

### from_mnemonic

Локально получить технический ключ подписи; поля запроса передаются именованными аргументами.

```python
from_mnemonic(*, mnemonic: 'str', passphrase: 'str' = '', account_path: 'str' = "m/44'/60'/0'/0/0", account_index: 'int | None' = None, **kwargs) -> 'T'
```

## SetTokenUriNftRequest

Публичная операция/свойство SDK. Ниже приведены точные типы, значения по умолчанию и тип результата; контекст использования дан в руководстве раздела.

```python
SetTokenUriNftRequest(kind: 'NftKind', nft: 'str', token_id: 'int', token_uri: 'str', private_key: 'str') -> None
```

- `kind`: `NftKind`; required.
- `nft`: `str`; required.
- `token_id`: `int`; required.
- `token_uri`: `str`; required.
- `private_key`: `str`; use from_mnemonic; technical field, hidden in repr.

### from_mnemonic

Локально получить технический ключ подписи; поля запроса передаются именованными аргументами.

```python
from_mnemonic(*, mnemonic: 'str', passphrase: 'str' = '', account_path: 'str' = "m/44'/60'/0'/0/0", account_index: 'int | None' = None, **kwargs) -> 'T'
```

## AddDelReserveNftRequest

Публичная операция/свойство SDK. Ниже приведены точные типы, значения по умолчанию и тип результата; контекст использования дан в руководстве раздела.

```python
AddDelReserveNftRequest(kind: 'NftKind', nft: 'str', token_id: 'int', reserve_wei: 'int', private_key: 'str') -> None
```

- `kind`: `NftKind`; required.
- `nft`: `str`; required.
- `token_id`: `int`; required.
- `reserve_wei`: `int`; required.
- `private_key`: `str`; use from_mnemonic; technical field, hidden in repr.

### from_mnemonic

Локально получить технический ключ подписи; поля запроса передаются именованными аргументами.

```python
from_mnemonic(*, mnemonic: 'str', passphrase: 'str' = '', account_path: 'str' = "m/44'/60'/0'/0/0", account_index: 'int | None' = None, **kwargs) -> 'T'
```

## DelegateNftRequest

Публичная операция/свойство SDK. Ниже приведены точные типы, значения по умолчанию и тип результата; контекст использования дан в руководстве раздела.

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

Локально получить технический ключ подписи; поля запроса передаются именованными аргументами.

```python
from_mnemonic(*, mnemonic: 'str', passphrase: 'str' = '', account_path: 'str' = "m/44'/60'/0'/0/0", account_index: 'int | None' = None, **kwargs) -> 'T'
```

## HoldNftRequest

Публичная операция/свойство SDK. Ниже приведены точные типы, значения по умолчанию и тип результата; контекст использования дан в руководстве раздела.

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

Локально получить технический ключ подписи; поля запроса передаются именованными аргументами.

```python
from_mnemonic(*, mnemonic: 'str', passphrase: 'str' = '', account_path: 'str' = "m/44'/60'/0'/0/0", account_index: 'int | None' = None, **kwargs) -> 'T'
```

## TransferNftStakeRequest

Публичная операция/свойство SDK. Ниже приведены точные типы, значения по умолчанию и тип результата; контекст использования дан в руководстве раздела.

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

Локально получить технический ключ подписи; поля запроса передаются именованными аргументами.

```python
from_mnemonic(*, mnemonic: 'str', passphrase: 'str' = '', account_path: 'str' = "m/44'/60'/0'/0/0", account_index: 'int | None' = None, **kwargs) -> 'T'
```

## WithdrawNftRequest

Публичная операция/свойство SDK. Ниже приведены точные типы, значения по умолчанию и тип результата; контекст использования дан в руководстве раздела.

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

Локально получить технический ключ подписи; поля запроса передаются именованными аргументами.

```python
from_mnemonic(*, mnemonic: 'str', passphrase: 'str' = '', account_path: 'str' = "m/44'/60'/0'/0/0", account_index: 'int | None' = None, **kwargs) -> 'T'
```

## NftService

Публичная операция/свойство SDK. Ниже приведены точные типы, значения по умолчанию и тип результата; контекст использования дан в руководстве раздела.

### add_del_reserve

Публичная операция/свойство SDK. Ниже приведены точные типы, значения по умолчанию и тип результата; контекст использования дан в руководстве раздела.

```python
async add_del_reserve(self, request: 'AddDelReserveNftRequest', broadcast: 'bool' = False, wait_receipt: 'bool' = False) -> 'TransactionResult'
```

### approve

Публичная операция/свойство SDK. Ниже приведены точные типы, значения по умолчанию и тип результата; контекст использования дан в руководстве раздела.

```python
async approve(self, request: 'NftApproveRequest', broadcast: 'bool' = False, wait_receipt: 'bool' = False) -> 'TransactionResult'
```

### balance_of

Публичная операция/свойство SDK. Ниже приведены точные типы, значения по умолчанию и тип результата; контекст использования дан в руководстве раздела.

```python
async balance_of(self, nft: 'str', owner: 'str', token_id: 'int | None' = None, kind: 'NftKind' = 'erc721') -> 'int'
```

### burn

Публичная операция/свойство SDK. Ниже приведены точные типы, значения по умолчанию и тип результата; контекст использования дан в руководстве раздела.

```python
async burn(self, request: 'BurnNftRequest', broadcast: 'bool' = False, wait_receipt: 'bool' = False) -> 'TransactionResult'
```

### create_collection

Публичная операция/свойство SDK. Ниже приведены точные типы, значения по умолчанию и тип результата; контекст использования дан в руководстве раздела.

```python
async create_collection(self, request: 'CreateNftCollectionRequest', broadcast: 'bool' = False, wait_receipt: 'bool' = False) -> 'TransactionResult'
```

### delegate

Публичная операция/свойство SDK. Ниже приведены точные типы, значения по умолчанию и тип результата; контекст использования дан в руководстве раздела.

```python
async delegate(self, request: 'DelegateNftRequest', broadcast: 'bool' = False, wait_receipt: 'bool' = False) -> 'DecimalWorkflowResult'
```

### disable_mint

Публичная операция/свойство SDK. Ниже приведены точные типы, значения по умолчанию и тип результата; контекст использования дан в руководстве раздела.

```python
async disable_mint(self, request: 'DisableMintNftRequest', broadcast: 'bool' = False, wait_receipt: 'bool' = False) -> 'TransactionResult'
```

### hold

Публичная операция/свойство SDK. Ниже приведены точные типы, значения по умолчанию и тип результата; контекст использования дан в руководстве раздела.

```python
async hold(self, request: 'HoldNftRequest', broadcast: 'bool' = False, wait_receipt: 'bool' = False) -> 'DecimalWorkflowResult'
```

### is_approved_for_all

Публичная операция/свойство SDK. Ниже приведены точные типы, значения по умолчанию и тип результата; контекст использования дан в руководстве раздела.

```python
async is_approved_for_all(self, kind: 'NftKind', nft: 'str', owner: 'str', operator: 'str') -> 'bool'
```

### mint

Публичная операция/свойство SDK. Ниже приведены точные типы, значения по умолчанию и тип результата; контекст использования дан в руководстве раздела.

```python
async mint(self, request: 'MintNftRequest', broadcast: 'bool' = False, wait_receipt: 'bool' = False) -> 'TransactionResult'
```

### owner_of

Публичная операция/свойство SDK. Ниже приведены точные типы, значения по умолчанию и тип результата; контекст использования дан в руководстве раздела.

```python
async owner_of(self, nft: 'str', token_id: 'int') -> 'str'
```

### set_approval_for_all

Публичная операция/свойство SDK. Ниже приведены точные типы, значения по умолчанию и тип результата; контекст использования дан в руководстве раздела.

```python
async set_approval_for_all(self, request: 'NftApprovalRequest', broadcast: 'bool' = False, wait_receipt: 'bool' = False) -> 'TransactionResult'
```

### set_token_uri

Публичная операция/свойство SDK. Ниже приведены точные типы, значения по умолчанию и тип результата; контекст использования дан в руководстве раздела.

```python
async set_token_uri(self, request: 'SetTokenUriNftRequest', broadcast: 'bool' = False, wait_receipt: 'bool' = False) -> 'TransactionResult'
```

### transfer

Публичная операция/свойство SDK. Ниже приведены точные типы, значения по умолчанию и тип результата; контекст использования дан в руководстве раздела.

```python
async transfer(self, request: 'NftTransferRequest', broadcast: 'bool' = False, wait_receipt: 'bool' = False) -> 'TransactionResult'
```

### transfer_batch_erc1155

Публичная операция/свойство SDK. Ниже приведены точные типы, значения по умолчанию и тип результата; контекст использования дан в руководстве раздела.

```python
async transfer_batch_erc1155(self, request: 'NftBatchTransferRequest', broadcast: 'bool' = False, wait_receipt: 'bool' = False) -> 'TransactionResult'
```

### transfer_stake

Публичная операция/свойство SDK. Ниже приведены точные типы, значения по умолчанию и тип результата; контекст использования дан в руководстве раздела.

```python
async transfer_stake(self, request: 'TransferNftStakeRequest', broadcast: 'bool' = False, wait_receipt: 'bool' = False) -> 'TransactionResult'
```

### withdraw

Публичная операция/свойство SDK. Ниже приведены точные типы, значения по умолчанию и тип результата; контекст использования дан в руководстве раздела.

```python
async withdraw(self, request: 'WithdrawNftRequest', broadcast: 'bool' = False, wait_receipt: 'bool' = False) -> 'TransactionResult'
```
