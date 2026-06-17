# Python SDK

Reference package: `decimal-web3-sdk`.

Документация построена в привычной логике официального Decimal Python SDK: wallet/request -> расчет комиссии -> подпись -> broadcast -> проверка результата. Отличие текущего SDK в том, что транзакционный слой работает через Decimal EVM/Web3.

## Назначение

Python SDK является основной реализацией Decimal Web3 SDK для локальных скриптов, серверных задач, CLI, тестового кошелька, мониторинга, обучения транзакций и будущей автоматизации.

SDK не привязан к инфраструктуре MintCandy. Для продакшена указывайте свои Decimal Web3/API/WS endpoint-ы или публичные endpoint-ы Decimal, если они подходят под вашу нагрузку.

## Установка

```powershell
python -m venv .venv
.\.venv\Scripts\activate
pip install -e ".[dev]"
```

После релиза:

```powershell
pip install decimal-web3-sdk
```

## Конфигурация сети

Mainnet:

```python
from decimal_web3_sdk import NetworkConfig

config = NetworkConfig.mainnet()
```

По умолчанию используется официальный Web3 RPC:

```text
https://node.decimalchain.com/web3/
```

REST API задается явно, потому что API-gateway зависит от выбранной инфраструктуры:

```python
config = NetworkConfig.custom(
    chain_id=75,
    web3_urls=["https://your-node.example/web3/"],
    api_root_url="https://your-api.example",
    api_base_url="https://your-api.example/v1",
    ws_urls=["wss://your-node.example/ws/"],
)
```

`your-node.example` и `your-api.example` - это заглушки, а не реальные дефолтные адреса. Если нужен обычный mainnet на публичном Decimal RPC, достаточно:

```python
from decimal_web3_sdk import DecimalClient

client = DecimalClient()
```

Если нужен testnet:

```python
from decimal_web3_sdk import DecimalClient, NetworkConfig

client = DecimalClient(NetworkConfig.testnet())
```

Testnet/devnet:

```powershell
$env:DECIMAL_TESTNET_CHAIN_ID="202020"
$env:DECIMAL_TESTNET_WEB3_URLS="https://testnet-val.decimalchain.com/web3/,https://202020.rpc.thirdweb.com"
$env:DECIMAL_TESTNET_API_ROOT="https://testnet-gate.decimalchain.com/api/"
$env:DECIMAL_TESTNET_API_BASE="https://testnet-api.decimalchain.com/api/"
```

```python
config = NetworkConfig.testnet()
```

Devnet:

```python
config = NetworkConfig.devnet()
```

Дефолтные URL взяты из официального `dsc-js-sdk`:

```text
mainnet: https://node.decimalchain.com/web3/
testnet: https://testnet-val.decimalchain.com/web3/
devnet:  https://devnet-val.decimalchain.com/web3/
```

Для testnet SDK также добавляет публичный сторонний fallback `https://202020.rpc.thirdweb.com`, потому что `testnet-val` может отдавать `403` для прямых RPC-запросов из отдельных окружений. Это не официальный Decimal endpoint. Для релиза и приложений лучше указать свои endpoint-ы явно.

## Базовое использование

```python
import asyncio
from decimal_web3_sdk import DecimalClient

async def main():
    async with DecimalClient() as client:
        print(await client.block_number())

asyncio.run(main())
```

## Wallet helpers

```python
from decimal_web3_sdk.wallet import mnemonic_to_account, private_key_to_address

wallet = mnemonic_to_account("test test test test test test test test test test test junk")
address = wallet.address

# Низкоуровневый выход для signer-а, если он действительно нужен сервису:
private_key = wallet.private_key
address = private_key_to_address("0x...")
```

По умолчанию используется EVM derivation path `m/44'/60'/0'/0/0`. SDK не хранит приватные ключи и seed-фразы. Для приложений пользовательский вход должен быть через seed phrase, а private key использовать только как производный технический формат для подписи.

Для приложений используйте `*.from_mnemonic(...)` на request-классах. Тогда приложение передает seed phrase, а SDK локально получает private key только на момент подписи.

CLI:

```powershell
python -m decimal_web3_sdk.cli wallet-generate
python -m decimal_web3_sdk.cli wallet-from-mnemonic "seed words ..."
```

## Read-only REST

```python
async with DecimalClient(config) as client:
    latest = await client.rest.latest_block()
    tx = await client.rest.tx("0x...")
    balances = await client.rest.wallet_balances("0x...")
    validators = await client.rest.validators()
```

## DEL транзакции

Типовой порядок для любой транзакции:

1. Создать request из seed phrase через `*.from_mnemonic(...)`.
2. Посчитать комиссию через `estimate_fee_for_*` или `calculate_fee(...)`.
3. Показать пользователю `fee_del`, `required_del`, `missing_del`.
4. Только после подтверждения подписать/отправить через `send_*`.
5. Получить `TransactionResult` с hash/status/block/receipt.

```python
from decimal_web3_sdk import NativeTransferRequest

seed_phrase = "seed words from secure app storage"

result = await client.tx.send_del(
    NativeTransferRequest.from_mnemonic(
        to="0xRecipient",
        amount_del="0.01",
        mnemonic=seed_phrase,
        memo="optional",
    ),
    broadcast=False,
)

print(result.success, result.gas, result.fee_del, result.raw_tx_hex)
```

Отправка:

```python
result = await client.tx.send_del(request, broadcast=True, wait_receipt=True)
print(result.tx_hash, result.status, result.block_number, result.gas_used, result.effective_fee_del)
```

Низкоуровневый вариант `NativeTransferRequest(..., private_key="0x...")` тоже остается: он нужен для серверных сервисов, тестов и случаев, где ключ уже хранится во внешнем signer-е.

Все request-классы, которым нужен signer, поддерживают `from_mnemonic(...)`: DEL, ERC20, generic contract calls, staking, token, NFT, checks и bridge workflows. SDK локально получает private key только на момент подписи и не сохраняет seed phrase.

## Fee preflight

Перед подписью/отправкой SDK:

1. Строит draft.
2. Оценивает gas.
3. Считает `fee_wei = gas * gas_price`.
4. Проверяет `native_balance >= value + fee`.
5. Для ERC20 дополнительно проверяет token balance.
6. При нехватке возвращает `TransactionResult(success=False, error=...)` без broadcast.

`FeePreflight` считается до подписи и не создает raw transaction. Его можно показать пользователю как предварительный расчет комиссии. После отправки `TransactionResult` содержит нормализованные поля `tx_hash`, `status`, `block_number`, `transaction_index`, `gas_used`, `effective_fee_del`, а также сырой `receipt` для расширенной диагностики.

`TransactionResult.status` принимает практичные значения:

- `dry_run`: транзакция построена и подписана локально, но не отправлена;
- `pending`: broadcast выполнен, receipt еще не найден;
- `success`: receipt получен, `status == 1`;
- `failed`: receipt получен, `status == 0`.

Для contract-call с calldata SDK перед подписью проверяет, что на целевом адресе выбранной сети есть bytecode. Это защищает от ситуации, когда mainnet/system contract адрес случайно используется в testnet/devnet: транзакция к пустому адресу может получить EVM `status=1`, но никакой контракт не выполнится.

```python
exists = await client.contract_code_exists("0xContract")
if not exists:
    print("Wrong network or contract address")
```

В таком случае SDK вернет `success=False`, `tx_hash=None` и пользовательское сообщение: `Контракт сети недоступен. Проверьте сеть или адрес контракта.`

Для пользовательских интерфейсов дополнительно заполняется `result.user_message`, например:

- `Недостаточно DEL для суммы и комиссии.`
- `Недостаточно DEL для комиссии.`
- `Недостаточно токенов на балансе.`
- `Нужно разрешение на списание токена.`

По умолчанию после RPC `estimateGas` применяется запас `gas_limit_multiplier=1.10`, как в Decimal Go SDK. Если нужен строго сырой estimate:

```python
from decimal_web3_sdk import NetworkConfig
from decimal_web3_sdk.limits import SafetyLimits

config = NetworkConfig.custom(
    chain_id=75,
    web3_urls=["https://node.decimalchain.com/web3/"],
    safety=SafetyLimits(gas_limit_multiplier=1.0),
)
```

Комиссию можно посчитать отдельно до подписи:

```python
request = NativeTransferRequest.from_mnemonic(
    to="0xRecipient",
    amount_del="0.01",
    mnemonic=seed_phrase,
)
draft = await client.tx.build_native_transfer(request)
quote = await client.tx.calculate_fee(draft)

print(quote.ok, quote.gas, quote.gas_price_wei, quote.fee_del, quote.missing_del)
```

Пример полного preflight перед отправкой:

```python
quote = await client.tx.estimate_fee_for_native_transfer(request)
if not quote.ok:
    print("Need more DEL:", quote.missing_del)
else:
    print("Fee:", quote.fee_del, "Total:", quote.required_del)

result = await client.tx.send_del(request, broadcast=True, wait_receipt=True)
print(result.tx_hash, result.status, result.block_number)
```

## Approve и одна транзакция

Некоторые EVM workflow требуют allowance: ERC20 multisend, ERC20 staking/delegate/hold, token convert. SDK сначала проверяет баланс токена и allowance, а затем выбирает путь:

- Если allowance уже хватает, отправляется только основная транзакция.
- Если токен и контракт поддерживают `permit`/`...ByPermit`, SDK может уложиться в одну транзакцию без отдельного `approve`.
- Если permit недоступен, нужен отдельный `approve`, а затем основная транзакция. Это ограничение ERC20: allowance появляется в state только после майнинга approve.

```python
workflow = await client.decimal.delegate_erc20(request, broadcast=False)

print(workflow.steps)
print(workflow.one_transaction)
print(workflow.requires_secondary_transaction)
print(workflow.total_fee_del)
```

Для `delegate_erc20`, `hold_erc20` и `multisend_erc20` по умолчанию включен `prefer_permit=True`. Для `convert_erc20` в официальных Decimal JS/Go SDK используется `approveToken(...)` перед `convertToken(...)`; отдельного `convertByPermit` в публичном API не найдено, поэтому без заранее выставленного allowance это две транзакции.

Для готовых типов есть shortcuts:

```python
quote = await client.tx.estimate_fee_for_native_transfer(request)
quote = await client.tx.estimate_fee_for_erc20_transfer(erc20_request)
quote = await client.tx.estimate_fee_for_erc20_approve(approve_request)
quote = await client.tx.estimate_fee_for_contract_call(contract_request)
```

## Memo / сообщение в транзакции

Memo поддерживается только там, где формат транзакции безопасно может его нести:

```python
from decimal_web3_sdk import memo_supported_for

print(memo_supported_for("send-del"))          # True
print(memo_supported_for("multisend-del"))    # True
print(memo_supported_for("erc20-transfer"))   # False
```

Можно использовать:

- `NativeTransferRequest.memo` при обычной отправке DEL. SDK кодирует текст как UTF-8 в `data`, считает gas уже с этим payload и подписывает транзакцию с memo.
- `MultisendDelRequest.memo` при мультисенде DEL. SDK кодирует одно UTF-8 memo на весь batch как последний zero-value call к `0x000...000`, как это читает Decimal explorer.

Нельзя использовать как универсальный memo:

- ERC20 `transfer`, `approve`, `transferFrom`: поле `data` занято ABI-вызовом токена.
- `ContractCallRequest`: memo возможен только если конкретный контракт сам имеет аргумент note/message.
- Staking/token/NFT/checks/bridge workflow: текущие request-классы передают только аргументы системных контрактов.
- ERC20 multisend через Decimal multicall: token calls используют ERC20 `transferFrom`; универсальный memo для этого пути не включен, пока не проверен на боевых транзакциях именно ERC20 multisend.

## ERC20

```python
from decimal_web3_sdk import Erc20TransferFromRequest, Erc20TransferRequest

info = await client.erc20.info("0xToken")
balance = await client.erc20.balance("0xToken", "0xOwner")

result = await client.tx.send_erc20(
    Erc20TransferRequest.from_mnemonic(
        token="0xToken",
        to="0xRecipient",
        amount="1.5",
        mnemonic=seed_phrase,
    ),
    broadcast=False,
)

await client.tx.transfer_from_erc20(
    Erc20TransferFromRequest.from_mnemonic(
        token="0xToken",
        owner="0xOwner",
        to="0xRecipient",
        amount="1.5",
        mnemonic=seed_phrase,
    ),
    broadcast=False,
)
```

## Decimal staking и multisend

```python
from decimal_web3_sdk import DelegateDelRequest, DelegateErc20Request

await client.decimal.delegate_del(
    DelegateDelRequest.from_mnemonic(
        validator="0xValidator",
        amount_del="1",
        mnemonic=seed_phrase,
    ),
    broadcast=False,
)

await client.decimal.delegate_erc20(
    DelegateErc20Request.from_mnemonic(
        token="0xToken",
        validator="0xValidator",
        amount="10",
        mnemonic=seed_phrase,
    ),
    broadcast=False,
)
```

ERC20 staking/multisend поддерживает allowance, permit-first сценарий и approve fallback.

## Validator online/offline

Для обслуживания своих валидаторных нод используйте EVM `master-validator` contract. Без `broadcast=True` SDK только строит транзакцию и считает комиссию:

```python
from decimal_web3_sdk import ValidatorSelfPauseRequest

await client.decimal.pause_self_validator(
    ValidatorSelfPauseRequest.from_mnemonic(mnemonic=seed_phrase),
    broadcast=False,
)

await client.decimal.unpause_self_validator(
    ValidatorSelfPauseRequest.from_mnemonic(mnemonic=seed_phrase),
    broadcast=False,
)
```

Совместимые с JS SDK методы для адресного управления:

```python
from decimal_web3_sdk import ValidatorPauseRequest

await client.decimal.pause_validator(
    ValidatorPauseRequest.from_mnemonic(validator="0xValidator", mnemonic=seed_phrase),
    broadcast=False,
)
await client.decimal.unpause_validator(
    ValidatorPauseRequest.from_mnemonic(validator="0xValidator", mnemonic=seed_phrase),
    broadcast=False,
)
```

## Token Center

```python
from decimal_web3_sdk import (
    BuyTokenRequest,
    ConvertTokenRequest,
    token_creation_required_reserve_del,
)

await client.token.buy(
    BuyTokenRequest.from_mnemonic(token="0xToken", amount_del="1", mnemonic=seed_phrase),
    broadcast=False,
)

await client.token.convert(
    ConvertTokenRequest.from_mnemonic(
        token_in="0xTokenA",
        token_out="0xTokenB",
        amount_in="1",
        min_amount_out="0.95",
        mnemonic=seed_phrase,
    ),
    broadcast=False,
)
```

Создание резервного токена требует резерв `1000 DEL + комиссия за символ`. Правило перенесено из Decimal Go SDK:

```python
token_creation_required_reserve_del("ABC")       # 2501000 DEL
token_creation_required_reserve_del("MINTCANDY") # 1250 DEL
```

Если в `CreateTokenRequest` не передавать `reserve_value_wei`, SDK подставит обязательный резерв автоматически. Если нужен повышенный резерв, передайте `reserve_value_wei` явно.

## NFT

```python
from decimal_web3_sdk import CreateNftCollectionRequest, DelegateNftRequest

await client.nft.create_collection(
    CreateNftCollectionRequest.from_mnemonic(
        kind="erc721",
        symbol="ART",
        name="Art",
        contract_uri="ipfs://collection",
        mnemonic=seed_phrase,
    ),
    broadcast=False,
)
```

## CLI

```powershell
decimal-sdk block-number
decimal-sdk balance 0x...
decimal-sdk erc20-info 0xToken
python -m decimal_web3_sdk.cli wallet-from-mnemonic "seed words ..."
```

Для подписанных транзакций в приложениях используйте Python request-классы `*.from_mnemonic(...)`. CLI signing-команды остаются низкоуровневым интерфейсом для внешнего signer-а/secret-manager и не являются основным пользовательским сценарием.

## Тестовый прогон

```powershell
pytest -q
```

Live read-only:

```powershell
$env:DECIMAL_SDK_RUN_INTEGRATION="1"
pytest -q tests/integration
```

Broadcast training:

```powershell
$env:DECIMAL_TEST_NETWORK="testnet"
$env:DECIMAL_TEST_MNEMONIC="seed words ..."
$env:DECIMAL_TEST_TO="0x..."
$env:DECIMAL_TEST_DEL_AMOUNT="0.001"
$env:DECIMAL_TEST_BROADCAST="0"
decimal-sdk train-env
```

Можно использовать либо `DECIMAL_TEST_PRIVATE_KEY`, либо `DECIMAL_TEST_MNEMONIC`; если заданы оба, private key имеет приоритет. По умолчанию training harness использует `DECIMAL_TEST_NETWORK=testnet`. Перед подписью/отправкой он считает комиссию, а для визуального контроля записывает баланс и nonce до/после теста. `DECIMAL_TEST_BROADCAST=1` включайте только на testnet/devnet или на кошельке, который предназначен для реальных тренировочных транзакций.

## Статус

Готово:

- Web3 RPC pool.
- REST client.
- WS client с явным подключением.
- Wallet helpers.
- DEL/ERC20 transfer.
- Contract call.
- Fee preflight.
- 10% gas-limit buffer после estimateGas с возможностью переопределения.
- ERC20 approve/permit helpers.
- Decimal DEL/ERC20 staking, hold, unbond, withdraw hold.
- DEL/ERC20 multisend.
- Token Center buy/sell/convert/burn/mint/create/update details и расчет обязательного резерва создания токена.
- NFT ERC721/ERC1155 create/mint/transfer/approve/delegate/hold/withdraw.
- CLI.
- Agents/orchestrator/monitoring.
- Transaction training journal.

Осталось до полноценного стабильного релиза:

- live broadcast matrix на testnet/devnet;
- больше typed DTO для REST payloads;
- read-only staking summary зависит от выбранного API-gateway;
- публикация wheel/sdist в package registry;
- отдельная security note для ключей, mobile signer-а и backend signer-а.
