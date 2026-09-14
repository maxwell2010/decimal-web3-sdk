# tokens

[Guide](../README.md)

Complete examples below use testnet, require EXPECTED_ADDRESS and never broadcast. Other required environment variables appear in each example. They can sign locally; for unsigned fees use the fee guide. Auto-approval is disabled in examples. Contract-dependent methods require compatible deployed code and permissions.

## tx.approve_erc20

Set a spender allowance; amount zero revokes it.

[Erc20ApproveRequest](../reference/transactions.md#erc20approverequest)

```python
import asyncio
import getpass
import json
import os
import time
from decimal_web3_sdk import (
    DecimalClient, NetworkConfig, mnemonic_to_account, Erc20ApproveRequest
)


async def main():
    mnemonic = getpass.getpass("Mnemonic (local, hidden): ")
    wallet = mnemonic_to_account(mnemonic, account_index=0)
    expected = os.environ["EXPECTED_ADDRESS"]
    if wallet.address.lower() != expected.lower():
        raise ValueError("Unexpected signing account")
    request = Erc20ApproveRequest.from_mnemonic(
        mnemonic=mnemonic,
        account_index=0,
        token=os.environ["TOKEN"],
        spender=os.environ["SPENDER"],
        amount="0.000001",
    )
    async with DecimalClient(NetworkConfig.testnet()) as client:
        # Signs locally when preflight passes. NEVER broadcasts in this example.
        result = await client.tx.approve_erc20(
            request, broadcast=False, wait_receipt=False
        )
        print("success:", result.success)
        print("fee_DEL:", str(result.fee_del))
        print("message:", result.user_message)
        print("tx_hash:", result.tx_hash)


if __name__ == "__main__":
    asyncio.run(main())
```

## tx.send_erc20

Transfer ERC20 tokens from the signer; no approval is needed.

[Erc20TransferRequest](../reference/transactions.md#erc20transferrequest)

```python
import asyncio
import getpass
import json
import os
import time
from decimal_web3_sdk import (
    DecimalClient, NetworkConfig, mnemonic_to_account, Erc20TransferRequest
)


async def main():
    mnemonic = getpass.getpass("Mnemonic (local, hidden): ")
    wallet = mnemonic_to_account(mnemonic, account_index=0)
    expected = os.environ["EXPECTED_ADDRESS"]
    if wallet.address.lower() != expected.lower():
        raise ValueError("Unexpected signing account")
    request = Erc20TransferRequest.from_mnemonic(
        mnemonic=mnemonic,
        account_index=0,
        token=os.environ["TOKEN"],
        to=wallet.address,
        amount="0.000001",
    )
    async with DecimalClient(NetworkConfig.testnet()) as client:
        # Signs locally when preflight passes. NEVER broadcasts in this example.
        result = await client.tx.send_erc20(
            request, broadcast=False, wait_receipt=False
        )
        print("success:", result.success)
        print("fee_DEL:", str(result.fee_del))
        print("message:", result.user_message)
        print("tx_hash:", result.tx_hash)


if __name__ == "__main__":
    asyncio.run(main())
```

## tx.transfer_from_erc20

Transfer tokens using the owner's existing allowance to the signer.

[Erc20TransferFromRequest](../reference/transactions.md#erc20transferfromrequest)

```python
import asyncio
import getpass
import json
import os
import time
from decimal_web3_sdk import (
    DecimalClient, NetworkConfig, mnemonic_to_account, Erc20TransferFromRequest
)


async def main():
    mnemonic = getpass.getpass("Mnemonic (local, hidden): ")
    wallet = mnemonic_to_account(mnemonic, account_index=0)
    expected = os.environ["EXPECTED_ADDRESS"]
    if wallet.address.lower() != expected.lower():
        raise ValueError("Unexpected signing account")
    request = Erc20TransferFromRequest.from_mnemonic(
        mnemonic=mnemonic,
        account_index=0,
        token=os.environ["TOKEN"],
        owner=wallet.address,
        to=wallet.address,
        amount="0.000001",
    )
    async with DecimalClient(NetworkConfig.testnet()) as client:
        # Signs locally when preflight passes. NEVER broadcasts in this example.
        result = await client.tx.transfer_from_erc20(
            request, broadcast=False, wait_receipt=False
        )
        print("success:", result.success)
        print("fee_DEL:", str(result.fee_del))
        print("message:", result.user_message)
        print("tx_hash:", result.tx_hash)


if __name__ == "__main__":
    asyncio.run(main())
```

## decimal.multisend_erc20

Distribute ERC20 via multicall; permit or separate approval may be needed. Optional memo.

[MultisendErc20Request](../reference/decimal.md#multisenderc20request)

```python
import asyncio
import getpass
import json
import os
import time
from decimal_web3_sdk import (
    DecimalClient, NetworkConfig, mnemonic_to_account, MultisendErc20Request, MultisendErc20Recipient
)


async def main():
    mnemonic = getpass.getpass("Mnemonic (local, hidden): ")
    wallet = mnemonic_to_account(mnemonic, account_index=0)
    expected = os.environ["EXPECTED_ADDRESS"]
    if wallet.address.lower() != expected.lower():
        raise ValueError("Unexpected signing account")
    request = MultisendErc20Request.from_mnemonic(
        mnemonic=mnemonic,
        account_index=0,
        token=os.environ["TOKEN"],
        recipients=[MultisendErc20Recipient(wallet.address, "0.000001"), MultisendErc20Recipient(wallet.address, "0.000002")],
        memo="SDK example",
        auto_approve=False,
        prefer_permit=False,
        permit_deadline=int(time.time()) + 600,
    )
    async with DecimalClient(NetworkConfig.testnet()) as client:
        # Signs locally when preflight passes. NEVER broadcasts in this example.
        result = await client.decimal.multisend_erc20(
            request, broadcast=False, wait_receipt=False
        )
        print("success:", result.success)
        print("fee_DEL:", str(result.fee_del))
        print("message:", result.user_message)
        print("tx_hash:", result.tx_hash)


if __name__ == "__main__":
    asyncio.run(main())
```

## token.burn

Burn the signer's fungible tokens.

[BurnTokenRequest](../reference/token.md#burntokenrequest)

```python
import asyncio
import getpass
import json
import os
import time
from decimal_web3_sdk import (
    DecimalClient, NetworkConfig, mnemonic_to_account, BurnTokenRequest
)


async def main():
    mnemonic = getpass.getpass("Mnemonic (local, hidden): ")
    wallet = mnemonic_to_account(mnemonic, account_index=0)
    expected = os.environ["EXPECTED_ADDRESS"]
    if wallet.address.lower() != expected.lower():
        raise ValueError("Unexpected signing account")
    request = BurnTokenRequest.from_mnemonic(
        mnemonic=mnemonic,
        account_index=0,
        token=os.environ["TOKEN"],
        amount="0.000001",
    )
    async with DecimalClient(NetworkConfig.testnet()) as client:
        # Signs locally when preflight passes. NEVER broadcasts in this example.
        result = await client.token.burn(
            request, broadcast=False, wait_receipt=False
        )
        print("success:", result.success)
        print("fee_DEL:", str(result.fee_del))
        print("message:", result.user_message)
        print("tx_hash:", result.tx_hash)


if __name__ == "__main__":
    asyncio.run(main())
```

## token.buy

Buy reserve tokens with DEL and an explicit minimum output.

[BuyTokenRequest](../reference/token.md#buytokenrequest)

```python
import asyncio
import getpass
import json
import os
import time
from decimal_web3_sdk import (
    DecimalClient, NetworkConfig, mnemonic_to_account, BuyTokenRequest
)


async def main():
    mnemonic = getpass.getpass("Mnemonic (local, hidden): ")
    wallet = mnemonic_to_account(mnemonic, account_index=0)
    expected = os.environ["EXPECTED_ADDRESS"]
    if wallet.address.lower() != expected.lower():
        raise ValueError("Unexpected signing account")
    request = BuyTokenRequest.from_mnemonic(
        mnemonic=mnemonic,
        account_index=0,
        token=os.environ["TOKEN"],
        amount_del="0.000001",
    )
    async with DecimalClient(NetworkConfig.testnet()) as client:
        # Signs locally when preflight passes. NEVER broadcasts in this example.
        result = await client.token.buy(
            request, broadcast=False, wait_receipt=False
        )
        print("success:", result.success)
        print("fee_DEL:", str(result.fee_del))
        print("message:", result.user_message)
        print("tx_hash:", result.tx_hash)


if __name__ == "__main__":
    asyncio.run(main())
```

## token.convert

Convert tokens with a minimum output; may use permit or two transactions.

[ConvertTokenRequest](../reference/token.md#converttokenrequest)

```python
import asyncio
import getpass
import json
import os
import time
from decimal_web3_sdk import (
    DecimalClient, NetworkConfig, mnemonic_to_account, ConvertTokenRequest
)


async def main():
    mnemonic = getpass.getpass("Mnemonic (local, hidden): ")
    wallet = mnemonic_to_account(mnemonic, account_index=0)
    expected = os.environ["EXPECTED_ADDRESS"]
    if wallet.address.lower() != expected.lower():
        raise ValueError("Unexpected signing account")
    request = ConvertTokenRequest.from_mnemonic(
        mnemonic=mnemonic,
        account_index=0,
        token_in=os.environ["TOKEN_IN"],
        token_out=os.environ["TOKEN_OUT"],
        amount_in="0.000001",
        min_amount_out="0.000001",
        auto_approve=False,
        prefer_permit=False,
        permit_deadline=int(time.time()) + 600,
    )
    async with DecimalClient(NetworkConfig.testnet()) as client:
        # Signs locally when preflight passes. NEVER broadcasts in this example.
        result = await client.token.convert(
            request, broadcast=False, wait_receipt=False
        )
        print("success:", result.success)
        print("fee_DEL:", str(result.fee_del))
        print("message:", result.user_message)
        print("tx_hash:", result.tx_hash)


if __name__ == "__main__":
    asyncio.run(main())
```

## token.create

Create a reserve token; initial reserve and creation commission are not gas fees.

[CreateTokenRequest](../reference/token.md#createtokenrequest)

```python
import asyncio
import getpass
import json
import os
import time
from decimal_web3_sdk import (
    DecimalClient, NetworkConfig, mnemonic_to_account, CreateTokenRequest
)


async def main():
    mnemonic = getpass.getpass("Mnemonic (local, hidden): ")
    wallet = mnemonic_to_account(mnemonic, account_index=0)
    expected = os.environ["EXPECTED_ADDRESS"]
    if wallet.address.lower() != expected.lower():
        raise ValueError("Unexpected signing account")
    request = CreateTokenRequest.from_mnemonic(
        mnemonic=mnemonic,
        account_index=0,
        name="Example token",
        symbol="EXAMPLE",
        initial_mint_raw=1000000000000,
        min_total_supply_raw=1000000000000,
        max_total_supply_raw=1000000000000,
        crr=int(os.environ["CRR"]),
        identity=os.environ["IDENTITY"],
    )
    async with DecimalClient(NetworkConfig.testnet()) as client:
        # Signs locally when preflight passes. NEVER broadcasts in this example.
        result = await client.token.create(
            request, broadcast=False, wait_receipt=False
        )
        print("success:", result.success)
        print("fee_DEL:", str(result.fee_del))
        print("message:", result.user_message)
        print("tx_hash:", result.tx_hash)


if __name__ == "__main__":
    asyncio.run(main())
```

## token.create_reserveless

Create a token without reserve, with mint/burn flags and cap.

[CreateReservelessTokenRequest](../reference/token.md#createreservelesstokenrequest)

```python
import asyncio
import getpass
import json
import os
import time
from decimal_web3_sdk import (
    DecimalClient, NetworkConfig, mnemonic_to_account, CreateReservelessTokenRequest
)


async def main():
    mnemonic = getpass.getpass("Mnemonic (local, hidden): ")
    wallet = mnemonic_to_account(mnemonic, account_index=0)
    expected = os.environ["EXPECTED_ADDRESS"]
    if wallet.address.lower() != expected.lower():
        raise ValueError("Unexpected signing account")
    request = CreateReservelessTokenRequest.from_mnemonic(
        mnemonic=mnemonic,
        account_index=0,
        name="Example token",
        symbol="EXAMPLE",
        mintable=False,
        burnable=False,
        initial_mint_raw=1000000000000,
        cap_raw=1000000000000,
        identity=os.environ["IDENTITY"],
    )
    async with DecimalClient(NetworkConfig.testnet()) as client:
        # Signs locally when preflight passes. NEVER broadcasts in this example.
        result = await client.token.create_reserveless(
            request, broadcast=False, wait_receipt=False
        )
        print("success:", result.success)
        print("fee_DEL:", str(result.fee_del))
        print("message:", result.user_message)
        print("tx_hash:", result.tx_hash)


if __name__ == "__main__":
    asyncio.run(main())
```

## token.mint

Mint fungible tokens to a recipient; requires issuer rights.

[MintTokenRequest](../reference/token.md#minttokenrequest)

```python
import asyncio
import getpass
import json
import os
import time
from decimal_web3_sdk import (
    DecimalClient, NetworkConfig, mnemonic_to_account, MintTokenRequest
)


async def main():
    mnemonic = getpass.getpass("Mnemonic (local, hidden): ")
    wallet = mnemonic_to_account(mnemonic, account_index=0)
    expected = os.environ["EXPECTED_ADDRESS"]
    if wallet.address.lower() != expected.lower():
        raise ValueError("Unexpected signing account")
    request = MintTokenRequest.from_mnemonic(
        mnemonic=mnemonic,
        account_index=0,
        token=os.environ["TOKEN"],
        to=wallet.address,
        amount="0.000001",
    )
    async with DecimalClient(NetworkConfig.testnet()) as client:
        # Signs locally when preflight passes. NEVER broadcasts in this example.
        result = await client.token.mint(
            request, broadcast=False, wait_receipt=False
        )
        print("success:", result.success)
        print("fee_DEL:", str(result.fee_del))
        print("message:", result.user_message)
        print("tx_hash:", result.tx_hash)


if __name__ == "__main__":
    asyncio.run(main())
```

## token.sell

Sell reserve tokens for DEL with an explicit minimum output.

[SellTokenRequest](../reference/token.md#selltokenrequest)

```python
import asyncio
import getpass
import json
import os
import time
from decimal_web3_sdk import (
    DecimalClient, NetworkConfig, mnemonic_to_account, SellTokenRequest
)


async def main():
    mnemonic = getpass.getpass("Mnemonic (local, hidden): ")
    wallet = mnemonic_to_account(mnemonic, account_index=0)
    expected = os.environ["EXPECTED_ADDRESS"]
    if wallet.address.lower() != expected.lower():
        raise ValueError("Unexpected signing account")
    request = SellTokenRequest.from_mnemonic(
        mnemonic=mnemonic,
        account_index=0,
        token=os.environ["TOKEN"],
        amount="0.000001",
    )
    async with DecimalClient(NetworkConfig.testnet()) as client:
        # Signs locally when preflight passes. NEVER broadcasts in this example.
        result = await client.token.sell(
            request, broadcast=False, wait_receipt=False
        )
        print("success:", result.success)
        print("fee_DEL:", str(result.fee_del))
        print("message:", result.user_message)
        print("tx_hash:", result.tx_hash)


if __name__ == "__main__":
    asyncio.run(main())
```

## token.update_details

Update token identity and supply cap; requires issuer rights.

[UpdateTokenDetailsRequest](../reference/token.md#updatetokendetailsrequest)

```python
import asyncio
import getpass
import json
import os
import time
from decimal_web3_sdk import (
    DecimalClient, NetworkConfig, mnemonic_to_account, UpdateTokenDetailsRequest
)


async def main():
    mnemonic = getpass.getpass("Mnemonic (local, hidden): ")
    wallet = mnemonic_to_account(mnemonic, account_index=0)
    expected = os.environ["EXPECTED_ADDRESS"]
    if wallet.address.lower() != expected.lower():
        raise ValueError("Unexpected signing account")
    request = UpdateTokenDetailsRequest.from_mnemonic(
        mnemonic=mnemonic,
        account_index=0,
        token=os.environ["TOKEN"],
        identity=os.environ["IDENTITY"],
        max_total_supply_raw=1000000000000,
    )
    async with DecimalClient(NetworkConfig.testnet()) as client:
        # Signs locally when preflight passes. NEVER broadcasts in this example.
        result = await client.token.update_details(
            request, broadcast=False, wait_receipt=False
        )
        print("success:", result.success)
        print("fee_DEL:", str(result.fee_del))
        print("message:", result.user_message)
        print("tx_hash:", result.tx_hash)


if __name__ == "__main__":
    asyncio.run(main())
```
