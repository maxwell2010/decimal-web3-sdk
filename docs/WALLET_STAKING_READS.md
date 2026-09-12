# Wallet Staking Reads

Дата: 2026-08-18

## Задача

Добавить в SDK read-only получение делегированных токенов кошелька, чтобы приложение могло показать стейкинг по валидаторам и затем подготовить операции отзыва стейка (`unbond`).

Важно: SDK не должен хранить seed phrase, private key, приватные RPC/API URL или ключи доступа. Все endpoint-ы должны задаваться через `NetworkConfig` или переменные окружения.

## Что понадобилось

- Endpoint активных делегаций:

```http
GET /validators/wallet/{address}/stakes/coins
```

- Endpoint текущих анбондов:

```http
GET /validators/{address}/unstakes/coins
```

- Endpoint переносов стейка, если API его поддерживает:

```http
GET /validators/wallet/{address}/transfer/coins
```

- Endpoint справочника монеты для резолва DRC20/ERC20 contract address:

```http
GET /coins/{symbol}
```

В `DecimalApi` это соответствует proxy/facade логике поверх Decimal node state. В `Notify2025` используется такой же подход: стейкинг берется через wallet staking endpoint, а данные монеты и цены добираются отдельно через coin endpoint.

## Почему одного staking endpoint недостаточно

Ответ `/validators/wallet/{address}/stakes/coins` уже содержит:

- валидатор;
- символ монеты;
- сумму делегирования;
- сумму в базовой DEL-оценке;
- hold/unlocked данные;
- тип стейка.

Но для полноценного SDK этого мало: для `unbond_erc20` нужен contract address токена. В staking payload его может не быть, поэтому SDK дополнительно берет символы из стейка и точечно резолвит их через `/coins/{symbol}`.

Для `DEL` contract address не нужен. SDK помечает такие позиции как `is_native=True` и оставляет `token_address=None`, чтобы приложение не перепутало native DEL unbond с ERC20 unbond.

## Что добавлено в SDK

Файл:

```text
src/decimal_web3_sdk/rest.py
```

Новые dataclass-модели:

```python
WalletStakeHold
WalletStakePosition
WalletUnstakePosition
WalletStakingSummary
```

Новые методы:

```python
await client.rest.wallet_stakes(address)
await client.rest.wallet_unstakes(address)
await client.rest.wallet_stake_transfers(address)
await client.rest.wallet_staking_summary(address)
await client.rest.coin_registry_for_symbols(symbols)
```

Нормализатор:

```python
normalize_wallet_staking_summary(
    address,
    stakes_payload,
    unstakes_payload=None,
    coins_payload=None,
)
```

Экспорт добавлен в:

```text
src/decimal_web3_sdk/__init__.py
```

CLI-команда добавлена в:

```text
src/decimal_web3_sdk/cli.py
```

```powershell
python -m decimal_web3_sdk.cli wallet-staking 0xWallet
```

## Как работает цепочка

1. SDK запрашивает активные делегации кошелька.
2. Опционально параллельно запрашивает текущие анбонды.
3. Из staking payload собирает уникальные символы токенов, кроме `DEL`.
4. По каждому символу вызывает `/coins/{symbol}`.
5. Из coin object берет `drc20_address`.
6. Собирает `WalletStakingSummary`.

Позиция стейка содержит:

```python
position.validator_name
position.validator
position.symbol
position.amount
position.amount_raw
position.base_amount_del
position.base_amount_raw
position.is_hold
position.is_native
position.token_address
position.token
position.hold_amount
position.unlocked_amount
position.api_unlocked_delta
position.holds
position.held_amount
position.matured_hold_amount
position.available_to_unbond
position.held_base_amount_del
position.available_base_amount_del
position.can_unbond
position.can_withdraw_hold
position.raw
```

## Как определить состояние стейка

SDK разделяет несколько величин:

- `amount` - вся сумма позиции в делегировании;
- `held_amount` - часть позиции, которая находится в hold;
- `api_unlocked_delta` / `unlocked_amount` - разница, которую вернул API как `delegatedCoins - hold_amount`;
- `matured_hold_amount` - сумма hold-записей, которые API уже пометил как `is_expired=True`;
- `available_to_unbond` - часть позиции, которую SDK считает безопасной для обычного `unbond`.

Правило:

```python
if position.is_hold or position.hold_amount > 0:
    available = position.unlocked_amount
else:
    available = position.amount
```

Для native `DEL`:

```python
if position.is_native and position.can_unbond:
    # использовать UnbondDelRequest
```

Для DRC20/ERC20 токена:

```python
if not position.is_native and position.token_address and position.can_unbond:
    # использовать UnbondErc20Request(token=position.token_address)
```

Hold-часть нельзя отозвать обычным `unbond`, пока конкретная hold-запись не созрела. Для таких позиций UI должен показывать `held_amount` отдельно, а список hold-записей брать из `position.holds`.

Для контрактных методов `getHoldStake` / `withdrawHold` timestamp берется из `hold.hold_end_time` (`hold.contract_hold_timestamp`), а не из `hold_start_time`.

`unlocked_amount` не смешивается с hold-частью даже для `DEL`. Перед отправкой обычного `withdraw` остаток следует подтвердить через `get_stake_snapshot(...)` и contract preflight: индексатор может отставать от состояния контракта.

## Строгое чтение контракта

Контракт Decimal кодирует fungible stake типами `DRC20=1` и `DEL=4`. Для `DEL`
поле `token` содержит адрес WDEL из выбранной конфигурации, но это по-прежнему
native DEL-позиция. SDK не принимает NFT-типы как монеты и строго проверяет
`validator`, `delegator`, `token`, `tokenId=0`, тип и hold key.

```python
snapshot = await client.decimal.get_stake_snapshot(
    validator="0xValidator",
    delegator="0xWallet",
    token=client.config.contracts.wdel,
    hold_timestamps=[1820176010, 1820210108],
)

print(snapshot.regular_amount())
print(snapshot.held_amount())
print(snapshot.matured_holds())
print(snapshot.missing_hold_timestamps)
```

Snapshot читает обычный `getStake` и только переданные `getHoldStake` на одном
блоке. Список ограничен 100 ключами, глобального сканирования контракта нет.
Timestamp для hold должен быть известен из индексатора или события контракта.
Пустой контрактный ответ сохраняется как `exists=False`, а не превращается в
реальную позицию с нулевым балансом.

Для передачи ответа в JSON используйте `as_dict()`. Все потенциально большие
`uint256` (`amount_raw`, `token_id`, `hold_timestamp`) возвращаются строками:

```python
stake = await client.decimal.get_stake(
    "0xValidator",
    "0xWallet",
    client.config.contracts.wdel,
)
payload = stake.as_dict()

assert payload["amount_raw"] == "100000000000000000"
assert payload["amount"] == "0.1"
```

Не переводите raw amount во `float` или JavaScript `Number`. Для отображения
используйте готовую строку `amount`, а для точных вычислений в Python -
`stake.amount()` (`Decimal`).

В старом JS SDK описан `getStakesPageByMember`, однако в актуальной mainnet
реализации Delegation этого selector нет. Python SDK поэтому не публикует метод,
который гарантированно завершался бы revert. Для discovery нужен ограниченный
индексатор, после чего каждая выбранная позиция проверяется методами выше.

Когда hold уже созрел, для DEL может потребоваться не обычный `withdraw`, а reset-сценарий:

```python
from decimal_web3_sdk import WithdrawDelStakeWithResetRequest

request = WithdrawDelStakeWithResetRequest(
    validator=position.validator,
    amount_del="4.21",
    hold_timestamps_to_reset=[1787078776],
    private_key=account.private_key,
)

fee = await client.decimal.estimate_fee_for_withdraw_del_stake_with_reset(request, exact=True)

if fee.ok:
    result = await client.decimal.withdraw_del_stake_with_reset(
        request,
        broadcast=True,
        wait_receipt=True,
    )
```

`hold_timestamps_to_reset` заполняется значениями `hold.contract_hold_timestamp`, то есть обычно `hold_end_time`.

Агрегаты по символам доступны прямо из summary:

```python
summary.delegated_by_symbol
summary.held_by_symbol
summary.available_to_unbond_by_symbol
summary.held_positions
summary.available_positions
```

## Пример использования

```python
from decimal_web3_sdk import DecimalClient, NetworkConfig

config = NetworkConfig.custom(
    chain_id=75,
    web3_urls=["https://your-decimal-rpc.example/web3/"],
    api_base_url="https://your-api.example/v1",
)

async with DecimalClient(config) as client:
    summary = await client.rest.wallet_staking_summary("0xWallet")

    print(summary.total_del)

    for position in summary.positions:
        print(
            position.validator_name,
            position.symbol,
            position.amount,
            position.base_amount_del,
            position.is_native,
            position.token_address,
        )
```

Пример списка доступного к отзыву:

```python
for position in summary.available_positions:
    print(
        position.validator_name,
        position.symbol,
        position.available_to_unbond,
        position.token_address,
    )
```

## Проверка на рабочем кошельке

Проверка выполнялась read-only по seed phrase из локального `.env`. Seed phrase и private key не выводились.

Результат:

- найдено `12` позиций делегирования;
- найдено `2` валидатора;
- `2` позиции native `DEL`;
- `10` позиций токенов с найденным `token_address`;
- активных анбондов: `0`.

Валидаторы:

- `MAKAROVSKY`;
- `Spacebot`.

Токены в делегировании:

- `BYACADEMY`;
- `DEL`;
- `EMELYANOV`;
- `MAKAROVSKY`;
- `MAXMODA`;
- `SHEVELEV`;
- `BALANCE`;
- `KOLLABIUM`;
- `MONOLIT`;
- `SBT`.

## Ограничения

- Если выбранный API не поддерживает `/validators/wallet/{address}/stakes/coins`, SDK не сможет получить read-only staking summary.
- Если `/coins/{symbol}` недоступен или монета не найдена, позиция останется с суммой и символом, но без `token_address`.
- Для native `DEL` `token_address` всегда должен быть `None`.
- Для ERC20/DRC20 `unbond` приложению нужно использовать `position.token_address`.
- `available_to_unbond` считается из API/state payload. Перед реальным `unbond` подтвердите обычную позицию через `get_stake_snapshot(...)` и обязательно вызывайте fee/preflight estimate.

## Проверка unbond preflight

Для позиции `Spacebot / DEL` read-only API показал:

```text
total: 404.802440067203299394 DEL
hold: 402.267370842988191794 DEL
available_to_unbond: 2.5350692242151076 DEL
```

Но preflight обычного `withdraw` для native DEL вернул `execution reverted`, поэтому broadcast выполнять нельзя. Проверены варианты WDEL, DEL token и zero address.

Дополнительно проверено, что `getStake(validator, wallet, WDEL)` для этих DEL-позиций возвращает обычный stake amount `0`, а сами DEL лежат как hold-записи. `getHoldStake` находит их по `hold_end_time`.

После созревания первого `MAKAROVSKY / DEL` hold обычный `withdraw` все еще возвращает revert, но `withdrawWithReset(validator, WDEL, amount, [hold_end_time])` проходит preflight. Ниже сохранен исторический расчет со старым принудительным cap `20 gwei`; использовать его как актуальную комиссию нельзя:

```text
validator: MAKAROVSKY
amount: 4.21 DEL
hold_timestamps_to_reset: [1787078776]
gas: 376308
gas_limit: 413939
effective gas price: 20 gwei
fee: 0.00752616 DEL
```

Сеть потребовала более высокий minimum global fee, после чего retry прошел с минимально допустимым gas price. Фактическая транзакция `0xc1dac6b3c70b0c689c6d0f1cb19c5bba57e93bc7f254788128d860dc238b492a` вошла в блок `33232007`; Explorer показал комиссию `0.438 DEL`. Теперь SDK по умолчанию берет oracle gas price сети без жесткого cap и показывает exact и buffered значения отдельно.

Поэтому приложение должно разделять подтвержденный обычный DEL stake и конкретные hold-записи. Для созревшего hold предлагается отдельный сценарий `withdraw_del_stake_with_reset`; будущий hold отзывать нельзя.

Для контрольной ERC20/DRC20 позиции `Spacebot / MONOLIT` preflight прошел:

```text
amount: 0.929292502986179406 MONOLIT
gas: 276515
fee: 0.0055303 DEL
```

Вывод: SDK должен показывать API-доступность как предварительную подсказку, но перед отправкой staking withdraw всегда делать contract preflight. Для DEL hold-позиций требуется отдельная проверка правил контракта Decimal.

## История выводов стейка

В explorer есть отдельный пользовательский блок `История выводов`: это уже заказанные выводы стейка, которые ожидают дату возврата на кошелек или недавно завершились. Для него в SDK добавлен отдельный read-only метод:

```python
withdrawals = await client.rest.wallet_stake_withdrawals(address)

for item in withdrawals:
    print(item.validator_name, item.symbol, item.amount, item.available_time)
```

По умолчанию метод возвращает только актуальные выводы, у которых дата возврата еще не наступила. Для аудита истории можно включить завершенные записи:

```python
withdrawals = await client.rest.wallet_stake_withdrawals(
    address,
    include_completed=True,
    recent_days=90,
)
```

Источники данных:

- `/validators/{address}/unstakes/coins` - pending undelegations из node state;
- `/txs?address={address}` - индексированные транзакции кошелька;
- `tx_hashes=[...]` - точечное обогащение по известным hash, если индекс списка еще не догнал детальную запись.

Для `withdraw_with_reset` SDK считает дату возврата как `timestamp + 15 days`, если API не отдал готовое поле `unbonding_time`, `unlock_date` или `completion_time`. Технический `WDEL` в таких записях нормализуется в пользовательский `DEL`.

Пример после успешного `withdraw_del_stake_with_reset`:

```text
validator: MAKAROVSKY
symbol: DEL
amount: 4.21
tx: 0xc1dac6b3c70b0c689c6d0f1cb19c5bba57e93bc7f254788128d860dc238b492a
available_time: 2026-09-03T14:03:42Z
```

## Mainnet preflight для FRIDAYCOIN

На кошельке `0xB31Ece152AA5990A851877f28217B6F6eFddCdCd` состояние проверено
напрямую через `Delegation.getStake` и `Delegation.getHoldStake`:

```text
token: FRIDAYCOIN
token address: 0x2CD327990E13270f078F52E3A986a497E1012A39
validator: Freedom
regular delegation: 100 FRIDAYCOIN
hold delegation: 100 FRIDAYCOIN
hold timestamp: 1787933707
hold time: 2026-08-28T16:15:07Z
```

Холд уже созрел. Без подписи и broadcast выполнен exact preflight на минимальной сумме
`0.000001 FRIDAYCOIN`. При oracle gas price `1190.475 gwei` получены результаты:

| Операция | Gas | Exact fee, DEL | Результат |
|---|---:|---:|---|
| Обычный unbond | 276467 | 0.329127051825 | Доступно |
| Вывод созревшего hold | 296863 | 0.353407979925 | Доступно |
| Перенос обычного стейка | 286248 | 0.3407710878 | Доступно |
| Перенос hold-стейка | 306652 | 0.3650615397 | Доступно |
| `withdrawWithReset` | 383240 | 0.456237639 | Доступно |

Все пять вызовов прошли `eth_estimateGas` и проверку достаточности DEL-баланса. Это
снимок сетевой комиссии, а не фиксированный тариф: перед каждой отправкой расчет нужно
повторять. Баланс до и после dry-run остался `4.762111774673044717 DEL`.

## Тесты

Добавлены unit-тесты:

```text
tests/test_wallet_staking_summary.py
```

Проверяют:

- нормализацию grouped staking payload;
- суммы `delegatedCoins` и `delegatedBaseCoins`;
- валидаторов;
- hold/unlocked поля;
- анбонды;
- историю выводов стейка;
- нормализацию `WDEL` -> `DEL` для `withdraw_with_reset`;
- enrichment токена через `drc20_address`;
- разделение native `DEL` и ERC20/DRC20 токенов.

Команда:

```powershell
pytest -q
```

Результат:

```text
31 passed
```
