# nft

[Guide](../README.md)

Полные примеры ниже используют testnet, требуют EXPECTED_ADDRESS и не отправляют транзакции. Остальные обязательные переменные окружения указаны в коде. Возможна локальная подпись; для расчета без подписи используйте раздел комиссий. Автоматический approve в примерах отключен. Контрактные методы требуют совместимого развернутого контракта и прав.

## nft.add_del_reserve

Пополнить резерв NFT нативным DEL.

[AddDelReserveNftRequest](../reference/nft.md#adddelreservenftrequest)

```python
import asyncio
import getpass
import json
import os
import time
from decimal_web3_sdk import (
    DecimalClient, NetworkConfig, mnemonic_to_account, AddDelReserveNftRequest
)


async def main():
    mnemonic = getpass.getpass("Mnemonic (local, hidden): ")
    wallet = mnemonic_to_account(mnemonic, account_index=0)
    expected = os.environ["EXPECTED_ADDRESS"]
    if wallet.address.lower() != expected.lower():
        raise ValueError("Unexpected signing account")
    request = AddDelReserveNftRequest.from_mnemonic(
        mnemonic=mnemonic,
        account_index=0,
        kind="erc721",
        nft=os.environ["NFT"],
        token_id=int(os.environ["TOKEN_ID"]),
        reserve_wei=1000000000000,
    )
    async with DecimalClient(NetworkConfig.testnet()) as client:
        # Signs locally when preflight passes. NEVER broadcasts in this example.
        result = await client.nft.add_del_reserve(
            request, broadcast=False, wait_receipt=False
        )
        print("success:", result.success)
        print("fee_DEL:", str(result.fee_del))
        print("message:", result.user_message)
        print("tx_hash:", result.tx_hash)


if __name__ == "__main__":
    asyncio.run(main())
```

## nft.add_token_reserve

Пополнить токен-резерв NFT в raw по существующему allowance либо переданному permit.

[AddTokenReserveNftRequest](../reference/nft_operations.md#addtokenreservenftrequest)

```python
import asyncio
import getpass
import json
import os
import time
from decimal_web3_sdk import (
    DecimalClient, NetworkConfig, mnemonic_to_account, AddTokenReserveNftRequest
)


async def main():
    mnemonic = getpass.getpass("Mnemonic (local, hidden): ")
    wallet = mnemonic_to_account(mnemonic, account_index=0)
    expected = os.environ["EXPECTED_ADDRESS"]
    if wallet.address.lower() != expected.lower():
        raise ValueError("Unexpected signing account")
    request = AddTokenReserveNftRequest.from_mnemonic(
        mnemonic=mnemonic,
        account_index=0,
        nft=os.environ["NFT"],
        token_id=int(os.environ["TOKEN_ID"]),
        reserve_amount_raw=1000000000000,
    )
    async with DecimalClient(NetworkConfig.testnet()) as client:
        # Signs locally when preflight passes. NEVER broadcasts in this example.
        result = await client.nft.add_token_reserve(
            request, broadcast=False, wait_receipt=False
        )
        print("success:", result.success)
        print("fee_DEL:", str(result.fee_del))
        print("message:", result.user_message)
        print("tx_hash:", result.tx_hash)


if __name__ == "__main__":
    asyncio.run(main())
```

## nft.approve

Разрешить оператору работу с одним ERC721 ID.

[NftApproveRequest](../reference/nft.md#nftapproverequest)

```python
import asyncio
import getpass
import json
import os
import time
from decimal_web3_sdk import (
    DecimalClient, NetworkConfig, mnemonic_to_account, NftApproveRequest
)


async def main():
    mnemonic = getpass.getpass("Mnemonic (local, hidden): ")
    wallet = mnemonic_to_account(mnemonic, account_index=0)
    expected = os.environ["EXPECTED_ADDRESS"]
    if wallet.address.lower() != expected.lower():
        raise ValueError("Unexpected signing account")
    request = NftApproveRequest.from_mnemonic(
        mnemonic=mnemonic,
        account_index=0,
        nft=os.environ["NFT"],
        to=wallet.address,
        token_id=int(os.environ["TOKEN_ID"]),
    )
    async with DecimalClient(NetworkConfig.testnet()) as client:
        # Signs locally when preflight passes. NEVER broadcasts in this example.
        result = await client.nft.approve(
            request, broadcast=False, wait_receipt=False
        )
        print("success:", result.success)
        print("fee_DEL:", str(result.fee_del))
        print("message:", result.user_message)
        print("tx_hash:", result.tx_hash)


if __name__ == "__main__":
    asyncio.run(main())
```

## nft.burn

Сжечь NFT; возврат резерва зависит от контракта коллекции.

[BurnNftRequest](../reference/nft.md#burnnftrequest)

```python
import asyncio
import getpass
import json
import os
import time
from decimal_web3_sdk import (
    DecimalClient, NetworkConfig, mnemonic_to_account, BurnNftRequest
)


async def main():
    mnemonic = getpass.getpass("Mnemonic (local, hidden): ")
    wallet = mnemonic_to_account(mnemonic, account_index=0)
    expected = os.environ["EXPECTED_ADDRESS"]
    if wallet.address.lower() != expected.lower():
        raise ValueError("Unexpected signing account")
    request = BurnNftRequest.from_mnemonic(
        mnemonic=mnemonic,
        account_index=0,
        kind="erc721",
        nft=os.environ["NFT"],
        token_id=int(os.environ["TOKEN_ID"]),
    )
    async with DecimalClient(NetworkConfig.testnet()) as client:
        # Signs locally when preflight passes. NEVER broadcasts in this example.
        result = await client.nft.burn(
            request, broadcast=False, wait_receipt=False
        )
        print("success:", result.success)
        print("fee_DEL:", str(result.fee_del))
        print("message:", result.user_message)
        print("tx_hash:", result.tx_hash)


if __name__ == "__main__":
    asyncio.run(main())
```

## nft.complete_stake

Завершить разморозку NFT-стейков по точным индексам очереди.

[CompleteNftStakeRequest](../reference/nft_operations.md#completenftstakerequest)

```python
import asyncio
import getpass
import json
import os
import time
from decimal_web3_sdk import (
    DecimalClient, NetworkConfig, mnemonic_to_account, CompleteNftStakeRequest
)


async def main():
    mnemonic = getpass.getpass("Mnemonic (local, hidden): ")
    wallet = mnemonic_to_account(mnemonic, account_index=0)
    expected = os.environ["EXPECTED_ADDRESS"]
    if wallet.address.lower() != expected.lower():
        raise ValueError("Unexpected signing account")
    request = CompleteNftStakeRequest.from_mnemonic(
        mnemonic=mnemonic,
        account_index=0,
        indexes=tuple(json.loads(os.environ["FROZEN_STAKE_INDEXES"])),
    )
    async with DecimalClient(NetworkConfig.testnet()) as client:
        # Signs locally when preflight passes. NEVER broadcasts in this example.
        result = await client.nft.complete_stake(
            request, broadcast=False, wait_receipt=False
        )
        print("success:", result.success)
        print("fee_DEL:", str(result.fee_del))
        print("message:", result.user_message)
        print("tx_hash:", result.tx_hash)


if __name__ == "__main__":
    asyncio.run(main())
```

## nft.create_collection

Создать NFT-коллекцию ERC721 или ERC1155.

[CreateNftCollectionRequest](../reference/nft.md#createnftcollectionrequest)

```python
import asyncio
import getpass
import json
import os
import time
from decimal_web3_sdk import (
    DecimalClient, NetworkConfig, mnemonic_to_account, CreateNftCollectionRequest
)


async def main():
    mnemonic = getpass.getpass("Mnemonic (local, hidden): ")
    wallet = mnemonic_to_account(mnemonic, account_index=0)
    expected = os.environ["EXPECTED_ADDRESS"]
    if wallet.address.lower() != expected.lower():
        raise ValueError("Unexpected signing account")
    request = CreateNftCollectionRequest.from_mnemonic(
        mnemonic=mnemonic,
        account_index=0,
        kind="erc721",
        symbol="EXAMPLE",
        name="Example token",
        contract_uri=os.environ["CONTRACT_URI"],
    )
    async with DecimalClient(NetworkConfig.testnet()) as client:
        # Signs locally when preflight passes. NEVER broadcasts in this example.
        result = await client.nft.create_collection(
            request, broadcast=False, wait_receipt=False
        )
        print("success:", result.success)
        print("fee_DEL:", str(result.fee_del))
        print("message:", result.user_message)
        print("tx_hash:", result.tx_hash)


if __name__ == "__main__":
    asyncio.run(main())
```

## nft.create_reserveless_collection

Создать DRC721/DRC1155 без резерва по текущему ABI NFTCenter.

[CreateReservelessNftCollectionRequest](../reference/nft_operations.md#createreservelessnftcollectionrequest)

```python
import asyncio
import getpass
import json
import os
import time
from decimal_web3_sdk import (
    DecimalClient, NetworkConfig, mnemonic_to_account, CreateReservelessNftCollectionRequest
)


async def main():
    mnemonic = getpass.getpass("Mnemonic (local, hidden): ")
    wallet = mnemonic_to_account(mnemonic, account_index=0)
    expected = os.environ["EXPECTED_ADDRESS"]
    if wallet.address.lower() != expected.lower():
        raise ValueError("Unexpected signing account")
    request = CreateReservelessNftCollectionRequest.from_mnemonic(
        mnemonic=mnemonic,
        account_index=0,
        kind="erc721",
        creator=wallet.address,
        symbol="EXAMPLE",
        name="Example token",
        contract_uri=os.environ["CONTRACT_URI"],
    )
    async with DecimalClient(NetworkConfig.testnet()) as client:
        # Signs locally when preflight passes. NEVER broadcasts in this example.
        result = await client.nft.create_reserveless_collection(
            request, broadcast=False, wait_receipt=False
        )
        print("success:", result.success)
        print("fee_DEL:", str(result.fee_del))
        print("message:", result.user_message)
        print("tx_hash:", result.tx_hash)


if __name__ == "__main__":
    asyncio.run(main())
```

## nft.delegate

Делегировать NFT; может потребоваться разрешение оператору коллекции.

[DelegateNftRequest](../reference/nft.md#delegatenftrequest)

```python
import asyncio
import getpass
import json
import os
import time
from decimal_web3_sdk import (
    DecimalClient, NetworkConfig, mnemonic_to_account, DelegateNftRequest
)


async def main():
    mnemonic = getpass.getpass("Mnemonic (local, hidden): ")
    wallet = mnemonic_to_account(mnemonic, account_index=0)
    expected = os.environ["EXPECTED_ADDRESS"]
    if wallet.address.lower() != expected.lower():
        raise ValueError("Unexpected signing account")
    request = DelegateNftRequest.from_mnemonic(
        mnemonic=mnemonic,
        account_index=0,
        kind="erc721",
        nft=os.environ["NFT"],
        validator=os.environ["VALIDATOR"],
        token_id=int(os.environ["TOKEN_ID"]),
        auto_approve=False,
    )
    async with DecimalClient(NetworkConfig.testnet()) as client:
        # Signs locally when preflight passes. NEVER broadcasts in this example.
        result = await client.nft.delegate(
            request, broadcast=False, wait_receipt=False
        )
        print("success:", result.success)
        print("fee_DEL:", str(result.fee_del))
        print("message:", result.user_message)
        print("tx_hash:", result.tx_hash)


if __name__ == "__main__":
    asyncio.run(main())
```

## nft.disable_mint

Отключить выпуск в коллекции; операция может быть необратимой.

[DisableMintNftRequest](../reference/nft.md#disablemintnftrequest)

```python
import asyncio
import getpass
import json
import os
import time
from decimal_web3_sdk import (
    DecimalClient, NetworkConfig, mnemonic_to_account, DisableMintNftRequest
)


async def main():
    mnemonic = getpass.getpass("Mnemonic (local, hidden): ")
    wallet = mnemonic_to_account(mnemonic, account_index=0)
    expected = os.environ["EXPECTED_ADDRESS"]
    if wallet.address.lower() != expected.lower():
        raise ValueError("Unexpected signing account")
    request = DisableMintNftRequest.from_mnemonic(
        mnemonic=mnemonic,
        account_index=0,
        kind="erc721",
        nft=os.environ["NFT"],
    )
    async with DecimalClient(NetworkConfig.testnet()) as client:
        # Signs locally when preflight passes. NEVER broadcasts in this example.
        result = await client.nft.disable_mint(
            request, broadcast=False, wait_receipt=False
        )
        print("success:", result.success)
        print("fee_DEL:", str(result.fee_del))
        print("message:", result.user_message)
        print("tx_hash:", result.tx_hash)


if __name__ == "__main__":
    asyncio.run(main())
```

## nft.hold

Делегировать NFT в hold; может потребоваться разрешение оператору.

[HoldNftRequest](../reference/nft.md#holdnftrequest)

```python
import asyncio
import getpass
import json
import os
import time
from decimal_web3_sdk import (
    DecimalClient, NetworkConfig, mnemonic_to_account, HoldNftRequest
)


async def main():
    mnemonic = getpass.getpass("Mnemonic (local, hidden): ")
    wallet = mnemonic_to_account(mnemonic, account_index=0)
    expected = os.environ["EXPECTED_ADDRESS"]
    if wallet.address.lower() != expected.lower():
        raise ValueError("Unexpected signing account")
    request = HoldNftRequest.from_mnemonic(
        mnemonic=mnemonic,
        account_index=0,
        kind="erc721",
        nft=os.environ["NFT"],
        validator=os.environ["VALIDATOR"],
        token_id=int(os.environ["TOKEN_ID"]),
        hold_timestamp=int(os.environ["HOLD_TIMESTAMP"]),
        auto_approve=False,
    )
    async with DecimalClient(NetworkConfig.testnet()) as client:
        # Signs locally when preflight passes. NEVER broadcasts in this example.
        result = await client.nft.hold(
            request, broadcast=False, wait_receipt=False
        )
        print("success:", result.success)
        print("fee_DEL:", str(result.fee_del))
        print("message:", result.user_message)
        print("tx_hash:", result.tx_hash)


if __name__ == "__main__":
    asyncio.run(main())
```

## nft.hold_with_reset

Сбросить выбранные NFT-hold и установить новый срок hold.

[HoldNftWithResetRequest](../reference/nft_operations.md#holdnftwithresetrequest)

```python
import asyncio
import getpass
import json
import os
import time
from decimal_web3_sdk import (
    DecimalClient, NetworkConfig, mnemonic_to_account, HoldNftWithResetRequest
)


async def main():
    mnemonic = getpass.getpass("Mnemonic (local, hidden): ")
    wallet = mnemonic_to_account(mnemonic, account_index=0)
    expected = os.environ["EXPECTED_ADDRESS"]
    if wallet.address.lower() != expected.lower():
        raise ValueError("Unexpected signing account")
    request = HoldNftWithResetRequest.from_mnemonic(
        mnemonic=mnemonic,
        account_index=0,
        validator=os.environ["VALIDATOR"],
        nft=os.environ["NFT"],
        token_id=int(os.environ["TOKEN_ID"]),
        amount=1,
        hold_timestamps_to_reset=tuple(json.loads(os.environ["HOLD_TIMESTAMPS_TO_RESET"])),
        new_hold_timestamp=int(os.environ["NEW_HOLD_TIMESTAMP"]),
    )
    async with DecimalClient(NetworkConfig.testnet()) as client:
        # Signs locally when preflight passes. NEVER broadcasts in this example.
        result = await client.nft.hold_with_reset(
            request, broadcast=False, wait_receipt=False
        )
        print("success:", result.success)
        print("fee_DEL:", str(result.fee_del))
        print("message:", result.user_message)
        print("tx_hash:", result.tx_hash)


if __name__ == "__main__":
    asyncio.run(main())
```

## nft.mint

Выпустить NFT с необязательным резервом; нужны права коллекции.

[MintNftRequest](../reference/nft.md#mintnftrequest)

```python
import asyncio
import getpass
import json
import os
import time
from decimal_web3_sdk import (
    DecimalClient, NetworkConfig, mnemonic_to_account, MintNftRequest
)


async def main():
    mnemonic = getpass.getpass("Mnemonic (local, hidden): ")
    wallet = mnemonic_to_account(mnemonic, account_index=0)
    expected = os.environ["EXPECTED_ADDRESS"]
    if wallet.address.lower() != expected.lower():
        raise ValueError("Unexpected signing account")
    request = MintNftRequest.from_mnemonic(
        mnemonic=mnemonic,
        account_index=0,
        kind="erc721",
        nft=os.environ["NFT"],
        to=wallet.address,
        token_uri=os.environ["TOKEN_URI"],
    )
    async with DecimalClient(NetworkConfig.testnet()) as client:
        # Signs locally when preflight passes. NEVER broadcasts in this example.
        result = await client.nft.mint(
            request, broadcast=False, wait_receipt=False
        )
        print("success:", result.success)
        print("fee_DEL:", str(result.fee_del))
        print("message:", result.user_message)
        print("tx_hash:", result.tx_hash)


if __name__ == "__main__":
    asyncio.run(main())
```

## nft.reset_stake_hold

Сбросить один доступный NFT-hold делегатора.

[ResetNftStakeHoldRequest](../reference/nft_operations.md#resetnftstakeholdrequest)

```python
import asyncio
import getpass
import json
import os
import time
from decimal_web3_sdk import (
    DecimalClient, NetworkConfig, mnemonic_to_account, ResetNftStakeHoldRequest
)


async def main():
    mnemonic = getpass.getpass("Mnemonic (local, hidden): ")
    wallet = mnemonic_to_account(mnemonic, account_index=0)
    expected = os.environ["EXPECTED_ADDRESS"]
    if wallet.address.lower() != expected.lower():
        raise ValueError("Unexpected signing account")
    request = ResetNftStakeHoldRequest.from_mnemonic(
        mnemonic=mnemonic,
        account_index=0,
        validator=os.environ["VALIDATOR"],
        nft=os.environ["NFT"],
        token_id=int(os.environ["TOKEN_ID"]),
        delegator=wallet.address,
        hold_timestamp=int(os.environ["HOLD_TIMESTAMP"]),
    )
    async with DecimalClient(NetworkConfig.testnet()) as client:
        # Signs locally when preflight passes. NEVER broadcasts in this example.
        result = await client.nft.reset_stake_hold(
            request, broadcast=False, wait_receipt=False
        )
        print("success:", result.success)
        print("fee_DEL:", str(result.fee_del))
        print("message:", result.user_message)
        print("tx_hash:", result.tx_hash)


if __name__ == "__main__":
    asyncio.run(main())
```

## nft.reset_stake_holds

Сбросить несколько доступных NFT-hold, как в новой ветке JS SDK.

[ResetNftStakeHoldsRequest](../reference/nft_operations.md#resetnftstakeholdsrequest)

```python
import asyncio
import getpass
import json
import os
import time
from decimal_web3_sdk import (
    DecimalClient, NetworkConfig, mnemonic_to_account, ResetNftStakeHoldsRequest
)


async def main():
    mnemonic = getpass.getpass("Mnemonic (local, hidden): ")
    wallet = mnemonic_to_account(mnemonic, account_index=0)
    expected = os.environ["EXPECTED_ADDRESS"]
    if wallet.address.lower() != expected.lower():
        raise ValueError("Unexpected signing account")
    request = ResetNftStakeHoldsRequest.from_mnemonic(
        mnemonic=mnemonic,
        account_index=0,
        validator=os.environ["VALIDATOR"],
        nft=os.environ["NFT"],
        token_id=int(os.environ["TOKEN_ID"]),
        delegator=wallet.address,
        hold_timestamps=tuple(json.loads(os.environ["HOLD_TIMESTAMPS"])),
    )
    async with DecimalClient(NetworkConfig.testnet()) as client:
        # Signs locally when preflight passes. NEVER broadcasts in this example.
        result = await client.nft.reset_stake_holds(
            request, broadcast=False, wait_receipt=False
        )
        print("success:", result.success)
        print("fee_DEL:", str(result.fee_del))
        print("message:", result.user_message)
        print("tx_hash:", result.tx_hash)


if __name__ == "__main__":
    asyncio.run(main())
```

## nft.set_approval_for_all

Выдать или отменить полномочия NFT-оператора для коллекции.

[NftApprovalRequest](../reference/nft.md#nftapprovalrequest)

```python
import asyncio
import getpass
import json
import os
import time
from decimal_web3_sdk import (
    DecimalClient, NetworkConfig, mnemonic_to_account, NftApprovalRequest
)


async def main():
    mnemonic = getpass.getpass("Mnemonic (local, hidden): ")
    wallet = mnemonic_to_account(mnemonic, account_index=0)
    expected = os.environ["EXPECTED_ADDRESS"]
    if wallet.address.lower() != expected.lower():
        raise ValueError("Unexpected signing account")
    request = NftApprovalRequest.from_mnemonic(
        mnemonic=mnemonic,
        account_index=0,
        kind="erc721",
        nft=os.environ["NFT"],
        operator=os.environ["OPERATOR"],
        approved=False,
    )
    async with DecimalClient(NetworkConfig.testnet()) as client:
        # Signs locally when preflight passes. NEVER broadcasts in this example.
        result = await client.nft.set_approval_for_all(
            request, broadcast=False, wait_receipt=False
        )
        print("success:", result.success)
        print("fee_DEL:", str(result.fee_del))
        print("message:", result.user_message)
        print("tx_hash:", result.tx_hash)


if __name__ == "__main__":
    asyncio.run(main())
```

## nft.set_token_uri

Обновить URI метаданных NFT; нужны права контракта.

[SetTokenUriNftRequest](../reference/nft.md#settokenurinftrequest)

```python
import asyncio
import getpass
import json
import os
import time
from decimal_web3_sdk import (
    DecimalClient, NetworkConfig, mnemonic_to_account, SetTokenUriNftRequest
)


async def main():
    mnemonic = getpass.getpass("Mnemonic (local, hidden): ")
    wallet = mnemonic_to_account(mnemonic, account_index=0)
    expected = os.environ["EXPECTED_ADDRESS"]
    if wallet.address.lower() != expected.lower():
        raise ValueError("Unexpected signing account")
    request = SetTokenUriNftRequest.from_mnemonic(
        mnemonic=mnemonic,
        account_index=0,
        kind="erc721",
        nft=os.environ["NFT"],
        token_id=int(os.environ["TOKEN_ID"]),
        token_uri=os.environ["TOKEN_URI"],
    )
    async with DecimalClient(NetworkConfig.testnet()) as client:
        # Signs locally when preflight passes. NEVER broadcasts in this example.
        result = await client.nft.set_token_uri(
            request, broadcast=False, wait_receipt=False
        )
        print("success:", result.success)
        print("fee_DEL:", str(result.fee_del))
        print("message:", result.user_message)
        print("tx_hash:", result.tx_hash)


if __name__ == "__main__":
    asyncio.run(main())
```

## nft.stake_to_hold

Перевести существующий NFT-стейк в hold через delegation-nft.

[StakeNftToHoldRequest](../reference/nft_operations.md#stakenfttoholdrequest)

```python
import asyncio
import getpass
import json
import os
import time
from decimal_web3_sdk import (
    DecimalClient, NetworkConfig, mnemonic_to_account, StakeNftToHoldRequest
)


async def main():
    mnemonic = getpass.getpass("Mnemonic (local, hidden): ")
    wallet = mnemonic_to_account(mnemonic, account_index=0)
    expected = os.environ["EXPECTED_ADDRESS"]
    if wallet.address.lower() != expected.lower():
        raise ValueError("Unexpected signing account")
    request = StakeNftToHoldRequest.from_mnemonic(
        mnemonic=mnemonic,
        account_index=0,
        validator=os.environ["VALIDATOR"],
        nft=os.environ["NFT"],
        token_id=int(os.environ["TOKEN_ID"]),
        amount=1,
        old_hold_timestamp=int(os.environ["OLD_HOLD_TIMESTAMP"]),
        new_hold_timestamp=int(os.environ["NEW_HOLD_TIMESTAMP"]),
    )
    async with DecimalClient(NetworkConfig.testnet()) as client:
        # Signs locally when preflight passes. NEVER broadcasts in this example.
        result = await client.nft.stake_to_hold(
            request, broadcast=False, wait_receipt=False
        )
        print("success:", result.success)
        print("fee_DEL:", str(result.fee_del))
        print("message:", result.user_message)
        print("tx_hash:", result.tx_hash)


if __name__ == "__main__":
    asyncio.run(main())
```

## nft.transfer

Передать NFT ERC721 или ERC1155 получателю.

[NftTransferRequest](../reference/nft.md#nfttransferrequest)

```python
import asyncio
import getpass
import json
import os
import time
from decimal_web3_sdk import (
    DecimalClient, NetworkConfig, mnemonic_to_account, NftTransferRequest
)


async def main():
    mnemonic = getpass.getpass("Mnemonic (local, hidden): ")
    wallet = mnemonic_to_account(mnemonic, account_index=0)
    expected = os.environ["EXPECTED_ADDRESS"]
    if wallet.address.lower() != expected.lower():
        raise ValueError("Unexpected signing account")
    request = NftTransferRequest.from_mnemonic(
        mnemonic=mnemonic,
        account_index=0,
        kind="erc721",
        nft=os.environ["NFT"],
        to=wallet.address,
        token_id=int(os.environ["TOKEN_ID"]),
    )
    async with DecimalClient(NetworkConfig.testnet()) as client:
        # Signs locally when preflight passes. NEVER broadcasts in this example.
        result = await client.nft.transfer(
            request, broadcast=False, wait_receipt=False
        )
        print("success:", result.success)
        print("fee_DEL:", str(result.fee_del))
        print("message:", result.user_message)
        print("tx_hash:", result.tx_hash)


if __name__ == "__main__":
    asyncio.run(main())
```

## nft.transfer_batch_erc1155

Передать списки ID и количеств ERC1155 одним вызовом.

[NftBatchTransferRequest](../reference/nft.md#nftbatchtransferrequest)

```python
import asyncio
import getpass
import json
import os
import time
from decimal_web3_sdk import (
    DecimalClient, NetworkConfig, mnemonic_to_account, NftBatchTransferRequest
)


async def main():
    mnemonic = getpass.getpass("Mnemonic (local, hidden): ")
    wallet = mnemonic_to_account(mnemonic, account_index=0)
    expected = os.environ["EXPECTED_ADDRESS"]
    if wallet.address.lower() != expected.lower():
        raise ValueError("Unexpected signing account")
    request = NftBatchTransferRequest.from_mnemonic(
        mnemonic=mnemonic,
        account_index=0,
        nft=os.environ["NFT"],
        to=wallet.address,
        token_ids=[1, 2],
        amounts=[1, 1],
    )
    async with DecimalClient(NetworkConfig.testnet()) as client:
        # Signs locally when preflight passes. NEVER broadcasts in this example.
        result = await client.nft.transfer_batch_erc1155(
            request, broadcast=False, wait_receipt=False
        )
        print("success:", result.success)
        print("fee_DEL:", str(result.fee_del))
        print("message:", result.user_message)
        print("tx_hash:", result.tx_hash)


if __name__ == "__main__":
    asyncio.run(main())
```

## nft.transfer_stake

Перенести обычный или удерживаемый NFT-стейк другому валидатору.

[TransferNftStakeRequest](../reference/nft.md#transfernftstakerequest)

```python
import asyncio
import getpass
import json
import os
import time
from decimal_web3_sdk import (
    DecimalClient, NetworkConfig, mnemonic_to_account, TransferNftStakeRequest
)


async def main():
    mnemonic = getpass.getpass("Mnemonic (local, hidden): ")
    wallet = mnemonic_to_account(mnemonic, account_index=0)
    expected = os.environ["EXPECTED_ADDRESS"]
    if wallet.address.lower() != expected.lower():
        raise ValueError("Unexpected signing account")
    request = TransferNftStakeRequest.from_mnemonic(
        mnemonic=mnemonic,
        account_index=0,
        nft=os.environ["NFT"],
        validator=os.environ["VALIDATOR"],
        new_validator=os.environ["NEW_VALIDATOR"],
        token_id=int(os.environ["TOKEN_ID"]),
    )
    async with DecimalClient(NetworkConfig.testnet()) as client:
        # Signs locally when preflight passes. NEVER broadcasts in this example.
        result = await client.nft.transfer_stake(
            request, broadcast=False, wait_receipt=False
        )
        print("success:", result.success)
        print("fee_DEL:", str(result.fee_del))
        print("message:", result.user_message)
        print("tx_hash:", result.tx_hash)


if __name__ == "__main__":
    asyncio.run(main())
```

## nft.transfer_with_reset

Сбросить выбранные NFT-hold и запросить перенос другому валидатору.

[TransferNftWithResetRequest](../reference/nft_operations.md#transfernftwithresetrequest)

```python
import asyncio
import getpass
import json
import os
import time
from decimal_web3_sdk import (
    DecimalClient, NetworkConfig, mnemonic_to_account, TransferNftWithResetRequest
)


async def main():
    mnemonic = getpass.getpass("Mnemonic (local, hidden): ")
    wallet = mnemonic_to_account(mnemonic, account_index=0)
    expected = os.environ["EXPECTED_ADDRESS"]
    if wallet.address.lower() != expected.lower():
        raise ValueError("Unexpected signing account")
    request = TransferNftWithResetRequest.from_mnemonic(
        mnemonic=mnemonic,
        account_index=0,
        validator=os.environ["VALIDATOR"],
        nft=os.environ["NFT"],
        token_id=int(os.environ["TOKEN_ID"]),
        amount=1,
        hold_timestamps_to_reset=tuple(json.loads(os.environ["HOLD_TIMESTAMPS_TO_RESET"])),
        new_validator=os.environ["NEW_VALIDATOR"],
    )
    async with DecimalClient(NetworkConfig.testnet()) as client:
        # Signs locally when preflight passes. NEVER broadcasts in this example.
        result = await client.nft.transfer_with_reset(
            request, broadcast=False, wait_receipt=False
        )
        print("success:", result.success)
        print("fee_DEL:", str(result.fee_del))
        print("message:", result.user_message)
        print("tx_hash:", result.tx_hash)


if __name__ == "__main__":
    asyncio.run(main())
```

## nft.withdraw

Инициировать отзыв обычного или созревшего удерживаемого NFT-стейка.

[WithdrawNftRequest](../reference/nft.md#withdrawnftrequest)

```python
import asyncio
import getpass
import json
import os
import time
from decimal_web3_sdk import (
    DecimalClient, NetworkConfig, mnemonic_to_account, WithdrawNftRequest
)


async def main():
    mnemonic = getpass.getpass("Mnemonic (local, hidden): ")
    wallet = mnemonic_to_account(mnemonic, account_index=0)
    expected = os.environ["EXPECTED_ADDRESS"]
    if wallet.address.lower() != expected.lower():
        raise ValueError("Unexpected signing account")
    request = WithdrawNftRequest.from_mnemonic(
        mnemonic=mnemonic,
        account_index=0,
        nft=os.environ["NFT"],
        validator=os.environ["VALIDATOR"],
        token_id=int(os.environ["TOKEN_ID"]),
    )
    async with DecimalClient(NetworkConfig.testnet()) as client:
        # Signs locally when preflight passes. NEVER broadcasts in this example.
        result = await client.nft.withdraw(
            request, broadcast=False, wait_receipt=False
        )
        print("success:", result.success)
        print("fee_DEL:", str(result.fee_del))
        print("message:", result.user_message)
        print("tx_hash:", result.tx_hash)


if __name__ == "__main__":
    asyncio.run(main())
```

## nft.withdraw_with_reset

Сбросить выбранные NFT-hold и запросить вывод; завершение остается отдельным шагом.

[WithdrawNftWithResetRequest](../reference/nft_operations.md#withdrawnftwithresetrequest)

```python
import asyncio
import getpass
import json
import os
import time
from decimal_web3_sdk import (
    DecimalClient, NetworkConfig, mnemonic_to_account, WithdrawNftWithResetRequest
)


async def main():
    mnemonic = getpass.getpass("Mnemonic (local, hidden): ")
    wallet = mnemonic_to_account(mnemonic, account_index=0)
    expected = os.environ["EXPECTED_ADDRESS"]
    if wallet.address.lower() != expected.lower():
        raise ValueError("Unexpected signing account")
    request = WithdrawNftWithResetRequest.from_mnemonic(
        mnemonic=mnemonic,
        account_index=0,
        validator=os.environ["VALIDATOR"],
        nft=os.environ["NFT"],
        token_id=int(os.environ["TOKEN_ID"]),
        amount=1,
        hold_timestamps_to_reset=tuple(json.loads(os.environ["HOLD_TIMESTAMPS_TO_RESET"])),
    )
    async with DecimalClient(NetworkConfig.testnet()) as client:
        # Signs locally when preflight passes. NEVER broadcasts in this example.
        result = await client.nft.withdraw_with_reset(
            request, broadcast=False, wait_receipt=False
        )
        print("success:", result.success)
        print("fee_DEL:", str(result.fee_del))
        print("message:", result.user_message)
        print("tx_hash:", result.tx_hash)


if __name__ == "__main__":
    asyncio.run(main())
```
