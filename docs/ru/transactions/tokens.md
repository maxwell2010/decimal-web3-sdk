# tokens

[Guide](../README.md)

Полные примеры ниже используют testnet, требуют EXPECTED_ADDRESS и не отправляют транзакции. Остальные обязательные переменные окружения указаны в коде. Возможна локальная подпись; для расчета без подписи используйте раздел комиссий. Автоматический approve в примерах отключен. Контрактные методы требуют совместимого развернутого контракта и прав.

## tx.approve_erc20

Установить лимит расходования для spender; ноль отменяет разрешение.

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

Перевод ERC20 от подписанта; approve не требуется.

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

Перевод токенов владельца по ранее выданному разрешению подписанту.

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

Рассылка ERC20 через multicall; при необходимости permit либо отдельный approve. Поддерживается memo.

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

Сжечь принадлежащие подписанту взаимозаменяемые токены.

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

Купить резервный токен за DEL с нижней границей выхода.

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

## token.buy_exact

Купить точное количество токена в raw-единицах с максимальным расходом DEL.

[BuyExactTokenRequest](../reference/token_operations.md#buyexacttokenrequest)

```python
import asyncio
import getpass
import json
import os
import time
from decimal_web3_sdk import (
    DecimalClient, NetworkConfig, mnemonic_to_account, BuyExactTokenRequest
)


async def main():
    mnemonic = getpass.getpass("Mnemonic (local, hidden): ")
    wallet = mnemonic_to_account(mnemonic, account_index=0)
    expected = os.environ["EXPECTED_ADDRESS"]
    if wallet.address.lower() != expected.lower():
        raise ValueError("Unexpected signing account")
    request = BuyExactTokenRequest.from_mnemonic(
        mnemonic=mnemonic,
        account_index=0,
        token=os.environ["TOKEN"],
        recipient=wallet.address,
        amount_out_raw=1000000000000,
        max_amount_del="0.000001",
    )
    async with DecimalClient(NetworkConfig.testnet()) as client:
        # Signs locally when preflight passes. NEVER broadcasts in this example.
        result = await client.token.buy_exact(
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

Обменять токены с минимальным выходом; возможны permit или две транзакции.

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

## token.convert_to_del

Конвертация GasCenter с permit владельца; не обычная продажа токена.

[ConvertToDelRequest](../reference/token_operations.md#converttodelrequest)

```python
import asyncio
import getpass
import json
import os
import time
from decimal_web3_sdk import (
    DecimalClient, NetworkConfig, mnemonic_to_account, ConvertToDelRequest, PermitSignature
)


async def main():
    mnemonic = getpass.getpass("Mnemonic (local, hidden): ")
    wallet = mnemonic_to_account(mnemonic, account_index=0)
    expected = os.environ["EXPECTED_ADDRESS"]
    if wallet.address.lower() != expected.lower():
        raise ValueError("Unexpected signing account")
    request = ConvertToDelRequest.from_mnemonic(
        mnemonic=mnemonic,
        account_index=0,
        owner=wallet.address,
        token=os.environ["TOKEN"],
        amount_raw=1000000000000,
        estimated_gas=int(os.environ["ESTIMATED_GAS"]),
        permit=PermitSignature(deadline=int(os.environ["PERMIT_DEADLINE"]), v=int(os.environ["PERMIT_V"]), r=bytes.fromhex(os.environ["PERMIT_R"].removeprefix("0x")), s=bytes.fromhex(os.environ["PERMIT_S"].removeprefix("0x"))),
    )
    async with DecimalClient(NetworkConfig.testnet()) as client:
        # Signs locally when preflight passes. NEVER broadcasts in this example.
        result = await client.token.convert_to_del(
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

Создать резервный токен; начальный резерв и комиссия создания не являются gas-комиссией.

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

Создать безрезервный токен с флагами выпуска/сжигания и пределом эмиссии.

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

Выпустить токены получателю; нужны права эмитента.

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

Продать резервный токен за DEL с нижней границей выхода.

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

## token.sell_for_exact_del

Продать токен для точного выхода DEL с максимальным расходом токенов в raw.

[SellForExactDelRequest](../reference/token_operations.md#sellforexactdelrequest)

```python
import asyncio
import getpass
import json
import os
import time
from decimal_web3_sdk import (
    DecimalClient, NetworkConfig, mnemonic_to_account, SellForExactDelRequest
)


async def main():
    mnemonic = getpass.getpass("Mnemonic (local, hidden): ")
    wallet = mnemonic_to_account(mnemonic, account_index=0)
    expected = os.environ["EXPECTED_ADDRESS"]
    if wallet.address.lower() != expected.lower():
        raise ValueError("Unexpected signing account")
    request = SellForExactDelRequest.from_mnemonic(
        mnemonic=mnemonic,
        account_index=0,
        token=os.environ["TOKEN"],
        recipient=wallet.address,
        amount_out_del="0.000001",
        max_amount_in_raw=1000000000000,
    )
    async with DecimalClient(NetworkConfig.testnet()) as client:
        # Signs locally when preflight passes. NEVER broadcasts in this example.
        result = await client.token.sell_for_exact_del(
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

Обновить identity и предел эмиссии токена; нужны права эмитента.

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

## token.update_min_supply

Legacy-изменение минимальной эмиссии; по умолчанию отключено.

[UpdateTokenMinSupplyRequest](../reference/token_operations.md#updatetokenminsupplyrequest)

```python
import asyncio
import getpass
import json
import os
import time
from decimal_web3_sdk import (
    DecimalClient, NetworkConfig, mnemonic_to_account, UpdateTokenMinSupplyRequest
)


async def main():
    mnemonic = getpass.getpass("Mnemonic (local, hidden): ")
    wallet = mnemonic_to_account(mnemonic, account_index=0)
    expected = os.environ["EXPECTED_ADDRESS"]
    if wallet.address.lower() != expected.lower():
        raise ValueError("Unexpected signing account")
    request = UpdateTokenMinSupplyRequest.from_mnemonic(
        mnemonic=mnemonic,
        account_index=0,
        token=os.environ["TOKEN"],
        min_total_supply_raw=1000000000000,
        allow_legacy=os.environ.get("ALLOW_LEGACY_CONTRACT", "0") == "1",
    )
    async with DecimalClient(NetworkConfig.testnet()) as client:
        # Signs locally when preflight passes. NEVER broadcasts in this example.
        result = await client.token.update_min_supply(
            request, broadcast=False, wait_receipt=False
        )
        print("success:", result.success)
        print("fee_DEL:", str(result.fee_del))
        print("message:", result.user_message)
        print("tx_hash:", result.tx_hash)


if __name__ == "__main__":
    asyncio.run(main())
```
