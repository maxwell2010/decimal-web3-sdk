# Decimal Web3 SDK Roadmap

## Phase 0 - Repository Reset

Status: started.

- Перенести старый монолитный SDK в `backup/legacy_*`.
- Создать чистую структуру `src/decimal_web3_sdk`.
- Зафиксировать источники: старый Python SDK, `decimal_python_sdk`, `DecimalApi`, JS SDK, Go SDK, `go-smart-node`.
- Описать архитектуру и публичный API.

## Phase 1 - Read-only SDK

Goal: безопасный SDK без отправки транзакций.

- Web3 failover over user-supplied Decimal RPC endpoints.
- REST client для собственного API:
  - health
  - latest block
  - block by height
  - tx by hash
  - address balances
  - address tx history
  - validators
  - coins/tokens
- Wallet helpers:
  - private key -> address
  - mnemonic -> private key
  - checksum validation
- Contract reads:
  - ERC20 balance/name/symbol/decimals
  - allowance
  - delegation/stake reads
- Typed DTO вместо сырых dict там, где формат стабилен.

Current status:

- `RestClient` added for blocks, txs, addresses, coins, validators, rewards.
- `Erc20Service` added for info, balance, allowance and unit conversion.
- Core Decimal system contract addresses added to `NetworkConfig`.

## Phase 2 - Transaction Builders

Goal: строить, оценивать и подписывать транзакции локально.

- Единый результат:
  - `success`
  - `tx_hash`
  - `fee_del`
  - `gas`
  - `raw_tx`
  - `error`
- `broadcast=False` для dry-run/оценки комиссии.
- DEL:
  - send
  - send with memo
  - wrap/unwrap WDEL
- ERC20:
  - transfer
  - approve
  - transferFrom
  - permit detection
- Staking:
  - delegate DEL
  - unbond DEL
  - delegate ERC20
  - hold
  - withdraw hold
- Multisend:
  - DEL multisend
  - token multisend
  - permit-first strategy
  - fallback approve + aggregate

Current status:

- Native DEL transfer build/estimate/sign/broadcast service added.
- Native transaction pipeline agents added:
  - build
  - estimate gas
  - sign
  - broadcast
  - receipt poll

## Phase 3 - Decimal-specific Modules

Goal: покрыть особенности сети Decimal.

- Token center:
  - create token
  - create reserveless token
  - update details
  - mint/burn
  - buy/sell/convert
- Validator module:
  - validators list
  - validator info
  - delegations
  - rewards, если endpoint доступен
- NFT:
  - DRC721/DRC1155 transfer
  - deploy collection
  - approve/setApprovalForAll
  - NFT delegation/hold/withdraw
- Events/indexer:
  - нормализованные события транзакций
  - stake summary
  - hold timestamps discovery

## Phase 4 - API And Node Integration

Goal: SDK плотно работает с Decimal-compatible API gateway.

- Стандартизировать REST DTO.
- Добавить retries, timeouts, cache TTL.
- Поддержать API base failover.
- Добавить WS client:
  - new blocks
  - pending tx status
  - address tx stream
- Синхронизировать SDK тесты с локальными node/API endpoints.

## Phase 4.5 - Agents, Orchestrator, Monitoring

Goal: сделать SDK управляемым и измеримым.

- Agent API:
  - health check
  - latest block
  - REST latency
  - gas estimate
  - tx build
  - tx broadcast
  - receipt polling
- Orchestrator:
  - parallel checks
  - sequential tx pipeline
  - per-stage timeout
  - stop-on-error mode
  - structured result
- Monitoring:
  - timings per step
  - success/fail counters
  - endpoint health snapshot
  - future Prometheus/OpenTelemetry exporters
- Transaction SLA:
  - target total: 5 seconds
  - build: 1.0s
  - estimate: 1.5s
  - broadcast: 1.5s
  - first receipt/status poll: 1.0s
  - distinguish broadcast SLA from confirmation SLA

Current status:

- Safe REST/RPC client-side rate spacing added.
- REST page limits are clamped.
- WS client added with manual connection and capped subscriptions.
- Live integration tests are opt-in only.

## Phase 5 - CLI

Goal: удобное локальное использование.

Commands:

- `decimal-sdk balance 0x...`
- `decimal-sdk tx 0xhash`
- `decimal-sdk send-del --to ... --amount ... --dry-run`
- `decimal-sdk send-token --token ... --to ... --amount ... --dry-run`
- `decimal-sdk validators`
- `decimal-sdk stakes 0x...`

CLI должен использовать тот же SDK, без отдельной логики.

## Phase 6 - TypeScript SDK

Goal: мобильные приложения, Node.js, React Native.

- Повторить публичный API Python SDK.
- Использовать `ethers` или `viem` для Web3/signing.
- REST/WS слой сделать максимально одинаковым по DTO.
- Выпустить package:
  - `@mintcandy/decimal-sdk`
  - ESM/CJS builds
  - React Native compatibility

## Phase 6.5 - Java SDK

Goal: Android/JVM/Desktop.

- Повторить core DTO:
  - `NetworkConfig`
  - `TransactionPolicy`
  - `AgentResult`
  - `OrchestratorResult`
- HTTP REST client.
- Web3 signing через JVM-compatible Ethereum библиотеку.
- Android-safe storage hooks for private keys, without storing keys by default.

## Phase 7 - Quality Gate

- Unit tests без сети.
- Integration tests против явно заданных testnet/mainnet endpoints.
- Fixtures из реальных tx.
- Golden tests для ABI encoding.
- Security checklist:
  - private key never logged
  - no seed persistence by default
  - explicit broadcast flag
  - transaction preview before send

## Immediate Next Steps

1. Перенести проверенные ABI из backup или `go-smart-node/contracts`.
2. Добавить REST client endpoints из `DecimalApi/server_files/rest_api_server.py`.
3. Реализовать read-only методы `balance`, `token`, `tx`, `blocks`, `validators`.
4. Добавить первые integration tests на явно заданный endpoint через переменные окружения.
5. После read-only стабилизации переносить transaction builders из старого SDK маленькими модулями.
6. Развить `agents/orchestrator/monitoring` до transaction pipeline.
7. Синхронизировать Python, Web JS и Java DTO.
