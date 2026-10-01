# Changelog

## 0.1.3 - Refreshed 2026-10-01

Maintainer-requested replacement of the existing GitHub preview without a
package version change. The v0.1.3 tag, wheel and sdist are refreshed;
SHA256SUMS changes. Existing 0.1.3 installations need
`--force-reinstall --no-cache-dir` to receive this build. This is not a PyPI upload.

- Read reserve and reserveless token properties through their respective live
  ABI methods. Keep supply, redemption minimum and spendable wallet balance
  distinct; represent every amount exactly without floats.
- Expose actual receipt fees separately from preflight gas budgets and include
  actual fees across multi-step workflows.
- Update testnet NFT staking to the active unified Delegation contract. Confirm
  DRC1155 delegation, stake transfer, withdrawal and both matured completions.
- Confirm testnet one-owner Safe creation and execution plus DEL check creation
  and redemption. Token-check creation still reverts during unsigned preflight;
  validator administration and bridge remain outside live coverage.
- Keep unsupported NFT reset calls explicit, and add check-hash extraction plus
  mnemonic-based redemption signing. No mainnet transaction was broadcast for
  this refresh.

## 0.1.3 - 2026-09-24

- Reconcile current reserved NFT collection creation with the six-field metadata
  tuple and createDRC721/createDRC1155, and native-reserve mint with mintByDEL.
- Add unsigned creation/mint preparation, registered collection/reserve reads and
  NFTCreated decoding without assuming that a collection creation mints an NFT.
- Validate exact per-copy reserve minimums and existing DRC1155 reserve type,
  token and total rate. Approval and mint remain separate, explicit operations.
- Generate the shared Console NFT profile from the same reviewed ABI snapshots.
  The legacy URI setter now requires opt-in; it is absent from current NFT ABIs.
- Resolve current testnet TokenCenter, Delegation, NFTCenter and related system
  addresses from the public contract registry and verified on-chain code.
- Match testnet token symbol rules, creation reserve tiers and live mint/update
  selectors. Return both transaction references and total estimated fee when
  changing token identity and maximum supply.
- Prefer one-transaction permit routes; avoid implicit approve transactions by
  default and require receipt waiting for explicitly requested two-step sends.
- Confirm testnet DEL memo and multisend, token creation, transfer, allowance,
  permit multisend, buy/sell/convert, staking requests and NFT721/1155 lifecycles.
  Pending stake unbond/transfer is distinguished from final settlement.
- Keep unverified methods clearly identified in the validation report. No
  mainnet broadcasts were performed for this release.

## 0.1.2 - Refreshed 2026-09-16

Maintainer-requested replacement of the existing GitHub preview, without a package
version change. The v0.1.2 tag and wheel/sdist are refreshed; SHA256SUMS changes.
Existing 0.1.2 installations need --force-reinstall --no-cache-dir to receive this
build. Releases v0.1 and v0.1.1 remain unchanged. This is not a PyPI upload.

- Reuse seven mined mainnet examples in offline calldata/receipt regressions,
  separating SDK sends from multisend-service and external protocol references.
  Cover direct native memo, native multisend, withdrawWithReset, ERC20 transfer,
  approve, and multisend through allowance, approve and permit routes.
- Do not report an EIP-1559 fee ceiling as the actual fee when effectiveGasPrice
  is absent. Keep actual fee fields unknown while preserving the successful
  receipt status, hash and block. Fixed-price legacy/access-list fallback remains.
- Avoid nested HTTP retries inside RpcPool so an unavailable endpoint does not
  silently multiply the configured request timeout before fallback.
- Rebind ERC20, fungible staking, validator, NFT ownership/approval, checks nonce and token
  lookup reads to the selected RPC on each failover attempt. Preserve explicit
  historical block identifiers for stake reads.
- Add an opt-in unsigned wallet preflight script with dedicated mnemonic/address
  validation, a read-only RPC allowlist and redacted error reports. No broadcast
  or signing mode is exposed by the script.
- Add a separate opt-in, budget-limited self-transfer runner. Validate the wallet,
  network, nonce and payload before every signature, including fee retries; journal
  transaction hashes before broadcast and reconcile receipts before resuming.
- Confirm four authorized mainnet self-transfers with fee and balance reconciliation.
  Testnet remains unavailable from the validation environment; broader live coverage
  is still incomplete. Detailed limits are recorded in the bilingual status guides.

## 0.1.2 - 2026-09-15

GitHub preview in the 0.1 series. New operations have offline coverage; live
transaction and ABI limitations remain documented. This is not a stable-parity claim.

- Add a permanent GitHub requirements URL for pip install/upgrade of the latest
  published preview. Each update points to an immutable versioned wheel.
- Keep authored documentation punctuation to ASCII hyphens and enforce it in tests.

- Use certifi for SDK-owned REST/WSS TLS trust, with explicit custom CA configuration
  shared with RPC. Keep certificate and hostname verification enabled; do not mutate
  the Windows trust store or retry insecurely on certificate failures.
- Add 23 typed methods covering the 24 previously missing JS operations; reserveless
  NFT collection variants share one method. Add the NFT feature-branch batch hold reset.
- Add fee-only preparation for every new operation, without signing or approvals.
- Add weighted Safe creation, EIP-712 signatures, on-chain tuple approvals, execution
  simulation, nonce/weight validation and inner receipt outcome checks.
- Add exact NFT stake/frozen-stake reads and current four-field frozen state decoding.
- Correct the testnet delegation-nft target from the official NFT feature branch.
- Bundle minimal, source-attributed API ABI fragments. Keep three legacy methods
  disabled unless explicitly opted in; do not claim full JS or live network parity.
- Add bilingual examples, independent calldata/precision tests and read-only RPC checks.
- No funded credentials or network broadcasts during release verification.

## 0.1.1

GitHub prerelease in the 0.1 series. The existing v0.1 / package 0.1.0 is unchanged.
Not published to PyPI. Known ABI differences prevent a full parity/stable claim.

- Version-pinned GitHub wheel and source-archive installation without Git.
- Mainnet is the default for both the Python client and CLI; testnet remains explicit.
- Source-pinned comparison: JS 95, Go 53, Python 55 specialized EVM write methods.
  Counts are API entry points, not unique protocol transaction types or live coverage.

- Bilingual, module-based guides, generated API signatures and complete examples
  for all 55 high-level transaction entry points.
- Offline transaction encoding/signing checks; no production transfers in release QA.
- Exact native/token/fee amounts independent of the global Decimal precision.
- Amount helpers now reject floats, booleans, non-finite values and fractional
  decimal counts. Use strings or Decimal. This is a deliberate compatibility change.
- Private keys and mnemonics hidden from dataclass repr.
- Pending nonce lookup, RPC chain validation and fail-closed contract code checks.
- Receipt RPC failures no longer appear as a missing/pending transaction.
- Withdrawal history distinguishes maturity from confirmed completion; estimated
  completion dates and unknown token raw units are explicitly identified.
- Official Decimal RPC defaults, explicit custom-network configuration, MIT license
  with preserved third-party notice, artifact checks and installation verification.

See [English limitations](docs/en/status.md) or [ограничения на русском](docs/ru/status.md)
before using contract-dependent operations. This is not complete JS/Go SDK parity.
