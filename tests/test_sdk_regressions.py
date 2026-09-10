from __future__ import annotations

from types import SimpleNamespace

import pytest
from eth_account import Account
from web3 import Web3

from decimal_web3_sdk.config import OFFICIAL_MAINNET_API_ROOT, NetworkConfig, SystemContracts
from decimal_web3_sdk.decimal import (
    DecimalService,
    HoldDelRequest,
    MultisendDelRequest,
    MultisendRecipient,
    TransferStakeDelRequest,
)
from decimal_web3_sdk.erc20 import PermitSignature
from decimal_web3_sdk.rest import RestClient
from decimal_web3_sdk.token import ConvertTokenRequest, TokenService
from decimal_web3_sdk.test_harness import _test_private_key_from_env, run_env_training
from decimal_web3_sdk.transactions import (
    ContractCallRequest,
    NativeTransferRequest,
    TransactionDraft,
    TransactionResult,
)
from decimal_web3_sdk.wallet import (
    derivation_path_for_index,
    mnemonic_to_account,
    mnemonic_to_accounts,
)


Account.enable_unaudited_hdwallet_features()
PRIVATE_KEY = "0x" + Account.create().key.hex()
_, MNEMONIC = Account.create_with_mnemonic(num_words=12)
TOKEN_IN = "0x1000000000000000000000000000000000000001"
TOKEN_OUT = "0x2000000000000000000000000000000000000002"
VALIDATOR_A = "0x3000000000000000000000000000000000000003"
VALIDATOR_B = "0x4000000000000000000000000000000000000004"


class _FakeTx:
    def __init__(self) -> None:
        self.native_request: NativeTransferRequest | None = None
        self.contract_request: ContractCallRequest | None = None
        self.approve_calls = 0
        self.send_del_calls = 0

    async def build_native_transfer(self, request: NativeTransferRequest) -> TransactionDraft:
        self.native_request = request
        return TransactionDraft(
            tx={
                "to": Web3.to_checksum_address(request.to),
                "value": Web3.to_wei(request.amount_del, "ether"),
                "data": "0x" + (request.memo or "").encode().hex(),
            },
            from_address=Web3.to_checksum_address("0xf39fd6e51aad88f6f4ce6ab8827279cfffb92266"),
            to_address=Web3.to_checksum_address(request.to),
            value_wei=Web3.to_wei(request.amount_del, "ether"),
        )

    async def build_contract_call(self, request: ContractCallRequest) -> TransactionDraft:
        self.contract_request = request
        return TransactionDraft(
            tx={"to": Web3.to_checksum_address(request.contract), "data": request.data, "value": request.value_wei},
            from_address=Web3.to_checksum_address("0xf39fd6e51aad88f6f4ce6ab8827279cfffb92266"),
            to_address=Web3.to_checksum_address(request.contract),
            value_wei=request.value_wei,
        )

    async def send_draft(self, draft, private_key, broadcast, wait_receipt) -> TransactionResult:
        return TransactionResult(success=True, status="dry_run", gas=21_000, fee_wei=1)

    async def approve_erc20(self, *args, **kwargs) -> TransactionResult:
        self.approve_calls += 1
        return TransactionResult(success=True, status="dry_run")

    async def send_del(self, request, broadcast=False, wait_receipt=False) -> TransactionResult:
        self.send_del_calls += 1
        await self.build_native_transfer(request)
        return TransactionResult(success=True, status="pending" if broadcast else "dry_run")


class _FakeErc20:
    async def info(self, token: str):
        return SimpleNamespace(decimals=18)

    async def balance(self, token: str, owner: str):
        return SimpleNamespace(raw=10**24)

    async def allowance(self, token: str, owner: str, spender: str) -> int:
        return 0

    async def permit_signature(self, *args, **kwargs) -> PermitSignature:
        return PermitSignature(deadline=2**256 - 1, v=27, r=b"\x01" * 32, s=b"\x02" * 32)


class _FakeClient:
    def __init__(self) -> None:
        self.web3 = Web3()
        self.config = NetworkConfig(
            contracts=SystemContracts(
                delegation="0x5000000000000000000000000000000000000005",
                token_center="0x6000000000000000000000000000000000000006",
                wdel="0x7000000000000000000000000000000000000007",
            )
        )
        self.tx = _FakeTx()
        self.erc20 = _FakeErc20()


class _FakeDelegationCall:
    def __init__(self, value) -> None:
        self._value = value

    def call(self):
        return self._value


class _FakeDelegationFunctions:
    def __init__(self, regular, held) -> None:
        self._regular = regular
        self._held = held
        self.get_stake_args = None
        self.get_hold_stake_args = None

    def getStake(self, *args):
        self.get_stake_args = args
        return _FakeDelegationCall(self._regular)

    def getHoldStake(self, *args):
        self.get_hold_stake_args = args
        return _FakeDelegationCall(self._held)


class _FakeDelegationContract:
    def __init__(self, regular, held) -> None:
        self.functions = _FakeDelegationFunctions(regular, held)


class _FakeRpc:
    async def call(self, callback):
        return callback(None)


@pytest.mark.asyncio
async def test_one_recipient_del_multisend_is_direct_transfer_with_memo() -> None:
    client = _FakeClient()
    service = DecimalService(client)
    recipient = "0x8000000000000000000000000000000000000008"

    draft = await service.build_multisend_del(
        MultisendDelRequest(
            recipients=[MultisendRecipient(to=recipient, amount_del="0.01")],
            private_key=PRIVATE_KEY,
            memo="single recipient",
        )
    )

    assert client.tx.native_request is not None
    assert client.tx.contract_request is None
    assert draft.to_address == Web3.to_checksum_address(recipient)
    assert bytes.fromhex(draft.tx["data"][2:]).decode() == "single recipient"

    result = await service.multisend_del(
        MultisendDelRequest(
            recipients=[MultisendRecipient(to=recipient, amount_del="0.01")],
            private_key=PRIVATE_KEY,
            memo="single recipient",
        )
    )
    assert result.success is True
    assert client.tx.send_del_calls == 1


@pytest.mark.asyncio
async def test_convert_uses_permit_overload_as_one_transaction() -> None:
    client = _FakeClient()
    result = await TokenService(client).convert(
        ConvertTokenRequest(
            token_in=TOKEN_IN,
            token_out=TOKEN_OUT,
            amount_in="1",
            min_amount_out="0.9",
            private_key=PRIVATE_KEY,
        )
    )

    assert result.success is True
    assert result.one_transaction is True
    assert result.steps == ("convert_erc20_by_permit",)
    assert client.tx.approve_calls == 0
    assert client.tx.contract_request is not None
    expected = Web3.keccak(
        text="convert(address,address,uint256,uint256,address,uint256,uint8,bytes32,bytes32)"
    )[:4].hex()
    assert client.tx.contract_request.data[2:10] == expected


@pytest.mark.asyncio
async def test_del_stake_transfer_uses_wdel_without_approve() -> None:
    client = _FakeClient()
    result = await DecimalService(client).transfer_stake_del(
        TransferStakeDelRequest(
            validator=VALIDATOR_A,
            new_validator=VALIDATOR_B,
            amount_del="0.01",
            private_key=PRIVATE_KEY,
        )
    )

    assert result.success is True
    assert result.steps == ("transfer_stake_del",)
    assert client.tx.approve_calls == 0
    assert client.tx.contract_request is not None
    expected = Web3.keccak(text="transfer(address,address,uint256,address)")[:4].hex()
    assert client.tx.contract_request.data[2:10] == expected


@pytest.mark.asyncio
async def test_hold_result_returns_unlock_timestamp_and_iso_time() -> None:
    client = _FakeClient()
    timestamp = 1_800_000_000
    result = await DecimalService(client).hold_del(
        HoldDelRequest(
            validator=VALIDATOR_A,
            amount_del="0.01",
            hold_timestamp=timestamp,
            private_key=PRIVATE_KEY,
        )
    )

    assert result.hold_timestamp == timestamp
    assert result.hold_time == "2027-01-15T08:00:00Z"


@pytest.mark.asyncio
async def test_direct_contract_reads_return_regular_and_held_token_stakes(monkeypatch) -> None:
    client = _FakeClient()
    client.rpc = _FakeRpc()
    service = DecimalService(client)
    delegator = "0x9000000000000000000000000000000000000009"
    hold_timestamp = 1_787_933_707
    regular = (VALIDATOR_A, delegator, TOKEN_IN, 100 * 10**18, 0, 1, 0)
    held = (VALIDATOR_A, delegator, TOKEN_IN, 100 * 10**18, 0, 1, hold_timestamp)
    contract = _FakeDelegationContract(regular, held)
    monkeypatch.setattr(service, "_delegation_contract", lambda: contract)

    regular_stake = await service.get_stake(VALIDATOR_A, delegator, TOKEN_IN)
    held_stake = await service.get_hold_stake(
        VALIDATOR_A,
        delegator,
        TOKEN_IN,
        hold_timestamp,
    )

    assert regular_stake.amount() == 100
    assert regular_stake.hold_time is None
    assert held_stake.amount() == 100
    assert held_stake.hold_timestamp == hold_timestamp
    assert held_stake.hold_time == "2026-08-28T16:15:07Z"
    assert contract.functions.get_hold_stake_args[-1] == hold_timestamp


def test_mnemonic_sequence_derives_indices_zero_through_nine() -> None:
    wallets = mnemonic_to_accounts(MNEMONIC)

    assert len(wallets) == 10
    assert len({wallet.address for wallet in wallets}) == 10
    assert wallets[0].derivation_path == derivation_path_for_index(0)
    assert wallets[9].derivation_path == derivation_path_for_index(9)
    assert mnemonic_to_account(MNEMONIC, account_index=9).address == wallets[9].address
    request = NativeTransferRequest.from_mnemonic(
        to=wallets[0].address,
        amount_del="0.01",
        mnemonic=MNEMONIC,
        account_index=9,
    )
    assert request.private_key == wallets[9].private_key


def test_network_config_uses_oracle_gas_price_by_default(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("DECIMAL_MAX_GAS_PRICE_WEI", raising=False)
    monkeypatch.delenv("DECIMAL_MAX_GAS_PRICE_GWEI", raising=False)
    monkeypatch.delenv("DECIMAL_GAS_PRICE_GWEI", raising=False)
    monkeypatch.setenv("DECIMAL_API_BASE", "")

    config = NetworkConfig.mainnet()
    custom = NetworkConfig.custom(web3_urls=["https://node.invalid/web3/"])

    assert config.safety.max_gas_price_wei is None
    assert custom.safety.max_gas_price_wei is None
    assert config.api_base_url == OFFICIAL_MAINNET_API_ROOT


def test_training_credentials_are_network_scoped(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("DECIMAL_TEST_NETWORK", "mainnet")
    monkeypatch.setenv("DECIMAL_MAINNET_TEST_MNEMONIC", MNEMONIC)
    monkeypatch.setenv("DECIMAL_TESTNET_TEST_MNEMONIC", "unused")

    private_key = _test_private_key_from_env("mainnet")

    assert private_key == mnemonic_to_account(MNEMONIC).private_key


@pytest.mark.asyncio
async def test_training_rejects_mnemonic_address_mismatch_before_rpc(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("DECIMAL_TEST_NETWORK", "mainnet")
    monkeypatch.setenv("DECIMAL_MAINNET_TEST_MNEMONIC", MNEMONIC)
    monkeypatch.setenv(
        "DECIMAL_MAINNET_TEST_EXPECTED_ADDRESS",
        "0x0000000000000000000000000000000000000001",
    )

    with pytest.raises(RuntimeError, match="address mismatch"):
        await run_env_training()


@pytest.mark.asyncio
async def test_withdrawal_history_does_not_hide_total_api_failure() -> None:
    class _FailingRestClientOwner:
        config = SimpleNamespace(safety=SimpleNamespace(rest_max_limit=100))

        async def rest_get(self, *args, **kwargs):
            raise ConnectionError("upstream unavailable")

    with pytest.raises(ConnectionError, match="upstream unavailable"):
        await RestClient(_FailingRestClientOwner()).wallet_stake_withdrawals(
            "0x0000000000000000000000000000000000000001"
        )
