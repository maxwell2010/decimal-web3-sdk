# Decimal Web3 Python SDK

`decimal-web3-sdk` is a Python SDK for Decimal EVM/Web3 applications. It is designed for local scripts, backend services, CLI tools, mobile backends, transaction training, monitoring, and release automation.

The SDK does not require MintCandy infrastructure. Use the official Decimal public RPC, your own Decimal node, or any compatible Decimal Web3/API gateway.

Project links:

- MintCandy: https://mintcandy.ru/
- Maintainer contact: `@Maxwell2019`

## Install

From PyPI after release:

```bash
pip install decimal-web3-sdk
```

From this repository:

```bash
python -m venv .venv
.\.venv\Scripts\activate
pip install -e ".[dev]"
```

Build local release artifacts:

```bash
python -m build
```

## Network Configuration

Mainnet uses the public Decimal Web3 RPC by default:

```python
from decimal_web3_sdk import NetworkConfig

config = NetworkConfig.mainnet()
```

Default mainnet Web3 RPC:

```text
https://node.decimalchain.com/web3/
```

For production apps, pass your own infrastructure explicitly:

```python
from decimal_web3_sdk import DecimalClient, NetworkConfig

config = NetworkConfig.custom(
    chain_id=75,
    web3_urls=["https://your-decimal-node.example/web3/"],
    api_root_url="https://your-decimal-api.example",
    api_base_url="https://your-decimal-api.example/v1",
    ws_urls=["wss://your-decimal-node.example/ws/"],
)

client = DecimalClient(config)
```

Do not use `your-decimal-node.example` literally. It is a placeholder for your own Decimal node/API. For the default public mainnet RPC you only need:

```python
client = DecimalClient()
```

Environment variables are supported:

```bash
DECIMAL_WEB3_URLS=https://node.decimalchain.com/web3/
DECIMAL_API_ROOT=https://your-decimal-api.example
DECIMAL_API_BASE=https://your-decimal-api.example/v1
DECIMAL_API_FALLBACK_BASES=https://your-fallback-api.example/v1
DECIMAL_API_KEY=
```

Testnet/devnet defaults follow the official Decimal `dsc-js-sdk` network map. You can override them with your own nodes at any time:

```bash
DECIMAL_TESTNET_CHAIN_ID=202020
DECIMAL_TESTNET_WEB3_URLS=https://testnet-val.decimalchain.com/web3/,https://202020.rpc.thirdweb.com
DECIMAL_TESTNET_API_ROOT=https://testnet-gate.decimalchain.com/api/
DECIMAL_TESTNET_API_BASE=https://testnet-api.decimalchain.com/api/
```

```python
config = NetworkConfig.testnet()
```

Default Decimal endpoints mirrored from `dsc-js-sdk` where available:

```text
mainnet web3: https://node.decimalchain.com/web3/
mainnet api:  https://mainnet-api.decimalchain.com/api/
mainnet gate: https://mainnet-gate.decimalchain.com/api/

testnet web3: https://testnet-val.decimalchain.com/web3/
testnet public third-party web3 fallback: https://202020.rpc.thirdweb.com
testnet api:  https://testnet-api.decimalchain.com/api/
testnet gate: https://testnet-gate.decimalchain.com/api/

devnet web3: https://devnet-val.decimalchain.com/web3/
devnet api:  https://devnet-api.decimalchain.com/api/
devnet gate: https://devnet-gate.decimalchain.com/api/
```

`https://202020.rpc.thirdweb.com` is not an official Decimal endpoint. It is kept only as a public fallback for Decimal testnet chain id `202020` when the official testnet Web3 endpoint is not reachable from the current environment.

## Quick Start

```python
import asyncio
from decimal_web3_sdk import DecimalClient

async def main():
    async with DecimalClient() as client:
        print(await client.block_number())

asyncio.run(main())
```

## Wallet Helpers

```python
from decimal_web3_sdk.wallet import mnemonic_to_account, private_key_to_address

wallet = mnemonic_to_account("test test test test test test test test test test test junk")
address = wallet.address

# Low-level signer output, when a backend service needs it explicitly:
private_key = wallet.private_key
address = private_key_to_address("0x...")
```

Default mnemonic derivation path is the EVM path `m/44'/60'/0'/0/0`, which is suitable for Decimal EVM addresses. The SDK never stores seed phrases or private keys. Keep them outside source code and pass them through secure storage or environment variables.

For applications, prefer request constructors such as `NativeTransferRequest.from_mnemonic(...)`. They derive the private key locally only for signing; your UI can keep working with the user's seed phrase.

CLI helpers:

```bash
python -m decimal_web3_sdk.cli wallet-generate
python -m decimal_web3_sdk.cli wallet-from-mnemonic "seed words ..."
```

## Read-only API

REST API calls require `api_base_url`/`api_root_url` because Decimal API gateways are deployment-specific:

```python
async with DecimalClient(config) as client:
    latest = await client.rest.latest_block()
    tx = await client.rest.tx("0x...")
    balances = await client.rest.wallet_balances("0x...")
    validators = await client.rest.validators()
```

## DEL Transfer

Transactions are dry-run by default in examples: SDK builds, estimates gas, checks fee/balance, signs locally, and only broadcasts when `broadcast=True`. The transaction flow follows the official Decimal Python SDK shape: wallet/request -> fee calculation -> sign -> broadcast -> inspect result.

```python
from decimal_web3_sdk import NativeTransferRequest

seed_phrase = "seed words from secure app storage"

request = NativeTransferRequest.from_mnemonic(
    to="0xRecipient",
    amount_del="0.01",
    mnemonic=seed_phrase,
    memo="optional",
)

result = await client.tx.send_del(request, broadcast=False)
print(result.success, result.gas, result.fee_del, result.raw_tx_hex)
```

Broadcast:

```python
result = await client.tx.send_del(request, broadcast=True, wait_receipt=True)
print(result.tx_hash, result.status, result.block_number, result.gas_used)
```

Low-level services may still pass `private_key="0x..."` directly when the signer is already managed outside the SDK.

All transaction request classes that need a signer support `from_mnemonic(...)`: native DEL, ERC20, generic contract calls, staking, token, NFT, checks, and bridge workflows. The SDK derives the private key locally only for signing and does not persist seed phrases.

## Fee Calculation

You can calculate fee and balance requirements before signing:

```python
draft = await client.tx.build_native_transfer(request)
quote = await client.tx.calculate_fee(draft)

print(quote.ok, quote.gas, quote.oracle_gas_price_wei, quote.minimum_fee_del, quote.missing_del)
```

`FeePreflight` is calculated before signing. The SDK refreshes the network gas oracle through `eth_gasPrice` and uses `max(user_gas_price, oracle_gas_price)` before signing, so `fee_wei` / `minimum_fee_wei` is the minimum fee required by the current network oracle. Use it to show the expected fee and missing DEL in an application UI without creating a raw signed transaction. After broadcast, `TransactionResult` exposes `tx_hash`, `status`, `block_number`, `transaction_index`, `gas_used`, `effective_fee_del`, and the raw `receipt`.

Transaction statuses are normalized as `dry_run`, `pending`, `success`, or `failed`.

Shortcuts are available for common transaction types:

```python
quote = await client.tx.estimate_fee_for_native_transfer(request)
quote = await client.tx.estimate_fee_for_erc20_transfer(erc20_request)
quote = await client.tx.estimate_fee_for_erc20_approve(approve_request)
quote = await client.tx.estimate_fee_for_contract_call(contract_request)
```

`send_*` and high-level token/staking/NFT workflows call the same fee calculation before signing. If DEL is insufficient for `value + fee`, SDK returns `success=False` and does not sign or broadcast.

Contract calls with calldata also verify that the target address has bytecode on the selected network before signing. If a mainnet system contract address is accidentally used on testnet/devnet, SDK returns `success=False`, `tx_hash=None`, and `user_message="Контракт сети недоступен. Проверьте сеть или адрес контракта."`

## Approve and One-Transaction Workflows

ERC20 workflows check token balance and allowance before signing. If allowance is already enough, only the main transaction is sent. For ERC20 multisend, memo is included in that same multicall transaction. If the token supports `permit`, SDK can put `permit + transferFrom calls + memo` into one multicall transaction. Otherwise ERC20 allowance must be created by a mined `approve` transaction first.

`DecimalWorkflowResult` exposes `steps`, `one_transaction`, `requires_secondary_transaction`, `transaction_count`, and `total_fee_del` so apps can show the user whether the workflow is one transaction or approve + action.

By default `NetworkConfig` applies a `1.10` gas limit multiplier after RPC `estimateGas`, matching the safety buffer used in the Decimal Go SDK. Override it when exact raw estimates are required:

```python
from decimal_web3_sdk import NetworkConfig
from decimal_web3_sdk.limits import SafetyLimits

config = NetworkConfig.mainnet()
config.safety = SafetyLimits(gas_limit_multiplier=1.0)
```

Transaction failures include `result.user_message` for UI/CLI use, for example `Недостаточно DEL для комиссии.` or `Недостаточно токенов на балансе.`.

## Memo Support

`memo` is only available where the underlying transaction format can safely carry it:

```python
from decimal_web3_sdk import memo_supported_for

print(memo_supported_for("send-del"))          # True
print(memo_supported_for("multisend-del"))    # True
print(memo_supported_for("multisend-erc20"))  # True
print(memo_supported_for("erc20-transfer"))   # False
```

Supported:

- `NativeTransferRequest.memo` for native DEL transfers. The SDK encodes UTF-8 text into EVM transaction `data`, estimates gas with that payload, and includes it in the signed transaction.
- `MultisendDelRequest.memo` for native DEL multisend. The SDK encodes one UTF-8 memo for the whole batch as the final zero-value call to `0x000...000`, matching Decimal explorer multisend parsing.
- `MultisendErc20Request.memo` for ERC20 multisend. ERC20 transfer calls keep their ABI calldata, and the SDK adds one final zero-value memo call to the multicall aggregate.

Not supported as a generic memo:

- ERC20 `transfer`, `approve`, and `transferFrom`: `data` is occupied by ERC20 ABI calldata.
- Generic `ContractCallRequest`: pass a note only if the target contract has its own note/message argument.
- Decimal staking/token/NFT/checks/bridge workflows: current request classes expose only the contract arguments.

## ERC20 Transfer

```python
from decimal_web3_sdk import Erc20TransferFromRequest, Erc20TransferRequest

result = await client.tx.send_erc20(
    Erc20TransferRequest.from_mnemonic(
        token="0xToken",
        to="0xRecipient",
        amount="1.5",
        mnemonic=seed_phrase,
    ),
    broadcast=False,
)
```

`transferFrom` with allowance preflight:

```python
result = await client.tx.transfer_from_erc20(
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

Before signing, the SDK checks:

- native DEL balance for gas;
- transfer value plus fee for DEL transfers;
- token balance for ERC20 transfers;
- allowance/permit path for token workflows that need approval.

## Decimal Staking And Token Workflows

```python
from decimal_web3_sdk import (
    DelegateDelRequest,
    ConvertTokenRequest,
    token_creation_required_reserve_del,
)

await client.decimal.delegate_del(
    DelegateDelRequest.from_mnemonic(
        validator="0xValidator",
        amount_del="1",
        mnemonic=seed_phrase,
    ),
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

Token creation reserve can be calculated before sending. If `CreateTokenRequest.reserve_value_wei` is omitted, SDK uses the Decimal Go SDK rule: `1000 DEL` minimum reserve plus symbol-length commission.

```python
print(token_creation_required_reserve_del("MINTCANDY"))  # 1250 DEL
```

Validator online/offline controls use the Decimal EVM `master-validator` contract. For node-local maintenance prefer self methods. Use a seed phrase only from secure node-local storage, or pass `private_key` only when an external signer/secret manager already owns it:

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

Admin-compatible methods matching the JS SDK are also available:

```python
from decimal_web3_sdk import ValidatorPauseRequest

await client.decimal.pause_validator(
    ValidatorPauseRequest.from_mnemonic(validator="0xValidator", mnemonic=seed_phrase),
)
await client.decimal.unpause_validator(
    ValidatorPauseRequest.from_mnemonic(validator="0xValidator", mnemonic=seed_phrase),
)
```

Implemented high-level modules:

- `tx`: native DEL, contract calls, ERC20 transfer/approve, fee preflight.
- `erc20`: info, balance, allowance, permit helpers.
- `decimal`: DEL/ERC20 delegate, hold, unbond, withdraw hold, multisend, validator online/offline.
- `token`: buy, sell, convert, burn, mint, update details, create token.
- `nft`: ERC721/ERC1155 create, mint, transfer, approve, delegate, hold, withdraw.
- `checks`: create/redeem EVM checks with explicit contract address.
- `bridge`: bridge transfer/complete helpers with explicit contract address.
- `rest`: blocks, transactions, addresses, balances, coins, validators, rewards.
- `ws`: explicit WebSocket subscriptions.
- `agents`/`orchestrator`/`monitoring`: endpoint checks, timings, SLA-style transaction pipeline support.

## CLI

```bash
decimal-sdk block-number
decimal-sdk balance 0x...
decimal-sdk erc20-info 0xToken
python -m decimal_web3_sdk.cli wallet-from-mnemonic "seed words ..."
```

For signed transactions in apps, prefer the Python `*.from_mnemonic(...)` request constructors shown above. CLI signing commands are a low-level interface for external signer/secret-manager flows and are not the normal user-facing path.

## Tests

Unit tests do not touch live nodes:

```bash
pytest -q
```

Live read-only smoke tests are opt-in:

```bash
DECIMAL_SDK_RUN_INTEGRATION=1 pytest -q tests/integration
```

Broadcast training is opt-in and requires a funded test wallet:

```bash
DECIMAL_TEST_NETWORK=testnet
DECIMAL_TEST_MNEMONIC="seed words ..."
DECIMAL_TEST_TO=0x...
DECIMAL_TEST_DEL_AMOUNT=0.001
DECIMAL_TEST_BROADCAST=0
decimal-sdk train-env
```

`train-env` calculates the fee before signing/sending, then records the transaction result. For visual test reporting it also stores the account balance and nonce before/after the case. Set `DECIMAL_TEST_BROADCAST=1` only on testnet/devnet or with a wallet intended for real training transactions.

## Relation To The Legacy Decimal Python SDK

The legacy official SDK documented the same basic flow: create/import wallet, initialize API/gateway, build transaction message, calculate fee, sign, broadcast, then inspect result. This SDK keeps that mental model but targets Decimal EVM/Web3 contracts and JSON-RPC.

Legacy concepts mapped here:

- `Wallet` -> local private key helpers and external secure storage.
- `DscAPI(gateway, web3)` -> `DecimalClient(NetworkConfig.custom(...))`.
- `Transaction.build_tx(...)` -> typed request dataclasses and service methods.
- `calculate_fee(...)` -> `estimate()` plus `preflight_fee()`.
- `broadcast(...)` -> `broadcast=True`.

## License

MIT License. See `LICENSE`.
