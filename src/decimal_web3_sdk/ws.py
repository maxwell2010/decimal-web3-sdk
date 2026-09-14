from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Any

import aiohttp


@dataclass(frozen=True)
class WsMessage:
    raw: str
    data: dict[str, Any] | list[Any] | str | None


class DecimalWsClient:
    def __init__(self, config, session: aiohttp.ClientSession | None = None) -> None:
        self.config = config
        self._external_session = session
        self._session: aiohttp.ClientSession | None = session
        self._ws: aiohttp.ClientWebSocketResponse | None = None
        self._url_index = 0
        self._subscriptions = 0
        self._request_id = 0

    @property
    def connected(self) -> bool:
        return self._ws is not None and not self._ws.closed

    async def connect(self) -> bool:
        if self.connected:
            return True
        if not self.config.ws_urls:
            return False
        session = await self._get_session()
        url = self.config.ws_urls[self._url_index]
        self._ws = await session.ws_connect(
            url,
            heartbeat=self.config.safety.ws_ping_interval_seconds,
            autoping=True,
            timeout=10,
        )
        return self.connected

    async def close(self) -> None:
        if self._ws is not None:
            await self._ws.close()
            self._ws = None
        if self._session is not None and self._external_session is None:
            await self._session.close()
            self._session = None

    async def subscribe(self, query: str) -> dict[str, Any]:
        if self._subscriptions >= self.config.safety.ws_max_subscriptions:
            raise RuntimeError("WS subscription limit reached")
        if not self.connected:
            await self.connect()
        if self._ws is None:
            raise RuntimeError("WS is not connected")
        self._request_id += 1
        payload = {"jsonrpc": "2.0", "method": "subscribe", "id": self._request_id, "params": {"query": query}}
        await self._ws.send_str(json.dumps(payload))
        self._subscriptions += 1
        return payload

    async def unsubscribe(self, query: str) -> dict[str, Any]:
        if not self.connected or self._ws is None:
            raise RuntimeError("WS is not connected")
        self._request_id += 1
        payload = {
            "jsonrpc": "2.0",
            "method": "unsubscribe",
            "id": self._request_id,
            "params": {"query": query},
        }
        await self._ws.send_str(json.dumps(payload))
        self._subscriptions = max(0, self._subscriptions - 1)
        return payload

    async def receive_once(self, timeout_seconds: float = 5.0) -> WsMessage | None:
        if not self.connected or self._ws is None:
            raise RuntimeError("WS is not connected")
        msg = await self._ws.receive(timeout=timeout_seconds)
        if msg.type == aiohttp.WSMsgType.TEXT:
            raw = str(msg.data)
            try:
                data = json.loads(raw)
            except json.JSONDecodeError:
                data = raw
            return WsMessage(raw=raw, data=data)
        if msg.type in (aiohttp.WSMsgType.CLOSE, aiohttp.WSMsgType.CLOSED, aiohttp.WSMsgType.ERROR):
            return None
        return WsMessage(raw=str(msg.data), data=None)

    async def _get_session(self) -> aiohttp.ClientSession:
        if self._session is None:
            self._session = aiohttp.ClientSession()
        return self._session
