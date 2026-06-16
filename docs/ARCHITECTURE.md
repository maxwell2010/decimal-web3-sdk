# SDK Architecture

## Design Principles

- SDK не должен зависеть от публичного `api.decimalchain.com` как от обязательного источника.
- Web3 RPC, REST API и WS должны быть взаимозаменяемыми через `NetworkConfig`.
- Транзакции строятся локально, подписываются локально, отправляются через настроенные Web3 endpoints.
- REST используется для быстрых read-only сценариев: история, блоки, адреса, валидаторы, токены, цены.
- WS используется для подписок: новые блоки, транзакции, статусы, события адреса.
- Балансы кошельков для UI и мобильного приложения желательно брать из быстрого агрегированного API выбранной инфраструктуры, а не через массовые `balanceOf`/`symbols=all` на клиенте.

## Layers

1. `config` - сети, endpoints, chain id, адреса системных контрактов.
2. `rpc` - отказоустойчивый JSON-RPC pool с переключением между нодами.
3. `rest` - клиент Decimal-compatible API gateway.
4. `erc20` - ERC20 read-only helpers, balances, allowance, unit conversion.
5. `wallet` - ключи, адреса, подписи, typed data.
6. `contracts` - ABI registry, контрактные wrappers.
7. `transactions` - builders/sign/broadcast для DEL, затем ERC20/staking/multisend/NFT.
8. `client` - удобный фасад для приложений.
9. `cli` - консольная утилита поверх SDK.
10. `agents` - проверочные и транзакционные агенты.
11. `orchestrator` - параллельное/последовательное выполнение агентов с таймаутами.
12. `monitoring` - health snapshots, latency, SLA, future Prometheus/OpenTelemetry export.

## Public API Shape

```python
client = DecimalClient(NetworkConfig.mainnet())
await client.balance_del(address)
await client.tokens.balance(token, address)
await client.tx.send_del(to, amount, private_key, broadcast=False)
await client.tx.send_del(to, amount, private_key, broadcast=True)
await client.validators.list()
await client.ws.subscribe_address(address)
```

Current Python API shape:

```python
await client.rest.latest_block()
await client.rest.address_full(address, symbols="FRIDAYCOIN")
await client.rest.wallet_balances(address)
await client.erc20.balance(token, address)
await client.tx.send_del(request, broadcast=False)
await client.monitor().snapshot()
```

## Read-only Endpoint Groups

SDK ожидает Decimal-compatible API gateway с такими группами endpoint-ов:

| Группа | Endpoint | Назначение | Клиент |
|---|---|---|---|
| Балансы | `/erc20/balances/{address}?limit=300&include_bank=1&prefer_bank=1` | Быстрый полный список DEL/custom coin/ERC20 балансов | Mobile, Python SDK, сервисы |
| Стейкинг | `/wallets/{address}/staking` или аналог | Публичная безопасная сводка стейкинга | Mobile |
| Транзакции | `/txs`, `/addresses/{address}/txs`, `/txs/{hash}` | История и детали транзакций | Mobile, Notify, SDK |
| Блоки | `/blocks/latest`, `/blocks/{height}`, `/blocks/{height}/txs` | Высота, блоки, аудит | SDK, мониторинг |
| Монеты | `/coins`, `/coins/{denom}`, `/coins/prices` | Метаданные токена, цена, список монет | Mobile, Notify |
| Валидаторы | `/validators`, `/validators/{validator}`, `/validators/wallet/{address}/stakes/coins` | Валидаторы и делегирование | Mobile, Notify |
| Реварды | `/rewards/db/delegators/{address}/summary` | Быстрый расчет ревардов из индексера | Notify, сервисы |

Публичные mobile endpoints должны быть read-only и безопасными. Защищенные endpoint-ы с `X-API-Key` должны использоваться только серверными сервисами. В мобильное приложение сервисные ключи не вшиваются.

## Balance Loading Policy

Запрещенный для UI путь:

- не дергать `live=1` из мобильного приложения;
- не дергать `symbols=all&erc20_limit=1600` при открытии кошелька;
- не делать `balanceOf` по сотням/тысячам контрактов на устройстве.

Разрешенный быстрый путь:

1. primary API `/erc20/balances/{address}?limit=300&include_bank=1&prefer_bank=1`;
2. fallback API with the same shape;
3. если обе ноды недоступны, показать кеш последнего успешного ответа;
4. для серверных сервисов можно использовать защищенный API с ключом.

Если у кошелька не хватает contract-only токенов, прогрев делается на сервере индексером:

```bash
/home/evm_reader_tx/venv/bin/python /home/evm_reader_tx/erc20_balance_indexer.py --refresh-wallet 0x...
```

## Cross-platform Strategy

Python SDK остается первым reference implementation для серверов, CLI и локальной автоматизации.

TypeScript SDK нужно делать вторым слоем с таким же naming и DTO:

- Node.js CLI и backend.
- React Native/mobile.
- Browser wallet integrations.

Для мобильных приложений желательно держать бизнес-логику в TypeScript SDK, а тяжелые read-only запросы отдавать через выбранный REST API.

## Agents And Orchestrator

Агент - маленький независимый исполнитель: health check, latest block, gas estimation, transaction build, broadcast, receipt polling, API latency probe.

Оркестратор управляет агентами:

- parallel run для независимых проверок;
- sequential run для транзакционного pipeline;
- per-agent timeout;
- общий SLA через `TransactionPolicy`;
- метрики по каждому шагу.

Целевой быстрый pipeline:

1. build transaction: до 1.0s;
2. estimate gas: до 1.5s;
3. broadcast: до 1.5s;
4. first receipt/status poll: до 1.0s.

Итого бюджет 5 секунд. Фактическое подтверждение блока зависит от сети, поэтому SDK должен честно разделять `broadcasted_under_5s` и `confirmed_under_5s`.

## Web JS And Java

Python SDK является reference implementation.

Web JS SDK:

- package: `@mintcandy/decimal-sdk`;
- transport: REST/WS + `viem` for Web3/signing;
- targets: browser, Node.js, React Native.

Java SDK:

- package: `ru.mintcandy.decimal`;
- targets: Android, JVM backend, desktop tools;
- same DTO naming as Python/Web JS.

## Node Safety

SDK придерживается safe defaults, чтобы не перегружать выбранную инфраструктуру:

- no load tests in SDK by default;
- integration tests are opt-in only via `DECIMAL_SDK_RUN_INTEGRATION=1`;
- REST pagination is clamped by `SafetyLimits.rest_max_limit`;
- REST/RPC calls have small client-side spacing through `AsyncRateLimiter`;
- WS client is manual-connect only;
- WS does not run background infinite receive loops;
- WS subscriptions are capped by `SafetyLimits.ws_max_subscriptions`.

Для production мониторинга отдельный сервис должен задавать явные интервалы и лимиты, а не опираться на tight polling внутри SDK.

Важно: SDK работает только через публичные Web3/REST/WS интерфейсы и не меняет программный код, конфиги или файлы на самих нодах.
