from __future__ import annotations

import csv
import asyncio
import os
import time
from dataclasses import asdict, dataclass, replace
from datetime import datetime, timezone
from decimal import Decimal
from pathlib import Path
from typing import Any

from dotenv import load_dotenv

from .client import DecimalClient
from .config import NetworkConfig
from .decimal import (
    DelegateDelRequest,
    DelegateErc20Request,
    HoldErc20Request,
    MultisendDelRequest,
    MultisendErc20Recipient,
    MultisendErc20Request,
    MultisendRecipient,
)
from .token import (
    BurnTokenRequest,
    BuyTokenRequest,
    ConvertTokenRequest,
    CreateReservelessTokenRequest,
    SellTokenRequest,
)
from .transactions import Erc20ApproveRequest, Erc20TransferRequest, FeePreflight, NativeTransferRequest
from .wallet import DEFAULT_DERIVATION_PATH, mnemonic_to_private_key, private_key_to_address


@dataclass(frozen=True)
class TxTrainingCase:
    name: str
    kind: str
    expected_steps: int
    broadcast: bool = False


@dataclass(frozen=True)
class TxTrainingRecord:
    timestamp: str
    name: str
    kind: str
    success: bool
    broadcast: bool
    chain_id: int | None
    account: str | None
    balance_before_del: str | None
    balance_after_del: str | None
    nonce_before: int | None
    nonce_after: int | None
    preflight_fee_wei: int | None
    preflight_fee_del: str | None
    preflight_required_del: str | None
    preflight_missing_del: str | None
    tx_hash: str | None
    status: str | None
    block_number: int | None
    gas: int | None
    fee_wei: int | None
    fee_del: str | None
    effective_fee_del: str | None
    elapsed_ms: float
    expected_steps: int
    actual_steps: int
    extra_steps_required: bool
    error: str | None


class TxTrainingJournal:
    def __init__(self, path: str | Path = "reports/tx_training.csv") -> None:
        self.path = Path(path)

    def append(self, record: TxTrainingRecord) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        exists = self.path.exists()
        with self.path.open("a", newline="", encoding="utf-8") as fh:
            writer = csv.DictWriter(fh, fieldnames=list(asdict(record).keys()))
            if not exists:
                writer.writeheader()
            writer.writerow(asdict(record))


async def run_env_training(journal: TxTrainingJournal | None = None) -> list[TxTrainingRecord]:
    load_dotenv(override=False)
    network = _test_network()
    private_key = _test_private_key_from_env(network)
    if not private_key:
        raise RuntimeError(
            f"{_network_env_prefix(network)}_TEST_PRIVATE_KEY or "
            f"{_network_env_prefix(network)}_TEST_MNEMONIC is required for transaction training"
        )

    account = private_key_to_address(private_key)
    expected_address = _test_expected_address(network)
    if expected_address and account.lower() != expected_address.lower():
        raise RuntimeError(
            f"Training credential address mismatch: expected {expected_address}, derived {account}"
        )

    broadcast = os.getenv("DECIMAL_TEST_BROADCAST") == "1"
    if broadcast and network == "mainnet" and not expected_address:
        raise RuntimeError(
            "Mainnet broadcast requires DECIMAL_MAINNET_TEST_EXPECTED_ADDRESS"
        )
    wait_receipt = os.getenv("DECIMAL_TEST_WAIT_RECEIPT") == "1"
    journal = journal or TxTrainingJournal(os.getenv("DECIMAL_TEST_REPORT", "reports/tx_training.csv"))
    records: list[TxTrainingRecord] = []

    async with DecimalClient(_training_config(network)) as client:
        to = os.getenv("DECIMAL_TEST_TO") or await client.address_from_private_key(private_key)
        del_amount = Decimal(os.getenv("DECIMAL_TEST_DEL_AMOUNT", "0"))
        if del_amount > 0:
            request = NativeTransferRequest(to=to, amount_del=del_amount, private_key=private_key)
            record = await _run_tracked_case(
                client,
                account,
                name="send_del",
                kind="DEL",
                broadcast=broadcast,
                expected_steps=1,
                actual_steps=1,
                preflight_factory=lambda: client.tx.estimate_fee_for_native_transfer(request),
                tx_factory=lambda: client.tx.send_del(request, broadcast=broadcast, wait_receipt=wait_receipt),
            )
            records.append(record)

        token = os.getenv("DECIMAL_TEST_ERC20_TOKEN")
        token_amount = os.getenv("DECIMAL_TEST_ERC20_AMOUNT")
        if token and token_amount:
            result, elapsed = await _timed(
                client.tx.send_erc20(
                    Erc20TransferRequest(
                        token=token,
                        to=to,
                        amount=Decimal(token_amount),
                        private_key=private_key,
                        decimals=_env_int("DECIMAL_TEST_ERC20_DECIMALS"),
                    ),
                    broadcast=broadcast,
                    wait_receipt=wait_receipt,
                )
            )
            records.append(
                _record("send_erc20", "ERC20", result, elapsed, broadcast, expected_steps=1, actual_steps=1)
            )

        spender = os.getenv("DECIMAL_TEST_ERC20_SPENDER")
        approve_amount = os.getenv("DECIMAL_TEST_ERC20_APPROVE_AMOUNT")
        if token and spender and approve_amount:
            result, elapsed = await _timed(
                client.tx.approve_erc20(
                    Erc20ApproveRequest(
                        token=token,
                        spender=spender,
                        amount=Decimal(approve_amount),
                        private_key=private_key,
                        decimals=_env_int("DECIMAL_TEST_ERC20_DECIMALS"),
                    ),
                    broadcast=broadcast,
                    wait_receipt=wait_receipt,
                )
            )
            records.append(
                _record("approve_erc20", "ERC20_APPROVE", result, elapsed, broadcast, expected_steps=1, actual_steps=1)
            )

        token_delegate_amount = os.getenv("DECIMAL_TEST_ERC20_DELEGATE_AMOUNT")
        validator = os.getenv("DECIMAL_TEST_VALIDATOR")
        if token and validator and token_delegate_amount:
            result, elapsed = await _timed(
                client.decimal.delegate_erc20(
                    DelegateErc20Request(
                        token=token,
                        validator=validator,
                        amount=Decimal(token_delegate_amount),
                        private_key=private_key,
                        decimals=_env_int("DECIMAL_TEST_ERC20_DECIMALS"),
                    ),
                    broadcast=broadcast,
                    wait_receipt=wait_receipt,
                )
            )
            records.append(
                _record(
                    "delegate_erc20",
                    "ERC20_DELEGATE",
                    result,
                    elapsed,
                    broadcast,
                    expected_steps=result.expected_steps,
                    actual_steps=result.actual_steps,
                )
            )

        token_hold_amount = os.getenv("DECIMAL_TEST_ERC20_HOLD_AMOUNT")
        token_hold_timestamp = _env_int("DECIMAL_TEST_ERC20_HOLD_TIMESTAMP")
        if token and validator and token_hold_amount and token_hold_timestamp:
            result, elapsed = await _timed(
                client.decimal.hold_erc20(
                    HoldErc20Request(
                        token=token,
                        validator=validator,
                        amount=Decimal(token_hold_amount),
                        hold_timestamp=token_hold_timestamp,
                        private_key=private_key,
                        decimals=_env_int("DECIMAL_TEST_ERC20_DECIMALS"),
                    ),
                    broadcast=broadcast,
                    wait_receipt=wait_receipt,
                )
            )
            records.append(
                _record(
                    "hold_erc20",
                    "ERC20_HOLD",
                    result,
                    elapsed,
                    broadcast,
                    expected_steps=result.expected_steps,
                    actual_steps=result.actual_steps,
                )
            )

        token_multisend_amount = os.getenv("DECIMAL_TEST_ERC20_MULTISEND_AMOUNT")
        if token and token_multisend_amount:
            result, elapsed = await _timed(
                client.decimal.multisend_erc20(
                    MultisendErc20Request(
                        token=token,
                        recipients=[MultisendErc20Recipient(to=to, amount=Decimal(token_multisend_amount))],
                        private_key=private_key,
                        decimals=_env_int("DECIMAL_TEST_ERC20_DECIMALS"),
                        memo=os.getenv("DECIMAL_TEST_ERC20_MULTISEND_MEMO"),
                    ),
                    broadcast=broadcast,
                    wait_receipt=wait_receipt,
                )
            )
            records.append(
                _record(
                    "multisend_erc20",
                    "ERC20_MULTISEND",
                    result,
                    elapsed,
                    broadcast,
                    expected_steps=result.expected_steps,
                    actual_steps=result.actual_steps,
                )
            )

        buy_token = os.getenv("DECIMAL_TEST_BUY_TOKEN")
        buy_token_amount = os.getenv("DECIMAL_TEST_BUY_TOKEN_DEL_AMOUNT")
        if buy_token and buy_token_amount:
            result, elapsed = await _timed(
                client.token.buy(
                    BuyTokenRequest(
                        token=buy_token,
                        amount_del=Decimal(buy_token_amount),
                        private_key=private_key,
                        min_amount_out_raw=int(os.getenv("DECIMAL_TEST_BUY_TOKEN_MIN_OUT_RAW", "0")),
                    ),
                    broadcast=broadcast,
                    wait_receipt=wait_receipt,
                )
            )
            records.append(
                _record("buy_token", "TOKEN_BUY", result, elapsed, broadcast, expected_steps=1, actual_steps=1)
            )

        sell_token = os.getenv("DECIMAL_TEST_SELL_TOKEN")
        sell_token_amount = os.getenv("DECIMAL_TEST_SELL_TOKEN_AMOUNT")
        if sell_token and sell_token_amount:
            result, elapsed = await _timed(
                client.token.sell(
                    SellTokenRequest(
                        token=sell_token,
                        amount=Decimal(sell_token_amount),
                        private_key=private_key,
                        min_amount_del_out_wei=int(os.getenv("DECIMAL_TEST_SELL_TOKEN_MIN_DEL_OUT_WEI", "1")),
                        decimals=_env_int("DECIMAL_TEST_SELL_TOKEN_DECIMALS"),
                    ),
                    broadcast=broadcast,
                    wait_receipt=wait_receipt,
                )
            )
            records.append(
                _record("sell_token", "TOKEN_SELL", result, elapsed, broadcast, expected_steps=1, actual_steps=1)
            )

        convert_token_in = os.getenv("DECIMAL_TEST_CONVERT_TOKEN_IN")
        convert_token_out = os.getenv("DECIMAL_TEST_CONVERT_TOKEN_OUT")
        convert_amount = os.getenv("DECIMAL_TEST_CONVERT_AMOUNT_IN")
        convert_min_out = os.getenv("DECIMAL_TEST_CONVERT_MIN_AMOUNT_OUT")
        if convert_token_in and convert_token_out and convert_amount and convert_min_out:
            result, elapsed = await _timed(
                client.token.convert(
                    ConvertTokenRequest(
                        token_in=convert_token_in,
                        token_out=convert_token_out,
                        amount_in=Decimal(convert_amount),
                        min_amount_out=Decimal(convert_min_out),
                        private_key=private_key,
                        token_in_decimals=_env_int("DECIMAL_TEST_CONVERT_TOKEN_IN_DECIMALS"),
                        token_out_decimals=_env_int("DECIMAL_TEST_CONVERT_TOKEN_OUT_DECIMALS"),
                    ),
                    broadcast=broadcast,
                    wait_receipt=wait_receipt,
                )
            )
            records.append(
                _record(
                    "convert_token",
                    "TOKEN_CONVERT",
                    result,
                    elapsed,
                    broadcast,
                    expected_steps=result.expected_steps,
                    actual_steps=result.actual_steps,
                )
            )

        burn_token = os.getenv("DECIMAL_TEST_BURN_TOKEN")
        burn_amount = os.getenv("DECIMAL_TEST_BURN_TOKEN_AMOUNT")
        if burn_token and burn_amount:
            result, elapsed = await _timed(
                client.token.burn(
                    BurnTokenRequest(
                        token=burn_token,
                        amount=Decimal(burn_amount),
                        private_key=private_key,
                        decimals=_env_int("DECIMAL_TEST_BURN_TOKEN_DECIMALS"),
                    ),
                    broadcast=broadcast,
                    wait_receipt=wait_receipt,
                )
            )
            records.append(
                _record("burn_token", "TOKEN_BURN", result, elapsed, broadcast, expected_steps=1, actual_steps=1)
            )

        create_symbol = os.getenv("DECIMAL_TEST_CREATE_RESERVELESS_SYMBOL")
        if create_symbol:
            result, elapsed = await _timed(
                client.token.create_reserveless(
                    CreateReservelessTokenRequest(
                        name=os.getenv("DECIMAL_TEST_CREATE_RESERVELESS_NAME", create_symbol),
                        symbol=create_symbol,
                        mintable=os.getenv("DECIMAL_TEST_CREATE_RESERVELESS_MINTABLE", "1") == "1",
                        burnable=os.getenv("DECIMAL_TEST_CREATE_RESERVELESS_BURNABLE", "1") == "1",
                        initial_mint_raw=int(os.getenv("DECIMAL_TEST_CREATE_RESERVELESS_INITIAL_RAW", "0")),
                        cap_raw=int(os.getenv("DECIMAL_TEST_CREATE_RESERVELESS_CAP_RAW", "0")),
                        identity=os.getenv("DECIMAL_TEST_CREATE_RESERVELESS_IDENTITY", ""),
                        private_key=private_key,
                    ),
                    broadcast=broadcast,
                    wait_receipt=wait_receipt,
                )
            )
            records.append(
                _record(
                    "create_reserveless_token",
                    "TOKEN_CREATE_RESERVELESS",
                    result,
                    elapsed,
                    broadcast,
                    expected_steps=1,
                    actual_steps=1,
                )
            )

        delegate_amount = os.getenv("DECIMAL_TEST_DELEGATE_DEL_AMOUNT")
        if validator and delegate_amount:
            result, elapsed = await _timed(
                client.decimal.delegate_del(
                    DelegateDelRequest(
                        validator=validator,
                        amount_del=Decimal(delegate_amount),
                        private_key=private_key,
                    ),
                    broadcast=broadcast,
                    wait_receipt=wait_receipt,
                )
            )
            records.append(
                _record(
                    "delegate_del",
                    "DEL_DELEGATE",
                    result,
                    elapsed,
                    broadcast,
                    expected_steps=1,
                    actual_steps=1,
                )
            )

        multisend_amount = os.getenv("DECIMAL_TEST_MULTISEND_DEL_AMOUNT")
        if multisend_amount:
            request = MultisendDelRequest(
                recipients=[MultisendRecipient(to=to, amount_del=Decimal(multisend_amount))],
                private_key=private_key,
                memo=os.getenv("DECIMAL_TEST_MULTISEND_MEMO"),
            )
            record = await _run_tracked_case(
                client,
                account,
                name="multisend_del",
                kind="DEL_MULTISEND",
                broadcast=broadcast,
                expected_steps=1,
                actual_steps=1,
                preflight_factory=lambda: client.decimal.estimate_fee_for_multisend_del(request),
                tx_factory=lambda: client.decimal.multisend_del(
                    request,
                    broadcast=broadcast,
                    wait_receipt=wait_receipt,
                ),
            )
            records.append(record)

    for record in records:
        journal.append(record)
    return records


async def _timed(awaitable) -> tuple[Any, float]:
    started = time.perf_counter()
    result = await awaitable
    return result, (time.perf_counter() - started) * 1000


async def _run_tracked_case(
    client: DecimalClient,
    account: str,
    *,
    name: str,
    kind: str,
    broadcast: bool,
    expected_steps: int,
    actual_steps: int,
    tx_factory,
    preflight_factory=None,
) -> TxTrainingRecord:
    balance_before, nonce_before = await _account_state(client, account)
    preflight = await preflight_factory() if preflight_factory is not None else None
    result, elapsed = await _timed(tx_factory())
    if broadcast and result.tx_hash and result.status == "pending":
        result = await _wait_for_training_receipt(client, result)
    balance_after, nonce_after = await _account_state(client, account)
    return _record(
        name,
        kind,
        result,
        elapsed,
        broadcast,
        expected_steps=expected_steps,
        actual_steps=actual_steps,
        chain_id=client.config.chain_id,
        account=account,
        balance_before_del=balance_before,
        balance_after_del=balance_after,
        nonce_before=nonce_before,
        nonce_after=nonce_after,
        preflight=preflight,
    )


async def _account_state(client: DecimalClient, account: str) -> tuple[str, int]:
    balance_wei = int(await client.balance_wei(account))
    nonce = int(await client.transaction_count(account))
    return str(Decimal(balance_wei) / Decimal(10**18)), nonce


async def _wait_for_training_receipt(client: DecimalClient, result):
    timeout = float(os.getenv("DECIMAL_TEST_RECEIPT_TIMEOUT_SECONDS", "20"))
    poll = float(os.getenv("DECIMAL_TEST_RECEIPT_POLL_SECONDS", "1"))
    deadline = asyncio.get_running_loop().time() + timeout
    while asyncio.get_running_loop().time() < deadline:
        receipt = await client.transaction_receipt(result.tx_hash)
        if receipt is not None:
            status = receipt.get("status")
            gas_used = _int_or_none(receipt.get("gasUsed") or receipt.get("gas_used"))
            gas_price = _int_or_none(receipt.get("effectiveGasPrice") or receipt.get("effective_gas_price"))
            if gas_price is None and result.fee_wei is not None and result.gas:
                gas_price = int(result.fee_wei) // int(result.gas)
            effective_fee = gas_used * gas_price if gas_used is not None and gas_price is not None else None
            return replace(
                result,
                status="success" if status == 1 else "failed" if status == 0 else result.status,
                block_number=_int_or_none(receipt.get("blockNumber") or receipt.get("block_number")),
                transaction_index=_int_or_none(receipt.get("transactionIndex") or receipt.get("transaction_index")),
                gas_used=gas_used,
                effective_gas_price_wei=gas_price,
                effective_fee_wei=effective_fee,
                effective_fee_del=Decimal(effective_fee) / Decimal(10**18) if effective_fee is not None else None,
                receipt=dict(receipt),
            )
        await asyncio.sleep(poll)
    return result


def _record(
    name: str,
    kind: str,
    result,
    elapsed_ms: float,
    broadcast: bool,
    expected_steps: int,
    actual_steps: int,
    chain_id: int | None = None,
    account: str | None = None,
    balance_before_del: str | None = None,
    balance_after_del: str | None = None,
    nonce_before: int | None = None,
    nonce_after: int | None = None,
    preflight: FeePreflight | None = None,
) -> TxTrainingRecord:
    return TxTrainingRecord(
        timestamp=datetime.now(timezone.utc).isoformat(),
        name=name,
        kind=kind,
        success=bool(result.success),
        broadcast=broadcast,
        chain_id=chain_id,
        account=account,
        balance_before_del=balance_before_del,
        balance_after_del=balance_after_del,
        nonce_before=nonce_before,
        nonce_after=nonce_after,
        preflight_fee_wei=preflight.fee_wei if preflight is not None else None,
        preflight_fee_del=str(preflight.fee_del) if preflight is not None else None,
        preflight_required_del=str(preflight.required_del) if preflight is not None else None,
        preflight_missing_del=str(preflight.missing_del) if preflight is not None else None,
        tx_hash=result.tx_hash,
        status=result.status,
        block_number=result.block_number,
        gas=result.gas,
        fee_wei=result.fee_wei,
        fee_del=str(result.fee_del) if result.fee_del is not None else None,
        effective_fee_del=str(result.effective_fee_del) if result.effective_fee_del is not None else None,
        elapsed_ms=round(elapsed_ms, 3),
        expected_steps=expected_steps,
        actual_steps=actual_steps,
        extra_steps_required=actual_steps > expected_steps,
        error=result.error,
    )


def _env_int(name: str) -> int | None:
    value = os.getenv(name)
    if not value:
        return None
    return int(value)


def _int_or_none(value) -> int | None:
    if value is None:
        return None
    return int(value)


def _test_network() -> str:
    network = os.getenv("DECIMAL_TEST_NETWORK", "testnet").strip().lower()
    if network not in {"testnet", "devnet", "mainnet"}:
        raise RuntimeError("DECIMAL_TEST_NETWORK must be one of: testnet, devnet, mainnet")
    return network


def _training_config(network: str | None = None) -> NetworkConfig:
    network = network or _test_network()
    if network == "mainnet":
        return NetworkConfig.mainnet()
    if network == "devnet":
        return NetworkConfig.devnet()
    if network == "testnet":
        return NetworkConfig.testnet()
    raise RuntimeError("DECIMAL_TEST_NETWORK must be one of: testnet, devnet, mainnet")


def _network_env_prefix(network: str) -> str:
    return f"DECIMAL_{network.upper()}"


def _test_expected_address(network: str) -> str | None:
    return os.getenv(f"{_network_env_prefix(network)}_TEST_EXPECTED_ADDRESS")


def _test_private_key_from_env(network: str | None = None) -> str | None:
    network = network or _test_network()
    prefix = _network_env_prefix(network)
    private_key = os.getenv(f"{prefix}_TEST_PRIVATE_KEY")
    if private_key:
        return private_key
    mnemonic = os.getenv(f"{prefix}_TEST_MNEMONIC")
    if not mnemonic:
        return None
    return mnemonic_to_private_key(
        mnemonic,
        passphrase=os.getenv(f"{prefix}_TEST_MNEMONIC_PASSPHRASE", ""),
        account_path=os.getenv(f"{prefix}_TEST_DERIVATION_PATH", DEFAULT_DERIVATION_PATH),
    )
