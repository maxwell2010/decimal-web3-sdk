from __future__ import annotations

import pytest

from decimal_web3_sdk import DecimalClient, NetworkConfig


@pytest.mark.integration
@pytest.mark.asyncio
async def test_live_readonly_health_snapshot() -> None:
    async with DecimalClient() as client:
        block_number = await client.block_number()

    assert block_number > 0


@pytest.mark.integration
@pytest.mark.asyncio
async def test_live_readonly_rest_health_when_configured() -> None:
    config = NetworkConfig.mainnet()
    if not config.api_root_url:
        pytest.skip("Set DECIMAL_API_ROOT to run REST health smoke")

    async with DecimalClient(config) as client:
        data = await client.rest.health()

    assert isinstance(data, dict)
