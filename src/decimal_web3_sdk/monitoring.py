from __future__ import annotations

from dataclasses import dataclass

from .agents import AgentContext, HealthCheckAgent, LatestBlockAgent, RestLatencyAgent, TransactionSlaAgent
from .orchestrator import AgentOrchestrator, OrchestratorResult
from .policy import TransactionPolicy


@dataclass(frozen=True)
class MonitorSnapshot:
    healthy: bool
    result: OrchestratorResult


class DecimalMonitor:
    def __init__(self, client, policy: TransactionPolicy | None = None) -> None:
        self.client = client
        self.policy = policy or TransactionPolicy.fast()
        self.orchestrator = AgentOrchestrator(
            [TransactionSlaAgent(), HealthCheckAgent(), LatestBlockAgent(), RestLatencyAgent()],
            default_timeout_seconds=self.policy.target_total_seconds,
        )

    async def snapshot(self) -> MonitorSnapshot:
        context = AgentContext(client=self.client, policy=self.policy)
        result = await self.orchestrator.run_sequential(context, stop_on_error=False)
        return MonitorSnapshot(healthy=result.success, result=result)
