# staking

[Guide](../README.md)

Complete examples below use testnet, require EXPECTED_ADDRESS and never broadcast. Other required environment variables appear in each example. They can sign locally; for unsigned fees use the fee guide. Auto-approval is disabled in examples. Contract-dependent methods require compatible deployed code and permissions.

## decimal.apply_stake_penalties

Legacy accumulated penalties call; explicit opt-in required.

[ApplyStakePenaltiesRequest](../reference/staking_operations.md#applystakepenaltiesrequest)

```python
import asyncio
import getpass
import json
import os
import time
from decimal_web3_sdk import (
    DecimalClient, NetworkConfig, mnemonic_to_account, ApplyStakePenaltiesRequest
)


async def main():
    mnemonic = getpass.getpass("Mnemonic (local, hidden): ")
    wallet = mnemonic_to_account(mnemonic, account_index=0)
    expected = os.environ["EXPECTED_ADDRESS"]
    if wallet.address.lower() != expected.lower():
        raise ValueError("Unexpected signing account")
    request = ApplyStakePenaltiesRequest.from_mnemonic(
        mnemonic=mnemonic,
        account_index=0,
        validator=os.environ["VALIDATOR"],
        delegator=wallet.address,
        token=os.environ["TOKEN"],
        allow_legacy=os.environ.get("ALLOW_LEGACY_CONTRACT", "0") == "1",
    )
    async with DecimalClient(NetworkConfig.testnet()) as client:
        # Signs locally when preflight passes. NEVER broadcasts in this example.
        result = await client.decimal.apply_stake_penalties(
            request, broadcast=False, wait_receipt=False
        )
        print("success:", result.success)
        print("fee_DEL:", str(result.fee_del))
        print("message:", result.user_message)
        print("tx_hash:", result.tx_hash)


if __name__ == "__main__":
    asyncio.run(main())
```

## decimal.apply_stake_penalty

Legacy single penalty call; not in the inspected current Delegation ABI.

[ApplyStakePenaltyRequest](../reference/staking_operations.md#applystakepenaltyrequest)

```python
import asyncio
import getpass
import json
import os
import time
from decimal_web3_sdk import (
    DecimalClient, NetworkConfig, mnemonic_to_account, ApplyStakePenaltyRequest
)


async def main():
    mnemonic = getpass.getpass("Mnemonic (local, hidden): ")
    wallet = mnemonic_to_account(mnemonic, account_index=0)
    expected = os.environ["EXPECTED_ADDRESS"]
    if wallet.address.lower() != expected.lower():
        raise ValueError("Unexpected signing account")
    request = ApplyStakePenaltyRequest.from_mnemonic(
        mnemonic=mnemonic,
        account_index=0,
        validator=os.environ["VALIDATOR"],
        delegator=wallet.address,
        token=os.environ["TOKEN"],
        allow_legacy=os.environ.get("ALLOW_LEGACY_CONTRACT", "0") == "1",
    )
    async with DecimalClient(NetworkConfig.testnet()) as client:
        # Signs locally when preflight passes. NEVER broadcasts in this example.
        result = await client.decimal.apply_stake_penalty(
            request, broadcast=False, wait_receipt=False
        )
        print("success:", result.success)
        print("fee_DEL:", str(result.fee_del))
        print("message:", result.user_message)
        print("tx_hash:", result.tx_hash)


if __name__ == "__main__":
    asyncio.run(main())
```

## decimal.complete_stake

Finalize frozen fungible stakes by queue index after the freeze period.

[CompleteStakeRequest](../reference/staking_operations.md#completestakerequest)

```python
import asyncio
import getpass
import json
import os
import time
from decimal_web3_sdk import (
    DecimalClient, NetworkConfig, mnemonic_to_account, CompleteStakeRequest
)


async def main():
    mnemonic = getpass.getpass("Mnemonic (local, hidden): ")
    wallet = mnemonic_to_account(mnemonic, account_index=0)
    expected = os.environ["EXPECTED_ADDRESS"]
    if wallet.address.lower() != expected.lower():
        raise ValueError("Unexpected signing account")
    request = CompleteStakeRequest.from_mnemonic(
        mnemonic=mnemonic,
        account_index=0,
        indexes=tuple(json.loads(os.environ["FROZEN_STAKE_INDEXES"])),
    )
    async with DecimalClient(NetworkConfig.testnet()) as client:
        # Signs locally when preflight passes. NEVER broadcasts in this example.
        result = await client.decimal.complete_stake(
            request, broadcast=False, wait_receipt=False
        )
        print("success:", result.success)
        print("fee_DEL:", str(result.fee_del))
        print("message:", result.user_message)
        print("tx_hash:", result.tx_hash)


if __name__ == "__main__":
    asyncio.run(main())
```

## decimal.delegate_del

Delegate native DEL to a validator.

[DelegateDelRequest](../reference/decimal.md#delegatedelrequest)

```python
import asyncio
import getpass
import json
import os
import time
from decimal_web3_sdk import (
    DecimalClient, NetworkConfig, mnemonic_to_account, DelegateDelRequest
)


async def main():
    mnemonic = getpass.getpass("Mnemonic (local, hidden): ")
    wallet = mnemonic_to_account(mnemonic, account_index=0)
    expected = os.environ["EXPECTED_ADDRESS"]
    if wallet.address.lower() != expected.lower():
        raise ValueError("Unexpected signing account")
    request = DelegateDelRequest.from_mnemonic(
        mnemonic=mnemonic,
        account_index=0,
        validator=os.environ["VALIDATOR"],
        amount_del="0.000001",
    )
    async with DecimalClient(NetworkConfig.testnet()) as client:
        # Signs locally when preflight passes. NEVER broadcasts in this example.
        result = await client.decimal.delegate_del(
            request, broadcast=False, wait_receipt=False
        )
        print("success:", result.success)
        print("fee_DEL:", str(result.fee_del))
        print("message:", result.user_message)
        print("tx_hash:", result.tx_hash)


if __name__ == "__main__":
    asyncio.run(main())
```

## decimal.delegate_erc20

Delegate a reserve token; permission may be needed.

[DelegateErc20Request](../reference/decimal.md#delegateerc20request)

```python
import asyncio
import getpass
import json
import os
import time
from decimal_web3_sdk import (
    DecimalClient, NetworkConfig, mnemonic_to_account, DelegateErc20Request
)


async def main():
    mnemonic = getpass.getpass("Mnemonic (local, hidden): ")
    wallet = mnemonic_to_account(mnemonic, account_index=0)
    expected = os.environ["EXPECTED_ADDRESS"]
    if wallet.address.lower() != expected.lower():
        raise ValueError("Unexpected signing account")
    request = DelegateErc20Request.from_mnemonic(
        mnemonic=mnemonic,
        account_index=0,
        token=os.environ["TOKEN"],
        validator=os.environ["VALIDATOR"],
        amount="0.000001",
        auto_approve=False,
        prefer_permit=False,
        permit_deadline=int(time.time()) + 600,
    )
    async with DecimalClient(NetworkConfig.testnet()) as client:
        # Signs locally when preflight passes. NEVER broadcasts in this example.
        result = await client.decimal.delegate_erc20(
            request, broadcast=False, wait_receipt=False
        )
        print("success:", result.success)
        print("fee_DEL:", str(result.fee_del))
        print("message:", result.user_message)
        print("tx_hash:", result.tx_hash)


if __name__ == "__main__":
    asyncio.run(main())
```

## decimal.hold_del

Delegate DEL with an explicit hold-end Unix timestamp.

[HoldDelRequest](../reference/decimal.md#holddelrequest)

```python
import asyncio
import getpass
import json
import os
import time
from decimal_web3_sdk import (
    DecimalClient, NetworkConfig, mnemonic_to_account, HoldDelRequest
)


async def main():
    mnemonic = getpass.getpass("Mnemonic (local, hidden): ")
    wallet = mnemonic_to_account(mnemonic, account_index=0)
    expected = os.environ["EXPECTED_ADDRESS"]
    if wallet.address.lower() != expected.lower():
        raise ValueError("Unexpected signing account")
    request = HoldDelRequest.from_mnemonic(
        mnemonic=mnemonic,
        account_index=0,
        validator=os.environ["VALIDATOR"],
        amount_del="0.000001",
        hold_timestamp=int(os.environ["HOLD_TIMESTAMP"]),
    )
    async with DecimalClient(NetworkConfig.testnet()) as client:
        # Signs locally when preflight passes. NEVER broadcasts in this example.
        result = await client.decimal.hold_del(
            request, broadcast=False, wait_receipt=False
        )
        print("success:", result.success)
        print("fee_DEL:", str(result.fee_del))
        print("message:", result.user_message)
        print("tx_hash:", result.tx_hash)


if __name__ == "__main__":
    asyncio.run(main())
```

## decimal.hold_erc20

Delegate ERC20 with a hold end; permission may be needed.

[HoldErc20Request](../reference/decimal.md#holderc20request)

```python
import asyncio
import getpass
import json
import os
import time
from decimal_web3_sdk import (
    DecimalClient, NetworkConfig, mnemonic_to_account, HoldErc20Request
)


async def main():
    mnemonic = getpass.getpass("Mnemonic (local, hidden): ")
    wallet = mnemonic_to_account(mnemonic, account_index=0)
    expected = os.environ["EXPECTED_ADDRESS"]
    if wallet.address.lower() != expected.lower():
        raise ValueError("Unexpected signing account")
    request = HoldErc20Request.from_mnemonic(
        mnemonic=mnemonic,
        account_index=0,
        token=os.environ["TOKEN"],
        validator=os.environ["VALIDATOR"],
        amount="0.000001",
        hold_timestamp=int(os.environ["HOLD_TIMESTAMP"]),
        auto_approve=False,
        prefer_permit=False,
        permit_deadline=int(time.time()) + 600,
    )
    async with DecimalClient(NetworkConfig.testnet()) as client:
        # Signs locally when preflight passes. NEVER broadcasts in this example.
        result = await client.decimal.hold_erc20(
            request, broadcast=False, wait_receipt=False
        )
        print("success:", result.success)
        print("fee_DEL:", str(result.fee_del))
        print("message:", result.user_message)
        print("tx_hash:", result.tx_hash)


if __name__ == "__main__":
    asyncio.run(main())
```

## decimal.hold_stake_with_reset

Reset eligible token holds and create a new hold schedule.

[HoldStakeWithResetRequest](../reference/decimal.md#holdstakewithresetrequest)

```python
import asyncio
import getpass
import json
import os
import time
from decimal_web3_sdk import (
    DecimalClient, NetworkConfig, mnemonic_to_account, HoldStakeWithResetRequest
)


async def main():
    mnemonic = getpass.getpass("Mnemonic (local, hidden): ")
    wallet = mnemonic_to_account(mnemonic, account_index=0)
    expected = os.environ["EXPECTED_ADDRESS"]
    if wallet.address.lower() != expected.lower():
        raise ValueError("Unexpected signing account")
    request = HoldStakeWithResetRequest.from_mnemonic(
        mnemonic=mnemonic,
        account_index=0,
        token=os.environ["TOKEN"],
        validator=os.environ["VALIDATOR"],
        amount="0.000001",
        new_hold_timestamp=int(os.environ["NEW_HOLD_TIMESTAMP"]),
        hold_timestamps_to_reset=tuple(json.loads(os.environ["HOLD_TIMESTAMPS_TO_RESET"])),
    )
    async with DecimalClient(NetworkConfig.testnet()) as client:
        # Signs locally when preflight passes. NEVER broadcasts in this example.
        result = await client.decimal.hold_stake_with_reset(
            request, broadcast=False, wait_receipt=False
        )
        print("success:", result.success)
        print("fee_DEL:", str(result.fee_del))
        print("message:", result.user_message)
        print("tx_hash:", result.tx_hash)


if __name__ == "__main__":
    asyncio.run(main())
```

## decimal.reset_stake_hold

Reset an eligible matured hold for the specified delegator.

[ResetStakeHoldRequest](../reference/decimal.md#resetstakeholdrequest)

```python
import asyncio
import getpass
import json
import os
import time
from decimal_web3_sdk import (
    DecimalClient, NetworkConfig, mnemonic_to_account, ResetStakeHoldRequest
)


async def main():
    mnemonic = getpass.getpass("Mnemonic (local, hidden): ")
    wallet = mnemonic_to_account(mnemonic, account_index=0)
    expected = os.environ["EXPECTED_ADDRESS"]
    if wallet.address.lower() != expected.lower():
        raise ValueError("Unexpected signing account")
    request = ResetStakeHoldRequest.from_mnemonic(
        mnemonic=mnemonic,
        account_index=0,
        validator=os.environ["VALIDATOR"],
        delegator=wallet.address,
        hold_timestamp=int(os.environ["HOLD_TIMESTAMP"]),
    )
    async with DecimalClient(NetworkConfig.testnet()) as client:
        # Signs locally when preflight passes. NEVER broadcasts in this example.
        result = await client.decimal.reset_stake_hold(
            request, broadcast=False, wait_receipt=False
        )
        print("success:", result.success)
        print("fee_DEL:", str(result.fee_del))
        print("message:", result.user_message)
        print("tx_hash:", result.tx_hash)


if __name__ == "__main__":
    asyncio.run(main())
```

## decimal.stake_token_to_hold

Move a token stake into a hold with a new end timestamp.

[StakeTokenToHoldRequest](../reference/decimal.md#staketokentoholdrequest)

```python
import asyncio
import getpass
import json
import os
import time
from decimal_web3_sdk import (
    DecimalClient, NetworkConfig, mnemonic_to_account, StakeTokenToHoldRequest
)


async def main():
    mnemonic = getpass.getpass("Mnemonic (local, hidden): ")
    wallet = mnemonic_to_account(mnemonic, account_index=0)
    expected = os.environ["EXPECTED_ADDRESS"]
    if wallet.address.lower() != expected.lower():
        raise ValueError("Unexpected signing account")
    request = StakeTokenToHoldRequest.from_mnemonic(
        mnemonic=mnemonic,
        account_index=0,
        token=os.environ["TOKEN"],
        validator=os.environ["VALIDATOR"],
        amount="0.000001",
        old_hold_timestamp=int(os.environ["OLD_HOLD_TIMESTAMP"]),
        new_hold_timestamp=int(os.environ["NEW_HOLD_TIMESTAMP"]),
    )
    async with DecimalClient(NetworkConfig.testnet()) as client:
        # Signs locally when preflight passes. NEVER broadcasts in this example.
        result = await client.decimal.stake_token_to_hold(
            request, broadcast=False, wait_receipt=False
        )
        print("success:", result.success)
        print("fee_DEL:", str(result.fee_del))
        print("message:", result.user_message)
        print("tx_hash:", result.tx_hash)


if __name__ == "__main__":
    asyncio.run(main())
```

## decimal.transfer_del_stake_with_reset

Reset selected DEL holds and move stake to another validator.

[TransferDelStakeWithResetRequest](../reference/decimal.md#transferdelstakewithresetrequest)

```python
import asyncio
import getpass
import json
import os
import time
from decimal_web3_sdk import (
    DecimalClient, NetworkConfig, mnemonic_to_account, TransferDelStakeWithResetRequest
)


async def main():
    mnemonic = getpass.getpass("Mnemonic (local, hidden): ")
    wallet = mnemonic_to_account(mnemonic, account_index=0)
    expected = os.environ["EXPECTED_ADDRESS"]
    if wallet.address.lower() != expected.lower():
        raise ValueError("Unexpected signing account")
    request = TransferDelStakeWithResetRequest.from_mnemonic(
        mnemonic=mnemonic,
        account_index=0,
        old_validator=os.environ["OLD_VALIDATOR"],
        new_validator=os.environ["NEW_VALIDATOR"],
        amount_del="0.000001",
        hold_timestamps_to_reset=tuple(json.loads(os.environ["HOLD_TIMESTAMPS_TO_RESET"])),
    )
    async with DecimalClient(NetworkConfig.testnet()) as client:
        # Signs locally when preflight passes. NEVER broadcasts in this example.
        result = await client.decimal.transfer_del_stake_with_reset(
            request, broadcast=False, wait_receipt=False
        )
        print("success:", result.success)
        print("fee_DEL:", str(result.fee_del))
        print("message:", result.user_message)
        print("tx_hash:", result.tx_hash)


if __name__ == "__main__":
    asyncio.run(main())
```

## decimal.transfer_stake_del

Move regular or held DEL stake to another validator.

[TransferStakeDelRequest](../reference/decimal.md#transferstakedelrequest)

```python
import asyncio
import getpass
import json
import os
import time
from decimal_web3_sdk import (
    DecimalClient, NetworkConfig, mnemonic_to_account, TransferStakeDelRequest
)


async def main():
    mnemonic = getpass.getpass("Mnemonic (local, hidden): ")
    wallet = mnemonic_to_account(mnemonic, account_index=0)
    expected = os.environ["EXPECTED_ADDRESS"]
    if wallet.address.lower() != expected.lower():
        raise ValueError("Unexpected signing account")
    request = TransferStakeDelRequest.from_mnemonic(
        mnemonic=mnemonic,
        account_index=0,
        validator=os.environ["VALIDATOR"],
        new_validator=os.environ["NEW_VALIDATOR"],
        amount_del="0.000001",
    )
    async with DecimalClient(NetworkConfig.testnet()) as client:
        # Signs locally when preflight passes. NEVER broadcasts in this example.
        result = await client.decimal.transfer_stake_del(
            request, broadcast=False, wait_receipt=False
        )
        print("success:", result.success)
        print("fee_DEL:", str(result.fee_del))
        print("message:", result.user_message)
        print("tx_hash:", result.tx_hash)


if __name__ == "__main__":
    asyncio.run(main())
```

## decimal.transfer_stake_erc20

Move regular or held token stake to another validator.

[TransferStakeErc20Request](../reference/decimal.md#transferstakeerc20request)

```python
import asyncio
import getpass
import json
import os
import time
from decimal_web3_sdk import (
    DecimalClient, NetworkConfig, mnemonic_to_account, TransferStakeErc20Request
)


async def main():
    mnemonic = getpass.getpass("Mnemonic (local, hidden): ")
    wallet = mnemonic_to_account(mnemonic, account_index=0)
    expected = os.environ["EXPECTED_ADDRESS"]
    if wallet.address.lower() != expected.lower():
        raise ValueError("Unexpected signing account")
    request = TransferStakeErc20Request.from_mnemonic(
        mnemonic=mnemonic,
        account_index=0,
        token=os.environ["TOKEN"],
        validator=os.environ["VALIDATOR"],
        new_validator=os.environ["NEW_VALIDATOR"],
        amount="0.000001",
    )
    async with DecimalClient(NetworkConfig.testnet()) as client:
        # Signs locally when preflight passes. NEVER broadcasts in this example.
        result = await client.decimal.transfer_stake_erc20(
            request, broadcast=False, wait_receipt=False
        )
        print("success:", result.success)
        print("fee_DEL:", str(result.fee_del))
        print("message:", result.user_message)
        print("tx_hash:", result.tx_hash)


if __name__ == "__main__":
    asyncio.run(main())
```

## decimal.transfer_stake_with_reset

Reset selected token holds and move stake to another validator.

[TransferStakeWithResetRequest](../reference/decimal.md#transferstakewithresetrequest)

```python
import asyncio
import getpass
import json
import os
import time
from decimal_web3_sdk import (
    DecimalClient, NetworkConfig, mnemonic_to_account, TransferStakeWithResetRequest
)


async def main():
    mnemonic = getpass.getpass("Mnemonic (local, hidden): ")
    wallet = mnemonic_to_account(mnemonic, account_index=0)
    expected = os.environ["EXPECTED_ADDRESS"]
    if wallet.address.lower() != expected.lower():
        raise ValueError("Unexpected signing account")
    request = TransferStakeWithResetRequest.from_mnemonic(
        mnemonic=mnemonic,
        account_index=0,
        token=os.environ["TOKEN"],
        old_validator=os.environ["OLD_VALIDATOR"],
        new_validator=os.environ["NEW_VALIDATOR"],
        amount="0.000001",
        hold_timestamps_to_reset=tuple(json.loads(os.environ["HOLD_TIMESTAMPS_TO_RESET"])),
    )
    async with DecimalClient(NetworkConfig.testnet()) as client:
        # Signs locally when preflight passes. NEVER broadcasts in this example.
        result = await client.decimal.transfer_stake_with_reset(
            request, broadcast=False, wait_receipt=False
        )
        print("success:", result.success)
        print("fee_DEL:", str(result.fee_del))
        print("message:", result.user_message)
        print("tx_hash:", result.tx_hash)


if __name__ == "__main__":
    asyncio.run(main())
```

## decimal.unbond_del

Request withdrawal from the regular DEL stake; this starts unbonding, not immediate payment.

[UnbondDelRequest](../reference/decimal.md#unbonddelrequest)

```python
import asyncio
import getpass
import json
import os
import time
from decimal_web3_sdk import (
    DecimalClient, NetworkConfig, mnemonic_to_account, UnbondDelRequest
)


async def main():
    mnemonic = getpass.getpass("Mnemonic (local, hidden): ")
    wallet = mnemonic_to_account(mnemonic, account_index=0)
    expected = os.environ["EXPECTED_ADDRESS"]
    if wallet.address.lower() != expected.lower():
        raise ValueError("Unexpected signing account")
    request = UnbondDelRequest.from_mnemonic(
        mnemonic=mnemonic,
        account_index=0,
        validator=os.environ["VALIDATOR"],
        amount_del="0.000001",
    )
    async with DecimalClient(NetworkConfig.testnet()) as client:
        # Signs locally when preflight passes. NEVER broadcasts in this example.
        result = await client.decimal.unbond_del(
            request, broadcast=False, wait_receipt=False
        )
        print("success:", result.success)
        print("fee_DEL:", str(result.fee_del))
        print("message:", result.user_message)
        print("tx_hash:", result.tx_hash)


if __name__ == "__main__":
    asyncio.run(main())
```

## decimal.unbond_erc20

Request withdrawal from the regular token stake.

[UnbondErc20Request](../reference/decimal.md#unbonderc20request)

```python
import asyncio
import getpass
import json
import os
import time
from decimal_web3_sdk import (
    DecimalClient, NetworkConfig, mnemonic_to_account, UnbondErc20Request
)


async def main():
    mnemonic = getpass.getpass("Mnemonic (local, hidden): ")
    wallet = mnemonic_to_account(mnemonic, account_index=0)
    expected = os.environ["EXPECTED_ADDRESS"]
    if wallet.address.lower() != expected.lower():
        raise ValueError("Unexpected signing account")
    request = UnbondErc20Request.from_mnemonic(
        mnemonic=mnemonic,
        account_index=0,
        token=os.environ["TOKEN"],
        validator=os.environ["VALIDATOR"],
        amount="0.000001",
    )
    async with DecimalClient(NetworkConfig.testnet()) as client:
        # Signs locally when preflight passes. NEVER broadcasts in this example.
        result = await client.decimal.unbond_erc20(
            request, broadcast=False, wait_receipt=False
        )
        print("success:", result.success)
        print("fee_DEL:", str(result.fee_del))
        print("message:", result.user_message)
        print("tx_hash:", result.tx_hash)


if __name__ == "__main__":
    asyncio.run(main())
```

## decimal.withdraw_del_stake_with_reset

Reset selected matured DEL holds and request withdrawal.

[WithdrawDelStakeWithResetRequest](../reference/decimal.md#withdrawdelstakewithresetrequest)

```python
import asyncio
import getpass
import json
import os
import time
from decimal_web3_sdk import (
    DecimalClient, NetworkConfig, mnemonic_to_account, WithdrawDelStakeWithResetRequest
)


async def main():
    mnemonic = getpass.getpass("Mnemonic (local, hidden): ")
    wallet = mnemonic_to_account(mnemonic, account_index=0)
    expected = os.environ["EXPECTED_ADDRESS"]
    if wallet.address.lower() != expected.lower():
        raise ValueError("Unexpected signing account")
    request = WithdrawDelStakeWithResetRequest.from_mnemonic(
        mnemonic=mnemonic,
        account_index=0,
        validator=os.environ["VALIDATOR"],
        amount_del="0.000001",
        hold_timestamps_to_reset=tuple(json.loads(os.environ["HOLD_TIMESTAMPS_TO_RESET"])),
    )
    async with DecimalClient(NetworkConfig.testnet()) as client:
        # Signs locally when preflight passes. NEVER broadcasts in this example.
        result = await client.decimal.withdraw_del_stake_with_reset(
            request, broadcast=False, wait_receipt=False
        )
        print("success:", result.success)
        print("fee_DEL:", str(result.fee_del))
        print("message:", result.user_message)
        print("tx_hash:", result.tx_hash)


if __name__ == "__main__":
    asyncio.run(main())
```

## decimal.withdraw_hold_del

Withdraw a matured DEL hold using its exact hold key.

[WithdrawHoldDelRequest](../reference/decimal.md#withdrawholddelrequest)

```python
import asyncio
import getpass
import json
import os
import time
from decimal_web3_sdk import (
    DecimalClient, NetworkConfig, mnemonic_to_account, WithdrawHoldDelRequest
)


async def main():
    mnemonic = getpass.getpass("Mnemonic (local, hidden): ")
    wallet = mnemonic_to_account(mnemonic, account_index=0)
    expected = os.environ["EXPECTED_ADDRESS"]
    if wallet.address.lower() != expected.lower():
        raise ValueError("Unexpected signing account")
    request = WithdrawHoldDelRequest.from_mnemonic(
        mnemonic=mnemonic,
        account_index=0,
        validator=os.environ["VALIDATOR"],
        amount_del="0.000001",
        hold_timestamp=int(os.environ["HOLD_TIMESTAMP"]),
    )
    async with DecimalClient(NetworkConfig.testnet()) as client:
        # Signs locally when preflight passes. NEVER broadcasts in this example.
        result = await client.decimal.withdraw_hold_del(
            request, broadcast=False, wait_receipt=False
        )
        print("success:", result.success)
        print("fee_DEL:", str(result.fee_del))
        print("message:", result.user_message)
        print("tx_hash:", result.tx_hash)


if __name__ == "__main__":
    asyncio.run(main())
```

## decimal.withdraw_hold_erc20

Withdraw a matured ERC20 hold using its exact hold key.

[WithdrawHoldErc20Request](../reference/decimal.md#withdrawholderc20request)

```python
import asyncio
import getpass
import json
import os
import time
from decimal_web3_sdk import (
    DecimalClient, NetworkConfig, mnemonic_to_account, WithdrawHoldErc20Request
)


async def main():
    mnemonic = getpass.getpass("Mnemonic (local, hidden): ")
    wallet = mnemonic_to_account(mnemonic, account_index=0)
    expected = os.environ["EXPECTED_ADDRESS"]
    if wallet.address.lower() != expected.lower():
        raise ValueError("Unexpected signing account")
    request = WithdrawHoldErc20Request.from_mnemonic(
        mnemonic=mnemonic,
        account_index=0,
        token=os.environ["TOKEN"],
        validator=os.environ["VALIDATOR"],
        amount="0.000001",
        hold_timestamp=int(os.environ["HOLD_TIMESTAMP"]),
    )
    async with DecimalClient(NetworkConfig.testnet()) as client:
        # Signs locally when preflight passes. NEVER broadcasts in this example.
        result = await client.decimal.withdraw_hold_erc20(
            request, broadcast=False, wait_receipt=False
        )
        print("success:", result.success)
        print("fee_DEL:", str(result.fee_del))
        print("message:", result.user_message)
        print("tx_hash:", result.tx_hash)


if __name__ == "__main__":
    asyncio.run(main())
```

## decimal.withdraw_stake_with_reset

Reset selected matured token holds and request withdrawal.

[WithdrawStakeWithResetRequest](../reference/decimal.md#withdrawstakewithresetrequest)

```python
import asyncio
import getpass
import json
import os
import time
from decimal_web3_sdk import (
    DecimalClient, NetworkConfig, mnemonic_to_account, WithdrawStakeWithResetRequest
)


async def main():
    mnemonic = getpass.getpass("Mnemonic (local, hidden): ")
    wallet = mnemonic_to_account(mnemonic, account_index=0)
    expected = os.environ["EXPECTED_ADDRESS"]
    if wallet.address.lower() != expected.lower():
        raise ValueError("Unexpected signing account")
    request = WithdrawStakeWithResetRequest.from_mnemonic(
        mnemonic=mnemonic,
        account_index=0,
        token=os.environ["TOKEN"],
        validator=os.environ["VALIDATOR"],
        amount="0.000001",
        hold_timestamps_to_reset=tuple(json.loads(os.environ["HOLD_TIMESTAMPS_TO_RESET"])),
    )
    async with DecimalClient(NetworkConfig.testnet()) as client:
        # Signs locally when preflight passes. NEVER broadcasts in this example.
        result = await client.decimal.withdraw_stake_with_reset(
            request, broadcast=False, wait_receipt=False
        )
        print("success:", result.success)
        print("fee_DEL:", str(result.fee_del))
        print("message:", result.user_message)
        print("tx_hash:", result.tx_hash)


if __name__ == "__main__":
    asyncio.run(main())
```
