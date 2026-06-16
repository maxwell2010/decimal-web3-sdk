# Decimal Web JS SDK

Target package: `@mintcandy/decimal-sdk`.

Use cases:

- Browser wallets and dashboards.
- Node.js automation.
- React Native mobile apps.
- Shared DTO with Python SDK.

Performance target:

- Build + estimate + broadcast path should be budgeted for 5 seconds where node latency allows it.
- Confirmation is network-dependent, so SDK reports broadcast time and optional receipt wait separately.

Implemented now:

- `DecimalWeb3Client` for Decimal RPC and aggregated REST.
- Read-only helpers: `health`, `latestBlock`, `blockNumber`, `balanceWei`, `balanceDel`, ERC20 `info`, `balance`, `allowance`.
- Transaction draft helpers for DEL and ERC20 transfer.
- Gas estimate, DEL fee preflight, local signing with `viem/accounts`, optional raw transaction broadcast.
- `AgentOrchestrator` matching the Python orchestration shape.

```bash
npm install
npm run build
```

```ts
import { DecimalWeb3Client } from "@mintcandy/decimal-sdk";

const client = new DecimalWeb3Client();
const block = await client.blockNumber();
const health = await client.health();
```
