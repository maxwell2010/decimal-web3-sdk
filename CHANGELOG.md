# Changelog

## 0.1.2.dev0 (Unreleased)

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
- No release publication, funded credentials or network broadcasts during this work.

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
