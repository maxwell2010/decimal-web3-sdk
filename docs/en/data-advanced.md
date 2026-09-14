# Data and Advanced APIs
[Guide](README.md) | [API index](api.md)

## Data Access
DecimalClient provides block_number, balance_wei/balance_del, transaction_count
(pending nonce), gas_price, estimate_gas, contract_code and transaction_receipt.
Read methods do not require a signer. contract_code_exists only tests code
presence, not ABI compatibility. receipt None means not found, not an RPC outage.

RestClient offers block/block_txs, tx/txs, address/address_full/address_txs,
wallet_balances, coins/coin/coin_registry/coin_prices, validators/validator,
validator_delegations, rewards_delegator and wallet staking/withdrawal methods.
Page clamps limit/offset to configured safety bounds; one page is not the entire
network. Coin registry can be bounded too: do not label a limited list complete.
Raw REST results follow the server schema and are not universally normalized.

Some REST routes, notably /evm/wallet/... and normalized staking, were developed
against a compatible facade and are not guaranteed on every official microservice.
NetworkConfig API overrides select a compatible deployment without changing RPC.
Never replace an unavailable response with an empty balance.
_json_loads_exact preserves JSON decimal precision internally.

## WebSocket
DecimalWsClient supports connect/close, subscribe/unsubscribe and receive_once.
It uses Tendermint-style JSON-RPC subscriptions, not an Ethereum eth_subscribe
adapter. Configure an appropriate WS URL explicitly. WsMessage contains method
and params. SafetyLimits controls subscription/rate limits, not service availability.
Use finally/async context to close sessions.

## CLI
```shell
decimal-sdk --help
decimal-sdk --network testnet block-number
decimal-sdk wallet-sequence
decimal-sdk wallet-from-mnemonic
```

CLI defaults to mainnet, like DecimalClient(). Select --network testnet explicitly for tests.
Wallet commands can prompt for a mnemonic locally without shell-history exposure.
Normal transaction commands also prompt when --private-key is omitted.
--account-index selects the transaction signing account. Technical key arguments
remain for compatibility but are discouraged. wallet-generate intentionally emits
new recovery material; protect stdout. wallet-from-mnemonic hides keys by default.

## Optional Compatibility Utilities
- AbiRegistry loads a caller-supplied JSON ABI; no downloaded remote code is executed.
- TransactionPolicy, DecimalMonitor and AgentOrchestrator organize bounded health,
  latency, receipt and transaction steps. AgentContext.data is caller-owned and
  may contain secrets; do not log it.
- The transaction agents build, estimate, sign, broadcast and poll separately.
  Adding BroadcastTransactionAgent really sends transactions.
- telemetry collects durations/metrics; use it without confidential payloads.
- test_harness/TxTrainingJournal is an opt-in local QA utility retained for API
  compatibility. It uses separate network-scoped environment settings, not the
  CLI --network flag. Default broadcast is disabled; real tests require explicit
  funded-wallet configuration and expected-address validation.
- candy_protocol is a mainnet-only unsigned compatibility adapter. It reads the
  bundled allowlisted profile and supports contract-call and native/token burn
  construction. This is not the mobile wallet and does not include an app server.

Exact signatures and optional/default fields for every utility are in the
[generated reference](api.md). Legacy framework helpers are not required to send
a normal Decimal transaction.
