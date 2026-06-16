from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Protocol

from .policy import TransactionPolicy


@dataclass
class AgentContext:
    client: Any | None = None
    data: dict[str, Any] = field(default_factory=dict)
    policy: TransactionPolicy = field(default_factory=TransactionPolicy.fast)


@dataclass(frozen=True)
class AgentResult:
    name: str
    success: bool
    payload: dict[str, Any] = field(default_factory=dict)
    error: str | None = None


class DecimalAgent(Protocol):
    name: str

    async def run(self, context: AgentContext) -> AgentResult:
        raise NotImplementedError


class HealthCheckAgent:
    name = "health_check"

    async def run(self, context: AgentContext) -> AgentResult:
        client = context.client
        if client is None:
            return AgentResult(self.name, False, error="Client is required")
        connected = await client.connect()
        return AgentResult(self.name, connected, {"connected": connected})


class LatestBlockAgent:
    name = "latest_block"

    async def run(self, context: AgentContext) -> AgentResult:
        client = context.client
        if client is None:
            return AgentResult(self.name, False, error="Client is required")
        block_number = await client.block_number()
        return AgentResult(self.name, True, {"block_number": block_number})


class RestLatencyAgent:
    name = "rest_latency"

    async def run(self, context: AgentContext) -> AgentResult:
        client = context.client
        if client is None:
            return AgentResult(self.name, False, error="Client is required")
        data = await client.rest.health()
        return AgentResult(self.name, True, {"health": data})


class TransactionSlaAgent:
    name = "transaction_sla"

    async def run(self, context: AgentContext) -> AgentResult:
        try:
            context.policy.validate()
        except ValueError as exc:
            return AgentResult(self.name, False, error=str(exc))
        return AgentResult(
            self.name,
            True,
            {
                "target_total_seconds": context.policy.target_total_seconds,
                "build_timeout_seconds": context.policy.build_timeout_seconds,
                "estimate_timeout_seconds": context.policy.estimate_timeout_seconds,
                "broadcast_timeout_seconds": context.policy.broadcast_timeout_seconds,
                "receipt_poll_seconds": context.policy.receipt_poll_seconds,
                "max_rpc_attempts": context.policy.max_rpc_attempts,
            },
        )
