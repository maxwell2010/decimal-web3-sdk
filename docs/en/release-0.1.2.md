# Decimal Web3 SDK 0.1.2

GitHub preview in the 0.1 series. Python 3.10+, MIT, Windows/Linux support.
[Russian notes](https://github.com/maxwell2010/decimal-web3-sdk/blob/v0.1.2/docs/ru/release-0.1.2.md)

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

Pin this version for reproducibility:
```shell
python -m pip install "https://github.com/maxwell2010/decimal-web3-sdk/releases/download/v0.1.2/decimal_web3_sdk-0.1.2-py3-none-any.whl"
```

## Verification And Limits
244 local offline tests pass, including 17 TLS tests. Lint, reference generation,
source/artifact audits and wheel/sdist checks are release gates. No funded credentials
were loaded and no transaction was broadcast. Official mainnet and IPFS HTTPS checks
were read-only; testnet was unavailable. New on-chain transaction settlement remains
unverified. Three legacy methods require opt-in; existing partial ABI/permit differences
remain. This is not a stable/full-parity release or a PyPI publication.

[Current limitations](https://github.com/maxwell2010/decimal-web3-sdk/blob/v0.1.2/docs/en/status.md)
| [CI](https://github.com/maxwell2010/decimal-web3-sdk/actions/workflows/ci.yml)
| [Documentation](https://github.com/maxwell2010/decimal-web3-sdk/blob/v0.1.2/docs/en/README.md)

By [MintCandy](https://mintcandy.ru/) and [@Maxwell2019](https://t.me/Maxwell2019).
Older releases remain unchanged. SHA256SUMS accompanies the versioned artifacts.
