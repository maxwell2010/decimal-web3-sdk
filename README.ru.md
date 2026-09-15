# Decimal Web3 SDK

Независимый SDK для Decimal EVM от [MintCandy](https://mintcandy.ru/) и
[@Maxwell2019](https://t.me/Maxwell2019). Лицензия MIT, Python 3.10+.
Пакет: `decimal-web3-sdk`; импорт: `decimal_web3_sdk`.

**Версия 0.1.2 - предварительный релиз GitHub, не stable и не полное совпадение с официальными SDK.**
79 транзакционных методов проверяются офлайн, это не полное сетевое совпадение с JS/Go SDK.
Новые операции, legacy-ограничения и обновления NFT описаны в
[журнале разработки](docs/ru/transaction-parity-development.md).
[Сравнение SDK](docs/ru/upstream-parity.md): JS 95 / Go 53 / Python 79 специализированных EVM-методов, не процент полноты.

[English](README.md) | [Документация](docs/ru/README.md) | [Полный API](docs/ru/api.md)

## Установка Без Git

Требуются Python 3.10+ и pip. Автоматически установятся web3, eth-account,
aiohttp, certifi, python-dotenv и их зависимости.
[Поддержка ОС и требования установки](docs/ru/install.md).

Для установки или обновления до последней опубликованной версии используйте одну команду:
```shell
python -m pip install --upgrade -r "https://raw.githubusercontent.com/maxwell2010/decimal-web3-sdk/main/requirements-latest.txt"
```

Файл указывает на wheel конкретного релиза GitHub и обновляется при каждом
проверенном выпуске, включая предварительные. Обновление происходит только при
запуске команды, не внутри SDK автоматически. Git и вход в GitHub не требуются.

Для воспроизводимой установки конкретной версии:
```shell
python -m pip install "https://github.com/maxwell2010/decimal-web3-sdk/releases/download/v0.1.2/decimal_web3_sdk-0.1.2-py3-none-any.whl"
```

Либо из исходного архива той же версии:
```shell
python -m pip install "https://github.com/maxwell2010/decimal-web3-sdk/archive/refs/tags/v0.1.2.zip"
```

Основной источник установки: GitHub; публикация в PyPI выполняется отдельно.
Для production фиксируйте релиз; latest - отдельный канал обновления по выбору
пользователя. [Инструкция](docs/ru/releasing.md).

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
