# Web JS SDK

Package: `@mintcandy/decimal-sdk`.

Path:

```text
packages/web-js
```

## Назначение

Web JS SDK нужен для:

- браузерных Decimal-интеграций;
- Node.js приложений;
- React Native/Mobile shared logic;
- будущего CandyWallet transaction layer.

SDK использует `viem` и настраиваемые Decimal RPC/REST endpoints.

## Установка

Из папки пакета:

```powershell
cd packages\web-js
npm install
npm run build
```

Локальное использование в другом проекте:

```powershell
npm install ..\packages\web-js
```

или после публикации:

```powershell
npm install @mintcandy/decimal-sdk
```

## Быстрая проверка

```powershell
cd packages\web-js
npm install
npm run build
```

Сборка создает:

```text
dist/index.js
dist/index.d.ts
```

## Базовое использование

```ts
import { DecimalWeb3Client } from "@mintcandy/decimal-sdk";

const client = new DecimalWeb3Client();

const block = await client.blockNumber();
const health = await client.health();
const balance = await client.balanceDel("0x...");
```

## Network config

```ts
import { DecimalWeb3Client, mainnetConfig } from "@mintcandy/decimal-sdk";

const config = mainnetConfig();
const client = new DecimalWeb3Client(config);
```

Default Web3 endpoint:

- `https://node.decimalchain.com/web3/`

REST/API endpoint-ы для production передаются явно через config.

## Read-only методы

```ts
await client.health();
await client.latestBlock();
await client.blockNumber();
await client.balanceWei("0x...");
await client.balanceDel("0x...");
await client.erc20Info("0xToken");
await client.erc20Balance("0xToken", "0xOwner");
await client.erc20Allowance("0xToken", "0xOwner", "0xSpender");
```

## Transaction draft

```ts
const draft = await client.buildNativeTransfer({
  privateKey: "0x...",
  to: "0xRecipient",
  amountDel: "0.1",
});

const result = await client.sendDraft(draft, "0x...", false);
console.log(result.success, result.feeDel, result.rawTx);
```

`broadcast=false` делает dry-run: строит, оценивает, проверяет fee preflight и подписывает локально, но не отправляет.

## ERC20 transfer

```ts
const draft = await client.buildErc20Transfer({
  privateKey: "0x...",
  token: "0xToken",
  to: "0xRecipient",
  amountRaw: 1000000000000000000n,
});

const result = await client.sendDraft(draft, "0x...", false);
```

## Fee preflight

```ts
const estimated = await client.estimate(draft);
const preflight = await client.preflightFee(estimated);

if (!preflight.ok) {
  console.log(preflight.missingWei);
}
```

## Agents

```ts
import { AgentOrchestrator, fastTransactionPolicy } from "@mintcandy/decimal-sdk";

const orchestrator = new AgentOrchestrator([
  {
    name: "custom",
    async run(context) {
      return { name: "custom", success: true, payload: context.data };
    },
  },
]);

const result = await orchestrator.runParallel({
  client,
  data: {},
  policy: fastTransactionPolicy(),
});
```

## Текущий статус

Готово:

- `DecimalWeb3Client`.
- RPC/REST reads.
- ERC20 info/balance/allowance.
- DEL and ERC20 transaction draft.
- Gas estimate.
- Fee preflight.
- Local signing.
- Optional raw transaction broadcast.
- Agent orchestrator.

Осталось:

- parity со всеми Python workflows;
- Token Center helpers;
- NFT helpers;
- React Native storage/key management adapters;
- browser wallet provider adapter.
