from __future__ import annotations

import argparse
import asyncio
import json
from datetime import datetime, timezone
from decimal import Decimal
from pathlib import Path
from typing import Any

from hexbytes import HexBytes
from web3 import Web3

from decimal_web3_sdk import DecimalClient, NetworkConfig, decode_memo_data
from decimal_web3_sdk.decimal import MULTICALL_ABI
from decimal_web3_sdk.token import TOKEN_CENTER_ABI


def _network(name: str) -> NetworkConfig:
    normalized = name.strip().lower()
    if normalized == "mainnet":
        return NetworkConfig.mainnet()
    if normalized == "devnet":
        return NetworkConfig.devnet()
    if normalized == "testnet":
        return NetworkConfig.testnet()
    raise ValueError("--network must be one of: testnet, devnet, mainnet")


async def collect_samples(tx_hashes: list[str], *, network: str, out_dir: Path) -> list[dict[str, Any]]:
    out_dir.mkdir(parents=True, exist_ok=True)
    config = _network(network)
    async with DecimalClient(config) as client:
        block_number = await client.block_number()
        samples = []
        for tx_hash in tx_hashes:
            sample = await _collect_one(client, tx_hash, block_number)
            samples.append(sample)
            output = out_dir / f"{sample['network']}_{sample['tx_hash'].removeprefix('0x')}.json"
            output.write_text(json.dumps(sample, ensure_ascii=False, indent=2), encoding="utf-8")
        manifest = {
            "created_at": datetime.now(timezone.utc).isoformat(),
            "network": config.name,
            "chain_id": config.chain_id,
            "sample_count": len(samples),
            "samples": [
                {
                    "tx_hash": item["tx_hash"],
                    "type": item["decoded"]["type"],
                    "status": item["receipt"].get("status") if item.get("receipt") else None,
                    "block_number": item["receipt"].get("blockNumber") if item.get("receipt") else None,
                    "file": f"{item['network']}_{item['tx_hash'].removeprefix('0x')}.json",
                }
                for item in samples
            ],
        }
        (out_dir / f"{config.name}_manifest.json").write_text(
            json.dumps(manifest, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
        return samples


async def _collect_one(client: DecimalClient, tx_hash: str, block_now: int) -> dict[str, Any]:
    normalized_hash = tx_hash if tx_hash.startswith("0x") else f"0x{tx_hash}"
    tx = await client.rpc.call(lambda w3: dict(w3.eth.get_transaction(normalized_hash)))
    receipt = await client.transaction_receipt(normalized_hash)
    decoded = _decode_transaction(client, tx)
    return {
        "created_at": datetime.now(timezone.utc).isoformat(),
        "network": client.config.name,
        "chain_id": client.config.chain_id,
        "block_now": block_now,
        "tx_hash": normalized_hash,
        "explorer_url": _explorer_url(client.config.name, normalized_hash),
        "transaction": _jsonable(tx),
        "receipt": _jsonable(receipt),
        "decoded": decoded,
    }


def _decode_transaction(client: DecimalClient, tx: dict[str, Any]) -> dict[str, Any]:
    to_address = _lower(tx.get("to"))
    multicall = _lower(client.config.contracts.multicall)
    token_center = _lower(client.config.contracts.token_center)
    value_wei = int(tx.get("value") or 0)
    input_data = _hex(tx.get("input") or tx.get("data") or "0x")

    if to_address == multicall:
        return _decode_multicall(client, tx, input_data, value_wei)
    if to_address == token_center:
        return _decode_token_center(client, tx, input_data, value_wei)

    memo = None
    if input_data and input_data != "0x":
        try:
            memo = decode_memo_data(input_data)
        except ValueError:
            memo = None
    if value_wei > 0:
        return {
            "type": "native_del_transfer",
            "from": tx.get("from"),
            "to": tx.get("to"),
            "amount_del": _wei_to_del(value_wei),
            "memo": memo,
        }
    return {
        "type": "unknown_contract_call" if input_data != "0x" else "unknown",
        "from": tx.get("from"),
        "to": tx.get("to"),
        "value_del": _wei_to_del(value_wei),
        "input_selector": input_data[:10] if input_data else None,
    }


def _decode_token_center(client: DecimalClient, tx: dict[str, Any], input_data: str, value_wei: int) -> dict[str, Any]:
    contract = client.web3.eth.contract(
        address=Web3.to_checksum_address(client.config.contracts.token_center),
        abi=TOKEN_CENTER_ABI,
    )
    try:
        function, args = contract.decode_function_input(input_data)
    except Exception as exc:
        return {
            "type": "token_center_unknown",
            "decode_error": str(exc),
            "input_selector": input_data[:10],
            "value_del": _wei_to_del(value_wei),
        }
    decoded: dict[str, Any] = {
        "type": f"token_center_{function.fn_name}",
        "function": function.fn_name,
        "from": tx.get("from"),
        "to": tx.get("to"),
        "value_del": _wei_to_del(value_wei),
        "args": _jsonable(args),
    }
    if function.fn_name == "createTokenReserveless":
        decoded["type"] = "create_reserveless_token"
        decoded["symbol"] = args.get("symbol")
        decoded["name"] = args.get("name")
        decoded["mintable"] = args.get("mintable")
        decoded["burnable"] = args.get("burnable")
        decoded["initial_mint_raw"] = args.get("initialMint")
        decoded["cap_raw"] = args.get("cap")
    elif function.fn_name == "createToken":
        decoded["type"] = "create_token"
        decoded["meta"] = _jsonable(args.get("meta"))
    elif function.fn_name == "convert":
        decoded["type"] = "token_convert"
    return decoded


def _decode_multicall(client: DecimalClient, tx: dict[str, Any], input_data: str, value_wei: int) -> dict[str, Any]:
    contract = client.web3.eth.contract(
        address=Web3.to_checksum_address(client.config.contracts.multicall),
        abi=MULTICALL_ABI,
    )
    try:
        function, args = contract.decode_function_input(input_data)
    except Exception as exc:
        return {
            "type": "multicall_unknown",
            "decode_error": str(exc),
            "input_selector": input_data[:10],
            "amount_del": _wei_to_del(value_wei),
        }
    calls = []
    memo = None
    for index, call in enumerate(args.get("calls", [])):
        if isinstance(call, dict):
            target = call["target"]
            call_value = call["value"]
            call_data = call["callData"]
        else:
            target, call_value, call_data = call
        call_data_hex = _hex(call_data)
        is_memo_call = _lower(target) == "0x0000000000000000000000000000000000000000" and int(call_value) == 0
        if is_memo_call:
            try:
                memo = bytes.fromhex(call_data_hex.removeprefix("0x")).decode("utf-8")
            except UnicodeDecodeError:
                memo = None
        calls.append(
            {
                "index": index,
                "target": target,
                "value_wei": int(call_value),
                "value_del": _wei_to_del(int(call_value)),
                "data": call_data_hex,
                "is_memo_call": is_memo_call,
            }
        )
    return {
        "type": "multisend_del",
        "function": function.fn_name,
        "from": tx.get("from"),
        "to": tx.get("to"),
        "amount_del": _wei_to_del(value_wei),
        "recipient_count": len([item for item in calls if not item["is_memo_call"]]),
        "memo": memo,
        "calls": calls,
    }


def _jsonable(value: Any) -> Any:
    if value is None:
        return None
    if isinstance(value, HexBytes):
        return value.hex()
    if isinstance(value, bytes):
        return "0x" + value.hex()
    if isinstance(value, Decimal):
        return str(value)
    if isinstance(value, dict):
        return {str(key): _jsonable(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [_jsonable(item) for item in value]
    return value


def _hex(value: Any) -> str:
    if isinstance(value, HexBytes):
        return value.hex()
    if isinstance(value, bytes):
        return "0x" + value.hex()
    return str(value)


def _lower(value: Any) -> str:
    return str(value or "").lower()


def _wei_to_del(value_wei: int) -> str:
    return str(Decimal(int(value_wei)) / Decimal(10**18))


def _explorer_url(network: str, tx_hash: str) -> str:
    base = "https://testnet-explorer.decimalchain.com/transactions"
    if "mainnet" in network:
        base = "https://explorer.decimalchain.com/transactions"
    return f"{base}/{tx_hash}"


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Collect read-only tx-reader samples from Decimal RPC.")
    parser.add_argument("--network", default="testnet", choices=["testnet", "devnet", "mainnet"])
    parser.add_argument("--out", default="reports/tx_reader_samples")
    parser.add_argument("tx_hash", nargs="+")
    return parser


def main() -> None:
    args = _build_parser().parse_args()
    samples = asyncio.run(collect_samples(args.tx_hash, network=args.network, out_dir=Path(args.out)))
    print(json.dumps([{"tx_hash": item["tx_hash"], "decoded": item["decoded"]} for item in samples], ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
