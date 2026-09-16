# Decimal Web3 SDK 0.1.2

GitHub preview in the 0.1 series. Python 3.10+, MIT, Windows/Linux support.
[Russian notes](https://github.com/maxwell2010/decimal-web3-sdk/blob/v0.1.2/docs/ru/release-0.1.2.md)

## Same-Version Refresh, 2026-09-16
At the maintainer's request the existing v0.1.2 tag, wheel and sdist are updated;
the package version stays 0.1.2. Checksums change. This remains a preview.
- Fix nested HTTP retries and rebind contract reads to the selected fallback RPC.
- Do not report a type-2 fee ceiling as an actual charge. Without a reliable
  effectiveGasPrice the actual fee remains unknown while confirmed success is preserved.
- Add 41 regression tests using seven mined examples and a shared evidence register.
- Add separate opt-in unsigned wallet preflight and budget-limited self-transfer
  tools. Installing the package never sends a transaction.
- Include JSON test fixtures in the sdist; exclude funded credentials and local reports.

If 0.1.2 is already installed, --upgrade alone may skip it. Refresh without pip's cache:
```shell
python -m pip install --force-reinstall --no-cache-dir "https://github.com/maxwell2010/decimal-web3-sdk/releases/download/v0.1.2/decimal_web3_sdk-0.1.2-py3-none-any.whl"
python -m pip check
```
For reproducibility retain the wheel and its checksum from SHA256SUMS.

## Changes
- Fix verified HTTPS/WSS trust with certifi. Private CA files remain configurable;
  certificate and hostname checks are never disabled by the SDK fix.
- Add 24 typed methods for weighted Safe, NFT staking, validators, tokens and staking.
  The catalog now contains 79 high-level transaction entry points.
- Preserve exact amounts and unsigned fee preparation before local signing.
- Update English/Russian documentation, installation requirements and SDK comparison.
- Add a permanent pip update manifest and tests preventing long dash punctuation.

## Install Or Update
No Git or GitHub login required:
```shell
python -m pip install --upgrade -r "https://raw.githubusercontent.com/maxwell2010/decimal-web3-sdk/main/requirements-latest.txt"
```
This opts into the latest published preview. Updates occur only when the command runs.
The manifest follows published versioned wheels, not unreleased source changes.

For a new installation of this version:
```shell
python -m pip install "https://github.com/maxwell2010/decimal-web3-sdk/releases/download/v0.1.2/decimal_web3_sdk-0.1.2-py3-none-any.whl"
```

## Verification And Limits
329 local offline tests pass. Lint, reference generation,
source/artifact audits and wheel/sdist checks are release gates. Four separately
authorized mainnet self-transfer tests were confirmed, costing 0.159548649975 DEL;
earlier successful operations are recorded separately in the evidence register.
No new signing or broadcasts were performed for building/publishing this refresh.
The testnet read recheck timed out; not every endpoint was checked. Complete NFT,
Safe, validator administration and other lifecycles remain unverified on-chain.
Three legacy methods require opt-in; existing partial ABI/permit differences
remain. This is not a stable/full-parity release or a PyPI publication.

[Current limitations](https://github.com/maxwell2010/decimal-web3-sdk/blob/v0.1.2/docs/en/status.md)
| [CI](https://github.com/maxwell2010/decimal-web3-sdk/actions/workflows/ci.yml)
| [Documentation](https://github.com/maxwell2010/decimal-web3-sdk/blob/v0.1.2/docs/en/README.md)

By [MintCandy](https://mintcandy.ru/) and [@Maxwell2019](https://t.me/Maxwell2019).
Releases v0.1 and v0.1.1 remain unchanged. Refreshed v0.1.2 artifacts have new SHA256SUMS.
