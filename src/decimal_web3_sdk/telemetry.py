from __future__ import annotations

import time
from dataclasses import dataclass, field
from statistics import mean


@dataclass(frozen=True)
class Timing:
    name: str
    duration_ms: float
    success: bool
    tags: dict[str, str] = field(default_factory=dict)


class MetricsCollector:
    def __init__(self) -> None:
        self._timings: list[Timing] = []

    @property
    def timings(self) -> tuple[Timing, ...]:
        return tuple(self._timings)

    def observe(
        self,
        name: str,
        started_at: float,
        success: bool,
        tags: dict[str, str] | None = None,
    ) -> Timing:
        timing = Timing(
            name=name,
            duration_ms=(time.perf_counter() - started_at) * 1000,
            success=success,
            tags=tags or {},
        )
        self._timings.append(timing)
        return timing

    def summary(self) -> dict[str, float | int]:
        if not self._timings:
            return {"count": 0, "success": 0, "failed": 0, "avg_ms": 0.0, "max_ms": 0.0}
        durations = [item.duration_ms for item in self._timings]
        success = sum(1 for item in self._timings if item.success)
        return {
            "count": len(self._timings),
            "success": success,
            "failed": len(self._timings) - success,
            "avg_ms": mean(durations),
            "max_ms": max(durations),
        }


class Stopwatch:
    def __init__(self) -> None:
        self.started_at = time.perf_counter()

    @property
    def elapsed_ms(self) -> float:
        return (time.perf_counter() - self.started_at) * 1000
