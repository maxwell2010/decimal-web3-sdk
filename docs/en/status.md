# Release Status
[Guide](README.md) | [Transaction catalog](../transaction-catalog.json)

Version **0.1.2**, GitHub preview. This is not a stable, full-parity or independently
security-audited replacement for the official JS/Go SDKs.

## Verified Scope
- 79 high-level transaction entry points with offline request construction,
  ABI encoding, unsigned fee preparation and/or local signing coverage.
- 24 new Python methods: weighted Safe, NFT reset/withdraw/transfer/complete,
  validator administration, exact token operations and additional staking helpers.
- Exact integer/Decimal amounts, memo, DEL/ERC20 multisend and allowance/permit regressions.
- REST/WSS certificate validation using certifi or explicit custom CAs. Expired,
  untrusted and wrong-host certificates are rejected, without insecure fallback.
- Official mainnet RPC read checks, including contract code and NFT freeze times.
  These do not prove that every ABI method executes successfully.
- Verified HTTPS to Decimal IPFS returned HTTP 404 at the root. This verifies TLS,
  not an upload, pinning or WebSocket round-trip.
- Package build/offline QA does not load funded credentials or broadcast. The
  separately authorized mainnet checks are listed below; they are not repeated for publishing.

[Operation and TLS validation](../validation/transaction-parity-development.json)
| [Detailed development results](transaction-parity-development.md)
| [Release CI runs](https://github.com/maxwell2010/decimal-web3-sdk/actions/workflows/ci.yml)

The 225-test operation stage and 242-test TLS stage are historical checkpoints;
the final release suite also checks the latest manifest and documentation typography.
One upstream websockets.legacy deprecation warning remains.
CI targets Windows/Ubuntu on Python 3.10, 3.12 and 3.13. macOS and additional
architectures are not verified. Inspect the CI run for the release commit.

## Post-Release Validation, 2026-09-16

The working branch included in the 0.1.2 refresh confirmed four authorized mainnet transactions:
native DEL, native DEL with a direct UTF-8 memo, two-row native DEL multisend with
memo, and an ERC20 transfer. All recipients were the sender's own address.
Native multisend required no approve. The ERC20 Transfer event and unchanged token
balance were checked; the DEL balance decrease matched the total receipt fees.

| Operation | Estimated gas | Used gas | Actual fee, DEL |
| --- | ---: | ---: | ---: |
| DEL self-transfer | 21000 | 21000 | 0.024999975 |
| DEL self-transfer with memo | 21496 | 21496 | 0.0255904506 |
| DEL multisend, two self-address rows | 46614 | 46614 | 0.05549280165 |
| ERC20 self-transfer | 45119 | 44911 | 0.053465422725 |

These transactions used 1190.475 gwei from the network, not a fixed gas-price cap.
Total actual cost: 0.159548649975 DEL, within the approved 0.25 DEL test block.
An estimate is not a fixed quote; the gas-limit buffer is not the gas actually used.
Legacy receipts omitted effectiveGasPrice; the confirmed transaction's gasPrice
was used for reconciliation. This fallback must not use an EIP-1559 maximum fee.

The testnet read recheck timed out. No testnet balance or new testnet receipts are
claimed. This is not evidence that every testnet endpoint is unavailable.
These four cases do not verify different-recipient multisend, ERC20 multisend,
permit, staking, NFT, Safe or validator lifecycles. The 2026-09-16 refresh includes
RPC failover and receipt-fee fixes, with 329 offline tests passing locally.

## Earlier Validation

The [shared evidence register](../validation/transaction-evidence.md) includes
earlier testnet DEL, mainnet direct DEL with memo and mainnet DEL withdrawWithReset.
Do not repeat them just to populate a new report. Including the September 16 run,
seven successful SDK receipts cover five scenario variants, not seven distinct
methods or complete SDK coverage.

Earlier service approve/multisend and an external permit/multisend transaction are
also confirmed protocol references, not current Python SDK end-to-end sends.
The historical token creation was a no-op; the historical testnet multisend has
conflicting execution evidence and is not counted as a proven contract operation.
Further checks start with history, read-only inspection and offline regression
tests, avoiding routine paid repeats of already verified scenarios.

## Stable-Release Gates
1. Verify contract ABI compatibility and successful settlement on every target network.
   New operations have not been broadcast in this release preparation. Official
   testnet was unavailable during read checks; no new testnet receipts are claimed.
2. Test approval-dependent workflows, nonstandard permit domains and atomic routes
   with compatible deployed tokens. Unsigned simulation cannot create allowance.
3. Confirm indexed API schemas, complete wallet/stake discovery and withdrawal queues.
   API deltas and timestamps alone do not prove withdrawable stake.
4. Three legacy methods remain opt-in and absent from inspected current ABIs:
   token.update_min_supply, decimal.apply_stake_penalty, decimal.apply_stake_penalties.
5. Current reserveless NFT metadata uses refundable, not the older JS allowMint flag.
   Pre-existing partial selectors and permit variants still need reconciliation.

## Official SDK Parity
[Detailed comparison](upstream-parity.md): **JS 95 / Go 53 / Python 79** specialized
EVM write entry points. Counts are neither unique protocol transaction types nor
a parity percentage. Some counterparts remain partial despite having a typed method.

Legacy Cosmos/protobuf/governance, mixed-asset multisend, all permit variants,
reserve calculators and full verification/IPFS tooling are not complete SDK features.
Safe and the new NFT/validator helpers now have offline coverage, not live assurance.

Reference sources: [JS SDK](https://bitbucket.org/decimalteam/dsc-js-sdk/src/master/),
[Go SDK](https://bitbucket.org/decimalteam/dsc-go-sdk/src/master/),
[Python SDK](https://bitbucket.org/decimalteam/dsc-python-sdk/src/master/).
Pinned upstream source snapshots are parsed, never executed by the comparison tool.
