# rest

[Index](../api.md)

Сигнатуры сформированы из кода релиза. Обязательные поля не имеют значения по умолчанию.

## Page

Публичная операция/свойство SDK. Ниже приведены точные типы, значения по умолчанию и тип результата; контекст использования дан в руководстве раздела.

```python
Page(limit: 'int' = 50, offset: 'int' = 0, order: 'str' = 'desc') -> None
```

- `limit`: `int`; 50.
- `offset`: `int`; 0.
- `order`: `str`; 'desc'.

### params

Публичная операция/свойство SDK. Ниже приведены точные типы, значения по умолчанию и тип результата; контекст использования дан в руководстве раздела.

```python
params(self, max_limit: 'int' = 100) -> 'dict[str, Any]'
```

## WalletStakeHold

Публичная операция/свойство SDK. Ниже приведены точные типы, значения по умолчанию и тип результата; контекст использования дан в руководстве раздела.

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

Публичная операция/свойство SDK. Ниже приведены точные типы, значения по умолчанию и тип результата; контекст использования дан в руководстве раздела.

```python
contract_hold_timestamp: int | None
```

## WalletStakePosition

Публичная операция/свойство SDK. Ниже приведены точные типы, значения по умолчанию и тип результата; контекст использования дан в руководстве раздела.

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

Публичная операция/свойство SDK. Ниже приведены точные типы, значения по умолчанию и тип результата; контекст использования дан в руководстве раздела.

```python
api_unlocked_delta: Decimal
```

### available_base_amount_del

Публичная операция/свойство SDK. Ниже приведены точные типы, значения по умолчанию и тип результата; контекст использования дан в руководстве раздела.

```python
available_base_amount_del: Decimal
```

### available_to_unbond

Публичная операция/свойство SDK. Ниже приведены точные типы, значения по умолчанию и тип результата; контекст использования дан в руководстве раздела.

```python
available_to_unbond: Decimal
```

### can_unbond

Публичная операция/свойство SDK. Ниже приведены точные типы, значения по умолчанию и тип результата; контекст использования дан в руководстве раздела.

```python
can_unbond: bool
```

### can_withdraw_hold

Публичная операция/свойство SDK. Ниже приведены точные типы, значения по умолчанию и тип результата; контекст использования дан в руководстве раздела.

```python
can_withdraw_hold: bool
```

### held_amount

Публичная операция/свойство SDK. Ниже приведены точные типы, значения по умолчанию и тип результата; контекст использования дан в руководстве раздела.

```python
held_amount: Decimal
```

### held_base_amount_del

Публичная операция/свойство SDK. Ниже приведены точные типы, значения по умолчанию и тип результата; контекст использования дан в руководстве раздела.

```python
held_base_amount_del: Decimal
```

### matured_hold_amount

Публичная операция/свойство SDK. Ниже приведены точные типы, значения по умолчанию и тип результата; контекст использования дан в руководстве раздела.

```python
matured_hold_amount: Decimal
```

## WalletUnstakePosition

Публичная операция/свойство SDK. Ниже приведены точные типы, значения по умолчанию и тип результата; контекст использования дан в руководстве раздела.

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

Публичная операция/свойство SDK. Ниже приведены точные типы, значения по умолчанию и тип результата; контекст использования дан в руководстве раздела.

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

Публичная операция/свойство SDK. Ниже приведены точные типы, значения по умолчанию и тип результата; контекст использования дан в руководстве раздела.

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

Публичная операция/свойство SDK. Ниже приведены точные типы, значения по умолчанию и тип результата; контекст использования дан в руководстве раздела.

```python
available_positions: tuple[WalletStakePosition, ...]
```

### available_to_unbond_by_symbol

Публичная операция/свойство SDK. Ниже приведены точные типы, значения по умолчанию и тип результата; контекст использования дан в руководстве раздела.

```python
available_to_unbond_by_symbol: dict[str, Decimal]
```

### delegated_by_symbol

Публичная операция/свойство SDK. Ниже приведены точные типы, значения по умолчанию и тип результата; контекст использования дан в руководстве раздела.

```python
delegated_by_symbol: dict[str, Decimal]
```

### held_by_symbol

Публичная операция/свойство SDK. Ниже приведены точные типы, значения по умолчанию и тип результата; контекст использования дан в руководстве раздела.

```python
held_by_symbol: dict[str, Decimal]
```

### held_positions

Публичная операция/свойство SDK. Ниже приведены точные типы, значения по умолчанию и тип результата; контекст использования дан в руководстве раздела.

```python
held_positions: tuple[WalletStakePosition, ...]
```

## normalize_wallet_staking_summary

Публичная операция/свойство SDK. Ниже приведены точные типы, значения по умолчанию и тип результата; контекст использования дан в руководстве раздела.

```python
normalize_wallet_staking_summary(address: 'str', stakes_payload: 'dict[str, Any]', unstakes_payload: 'dict[str, Any] | None' = None, coins_payload: 'dict[str, Any] | None' = None) -> 'WalletStakingSummary'
```

## normalize_wallet_stake_withdrawals

Публичная операция/свойство SDK. Ниже приведены точные типы, значения по умолчанию и тип результата; контекст использования дан в руководстве раздела.

```python
normalize_wallet_stake_withdrawals(address: 'str', *, unstakes_payload: 'dict[str, Any] | None' = None, txs_payload: 'dict[str, Any] | None' = None, tx_payloads: 'list[dict[str, Any] | None] | None' = None, include_completed: 'bool' = False, recent_days: 'int | None' = None, unbonding_days: 'int' = 15, now_timestamp: 'int | None' = None) -> 'tuple[WalletStakeWithdrawal, ...]'
```

## RestClient

Публичная операция/свойство SDK. Ниже приведены точные типы, значения по умолчанию и тип результата; контекст использования дан в руководстве раздела.

### address

Публичная операция/свойство SDK. Ниже приведены точные типы, значения по умолчанию и тип результата; контекст использования дан в руководстве раздела.

```python
async address(self, address: 'str') -> 'dict[str, Any]'
```

### address_full

Публичная операция/свойство SDK. Ниже приведены точные типы, значения по умолчанию и тип результата; контекст использования дан в руководстве раздела.

```python
async address_full(self, address: 'str', with_erc20: 'bool' = True, symbols: 'str | None' = None) -> 'dict[str, Any]'
```

### address_txs

Публичная операция/свойство SDK. Ниже приведены точные типы, значения по умолчанию и тип результата; контекст использования дан в руководстве раздела.

```python
async address_txs(self, address: 'str', page: 'Page | None' = None) -> 'dict[str, Any]'
```

### block

Публичная операция/свойство SDK. Ниже приведены точные типы, значения по умолчанию и тип результата; контекст использования дан в руководстве раздела.

```python
async block(self, height: 'int') -> 'dict[str, Any]'
```

### block_txs

Публичная операция/свойство SDK. Ниже приведены точные типы, значения по умолчанию и тип результата; контекст использования дан в руководстве раздела.

```python
async block_txs(self, height: 'int', page: 'Page | None' = None) -> 'dict[str, Any]'
```

### coin

Публичная операция/свойство SDK. Ниже приведены точные типы, значения по умолчанию и тип результата; контекст использования дан в руководстве раздела.

```python
async coin(self, denom: 'str') -> 'dict[str, Any]'
```

### coin_prices

Публичная операция/свойство SDK. Ниже приведены точные типы, значения по умолчанию и тип результата; контекст использования дан в руководстве раздела.

```python
async coin_prices(self) -> 'dict[str, Any]'
```

### coin_registry

Публичная операция/свойство SDK. Ниже приведены точные типы, значения по умолчанию и тип результата; контекст использования дан в руководстве раздела.

```python
async coin_registry(self, with_price: 'bool' = False, limit: 'int' = 500) -> 'dict[str, Any]'
```

### coin_registry_for_symbols

Публичная операция/свойство SDK. Ниже приведены точные типы, значения по умолчанию и тип результата; контекст использования дан в руководстве раздела.

```python
async coin_registry_for_symbols(self, symbols: 'list[str]', with_price: 'bool' = False) -> 'dict[str, Any]'
```

### coins

Публичная операция/свойство SDK. Ниже приведены точные типы, значения по умолчанию и тип результата; контекст использования дан в руководстве раздела.

```python
async coins(self, with_price: 'bool' = False, limit: 'int' = 100) -> 'dict[str, Any]'
```

### health

Публичная операция/свойство SDK. Ниже приведены точные типы, значения по умолчанию и тип результата; контекст использования дан в руководстве раздела.

```python
async health(self) -> 'dict[str, Any]'
```

### latest_block

Публичная операция/свойство SDK. Ниже приведены точные типы, значения по умолчанию и тип результата; контекст использования дан в руководстве раздела.

```python
async latest_block(self) -> 'dict[str, Any]'
```

### rewards_delegator

Публичная операция/свойство SDK. Ниже приведены точные типы, значения по умолчанию и тип результата; контекст использования дан в руководстве раздела.

```python
async rewards_delegator(self, delegator: 'str') -> 'dict[str, Any]'
```

### tx

Публичная операция/свойство SDK. Ниже приведены точные типы, значения по умолчанию и тип результата; контекст использования дан в руководстве раздела.

```python
async tx(self, tx_hash: 'str') -> 'dict[str, Any]'
```

### txs

Публичная операция/свойство SDK. Ниже приведены точные типы, значения по умолчанию и тип результата; контекст использования дан в руководстве раздела.

```python
async txs(self, page: 'Page | None' = None, **filters: 'Any') -> 'dict[str, Any]'
```

### validator

Публичная операция/свойство SDK. Ниже приведены точные типы, значения по умолчанию и тип результата; контекст использования дан в руководстве раздела.

```python
async validator(self, validator: 'str') -> 'dict[str, Any]'
```

### validator_delegations

Публичная операция/свойство SDK. Ниже приведены точные типы, значения по умолчанию и тип результата; контекст использования дан в руководстве раздела.

```python
async validator_delegations(self, validator: 'str') -> 'dict[str, Any]'
```

### validators

Публичная операция/свойство SDK. Ниже приведены точные типы, значения по умолчанию и тип результата; контекст использования дан в руководстве раздела.

```python
async validators(self) -> 'dict[str, Any]'
```

### wallet_balances

Публичная операция/свойство SDK. Ниже приведены точные типы, значения по умолчанию и тип результата; контекст использования дан в руководстве раздела.

```python
async wallet_balances(self, address: 'str', limit: 'int' = 300, offset: 'int' = 0, include_bank: 'bool' = True, prefer_bank: 'bool' = True) -> 'dict[str, Any]'
```

### wallet_stake_transfers

Публичная операция/свойство SDK. Ниже приведены точные типы, значения по умолчанию и тип результата; контекст использования дан в руководстве раздела.

```python
async wallet_stake_transfers(self, address: 'str') -> 'dict[str, Any]'
```

### wallet_stake_withdrawals

Публичная операция/свойство SDK. Ниже приведены точные типы, значения по умолчанию и тип результата; контекст использования дан в руководстве раздела.

```python
async wallet_stake_withdrawals(self, address: 'str', *, page: 'Page | None' = None, include_completed: 'bool' = False, recent_days: 'int | None' = None, tx_hashes: 'list[str] | None' = None, unbonding_days: 'int' = 15) -> 'tuple[WalletStakeWithdrawal, ...]'
```

### wallet_stakes

Публичная операция/свойство SDK. Ниже приведены точные типы, значения по умолчанию и тип результата; контекст использования дан в руководстве раздела.

```python
async wallet_stakes(self, address: 'str') -> 'dict[str, Any]'
```

### wallet_staking_summary

Публичная операция/свойство SDK. Ниже приведены точные типы, значения по умолчанию и тип результата; контекст использования дан в руководстве раздела.

```python
async wallet_staking_summary(self, address: 'str', *, include_unstakes: 'bool' = True, enrich_tokens: 'bool' = True, coin_lookup_limit: 'int' = 500) -> 'WalletStakingSummary'
```

### wallet_unstakes

Публичная операция/свойство SDK. Ниже приведены точные типы, значения по умолчанию и тип результата; контекст использования дан в руководстве раздела.

```python
async wallet_unstakes(self, address: 'str') -> 'dict[str, Any]'
```
