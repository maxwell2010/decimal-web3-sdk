# Decimal SDK Status Report

Дата: 2026-06-16

## Кратко

Python SDK уже покрывает основной Decimal EVM/Web3 слой: Web3 RPC, REST facade, WS client, транзакции DEL/ERC20, fee preflight, staking/token/NFT workflows, CLI, agents/orchestrator/monitoring и training harness.

Перед публичным релизом SDK отвязан от приватных MintCandy endpoint-ов: дефолтные mainnet/testnet/devnet endpoint-ы взяты из официального `dsc-js-sdk`, а пользователь может заменить их своими Decimal node/API URL.

## Реализовано

- `NetworkConfig.mainnet()`, `NetworkConfig.testnet()`, `NetworkConfig.devnet()`, `NetworkConfig.custom()`.
- Web3 RPC pool с failover по списку URL.
- `contract_code()` / `contract_code_exists()` для диагностики системных и пользовательских контрактов выбранной сети.
- REST client для block/tx/address/balance/coin/validator/reward endpoints.
- WS client с явным подключением.
- Wallet helpers для seed phrase -> private key -> EVM address, приватного ключа и checksum-адресов.
- DEL transfer.
- Generic contract call.
- ERC20 transfer/approve.
- ERC20 transferFrom with owner balance and spender allowance preflight.
- Gas estimate.
- 10% gas-limit buffer после `estimateGas`, как в Decimal Go SDK.
- Отдельный расчет комиссии `calculate_fee(...)`/`estimate_fee_for_*` до подписи.
- Fee preflight до подписи и broadcast во всех send/workflow путях.
- Contract-call с calldata блокируется до подписи, если целевой адрес в выбранной сети не содержит bytecode.
- Пользовательские сообщения ошибок без технических RPC-параметров.
- Memo capability matrix: DEL transfer поддерживает UTF-8 memo в tx `data`; DEL multisend поддерживает одно memo на batch через финальный zero-value call к `0x0`; ERC20/contract/staking/token/NFT/checks/bridge не имеют универсального memo.
- ERC20 balance preflight.
- Decimal service:
  - delegate DEL;
  - hold DEL;
  - unbond DEL;
  - withdraw hold DEL;
  - multisend DEL;
  - delegate ERC20;
  - hold ERC20;
  - unbond ERC20;
  - withdraw hold ERC20;
  - multisend ERC20;
  - permit-first / approve fallback.
  - stake transfer/redelegate;
  - stake hold/reset and with-reset helpers.
- Token Center:
  - buy;
  - sell;
  - convert;
  - burn;
  - mint;
  - update details;
  - create token;
  - create reservless token;
  - расчет обязательного резерва создания токена по правилам Decimal Go SDK.
- NFT service:
  - ERC721/ERC1155 create collection;
  - mint;
  - transfer;
  - set approval for all;
  - delegate;
  - hold;
  - transfer stake;
  - withdraw;
  - burn;
  - ERC721 single-token approve.
- Checks service:
  - create DEL checks;
  - create token checks;
  - redeem checks.
- Bridge service:
  - native transfer;
  - token transfer;
  - complete transfer.
- CLI.
- Agents/orchestrator.
- Monitoring snapshot.
- Training harness with CSV journal.
- Training harness defaults to testnet, calculates preflight fee before signing/sending, and records balance/nonce before/after only for visual test reporting.
- Web JS and Java package skeletons remain in the repository, but Python is the release reference.
- Documentation flow is aligned with the official legacy Decimal Python SDK style: wallet/request, fee calculation, signing, broadcast, result inspection.

## Проверки

Unit tests:

```text
160 passed, 2 skipped
```

Package checks:

```text
python -m build -> OK
python -m twine check dist\* -> OK
```

Mainnet public Web3 smoke:

```text
https://node.decimalchain.com/web3/ -> eth_chainId = 0x4b
```

Testnet/devnet:

- `NetworkConfig.testnet()` uses official Decimal testnet Web3 by default and can be overridden with custom Decimal-compatible RPC endpoints;
- smoke checked through SDK on chain id `202020`;
- funded test wallet balance read successfully;
- `wait_receipt=True` uses configurable receipt wait defaults `7s` timeout / `3s` poll;
- dry-run `send_del` from mnemonic with memo: OK, gas estimated;
- dry-run `multisend_del` from mnemonic with memo: OK, gas estimated;
- live `send_del` self-transfer on testnet confirmed:
  - hash `807320c65fdfe97c6bf348bb0eaa5a6da8867e1a0f560deab7e03170e6379501`;
  - block `20785269`;
  - receipt status `1`;
  - gas used `21000`;
  - balance after check `999948.7177595883 tDEL`;
  - nonce after check `3`.
- live `multisend_del` self-transfer with memo on testnet confirmed:
  - hash `40e681c38d36a88b3488c179b66ca55ccbdaef45fe020e993473604cd656b65e`;
  - block `20785359`;
  - receipt status `1`;
  - preflight fee `20.007760882352924538 tDEL`;
  - effective fee `18.188590588235278992 tDEL`;
  - memo `sdk multisend memo test`;
  - balance after check `999930.529168 tDEL`;
  - nonce after check `4`.
- live `create_reserveless_token` on testnet confirmed:
  - this entry is now classified as an invalid no-op system-contract test, not a real token creation;
  - symbol `SDKQAZ`;
  - hash `fda34fac18f557fc57b4ea5ccd64474d258c56b6a49ee0cc5c1a5f68fca866e4`;
  - block `20785435`;
  - receipt status `1`, but target TokenCenter address had no bytecode and receipt logs were empty;
  - gas used `23352`;
  - preflight fee `19.987530588235277496 tDEL`;
  - balance after check `999912.359251529411837588 tDEL`;
  - nonce after check `5`.
- after adding bytecode preflight, the same class of transaction is blocked before signing/broadcast:
  - user message `Контракт сети недоступен. Проверьте сеть или адрес контракта.`;
  - `tx_hash=None`;
  - balance before/after `999894.08662741176479396 tDEL`;
  - nonce before/after `6`.
- current test wallet balance after all live checks: `999894.08662741176479396 tDEL`.
- tx-reader sample corpus created in `reports/tx_reader_samples`:
  - `native_del_transfer`;
  - `multisend_del` with decoded aggregate calls and memo;
  - `create_reserveless_token` with decoded TokenCenter args.
- full live broadcast matrix still requires `DECIMAL_TEST_BROADCAST=1` and minimal test amounts for the remaining transaction types.
- testnet TokenCenter/delegation/master-validator addresses require working ContractCenter/subgraph/API discovery; public Decimal API/subgraph returned `403` from this environment.
- Live broadcast not confirmed yet for TokenCenter, ERC20 workflows, staking, NFT, checks, bridge, and validator admin flows. Unit/dry-run coverage exists, but live testnet broadcast is blocked until real testnet system contract addresses and safe parameters are available.

Approve/permit behavior:

- ERC20 delegate/hold and ERC20 multisend try one-transaction permit flows first.
- If permit is unavailable and allowance is low, SDK reports `requires_secondary_transaction=True` and runs approve + action.
- Token convert follows official JS/Go SDK behavior: approve token center first, then convert. No public `convertByPermit` method was found in the scanned official SDKs.

## Что не хватает

- Полная live broadcast матрица на testnet/devnet:
  - DEL transfer;
  - ERC20 transfer;
  - ERC20 approve;
  - token buy/sell/convert;
  - delegate/unbond/withdraw;
  - multisend;
  - NFT create/mint/transfer/delegate;
  - checks DEL/token/redeem;
  - bridge native/token/complete.
- Typed REST DTO вместо сырых `dict[str, Any]` для части read-only ответов.
- Стабильный read-only staking summary зависит от API-gateway. В SDK есть транзакционный staking workflow, но чтение агрегированных делегаций должно приходить от выбранного API.
- Safe-style multisig helpers.
- Legacy Cosmos/protobuf compatibility layer.
- Нужна отдельная публикация wheel/sdist в PyPI или приватный package registry.
- Нужна security note для production key management.

## Релизные решения

- Лицензия: MIT.
- Package name: `decimal-web3-sdk`.
- Python: `>=3.10`.
- Maintainer/project links:
  - `@Maxwell2019`;
  - https://mintcandy.ru/.
- Приватные endpoint-карты вынесены из публичной документации в `backup/release_private_docs`.

## Следующие шаги

1. Прогнать `pytest -q`.
2. Прогнать `DECIMAL_SDK_RUN_INTEGRATION=1 pytest -q tests/integration` с рабочими endpoint-ами.
3. На testnet/devnet запустить training harness с `DECIMAL_TEST_BROADCAST=0`, затем с `1`.
4. Собрать `python -m build`.
5. Проверить wheel установкой в чистое virtualenv.
6. После testnet broadcast matrix поднять версию до `0.2.0` или `1.0.0rc1`.
