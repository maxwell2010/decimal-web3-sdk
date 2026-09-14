# Installation Requirements
[Guide](README.md) | [Russian](../ru/install.md) | [Releases](releasing.md)

## Minimum Requirements
- CPython **3.10 or newer** and pip. Python 3.12, 64-bit is the locally verified choice.
- Internet access to GitHub for the SDK and the configured Python package index for dependencies.
- HTTPS access to a Decimal RPC for network operations. Local signing/encoding does not need a node.
- A writable virtual environment is recommended; administrator/root installation is unnecessary.
- No Git, Node.js, Go, Java, Android SDK, GPU or locally running blockchain node is required.

There is no measured RAM/disk minimum. The small SDK wheel does not include its
dependency downloads; pip installs those separately. Resource requirements depend
on workload, concurrency, dependency wheels and optional tooling.

## Operating Systems
The SDK wheel is `py3-none-any`: no SDK-specific native binary or OS lock.

| Platform | Verification / limitations |
| --- | --- |
| Windows | Local clean pip installation on CPython 3.12; CI tests/builds passed on 3.10, 3.12 and 3.13. |
| Linux | Ubuntu CI tests/builds passed on CPython 3.10, 3.12 and 3.13. |
| macOS | Expected to work with compatible Python/dependency wheels; not tested in this release preparation. |
| Other architectures / Python 3.14+ | Not verified; dependency wheel availability must be checked. |

[Verified CI run](https://github.com/maxwell2010/decimal-web3-sdk/actions/runs/34864115558)
checks the release code before this documentation-only update. These are offline
tests and packaging checks, not live blockchain transaction verification.

Use an OS version supported by your chosen Python distribution. Some transitive
dependencies contain native extensions. If pip cannot find a compatible wheel,
it may require a platform compiler/build toolchain; the SDK itself does not.

## Automatically Installed Dependencies
These are the direct runtime requirements from pyproject.toml:

| Package | Required version | Purpose |
| --- | --- | --- |
| web3 | >=7.13,<8 | EVM JSON-RPC, contracts and ABI operations |
| eth-account | >=0.13.7,<0.14 | Local accounts, mnemonic derivation and signing |
| aiohttp | >=3.12,<4 | Asynchronous HTTP and WebSocket clients |
| python-dotenv | >=1.0 | Optional local dotenv configuration support |

pip also resolves their transitive dependencies, such as eth-abi, eth-utils,
eth-keys, hexbytes, rlp and pydantic. The exact set/versions depend on the Python
version, platform and resolver; no claim of a fixed complete dependency list is made.
Do not install each library manually. `pip check` verifies dependency consistency.

pytest, pytest-asyncio, Ruff, mypy, build and Twine are only installed with `[dev]`.
The optional upstream comparison tool additionally needs tree-sitter parsers;
they are not runtime dependencies or installed by a normal SDK installation.

## Install and Verify
```shell
python --version
python -m venv .venv
```
Activate on Windows PowerShell:
```powershell
.\.venv\Scripts\Activate.ps1
```
Or activate on Linux/macOS:
```shell
. .venv/bin/activate
```
Then install directly from the versioned GitHub release:
```shell
python -m pip install --upgrade pip
python -m pip install "https://github.com/maxwell2010/decimal-web3-sdk/releases/download/v0.1.1/decimal_web3_sdk-0.1.1-py3-none-any.whl"
python -m pip check
python -c "import decimal_web3_sdk; print(decimal_web3_sdk.__version__)"
python -m pip list
```

Expected SDK version: `0.1.1`. No mnemonic or private key is needed for installation.
Client and CLI default to **mainnet**. For testing select `NetworkConfig.testnet()`
or `decimal-sdk --network testnet ...` explicitly. Transaction examples keep
broadcast disabled; installing the package never submits transactions.
