# Decimal Web3 SDK

Independent Decimal EVM SDK by [MintCandy](https://mintcandy.ru/) and
[@Maxwell2019](https://t.me/Maxwell2019). MIT license, Python 3.10+.
Package: `decimal-web3-sdk`; import: `decimal_web3_sdk`.

**Version 0.1.2 is a GitHub preview, not a stable/full-parity release.**
79 high-level transaction entry points have offline encoding/signing coverage, not full live parity.
New methods, legacy limitations and the updated NFT sources are described in the
[development notes](docs/en/transaction-parity-development.md).
[Official SDK comparison](docs/en/upstream-parity.md): JS 95 / Go 53 / Python 79 specialized EVM write entry points, not a parity percentage.

[Русский README](README.ru.md) | [English guide](docs/en/README.md) | [Русская документация](docs/ru/README.md)

## Install Without Git

Requires Python 3.10+ and pip. Runtime dependencies install automatically:
web3, eth-account, aiohttp, certifi and python-dotenv, plus their dependencies.
[OS support and installation requirements](docs/en/install.md).

Install or upgrade to the latest published preview using the same command each time:
```shell
python -m pip install --upgrade -r "https://raw.githubusercontent.com/maxwell2010/decimal-web3-sdk/main/requirements-latest.txt"
```

The manifest points to a versioned GitHub release wheel and changes with each
reviewed release. It includes previews. Updates happen only when you run the
command, never automatically inside the SDK. Git and GitHub login are not required.

For this release's wheel:
```shell
python -m pip install "https://github.com/maxwell2010/decimal-web3-sdk/releases/download/v0.1.2/decimal_web3_sdk-0.1.2-py3-none-any.whl"
```

**0.1.2 was refreshed in place on 2026-09-16.** If it is already installed,
`--upgrade` alone may skip it. Reinstall the refreshed build without pip's cache:
```shell
python -m pip install --force-reinstall --no-cache-dir "https://github.com/maxwell2010/decimal-web3-sdk/releases/download/v0.1.2/decimal_web3_sdk-0.1.2-py3-none-any.whl"
```
The version remains 0.1.2; the release's SHA256SUMS distinguishes the new artifacts.
For reproducibility, retain the downloaded wheel and its verified checksum.

Alternatively, from the same version's source archive:
```shell
python -m pip install "https://github.com/maxwell2010/decimal-web3-sdk/archive/refs/tags/v0.1.2.zip"
```

GitHub is the primary distribution source; PyPI publication is separate.
Use a pinned release for production; the latest manifest is an opt-in update channel.
[Build and publishing instructions](docs/en/releasing.md).

## Read a Balance

```python
import asyncio
import os
from decimal_web3_sdk import DecimalClient

async def main():
    async with DecimalClient() as client:
        balance = await client.balance_del(os.environ["WALLET_ADDRESS"])
        print(format(balance, "f"))

asyncio.run(main())
```

The client and CLI default to **mainnet**, using official Decimal RPCs.
Select `NetworkConfig.testnet()` or CLI `--network testnet` explicitly for tests;
custom nodes remain supported.
No signer is required to read balances.
`format_units_string(100000000000000000, 18)` returns exactly `"0.1"`.
Use strings or Decimal, never float, for amounts.

Every transaction has a complete example in the module guides.
Examples derive signing keys locally from a mnemonic and disable broadcast.
`broadcast=False` may still sign; use fee-estimation APIs for unsigned checks.
DEL needs no approval. ERC20 permit needs compatible token and target contracts;
otherwise an approval remains a separate transaction.

[Security](SECURITY.md) | [Changelog](CHANGELOG.md) | [API reference](docs/en/api.md)
