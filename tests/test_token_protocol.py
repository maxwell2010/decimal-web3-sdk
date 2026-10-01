"""Token protocol guards and calldata, without live signing or broadcasting."""

from types import SimpleNamespace
from unittest.mock import AsyncMock
from decimal import Decimal

import pytest
from web3 import Web3

from decimal_web3_sdk.token import (
    CreateReservelessTokenRequest,
    CreateTokenRequest,
    MintTokenRequest,
    TokenService,
    UpdateTokenDetailsRequest,
    token_creation_required_reserve_wei,
)
from decimal_web3_sdk.erc20 import TokenInfo
from decimal_web3_sdk.transactions import TransactionResult


KEY = "0x" + "11" * 32
TOKEN = "0x1000000000000000000000000000000000000001"
CENTER = "0x2000000000000000000000000000000000000002"


@pytest.mark.asyncio
async def test_reserve_properties_keep_minimum_above_current_supply_exact():
    token, client = service()
    client.erc20.info = AsyncMock(return_value=TokenInfo(TOKEN, "Baron", "BARON", 18))
    values = {
        "minTotalSupply": 100_000_000 * 10**18,
        "maxTotalSupply": 10_000_000_000 * 10**18,
        "totalSupply": 44_700_070_663_894_964_849_192_929,
        "creator": CENTER,
        "identity": "ipfs://example",
    }
    token._read_token_property = AsyncMock(side_effect=lambda address, name: values[name])
    result = await token.properties(TOKEN)
    assert result.kind == "reserve" and result.owner is None
    assert result.min_total_supply_raw > result.total_supply_raw
    assert result.as_dict()["min_total_supply"]["raw"] == str(values["minTotalSupply"])
    assert result.as_dict()["total_supply"]["raw"] == str(values["totalSupply"])


@pytest.mark.asyncio
async def test_reserveless_properties_use_owner_cap_and_no_reserve_fields():
    token, client = service()
    client.erc20.info = AsyncMock(return_value=TokenInfo(TOKEN, "Revolutes", "REVOLUTES", 18))
    values = {
        "owner": CENTER,
        "cap": 2**256 - 1,
        "mintable": True,
        "burnable": True,
        "totalSupply": 25_670_131_708_404_964_400,
        "identity": "identity-hash",
    }
    def read(address, name):
        if name == "minTotalSupply":
            raise ValueError("method unavailable")
        return values[name]
    token._read_token_property = AsyncMock(side_effect=read)
    result = await token.properties(TOKEN)
    assert result.kind == "reserveless" and result.creator is None
    assert result.min_total_supply_raw is None and result.max_total_supply_raw is None
    assert result.unlimited_cap
    assert result.as_dict()["total_supply"]["formatted"] == "25.6701317084049644"
    assert result.as_dict()["cap"]["raw"] == str(2**256 - 1)


@pytest.mark.asyncio
async def test_properties_do_not_replace_rpc_failure_with_zero():
    token, client = service()
    client.erc20.info = AsyncMock(return_value=TokenInfo(TOKEN, "Unknown", "UNK", 18))
    token._read_token_property = AsyncMock(side_effect=ConnectionError("RPC unavailable"))
    with pytest.raises(ConnectionError):
        await token.properties(TOKEN)


class FakeTx:
    def __init__(self):
        self.calls = []
        self.results = []

    async def build_contract_call(self, request):
        self.calls.append(request)
        return request

    async def send_draft(self, draft, private_key, broadcast, wait_receipt):
        assert not broadcast
        return self.results.pop(0) if self.results else TransactionResult(success=True, status="dry_run")


class FakeRpc:
    def __init__(self, value=True):
        self.value = value

    async def call(self, callback):
        if isinstance(self.value, Exception):
            raise self.value
        return self.value


def service(chain_id=202020, rpc_value=True, name=None):
    client = SimpleNamespace(
        web3=Web3(),
        config=SimpleNamespace(
            chain_id=chain_id, name=name or ("decimal-mainnet" if chain_id == 75 else "decimal-testnet"),
            contracts=SimpleNamespace(token_center=CENTER),
        ),
        tx=FakeTx(),
        rpc=FakeRpc(rpc_value),
        erc20=SimpleNamespace(),
    )
    return TokenService(client), client


def reserve_request(symbol, reserve_value_wei=None):
    return CreateTokenRequest(
        name="Example", symbol=symbol, initial_mint_raw=100, min_total_supply_raw=0,
        max_total_supply_raw=1000, crr=50, identity="identity", private_key=KEY,
        reserve_value_wei=reserve_value_wei,
    )


def reserveless_request(symbol):
    return CreateReservelessTokenRequest(
        name="Example", symbol=symbol, mintable=True, burnable=True,
        initial_mint_raw=100, cap_raw=1000, identity="identity", private_key=KEY,
    )


@pytest.mark.asyncio
@pytest.mark.parametrize("symbol,fee", [
    ("abc", "2500"), ("abcd", "250"), ("abcde", "25"),
    ("abcdef", "2.5"), ("abcdefg", "0.25"), ("abcdefghij", "0.25"),
])
async def test_testnet_creation_default_value(symbol, fee):
    token, client = service()
    await token.create(reserve_request(symbol))
    assert client.tx.calls[0].value_wei == Web3.to_wei(1, "ether") + Web3.to_wei(fee, "ether")
    function, args = token._token_center_contract().decode_function_input(client.tx.calls[0].data)
    assert function.fn_name == "createToken"
    assert args["meta"]["symbol"] == symbol


@pytest.mark.asyncio
async def test_mainnet_default_unchanged_and_explicit_value_preserved():
    token, client = service(chain_id=75)
    await token.create(reserve_request("EXAMPLE"))
    assert client.tx.calls[0].value_wei == token_creation_required_reserve_wei("EXAMPLE")
    token, client = service()
    explicit = Web3.to_wei("1.25", "ether") + 123
    await token.create(reserve_request("example", reserve_value_wei=explicit))
    assert client.tx.calls[0].value_wei == explicit


@pytest.mark.asyncio
async def test_testnet_rejects_underfunded_explicit_reserve():
    token, client = service()
    with pytest.raises(ValueError, match="reserve value"):
        await token.create(reserve_request("example", reserve_value_wei=Web3.to_wei(1, "ether")))
    assert not client.tx.calls


@pytest.mark.asyncio
async def test_devnet_does_not_inherit_testnet_fee_schedule():
    token, client = service(name="decimal-devnet")
    await token.create(reserve_request("EXAMPLE"))
    assert client.tx.calls[0].value_wei == token_creation_required_reserve_wei("EXAMPLE")


@pytest.mark.asyncio
@pytest.mark.parametrize("symbol", ["ABC", "aB3", "ab", "abcdefghijk", "a-b", "a b", "ébc"])
async def test_testnet_rejects_invalid_symbols_before_build(symbol):
    token, client = service()
    with pytest.raises(ValueError, match="symbol"):
        await token.create(reserve_request(symbol))
    with pytest.raises(ValueError, match="symbol"):
        await token.create_reserveless(reserveless_request(symbol))
    assert not client.tx.calls


@pytest.mark.asyncio
async def test_reserveless_creation_is_zero_value():
    token, client = service()
    await token.create_reserveless(reserveless_request("abc3"))
    assert client.tx.calls[0].value_wei == 0


@pytest.mark.asyncio
@pytest.mark.parametrize("rpc_value", [False, RuntimeError("unsupported")])
async def test_mint_fails_closed_without_mintable_reserveless_token(rpc_value):
    token, client = service(rpc_value=rpc_value)
    request = MintTokenRequest(token=TOKEN, to=TOKEN, amount=1, private_key=KEY, decimals=18)
    with pytest.raises(ValueError, match="Mint|mintable"):
        await token.mint(request)
    assert not client.tx.calls


@pytest.mark.asyncio
async def test_mint_encodes_only_after_mintable_read():
    token, client = service()
    assert "mintable" in [entry["name"] for entry in token._token_contract(TOKEN).abi]
    assert "getMintable" not in [entry["name"] for entry in token._token_contract(TOKEN).abi]
    request = MintTokenRequest(token=TOKEN, to=CENTER, amount=2, private_key=KEY, decimals=18)
    await token.mint(request)
    function, args = token._token_contract(TOKEN).decode_function_input(client.tx.calls[0].data)
    assert function.fn_name == "mint"
    assert args["amount"] == 2 * 10**18


@pytest.mark.asyncio
async def test_update_details_uses_two_ordered_calls_and_keeps_first_status():
    token, client = service(rpc_value=10**18)
    client.tx.results.extend([
        TransactionResult(success=True, status="dry_run", fee_wei=10**16),
        TransactionResult(success=True, status="dry_run", fee_wei=2 * 10**16),
    ])
    request = UpdateTokenDetailsRequest(token=TOKEN, identity="new", max_total_supply_raw=900, private_key=KEY)
    result = await token.update_details(request)
    assert result.fee_wei == 3 * 10**16
    assert result.fee_del == Decimal("0.03")
    assert result.events["update_identity"]["fee_wei"] == 10**16
    assert result.events["update_max_total_supply"]["fee_wei"] == 2 * 10**16
    assert [token._token_contract(TOKEN).decode_function_input(call.data)[0].fn_name for call in client.tx.calls] == [
        "updateIdentity", "updateMaxTotalSupply",
    ]
    assert token._token_contract(TOKEN).decode_function_input(client.tx.calls[1].data)[1]["maximum"] == 900


@pytest.mark.asyncio
async def test_update_details_stops_on_first_failure_and_rejects_unsafe_broadcast():
    token, client = service(rpc_value=10**18)
    client.tx.results.append(TransactionResult(success=False, status="failed", error="revert"))
    request = UpdateTokenDetailsRequest(token=TOKEN, identity="new", max_total_supply_raw=900, private_key=KEY)
    result = await token.update_details(request)
    assert not result.success
    assert len(client.tx.calls) == 1
    with pytest.raises(ValueError, match="wait_receipt"):
        await token.update_details(request, broadcast=True)
    assert len(client.tx.calls) == 1


@pytest.mark.asyncio
async def test_update_details_requires_reserve_token():
    token, client = service(rpc_value=RuntimeError("unsupported"))
    request = UpdateTokenDetailsRequest(token=TOKEN, identity="new", max_total_supply_raw=900, private_key=KEY)
    with pytest.raises(ValueError, match="reserve token"):
        await token.update_details(request)
    assert not client.tx.calls
