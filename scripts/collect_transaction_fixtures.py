"""Collect public, already-mined mainnet examples. No keys, signing or broadcast."""

from __future__ import annotations

import argparse
import asyncio
from datetime import datetime, timezone
import json
from pathlib import Path
import sys

from hexbytes import HexBytes
from web3 import Web3

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from decimal_web3_sdk import DecimalClient, NetworkConfig
from decimal_web3_sdk.rpc import RpcPool


READ_METHODS = frozenset({"eth_chainId", "eth_getTransactionByHash", "eth_getTransactionReceipt", "eth_getCode"})


class FixtureProvider(Web3.HTTPProvider):
    def make_request(self, method, params):
        if method not in READ_METHODS:
            raise RuntimeError("Fixture collector only reads existing transactions")
        return super().make_request(method, params)

    def make_batch_request(self, requests):
        raise RuntimeError("Fixture collector forbids batch RPC")


class FixtureRpc(RpcPool):
    def _create_web3(self, url):
        return Web3(FixtureProvider(url, request_kwargs={"timeout": 5}, exception_retry_configuration=None))


def hex_string(value):
    return "0x" + bytes(HexBytes(value)).hex()


def snapshot(name, source, tx_hash, tx, receipt, code, code_error=None):
    if (
        hex_string(tx["hash"]).lower() != tx_hash.lower()
        or hex_string(receipt["transactionHash"]).lower() != tx_hash.lower()
        or int(tx["chainId"]) != 75 or int(receipt["status"]) != 1
        or int(tx["blockNumber"]) != int(receipt["blockNumber"])
        or hex_string(tx["blockHash"]) != hex_string(receipt["blockHash"])
    ):
        raise ValueError("Transaction identity, network or successful receipt did not match")
    return {
        "name": name, "source": source, "hash": tx_hash,
        "transaction": {
            "chainId": 75, "from": tx["from"], "to": tx["to"], "nonce": int(tx["nonce"]),
            "value": str(tx["value"]), "input": hex_string(tx["input"]),
            "gas": int(tx["gas"]), "gasPrice": str(tx["gasPrice"]), "type": int(tx["type"]),
            **{key: str(tx[key]) for key in ("maxFeePerGas", "maxPriorityFeePerGas") if tx.get(key) is not None},
        },
        "receipt": {
            "status": 1, "blockNumber": int(receipt["blockNumber"]),
            "blockHash": hex_string(receipt["blockHash"]), "transactionHash": tx_hash,
            "gasUsed": int(receipt["gasUsed"]),
            **({"effectiveGasPrice": str(receipt["effectiveGasPrice"])} if receipt.get("effectiveGasPrice") is not None else {}),
            "logs": [{"address": log["address"], "topics": [hex_string(t) for t in log["topics"]], "data": hex_string(log["data"])} for log in receipt["logs"]],
        },
        "recipient_code_at_receipt": (
            {"status": "read", "bytes": len(code), "keccak256": hex_string(Web3.keccak(code))}
            if code is not None else {"status": "unavailable", "error_type": code_error}
        ),
    }


async def collect(manifest, output):
    sources = json.loads(manifest.read_text(encoding="utf-8"))
    if sources["chain_id"] != 75:
        raise ValueError("This historical fixture collector only supports mainnet")
    config = NetworkConfig.mainnet()
    rows = []
    async with DecimalClient(config) as client:
        client.rpc = FixtureRpc(config.web3_urls, chain_id=75)
        for item in sources["cases"]:
            name, source, tx_hash = item["name"], item["source"], item["hash"]
            if len(HexBytes(tx_hash)) != 32:
                raise ValueError("Invalid transaction hash")
            tx = await client.rpc.call(lambda w3: w3.eth.get_transaction(tx_hash))
            receipt = await client.transaction_receipt(tx_hash)
            if receipt is None:
                raise ValueError("A required historical receipt is unavailable")
            code, code_error = None, None
            try:
                code = await client.rpc.call(lambda w3: bytes(w3.eth.get_code(tx["to"], receipt["blockNumber"])))
            except RuntimeError as exc:
                # Pruned historical state is not evidence of an empty contract.
                code_error = type(exc.__cause__ or exc).__name__
            row = snapshot(name, source, tx_hash, tx, receipt, code, code_error)
            if name != "sdk_del_memo" and code == b"":
                raise ValueError("Historical contract target has no code")
            rows.append(row)
            print(json.dumps({"name": name, "block": receipt["blockNumber"], "status": "collected_read_only"}), flush=True)
    output.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "schema_version": 1, "collected_at": datetime.now(timezone.utc).isoformat(),
        "chain_id": 75, "signed": False, "broadcast": False, "secrets_loaded": False,
        "note": "Public mined calldata, including an already-used permit; no private credentials or raw signed Ethereum transactions.",
        "cases": rows,
    }
    # Do not silently replace evidence used by existing regression tests.
    with output.open("x", encoding="utf-8") as handle:
        handle.write(json.dumps(payload, indent=2) + "\n")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    try:
        asyncio.run(collect(args.manifest, args.output))
    except Exception as exc:
        print(json.dumps({"status": "failed", "error_type": type(exc).__name__}))
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
