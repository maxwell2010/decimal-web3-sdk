from __future__ import annotations

import asyncio
import time
from dataclasses import dataclass, field

from .agents import AgentContext, AgentResult, DecimalAgent
from .telemetry import MetricsCollector, Timing


@dataclass(frozen=True)
class OrchestratorResult:
    success: bool
    results: tuple[AgentResult, ...]
    timings: tuple[Timing, ...]
    metrics: dict[str, float | int] = field(default_factory=dict)


class AgentOrchestrator:
    def __init__(
        self,
        agents: list[DecimalAgent] | None = None,
        metrics: MetricsCollector | None = None,
        default_timeout_seconds: float = 5.0,
    ) -> None:
        self.agents = agents or []
        self.metrics = metrics or MetricsCollector()
        self.default_timeout_seconds = default_timeout_seconds

    def add(self, agent: DecimalAgent) -> None:
        self.agents.append(agent)

    async def run_parallel(
        self,
        context: AgentContext,
        timeout_seconds: float | None = None,
    ) -> OrchestratorResult:
        timeout = timeout_seconds or self.default_timeout_seconds
        results = await asyncio.gather(
            *(self._run_one(agent, context, timeout) for agent in self.agents)
        )
        return self._result(results)

    async def run_sequential(
        self,
        context: AgentContext,
        timeout_seconds: float | None = None,
        stop_on_error: bool = True,
    ) -> OrchestratorResult:
        timeout = timeout_seconds or self.default_timeout_seconds
        results: list[AgentResult] = []
        for agent in self.agents:
            result = await self._run_one(agent, context, timeout)
            results.append(result)
            if stop_on_error and not result.success:
                break
        return self._result(results)

    async def _run_one(
        self,
        agent: DecimalAgent,
        context: AgentContext,
        timeout_seconds: float,
    ) -> AgentResult:
        started_at = time.perf_counter()
        success = False
        try:
            result = await asyncio.wait_for(agent.run(context), timeout=timeout_seconds)
            success = result.success
            return result
        except TimeoutError:
            return AgentResult(agent.name, False, error=f"Agent timed out after {timeout_seconds}s")
        except Exception as exc:
            return AgentResult(agent.name, False, error=str(exc))
        finally:
            self.metrics.observe(agent.name, started_at, success, {"agent": agent.name})

    def _result(self, results: list[AgentResult]) -> OrchestratorResult:
        return OrchestratorResult(
            success=all(item.success for item in results),
            results=tuple(results),
            timings=self.metrics.timings,
            metrics=self.metrics.summary(),
        )
