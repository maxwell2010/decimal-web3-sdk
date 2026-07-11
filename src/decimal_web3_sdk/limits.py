from __future__ import annotations

import asyncio
import time
from dataclasses import dataclass


@dataclass(frozen=True)
class SafetyLimits:
    rest_max_limit: int = 100
    rest_min_interval_seconds: float = 0.15
    rpc_min_interval_seconds: float = 0.05
    gas_limit_multiplier: float = 1.10
    max_gas_price_wei: int | None = 20_000_000_000
    receipt_wait_timeout_seconds: float = 7.0
    receipt_poll_seconds: float = 3.0
    ws_max_subscriptions: int = 16
    ws_ping_interval_seconds: float = 30.0
    ws_reconnect_min_delay_seconds: float = 2.0
    integration_tests_enabled: bool = False


class AsyncRateLimiter:
    def __init__(self, min_interval_seconds: float) -> None:
        self._min_interval_seconds = max(0.0, min_interval_seconds)
        self._lock = asyncio.Lock()
        self._last_at = 0.0

    async def wait(self) -> None:
        if self._min_interval_seconds <= 0:
            return
        async with self._lock:
            now = time.perf_counter()
            delay = self._min_interval_seconds - (now - self._last_at)
            if delay > 0:
                await asyncio.sleep(delay)
            self._last_at = time.perf_counter()
