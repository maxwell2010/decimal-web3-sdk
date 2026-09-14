# checks

[Guide](../README.md)

Полные примеры ниже используют testnet, требуют EXPECTED_ADDRESS и не отправляют транзакции. Остальные обязательные переменные окружения указаны в коде. Возможна локальная подпись; для расчета без подписи используйте раздел комиссий. Автоматический approve в примерах отключен. Контрактные методы требуют совместимого развернутого контракта и прав.

## checks.create_del

Создать DEL-чеки одинакового номинала для адресов подписантов; value равен номиналу на число чеков.

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

Создать токен-чеки по существующему allowance или явно переданному permit.

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

Погасить чеки по соответствующим хешам и подписям.

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
