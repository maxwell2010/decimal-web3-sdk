# Decimal Web3 SDK

Independent Decimal EVM SDK by [MintCandy](https://mintcandy.ru/) and
[@Maxwell2019](https://t.me/Maxwell2019). MIT license, Python 3.10+.
Package: `decimal-web3-sdk`; import: `decimal_web3_sdk`.

**0.1.1 is a release candidate, not complete JS/Go SDK parity.**
55 high-level transaction entry points have offline encoding/signing coverage.
Contract compatibility still depends on the network. [Coverage and limitations](docs/en/status.md).
[Official SDK comparison](docs/en/upstream-parity.md): JS 95 / Go 53 / Python 55 specialized EVM write entry points, not a parity percentage.

[Русский README](README.ru.md) | [English guide](docs/en/README.md) | [Русская документация](docs/ru/README.md)

## Install Without Git

Requires Python 3.10+ and pip. Runtime dependencies install automatically:
web3, eth-account, aiohttp and python-dotenv, plus their dependencies.
[OS support and installation requirements](docs/en/install.md).

From the versioned GitHub release (no Git installation required):
```shell
python -m pip install "https://github.com/maxwell2010/decimal-web3-sdk/releases/download/v0.1.1/decimal_web3_sdk-0.1.1-py3-none-any.whl"
```

Alternatively, from the same version's source archive:
```shell
python -m pip install "https://github.com/maxwell2010/decimal-web3-sdk/archive/refs/tags/v0.1.1.zip"
```

These URLs require the corresponding GitHub release/tag to be published.
GitHub is the primary distribution source; PyPI publication is separate.
Pin a release version rather than installing a moving branch such as main.
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
