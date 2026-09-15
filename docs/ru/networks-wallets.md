# Сети и Кошельки
[Оглавление](README.md) | [Конфигурация](reference/config.md) | [Кошельки](reference/wallet.md)

| Пресет | Chain ID | Официальный RPC |
| --- | --- | --- |
| mainnet (по умолчанию) | 75 | https://node.decimalchain.com/web3/ |
| testnet | 202020 | https://testnet-val.decimalchain.com/web3/ |
| devnet | 202020 | https://devnet-val.decimalchain.com/web3/ |

Адреса соответствуют [официальному JS SDK](https://bitbucket.org/decimalteam/dsc-js-sdk/src/master/src/endpoints.ts).
Одинаковый chain ID testnet/devnet не означает одинаковые контракты.
SystemContracts хранит снимок адресов, не выполняет автоматический поиск.
При подготовке релиза mainnet проверен чтением, testnet был недоступен.

Основной индексированный API: https://api.decimalchain.com/api/v1/ .
Для других сетей поддомены testnet-api/devnet-api. Старые gate API используют
mainnet-gate/testnet-gate/devnet-gate и /api/. Старые REST-метаданные узлов
сохраняют HTTP /rest/ из JS SDK; секреты через HTTP передавать нельзя.
WebSocket URL по умолчанию не задан.

Переопределения окружения: DECIMAL_WEB3_URLS, DECIMAL_API_BASE,
DECIMAL_API_ROOT, DECIMAL_WS_URLS. Для других сетей префиксы DECIMAL_TESTNET_
и DECIMAL_DEVNET_. Список URL разделяется запятыми. SDK не загружает произвольный
dotenv при импорте. API-ключ необязателен и относится к вашему API.

## Своя Нода
```python
import os
from dataclasses import replace
from decimal_web3_sdk import NetworkConfig

config = replace(NetworkConfig.testnet(), web3_urls=[os.environ["MY_TESTNET_RPC"]])
```

Сохраняются сеть и снимок контрактов выбранного пресета.
NetworkConfig.custom требует web3_urls для работы клиента; API/WS нужны только
соответствующим сервисам. Для произвольной сети явно передавайте SystemContracts:
при отсутствии используется mainnet-снимок, а не поиск контрактов.
Адрес-заглушка не является настоящей нодой.

## Доверенные CA Для TLS

Начиная с версии `0.1.2`, собственные REST- и WebSocket-сессии SDK
используют набор CA из certifi без автоматического чтения кеша сертификатов Windows.
Проверки срока действия, доверенного издателя и имени домена остаются включенными.
Отсутствующий или неверный CA-файл вызывает ошибку: повтора с отключенной проверкой
нет. RPC уже использует штатную проверку сертификатов Requests.

Для своего CA задайте `tls_ca_file`: PEM-набор должен содержать все корни, нужные
вашим endpoints. Он заменяет набор по умолчанию для REST, WSS и RPC:

```python
import os
from dataclasses import replace
from decimal_web3_sdk import NetworkConfig

config = replace(NetworkConfig.mainnet(), tls_ca_file=os.environ["MY_CA_BUNDLE"])
```

Поддерживается также `NetworkConfig.custom(tls_ca_file=...)`. Пресеты читают
`DECIMAL_TLS_CA_FILE`; testnet/devnet сначала проверяют `DECIMAL_TESTNET_TLS_CA_FILE` /
`DECIMAL_DEVNET_TLS_CA_FILE`, затем общую переменную. Настройки Windows и глобального
Python не изменяются. При отсутствии `tls_ca_file` собственные aiohttp-сессии
учитывают `SSL_CERT_FILE` и/или `SSL_CERT_DIR`; явно заданный отдельный каталог CA
не дополняется публичными корнями автоматически. Для RPC без явного CA-файла SDK
сохраняется поведение Requests с `REQUESTS_CA_BUNDLE` / `CURL_CA_BUNDLE`.
Переданная пользователем сессия `DecimalWsClient` сохраняет свои TLS-настройки;
SDK ее не закрывает.

Используется [рекомендованная aiohttp настройка certifi с проверкой TLS](https://docs.aiohttp.org/en/stable/client_advanced.html#ssl-control-for-tcp-sockets).

## Сид-Фраза и Индексы
```python
import getpass
from decimal_web3_sdk import mnemonic_to_account, mnemonic_to_accounts

mnemonic = getpass.getpass("Mnemonic: ")
wallet = mnemonic_to_account(mnemonic, account_index=0)
print(wallet.address)
for index, account in enumerate(mnemonic_to_accounts(mnemonic, count=10)):
    print(index, account.address, account.derivation_path)
```

Индексы 0..9: `m/44'/60'/0'/0/i`. Это HD-деривация, не nonce транзакции.
BIP39 passphrase необязательна и не является PIN. Передавайте либо account_index,
либо account_path. Запросы from_mnemonic используют те же настройки.
generate_mnemonic_account создает новые секреты, результат нужно защищать.
Зависимость eth-account помечает HD-функциональность как unaudited.
