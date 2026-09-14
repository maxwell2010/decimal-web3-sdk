"""Read-only deployment check against official Decimal RPCs; never uses a signer."""
import argparse
import asyncio
import dataclasses
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from decimal_web3_sdk import DecimalClient, NetworkConfig
from decimal_web3_sdk.config import DEFAULT_MAINNET_WEB3_URLS, DEFAULT_TESTNET_WEB3_URLS, DEFAULT_DEVNET_WEB3_URLS


async def check(network):
    urls = {"mainnet": DEFAULT_MAINNET_WEB3_URLS, "testnet": DEFAULT_TESTNET_WEB3_URLS, "devnet": DEFAULT_DEVNET_WEB3_URLS}[network]
    config = dataclasses.replace(getattr(NetworkConfig, network)(), web3_urls=list(urls))
    report = {"network": network, "checked_at": datetime.now(timezone.utc).isoformat(),
              "rpc_source": "official Decimal defaults", "broadcast": False}
    client = DecimalClient(config)
    try:
        if not await client.connect():
            report["status"] = "unavailable_or_chain_mismatch"
            return report
        report["block"] = await client.block_number()
        report["chain_id"] = config.chain_id
        report["gas_price_wei"] = str(await client.gas_price())
        contracts = {}
        for name, address in dataclasses.asdict(config.contracts).items():
            if len(address) != 42:
                contracts[name] = {"status": "not_configured"}
                continue
            code = await client.contract_code(address)
            contracts[name] = {"address": address, "code_present": bool(code), "code_bytes": len(code)}
        report["contracts"] = contracts
        report["status"] = "read_only_ok"
        return report
    except Exception:
        report["status"] = "rpc_failed"
        return report
    finally:
        await client.close()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--network", choices=("mainnet", "testnet", "devnet"), default="testnet")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = asyncio.run(check(args.network))
    content = json.dumps(result, indent=2) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(content, encoding="utf-8")
    print(content)
    raise SystemExit(0 if result["status"] == "read_only_ok" else 1)


if __name__ == "__main__":
    main()
