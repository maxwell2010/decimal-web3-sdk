# bridge

[Guide](../README.md)

Полные примеры ниже используют testnet, требуют EXPECTED_ADDRESS и не отправляют транзакции. Остальные обязательные переменные окружения указаны в коде. Возможна локальная подпись; для расчета без подписи используйте раздел комиссий. Автоматический approve в примерах отключен. Контрактные методы требуют совместимого развернутого контракта и прав.

## bridge.complete_transfer

Завершить мостовой перевод с проверенным encoded VM, полученным от моста.

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

Начать мостовой перевод нативной монеты; завершение в целевой сети выполняется отдельно.

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

Начать мостовой перевод токена; allowance и сервисную комиссию обеспечивает вызывающий.

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
