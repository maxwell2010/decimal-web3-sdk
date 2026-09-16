"""Opt-in wallet checks and unsigned fee estimates. Cannot broadcast transactions."""

from __future__ import annotations

import argparse
import asyncio
from dataclasses import replace
from datetime import datetime, timezone
import json
from pathlib import Path
import sys

from dotenv import dotenv_values
from web3 import Web3

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from decimal_web3_sdk import (
    BuyExactTokenRequest,
    CreateMultisigRequest,
    CreateReservelessNftCollectionRequest,
    DecimalClient,
    DelegateDelRequest,
    Erc20ApproveRequest,
    Erc20TransferRequest,
    MultisendDelRequest,
    MultisendRecipient,
    NativeTransferRequest,
    NetworkConfig,
    SellForExactDelRequest,
    UnbondErc20Request,
    WeightedOwner,
)
from decimal_web3_sdk.erc20 import format_units_string
from decimal_web3_sdk.rpc import RpcPool
from decimal_web3_sdk.wallet import DEFAULT_DERIVATION_PATH, checksum, mnemonic_to_account


READ_METHODS = frozenset({
    "eth_chainId", "eth_blockNumber", "eth_getBlockByNumber", "eth_getBalance",
    "eth_getTransactionCount", "eth_getCode", "eth_gasPrice", "eth_estimateGas",
    "eth_call", "net_version", "web3_clientVersion",
})


class ReadOnlyProvider(Web3.HTTPProvider):
    def make_request(self, method, params):
        if method not in READ_METHODS:
            raise RuntimeError("Wallet audit forbids this RPC method")
        return super().make_request(method, params)

    def make_batch_request(self, requests):
        raise RuntimeError("Wallet audit does not allow batch RPC requests")


class AuditRpc(RpcPool):
    def _create_web3(self, url):
        kwargs = {"timeout": self._timeout}
        if self._ca_file:
            kwargs["verify"] = self._ca_file
        # Diagnostic runs use one bounded attempt per endpoint, not hidden HTTP retries.
        return Web3(ReadOnlyProvider(
            url, request_kwargs=kwargs, exception_retry_configuration=None,
        ))


def wallet_config(values, network):
    prefix = "DECIMAL_" + network.upper()
    mnemonic = values.get(prefix + "_TEST_MNEMONIC")
    expected = values.get(prefix + "_TEST_EXPECTED_ADDRESS")
    if not mnemonic or not expected:
        raise ValueError("Dedicated test mnemonic and expected address are required")
    try:
        account = mnemonic_to_account(
            mnemonic,
            passphrase=values.get(prefix + "_TEST_MNEMONIC_PASSPHRASE") or "",
            account_path=values.get(prefix + "_TEST_DERIVATION_PATH") or DEFAULT_DERIVATION_PATH,
        )
        valid = account.address == checksum(expected)
    except Exception:
        raise ValueError("Invalid dedicated test wallet configuration") from None
    if not valid:
        raise ValueError("Dedicated test wallet address mismatch")
    config = NetworkConfig.testnet() if network == "testnet" else NetworkConfig.mainnet()
    config_prefix = "DECIMAL_TESTNET" if network == "testnet" else "DECIMAL"
    urls = values.get(config_prefix + "_WEB3_URLS")
    ca = values.get(config_prefix + "_TLS_CA_FILE") or values.get("DECIMAL_TLS_CA_FILE")
    return account, replace(
        config,
        chain_id=202020 if network == "testnet" else 75,
        web3_urls=[url.strip() for url in urls.split(",") if url.strip()] if urls else config.web3_urls,
        tls_ca_file=ca or config.tls_ca_file,
    )


def failure(exc):
    # Exception text can contain private RPC URLs or request data. Never log it.
    return {
        "status": "blocked",
        "error_type": type(exc).__name__,
        "cause_type": type(exc.__cause__).__name__ if exc.__cause__ else None,
        "http_status": getattr(exc, "status", None),
    }


def fee_record(fee):
    return {
        "status": "estimated_unsigned",
        "balance_sufficient": fee.ok,
        "estimated_gas": fee.estimated_gas,
        "gas_limit": fee.gas_limit,
        "gas_price_gwei": format_units_string(fee.gas_price_wei, 9),
        "estimated_fee_del": format_units_string(fee.estimated_fee_wei, 18),
        "gas_limit_fee_del": format_units_string(fee.gas_limit_fee_wei, 18),
        "value_del": format_units_string(fee.value_wei, 18),
        "actual_fee_del": None,
    }


async def audit(args):
    values = dotenv_values(args.env_file, interpolate=False)
    account, config = wallet_config(values, args.network)
    client = DecimalClient(config)
    client.rpc = AuditRpc(config.web3_urls, timeout=5, chain_id=config.chain_id, ca_file=config.tls_ca_file)
    report = {
        "network": args.network, "chain_id": config.chain_id, "account": account.address,
        "checked_at": datetime.now(timezone.utc).isoformat(),
        "signed": False, "broadcast": False, "spent_del": "0", "checks": {},
    }
    checks = report["checks"]

    async def estimate(name, fn):
        try:
            checks[name] = fee_record(await fn())
        except Exception as exc:
            checks[name] = failure(exc)
        print(json.dumps({"check": name, **checks[name]}), flush=True)

    try:
        block = await client.block_number()
        balance = await client.rpc.call(lambda w3: w3.eth.get_balance(account.address, block))
        report.update(block=block, balance_before_del=format_units_string(balance, 18))
        print(json.dumps({key: value for key, value in report.items() if key != "checks"}), flush=True)
        for memo in (None, "Python SDK unsigned memo check"):
            request = NativeTransferRequest(
                to=account.address, amount_del="0.000001", private_key=account.private_key, memo=memo,
            )
            await estimate("send_del_memo" if memo else "send_del", lambda: client.tx.estimate_fee_for_native_transfer(request))
        request = MultisendDelRequest(
            recipients=[MultisendRecipient(account.address, "0.000001") for _ in range(2)],
            private_key=account.private_key, memo="Python SDK unsigned multisend check",
        )
        await estimate("multisend_del_2_self", lambda: client.decimal.estimate_fee_for_multisend_del(request))

        request = CreateMultisigRequest(
            private_key=account.private_key, owners=(WeightedOwner(account.address, 1),),
            weight_threshold=1, salt_nonce=block,
        )
        await estimate("create_safe", lambda: client.multisig.estimate_fee_for_operation(request))
        for kind in ("erc721", "erc1155"):
            request = CreateReservelessNftCollectionRequest(
                private_key=account.private_key, kind=kind, creator=account.address,
                symbol="SDKTEST" + str(block), name="SDK unsigned estimate",
                contract_uri="https://example.invalid/sdk-test.json",
            )
            await estimate("create_reserveless_" + kind, lambda: client.nft.estimate_fee_for_operation(request))

        if args.validator:
            request = DelegateDelRequest(validator=args.validator, amount_del="0.000001", private_key=account.private_key)
            await estimate("delegate_del", lambda: client.decimal.estimate_fee_for_delegate_del(request))
        if args.token:
            info = await client.erc20.info(args.token)
            token_balance = await client.erc20.balance(args.token, account.address)
            checks["token_balance"] = {"symbol": info.symbol, "decimals": info.decimals, "raw": str(token_balance.raw)}
            request = BuyExactTokenRequest(
                private_key=account.private_key, token=args.token, recipient=account.address,
                amount_out_raw=1, max_amount_del="0.000001",
            )
            await estimate("buy_exact_token", lambda: client.token.estimate_fee_for_operation(request))
            request = SellForExactDelRequest(
                private_key=account.private_key, token=args.token, recipient=account.address,
                max_amount_in_raw=10**info.decimals, amount_out_del="0.000001",
            )
            await estimate("sell_for_exact_del", lambda: client.token.estimate_fee_for_operation(request))
            request = Erc20TransferRequest(
                token=args.token, to=account.address, amount="0.000001", decimals=info.decimals, private_key=account.private_key,
            )
            await estimate("erc20_transfer", lambda: client.tx.estimate_fee_for_erc20_transfer(request))
            request = Erc20ApproveRequest(
                token=args.token, spender=config.contracts.multicall, amount="0.000001", decimals=info.decimals, private_key=account.private_key,
            )
            await estimate("erc20_approve_multicall", lambda: client.tx.estimate_fee_for_erc20_approve(request))
            if args.validator:
                stake = await client.decimal.get_stake(args.validator, account.address, args.token, block_identifier=block)
                checks["regular_stake"] = {"amount_raw": str(stake.amount_raw), "block": block, "hold_discovery_complete": False}
                request = UnbondErc20Request(
                    token=args.token, validator=args.validator, amount="0.000001", decimals=info.decimals, private_key=account.private_key,
                )
                await estimate("unbond_erc20", lambda: client.decimal.estimate_fee_for_unbond_erc20(request))
        report["balance_after_del"] = format_units_string(await client.balance_wei(account.address), 18)
    except Exception as exc:
        report["error"] = failure(exc)
    finally:
        await client.close()
    return report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--network", choices=("mainnet", "testnet"), required=True)
    parser.add_argument("--env-file", type=Path, required=True)
    parser.add_argument("--token")
    parser.add_argument("--validator")
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    try:
        report = asyncio.run(audit(args))
    except Exception as exc:
        report = {"network": args.network, "signed": False, "broadcast": False, "error": failure(exc)}
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2))
    if "error" in report:
        return 1
    return 2 if any(row.get("status") == "blocked" for row in report["checks"].values()) else 0


if __name__ == "__main__":
    raise SystemExit(main())
