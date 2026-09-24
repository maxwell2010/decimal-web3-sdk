# Текущий Протокол NFT
[Оглавление](README.md) | [Транзакции](transactions/nft.md)

Проверка протокола началась 2026-09-16. В 0.1.3 вошли исправления и подтверждены
создание, выпуск, перевод и сжигание DRC721/DRC1155 в тестовой сети.
[Хеши транзакций](../validation/testnet-transaction-campaign-2026-09-24.md).
Стейкинг NFT и все методы в майнете этим не подтверждены.

## Коллекция И Экземпляр
create_collection вызывает createDRC721/createDRC1155 для резервной коллекции.
create_reserveless_collection вызывает варианты Reserveless. Tuple общий:
creator, symbol, name, contractURI, refundable, burnable. Создание не вносит резерв
и не выпускает NFT. Символ относится к коллекции, а не к залоговому ERC20.

client.nft.created_collections(receipt) декодирует NFTCreated только от настроенного
NFTCenter. Сверяйте creator, kind, symbol, name, URI с запросом; нельзя брать первое
попавшееся событие multicall. Успех транзакции не доказывает mint. Метод не выдумывает
ID 1 или баланс. Владение проверяется balance_of/owner_of, режим - collection_state.

В [проверенном примере](../validation/nft-protocol-sync.md) создана пустая безрезервная
коллекция. Превратить ее в резервную нельзя. Выпуск NFT - отдельная транзакция,
которая требует отдельного подтверждения.

## Резерв И Выпуск
- DEL: общий резерв задается value_wei, вызывается payable mintByDEL. Остальные
  reserve-поля нулевые. Approve не нужен.
- ERC20: reserve_amount_raw - общий резерв в минимальных единицах токена,
  reserve_token - адрес токена, value_wei=0. NFTCenter.checkToken должен принять токен.
  Allowance выдается коллекции NFT, не NFTCenter.
- Без резерва: все reserve-поля нулевые. Иначе SDK отклоняет запрос, а не игнорирует
  резерв с выпуском фактически необеспеченного NFT.
- DRC721 выпускает один автоматически назначенный ID: amount=1, token_id=None.
- DRC1155: amount - число копий одного явного ID, включая ID 0. Резерв задается
  ЗА ВЕСЬ выпуск, а не за одну копию.
- Проверенный MIN_RESERVE=1000000000000000 raw на новый NFT/копию. Это не всегда
  0.001 токена в отображении: нужно учитывать decimals выбранного актива.
  build_mint читает минимум контракта и считает целыми числами.
- Для существующего DRC1155 ID сохраняются тип И адрес залогового токена;
  общая сумма должна быть rate(id) * amount. get_reserve возвращает точные raw-числа.

SDK проверяет адрес залога дополнительно: проверенный контракт при допвыпуске
проверяет только тип и rate. Ошибка RPC/checkToken не считается успешной проверкой.
Перед подписью необходим свежий estimateGas: состояние может измениться. Нужны
права на mint и достаточный баланс для резерва и газа.

## Без Подписи
Полный [пример подготовки](../en/nft-protocol.md#unsigned-preparation) создает
CreateNftCollectionRequest и MintNftRequest из локальной mnemonic, затем вызывает
build_create_collection/build_mint и calculate_fee(exact=True). Сетевых подписей,
approve, публикации метаданных и отправок в нем нет. По умолчанию используется mainnet.
Не передавайте адрес будущей коллекции в mint до ее отдельного подтверждения.

```python
import asyncio
import os
from decimal_web3_sdk import DecimalClient, MintNftRequest

async def main():
    async with DecimalClient() as client:
        request = MintNftRequest.from_mnemonic(
            mnemonic=os.environ["MNEMONIC"], kind="erc1155",
            nft=os.environ["NFT_ADDRESS"], to=os.environ["RECIPIENT"],
            token_uri=os.environ["TOKEN_URI"], token_id=0, amount=3,
            value_wei=3000000000000000,
        )
        draft = await client.nft.build_mint(request)
        fee = await client.tx.calculate_fee(draft, exact=True)
        print(fee.estimated_fee_del)

asyncio.run(main())
```

Для ERC20 проверьте client.erc20.allowance(token, owner, collection). При нехватке
подготовьте отдельный Erc20ApproveRequest: spender=collection, amount - ТОЧНАЯ общая
сумма через format_units_string(total_raw, decimals). build_erc20_approve и calculate_fee
ничего не отправляют. Approve подтверждается отдельно, затем mint собирается и
оценивается заново. Ошибка расчета mint без allowance не означает нулевую комиссию;
комиссия approve не покрывает обе операции. Нет неявного бесконечного approve или
автоматической второй подписи.

## Общий Профиль
Канонические ABI: nft_center.json, nft_721.json и nft_1155.json в src/decimal_web3_sdk/abi.
В каждом записаны официальный источник, implementation и хеш исходника. Из корня SDK:

```shell
python scripts/generate_nft_profile.py
python scripts/generate_nft_profile.py --check
```

Результат: src/decimal_web3_sdk/profiles/candy_mainnet_v1.json. Профиль только mainnet;
метаданные используют refundable, не allowMint. Python builder и профиль используют
одни проверенные ABI. Автозагрузки/исполнения удаленных ABI/исходников при работе SDK нет.
set_token_uri оставлен как legacy: в текущих ABI setTokenURI отсутствует, а
allow_legacy=True допустим лишь для независимо проверенного старого контракта.
