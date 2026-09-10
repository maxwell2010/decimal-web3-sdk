from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal

import pytest
from eth_abi import decode
from eth_account import Account
from web3 import Web3

from decimal_web3_sdk.config import NetworkConfig
from decimal_web3_sdk.decimal import (
    MULTICALL_ABI,
    DecimalService,
    MultisendDelRequest,
    MultisendErc20Recipient,
    MultisendErc20Request,
    MultisendRecipient,
    UnbondDelRequest,
    WithdrawDelStakeWithResetRequest,
)
from decimal_web3_sdk.erc20 import PermitSignature
from decimal_web3_sdk.transactions import ContractCallRequest, TransactionDraft, TransactionResult
from decimal_web3_sdk.wallet import checksum, private_key_to_address


PRIVATE_KEY = "0x" + Account.create().key.hex()
TOKEN = "0x32acafa38b2e3e17c99eff5d26ae69106fbeee73"
RECIPIENT_A = "0x048b4622A2dbb0c632F86B39F9ac8AEE15f3a803"
RECIPIENT_B = "0x0F881aAd73Bf156705B37B8931157f39f2dF1935"


@dataclass
class _FakeBalance:
    raw: int


class _FakeTxService:
    def __init__(self) -> None:
        self.last_request: ContractCallRequest | None = None
        self.approve_calls = 0

    async def build_contract_call(self, request: ContractCallRequest) -> TransactionDraft:
        self.last_request = request
        return TransactionDraft(
            tx={
                "from": private_key_to_address(request.private_key),
                "to": checksum(request.contract),
                "data": request.data,
                "value": int(request.value_wei),
            },
            from_address=private_key_to_address(request.private_key),
            to_address=checksum(request.contract),
            value_wei=int(request.value_wei),
        )

    async def send_draft(self, draft: TransactionDraft, private_key: str, broadcast: bool, wait_receipt: bool) -> TransactionResult:
        return TransactionResult(success=True, tx_hash="0x" + "12" * 32, fee_wei=0, fee_del=Decimal(0))

    async def approve_erc20(self, *args, **kwargs) -> TransactionResult:
        self.approve_calls += 1
        return TransactionResult(success=True, tx_hash="0x" + "34" * 32)


class _FakeErc20Service:
    def __init__(self, *, allowance: int = 0, permit_available: bool = True) -> None:
        self.allowance_value = allowance
        self.permit_available = permit_available
        self.allowance_calls = 0
        self.permit_calls = 0

    async def balance(self, token_address: str, owner: str) -> _FakeBalance:
        return _FakeBalance(raw=10**30)

    async def allowance(self, token_address: str, owner: str, spender: str) -> int:
        self.allowance_calls += 1
        return self.allowance_value

    async def permit_signature(
        self,
        token_address: str,
        owner: str,
        spender: str,
        value_raw: int,
        deadline: int,
        private_key: str,
    ) -> PermitSignature | None:
        self.permit_calls += 1
        if not self.permit_available:
            return None
        return PermitSignature(deadline=deadline, v=27, r=b"\x11" * 32, s=b"\x22" * 32)

    def build_permit_data(self, token_address: str, owner: str, spender: str, value_raw: int, permit: PermitSignature) -> str:
        contract = Web3().eth.contract(address=checksum(token_address), abi=[
            {
                "inputs": [
                    {"name": "owner", "type": "address"},
                    {"name": "spender", "type": "address"},
                    {"name": "value", "type": "uint256"},
                    {"name": "deadline", "type": "uint256"},
                    {"name": "v", "type": "uint8"},
                    {"name": "r", "type": "bytes32"},
                    {"name": "s", "type": "bytes32"},
                ],
                "name": "permit",
                "outputs": [],
                "stateMutability": "nonpayable",
                "type": "function",
            }
        ])
        return contract.functions.permit(
            checksum(owner),
            checksum(spender),
            int(value_raw),
            int(permit.deadline),
            int(permit.v),
            permit.r,
            permit.s,
        )._encode_transaction_data()

    def build_transfer_from_data(self, token_address: str, owner: str, to: str, amount_raw: int) -> str:
        contract = Web3().eth.contract(address=checksum(token_address), abi=[
            {
                "inputs": [
                    {"name": "from", "type": "address"},
                    {"name": "to", "type": "address"},
                    {"name": "value", "type": "uint256"},
                ],
                "name": "transferFrom",
                "outputs": [{"name": "", "type": "bool"}],
                "stateMutability": "nonpayable",
                "type": "function",
            }
        ])
        return contract.functions.transferFrom(
            checksum(owner),
            checksum(to),
            int(amount_raw),
        )._encode_transaction_data()


class _FakeClient:
    def __init__(self, *, erc20: _FakeErc20Service | None = None) -> None:
        self.config = NetworkConfig.mainnet()
        self.web3 = Web3()
        self.tx = _FakeTxService()
        self.erc20 = erc20 or _FakeErc20Service()


def _decode_aggregate(data: str):
    raw = bytes.fromhex(data[2:])
    assert raw[:4].hex() == Web3.keccak(text="aggregate((address,uint256,bytes)[])")[:4].hex()
    return decode(["(address,uint256,bytes)[]"], raw[4:])[0]


@pytest.mark.asyncio
async def test_multisend_del_never_uses_erc20_allowance_or_approve() -> None:
    client = _FakeClient()
    service = DecimalService(client)

    draft = await service.build_multisend_del(
        MultisendDelRequest(
            private_key=PRIVATE_KEY,
            recipients=[
                MultisendRecipient(RECIPIENT_A, "1.25"),
                MultisendRecipient(RECIPIENT_B, "2.75"),
            ],
            memo="hello del multisend",
        )
    )

    assert client.erc20.allowance_calls == 0
    assert client.erc20.permit_calls == 0
    assert client.tx.approve_calls == 0
    assert draft.value_wei == Web3.to_wei(Decimal("4"), "ether")

    calls = _decode_aggregate(draft.tx["data"])
    assert len(calls) == 3
    assert calls[0][0].lower() == checksum(RECIPIENT_A).lower()
    assert calls[0][1] == Web3.to_wei(Decimal("1.25"), "ether")
    assert calls[0][2] == b""
    assert calls[1][0].lower() == checksum(RECIPIENT_B).lower()
    assert calls[1][1] == Web3.to_wei(Decimal("2.75"), "ether")
    assert calls[1][2] == b""
    assert calls[2][0] == "0x0000000000000000000000000000000000000000"
    assert calls[2][1] == 0
    assert calls[2][2] == b"hello del multisend"


@pytest.mark.asyncio
async def test_unbond_del_uses_wdel_token_address_for_delegation_withdraw() -> None:
    client = _FakeClient()
    service = DecimalService(client)

    result = await service.unbond_del(
        UnbondDelRequest(
            validator=RECIPIENT_A,
            amount_del="1",
            private_key=PRIVATE_KEY,
        ),
        broadcast=False,
        wait_receipt=False,
    )

    assert result.success is True
    assert client.tx.last_request is not None
    assert client.tx.last_request.contract == client.config.contracts.delegation
    selector = Web3.keccak(text="withdraw(address,address,uint256)")[:4].hex()
    data = client.tx.last_request.data
    assert data.startswith("0x" + selector)
    decoded = decode(["address", "address", "uint256"], bytes.fromhex(data[10:]))
    assert decoded[0].lower() == checksum(RECIPIENT_A).lower()
    assert decoded[1].lower() == checksum(client.config.contracts.wdel).lower()
    assert decoded[2] == Web3.to_wei(Decimal("1"), "ether")


@pytest.mark.asyncio
async def test_withdraw_del_stake_with_reset_uses_wdel_and_hold_timestamps() -> None:
    client = _FakeClient()
    service = DecimalService(client)

    result = await service.withdraw_del_stake_with_reset(
        WithdrawDelStakeWithResetRequest(
            validator=RECIPIENT_A,
            amount_del="4.21",
            hold_timestamps_to_reset=[1787078776],
            private_key=PRIVATE_KEY,
        ),
        broadcast=False,
        wait_receipt=False,
    )

    assert result.success is True
    assert client.tx.last_request is not None
    assert client.tx.last_request.contract == client.config.contracts.delegation
    selector = Web3.keccak(text="withdrawWithReset(address,address,uint256,uint256[])")[:4].hex()
    data = client.tx.last_request.data
    assert data.startswith("0x" + selector)
    decoded = decode(["address", "address", "uint256", "uint256[]"], bytes.fromhex(data[10:]))
    assert decoded[0].lower() == checksum(RECIPIENT_A).lower()
    assert decoded[1].lower() == checksum(client.config.contracts.wdel).lower()
    assert decoded[2] == Web3.to_wei(Decimal("4.21"), "ether")
    assert list(decoded[3]) == [1787078776]


@pytest.mark.asyncio
async def test_multisend_erc20_uses_permit_plus_transfer_from_plus_memo_in_one_aggregate() -> None:
    client = _FakeClient(erc20=_FakeErc20Service(allowance=0, permit_available=True))
    service = DecimalService(client)

    result = await service.multisend_erc20(
        MultisendErc20Request(
            token=TOKEN,
            private_key=PRIVATE_KEY,
            decimals=18,
            recipients=[
                MultisendErc20Recipient(RECIPIENT_A, "1"),
                MultisendErc20Recipient(RECIPIENT_B, "2"),
            ],
            memo="token memo",
            prefer_permit=True,
            auto_approve=True,
        ),
        broadcast=False,
        wait_receipt=False,
    )

    assert result.success is True
    assert result.one_transaction is True
    assert result.requires_secondary_transaction is False
    assert result.steps == ("permit_erc20", "multisend_erc20")
    assert client.tx.approve_calls == 0
    assert client.erc20.permit_calls == 1

    assert client.tx.last_request is not None
    assert client.tx.last_request.contract == client.config.contracts.multicall
    assert client.tx.last_request.value_wei == 0
    calls = _decode_aggregate(client.tx.last_request.data)
    selectors = [call[2][:4].hex() if call[2] else "" for call in calls]
    assert selectors == ["d505accf", "23b872dd", "23b872dd", "746f6b65"]
    assert calls[-1][0] == "0x0000000000000000000000000000000000000000"
    assert calls[-1][2] == b"token memo"


@pytest.mark.asyncio
async def test_multisend_erc20_falls_back_to_approve_when_permit_unavailable() -> None:
    client = _FakeClient(erc20=_FakeErc20Service(allowance=0, permit_available=False))
    service = DecimalService(client)

    result = await service.multisend_erc20(
        MultisendErc20Request(
            token=TOKEN,
            private_key=PRIVATE_KEY,
            decimals=18,
            recipients=[MultisendErc20Recipient(RECIPIENT_A, "1")],
            memo="fallback memo",
            prefer_permit=True,
            auto_approve=True,
        ),
        broadcast=False,
        wait_receipt=False,
    )

    assert result.success is True
    assert result.steps == ("approve_erc20", "multisend_erc20")
    assert result.requires_secondary_transaction is True
    assert client.tx.approve_calls == 1
