# rest

[Index](../api.md)

Signatures are generated from the release source. Required fields have no default.

## Page

Page; types, defaults and return value are specified below.

```python
Page(limit: 'int' = 50, offset: 'int' = 0, order: 'str' = 'desc') -> None
```

- `limit`: `int`; 50.
- `offset`: `int`; 0.
- `order`: `str`; 'desc'.

### params

Params; types, defaults and return value are specified below.

```python
params(self, max_limit: 'int' = 100) -> 'dict[str, Any]'
```

## WalletStakeHold

Walletstakehold; types, defaults and return value are specified below.

```python
WalletStakeHold(amount: 'Decimal', amount_raw: 'str', hold_start_time: 'int | None' = None, hold_end_time: 'int | None' = None, is_active: 'bool' = False, is_expired: 'bool' = False, raw: 'dict[str, Any] | None' = None) -> None
```

- `amount`: `Decimal`; required.
- `amount_raw`: `str`; required.
- `hold_start_time`: `int | None`; None.
- `hold_end_time`: `int | None`; None.
- `is_active`: `bool`; False.
- `is_expired`: `bool`; False.
- `raw`: `dict[str, Any] | None`; None.

### contract_hold_timestamp

Contract hold timestamp; types, defaults and return value are specified below.

```python
contract_hold_timestamp: int | None
```

## WalletStakePosition

Walletstakeposition; types, defaults and return value are specified below.

```python
WalletStakePosition(validator: 'str', validator_name: 'str', symbol: 'str', amount: 'Decimal', amount_raw: 'str', base_amount_del: 'Decimal', base_amount_raw: 'str', is_hold: 'bool' = False, is_native: 'bool' = False, stake_type: 'str | None' = None, token_address: 'str | None' = None, token: 'dict[str, Any] | None' = None, hold_amount: 'Decimal' = Decimal('0'), unlocked_amount: 'Decimal' = Decimal('0'), holds: 'tuple[WalletStakeHold, ...]' = (), raw: 'dict[str, Any] | None' = None) -> None
```

- `validator`: `str`; required.
- `validator_name`: `str`; required.
- `symbol`: `str`; required.
- `amount`: `Decimal`; required.
- `amount_raw`: `str`; required.
- `base_amount_del`: `Decimal`; required.
- `base_amount_raw`: `str`; required.
- `is_hold`: `bool`; False.
- `is_native`: `bool`; False.
- `stake_type`: `str | None`; None.
- `token_address`: `str | None`; None.
- `token`: `dict[str, Any] | None`; None.
- `hold_amount`: `Decimal`; Decimal('0').
- `unlocked_amount`: `Decimal`; Decimal('0').
- `holds`: `tuple[WalletStakeHold, ...]`; ().
- `raw`: `dict[str, Any] | None`; None.

### api_unlocked_delta

Api unlocked delta; types, defaults and return value are specified below.

```python
api_unlocked_delta: Decimal
```

### available_base_amount_del

Available base amount del; types, defaults and return value are specified below.

```python
available_base_amount_del: Decimal
```

### available_to_unbond

Available to unbond; types, defaults and return value are specified below.

```python
available_to_unbond: Decimal
```

### can_unbond

Can unbond; types, defaults and return value are specified below.

```python
can_unbond: bool
```

### can_withdraw_hold

Can withdraw hold; types, defaults and return value are specified below.

```python
can_withdraw_hold: bool
```

### held_amount

Held amount; types, defaults and return value are specified below.

```python
held_amount: Decimal
```

### held_base_amount_del

Held base amount del; types, defaults and return value are specified below.

```python
held_base_amount_del: Decimal
```

### matured_hold_amount

Matured hold amount; types, defaults and return value are specified below.

```python
matured_hold_amount: Decimal
```

## WalletUnstakePosition

Walletunstakeposition; types, defaults and return value are specified below.

```python
WalletUnstakePosition(validator: 'str', validator_name: 'str', symbol: 'str', amount: 'Decimal', amount_raw: 'str', completion_time: 'str | None' = None, unfreeze_timestamp: 'int | None' = None, raw: 'dict[str, Any] | None' = None) -> None
```

- `validator`: `str`; required.
- `validator_name`: `str`; required.
- `symbol`: `str`; required.
- `amount`: `Decimal`; required.
- `amount_raw`: `str`; required.
- `completion_time`: `str | None`; None.
- `unfreeze_timestamp`: `int | None`; None.
- `raw`: `dict[str, Any] | None`; None.

## WalletStakeWithdrawal

Walletstakewithdrawal; types, defaults and return value are specified below.

```python
WalletStakeWithdrawal(validator: 'str', validator_name: 'str', symbol: 'str', amount: 'Decimal', amount_raw: 'str | None', available_timestamp: 'int | None' = None, available_time: 'str | None' = None, tx_hash: 'str | None' = None, block: 'int | None' = None, created_timestamp: 'int | None' = None, source: 'str' = 'api', is_completed: 'bool' = False, raw: 'dict[str, Any] | None' = None, is_matured: 'bool' = False, completion_estimated: 'bool' = False) -> None
```

- `validator`: `str`; required.
- `validator_name`: `str`; required.
- `symbol`: `str`; required.
- `amount`: `Decimal`; required.
- `amount_raw`: `str | None`; required.
- `available_timestamp`: `int | None`; None.
- `available_time`: `str | None`; None.
- `tx_hash`: `str | None`; None.
- `block`: `int | None`; None.
- `created_timestamp`: `int | None`; None.
- `source`: `str`; 'api'.
- `is_completed`: `bool`; False.
- `raw`: `dict[str, Any] | None`; None.
- `is_matured`: `bool`; False.
- `completion_estimated`: `bool`; False.

## WalletStakingSummary

Walletstakingsummary; types, defaults and return value are specified below.

```python
WalletStakingSummary(address: 'str', total_del: 'Decimal', coin_total_del: 'Decimal', nft_hold_total_del: 'Decimal', positions: 'tuple[WalletStakePosition, ...]', unstakes: 'tuple[WalletUnstakePosition, ...]' = (), raw_stakes: 'dict[str, Any] | None' = None, raw_unstakes: 'dict[str, Any] | None' = None) -> None
```

- `address`: `str`; required.
- `total_del`: `Decimal`; required.
- `coin_total_del`: `Decimal`; required.
- `nft_hold_total_del`: `Decimal`; required.
- `positions`: `tuple[WalletStakePosition, ...]`; required.
- `unstakes`: `tuple[WalletUnstakePosition, ...]`; ().
- `raw_stakes`: `dict[str, Any] | None`; None.
- `raw_unstakes`: `dict[str, Any] | None`; None.

### available_positions

Available positions; types, defaults and return value are specified below.

```python
available_positions: tuple[WalletStakePosition, ...]
```

### available_to_unbond_by_symbol

Available to unbond by symbol; types, defaults and return value are specified below.

```python
available_to_unbond_by_symbol: dict[str, Decimal]
```

### delegated_by_symbol

Delegated by symbol; types, defaults and return value are specified below.

```python
delegated_by_symbol: dict[str, Decimal]
```

### held_by_symbol

Held by symbol; types, defaults and return value are specified below.

```python
held_by_symbol: dict[str, Decimal]
```

### held_positions

Held positions; types, defaults and return value are specified below.

```python
held_positions: tuple[WalletStakePosition, ...]
```

## normalize_wallet_staking_summary

Normalize wallet staking summary; types, defaults and return value are specified below.

```python
normalize_wallet_staking_summary(address: 'str', stakes_payload: 'dict[str, Any]', unstakes_payload: 'dict[str, Any] | None' = None, coins_payload: 'dict[str, Any] | None' = None) -> 'WalletStakingSummary'
```

## normalize_wallet_stake_withdrawals

Normalize wallet stake withdrawals; types, defaults and return value are specified below.

```python
normalize_wallet_stake_withdrawals(address: 'str', *, unstakes_payload: 'dict[str, Any] | None' = None, txs_payload: 'dict[str, Any] | None' = None, tx_payloads: 'list[dict[str, Any] | None] | None' = None, include_completed: 'bool' = False, recent_days: 'int | None' = None, unbonding_days: 'int' = 15, now_timestamp: 'int | None' = None) -> 'tuple[WalletStakeWithdrawal, ...]'
```

## RestClient

Restclient; types, defaults and return value are specified below.

### address

Address; types, defaults and return value are specified below.

```python
async address(self, address: 'str') -> 'dict[str, Any]'
```

### address_full

Address full; types, defaults and return value are specified below.

```python
async address_full(self, address: 'str', with_erc20: 'bool' = True, symbols: 'str | None' = None) -> 'dict[str, Any]'
```

### address_txs

Address txs; types, defaults and return value are specified below.

```python
async address_txs(self, address: 'str', page: 'Page | None' = None) -> 'dict[str, Any]'
```

### block

Block; types, defaults and return value are specified below.

```python
async block(self, height: 'int') -> 'dict[str, Any]'
```

### block_txs

Block txs; types, defaults and return value are specified below.

```python
async block_txs(self, height: 'int', page: 'Page | None' = None) -> 'dict[str, Any]'
```

### coin

Coin; types, defaults and return value are specified below.

```python
async coin(self, denom: 'str') -> 'dict[str, Any]'
```

### coin_prices

Coin prices; types, defaults and return value are specified below.

```python
async coin_prices(self) -> 'dict[str, Any]'
```

### coin_registry

Coin registry; types, defaults and return value are specified below.

```python
async coin_registry(self, with_price: 'bool' = False, limit: 'int' = 500) -> 'dict[str, Any]'
```

### coin_registry_for_symbols

Coin registry for symbols; types, defaults and return value are specified below.

```python
async coin_registry_for_symbols(self, symbols: 'list[str]', with_price: 'bool' = False) -> 'dict[str, Any]'
```

### coins

Coins; types, defaults and return value are specified below.

```python
async coins(self, with_price: 'bool' = False, limit: 'int' = 100) -> 'dict[str, Any]'
```

### health

Health; types, defaults and return value are specified below.

```python
async health(self) -> 'dict[str, Any]'
```

### latest_block

Latest block; types, defaults and return value are specified below.

```python
async latest_block(self) -> 'dict[str, Any]'
```

### rewards_delegator

Rewards delegator; types, defaults and return value are specified below.

```python
async rewards_delegator(self, delegator: 'str') -> 'dict[str, Any]'
```

### tx

Tx; types, defaults and return value are specified below.

```python
async tx(self, tx_hash: 'str') -> 'dict[str, Any]'
```

### txs

Txs; types, defaults and return value are specified below.

```python
async txs(self, page: 'Page | None' = None, **filters: 'Any') -> 'dict[str, Any]'
```

### validator

Validator; types, defaults and return value are specified below.

```python
async validator(self, validator: 'str') -> 'dict[str, Any]'
```

### validator_delegations

Validator delegations; types, defaults and return value are specified below.

```python
async validator_delegations(self, validator: 'str') -> 'dict[str, Any]'
```

### validators

Validators; types, defaults and return value are specified below.

```python
async validators(self) -> 'dict[str, Any]'
```

### wallet_balances

Wallet balances; types, defaults and return value are specified below.

```python
async wallet_balances(self, address: 'str', limit: 'int' = 300, offset: 'int' = 0, include_bank: 'bool' = True, prefer_bank: 'bool' = True) -> 'dict[str, Any]'
```

### wallet_stake_transfers

Wallet stake transfers; types, defaults and return value are specified below.

```python
async wallet_stake_transfers(self, address: 'str') -> 'dict[str, Any]'
```

### wallet_stake_withdrawals

Wallet stake withdrawals; types, defaults and return value are specified below.

```python
async wallet_stake_withdrawals(self, address: 'str', *, page: 'Page | None' = None, include_completed: 'bool' = False, recent_days: 'int | None' = None, tx_hashes: 'list[str] | None' = None, unbonding_days: 'int' = 15) -> 'tuple[WalletStakeWithdrawal, ...]'
```

### wallet_stakes

Wallet stakes; types, defaults and return value are specified below.

```python
async wallet_stakes(self, address: 'str') -> 'dict[str, Any]'
```

### wallet_staking_summary

Wallet staking summary; types, defaults and return value are specified below.

```python
async wallet_staking_summary(self, address: 'str', *, include_unstakes: 'bool' = True, enrich_tokens: 'bool' = True, coin_lookup_limit: 'int' = 500) -> 'WalletStakingSummary'
```

### wallet_unstakes

Wallet unstakes; types, defaults and return value are specified below.

```python
async wallet_unstakes(self, address: 'str') -> 'dict[str, Any]'
```
