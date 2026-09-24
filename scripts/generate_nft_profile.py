"""Synchronize the unsigned profile with reviewed, bundled NFT ABI snapshots."""
import argparse
import json
from pathlib import Path

from eth_utils.abi import abi_to_signature

ROOT = Path(__file__).resolve().parents[1]
PROFILE = ROOT / "src/decimal_web3_sdk/profiles/candy_mainnet_v1.json"


def generated_profile():
    profile = json.loads(PROFILE.read_text(encoding="utf-8"))
    snapshots = {
        name: json.loads((ROOT / "src/decimal_web3_sdk/abi" / f"{name}.json").read_text(encoding="utf-8"))
        for name in ("nft_center", "nft_721", "nft_1155")
    }
    profile["reviewed"] = "2026-09-16"
    profile["abi"]["nftCenter"] = snapshots["nft_center"]["abi"]
    entries = {}
    for name in ("nft_721", "nft_1155"):
        for entry in snapshots[name]["abi"]:
            entries.setdefault((entry["type"], abi_to_signature(entry)), entry)
    profile["abi"]["nft"] = list(entries.values())
    profile["nftProtocol"] = {
        "reviewed": "2026-09-16", "reserveTypes": {"none": 0, "del": 1, "erc20": 2},
        "minimumReserveRaw": "1000000000000000",
        "creationMintsNfts": False, "erc1155MintReserveIsTotal": True,
        "implementations": {name: snapshots[name]["implementation"] for name in snapshots},
        "sources": {name: snapshots[name]["source"] for name in snapshots},
    }
    return json.dumps(profile, indent=2) + "\n"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    content = generated_profile()
    if args.check:
        if PROFILE.read_text(encoding="utf-8") != content:
            raise SystemExit("NFT profile differs from bundled ABI snapshots")
    else:
        PROFILE.write_text(content, encoding="utf-8")
    print("NFT profile: reviewed ABI snapshots synchronized")


if __name__ == "__main__":
    main()
