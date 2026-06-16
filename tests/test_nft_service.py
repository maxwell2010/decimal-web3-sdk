from __future__ import annotations

from types import SimpleNamespace

import pytest
from web3 import Web3

from decimal_web3_sdk.nft import (
    BurnNftRequest,
    CreateNftCollectionRequest,
    DelegateNftRequest,
    MintNftRequest,
    NftApproveRequest,
    NftService,
    NftTransferRequest,
)
from decimal_web3_sdk.transactions import TransactionService
from decimal_web3_sdk.wallet import private_key_to_address


PRIVATE_KEY = "0x" + "1" * 64
NFT = "0x" + "8" * 40
RECIPIENT = "0x" + "4" * 40
VALIDATOR = "0x" + "3" * 40


class FakeNftClient:
    def __init__(self, balance_wei: int = 10**21) -> None:
        self.web3 = Web3()
        self.config = SimpleNamespace(
            chain_id=75,
            contracts=SimpleNamespace(
                nft_center="0x9113ba675aa8f2ef0c068cee2cdabab95b6437fb",
                delegation_nft="0x5a6533e337f4b7f815aefb0609200acfbe1ba231",
            ),
        )
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
async def test_create_erc721_collection_builds_transaction() -> None:
    service = NftService(FakeNftClient())

    result = await service.create_collection(
        CreateNftCollectionRequest(
            kind="erc721",
            symbol="ART",
            name="Art",
            contract_uri="ipfs://collection",
            private_key=PRIVATE_KEY,
        )
    )

    assert result.success is True
    assert result.gas == 100_000


@pytest.mark.asyncio
async def test_mint_erc1155_builds_transaction() -> None:
    service = NftService(FakeNftClient())

    result = await service.mint(
        MintNftRequest(
            kind="erc1155",
            nft=NFT,
            to=RECIPIENT,
            token_id=7,
            amount=10,
            token_uri="ipfs://token",
            private_key=PRIVATE_KEY,
        )
    )

    assert result.success is True
    assert result.required_wei == 100_000_000_000_000


@pytest.mark.asyncio
async def test_transfer_erc721_reports_owner_mismatch_before_signing() -> None:
    service = NftService(FakeNftClient())

    async def owner_of(nft: str, token_id: int) -> str:
        return RECIPIENT

    service.owner_of = owner_of  # type: ignore[method-assign]

    result = await service.transfer(
        NftTransferRequest(kind="erc721", nft=NFT, to=RECIPIENT, token_id=1, private_key=PRIVATE_KEY)
    )

    assert result.success is False
    assert "NFT owner mismatch" in str(result.error)
    assert result.raw_tx_hex is None


@pytest.mark.asyncio
async def test_delegate_erc721_plans_approval_when_missing() -> None:
    service = NftService(FakeNftClient())
    owner = private_key_to_address(PRIVATE_KEY)

    async def owner_of(nft: str, token_id: int) -> str:
        return owner

    async def is_approved_for_all(kind: str, nft: str, owner: str, operator: str) -> bool:
        return False

    service.owner_of = owner_of  # type: ignore[method-assign]
    service.is_approved_for_all = is_approved_for_all  # type: ignore[method-assign]

    result = await service.delegate(
        DelegateNftRequest(kind="erc721", nft=NFT, validator=VALIDATOR, token_id=1, private_key=PRIVATE_KEY)
    )

    assert result.success is True
    assert result.steps == ("set_approval_for_all", "delegate_nft")
    assert result.extra_steps_required is True


@pytest.mark.asyncio
async def test_approve_erc721_builds_transaction_for_owner() -> None:
    service = NftService(FakeNftClient())
    owner = private_key_to_address(PRIVATE_KEY)

    async def owner_of(nft: str, token_id: int) -> str:
        return owner

    service.owner_of = owner_of  # type: ignore[method-assign]

    result = await service.approve(
        NftApproveRequest(nft=NFT, to=RECIPIENT, token_id=1, private_key=PRIVATE_KEY)
    )

    assert result.success is True
    assert result.raw_tx_hex is not None


@pytest.mark.asyncio
async def test_burn_erc721_reports_owner_mismatch_before_signing() -> None:
    service = NftService(FakeNftClient())

    async def owner_of(nft: str, token_id: int) -> str:
        return RECIPIENT

    service.owner_of = owner_of  # type: ignore[method-assign]

    result = await service.burn(
        BurnNftRequest(kind="erc721", nft=NFT, token_id=1, private_key=PRIVATE_KEY)
    )

    assert result.success is False
    assert "NFT owner mismatch" in str(result.error)
    assert result.raw_tx_hex is None


@pytest.mark.asyncio
async def test_burn_erc1155_builds_transaction_when_balance_is_enough() -> None:
    service = NftService(FakeNftClient())

    async def balance_of(nft: str, owner: str, token_id: int | None = None, kind: str = "erc721") -> int:
        return 10

    service.balance_of = balance_of  # type: ignore[method-assign]

    result = await service.burn(
        BurnNftRequest(kind="erc1155", nft=NFT, token_id=7, amount=3, private_key=PRIVATE_KEY)
    )

    assert result.success is True
    assert result.raw_tx_hex is not None
