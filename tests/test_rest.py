from __future__ import annotations

from types import SimpleNamespace

import pytest

from decimal_web3_sdk import Page, RestClient


class FakeClient:
    def __init__(self) -> None:
        self.calls: list[tuple[str, dict]] = []
        self.config = SimpleNamespace(safety=SimpleNamespace(rest_max_limit=100))

    async def rest_get(self, path: str, **params):
        self.calls.append((path, params))
        return {"Ok": True, "path": path, "params": params}

    async def rest_root_get(self, path: str, **params):
        self.calls.append((f"root:{path}", params))
        return {"Ok": True, "path": path, "params": params}


@pytest.mark.asyncio
async def test_rest_client_builds_address_full_query() -> None:
    client = FakeClient()
    rest = RestClient(client)

    result = await rest.address_full("0xabc", with_erc20=True, symbols="FRIDAYCOIN")

    assert result["path"] == "/addresses/0xabc/full"
    assert result["params"] == {"with_erc20": 1, "symbols": "FRIDAYCOIN"}


@pytest.mark.asyncio
async def test_rest_client_uses_page_defaults() -> None:
    client = FakeClient()
    rest = RestClient(client)

    await rest.txs(Page(limit=10, offset=20, order="asc"), address="0xabc")

    assert client.calls == [("/txs", {"limit": 10, "offset": 20, "order": "asc", "address": "0xabc"})]


def test_page_clamps_limit_and_offset() -> None:
    assert Page(limit=1000, offset=-1, order="wat").params(max_limit=100) == {
        "limit": 100,
        "offset": 0,
        "order": "desc",
    }
