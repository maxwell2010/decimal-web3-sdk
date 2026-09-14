# Данные и Дополнительные API
[Оглавление](README.md) | [Справочник](api.md)

## Доступ к Данным
DecimalClient: block_number, balance_wei/balance_del, transaction_count
(pending nonce), gas_price, estimate_gas, contract_code, transaction_receipt.
Подписант для чтения не нужен. contract_code_exists проверяет наличие кода,
не совместимость ABI. receipt=None означает отсутствие receipt, не ошибку RPC.

RestClient: block/block_txs, tx/txs, address/address_full/address_txs,
wallet_balances, coins/coin/coin_registry/coin_prices, validators/validator,
validator_delegations, rewards_delegator и методы стейкинга/выводов кошелька.
Page ограничивает limit/offset настройками safety. Одна страница не является
всей сетью; coin_registry также может быть ограничен. Raw-ответы сохраняют
схему сервера, универсальная нормализация всех endpoint не заявлена.

Часть маршрутов, включая /evm/wallet/... и нормализованный стейкинг, рассчитана
на совместимый API-фасад и может отсутствовать у официальных микросервисов.
API можно переопределить в NetworkConfig независимо от RPC.
Недоступный ответ нельзя подменять пустым балансом.
Внутренний JSON-парсер сохраняет точность дробных чисел.

## WebSocket
DecimalWsClient поддерживает connect/close, subscribe/unsubscribe, receive_once.
Это Tendermint-style JSON-RPC, не адаптер Ethereum eth_subscribe.
Совместимый WS URL задается явно. WsMessage содержит method и params.
SafetyLimits ограничивает подписки/частоту, не гарантирует доступность сервиса.
Всегда закрывайте сессии через finally/асинхронный контекст.

## CLI
```shell
decimal-sdk --help
decimal-sdk --network testnet block-number
decimal-sdk wallet-sequence
decimal-sdk wallet-from-mnemonic
```

По умолчанию CLI выбирает mainnet, как DecimalClient(). Для тестов явно задавайте --network testnet.
Сид-фраза может вводиться локальным скрытым запросом, не попадая в историю команд.
Транзакционные команды также запрашивают сид-фразу, если --private-key не задан.
--account-index выбирает адрес подписи. Передача технического ключа аргументом
сохранена для совместимости, но не рекомендуется.
wallet-generate намеренно выводит новый секрет для восстановления; защищайте stdout.
wallet-from-mnemonic по умолчанию ключ не показывает.

## Совместимые Дополнения
- AbiRegistry читает JSON ABI из указанного каталога; удаленный код не исполняется.
- TransactionPolicy, DecimalMonitor, AgentOrchestrator организуют проверки
  доступности, задержек, receipt и этапов транзакции. AgentContext.data принадлежит
  приложению и может содержать секреты; логировать его нельзя.
- Транзакционные агенты отдельно строят, оценивают, подписывают и отправляют.
  BroadcastTransactionAgent действительно отправляет транзакции.
- telemetry собирает длительности/метрики; не передавайте секретные payload.
- test_harness/TxTrainingJournal сохранен как необязательная QA-утилита.
  У него собственные сетевые переменные окружения, не CLI --network.
  Отправка по умолчанию отключена; для живых тестов нужна отдельная настройка
  пополненного кошелька и проверка ожидаемого адреса.
- candy_protocol является mainnet-only адаптером неподписанных вызовов.
  Использует разрешенный профиль и строит контрактные вызовы/сжигание DEL или
  токена. Это не мобильный кошелек и не сервер приложения.

Все сигнатуры, поля и значения по умолчанию перечислены в [справочнике](api.md).
Эти дополнительные модули не обязательны для обычной отправки Decimal.
