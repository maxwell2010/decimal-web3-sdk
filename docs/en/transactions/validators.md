# validators

[Guide](../README.md)

Complete examples below use testnet, require EXPECTED_ADDRESS and never broadcast. Other required environment variables appear in each example. They can sign locally; for unsigned fees use the fee guide. Auto-approval is disabled in examples. Contract-dependent methods require compatible deployed code and permissions.

## decimal.pause_self_validator

Pause the signer's validator; requires operator authority.

[ValidatorSelfPauseRequest](../reference/decimal.md#validatorselfpauserequest)

```python
import asyncio
import getpass
import json
import os
import time
from decimal_web3_sdk import (
    DecimalClient, NetworkConfig, mnemonic_to_account, ValidatorSelfPauseRequest
)


async def main():
    mnemonic = getpass.getpass("Mnemonic (local, hidden): ")
    wallet = mnemonic_to_account(mnemonic, account_index=0)
    expected = os.environ["EXPECTED_ADDRESS"]
    if wallet.address.lower() != expected.lower():
        raise ValueError("Unexpected signing account")
    request = ValidatorSelfPauseRequest.from_mnemonic(
        mnemonic=mnemonic,
        account_index=0,

    )
    async with DecimalClient(NetworkConfig.testnet()) as client:
        # Signs locally when preflight passes. NEVER broadcasts in this example.
        result = await client.decimal.pause_self_validator(
            request, broadcast=False, wait_receipt=False
        )
        print("success:", result.success)
        print("fee_DEL:", str(result.fee_del))
        print("message:", result.user_message)
        print("tx_hash:", result.tx_hash)


if __name__ == "__main__":
    asyncio.run(main())
```

## decimal.pause_validator

Pause a specified validator; requires contract-level authorization.

[ValidatorPauseRequest](../reference/decimal.md#validatorpauserequest)

```python
import asyncio
import getpass
import json
import os
import time
from decimal_web3_sdk import (
    DecimalClient, NetworkConfig, mnemonic_to_account, ValidatorPauseRequest
)


async def main():
    mnemonic = getpass.getpass("Mnemonic (local, hidden): ")
    wallet = mnemonic_to_account(mnemonic, account_index=0)
    expected = os.environ["EXPECTED_ADDRESS"]
    if wallet.address.lower() != expected.lower():
        raise ValueError("Unexpected signing account")
    request = ValidatorPauseRequest.from_mnemonic(
        mnemonic=mnemonic,
        account_index=0,
        validator=os.environ["VALIDATOR"],
    )
    async with DecimalClient(NetworkConfig.testnet()) as client:
        # Signs locally when preflight passes. NEVER broadcasts in this example.
        result = await client.decimal.pause_validator(
            request, broadcast=False, wait_receipt=False
        )
        print("success:", result.success)
        print("fee_DEL:", str(result.fee_del))
        print("message:", result.user_message)
        print("tx_hash:", result.tx_hash)


if __name__ == "__main__":
    asyncio.run(main())
```

## decimal.unpause_self_validator

Resume the signer's validator; requires operator authority.

[ValidatorSelfPauseRequest](../reference/decimal.md#validatorselfpauserequest)

```python
import asyncio
import getpass
import json
import os
import time
from decimal_web3_sdk import (
    DecimalClient, NetworkConfig, mnemonic_to_account, ValidatorSelfPauseRequest
)


async def main():
    mnemonic = getpass.getpass("Mnemonic (local, hidden): ")
    wallet = mnemonic_to_account(mnemonic, account_index=0)
    expected = os.environ["EXPECTED_ADDRESS"]
    if wallet.address.lower() != expected.lower():
        raise ValueError("Unexpected signing account")
    request = ValidatorSelfPauseRequest.from_mnemonic(
        mnemonic=mnemonic,
        account_index=0,

    )
    async with DecimalClient(NetworkConfig.testnet()) as client:
        # Signs locally when preflight passes. NEVER broadcasts in this example.
        result = await client.decimal.unpause_self_validator(
            request, broadcast=False, wait_receipt=False
        )
        print("success:", result.success)
        print("fee_DEL:", str(result.fee_del))
        print("message:", result.user_message)
        print("tx_hash:", result.tx_hash)


if __name__ == "__main__":
    asyncio.run(main())
```

## decimal.unpause_validator

Resume a specified validator; requires contract-level authorization.

[ValidatorPauseRequest](../reference/decimal.md#validatorpauserequest)

```python
import asyncio
import getpass
import json
import os
import time
from decimal_web3_sdk import (
    DecimalClient, NetworkConfig, mnemonic_to_account, ValidatorPauseRequest
)


async def main():
    mnemonic = getpass.getpass("Mnemonic (local, hidden): ")
    wallet = mnemonic_to_account(mnemonic, account_index=0)
    expected = os.environ["EXPECTED_ADDRESS"]
    if wallet.address.lower() != expected.lower():
        raise ValueError("Unexpected signing account")
    request = ValidatorPauseRequest.from_mnemonic(
        mnemonic=mnemonic,
        account_index=0,
        validator=os.environ["VALIDATOR"],
    )
    async with DecimalClient(NetworkConfig.testnet()) as client:
        # Signs locally when preflight passes. NEVER broadcasts in this example.
        result = await client.decimal.unpause_validator(
            request, broadcast=False, wait_receipt=False
        )
        print("success:", result.success)
        print("fee_DEL:", str(result.fee_del))
        print("message:", result.user_message)
        print("tx_hash:", result.tx_hash)


if __name__ == "__main__":
    asyncio.run(main())
```
