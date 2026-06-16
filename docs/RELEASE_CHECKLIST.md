# Release Checklist

## Before Build

- [ ] `pytest -q`
- [ ] `DECIMAL_SDK_RUN_INTEGRATION=1 pytest -q tests/integration`
- [ ] Testnet/devnet dry-run with `DECIMAL_TEST_BROADCAST=0`
- [ ] Testnet/devnet broadcast with `DECIMAL_TEST_BROADCAST=1`
- [ ] No private endpoint URLs in public README/docs/source defaults
- [ ] Version updated in `pyproject.toml`
- [ ] `LICENSE` present

## Build

```powershell
python -m build
```

Expected artifacts:

```text
dist/decimal_web3_sdk-<version>.tar.gz
dist/decimal_web3_sdk-<version>-py3-none-any.whl
```

## Clean Install Smoke

```powershell
python -m venv .release-venv
.\.release-venv\Scripts\activate
pip install dist\decimal_web3_sdk-<version>-py3-none-any.whl
decimal-sdk block-number
```

## Publish

Publish only after testnet/devnet broadcast matrix is green.
