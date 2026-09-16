"""Explicitly authorized, budget-limited self-transfer checks. No approve or staking."""

from __future__ import annotations

import argparse
import asyncio
from datetime import datetime, timezone
import json
from pathlib import Path
import sys

from dotenv import dotenv_values
from hexbytes import HexBytes
from web3 import Web3

sys.path.insert(0, str(Path(__file__).resolve().parent))
from check_wallet_preflight import failure, fee_record, wallet_config
from decimal_web3_sdk import (
    DecimalClient, Erc20TransferRequest, MultisendDelRequest, MultisendRecipient,
    NativeTransferRequest,
)
from decimal_web3_sdk.erc20 import format_units_string, parse_units
from decimal_web3_sdk.wallet import checksum


def check_signing_budget(draft, planned, consumed_wei, limit_wei):
    for field in ("chainId", "nonce", "value"):
        if draft.tx[field] != planned[field]:
            raise ValueError("Transaction differs from the approved plan")
    for field in ("from", "to"):
        if checksum(draft.tx[field]) != checksum(planned[field]):
            raise ValueError("Transaction address differs from the approved plan")
    if HexBytes(draft.tx["data"]) != HexBytes(planned["data"]):
        raise ValueError("Transaction calldata differs from the approved plan")
    gas = int(draft.tx["gas"])
    price = int(draft.tx["gasPrice"])
    if gas <= 0 or price <= 0:
        raise ValueError("Invalid transaction fee")
    reserved = gas * price + int(draft.tx["value"])
    if consumed_wei + reserved > limit_wei:
        raise ValueError("Approved test budget would be exceeded")
    return reserved


def save(path, report):
    temporary = path.with_suffix(".tmp")
    temporary.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    temporary.replace(path)


def receipt_fee(receipt, tx):
    price = receipt.get("effectiveGasPrice")
    if price is None:
        if int(tx["type"]) not in (0, 1):
            raise ValueError("Dynamic-fee receipt has no effective gas price")
        price = tx["gasPrice"]
    gas_used, price = int(receipt["gasUsed"]), int(price)
    if not 0 < gas_used <= int(tx["gas"]) or price <= 0:
        raise ValueError("Invalid confirmed transaction fee")
    return gas_used * price, price


def payload_matches(tx, planned):
    return (
        checksum(tx["from"]) == checksum(planned["from"])
        and checksum(tx["to"]) == checksum(planned["to"])
        and int(tx["value"]) == int(planned["value"])
        and HexBytes(tx["input"]) == HexBytes(planned["data"])
        and int(tx["nonce"]) == int(planned["nonce"])
        and (tx.get("chainId") is None or int(tx["chainId"]) == int(planned["chainId"]))
    )


def validate_resume(report, network, chain_id, address, limit, token):
    if (
        report["network"] != network or report["chain_id"] != chain_id
        or checksum(report["address"]) != checksum(address)
        or parse_units(report["limit_del"], 18) != limit
        or (report.get("token") is not None and checksum(report["token"]) != token)
    ):
        raise ValueError("Resume journal does not match the approved test block")


async def reconcile(client, report, cases):
    spent, consumed = 0, 0
    names = [case[0] for case in cases]
    rows = report["cases"]
    if [row["name"] for row in rows] != names[:len(rows)]:
        raise ValueError("Resume journal has unexpected or duplicate cases")
    for row, (_, build, _) in zip(rows, cases):
        confirmed = []
        for attempt in row["signed_attempts"]:
            receipt = await client.transaction_receipt(attempt["tx_hash"])
            if receipt is not None:
                confirmed.append((attempt, receipt))
        if len(confirmed) != 1 or int(confirmed[0][1]["status"]) != 1:
            raise ValueError("Unresolved or reverted transaction; resume will not resend it")
        attempt, receipt = confirmed[0]
        tx = await client.rpc.call(lambda w3: w3.eth.get_transaction(attempt["tx_hash"]))
        planned = dict((await build()).tx)
        planned["nonce"] = row["nonce"]
        if not payload_matches(tx, planned):
            raise ValueError("Confirmed transaction differs from the approved plan")
        if int(tx["gasPrice"]) != int(attempt["gas_price_wei"]) or int(tx["gas"]) != attempt["gas_limit"]:
            raise ValueError("Confirmed transaction differs from the signed fee record")
        if row["name"] == "erc20_self_transfer" and row.get("token_self_transfer_verified") is not True:
            raise ValueError("Token receipt requires manual event verification before resume")
        actual, price = receipt_fee(receipt, tx)
        spent += actual
        consumed += actual + int(tx["value"])
        row.update(
            status="confirmed", tx_hash=attempt["tx_hash"], block=int(receipt["blockNumber"]),
            gas_used=int(receipt["gasUsed"]), effective_gas_price_wei=str(price),
            actual_fee_del=format_units_string(actual, 18), onchain_payload_matches=True,
            reconciled_from_chain=True,
        )
    report["spent_fee_wei"], report["budget_consumed_wei"] = str(spent), str(consumed)
    return consumed


async def run(args):
    if not args.broadcast:
        raise ValueError("Use check_wallet_preflight.py for unsigned estimates")
    limit = parse_units(args.limit_del, 18)
    if not 0 < limit <= parse_units("0.25", 18):
        raise ValueError("This test block is limited to at most 0.25 DEL")
    values = dotenv_values(args.env_file, interpolate=False)
    account, config = wallet_config(values, args.network)
    if account.address != checksum(args.expected_address):
        raise ValueError("CLI expected address does not match the dedicated test wallet")
    token = checksum(args.token)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    report = {
        "network": args.network, "chain_id": config.chain_id, "address": account.address,
        "started_at": datetime.now(timezone.utc).isoformat(),
        "limit_del": format_units_string(limit, 18), "spent_fee_wei": "0", "token": token,
        "budget_consumed_wei": "0", "cases": [], "status": "running",
    }
    if args.resume:
        report = json.loads(args.output.read_text(encoding="utf-8"))
        validate_resume(report, args.network, config.chain_id, account.address, limit, token)
        backup = args.output.with_suffix(".before-resume-" + datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%f") + ".json")
        with backup.open("x", encoding="utf-8") as fh:
            fh.write(json.dumps(report, indent=2) + "\n")
    else:
        # Refuse to overwrite an earlier run: it might contain a pending transaction.
        with args.output.open("x", encoding="utf-8") as fh:
            fh.write(json.dumps(report, indent=2) + "\n")
    client = DecimalClient(config)
    consumed = 0
    try:
        block = await client.block_number()
        report.setdefault("start_block", block)
        report.setdefault("balance_before_del", format_units_string(await client.balance_wei(account.address), 18))
        info = await client.erc20.info(token)
        token_amount = parse_units("0.000001", info.decimals)
        if (await client.erc20.balance(token, account.address)).raw < token_amount:
            raise ValueError("Insufficient tokens for the self-transfer test")

        cases = []
        for name, memo in (("send_del", None), ("send_del_memo", "Python SDK single DEL memo test")):
            request = NativeTransferRequest(to=account.address, amount_del="0.000001", private_key=account.private_key, memo=memo)
            cases.append((name, lambda r=request: client.tx.build_native_transfer(r), lambda r=request: client.tx.send_del(r, broadcast=True, wait_receipt=True)))
        request = MultisendDelRequest(
            recipients=[MultisendRecipient(account.address, "0.000001") for _ in range(2)],
            private_key=account.private_key, memo="Python SDK self multisend test",
        )
        cases.append(("multisend_del_2_self", lambda r=request: client.decimal.build_multisend_del(r), lambda r=request: client.decimal.multisend_del(r, broadcast=True, wait_receipt=True)))
        request = Erc20TransferRequest(token=token, to=account.address, amount="0.000001", decimals=info.decimals, private_key=account.private_key)
        cases.append(("erc20_self_transfer", lambda r=request: client.tx.build_erc20_transfer(r), lambda r=request: client.tx.send_erc20(r, broadcast=True, wait_receipt=True)))

        if args.resume:
            consumed = await reconcile(client, report, cases)
            if consumed > limit:
                raise ValueError("Approved test budget was already exceeded")
            report["resumed_at"] = datetime.now(timezone.utc).isoformat()
            report["balance_on_resume_del"] = format_units_string(await client.balance_wei(account.address), 18)
            if "error" in report:
                report.setdefault("recovered_errors", []).append(report.pop("error"))
            report["status"] = "running"
            report["token"] = token
            save(args.output, report)
            print(json.dumps({"phase": "reconciled", "confirmed_cases": len(report["cases"]), "spent_fee_del": format_units_string(int(report["spent_fee_wei"]), 18)}), flush=True)

        for name, build, send in cases[len(report["cases"]):]:
            before = await client.balance_wei(account.address)
            latest_nonce = await client.rpc.call(lambda w3: w3.eth.get_transaction_count(account.address, "latest"))
            if latest_nonce != await client.transaction_count(account.address):
                raise ValueError("Wallet already has a pending transaction; stop instead of replacing it")
            draft = await build()
            planned = dict(draft.tx)
            if planned["nonce"] != latest_nonce:
                raise ValueError("Wallet nonce changed during preparation")
            fee = await client.tx.calculate_fee(draft)
            check_signing_budget(draft, planned, consumed, limit)
            if not fee.ok:
                raise ValueError("Insufficient native balance for the complete transaction")
            token_before = (await client.erc20.balance(token, account.address)).raw if name == "erc20_self_transfer" else None
            row = {
                "name": name, "nonce": latest_nonce, "status": "preflight",
                "balance_before_del": format_units_string(before, 18),
                "preflight": fee_record(fee), "signed_attempts": [],
            }
            if token_before is not None:
                row["token_balance_before_raw"] = str(token_before)
            report["cases"].append(row)
            save(args.output, report)
            print(json.dumps({"name": name, "phase": "before_signing", **row["preflight"]}), flush=True)
            if args.step:
                confirmation = await asyncio.to_thread(input, "Continue with SEND " + name + ": ")
                if confirmation.strip() != "SEND " + name:
                    raise ValueError("Step was not confirmed; no signature for this case")
            original_sign = client.tx.sign
            original_send = client.send_raw_transaction

            async def guarded_sign(candidate, key):
                reserved = check_signing_budget(candidate, planned, consumed, limit)
                signed = await original_sign(candidate, key)
                tx_hash = "0x" + bytes(Web3.keccak(signed.raw_tx)).hex()
                row["signed_attempts"].append({
                    "tx_hash": tx_hash, "gas_limit": int(candidate.tx["gas"]),
                    "gas_price_wei": str(candidate.tx["gasPrice"]), "reserved_wei": str(reserved),
                })
                row["status"] = "signed_not_yet_broadcast"
                save(args.output, report)
                return signed

            async def guarded_send(raw):
                tx_hash = "0x" + bytes(Web3.keccak(raw)).hex()
                if not any(item["tx_hash"] == tx_hash for item in row["signed_attempts"]):
                    raise ValueError("Broadcast hash was not approved by the signing guard")
                row["status"] = "broadcast_attempted"
                save(args.output, report)
                return await original_send(raw)

            client.tx.sign = guarded_sign
            client.send_raw_transaction = guarded_send
            try:
                result = await send()
                row["sdk_status"] = result.status
            finally:
                client.tx.sign = original_sign
                client.send_raw_transaction = original_send

            receipt = None
            deadline = asyncio.get_running_loop().time() + 60
            while row["signed_attempts"] and asyncio.get_running_loop().time() < deadline:
                for attempt in reversed(row["signed_attempts"]):
                    receipt = await client.transaction_receipt(attempt["tx_hash"])
                    if receipt is not None:
                        row["tx_hash"] = attempt["tx_hash"]
                        break
                if receipt is not None:
                    break
                await asyncio.sleep(3)
            if receipt is None:
                row["status"] = "unresolved_no_automatic_resend"
                report["status"] = "stopped_pending_review"
                save(args.output, report)
                return report

            tx = await client.rpc.call(lambda w3: w3.eth.get_transaction(row["tx_hash"]))
            actual, price = receipt_fee(receipt, tx)
            consumed += actual + int(planned["value"])
            report["spent_fee_wei"] = str(int(report["spent_fee_wei"]) + actual)
            report["budget_consumed_wei"] = str(consumed)
            row.update(
                status="confirmed" if int(receipt["status"]) == 1 else "reverted",
                block=int(receipt["blockNumber"]), gas_used=int(receipt["gasUsed"]),
                effective_gas_price_wei=str(price), actual_fee_del=format_units_string(actual, 18),
            )
            save(args.output, report)
            row["balance_after_del"] = format_units_string(await client.balance_wei(account.address), 18)
            row["onchain_payload_matches"] = payload_matches(tx, planned)
            if name == "erc20_self_transfer":
                token_after = (await client.erc20.balance(token, account.address)).raw
                row["token_balance_before_raw"] = str(token_before)
                row["token_balance_after_raw"] = str(token_after)
                transfer_topic = bytes(Web3.keccak(text="Transfer(address,address,uint256)"))
                expected_topic = bytes.fromhex(account.address[2:].lower()).rjust(32, b"\0")
                row["matching_transfer_logs"] = sum(
                    1 for log in receipt["logs"]
                    if checksum(log["address"]) == token and len(log["topics"]) == 3
                    and bytes(log["topics"][0]) == transfer_topic
                    and bytes(log["topics"][1]) == expected_topic
                    and bytes(log["topics"][2]) == expected_topic
                    and int.from_bytes(HexBytes(log["data"]), "big") == token_amount
                )
                row["token_self_transfer_verified"] = token_before == token_after and row["matching_transfer_logs"] == 1
            save(args.output, report)
            print(json.dumps({key: value for key, value in row.items() if key != "signed_attempts"}), flush=True)
            if row["status"] != "confirmed" or not row["onchain_payload_matches"] or row.get("token_self_transfer_verified") is False:
                raise ValueError("Receipt or post-transaction verification failed; stopping")
        report["status"] = "completed"
    except Exception as exc:
        report["status"] = "stopped"
        report["error"] = failure(exc)
    finally:
        report["finished_at"] = datetime.now(timezone.utc).isoformat()
        save(args.output, report)
        await client.close()
    return report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--network", required=True, choices=("mainnet", "testnet"))
    parser.add_argument("--env-file", required=True, type=Path)
    parser.add_argument("--expected-address", required=True)
    parser.add_argument("--token", required=True)
    parser.add_argument("--limit-del", required=True)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--broadcast", action="store_true")
    parser.add_argument("--step", action="store_true", help="Pause after each unsigned estimate")
    parser.add_argument("--resume", action="store_true", help="Reconcile every prior hash before continuing; never resend an unresolved case")
    args = parser.parse_args()
    try:
        report = asyncio.run(run(args))
    except Exception as exc:
        print(json.dumps({"status": "not_started", "error": failure(exc)}))
        return 1
    print(json.dumps({key: value for key, value in report.items() if key != "cases"}))
    return 0 if report["status"] == "completed" else 1


if __name__ == "__main__":
    raise SystemExit(main())
