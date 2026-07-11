from __future__ import annotations

from decimal_web3_sdk import NetworkConfig


def _clear_safety_env(monkeypatch, prefix: str = "DECIMAL") -> None:
    for suffix in (
        "GAS_PRICE_GWEI",
        "MAX_GAS_PRICE_GWEI",
        "MAX_GAS_PRICE_WEI",
        "GAS_LIMIT_MULTIPLIER",
        "RECEIPT_WAIT_TIMEOUT_SECONDS",
        "RECEIPT_POLL_SECONDS",
    ):
        monkeypatch.delenv(f"{prefix}_{suffix}", raising=False)


def test_mainnet_defaults_use_public_decimal_rpc(monkeypatch) -> None:
    for name in (
        "DECIMAL_WEB3_URLS",
        "DECIMAL_REST_URLS",
        "DECIMAL_WS_URLS",
        "DECIMAL_API_ROOT",
        "DECIMAL_API_BASE",
        "DECIMAL_API_FALLBACK_BASES",
    ):
        monkeypatch.delenv(name, raising=False)
    _clear_safety_env(monkeypatch)

    config = NetworkConfig.mainnet()

    assert config.chain_id == 75
    assert config.web3_urls == ["https://node.decimalchain.com/web3/"]
    assert config.rest_urls == ["http://node.decimalchain.com/rest/"]
    assert config.api_root_url == "https://mainnet-gate.decimalchain.com/api/"
    assert config.api_base_url == "https://mainnet-api.decimalchain.com/api/"
    assert config.safety.max_gas_price_wei == 20_000_000_000
    assert "mintcandy" not in repr(config).lower()


def test_testnet_defaults_follow_decimal_js_sdk(monkeypatch) -> None:
    for name in (
        "DECIMAL_TESTNET_CHAIN_ID",
        "DECIMAL_TESTNET_WEB3_URLS",
        "DECIMAL_TESTNET_REST_URLS",
        "DECIMAL_TESTNET_API_ROOT",
        "DECIMAL_TESTNET_API_BASE",
        "DECIMAL_TESTNET_API_FALLBACK_BASES",
    ):
        monkeypatch.delenv(name, raising=False)
    _clear_safety_env(monkeypatch, "DECIMAL_TESTNET")

    config = NetworkConfig.testnet()

    assert config.chain_id == 202020
    assert config.web3_urls == [
        "https://testnet-val.decimalchain.com/web3/",
        "https://202020.rpc.thirdweb.com",
    ]
    assert config.rest_urls == ["http://testnet-val.decimalchain.com/rest/"]
    assert config.api_root_url == "https://testnet-gate.decimalchain.com/api/"
    assert config.api_base_url == "https://testnet-api.decimalchain.com/api/"
    assert config.name == "decimal-testnet"


def test_devnet_defaults_follow_decimal_js_sdk(monkeypatch) -> None:
    for name in (
        "DECIMAL_DEVNET_CHAIN_ID",
        "DECIMAL_DEVNET_WEB3_URLS",
        "DECIMAL_DEVNET_REST_URLS",
        "DECIMAL_DEVNET_API_ROOT",
        "DECIMAL_DEVNET_API_BASE",
        "DECIMAL_DEVNET_API_FALLBACK_BASES",
    ):
        monkeypatch.delenv(name, raising=False)
    _clear_safety_env(monkeypatch, "DECIMAL_DEVNET")

    config = NetworkConfig.devnet()

    assert config.chain_id == 202020
    assert config.web3_urls == ["https://devnet-val.decimalchain.com/web3/"]
    assert config.rest_urls == ["http://devnet-val.decimalchain.com/rest/"]
    assert config.api_root_url == "https://devnet-gate.decimalchain.com/api/"
    assert config.api_base_url == "https://devnet-api.decimalchain.com/api/"
    assert config.name == "decimal-devnet"


def test_custom_config_accepts_user_infrastructure() -> None:
    config = NetworkConfig.custom(
        chain_id=75,
        web3_urls=["https://example.org/web3"],
        api_base_url="https://example.org/api/v1",
        api_root_url="https://example.org/api",
        name="my-decimal-node",
    )

    assert config.web3_urls == ["https://example.org/web3"]
    assert config.api_base_url == "https://example.org/api/v1"
    assert config.api_root_url == "https://example.org/api"
    assert config.name == "my-decimal-node"


def test_mainnet_gas_price_cap_can_use_friday_env_name(monkeypatch) -> None:
    _clear_safety_env(monkeypatch)
    monkeypatch.setenv("DECIMAL_GAS_PRICE_GWEI", "25")

    config = NetworkConfig.mainnet()

    assert config.safety.max_gas_price_wei == 25_000_000_000


def test_mainnet_gas_price_cap_can_be_disabled(monkeypatch) -> None:
    _clear_safety_env(monkeypatch)
    monkeypatch.setenv("DECIMAL_MAX_GAS_PRICE_WEI", "none")

    config = NetworkConfig.mainnet()

    assert config.safety.max_gas_price_wei is None
