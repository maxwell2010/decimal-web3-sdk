"""Offline safety/encoding tests for the explicit read-only atomic probe."""
import importlib.util
from pathlib import Path
from unittest.mock import Mock

from eth_abi import decode, encode
from eth_account import Account
import pytest
import requests
from web3 import Web3

from decimal_web3_sdk.contracts import AbiRegistry
from decimal_web3_sdk.decimal import MULTICALL_ABI

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("nft_atomic_probe", ROOT / "scripts/probe_nft_atomic.py")
probe = importlib.util.module_from_spec(spec)
spec.loader.exec_module(probe)


@pytest.fixture(autouse=True)
def no_signatures_or_network(monkeypatch):
    def forbidden(*args, **kwargs):
        pytest.fail("Offline atomic probe regression attempted network/signature")
    monkeypatch.setattr(requests.Session, "request", forbidden)
    monkeypatch.setattr(Account, "sign_transaction", forbidden)
    monkeypatch.setattr(Account, "sign_message", forbidden)


@pytest.mark.parametrize("method", ["eth_sendTransaction", "eth_sendRawTransaction", "eth_sign",
                                   "personal_sign", "eth_signTypedData_v4", "debug_setHead"])
def test_rpc_transport_rejects_mutating_methods_before_request(method):
    rpc = probe.ReadOnlyRpc("https://example.invalid")
    with pytest.raises(ValueError, match="Forbidden RPC"):
        rpc.call(method, [])
    assert not rpc.methods


@pytest.mark.parametrize("kind", ["721", "1155"])
@pytest.mark.parametrize("reserve", [False, True])
def test_sdk_builders_encode_creator_recipient_and_exact_native_reserve(kind, reserve):
    create = probe.create_call(kind, reserve)
    center = Web3().eth.contract(abi=AbiRegistry().load("nft_center"))
    function, fields = center.decode_function_input(create["data"])
    assert function.fn_name == "createDRC" + kind + ("" if reserve else "Reserveless")
    assert fields["meta"]["creator"].lower() == probe.OWNER.lower()
    assert create["value"] == "0" and create["to"] == probe.CENTER
    nft = Web3.to_checksum_address("0x" + "12" * 20)
    mint = probe.mint_call(kind, reserve, nft)
    contract = Web3().eth.contract(abi=AbiRegistry().load("nft_" + kind))
    function, fields = contract.decode_function_input(mint["data"])
    assert function.fn_name == ("mintByDEL" if reserve else "mint")
    assert list(fields.values())[0].lower() == probe.OWNER.lower()
    assert int(mint["value"]) == ((10**15 * (2 if kind == "1155" else 1)) if reserve else 0)
    if kind == "1155":
        assert list(fields.values())[1:3] == [0, 2]
    aggregate = probe.aggregate([create, mint])
    function, fields = Web3().eth.contract(abi=MULTICALL_ABI).decode_function_input(aggregate["data"])
    assert function.fn_name == "aggregate"
    assert len(fields["calls"]) == 2
    assert fields["calls"][1]["target"] == nft
    assert sum(c["value"] for c in fields["calls"]) == int(aggregate["value"], 16)


def test_unsafe_security_control_does_not_masquerade_as_user_creator():
    call = probe.create_call("721", False, creator=probe.MULTICALL)
    contract = Web3().eth.contract(abi=AbiRegistry().load("nft_center"))
    _, fields = contract.decode_function_input(call["data"])
    assert fields["meta"]["creator"].lower() == probe.MULTICALL.lower()
    assert fields["meta"]["creator"].lower() != probe.OWNER.lower()


@pytest.mark.parametrize("value", ["1000000000000000", "0x38d7ea4c68000", 10**15])
def test_simulation_only_sends_pinned_eth_call(value):
    rpc = Mock()
    probe.simulate(rpc, {"chainId": 75, "from": probe.OWNER, "to": probe.CENTER,
                         "data": "0x12345678", "value": value}, "0x201bb35")
    method, params = rpc.call.call_args.args
    assert method == "eth_call"
    assert params[1] == "0x201bb35"
    assert params[0]["value"] == hex(10**15)
    assert set(params[0]) == {"from", "to", "data", "value", "gas"}


@pytest.mark.parametrize("error", [
    {"code": -32000, "message": "state has been pruned"},
    {"code": -32601, "message": "method not found"},
    {"code": 429, "message": "rate limited"},
])
def test_infrastructure_failure_is_not_a_passing_contract_rejection(error):
    operation = Mock(side_effect=probe.RpcError(error))
    with pytest.raises(probe.RpcError):
        probe.expected_revert(operation)


def test_expected_revert_requires_actual_rejection():
    with pytest.raises(AssertionError, match="simulation succeeded"):
        probe.expected_revert(lambda: "0x")
    error = {"code": 3, "message": "execution reverted", "data": "0x47bc7cc8"}
    assert probe.expected_revert(Mock(side_effect=probe.RpcError(error))) == error
    assert probe.ONLY_CREATOR == "0x47bc7cc8"


def test_aggregate_decodes_simulation_outputs_not_transaction_receipts():
    encoded = "0x" + encode(["uint256", "bytes[]"], [123, [encode(["uint256"], [1])]]).hex()
    rpc = Mock()
    rpc.call.return_value = encoded
    outputs = probe.aggregate_results(rpc, [probe.create_call("721", False)], "0x7b")
    assert decode(["uint256"], outputs[0])[0] == 1
    assert rpc.call.call_args.args[0] == "eth_call"


def test_wrong_chain_stops_before_simulation():
    rpc = Mock()
    rpc.call.return_value = "0x1"
    with pytest.raises(AssertionError, match="Mainnet profile required"):
        probe.probe(rpc)
    rpc.call.assert_called_once_with("eth_chainId", [])
