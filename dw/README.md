# CandyWallet Mobile

Android-first mobile wallet for Decimal built on Expo/React Native.

## Goals

- Beautiful dark UI inspired by the existing Decimal wallet, but denser and clearer.
- Import/generate wallet, PIN and biometric gate.
- Assets, send/receive, token conversion, staking, settings.
- QR receive payloads include address, selected token and optional amount, so a QR can be a real payment request.
- Uses our Decimal API/RPC endpoints and will align with the SDK modules in `packages/`.
- Staking summary is loaded first from the public read-only endpoint `https://api.mintcandy.ru/v1/wallets/{0x}/staking`, then falls back to node endpoints.
- Asset balances are loaded through the fast indexed MintCandy API, not through client-side mass `balanceOf` calls.

## API Endpoints

Полная карта endpoint-ов: [../docs/MINTCANDY_API_ENDPOINTS.md](C:/Users/Maximus/PycharmProjects/PythonSDK/docs/MINTCANDY_API_ENDPOINTS.md).

Assets:

```http
GET https://node2.mintcandy.ru/mc-api/v1/erc20/balances/{0x_address}?limit=300&offset=0&include_bank=1&prefer_bank=1
```

Fallback:

```http
GET https://node1.mintcandy.ru/mc-api/v1/erc20/balances/{0x_address}?limit=300&offset=0&include_bank=1&prefer_bank=1
```

This response contains:

- native `DEL`;
- Decimal custom coin balances from the bank module;
- indexed DRC20/ERC20 contract balances;
- exact `balance_raw` values and formatted `balance` strings.

The mobile app must not use slow `live=1`, `symbols=all`, or `erc20_limit=1600` requests during wallet opening. If both APIs fail, the app displays cached assets from local storage.

Staking:

```http
GET https://api.mintcandy.ru/v1/wallets/{0x_address}/staking
```

Transactions:

```http
GET https://node2.mintcandy.ru/mc-api/v1/addresses/{0x_address}/txs?limit=100
```

Coins/prices:

```http
GET https://node2.mintcandy.ru/mc-api/v1/coins
GET https://node2.mintcandy.ru/mc-api/v1/coins/{denom}
GET https://api.mintcandy.ru/v1/market/del
```

## Run

```bash
npm install
npm run start
```

If Metro/Expo is already running and does not pick up API changes, restart it with cache reset:

```bash
npx expo start -c
```

Android:

```bash
npm run android
```
