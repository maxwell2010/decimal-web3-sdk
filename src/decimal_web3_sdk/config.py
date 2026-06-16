from __future__ import annotations

import os
from dataclasses import dataclass, field

from .limits import SafetyLimits


def _csv_env(name: str, fallback: list[str]) -> list[str]:
    raw = os.getenv(name)
    if not raw:
        return fallback
    return [item.strip() for item in raw.split(",") if item.strip()]


def _env(name: str, fallback: str = "") -> str:
    return os.getenv(name, fallback).strip()


@dataclass(frozen=True)
class SystemContracts:
    contract_center: str = "0xc108715a06f76caa96fa2c943ebf05159c29a87d"
    delegation: str = "0xa16c34ed1c0601c0e749e17ebef19752a15faa01"
    delegation_nft: str = "0x5a6533e337f4b7f815aefb0609200acfbe1ba231"
    master_validator: str = "0x630B03FF9EeD4C4A468dA9f481DF23F542070Aa4"
    nft_center: str = "0x9113ba675aa8f2ef0c068cee2cdabab95b6437fb"
    token_center: str = "0x9113ba675aa8f2ef0c068cee2cdabab95b6437fb"
    wdel: str = "0x1c5d8992da64c8d56ea413dd6f723061c29a7c0b"
    multicall: str = "0x7b23eb47587ca6482fc16cb3d9d426ec64d4b5fc"
    del_token: str = "0x16049a46126d69211de7c042465122badefa360c"


OFFICIAL_MAINNET_WEB3_URLS = ["https://node.decimalchain.com/web3/"]
OFFICIAL_TESTNET_WEB3_URLS = [
    "https://testnet-val.decimalchain.com/web3/",
    "https://202020.rpc.thirdweb.com",
]
OFFICIAL_DEVNET_WEB3_URLS = ["https://devnet-val.decimalchain.com/web3/"]

OFFICIAL_MAINNET_REST_URLS = ["http://node.decimalchain.com/rest/"]
OFFICIAL_TESTNET_REST_URLS = ["http://testnet-val.decimalchain.com/rest/"]
OFFICIAL_DEVNET_REST_URLS = ["http://devnet-val.decimalchain.com/rest/"]

OFFICIAL_MAINNET_API_ROOT = "https://mainnet-api.decimalchain.com/api/"
OFFICIAL_TESTNET_API_ROOT = "https://testnet-api.decimalchain.com/api/"
OFFICIAL_DEVNET_API_ROOT = "https://devnet-api.decimalchain.com/api/"
OFFICIAL_MAINNET_GATE_API_ROOT = "https://mainnet-gate.decimalchain.com/api/"
OFFICIAL_TESTNET_GATE_API_ROOT = "https://testnet-gate.decimalchain.com/api/"
OFFICIAL_DEVNET_GATE_API_ROOT = "https://devnet-gate.decimalchain.com/api/"


@dataclass(frozen=True)
class NetworkConfig:
    chain_id: int = 75
    web3_urls: list[str] = field(default_factory=list)
    rest_urls: list[str] = field(default_factory=list)
    ws_urls: list[str] = field(default_factory=list)
    api_root_url: str = ""
    api_base_url: str = ""
    api_fallback_base_urls: list[str] = field(default_factory=list)
    api_key: str | None = None
    name: str = "decimal-mainnet"
    contracts: SystemContracts = field(default_factory=SystemContracts)
    safety: SafetyLimits = field(default_factory=SafetyLimits)

    @classmethod
    def mainnet(cls) -> "NetworkConfig":
        return cls(
            web3_urls=_csv_env(
                "DECIMAL_WEB3_URLS",
                OFFICIAL_MAINNET_WEB3_URLS,
            ),
            rest_urls=_csv_env("DECIMAL_REST_URLS", OFFICIAL_MAINNET_REST_URLS),
            ws_urls=_csv_env("DECIMAL_WS_URLS", []),
            api_base_url=_env("DECIMAL_API_BASE", OFFICIAL_MAINNET_API_ROOT),
            api_root_url=_env("DECIMAL_API_ROOT", OFFICIAL_MAINNET_GATE_API_ROOT),
            api_fallback_base_urls=_csv_env("DECIMAL_API_FALLBACK_BASES", []),
            api_key=os.getenv("DECIMAL_API_KEY"),
            name=_env("DECIMAL_NETWORK_NAME", "decimal-mainnet"),
        )

    @classmethod
    def testnet(cls) -> "NetworkConfig":
        return cls(
            chain_id=int(_env("DECIMAL_TESTNET_CHAIN_ID", "202020")),
            web3_urls=_csv_env("DECIMAL_TESTNET_WEB3_URLS", OFFICIAL_TESTNET_WEB3_URLS),
            rest_urls=_csv_env("DECIMAL_TESTNET_REST_URLS", OFFICIAL_TESTNET_REST_URLS),
            ws_urls=_csv_env("DECIMAL_TESTNET_WS_URLS", []),
            api_base_url=_env("DECIMAL_TESTNET_API_BASE", OFFICIAL_TESTNET_API_ROOT),
            api_root_url=_env("DECIMAL_TESTNET_API_ROOT", OFFICIAL_TESTNET_GATE_API_ROOT),
            api_fallback_base_urls=_csv_env(
                "DECIMAL_TESTNET_API_FALLBACK_BASES",
                [],
            ),
            api_key=os.getenv("DECIMAL_TESTNET_API_KEY"),
            name=_env("DECIMAL_TESTNET_NETWORK_NAME", "decimal-testnet"),
        )

    @classmethod
    def devnet(cls) -> "NetworkConfig":
        return cls(
            chain_id=int(_env("DECIMAL_DEVNET_CHAIN_ID", "202020")),
            web3_urls=_csv_env("DECIMAL_DEVNET_WEB3_URLS", OFFICIAL_DEVNET_WEB3_URLS),
            rest_urls=_csv_env("DECIMAL_DEVNET_REST_URLS", OFFICIAL_DEVNET_REST_URLS),
            ws_urls=_csv_env("DECIMAL_DEVNET_WS_URLS", []),
            api_base_url=_env("DECIMAL_DEVNET_API_BASE", OFFICIAL_DEVNET_API_ROOT),
            api_root_url=_env("DECIMAL_DEVNET_API_ROOT", OFFICIAL_DEVNET_GATE_API_ROOT),
            api_fallback_base_urls=_csv_env(
                "DECIMAL_DEVNET_API_FALLBACK_BASES",
                [],
            ),
            api_key=os.getenv("DECIMAL_DEVNET_API_KEY"),
            name=_env("DECIMAL_DEVNET_NETWORK_NAME", "decimal-devnet"),
        )

    @classmethod
    def custom(
        cls,
        *,
        chain_id: int = 75,
        web3_urls: list[str] | None = None,
        rest_urls: list[str] | None = None,
        ws_urls: list[str] | None = None,
        api_root_url: str = "",
        api_base_url: str = "",
        api_fallback_base_urls: list[str] | None = None,
        api_key: str | None = None,
        name: str = "decimal-custom",
        contracts: SystemContracts | None = None,
        safety: SafetyLimits | None = None,
    ) -> "NetworkConfig":
        return cls(
            chain_id=chain_id,
            web3_urls=list(web3_urls or []),
            rest_urls=list(rest_urls or []),
            ws_urls=list(ws_urls or []),
            api_root_url=api_root_url,
            api_base_url=api_base_url,
            api_fallback_base_urls=list(api_fallback_base_urls or []),
            api_key=api_key,
            name=name,
            contracts=contracts or SystemContracts(),
            safety=safety or SafetyLimits(),
        )
