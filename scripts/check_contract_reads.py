"""Read-only checks on official RPCs. No credentials, signing or broadcasting."""

import asyncio
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from decimal_web3_sdk import DecimalClient, NetworkConfig, SystemContracts
from decimal_web3_sdk.config import (
    DEFAULT_MAINNET_WEB3_URLS,
    DEFAULT_TESTNET_WEB3_URLS,
    TESTNET_SYSTEM_CONTRACTS,
)
from decimal_web3_sdk.wallet import checksum


async def check(name, chain_id, urls, contracts):
    config = NetworkConfig.custom(name=name, chain_id=chain_id, web3_urls=urls, contracts=contracts)
    result = {"network": name, "chain_id": chain_id, "broadcast": False, "checks": {}}
    async with DecimalClient(config) as client:
        if not await client.connect():
            result["error"] = "Official RPC unavailable or chain ID mismatch"
            return result
        result["block"] = await client.block_number()
        for name in ("delegation_nft", "master_validator", "gas_center", "safe", "safe_factory"):
            target = checksum(getattr(contracts, name))
            code = await client.rpc.call(lambda w3, target=target: w3.eth.get_code(target))
            result["checks"][name + "_has_code"] = bool(code)
        try:
            result["checks"]["nft_withdraw_freeze_seconds"] = str(
                await client.nft.get_freeze_time(1)
            )
            result["checks"]["nft_transfer_freeze_seconds"] = str(
                await client.nft.get_freeze_time(2)
            )
            unused = "0x" + "11" * 20
            stake = await client.nft.get_stake(unused, unused, unused, 0)
            result["checks"]["unused_nft_stake_amount_raw"] = str(stake.amount_raw)
        except Exception as exc:
            result["error"] = str(exc)
    return result


async def main():
    for args in (
        ("mainnet", 75, DEFAULT_MAINNET_WEB3_URLS, SystemContracts()),
        ("testnet", 202020, DEFAULT_TESTNET_WEB3_URLS, TESTNET_SYSTEM_CONTRACTS),
    ):
        print(json.dumps(await check(*args), ensure_ascii=True), flush=True)


if __name__ == "__main__":
    asyncio.run(main())
