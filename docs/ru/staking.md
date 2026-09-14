# Делегирование, Hold и Выводы
[Оглавление](README.md) | [Все примеры стейкинга](transactions/staking.md)
| [Контрактное чтение](reference/decimal.md) | [Индексатор](reference/rest.md)

Последовательность: делегирование -> обычный стейк или hold -> созревание ->
отзыв/перенос. withdraw/unbond запускает период вывода, не обещает мгновенное
зачисление на кошелек. Перенос в другой валидатор не является переводом кошельку.

get_stake(validator, delegator, token) читает обычный стейк.
get_hold_stake дополнительно требует точный hold-end timestamp, не начало hold.
get_stake_snapshot читает обычный стейк и известные hold-ключи в одном блоке.
Суммы складываются точно. Метод не ищет все валидаторы и неизвестные hold.

```python
import asyncio
import json
import os
from decimal_web3_sdk import DecimalClient, NetworkConfig

async def main():
    async with DecimalClient(NetworkConfig.mainnet()) as client:
        snapshot = await client.decimal.get_stake_snapshot(
            os.environ["VALIDATOR"], os.environ["WALLET_ADDRESS"],
            client.config.contracts.wdel,
            hold_timestamps=json.loads(os.environ["HOLD_TIMESTAMPS"]),
        )
        print(json.dumps(snapshot.as_dict(), indent=2))

asyncio.run(main())
```

Нативный DEL в Delegation использует адрес WDEL и token_type DEL=4, не DRC20=1.
Тип и ID должны соответствовать позиции. Нельзя заменять проверенный контрактом
обычный стейк величиной api_delta. Схема индексатора использует 18 минимальных
единиц для сумм, а не произвольные decimals токена.

wallet_staking_summary собирает индексированные позиции и unstakes.
wallet_stake_withdrawals объединяет текущие unstakes с ограниченной историей.
is_matured означает созревание, is_completed требует явного подтверждения.
completion_estimated помечает дату, вычисленную через unbonding_days (по умолчанию
15), а не гарантированную сетью. Неизвестный raw токена остается None.
include_completed добавляет явно завершенные записи; recent_days может исключить
старые, но еще актуальные позиции.

Флаги индексатора и available_to_unbond предварительны. Перед отзывом проверьте
контрактный snapshot и оцените точную операцию.
После подтверждения сохраните result.hold_timestamp/hold_time и хеш в базе
приложения. В SDK нет постоянной базы кошельков. Reset/with-reset нужен не каждому
hold: выбирайте совместимый метод контракта и проверяйте симуляцией.
