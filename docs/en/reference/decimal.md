# decimal

[Index](../api.md)

Signatures are generated from the release source. Required fields have no default.

## DelegateDelRequest

Delegatedelrequest; types, defaults and return value are specified below.

```python
DelegateDelRequest(validator: 'str', amount_del: 'Decimal | str | int', private_key: 'str') -> None
```

- `validator`: `str`; required.
- `amount_del`: `Decimal | str | int`; required.
- `private_key`: `str`; use from_mnemonic; technical field, hidden in repr.

### from_mnemonic

Derive the technical signing key locally; pass request fields as keyword arguments.

```python
from_mnemonic(*, mnemonic: 'str', passphrase: 'str' = '', account_path: 'str' = "m/44'/60'/0'/0/0", account_index: 'int | None' = None, **kwargs) -> 'T'
```

## HoldDelRequest

Holddelrequest; types, defaults and return value are specified below.

```python
HoldDelRequest(validator: 'str', amount_del: 'Decimal | str | int', hold_timestamp: 'int', private_key: 'str') -> None
```

- `validator`: `str`; required.
- `amount_del`: `Decimal | str | int`; required.
- `hold_timestamp`: `int`; required.
- `private_key`: `str`; use from_mnemonic; technical field, hidden in repr.

### from_mnemonic

Derive the technical signing key locally; pass request fields as keyword arguments.

```python
from_mnemonic(*, mnemonic: 'str', passphrase: 'str' = '', account_path: 'str' = "m/44'/60'/0'/0/0", account_index: 'int | None' = None, **kwargs) -> 'T'
```

## UnbondDelRequest

Unbonddelrequest; types, defaults and return value are specified below.

```python
UnbondDelRequest(validator: 'str', amount_del: 'Decimal | str | int', private_key: 'str') -> None
```

- `validator`: `str`; required.
- `amount_del`: `Decimal | str | int`; required.
- `private_key`: `str`; use from_mnemonic; technical field, hidden in repr.

### from_mnemonic

Derive the technical signing key locally; pass request fields as keyword arguments.

```python
from_mnemonic(*, mnemonic: 'str', passphrase: 'str' = '', account_path: 'str' = "m/44'/60'/0'/0/0", account_index: 'int | None' = None, **kwargs) -> 'T'
```

## WithdrawHoldDelRequest

Withdrawholddelrequest; types, defaults and return value are specified below.

```python
WithdrawHoldDelRequest(validator: 'str', amount_del: 'Decimal | str | int', hold_timestamp: 'int', private_key: 'str') -> None
```

- `validator`: `str`; required.
- `amount_del`: `Decimal | str | int`; required.
- `hold_timestamp`: `int`; required.
- `private_key`: `str`; use from_mnemonic; technical field, hidden in repr.

### from_mnemonic

Derive the technical signing key locally; pass request fields as keyword arguments.

```python
from_mnemonic(*, mnemonic: 'str', passphrase: 'str' = '', account_path: 'str' = "m/44'/60'/0'/0/0", account_index: 'int | None' = None, **kwargs) -> 'T'
```

## MultisendRecipient

Multisendrecipient; types, defaults and return value are specified below.

```python
MultisendRecipient(to: 'str', amount_del: 'Decimal | str | int') -> None
```

- `to`: `str`; required.
- `amount_del`: `Decimal | str | int`; required.

## MultisendDelRequest

Multisenddelrequest; types, defaults and return value are specified below.

```python
MultisendDelRequest(recipients: 'list[MultisendRecipient]', private_key: 'str', memo: 'str | None' = None) -> None
```

- `recipients`: `list[MultisendRecipient]`; required.
- `private_key`: `str`; use from_mnemonic; technical field, hidden in repr.
- `memo`: `str | None`; None.

### from_mnemonic

Derive the technical signing key locally; pass request fields as keyword arguments.

```python
from_mnemonic(*, mnemonic: 'str', passphrase: 'str' = '', account_path: 'str' = "m/44'/60'/0'/0/0", account_index: 'int | None' = None, **kwargs) -> 'T'
```

## MultisendErc20Recipient

Multisenderc20recipient; types, defaults and return value are specified below.

```python
MultisendErc20Recipient(to: 'str', amount: 'Decimal | str | int') -> None
```

- `to`: `str`; required.
- `amount`: `Decimal | str | int`; required.

## MultisendErc20Request

Multisenderc20request; types, defaults and return value are specified below.

```python
MultisendErc20Request(token: 'str', recipients: 'list[MultisendErc20Recipient]', private_key: 'str', decimals: 'int | None' = None, memo: 'str | None' = None, auto_approve: 'bool' = True, prefer_permit: 'bool' = True, permit_deadline: 'int' = 115792089237316195423570985008687907853269984665640564039457584007913129639935) -> None
```

- `token`: `str`; required.
- `recipients`: `list[MultisendErc20Recipient]`; required.
- `private_key`: `str`; use from_mnemonic; technical field, hidden in repr.
- `decimals`: `int | None`; None.
- `memo`: `str | None`; None.
- `auto_approve`: `bool`; True.
- `prefer_permit`: `bool`; True.
- `permit_deadline`: `int`; 115792089237316195423570985008687907853269984665640564039457584007913129639935.

### from_mnemonic

Derive the technical signing key locally; pass request fields as keyword arguments.

```python
from_mnemonic(*, mnemonic: 'str', passphrase: 'str' = '', account_path: 'str' = "m/44'/60'/0'/0/0", account_index: 'int | None' = None, **kwargs) -> 'T'
```

## DelegateErc20Request

Delegateerc20request; types, defaults and return value are specified below.

```python
DelegateErc20Request(token: 'str', validator: 'str', amount: 'Decimal | str | int', private_key: 'str', decimals: 'int | None' = None, auto_approve: 'bool' = True, prefer_permit: 'bool' = True, permit_deadline: 'int' = 115792089237316195423570985008687907853269984665640564039457584007913129639935) -> None
```

- `token`: `str`; required.
- `validator`: `str`; required.
- `amount`: `Decimal | str | int`; required.
- `private_key`: `str`; use from_mnemonic; technical field, hidden in repr.
- `decimals`: `int | None`; None.
- `auto_approve`: `bool`; True.
- `prefer_permit`: `bool`; True.
- `permit_deadline`: `int`; 115792089237316195423570985008687907853269984665640564039457584007913129639935.

### from_mnemonic

Derive the technical signing key locally; pass request fields as keyword arguments.

```python
from_mnemonic(*, mnemonic: 'str', passphrase: 'str' = '', account_path: 'str' = "m/44'/60'/0'/0/0", account_index: 'int | None' = None, **kwargs) -> 'T'
```

## HoldErc20Request

Holderc20request; types, defaults and return value are specified below.

```python
HoldErc20Request(token: 'str', validator: 'str', amount: 'Decimal | str | int', hold_timestamp: 'int', private_key: 'str', decimals: 'int | None' = None, auto_approve: 'bool' = True, prefer_permit: 'bool' = True, permit_deadline: 'int' = 115792089237316195423570985008687907853269984665640564039457584007913129639935) -> None
```

- `token`: `str`; required.
- `validator`: `str`; required.
- `amount`: `Decimal | str | int`; required.
- `hold_timestamp`: `int`; required.
- `private_key`: `str`; use from_mnemonic; technical field, hidden in repr.
- `decimals`: `int | None`; None.
- `auto_approve`: `bool`; True.
- `prefer_permit`: `bool`; True.
- `permit_deadline`: `int`; 115792089237316195423570985008687907853269984665640564039457584007913129639935.

### from_mnemonic

Derive the technical signing key locally; pass request fields as keyword arguments.

```python
from_mnemonic(*, mnemonic: 'str', passphrase: 'str' = '', account_path: 'str' = "m/44'/60'/0'/0/0", account_index: 'int | None' = None, **kwargs) -> 'T'
```

## UnbondErc20Request

Unbonderc20request; types, defaults and return value are specified below.

```python
UnbondErc20Request(token: 'str', validator: 'str', amount: 'Decimal | str | int', private_key: 'str', decimals: 'int | None' = None) -> None
```

- `token`: `str`; required.
- `validator`: `str`; required.
- `amount`: `Decimal | str | int`; required.
- `private_key`: `str`; use from_mnemonic; technical field, hidden in repr.
- `decimals`: `int | None`; None.

### from_mnemonic

Derive the technical signing key locally; pass request fields as keyword arguments.

```python
from_mnemonic(*, mnemonic: 'str', passphrase: 'str' = '', account_path: 'str' = "m/44'/60'/0'/0/0", account_index: 'int | None' = None, **kwargs) -> 'T'
```

## WithdrawHoldErc20Request

Withdrawholderc20request; types, defaults and return value are specified below.

```python
WithdrawHoldErc20Request(token: 'str', validator: 'str', amount: 'Decimal | str | int', hold_timestamp: 'int', private_key: 'str', decimals: 'int | None' = None) -> None
```

- `token`: `str`; required.
- `validator`: `str`; required.
- `amount`: `Decimal | str | int`; required.
- `hold_timestamp`: `int`; required.
- `private_key`: `str`; use from_mnemonic; technical field, hidden in repr.
- `decimals`: `int | None`; None.

### from_mnemonic

Derive the technical signing key locally; pass request fields as keyword arguments.

```python
from_mnemonic(*, mnemonic: 'str', passphrase: 'str' = '', account_path: 'str' = "m/44'/60'/0'/0/0", account_index: 'int | None' = None, **kwargs) -> 'T'
```

## TransferStakeErc20Request

Transferstakeerc20request; types, defaults and return value are specified below.

```python
TransferStakeErc20Request(token: 'str', validator: 'str', new_validator: 'str', amount: 'Decimal | str | int', private_key: 'str', decimals: 'int | None' = None, hold_timestamp: 'int | None' = None) -> None
```

- `token`: `str`; required.
- `validator`: `str`; required.
- `new_validator`: `str`; required.
- `amount`: `Decimal | str | int`; required.
- `private_key`: `str`; use from_mnemonic; technical field, hidden in repr.
- `decimals`: `int | None`; None.
- `hold_timestamp`: `int | None`; None.

### from_mnemonic

Derive the technical signing key locally; pass request fields as keyword arguments.

```python
from_mnemonic(*, mnemonic: 'str', passphrase: 'str' = '', account_path: 'str' = "m/44'/60'/0'/0/0", account_index: 'int | None' = None, **kwargs) -> 'T'
```

## TransferStakeDelRequest

Transferstakedelrequest; types, defaults and return value are specified below.

```python
TransferStakeDelRequest(validator: 'str', new_validator: 'str', amount_del: 'Decimal | str | int', private_key: 'str', hold_timestamp: 'int | None' = None) -> None
```

- `validator`: `str`; required.
- `new_validator`: `str`; required.
- `amount_del`: `Decimal | str | int`; required.
- `private_key`: `str`; use from_mnemonic; technical field, hidden in repr.
- `hold_timestamp`: `int | None`; None.

### from_mnemonic

Derive the technical signing key locally; pass request fields as keyword arguments.

```python
from_mnemonic(*, mnemonic: 'str', passphrase: 'str' = '', account_path: 'str' = "m/44'/60'/0'/0/0", account_index: 'int | None' = None, **kwargs) -> 'T'
```

## StakeTokenToHoldRequest

Staketokentoholdrequest; types, defaults and return value are specified below.

```python
StakeTokenToHoldRequest(token: 'str', validator: 'str', amount: 'Decimal | str | int', old_hold_timestamp: 'int', new_hold_timestamp: 'int', private_key: 'str', decimals: 'int | None' = None) -> None
```

- `token`: `str`; required.
- `validator`: `str`; required.
- `amount`: `Decimal | str | int`; required.
- `old_hold_timestamp`: `int`; required.
- `new_hold_timestamp`: `int`; required.
- `private_key`: `str`; use from_mnemonic; technical field, hidden in repr.
- `decimals`: `int | None`; None.

### from_mnemonic

Derive the technical signing key locally; pass request fields as keyword arguments.

```python
from_mnemonic(*, mnemonic: 'str', passphrase: 'str' = '', account_path: 'str' = "m/44'/60'/0'/0/0", account_index: 'int | None' = None, **kwargs) -> 'T'
```

## ResetStakeHoldRequest

Resetstakeholdrequest; types, defaults and return value are specified below.

```python
ResetStakeHoldRequest(validator: 'str', delegator: 'str', private_key: 'str', hold_timestamp: 'int', token: 'str | None' = None) -> None
```

- `validator`: `str`; required.
- `delegator`: `str`; required.
- `private_key`: `str`; use from_mnemonic; technical field, hidden in repr.
- `hold_timestamp`: `int`; required.
- `token`: `str | None`; None.

### from_mnemonic

Derive the technical signing key locally; pass request fields as keyword arguments.

```python
from_mnemonic(*, mnemonic: 'str', passphrase: 'str' = '', account_path: 'str' = "m/44'/60'/0'/0/0", account_index: 'int | None' = None, **kwargs) -> 'T'
```

## WithdrawStakeWithResetRequest

Withdrawstakewithresetrequest; types, defaults and return value are specified below.

```python
WithdrawStakeWithResetRequest(token: 'str', validator: 'str', amount: 'Decimal | str | int', hold_timestamps_to_reset: 'list[int]', private_key: 'str', decimals: 'int | None' = None) -> None
```

- `token`: `str`; required.
- `validator`: `str`; required.
- `amount`: `Decimal | str | int`; required.
- `hold_timestamps_to_reset`: `list[int]`; required.
- `private_key`: `str`; use from_mnemonic; technical field, hidden in repr.
- `decimals`: `int | None`; None.

### from_mnemonic

Derive the technical signing key locally; pass request fields as keyword arguments.

```python
from_mnemonic(*, mnemonic: 'str', passphrase: 'str' = '', account_path: 'str' = "m/44'/60'/0'/0/0", account_index: 'int | None' = None, **kwargs) -> 'T'
```

## WithdrawDelStakeWithResetRequest

Withdrawdelstakewithresetrequest; types, defaults and return value are specified below.

```python
WithdrawDelStakeWithResetRequest(validator: 'str', amount_del: 'Decimal | str | int', hold_timestamps_to_reset: 'list[int]', private_key: 'str') -> None
```

- `validator`: `str`; required.
- `amount_del`: `Decimal | str | int`; required.
- `hold_timestamps_to_reset`: `list[int]`; required.
- `private_key`: `str`; use from_mnemonic; technical field, hidden in repr.

### from_mnemonic

Derive the technical signing key locally; pass request fields as keyword arguments.

```python
from_mnemonic(*, mnemonic: 'str', passphrase: 'str' = '', account_path: 'str' = "m/44'/60'/0'/0/0", account_index: 'int | None' = None, **kwargs) -> 'T'
```

## TransferStakeWithResetRequest

Transferstakewithresetrequest; types, defaults and return value are specified below.

```python
TransferStakeWithResetRequest(token: 'str', old_validator: 'str', new_validator: 'str', amount: 'Decimal | str | int', hold_timestamps_to_reset: 'list[int]', private_key: 'str', decimals: 'int | None' = None) -> None
```

- `token`: `str`; required.
- `old_validator`: `str`; required.
- `new_validator`: `str`; required.
- `amount`: `Decimal | str | int`; required.
- `hold_timestamps_to_reset`: `list[int]`; required.
- `private_key`: `str`; use from_mnemonic; technical field, hidden in repr.
- `decimals`: `int | None`; None.

### from_mnemonic

Derive the technical signing key locally; pass request fields as keyword arguments.

```python
from_mnemonic(*, mnemonic: 'str', passphrase: 'str' = '', account_path: 'str' = "m/44'/60'/0'/0/0", account_index: 'int | None' = None, **kwargs) -> 'T'
```

## TransferDelStakeWithResetRequest

Transferdelstakewithresetrequest; types, defaults and return value are specified below.

```python
TransferDelStakeWithResetRequest(old_validator: 'str', new_validator: 'str', amount_del: 'Decimal | str | int', hold_timestamps_to_reset: 'list[int]', private_key: 'str') -> None
```

- `old_validator`: `str`; required.
- `new_validator`: `str`; required.
- `amount_del`: `Decimal | str | int`; required.
- `hold_timestamps_to_reset`: `list[int]`; required.
- `private_key`: `str`; use from_mnemonic; technical field, hidden in repr.

### from_mnemonic

Derive the technical signing key locally; pass request fields as keyword arguments.

```python
from_mnemonic(*, mnemonic: 'str', passphrase: 'str' = '', account_path: 'str' = "m/44'/60'/0'/0/0", account_index: 'int | None' = None, **kwargs) -> 'T'
```

## HoldStakeWithResetRequest

Holdstakewithresetrequest; types, defaults and return value are specified below.

```python
HoldStakeWithResetRequest(token: 'str', validator: 'str', amount: 'Decimal | str | int', new_hold_timestamp: 'int', hold_timestamps_to_reset: 'list[int]', private_key: 'str', decimals: 'int | None' = None) -> None
```

- `token`: `str`; required.
- `validator`: `str`; required.
- `amount`: `Decimal | str | int`; required.
- `new_hold_timestamp`: `int`; required.
- `hold_timestamps_to_reset`: `list[int]`; required.
- `private_key`: `str`; use from_mnemonic; technical field, hidden in repr.
- `decimals`: `int | None`; None.

### from_mnemonic

Derive the technical signing key locally; pass request fields as keyword arguments.

```python
from_mnemonic(*, mnemonic: 'str', passphrase: 'str' = '', account_path: 'str' = "m/44'/60'/0'/0/0", account_index: 'int | None' = None, **kwargs) -> 'T'
```

## ValidatorSelfPauseRequest

Validatorselfpauserequest; types, defaults and return value are specified below.

```python
ValidatorSelfPauseRequest(private_key: 'str') -> None
```

- `private_key`: `str`; use from_mnemonic; technical field, hidden in repr.

### from_mnemonic

Derive the technical signing key locally; pass request fields as keyword arguments.

```python
from_mnemonic(*, mnemonic: 'str', passphrase: 'str' = '', account_path: 'str' = "m/44'/60'/0'/0/0", account_index: 'int | None' = None, **kwargs) -> 'T'
```

## ValidatorPauseRequest

Validatorpauserequest; types, defaults and return value are specified below.

```python
ValidatorPauseRequest(validator: 'str', private_key: 'str') -> None
```

- `validator`: `str`; required.
- `private_key`: `str`; use from_mnemonic; technical field, hidden in repr.

### from_mnemonic

Derive the technical signing key locally; pass request fields as keyword arguments.

```python
from_mnemonic(*, mnemonic: 'str', passphrase: 'str' = '', account_path: 'str' = "m/44'/60'/0'/0/0", account_index: 'int | None' = None, **kwargs) -> 'T'
```

## DelegationTokenType

Delegationtokentype; types, defaults and return value are specified below.

## DelegationStake

Delegationstake; types, defaults and return value are specified below.

```python
DelegationStake(validator: 'str', delegator: 'str', token: 'str', amount_raw: 'int', token_id: 'int', token_type: 'int', hold_timestamp: 'int', block_number: 'int | None' = None) -> None
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
amount(self, decimals: 'int' = 18) -> 'Decimal'
```

### amount_string

Amount string; types, defaults and return value are specified below.

```python
amount_string(self, decimals: 'int' = 18) -> 'str'
```

### as_dict

As dict; types, defaults and return value are specified below.

```python
as_dict(self, decimals: 'int' = 18) -> 'dict[str, object]'
```

### exists

Exists; types, defaults and return value are specified below.

```python
exists: bool
```

### hold_time

Hold time; types, defaults and return value are specified below.

```python
hold_time: str | None
```

### is_hold

Is hold; types, defaults and return value are specified below.

```python
is_hold: bool
```

### is_matured

Is matured; types, defaults and return value are specified below.

```python
is_matured(self, now_timestamp: 'int | None' = None) -> 'bool'
```

### is_native_del

Is native del; types, defaults and return value are specified below.

```python
is_native_del: bool
```

### token_type_enum

Token type enum; types, defaults and return value are specified below.

```python
token_type_enum: DelegationTokenType
```

## DelegationStakeSnapshot

Delegationstakesnapshot; types, defaults and return value are specified below.

```python
DelegationStakeSnapshot(block_number: 'int', regular: 'DelegationStake', holds: 'tuple[DelegationStake, ...]' = (), missing_hold_timestamps: 'tuple[int, ...]' = ()) -> None
```

- `block_number`: `int`; required.
- `regular`: `DelegationStake`; required.
- `holds`: `tuple[DelegationStake, ...]`; ().
- `missing_hold_timestamps`: `tuple[int, ...]`; ().

### as_dict

As dict; types, defaults and return value are specified below.

```python
as_dict(self, decimals: 'int' = 18) -> 'dict[str, object]'
```

### held_amount

Held amount; types, defaults and return value are specified below.

```python
held_amount(self, decimals: 'int' = 18) -> 'Decimal'
```

### held_amount_raw

Held amount raw; types, defaults and return value are specified below.

```python
held_amount_raw: int
```

### matured_holds

Matured holds; types, defaults and return value are specified below.

```python
matured_holds(self, now_timestamp: 'int | None' = None) -> 'tuple[DelegationStake, ...]'
```

### regular_amount

Regular amount; types, defaults and return value are specified below.

```python
regular_amount(self, decimals: 'int' = 18) -> 'Decimal'
```

### regular_amount_raw

Regular amount raw; types, defaults and return value are specified below.

```python
regular_amount_raw: int
```

### total_amount

Total amount; types, defaults and return value are specified below.

```python
total_amount(self, decimals: 'int' = 18) -> 'Decimal'
```

### total_amount_raw

Total amount raw; types, defaults and return value are specified below.

```python
total_amount_raw: int
```

## DecimalWorkflowResult

Decimalworkflowresult; types, defaults and return value are specified below.

```python
DecimalWorkflowResult(success: 'bool', name: 'str', steps: 'tuple[str, ...]', expected_steps: 'int', actual_steps: 'int', extra_steps_required: 'bool', primary: 'TransactionResult | None' = None, secondary: 'TransactionResult | None' = None, error: 'str | None' = None, user_message: 'str | None' = None) -> None
```

- `success`: `bool`; required.
- `name`: `str`; required.
- `steps`: `tuple[str, ...]`; required.
- `expected_steps`: `int`; required.
- `actual_steps`: `int`; required.
- `extra_steps_required`: `bool`; required.
- `primary`: `TransactionResult | None`; None.
- `secondary`: `TransactionResult | None`; None.
- `error`: `str | None`; None.
- `user_message`: `str | None`; None.

### fee_del

Fee del; types, defaults and return value are specified below.

```python
fee_del: Decimal | None
```

### fee_wei

Fee wei; types, defaults and return value are specified below.

```python
fee_wei: int | None
```

### gas

Gas; types, defaults and return value are specified below.

```python
gas: int | None
```

### hold_time

Hold time; types, defaults and return value are specified below.

```python
hold_time: str | None
```

### hold_timestamp

Hold timestamp; types, defaults and return value are specified below.

```python
hold_timestamp: int | None
```

### one_transaction

One transaction; types, defaults and return value are specified below.

```python
one_transaction: bool
```

### requires_secondary_transaction

Requires secondary transaction; types, defaults and return value are specified below.

```python
requires_secondary_transaction: bool
```

### total_fee_del

Total fee del; types, defaults and return value are specified below.

```python
total_fee_del: Decimal | None
```

### total_fee_wei

Total fee wei; types, defaults and return value are specified below.

```python
total_fee_wei: int | None
```

### transaction_count

Transaction count; types, defaults and return value are specified below.

```python
transaction_count: int
```

### tx_hash

Tx hash; types, defaults and return value are specified below.

```python
tx_hash: str | None
```

## DecimalService

Decimalservice; types, defaults and return value are specified below.

### build_multisend_del

Build transaction data/draft without broadcasting. See units and ABI constraints in the module guide.

```python
async build_multisend_del(self, request: 'MultisendDelRequest') -> 'TransactionDraft'
```

### delegate_del

Delegate del; types, defaults and return value are specified below.

```python
async delegate_del(self, request: 'DelegateDelRequest', broadcast: 'bool' = False, wait_receipt: 'bool' = False) -> 'TransactionResult'
```

### delegate_erc20

Delegate erc20; types, defaults and return value are specified below.

```python
async delegate_erc20(self, request: 'DelegateErc20Request', broadcast: 'bool' = False, wait_receipt: 'bool' = False) -> 'DecimalWorkflowResult'
```

### estimate_fee_for_delegate_del

Estimate gas and balance requirements without signing; RPC simulation may revert.

```python
async estimate_fee_for_delegate_del(self, request: 'DelegateDelRequest', *, exact: 'bool' = False) -> 'FeePreflight'
```

### estimate_fee_for_hold_del

Estimate gas and balance requirements without signing; RPC simulation may revert.

```python
async estimate_fee_for_hold_del(self, request: 'HoldDelRequest', *, exact: 'bool' = False) -> 'FeePreflight'
```

### estimate_fee_for_multisend_del

Estimate gas and balance requirements without signing; RPC simulation may revert.

```python
async estimate_fee_for_multisend_del(self, request: 'MultisendDelRequest', *, exact: 'bool' = False) -> 'FeePreflight'
```

### estimate_fee_for_transfer_del_stake_with_reset

Estimate gas and balance requirements without signing; RPC simulation may revert.

```python
async estimate_fee_for_transfer_del_stake_with_reset(self, request: 'TransferDelStakeWithResetRequest', *, exact: 'bool' = False) -> 'FeePreflight'
```

### estimate_fee_for_transfer_stake_del

Estimate gas and balance requirements without signing; RPC simulation may revert.

```python
async estimate_fee_for_transfer_stake_del(self, request: 'TransferStakeDelRequest', *, exact: 'bool' = False) -> 'FeePreflight'
```

### estimate_fee_for_transfer_stake_erc20

Estimate gas and balance requirements without signing; RPC simulation may revert.

```python
async estimate_fee_for_transfer_stake_erc20(self, request: 'TransferStakeErc20Request', *, exact: 'bool' = False) -> 'FeePreflight'
```

### estimate_fee_for_transfer_stake_with_reset

Estimate gas and balance requirements without signing; RPC simulation may revert.

```python
async estimate_fee_for_transfer_stake_with_reset(self, request: 'TransferStakeWithResetRequest', *, exact: 'bool' = False) -> 'FeePreflight'
```

### estimate_fee_for_unbond_del

Estimate gas and balance requirements without signing; RPC simulation may revert.

```python
async estimate_fee_for_unbond_del(self, request: 'UnbondDelRequest', *, exact: 'bool' = False) -> 'FeePreflight'
```

### estimate_fee_for_unbond_erc20

Estimate gas and balance requirements without signing; RPC simulation may revert.

```python
async estimate_fee_for_unbond_erc20(self, request: 'UnbondErc20Request', *, exact: 'bool' = False) -> 'FeePreflight'
```

### estimate_fee_for_withdraw_del_stake_with_reset

Estimate gas and balance requirements without signing; RPC simulation may revert.

```python
async estimate_fee_for_withdraw_del_stake_with_reset(self, request: 'WithdrawDelStakeWithResetRequest', *, exact: 'bool' = False) -> 'FeePreflight'
```

### estimate_fee_for_withdraw_hold_del

Estimate gas and balance requirements without signing; RPC simulation may revert.

```python
async estimate_fee_for_withdraw_hold_del(self, request: 'WithdrawHoldDelRequest', *, exact: 'bool' = False) -> 'FeePreflight'
```

### estimate_fee_for_withdraw_hold_erc20

Estimate gas and balance requirements without signing; RPC simulation may revert.

```python
async estimate_fee_for_withdraw_hold_erc20(self, request: 'WithdrawHoldErc20Request', *, exact: 'bool' = False) -> 'FeePreflight'
```

### estimate_fee_for_withdraw_stake_with_reset

Estimate gas and balance requirements without signing; RPC simulation may revert.

```python
async estimate_fee_for_withdraw_stake_with_reset(self, request: 'WithdrawStakeWithResetRequest', *, exact: 'bool' = False) -> 'FeePreflight'
```

### get_hold_stake

Get hold stake; types, defaults and return value are specified below.

```python
async get_hold_stake(self, validator: 'str', delegator: 'str', token: 'str', hold_timestamp: 'int', *, block_identifier: 'int | str | None' = None) -> 'DelegationStake'
```

### get_stake

Get stake; types, defaults and return value are specified below.

```python
async get_stake(self, validator: 'str', delegator: 'str', token: 'str', *, block_identifier: 'int | str | None' = None) -> 'DelegationStake'
```

### get_stake_snapshot

Get stake snapshot; types, defaults and return value are specified below.

```python
async get_stake_snapshot(self, validator: 'str', delegator: 'str', token: 'str', hold_timestamps: 'list[int] | tuple[int, ...]' = (), *, block_number: 'int | None' = None, max_hold_entries: 'int' = 100) -> 'DelegationStakeSnapshot'
```

### hold_del

Hold del; types, defaults and return value are specified below.

```python
async hold_del(self, request: 'HoldDelRequest', broadcast: 'bool' = False, wait_receipt: 'bool' = False) -> 'TransactionResult'
```

### hold_erc20

Hold erc20; types, defaults and return value are specified below.

```python
async hold_erc20(self, request: 'HoldErc20Request', broadcast: 'bool' = False, wait_receipt: 'bool' = False) -> 'DecimalWorkflowResult'
```

### hold_stake_with_reset

Hold stake with reset; types, defaults and return value are specified below.

```python
async hold_stake_with_reset(self, request: 'HoldStakeWithResetRequest', broadcast: 'bool' = False, wait_receipt: 'bool' = False) -> 'DecimalWorkflowResult'
```

### multisend_del

Multisend del; types, defaults and return value are specified below.

```python
async multisend_del(self, request: 'MultisendDelRequest', broadcast: 'bool' = False, wait_receipt: 'bool' = False) -> 'TransactionResult'
```

### multisend_erc20

Multisend erc20; types, defaults and return value are specified below.

```python
async multisend_erc20(self, request: 'MultisendErc20Request', broadcast: 'bool' = False, wait_receipt: 'bool' = False) -> 'DecimalWorkflowResult'
```

### pause_self_validator

Pause self validator; types, defaults and return value are specified below.

```python
async pause_self_validator(self, request: 'ValidatorSelfPauseRequest', broadcast: 'bool' = False, wait_receipt: 'bool' = False) -> 'DecimalWorkflowResult'
```

### pause_validator

Pause validator; types, defaults and return value are specified below.

```python
async pause_validator(self, request: 'ValidatorPauseRequest', broadcast: 'bool' = False, wait_receipt: 'bool' = False) -> 'DecimalWorkflowResult'
```

### reset_stake_hold

Reset stake hold; types, defaults and return value are specified below.

```python
async reset_stake_hold(self, request: 'ResetStakeHoldRequest', broadcast: 'bool' = False, wait_receipt: 'bool' = False) -> 'DecimalWorkflowResult'
```

### stake_token_to_hold

Stake token to hold; types, defaults and return value are specified below.

```python
async stake_token_to_hold(self, request: 'StakeTokenToHoldRequest', broadcast: 'bool' = False, wait_receipt: 'bool' = False) -> 'DecimalWorkflowResult'
```

### transfer_del_stake_with_reset

Transfer del stake with reset; types, defaults and return value are specified below.

```python
async transfer_del_stake_with_reset(self, request: 'TransferDelStakeWithResetRequest', broadcast: 'bool' = False, wait_receipt: 'bool' = False) -> 'DecimalWorkflowResult'
```

### transfer_stake_del

Transfer stake del; types, defaults and return value are specified below.

```python
async transfer_stake_del(self, request: 'TransferStakeDelRequest', broadcast: 'bool' = False, wait_receipt: 'bool' = False) -> 'DecimalWorkflowResult'
```

### transfer_stake_erc20

Transfer stake erc20; types, defaults and return value are specified below.

```python
async transfer_stake_erc20(self, request: 'TransferStakeErc20Request', broadcast: 'bool' = False, wait_receipt: 'bool' = False) -> 'DecimalWorkflowResult'
```

### transfer_stake_with_reset

Transfer stake with reset; types, defaults and return value are specified below.

```python
async transfer_stake_with_reset(self, request: 'TransferStakeWithResetRequest', broadcast: 'bool' = False, wait_receipt: 'bool' = False) -> 'DecimalWorkflowResult'
```

### unbond_del

Unbond del; types, defaults and return value are specified below.

```python
async unbond_del(self, request: 'UnbondDelRequest', broadcast: 'bool' = False, wait_receipt: 'bool' = False) -> 'TransactionResult'
```

### unbond_erc20

Unbond erc20; types, defaults and return value are specified below.

```python
async unbond_erc20(self, request: 'UnbondErc20Request', broadcast: 'bool' = False, wait_receipt: 'bool' = False) -> 'DecimalWorkflowResult'
```

### unpause_self_validator

Unpause self validator; types, defaults and return value are specified below.

```python
async unpause_self_validator(self, request: 'ValidatorSelfPauseRequest', broadcast: 'bool' = False, wait_receipt: 'bool' = False) -> 'DecimalWorkflowResult'
```

### unpause_validator

Unpause validator; types, defaults and return value are specified below.

```python
async unpause_validator(self, request: 'ValidatorPauseRequest', broadcast: 'bool' = False, wait_receipt: 'bool' = False) -> 'DecimalWorkflowResult'
```

### validator_is_active

Validator is active; types, defaults and return value are specified below.

```python
async validator_is_active(self, validator: 'str') -> 'bool'
```

### validator_is_member

Validator is member; types, defaults and return value are specified below.

```python
async validator_is_member(self, validator: 'str') -> 'bool'
```

### validator_status

Validator status; types, defaults and return value are specified below.

```python
async validator_status(self, validator: 'str') -> 'int'
```

### withdraw_del_stake_with_reset

Withdraw del stake with reset; types, defaults and return value are specified below.

```python
async withdraw_del_stake_with_reset(self, request: 'WithdrawDelStakeWithResetRequest', broadcast: 'bool' = False, wait_receipt: 'bool' = False) -> 'DecimalWorkflowResult'
```

### withdraw_hold_del

Withdraw hold del; types, defaults and return value are specified below.

```python
async withdraw_hold_del(self, request: 'WithdrawHoldDelRequest', broadcast: 'bool' = False, wait_receipt: 'bool' = False) -> 'TransactionResult'
```

### withdraw_hold_erc20

Withdraw hold erc20; types, defaults and return value are specified below.

```python
async withdraw_hold_erc20(self, request: 'WithdrawHoldErc20Request', broadcast: 'bool' = False, wait_receipt: 'bool' = False) -> 'DecimalWorkflowResult'
```

### withdraw_stake_with_reset

Withdraw stake with reset; types, defaults and return value are specified below.

```python
async withdraw_stake_with_reset(self, request: 'WithdrawStakeWithResetRequest', broadcast: 'bool' = False, wait_receipt: 'bool' = False) -> 'DecimalWorkflowResult'
```
