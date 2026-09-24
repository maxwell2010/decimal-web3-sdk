"""Read-only create+mint experiments using the SDK ABI/unsigned builders.

This is NOT an atomic mint API or a transaction sender. No keys, signatures,
dotenv, uploads, approvals or broadcasts. The unsafe multicall-creator case is
a negative security control, never a recommendation for a funded transaction.
Run: python scripts/probe_nft_atomic.py --rpc https://node.decimalchain.com/web3/
"""
from __future__ import annotations

import argparse
from collections import Counter
import json
from pathlib import Path
import sys

from eth_abi import decode
import requests
from web3 import Web3

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from decimal_web3_sdk.candy_protocol import build_unsigned_candy_call  # noqa: E402
from decimal_web3_sdk.config import SystemContracts  # noqa: E402
from decimal_web3_sdk.contracts import AbiRegistry  # noqa: E402
from decimal_web3_sdk.decimal import MULTICALL_ABI  # noqa: E402

OWNER = Web3.to_checksum_address("0x40900a48273644768c09183e00e43528c17a29f6")
CONTRACTS = SystemContracts()
CENTER = Web3.to_checksum_address(CONTRACTS.nft_center)
MULTICALL = Web3.to_checksum_address(CONTRACTS.multicall)
ZERO = "0x" + "00" * 20
URI = "ipfs://QmUs4nS5VJwacxpjwLz2zqnbXLD2GhUJkeTGdrbBW1mh79"
GAS = hex(10_000_000)
ONLY_CREATOR = "0x" + Web3.keccak(text="OnlyCreator()")[:4].hex()


class RpcError(RuntimeError):
    def __init__(self, error):
        self.error = error
        super().__init__(json.dumps(error, ensure_ascii=False))


class ReadOnlyRpc:
    ALLOWED = frozenset({"eth_chainId", "eth_blockNumber", "eth_getBlockByNumber",
                         "eth_getCode", "eth_call", "eth_getBalance"})

    def __init__(self, url):
        self.url = url
        self.session = requests.Session()
        self.methods = Counter()

    def call(self, method, params):
        if method not in self.ALLOWED:
            raise ValueError(f"Forbidden RPC method: {method}")
        self.methods[method] += 1
        response = self.session.post(self.url, json={"jsonrpc": "2.0", "id": 1,
            "method": method, "params": params}, timeout=25)
        response.raise_for_status()
        value = response.json()
        if "error" in value:
            raise RpcError(value["error"])
        return value["result"]


def create_call(kind, reserve, creator=OWNER):
    method = "createDRC" + kind + ("" if reserve else "Reserveless")
    return build_unsigned_candy_call(owner=OWNER, contract_type="nftCenter",
        signature=method + "((address,string,string,string,bool,bool))",
        args=[(creator, "SDKPROBE", "SDK read-only atomic probe", URI, True, True)])


def mint_call(kind, reserve, collection):
    args = [OWNER]
    if kind == "1155":
        args += [0, 2]
    args += [URI]
    signature = "mintByDEL(" if reserve else "mint("
    signature += "address," + ("uint256,uint256," if kind == "1155" else "") + "string"
    if not reserve:
        signature += ",uint256,address"
        args += [0, ZERO]
    signature += ")"
    return build_unsigned_candy_call(owner=OWNER, contract_type="nft", address=collection,
        signature=signature, args=args, value_wei=(10**15 * (2 if kind == "1155" else 1)) if reserve else 0)


def aggregate(calls):
    contract = Web3().eth.contract(address=MULTICALL, abi=MULTICALL_ABI)
    tuples = [(Web3.to_checksum_address(c["to"]), int(c["value"]), c["data"]) for c in calls]
    return {"from": OWNER, "to": MULTICALL, "gas": GAS,
            "value": hex(sum(int(c["value"]) for c in calls)),
            "data": contract.functions.aggregate(tuples)._encode_transaction_data()}


def read_call(kind, collection, name, *args):
    abi = AbiRegistry().load("nft_" + kind)
    contract = Web3().eth.contract(address=Web3.to_checksum_address(collection), abi=abi)
    return {"to": collection, "value": 0,
            "data": contract.get_function_by_name(name)(*args)._encode_transaction_data()}


def simulate(rpc, call, block):
    tx = {k: call[k] for k in ("from", "to", "data") if k in call}
    tx.setdefault("from", OWNER)
    value = call.get("value", 0)
    value = int(value, 16) if isinstance(value, str) and value.startswith("0x") else int(value)
    tx.update(value=hex(value), gas=GAS)
    return rpc.call("eth_call", [tx, block])


def aggregate_results(rpc, calls, block):
    result = simulate(rpc, aggregate(calls), block)
    _, returns = decode(["uint256", "bytes[]"], bytes.fromhex(result[2:]))
    return returns


def expected_revert(operation):
    try:
        operation()
    except RpcError as exc:
        # Transport/state availability failures are NOT successful negative tests.
        if "revert" not in json.dumps(exc.error).lower():
            raise
        return exc.error
    raise AssertionError("Expected contract revert, but simulation succeeded")


def probe(rpc):
    assert int(rpc.call("eth_chainId", []), 16) == 75, "Mainnet profile required"
    block = rpc.call("eth_blockNumber", [])
    header = rpc.call("eth_getBlockByNumber", [block, False])
    assert int(header["gasLimit"], 16) >= int(GAS, 16)
    assert int(rpc.call("eth_getBalance", [OWNER, block]), 16) >= 2 * 10**15
    for target in (CENTER, MULTICALL):
        assert rpc.call("eth_getCode", [target, block]) != "0x"
    report = {"rpc": rpc.url, "chain_id": 75, "block": int(block, 16),
              "block_hash": header["hash"], "sender_public_address": OWNER,
              "center": CENTER, "multicall": MULTICALL, "broadcasts": 0,
              "signatures": 0, "cases": []}
    for kind in ("721", "1155"):
        for reserve in (False, True):
            create = create_call(kind, reserve)
            raw = simulate(rpc, create, block)
            collection = Web3.to_checksum_address(decode(["address"], bytes.fromhex(raw[2:]))[0])
            assert rpc.call("eth_getCode", [collection, block]) == "0x"
            creator = read_call(kind, collection, "creator")
            balance = read_call(kind, collection, "balanceOf", OWNER, *([0] if kind == "1155" else []))
            returns = aggregate_results(rpc, [create, creator, balance], block)
            assert decode(["address"], returns[0])[0].lower() == collection.lower()
            assert decode(["address"], returns[1])[0].lower() == OWNER.lower()
            assert decode(["uint256"], returns[2])[0] == 0
            mint = mint_call(kind, reserve, collection)
            failure = expected_revert(lambda: aggregate_results(rpc, [create, mint, balance], block))

            # Security control: this succeeds only by permanently assigning the
            # creator role to an unrestricted PUBLIC multicall, not the user.
            unsafe_create = create_call(kind, reserve, creator=MULTICALL)
            checks = [creator, balance]
            if kind == "721":
                checks += [read_call(kind, collection, "ownerOf", 1)]
            if reserve:
                checks += [read_call(kind, collection, "getReserve", 1 if kind == "721" else 0)]
            unsafe = aggregate_results(rpc, [unsafe_create, mint, *checks], block)
            observed_creator = Web3.to_checksum_address(decode(["address"], unsafe[2])[0])
            observed_balance = decode(["uint256"], unsafe[3])[0]
            assert observed_creator == MULTICALL
            assert observed_balance == (1 if kind == "721" else 2)
            if kind == "721":
                assert decode(["address"], unsafe[4])[0].lower() == OWNER.lower()
            reserve_result = None
            if reserve:
                token, amount, reserve_type = decode(["(address,uint256,uint8)"], unsafe[-1])[0]
                assert token == ZERO and amount == int(mint["value"]) and reserve_type == 1
                reserve_result = {"token": token, "amount_raw": str(amount), "type": reserve_type}
            assert rpc.call("eth_getCode", [collection, block]) == "0x"
            report["cases"].append({"standard": "DRC" + kind,
                "reserve": "DEL" if reserve else "none", "simulated_address": collection,
                "create_only_balance": 0, "eoa_creator_create_mint": "reverted",
                "revert": failure, "public_multicall_creator_control": "succeeded_unsafe",
                "observed_creator": observed_creator, "observed_balance": observed_balance,
                "observed_reserve": reserve_result, "code_after_simulation": "0x"})

    # Existing, public, reserveless user collection: separate mint simulation
    # proves mint calldata is valid and exposes the precise caller restriction.
    existing = Web3.to_checksum_address("0x9b1129ec66afd4b7d20f95de078126853695ccfe")
    mint = mint_call("721", False, existing)
    new_id = decode(["uint256"], bytes.fromhex(simulate(rpc, mint, block)[2:]))[0]
    failure = expected_revert(lambda: simulate(rpc, {**mint, "from": MULTICALL}, block))
    assert ONLY_CREATOR.lower() in json.dumps(failure).lower()
    report["existing_collection_control"] = {"collection": existing,
        "owner_mint": "succeeded_in_simulation", "simulated_token_id": new_id,
        "multicall_sender_mint": "OnlyCreator()", "selector": ONLY_CREATOR, "revert": failure}
    report["rpc_methods"] = dict(rpc.methods)
    return report


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--rpc", required=True, help="Read-only Decimal mainnet JSON-RPC URL")
    args = parser.parse_args()
    print(json.dumps(probe(ReadOnlyRpc(args.rpc)), indent=2, ensure_ascii=False))
