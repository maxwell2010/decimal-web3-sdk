# Decimal SDK Status Report

Дата: 2026-06-13

## Кратко

Python SDK уже покрывает основной Decimal EVM/Web3 слой: Web3 RPC, REST facade, WS client, транзакции DEL/ERC20, fee preflight, staking/token/NFT workflows, CLI, agents/orchestrator/monitoring и training harness.

Перед публичным релизом SDK отвязан от приватных MintCandy endpoint-ов: дефолтные mainnet/testnet/devnet endpoint-ы взяты из официального `dsc-js-sdk`, а пользователь может заменить их своими Decimal node/API URL.

## Реализовано

- `NetworkConfig.mainnet()`, `NetworkConfig.testnet()`, `NetworkConfig.devnet()`, `NetworkConfig.custom()`.
- Web3 RPC pool с failover по списку URL.
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
- Web JS and Java package skeletons remain in the repository, but Python is the release reference.

## Проверки

Unit tests:

```text
96 passed, 2 skipped
```

Mainnet public Web3 smoke:

```text
https://node.decimalchain.com/web3/ -> eth_chainId = 0x4b
```

Testnet/devnet:

- public testnet/devnet endpoints are not hardcoded;
- use `DECIMAL_TESTNET_*` variables or `NetworkConfig.custom(...)`;
- broadcast tests require an explicitly funded test wallet and `DECIMAL_TEST_BROADCAST=1`.

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
- `from_mnemonic(...)` constructors for high-level staking/token/NFT/checks/bridge workflow request classes. Core DEL/ERC20/contract transaction requests already support mnemonic constructors.
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
