# bridge

[Guide](../README.md)

Complete examples below use testnet, require EXPECTED_ADDRESS and never broadcast. Other required environment variables appear in each example. They can sign locally; for unsigned fees use the fee guide. Auto-approval is disabled in examples. Contract-dependent methods require compatible deployed code and permissions.

## bridge.complete_transfer

Complete a bridge transfer with a verified encoded VM from the bridge.

[BridgeCompleteTransferRequest](../reference/bridge.md#bridgecompletetransferrequest)

```python
import asyncio
import getpass
import json
import os
import time
from decimal_web3_sdk import (
    DecimalClient, NetworkConfig, mnemonic_to_account, BridgeCompleteTransferRequest
)


async def main():
    mnemonic = getpass.getpass("Mnemonic (local, hidden): ")
    wallet = mnemonic_to_account(mnemonic, account_index=0)
    expected = os.environ["EXPECTED_ADDRESS"]
    if wallet.address.lower() != expected.lower():
        raise ValueError("Unexpected signing account")
    request = BridgeCompleteTransferRequest.from_mnemonic(
        mnemonic=mnemonic,
        account_index=0,
        contract=os.environ["CONTRACT"],
        encoded_vm=os.environ["ENCODED_VM"],
        unwrap_weth=False,
    )
    async with DecimalClient(NetworkConfig.testnet()) as client:
        # Signs locally when preflight passes. NEVER broadcasts in this example.
        result = await client.bridge.complete_transfer(
            request, broadcast=False, wait_receipt=False
        )
        print("success:", result.success)
        print("fee_DEL:", str(result.fee_del))
        print("message:", result.user_message)
        print("tx_hash:", result.tx_hash)


if __name__ == "__main__":
    asyncio.run(main())
```

## bridge.transfer_native

Start a native bridge transfer; destination completion is a separate workflow.

[BridgeTransferNativeRequest](../reference/bridge.md#bridgetransfernativerequest)

```python
import asyncio
import getpass
import json
import os
import time
from decimal_web3_sdk import (
    DecimalClient, NetworkConfig, mnemonic_to_account, BridgeTransferNativeRequest
)


async def main():
    mnemonic = getpass.getpass("Mnemonic (local, hidden): ")
    wallet = mnemonic_to_account(mnemonic, account_index=0)
    expected = os.environ["EXPECTED_ADDRESS"]
    if wallet.address.lower() != expected.lower():
        raise ValueError("Unexpected signing account")
    request = BridgeTransferNativeRequest.from_mnemonic(
        mnemonic=mnemonic,
        account_index=0,
        contract=os.environ["CONTRACT"],
        to=wallet.address,
        amount_wei=1000000000000,
        service_fee_wei=1000000000000,
        to_chain_id=int(os.environ["TO_CHAIN_ID"]),
        nonce=int(os.environ["NONCE"]),
    )
    async with DecimalClient(NetworkConfig.testnet()) as client:
        # Signs locally when preflight passes. NEVER broadcasts in this example.
        result = await client.bridge.transfer_native(
            request, broadcast=False, wait_receipt=False
        )
        print("success:", result.success)
        print("fee_DEL:", str(result.fee_del))
        print("message:", result.user_message)
        print("tx_hash:", result.tx_hash)


if __name__ == "__main__":
    asyncio.run(main())
```

## bridge.transfer_token

Start a token bridge transfer; allowance and service fee are caller responsibilities.

[BridgeTransferTokenRequest](../reference/bridge.md#bridgetransfertokenrequest)

```python
import asyncio
import getpass
import json
import os
import time
from decimal_web3_sdk import (
    DecimalClient, NetworkConfig, mnemonic_to_account, BridgeTransferTokenRequest
)


async def main():
    mnemonic = getpass.getpass("Mnemonic (local, hidden): ")
    wallet = mnemonic_to_account(mnemonic, account_index=0)
    expected = os.environ["EXPECTED_ADDRESS"]
    if wallet.address.lower() != expected.lower():
        raise ValueError("Unexpected signing account")
    request = BridgeTransferTokenRequest.from_mnemonic(
        mnemonic=mnemonic,
        account_index=0,
        contract=os.environ["CONTRACT"],
        token=os.environ["TOKEN"],
        to=wallet.address,
        amount_raw=1000000000000,
        service_fee_wei=1000000000000,
        to_chain_id=int(os.environ["TO_CHAIN_ID"]),
        nonce=int(os.environ["NONCE"]),
    )
    async with DecimalClient(NetworkConfig.testnet()) as client:
        # Signs locally when preflight passes. NEVER broadcasts in this example.
        result = await client.bridge.transfer_token(
            request, broadcast=False, wait_receipt=False
        )
        print("success:", result.success)
        print("fee_DEL:", str(result.fee_del))
        print("message:", result.user_message)
        print("tx_hash:", result.tx_hash)


if __name__ == "__main__":
    asyncio.run(main())
```
