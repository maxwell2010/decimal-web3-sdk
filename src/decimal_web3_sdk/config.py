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


def _env_float(name: str, fallback: float) -> float:
    raw = os.getenv(name)
    if raw is None or raw.strip() == "":
        return fallback
    return float(raw)


def _env_int(name: str, fallback: int) -> int:
    raw = os.getenv(name)
    if raw is None or raw.strip() == "":
        return fallback
    return int(raw)


def _env_optional_gas_price_wei(prefix: str = "DECIMAL") -> int | None:
    raw_wei = os.getenv(f"{prefix}_MAX_GAS_PRICE_WEI")
    if raw_wei is not None and raw_wei.strip() != "":
        value = raw_wei.strip().lower()
        if value in {"none", "off", "disabled", "0"}:
            return None
        return int(value)
    raw_gwei = os.getenv(f"{prefix}_MAX_GAS_PRICE_GWEI") or os.getenv(f"{prefix}_GAS_PRICE_GWEI")
    if raw_gwei is not None and raw_gwei.strip() != "":
        value = raw_gwei.strip().lower()
        if value in {"none", "off", "disabled", "0"}:
            return None
        return int(float(value) * 10**9)
    return 20_000_000_000


def _safety_from_env(prefix: str = "DECIMAL") -> SafetyLimits:
    return SafetyLimits(
        rest_max_limit=_env_int(f"{prefix}_REST_MAX_LIMIT", 100),
        rest_min_interval_seconds=_env_float(f"{prefix}_REST_MIN_INTERVAL_SECONDS", 0.15),
        rpc_min_interval_seconds=_env_float(f"{prefix}_RPC_MIN_INTERVAL_SECONDS", 0.05),
        gas_limit_multiplier=_env_float(f"{prefix}_GAS_LIMIT_MULTIPLIER", 1.10),
        max_gas_price_wei=_env_optional_gas_price_wei(prefix),
        receipt_wait_timeout_seconds=_env_float(f"{prefix}_RECEIPT_WAIT_TIMEOUT_SECONDS", 7.0),
        receipt_poll_seconds=_env_float(f"{prefix}_RECEIPT_POLL_SECONDS", 3.0),
        ws_max_subscriptions=_env_int(f"{prefix}_WS_MAX_SUBSCRIPTIONS", 16),
        ws_ping_interval_seconds=_env_float(f"{prefix}_WS_PING_INTERVAL_SECONDS", 30.0),
        ws_reconnect_min_delay_seconds=_env_float(f"{prefix}_WS_RECONNECT_MIN_DELAY_SECONDS", 2.0),
        integration_tests_enabled=bool(_env_int(f"{prefix}_INTEGRATION_TESTS_ENABLED", 0)),
    )


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
    checks: str = "0x9c3326594b49AFa24db9b988Cda1258d0dcb4e40"
    gas_center: str = "0xeF21c8573715F9c6b644d209B1E860Dbd2f7A947"
    safe: str = "0x15949c33775154549D073168C1094C5f3b28b5CB"
    safe_factory: str = "0x92466f09D5c82e8DdB8AaA7c5AdC63d43111F6c1"
    multi_send: str = "0x72b80471AAFabd1469ed1C51453DC9ca66068bC0"


TESTNET_SYSTEM_CONTRACTS = SystemContracts(
    multicall="0x81FD5FAe106dFD0343B0435a1bc0ef89BB14C317",
    checks="0xb6161CAA8Bd7167C2fa67b93b041FF9a94d6a735",
    gas_center="0xB32439bF0C3742D0a227BFEc78276F7bA15F8Aa1",
    safe="0xE0f30FcCAe2f9f9C7efee9af044C436841D466ee",
    safe_factory="0x4cC406B1713d3dF67e739D6f5918B6C98F614a38",
    multi_send="0xC0611a00CE349B9bCff3866351A2a5Aa9659c464",
)


DEVNET_SYSTEM_CONTRACTS = SystemContracts(
    multicall="0xd633Ac8b1fcb48A2b3d7a676D1B527E923f66213",
    checks="0x",
    gas_center="0xeF21c8573715F9c6b644d209B1E860Dbd2f7A947",
    safe="0xAaA4813B459B4af71C7C172880D504C6663c11F7",
    safe_factory="0xAa6Fe7d309741897f5E2De994c90155b0252d104",
    multi_send="0xf28404962e594aFAf7FE0a9eE2e760f925B3aCDc",
)


DEFAULT_MAINNET_WEB3_URLS = ["https://node.decimalchain.com/web3/"]
DEFAULT_TESTNET_WEB3_URLS = [
    "https://testnet-val.decimalchain.com/web3/",
    # Public third-party Decimal testnet RPC for chainId 202020.
    # It is intentionally a fallback, not an official Decimal endpoint.
    "https://202020.rpc.thirdweb.com",
]
DEFAULT_DEVNET_WEB3_URLS = ["https://devnet-val.decimalchain.com/web3/"]

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
                DEFAULT_MAINNET_WEB3_URLS,
            ),
            rest_urls=_csv_env("DECIMAL_REST_URLS", OFFICIAL_MAINNET_REST_URLS),
            ws_urls=_csv_env("DECIMAL_WS_URLS", []),
            api_base_url=_env("DECIMAL_API_BASE", OFFICIAL_MAINNET_API_ROOT),
            api_root_url=_env("DECIMAL_API_ROOT", OFFICIAL_MAINNET_GATE_API_ROOT),
            api_fallback_base_urls=_csv_env("DECIMAL_API_FALLBACK_BASES", []),
            api_key=os.getenv("DECIMAL_API_KEY"),
            name=_env("DECIMAL_NETWORK_NAME", "decimal-mainnet"),
            safety=_safety_from_env("DECIMAL"),
        )

    @classmethod
    def testnet(cls) -> "NetworkConfig":
        return cls(
            chain_id=int(_env("DECIMAL_TESTNET_CHAIN_ID", "202020")),
            web3_urls=_csv_env("DECIMAL_TESTNET_WEB3_URLS", DEFAULT_TESTNET_WEB3_URLS),
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
            contracts=TESTNET_SYSTEM_CONTRACTS,
            safety=_safety_from_env("DECIMAL_TESTNET"),
        )

    @classmethod
    def devnet(cls) -> "NetworkConfig":
        return cls(
            chain_id=int(_env("DECIMAL_DEVNET_CHAIN_ID", "202020")),
            web3_urls=_csv_env("DECIMAL_DEVNET_WEB3_URLS", DEFAULT_DEVNET_WEB3_URLS),
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
            contracts=DEVNET_SYSTEM_CONTRACTS,
            safety=_safety_from_env("DECIMAL_DEVNET"),
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
