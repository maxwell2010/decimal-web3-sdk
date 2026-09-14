# Release Status
[Guide](README.md) | [Transaction catalog](../transaction-catalog.json)

Development: 0.1.2.dev0, unpublished. See [new operation checks and limitations](transaction-parity-development.md).
The historical scope/results below describe the published 0.1.1 candidate, not the new development methods.
Neither version is a complete or independently security-audited implementation of every official JS/Go transaction.

## Verified Scope
- 55 high-level entry points: offline request creation from generated mnemonics,
  ABI encoding, gas preflight and local transaction signing with sender recovery.
- Existing allowance/permit/DEL multisend regression tests, memo handling,
  exact amount handling, staking normalization and held-stake reads.
- Official mainnet RPC responded, chain ID 75, system code present. This is
  a read-only deployment check, not proof that every ABI selector works.
- Official testnet RPC did not connect during this check; testnet broadcasts
  and fresh on-chain transaction receipts are NOT verified.
- No production mnemonic was loaded and no network transaction was sent in release QA.

[Mainnet report](../validation/mainnet.json) | [Testnet report](../validation/testnet.json)
| [Offline test environment and results](../validation/offline.json)

Local result: 131 tests passed, lint and compilation passed. One upstream
websockets.legacy deprecation warning remains; it is not a transaction failure.

## Stable-Release Gates
1. Verify current TokenCenter, Delegation, NftCenter, DelegationNFT and
   MasterValidator ABI/method compatibility on each target network.
   NFT defaults are now consistent with the reviewed mainnet profile, but typed
   legacy NFT method variants still need live validation.
2. Complete confirmed transaction testing on an available testnet with minimal
   funds. Offline tests do not prove permissions, economic limits or settlement.
3. Validate approve-dependent workflows after confirmed approval, including
   pending-approval handling and a complete two-step unsigned fee quote.
   A dry-run cannot make allowance exist for the second simulation.
4. Validate nonstandard permit domains and atomic permit routes against actual tokens.
5. Check official REST schemas/routes; facade-specific wallet/staking routes
   require a compatible backend. Stake-page discovery and withdrawal completion
   cannot be inferred from a timestamp or an API delta alone.
6. Audit public-export history separately and configure package ownership/publishing.
   A clean artifact does not sanitize inherited Git history.
7. CI matrix completed: Windows/Ubuntu with Python 3.10, 3.12 and 3.13.
   [All six jobs passed](https://github.com/maxwell2010/decimal-web3-sdk/actions/runs/34864115558).
   macOS and additional architectures remain unverified.

## Official SDK Parity

[Detailed comparison](upstream-parity.md): JS 95, Go 53, Python 55 specialized
EVM write entry points. These are neither unique protocol types nor a coverage
percentage. Differences were found in buy/sell, updateDetails, mintByETH
selectors and NFT routes. Those counterparts are marked partial, not equivalent.
The official SDK has both EVM and legacy Cosmos/protobuf layers.
This package is EVM-first. The following are outside its current high-level coverage:
Safe multisig creation/signing/execution; legacy Cosmos transaction types and
governance; full validator create/remove/meta/penalty administration; stake
complete/penalty helpers; all NFT reserve/reset/complete variants; all exact-in/out
token purchase/sale variants and reserve calculators; verification/IPFS tooling.
Generic contract calls do not turn these into tested high-level workflows.

Reference sources:
[JS SDK](https://bitbucket.org/decimalteam/dsc-js-sdk/src/master/),
[Go SDK](https://bitbucket.org/decimalteam/dsc-go-sdk/src/master/),
[Python SDK](https://bitbucket.org/decimalteam/dsc-python-sdk/src/master/).
The local JS endpoint/EVM interface reference was reviewed; this is not a claim
to have downloaded and executed every current upstream release.
