# multisig

[Guide](../README.md)

Полные примеры ниже используют testnet, требуют EXPECTED_ADDRESS и не отправляют транзакции. Остальные обязательные переменные окружения указаны в коде. Возможна локальная подпись; для расчета без подписи используйте раздел комиссий. Автоматический approve в примерах отключен. Контрактные методы требуют совместимого развернутого контракта и прав.

## multisig.approve_transaction

Подтвердить полный tuple транзакции Safe в сети; расходует gas.

[ApproveMultisigTransactionRequest](../reference/multisig.md#approvemultisigtransactionrequest)

```python
import asyncio
import getpass
import json
import os
import time
from decimal_web3_sdk import (
    DecimalClient, NetworkConfig, mnemonic_to_account, ApproveMultisigTransactionRequest, SafeTransaction
)


async def main():
    mnemonic = getpass.getpass("Mnemonic (local, hidden): ")
    wallet = mnemonic_to_account(mnemonic, account_index=0)
    expected = os.environ["EXPECTED_ADDRESS"]
    if wallet.address.lower() != expected.lower():
        raise ValueError("Unexpected signing account")
    request = ApproveMultisigTransactionRequest.from_mnemonic(
        mnemonic=mnemonic,
        account_index=0,
        safe=os.environ["SAFE_ADDRESS"],
        transaction=SafeTransaction(**json.loads(os.environ["SAFE_TRANSACTION"])),
    )
    async with DecimalClient(NetworkConfig.testnet()) as client:
        # Signs locally when preflight passes. NEVER broadcasts in this example.
        result = await client.multisig.approve_transaction(
            request, broadcast=False, wait_receipt=False
        )
        print("success:", result.success)
        print("fee_DEL:", str(result.fee_del))
        print("message:", result.user_message)
        print("tx_hash:", result.tx_hash)


if __name__ == "__main__":
    asyncio.run(main())
```

## multisig.create

Создать взвешенный Decimal Safe через SafeFactory с явным salt.

[CreateMultisigRequest](../reference/multisig.md#createmultisigrequest)

```python
import asyncio
import getpass
import json
import os
import time
from decimal_web3_sdk import (
    DecimalClient, NetworkConfig, mnemonic_to_account, CreateMultisigRequest, WeightedOwner
)


async def main():
    mnemonic = getpass.getpass("Mnemonic (local, hidden): ")
    wallet = mnemonic_to_account(mnemonic, account_index=0)
    expected = os.environ["EXPECTED_ADDRESS"]
    if wallet.address.lower() != expected.lower():
        raise ValueError("Unexpected signing account")
    request = CreateMultisigRequest.from_mnemonic(
        mnemonic=mnemonic,
        account_index=0,
        owners=tuple(WeightedOwner(**item) for item in json.loads(os.environ["SAFE_OWNERS"])),
        weight_threshold=int(os.environ["WEIGHT_THRESHOLD"]),
        salt_nonce=int(os.environ["SALT_NONCE"]),
    )
    async with DecimalClient(NetworkConfig.testnet()) as client:
        # Signs locally when preflight passes. NEVER broadcasts in this example.
        result = await client.multisig.create(
            request, broadcast=False, wait_receipt=False
        )
        print("success:", result.success)
        print("fee_DEL:", str(result.fee_del))
        print("message:", result.user_message)
        print("tx_hash:", result.tx_hash)


if __name__ == "__main__":
    asyncio.run(main())
```

## multisig.execute

Выполнить Safe-транзакцию после проверки nonce, подписей и весов; проверить внутренний результат.

[ExecuteMultisigTransactionRequest](../reference/multisig.md#executemultisigtransactionrequest)

```python
import asyncio
import getpass
import json
import os
import time
from decimal_web3_sdk import (
    DecimalClient, NetworkConfig, mnemonic_to_account, ExecuteMultisigTransactionRequest, SafeTransaction, SafeSignature
)


async def main():
    mnemonic = getpass.getpass("Mnemonic (local, hidden): ")
    wallet = mnemonic_to_account(mnemonic, account_index=0)
    expected = os.environ["EXPECTED_ADDRESS"]
    if wallet.address.lower() != expected.lower():
        raise ValueError("Unexpected signing account")
    request = ExecuteMultisigTransactionRequest.from_mnemonic(
        mnemonic=mnemonic,
        account_index=0,
        safe=os.environ["SAFE_ADDRESS"],
        transaction=SafeTransaction(**json.loads(os.environ["SAFE_TRANSACTION"])),
        signatures=tuple(SafeSignature(**item) for item in json.loads(os.environ["SAFE_SIGNATURES"])),
    )
    async with DecimalClient(NetworkConfig.testnet()) as client:
        # Signs locally when preflight passes. NEVER broadcasts in this example.
        result = await client.multisig.execute(
            request, broadcast=False, wait_receipt=False
        )
        print("success:", result.success)
        print("fee_DEL:", str(result.fee_del))
        print("message:", result.user_message)
        print("tx_hash:", result.tx_hash)


if __name__ == "__main__":
    asyncio.run(main())
```
