from __future__ import annotations

import asyncio
from collections.abc import Callable
from typing import TypeVar

from web3 import Web3

from ._tls import validate_ca_file
from .limits import AsyncRateLimiter

T = TypeVar("T")


class RpcPool:
    def __init__(self, urls: list[str], timeout: int = 10, min_interval_seconds: float = 0.05, *, chain_id: int | None = None, ca_file: str | None = None) -> None:
        if not urls:
            raise ValueError("At least one Web3 RPC URL is required")
        validate_ca_file(ca_file)
        self._urls = list(urls)
        self._chain_id = chain_id
        self._ca_file = ca_file
        self._validated_web3: Web3 | None = None
        self._timeout = timeout
        self._index = 0
        self._web3: Web3 | None = None
        self._limiter = AsyncRateLimiter(min_interval_seconds)

    @property
    def current_url(self) -> str:
        return self._urls[self._index]

    @property
    def web3(self) -> Web3:
        if self._web3 is None:
            self._web3 = self._create_web3(self.current_url)
        return self._web3

    async def connect(self) -> bool:
        def ready(w3):
            if not w3.is_connected():
                raise ConnectionError("RPC is not connected")
            return True
        try:
            return await self.call(ready)
        except RuntimeError:
            return False

    def rotate(self) -> None:
        self._index = (self._index + 1) % len(self._urls)
        self._web3 = None

    async def call(self, fn: Callable[[Web3], T]) -> T:
        last_error: Exception | None = None
        for _ in self._urls:
            try:
                await self._limiter.wait()
                w3 = self.web3
                if self._chain_id is not None and self._validated_web3 is not w3:
                    actual = await self._run(lambda: w3.eth.chain_id)
                    if int(actual) != self._chain_id:
                        raise ValueError("RPC chain ID does not match the configured network")
                    self._validated_web3 = w3
                return await self._run(lambda: fn(w3))
            except Exception as exc:
                last_error = exc
                self.rotate()
        detail = f": {last_error}" if last_error else ""
        raise RuntimeError(f"All Decimal Web3 RPC endpoints failed{detail}") from last_error

    def _create_web3(self, url: str) -> Web3:
        request_kwargs: dict[str, object] = {"timeout": self._timeout}
        if self._ca_file is not None:
            request_kwargs["verify"] = self._ca_file
        # RpcPool owns failover; provider retries would multiply each endpoint timeout.
        provider = Web3.HTTPProvider(
            url, request_kwargs=request_kwargs, exception_retry_configuration=None,
        )
        return Web3(provider)

    async def _run(self, fn: Callable[[], T]) -> T:
        loop = asyncio.get_running_loop()
        return await loop.run_in_executor(None, fn)
