from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class Page:
    limit: int = 50
    offset: int = 0
    order: str = "desc"

    def params(self, max_limit: int = 100) -> dict[str, Any]:
        limit = min(max(1, int(self.limit)), max_limit)
        offset = max(0, int(self.offset))
        order = "asc" if self.order == "asc" else "desc"
        return {"limit": limit, "offset": offset, "order": order}


class RestClient:
    def __init__(self, client) -> None:
        self._client = client

    @property
    def _max_limit(self) -> int:
        return int(self._client.config.safety.rest_max_limit)

    async def health(self) -> dict[str, Any]:
        return await self._client.rest_root_get("/health")

    async def latest_block(self) -> dict[str, Any]:
        return await self._client.rest_get("/blocks/latest")

    async def block(self, height: int) -> dict[str, Any]:
        return await self._client.rest_get(f"/blocks/{height}")

    async def block_txs(self, height: int, page: Page | None = None) -> dict[str, Any]:
        return await self._client.rest_get(
            f"/blocks/{height}/txs", **(page or Page()).params(self._max_limit)
        )

    async def tx(self, tx_hash: str) -> dict[str, Any]:
        return await self._client.rest_get(f"/txs/{tx_hash}")

    async def txs(self, page: Page | None = None, **filters: Any) -> dict[str, Any]:
        params = (page or Page()).params(self._max_limit)
        params.update({key: value for key, value in filters.items() if value is not None})
        return await self._client.rest_get("/txs", **params)

    async def address(self, address: str) -> dict[str, Any]:
        return await self._client.rest_get(f"/addresses/{address}")

    async def address_full(
        self,
        address: str,
        with_erc20: bool = True,
        symbols: str | None = None,
    ) -> dict[str, Any]:
        params: dict[str, Any] = {"with_erc20": int(with_erc20)}
        if symbols:
            params["symbols"] = symbols
        return await self._client.rest_get(f"/addresses/{address}/full", **params)

    async def wallet_balances(
        self,
        address: str,
        limit: int = 300,
        offset: int = 0,
        include_bank: bool = True,
        prefer_bank: bool = True,
    ) -> dict[str, Any]:
        """Fast full wallet balance: DEL + bank-module balances + indexed DRC20/ERC20 balances."""
        safe_limit = min(max(1, int(limit)), max(self._max_limit, 300))
        return await self._client.rest_get(
            f"/erc20/balances/{address}",
            limit=safe_limit,
            offset=max(0, int(offset)),
            include_bank=int(include_bank),
            prefer_bank=int(prefer_bank),
        )

    async def address_txs(self, address: str, page: Page | None = None) -> dict[str, Any]:
        return await self._client.rest_get(
            f"/addresses/{address}/txs", **(page or Page()).params(self._max_limit)
        )

    async def coins(self, with_price: bool = False, limit: int = 100) -> dict[str, Any]:
        safe_limit = min(max(1, int(limit)), self._max_limit)
        return await self._client.rest_get(
            "/coins", with_price=int(with_price), **{"pagination.limit": safe_limit}
        )

    async def coin(self, denom: str) -> dict[str, Any]:
        return await self._client.rest_get(f"/coins/{denom}")

    async def coin_prices(self) -> dict[str, Any]:
        return await self._client.rest_get("/coins/prices")

    async def validators(self) -> dict[str, Any]:
        return await self._client.rest_get("/validators")

    async def validator(self, validator: str) -> dict[str, Any]:
        return await self._client.rest_get(f"/validators/{validator}")

    async def validator_delegations(self, validator: str) -> dict[str, Any]:
        return await self._client.rest_get(f"/validators/{validator}/delegations")

    async def rewards_delegator(self, delegator: str) -> dict[str, Any]:
        return await self._client.rest_get(f"/rewards/delegators/{delegator}")
