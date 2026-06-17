# Sources And References

## Local Projects

- `C:\Users\Maximus\PycharmProjects\PythonSDK\backup\legacy_*` - старый Python SDK release, ABI, docs, known errors.
- `C:\Users\Maximus\PycharmProjects\decimal_python_sdk` - более ранний Python SDK, примеры, тесты, minimal SDK.
- `C:\Users\Maximus\PycharmProjects\DecimalApi` - собственные REST/WS/API на базе нод MintCandy.

## Decimal Upstream

Проверены HEAD внешних Bitbucket репозиториев 2026-05-19:

- `decimalteam/dsc-js-sdk`: `f98a4df7ef3fb3053482638845343e0aff69985c`
- `decimalteam/go-smart-node`: `4a97d83eb4ca874eb8b2f09d3b79261ff393f554`
- `decimalteam/dsc-go-sdk`: `3ef4a089b6020889e60783c2026df5725fb960e2`

Официальные Decimal API Swagger docs:

- prod blocks: `https://api.decimalchain.com/api/v1/blocks/docs/index.html`
- prod transactions: `https://api.decimalchain.com/api/v1/txs/docs/index.html`
- prod rewards: `https://api.decimalchain.com/api/v1/rewards/docs/index.html`
- prod coins: `https://api.decimalchain.com/api/v1/coins/docs/index.html`
- prod contracts: `https://api.decimalchain.com/api/v1/contracts/docs/index.html`
- prod NFTs: `https://api.decimalchain.com/api/v1/nfts/docs/index.html`
- prod validators: `https://api.decimalchain.com/api/v1/validators/docs/index.html`
- prod addresses: `https://api.decimalchain.com/api/v1/addresses/docs/index.html`
- testnet uses the same paths under `https://testnet-api.decimalchain.com/api/v1/...`

## What To Reuse

- Из старого Python SDK: ABI, Decimal contract addresses, transaction scenarios, permit/multisend notes, known errors.
- Из DecimalApi: own node endpoints, REST endpoints, address/tx/block/coin/validator API shape.
- Из go-smart-node: authoritative contracts, proto modules, chain behavior, gas/ante rules.
- Из JS/Go SDK: public API naming, transaction builders, signing conventions.
