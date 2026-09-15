# Дополнительные Транзакции: Разработка

История разработки **0.1.2**, предварительного релиза GitHub. Релиз 0.1.1 сохранен.
Новые операции не отправлялись ни в mainnet, ни в testnet. Реальные seed/private key не использовались.

## Что Добавлено

Из 24 отсутствовавших JS-операций добавлены типизированные аналоги: две операции
создания безрезервной NFT-коллекции объединены параметром `kind`, поэтому это 23
Python-метода. Дополнительно добавлен `nft.reset_stake_holds` из новой NFT-ветки.
Всего каталог теперь содержит **79 методов вместо 55**. Это не 79 доказанно
работающих сетевых сценариев и не число уникальных типов протокола.

| Раздел | Новые методы |
| --- | --- |
| DEL | `tx.burn_del` |
| Токены | `token.buy_exact`, `sell_for_exact_del`, `convert_to_del`, `update_min_supply` |
| Стейк | `decimal.complete_stake`, `apply_stake_penalty`, `apply_stake_penalties` |
| Валидаторы | `decimal.add_validator_token`, `add_validator_del`, `remove_validator`, `update_validator_metadata` |
| NFT | `nft.create_reserveless_collection`, `add_token_reserve`, `stake_to_hold`, `reset_stake_hold`, `reset_stake_holds`, `withdraw_with_reset`, `transfer_with_reset`, `hold_with_reset`, `complete_stake` |
| Safe | `multisig.create`, `approve_transaction`, `execute` |

Полные примеры с обязательными полями: [DEL](transactions/del.md),
[токены](transactions/tokens.md), [стейк](transactions/staking.md),
[валидаторы](transactions/validators.md), [NFT](transactions/nft.md), [Safe](transactions/multisig.md).

## Комиссия До Подписи

У новых контрактных методов один путь кодирования для комиссии и отправки:
`request.to_contract_call(client)` -> `service.build_operation(request)` ->
`service.estimate_fee_for_operation(request, exact=True)`.
Подготовка и расчет не подписывают транзакции, не создают permit и не отправляют approve.
`broadcast=False` в методе отправки означает локальную подпись после preflight, а не расчет без подписи.

```python
import asyncio
import getpass
import os
from decimal_web3_sdk import DecimalClient, NetworkConfig, BuyExactTokenRequest

async def main():
    request = BuyExactTokenRequest.from_mnemonic(
        mnemonic=getpass.getpass("Seed: "),
        token=os.environ["TOKEN"],
        recipient=os.environ["RECIPIENT"],
        amount_out_raw=int(os.environ["TOKEN_AMOUNT_RAW"]),
        max_amount_del=os.environ["MAX_AMOUNT_DEL"],
    )
    async with DecimalClient(NetworkConfig.testnet()) as client:
        quote = await client.token.estimate_fee_for_operation(request, exact=True)
        print("ready:", quote.ok)
        print("estimated DEL:", str(quote.estimated_fee_del))
        print("required DEL:", str(quote.required_del))

asyncio.run(main())
```

Для сжигания DEL: `tx.build_burn_del` и `tx.estimate_fee_for_burn_del`.
Сжигание необратимо. Для DEL approve не нужен. При `exact=False` сохраняется
существующий gas-limit buffer; это лимит расходов, не обещание фактической комиссии.
После изменения состояния контракт может потребовать другую комиссию.

`*_raw`, `*_wei`, NFT `token_id`, NFT `amount`, индексы и timestamps принимают
целые Python `int`, без float/округления. NFT `amount` означает число единиц,
не токен с 18 decimals. `amount_del` и аналогичные DEL-поля принимают точные
строки или Decimal. Новый `NftStake.as_dict()` возвращает большие количества и ID строками.

## Разрешения

Новые методы не прячут дополнительные отправки. Регистрация валидатора с токеном
и пополнение NFT-резерва без permit требуют уже достаточного allowance.
Неверное разрешение должно остановить RPC-симуляцию до подписи.
`AddTokenReserveNftRequest.permit` принимает готовую `PermitSignature` для нужного
reserve-токена и spender NFT. `ConvertToDelRequest` требует permit для GasCenter;
это отдельный контрактный сценарий, а не обычный `sell_for_exact_del`.
`estimated_gas` у GasCenter является аргументом контракта, не gas-limit внешней транзакции.
Правильные owner, spender, сумма, nonce, deadline и поддержка permit обязательны.

## NFT И Окончание Hold

Новая ветка JS `7dc2e4600ce4aa3dd8baf685d2f31b4f53bc08c7` является потомком
использованного master `6790d35e2decb0cbb06a9149a9c476c834f99223`.
Она исправляет ошибку расчета газа у `withReset`: все новые NFT-вызовы и оценки
должны использовать **delegation-nft**, не fungible Delegation.
Добавлены пакетный `resetHolds` и чтения `get_stake`, `get_stake_id`,
`get_hold_stake`, `get_frozen_stake`, `get_frozen_stakes`, `get_freeze_time`.
Явный `block_identifier` позволяет читать несколько значений на одном блоке.

В testnet установлен адрес NFT Delegation из этой ветки:
`0x07e2ad4dfc91412de09e33e4650254948b21a20c`, вместо mainnet-адреса.
Остальные старые testnet-адреса этим исправлением не подтверждаются.

Вывод/перенос создает frozen stake. Окончание hold не равно поступлению на кошелек:
после freeze-периода вызывается `complete_stake(indexes)`. Индексы берутся из
очереди/индексатора и перепроверяются `get_frozen_stakes(indexes)`, это не номера
валидаторов и не timestamps. Не используйте позицию строки UI как индекс очереди.

Актуальный ответ frozen stake содержит четыре поля:
`stake`, `freezeStatus`, `freezeType`, `unfreezeTimestamp`.
В примере feature-ветки показан старый трехэлементный вариант. SDK явно отклоняет
этот вариант, чтобы не принять тип операции за дату. Статус хранится отдельно,
его неизвестные значения не объявляются успешным завершением. Истекшая дата сама
по себе не означает доступность или завершение операции: нужна симуляция `complete`.
Полная on-chain выгрузка очереди без индексов не заявляется: проверенный ABI не
содержит getter, возвращающий всю очередь.

## Safe С Весами

Safe использует `(owner, weight)[]`, не просто список адресов.
Нужны `WeightedOwner`, порог веса и явный `salt_nonce` для создания.
`SafeTransaction` содержит nonce Safe и внутренние параметры вызова;
это не nonce внешнего кошелька и не его gas price.
`sign_safe_transaction(SignSafeTransactionRequest.from_mnemonic(...))` создает
локальную EIP-712 подпись. Она привязана к chain ID, адресу Safe и всем полям транзакции.
`approve_transaction` вместо этого отправляет отдельное on-chain подтверждение
полного tuple Safe-транзакции; оно расходует gas.

`execute` проверяет nonce, вес, уникальность и порядок подписей. Поддержаны EIP-712,
Safe eth_sign, approved-hash и контрактные подписи. Право использования approved-hash
и контрактных подписей проверяет контракт через eth_call, а не предположение SDK.
Внешний `status=1` не доказывает успех внутреннего действия: проверяются события
`ExecutionSuccess`/`ExecutionFailure` именно выбранного Safe и ожидаемого хеша.
Если receipt получен позже, вызовите `multisig.check_execution_result`.
После создания адрес доступен в `result.events["safe_address"]`, если receipt содержит ProxyCreation.

Универсальный `multisig.build_transaction(safe, unsigned_call, nonce=...)` позволяет
обернуть подготовленные NFT/другие вызовы вместо девяти однотипных JS-builder.
Запрос на выполнение должен подписываться владельцами Safe, а действие в контракте
выполняется от имени Safe, не внешнего отправителя.

## Ограничения И Источники

Результат: **225 тестов пройдено** на Windows/Python 3.12. Включены 79 методов
каталога, unsigned fee-only, независимая проверка calldata, больших чисел,
подписей Safe и NFT-ответов. Lint и аудит исходников пройдены.
Одна deprecation-предупреждение зависимости websockets.legacy остается.
Моковые оценки gas/цены в тестах не выдаются за реальные комиссии сети.
[Машиночитаемый отчет](../validation/transaction-parity-development.json).

На mainnet блоке 33638332 через SDK подтверждены chain ID 75, код пяти контрактов
и чтение NFT. Freeze-периоды: вывод 2592000 секунд (30 суток), перенос 1296000
секунд (15 суток); это значения на проверенном блоке, не константы SDK.
Testnet RPC не удалось подключить; testnet-проверки отправок не засчитываются.

Три новых аналога только legacy: `update_min_supply`, `apply_stake_penalty`,
`apply_stake_penalties`. Они отсутствуют в проверенных текущих ABI и по умолчанию
запрещены. `allow_legacy=True` допустим только для заведомо совместимого старого
контракта. Это не обход прав, комиссий или RPC-симуляции.
Текущий NFTCenter называет boolean `refundable`, а тип JS использует `allowMint`.
Новый безрезервный конструктор кодирует `refundable=False` и отдельный `burnable`;
эквивалентность старому `allowMint` не заявляется.

ABI-файлы взяты из официального [Contract API](https://api.decimalchain.com/api/v1/contracts/docs/index.html).
Их точные адреса-источники и даты находятся в `src/decimal_web3_sdk/abi/*.json`.
Исходники [NFT-ветки JS](https://bitbucket.org/decimalteam/dsc-js-sdk/src/7dc2e4600ce4aa3dd8baf685d2f31b4f53bc08c7/)
и [go-smart-node](https://bitbucket.org/decimalteam/go-smart-node/src/9e6c6d718d662083c4a524376a66d2c50bd4bc77/contracts/)
сверены отдельно. У ноды актуальный fungible Delegation ABI, но часть NFT/token ABI
старее опубликованных API. Обновление репозитория ноды не доказывает обновление каждого ABI.
Автоматического копирования всех ABI ноды или изменения действующих валидаторов нет.

Незавершенными остаются сетевые тесты новых отправок и прежние частичные совпадения
из [матрицы](upstream-parity.md), включая некоторые token/NFT selectors, permit и mixed-assets multisend.

## Передача В Консоль

Следующий этап: вкладка валидатора с проверкой полномочий текущего кошелька,
вкладка multisig, проверка NFT и загрузка аватаров валидатора, токена и NFT.
Кнопки управления не заменяют контрактную проверку прав; настоящие валидаторы
не останавливать и не удалять в рамках тестирования.

Официальный JS указывает `https://testnet-nft-ipfs.decimalchain.com/` для всех
сетей с пометкой TODO. `ipfs.ts` использует `POST /upload` для NFT,
`POST /upload-image` для картинки, multipart-поле `uploading_files`,
`GET /ipfs/{cid}` для чтения. Адрес загрузки и gateway должны стать отдельными
настройками, например `DECIMAL_IPFS_API_URL` и `DECIMAL_IPFS_GATEWAY_URL`.
При проверке HEAD корня TLS прошел штатную проверку, ответ HTTP 404.
Результат относится только к этому запросу и клиентскому стеку, а не к загрузке.
При последующей проверке интеграции консоли Python 3.12/aiohttp на Windows отклонил
`POST /upload-image` до отправки тела с `SSLCertVerificationError:
certificate has expired`. Это результат, сообщенный задачей консоли, а не повторная
независимая проверка SDK.

Независимая TLS-диагностика 15.09.2026 воспроизвела ошибку Python и обнаружила
устаревший кросс-подписанный `ISRG Root X2` в локальном хранилище Windows `CA`.
Издатель: `ISRG Root X1`, срок истек 15.09.2025 в 16:00:00 UTC. SHA-256:
`8B:05:B6:8C:C6:59:E5:ED:0F:CB:38:F2:C9:42:FB:FD:20:0E:6F:2F:F9:F8:5D:63:C6:99:4E:F5:E0:B0:27:01`.
Сертификат домена от Let's Encrypt YE1 действует с 22.07.2026 05:31:02 UTC
до 20.10.2026 05:31:01 UTC; все сертификаты, выданные сервером, действующие.
Python прошел проверку с временной копией того же набора доверенных сертификатов
без единственного истекшего локального CA, с `CERT_REQUIRED` и проверкой имени
домена. С набором certifi проверка также проходит. Постоянное хранилище Windows
и TLS-настройки приложений не изменялись. Причина воспроизведенной ошибки находится
в локальной цепочке доверия, а не в просрочке сертификата домена Decimal.
Загрузка и долговременный pinning остаются неподтвержденными.
Ошибку загрузки необходимо явно показывать.
Не отключать TLS-проверку и не включать upload-ключи или seed в клиентский код.

### Проверенное Исправление Клиента

SDK 0.1.2 использует certifi для собственных REST/WSS-сессий;
явный параметр `tls_ca_file` также передается RPC. Сертификаты Windows не удаляются,
проверка TLS не отключается. Приоритет настроек своего CA описан в разделе
[сетей и кошельков](networks-wallets.md).

После изменения проходят 242 офлайн-теста, включая 17 TLS-тестов. Настоящие
TLS-handshake в памяти принимают явно доверенный частный CA и отклоняют просроченный,
недоверенный и выписанный для другого домена сертификат. Ruff и проверка генерации
документации проходят. 15.09.2026 в 02:29 UTC собственные HTTP-сессии REST и WS
достигли корня Decimal IPFS с обычной проверкой TLS и получили HTTP 404.
Чтение mainnet RPC вернуло блок 33644205. Это не проверка живого WebSocket,
загрузки или pinning. Файлы и транзакции не отправлялись, релиз не публиковался.

Обновление консоли развертывать только после ее тестов и проверки отката.
Развертывание консоли и публикация SDK - отдельные операции; прежние теги и файлы SDK сохраняются.
