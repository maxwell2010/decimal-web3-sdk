from __future__ import annotations

from types import SimpleNamespace

import pytest
from web3 import Web3

from decimal_web3_sdk.bridge import (
    BridgeCompleteTransferRequest,
    BridgeService,
    BridgeTransferNativeRequest,
    BridgeTransferTokenRequest,
)
from decimal_web3_sdk.checks import (
    ChecksService,
    CreateChecksDelRequest,
    CreateChecksTokenRequest,
    RedeemChecksRequest,
)
from decimal_web3_sdk.transactions import TransactionService


PRIVATE_KEY = "0x" + "1" * 64
CONTRACT = "0x" + "9" * 40
TOKEN = "0x" + "5" * 40
RECIPIENT = "0x" + "4" * 40


class FakeContractClient:
    def __init__(self, balance_wei: int = 10**21) -> None:
        self.web3 = Web3()
        self.config = SimpleNamespace(chain_id=75)
        self.tx = TransactionService(self)
        self.balance = balance_wei

    async def transaction_count(self, address: str) -> int:
        return 1

    async def gas_price(self) -> int:
        return 1_000_000_000

    async def estimate_gas(self, tx: dict) -> int:
        assert tx["data"].startswith("0x")
        return 100_000

    async def balance_wei(self, address: str) -> int:
        return self.balance

    async def send_raw_transaction(self, raw_tx: bytes) -> str:
        return "0x" + "b" * 64

    async def transaction_receipt(self, tx_hash: str) -> dict | None:
        return None


@pytest.mark.asyncio
async def test_create_del_checks_uses_total_value() -> None:
    service = ChecksService(FakeContractClient())

    result = await service.create_del(
        CreateChecksDelRequest(
            contract=CONTRACT,
            signers=[RECIPIENT, "0x" + "6" * 40],
            amount_wei=10**18,
            due_block=123,
            nonce=7,
            private_key=PRIVATE_KEY,
        )
    )

    assert result.success is True
    assert result.required_wei == 2_000_100_000_000_000_000


@pytest.mark.asyncio
async def test_create_token_checks_and_redeem_build_transactions() -> None:
    service = ChecksService(FakeContractClient())

    create = await service.create_token(
        CreateChecksTokenRequest(
            contract=CONTRACT,
            token=TOKEN,
            signers=[RECIPIENT],
            amount_raw=10**18,
            due_block=123,
            nonce=7,
            private_key=PRIVATE_KEY,
        )
    )
    redeem = await service.redeem(
        RedeemChecksRequest(
            contract=CONTRACT,
            signatures=["0x" + "1" * 130],
            checks=["0x" + "2" * 64],
            private_key=PRIVATE_KEY,
        )
    )

    assert create.success is True
    assert redeem.success is True


@pytest.mark.asyncio
async def test_bridge_native_token_and_complete_build_transactions() -> None:
    service = BridgeService(FakeContractClient())

    native = await service.transfer_native(
        BridgeTransferNativeRequest(
            contract=CONTRACT,
            to=RECIPIENT,
            amount_wei=10**18,
            service_fee_wei=10**16,
            to_chain_id=1,
            nonce=7,
            private_key=PRIVATE_KEY,
        )
    )
    token = await service.transfer_token(
        BridgeTransferTokenRequest(
            contract=CONTRACT,
            token=TOKEN,
            to=RECIPIENT,
            amount_raw=10**18,
            service_fee_wei=10**16,
            to_chain_id=1,
            nonce=7,
            private_key=PRIVATE_KEY,
        )
    )
    complete = await service.complete_transfer(
        BridgeCompleteTransferRequest(
            contract=CONTRACT,
            encoded_vm="0x" + "1" * 64,
            unwrap_weth=False,
            private_key=PRIVATE_KEY,
        )
    )

    assert native.success is True
    assert token.success is True
    assert complete.success is True
