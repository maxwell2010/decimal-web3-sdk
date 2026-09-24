"""Current NFT create/mint semantics, without funded signers or network calls."""
import copy
import importlib.util
import json
from pathlib import Path
from unittest.mock import AsyncMock

from eth_abi import decode
from eth_account import Account
from hexbytes import HexBytes
import pytest
import requests
from web3 import Web3

import decimal_web3_sdk as sdk
from decimal_web3_sdk.contracts import AbiRegistry
from decimal_web3_sdk.candy_protocol import build_unsigned_candy_call, load_candy_profile
from decimal_web3_sdk._contract_operations import ZERO_ADDRESS
from decimal_web3_sdk.nft_operations import NftOperations

ROOT = Path(__file__).resolve().parents[1]
NFT = "0x" + "11" * 20
TOKEN = "0x" + "22" * 20
OWNER = "0x" + "33" * 20
OTHER = "0x" + "44" * 20
MINIMUM = 10**15


def forbidden(*args, **kwargs):
    pytest.fail("NFT regression attempted a signature or network request")


@pytest.fixture
def client(monkeypatch):
    monkeypatch.setattr(requests.Session, "request", forbidden)
    monkeypatch.setattr(Web3.HTTPProvider, "make_request", forbidden)
    monkeypatch.setattr(Account, "sign_transaction", forbidden)
    monkeypatch.setattr(Account, "sign_message", forbidden)
    client = sdk.DecimalClient(sdk.NetworkConfig.custom(web3_urls=["https://example.invalid"]))
    client.rpc._web3 = Web3()
    client.rpc.call = AsyncMock(side_effect=forbidden)
    client.transaction_count = AsyncMock(return_value=0)
    client.gas_price = AsyncMock(return_value=1)
    client.send_raw_transaction = AsyncMock(side_effect=forbidden)
    client.nft.collection_state = AsyncMock(return_value=sdk.NftCollectionState(True, "erc721", True))
    client.nft.check_reserve_token = AsyncMock(return_value=True)
    client.nft.get_reserve = AsyncMock(return_value=sdk.NftReserve(ZERO_ADDRESS, 0, 0))
    client.nft._read_nft_call = AsyncMock(return_value=MINIMUM)
    client.tx.calculate_fee = AsyncMock(return_value="unsigned quote")
    return client


@pytest.fixture
def key():
    return "0x" + bytes(Account.create().key).hex()


def mint_request(key, **kwargs):
    return sdk.MintNftRequest(private_key=key, kind="erc721", nft=NFT, to=OWNER,
                              token_uri="ipfs://example", **kwargs)


@pytest.mark.parametrize("kind,name", [("erc721", "createDRC721"), ("erc1155", "createDRC1155")])
async def test_reserved_create_uses_current_tuple_and_no_value(client, key, kind, name):
    request = sdk.CreateNftCollectionRequest(private_key=key, creator=OWNER, kind=kind,
        symbol="NFT", name="Collection", contract_uri="ipfs://example", refundable=True, burnable=False)
    draft = await client.nft.build_operation(request)
    raw = HexBytes(draft.tx["data"])
    assert raw[:4] == Web3.keccak(text=name + "((address,string,string,string,bool,bool))")[:4]
    assert decode(["(address,string,string,string,bool,bool)"], raw[4:])[0] == (OWNER, "NFT", "Collection", "ipfs://example", True, False)
    assert draft.value_wei == 0 and draft.raw_tx is None
    shared = build_unsigned_candy_call(owner=OWNER, contract_type="nftCenter",
        signature=name + "((address,string,string,string,bool,bool))", args=[(OWNER,"NFT","Collection","ipfs://example",True,False)])
    assert HexBytes(shared["data"]) == raw and shared["value"] == "0"
    assert await client.nft.estimate_fee_for_operation(request, exact=True) == "unsigned quote"
    client.rpc.call.assert_not_called()


@pytest.mark.parametrize("kind", ["erc721", "erc1155"])
@pytest.mark.parametrize("mode", ["del", "token", "none"])
async def test_mint_routes_have_exact_total_and_match_shared_profile(client, key, kind, mode):
    quantity = 1 if kind == "erc721" else 7
    total = MINIMUM * quantity + 123
    client.nft.collection_state.return_value = sdk.NftCollectionState(True, kind, mode != "none")
    fields = {"value_wei": total} if mode == "del" else {"reserve_amount_raw": total, "reserve_token": TOKEN} if mode == "token" else {}
    request = sdk.MintNftRequest(private_key=key, kind=kind, nft=NFT, to=OWNER, token_uri="ipfs://example",
        amount=quantity, token_id=0 if kind == "erc1155" else None, **fields)
    draft = await client.nft.build_mint(request)
    contract = Web3().eth.contract(abi=AbiRegistry().load("nft_721" if kind == "erc721" else "nft_1155"))
    function, args = contract.decode_function_input(draft.tx["data"])
    assert function.fn_name == ("mintByDEL" if mode == "del" else "mint")
    assert draft.value_wei == (total if mode == "del" else 0) and draft.raw_tx is None
    if mode == "token":
        assert args["reserveAmount"] == total
        client.nft.check_reserve_token.assert_awaited_once_with(Web3.to_checksum_address(TOKEN))
    else:
        client.nft.check_reserve_token.assert_not_awaited()
    shared = build_unsigned_candy_call(owner=draft.from_address, contract_type="nft", address=NFT,
        signature=function.signature, args=list(args.values()), value_wei=draft.value_wei)
    assert HexBytes(shared["data"]) == HexBytes(draft.tx["data"])


@pytest.mark.parametrize("fields", [
    {"value_wei": -1}, {"reserve_amount_raw": 0.1}, {"amount": True}, {"amount": 2},
    {"token_id": 1}, {"value_wei": MINIMUM, "reserve_token": TOKEN},
    {"value_wei": MINIMUM, "reserve_amount_raw": 1}, {"reserve_amount_raw": MINIMUM},
    {"value_wei": MINIMUM - 1}, {"reserve_amount_raw": 1, "reserve_token": TOKEN},
])
async def test_invalid_or_ambiguous_mint_is_rejected(client, key, fields):
    with pytest.raises((TypeError, ValueError)):
        await client.nft.build_mint(mint_request(key, **fields))


@pytest.mark.parametrize("state", [sdk.NftCollectionState(False,"erc721",False), sdk.NftCollectionState(True,"erc1155",True), sdk.NftCollectionState(True,"erc721",False)])
async def test_state_prevents_wrong_or_reserveless_deposit(client, key, state):
    client.nft.collection_state.return_value = state
    with pytest.raises(ValueError):
        await client.nft.build_mint(mint_request(key, value_wei=MINIMUM))


@pytest.mark.parametrize("wrong", ["token", "type", "total", None])
async def test_existing_1155_preserves_asset_type_and_exact_rate(client, key, wrong):
    client.nft.collection_state.return_value = sdk.NftCollectionState(True,"erc1155",True)
    client.nft.get_reserve.return_value = sdk.NftReserve(TOKEN, MINIMUM * 2, 2)
    client.nft._read_nft_call.return_value = MINIMUM
    fields = {"reserve_amount_raw": MINIMUM * 3, "reserve_token": TOKEN}
    if wrong == "token":
        fields["reserve_token"] = OTHER
    elif wrong == "type":
        fields = {"value_wei": MINIMUM * 3}
    elif wrong == "total":
        fields["reserve_amount_raw"] += 1
    request = sdk.MintNftRequest(private_key=key,kind="erc1155",nft=NFT,to=OWNER,token_uri="ipfs://example",token_id=0,amount=3,**fields)
    if wrong:
        with pytest.raises(ValueError):
            await client.nft.build_mint(request)
    else:
        draft = await client.nft.build_mint(request)
        assert draft.raw_tx is None and draft.value_wei == 0


async def test_new_1155_minimum_is_per_copy_not_total(client, key):
    client.nft.collection_state.return_value = sdk.NftCollectionState(True,"erc1155",True)
    request = sdk.MintNftRequest(private_key=key,kind="erc1155",nft=NFT,to=OWNER,token_uri="ipfs://example",token_id=0,amount=2,value_wei=MINIMUM)
    with pytest.raises(ValueError, match="per NFT"):
        await client.nft.build_mint(request)


async def test_eligibility_failure_is_not_treated_as_success(client, key):
    client.nft.check_reserve_token.side_effect = RuntimeError("unavailable or rejected")
    with pytest.raises(RuntimeError):
        await client.nft.build_mint(mint_request(key, reserve_amount_raw=MINIMUM, reserve_token=TOKEN))


def test_real_receipt_identifies_collection_not_minted_ids(client):
    row = json.loads((ROOT / "tests/fixtures/nft_collection_creation.json").read_text())
    result = client.nft.created_collections(row["receipt"])
    assert len(result) == 1
    created = result[0]
    assert created.nft_address.lower() == "0x9b1129ec66afd4b7d20f95de078126853695ccfe"
    assert created.creator == row["from"]
    assert created.kind == "erc721" and created.symbol == "tttest" and created.name == "test nft"
    assert created.burnable and not created.refundable
    assert not hasattr(created, "token_id")
    assert row["balance_latest"] == row["mint_transfer_count"] == 0
    assert Web3.keccak(text="ERC721NonexistentToken(uint256)")[:4].hex() in row["owner_of_1_error"]
    contract = Web3().eth.contract(abi=AbiRegistry().load("nft_center"))
    fn, args = contract.decode_function_input(row["input"])
    assert fn.fn_name == "createDRC721Reserveless"
    meta = args["meta"]
    assert fn(tuple(meta.values()))._encode_transaction_data() == row["input"]
    receipt = copy.deepcopy(row["receipt"])
    for log in receipt["logs"]:
        log["address"] = OTHER
    assert client.nft.created_collections(receipt) == ()
    receipt["status"] = 0
    with pytest.raises(ValueError):
        client.nft.created_collections(receipt)


def test_profile_is_generated_from_canonical_abis():
    spec = importlib.util.spec_from_file_location("nft_profile", ROOT / "scripts/generate_nft_profile.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    assert module.PROFILE.read_text() == module.generated_profile()
    profile = load_candy_profile()
    assert profile["abi"]["nftCenter"] == AbiRegistry().load("nft_center")
    assert profile["nftProtocol"]["creationMintsNfts"] is False
    assert profile["nftProtocol"]["minimumReserveRaw"] == str(MINIMUM)


async def test_current_nft_does_not_offer_legacy_uri_setter_without_opt_in(client, key):
    request = sdk.SetTokenUriNftRequest(private_key=key, kind="erc721", nft=NFT, token_id=1, token_uri="ipfs://example")
    with pytest.raises(ValueError, match="legacy opt-in"):
        await client.nft.set_token_uri(request, broadcast=False)
    client.rpc.call.assert_not_called()


async def test_contract_reads_rebind_provider_and_preserve_block(client):
    calls = []
    class Function:
        def __call__(self, *args):
            calls.append(args)
            return self
        def call(self, **kwargs):
            calls.append(kwargs)
            return (True, 0, True)
    from types import SimpleNamespace
    target = SimpleNamespace(eth=SimpleNamespace(contract=lambda **kwargs: SimpleNamespace(get_function_by_name=lambda name: Function())))
    async def read(fn):
        return fn(target)
    client.rpc.call = AsyncMock(side_effect=read)
    client.nft._read_nft_call = NftOperations._read_nft_call.__get__(client.nft)
    state = await NftOperations.collection_state(client.nft, NFT, block_identifier=123)
    assert state == sdk.NftCollectionState(True, "erc721", True)
    assert calls == [(Web3.to_checksum_address(NFT),), {"block_identifier": 123}]
    client.rpc.call.assert_awaited_once()
