# Decimal Web3 SDK

Независимый SDK для Decimal EVM от [MintCandy](https://mintcandy.ru/) и
[@Maxwell2019](https://t.me/Maxwell2019). Лицензия MIT, Python 3.10+.
Пакет: `decimal-web3-sdk`; импорт: `decimal_web3_sdk`.

**Эта ветка: неопубликованная 0.1.2.dev0. Публичный пакет остается 0.1.1.**
79 транзакционных методов проверяются офлайн, это не полное сетевое совпадение с JS/Go SDK.
Новые операции, legacy-ограничения и обновления NFT описаны в
[журнале разработки](docs/ru/transaction-parity-development.md).
[Сравнение SDK](docs/ru/upstream-parity.md): JS 95 / Go 53 / Python 79 специализированных EVM-методов, не процент полноты.

[English](README.md) | [Документация](docs/ru/README.md) | [Полный API](docs/ru/api.md)

## Установка Без Git

Ссылки ниже устанавливают опубликованную 0.1.1, без новых методов ветки разработки.

Требуются Python 3.10+ и pip. Автоматически установятся web3, eth-account,
aiohttp, python-dotenv и их зависимости.
[Поддержка ОС и требования установки](docs/ru/install.md).

Из версионного релиза GitHub, без установленного Git:
```shell
python -m pip install "https://github.com/maxwell2010/decimal-web3-sdk/releases/download/v0.1.1/decimal_web3_sdk-0.1.1-py3-none-any.whl"
```

Либо из исходного архива той же версии:
```shell
python -m pip install "https://github.com/maxwell2010/decimal-web3-sdk/archive/refs/tags/v0.1.1.zip"
```

Ссылки работают после публикации соответствующего релиза и тега GitHub.
Основной источник установки: GitHub; публикация в PyPI выполняется отдельно.
Фиксируйте версию релиза, не подвижную ветку main. [Инструкция](docs/ru/releasing.md).

## Получить Баланс

```python
import asyncio
import os
from decimal_web3_sdk import DecimalClient

async def main():
    async with DecimalClient() as client:
        balance = await client.balance_del(os.environ["WALLET_ADDRESS"])
        print(format(balance, "f"))

asyncio.run(main())
```

Клиент и CLI по умолчанию используют **mainnet** и официальные RPC Decimal.
Для тестов явно выбирайте `NetworkConfig.testnet()` или CLI `--network testnet`;
возможность использовать свои ноды сохранена.
Для чтения балансов не нужны ключи.
`100000000000000000` минимальных единиц при decimals=18 равно ровно `0.1`,
не `1`. Суммы передаются строками или Decimal, не float.

В каждом разделе приведены полные примеры транзакций со скрытым локальным вводом
сид-фразы и отключенной отправкой. `broadcast=False` допускает подпись; для
расчета без подписи используйте методы оценки комиссии.
DEL не требует approve. ERC20 permit работает только при совместимых контрактах;
иначе approve остается отдельной транзакцией.

[Безопасность](SECURITY.md) | [Изменения](CHANGELOG.md)
