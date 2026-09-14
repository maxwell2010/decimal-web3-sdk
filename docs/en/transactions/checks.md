# checks

[Guide](../README.md)

Complete examples below use testnet, require EXPECTED_ADDRESS and never broadcast. Other required environment variables appear in each example. They can sign locally; for unsigned fees use the fee guide. Auto-approval is disabled in examples. Contract-dependent methods require compatible deployed code and permissions.

## checks.create_del

Create equal-value DEL checks for signer addresses; value is amount times count.

[CreateChecksDelRequest](../reference/checks.md#createchecksdelrequest)

```python
import asyncio
import getpass
import json
import os
import time
from decimal_web3_sdk import (
    DecimalClient, NetworkConfig, mnemonic_to_account, CreateChecksDelRequest
)


async def main():
    mnemonic = getpass.getpass("Mnemonic (local, hidden): ")
    wallet = mnemonic_to_account(mnemonic, account_index=0)
    expected = os.environ["EXPECTED_ADDRESS"]
    if wallet.address.lower() != expected.lower():
        raise ValueError("Unexpected signing account")
    request = CreateChecksDelRequest.from_mnemonic(
        mnemonic=mnemonic,
        account_index=0,
        contract=os.environ["CONTRACT"],
        signers=[wallet.address],
        amount_wei=1000000000000,
        due_block=int(os.environ["DUE_BLOCK"]),
    )
    async with DecimalClient(NetworkConfig.testnet()) as client:
        # Signs locally when preflight passes. NEVER broadcasts in this example.
        result = await client.checks.create_del(
            request, broadcast=False, wait_receipt=False
        )
        print("success:", result.success)
        print("fee_DEL:", str(result.fee_del))
        print("message:", result.user_message)
        print("tx_hash:", result.tx_hash)


if __name__ == "__main__":
    asyncio.run(main())
```

## checks.create_token

Create token checks using existing allowance or an explicitly supplied permit.

[CreateChecksTokenRequest](../reference/checks.md#createcheckstokenrequest)

```python
import asyncio
import getpass
import json
import os
import time
from decimal_web3_sdk import (
    DecimalClient, NetworkConfig, mnemonic_to_account, CreateChecksTokenRequest
)


async def main():
    mnemonic = getpass.getpass("Mnemonic (local, hidden): ")
    wallet = mnemonic_to_account(mnemonic, account_index=0)
    expected = os.environ["EXPECTED_ADDRESS"]
    if wallet.address.lower() != expected.lower():
        raise ValueError("Unexpected signing account")
    request = CreateChecksTokenRequest.from_mnemonic(
        mnemonic=mnemonic,
        account_index=0,
        contract=os.environ["CONTRACT"],
        token=os.environ["TOKEN"],
        signers=[wallet.address],
        amount_raw=1000000000000,
        due_block=int(os.environ["DUE_BLOCK"]),
    )
    async with DecimalClient(NetworkConfig.testnet()) as client:
        # Signs locally when preflight passes. NEVER broadcasts in this example.
        result = await client.checks.create_token(
            request, broadcast=False, wait_receipt=False
        )
        print("success:", result.success)
        print("fee_DEL:", str(result.fee_del))
        print("message:", result.user_message)
        print("tx_hash:", result.tx_hash)


if __name__ == "__main__":
    asyncio.run(main())
```

## checks.redeem

Redeem checks using matching check hashes and signatures.

[RedeemChecksRequest](../reference/checks.md#redeemchecksrequest)

```python
import asyncio
import getpass
import json
import os
import time
from decimal_web3_sdk import (
    DecimalClient, NetworkConfig, mnemonic_to_account, RedeemChecksRequest
)


async def main():
    mnemonic = getpass.getpass("Mnemonic (local, hidden): ")
    wallet = mnemonic_to_account(mnemonic, account_index=0)
    expected = os.environ["EXPECTED_ADDRESS"]
    if wallet.address.lower() != expected.lower():
        raise ValueError("Unexpected signing account")
    request = RedeemChecksRequest.from_mnemonic(
        mnemonic=mnemonic,
        account_index=0,
        contract=os.environ["CONTRACT"],
        signatures=json.loads(os.environ["SIGNATURES"]),
        checks=json.loads(os.environ["CHECKS"]),
    )
    async with DecimalClient(NetworkConfig.testnet()) as client:
        # Signs locally when preflight passes. NEVER broadcasts in this example.
        result = await client.checks.redeem(
            request, broadcast=False, wait_receipt=False
        )
        print("success:", result.success)
        print("fee_DEL:", str(result.fee_del))
        print("message:", result.user_message)
        print("tx_hash:", result.tx_hash)


if __name__ == "__main__":
    asyncio.run(main())
```
