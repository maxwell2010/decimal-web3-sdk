from __future__ import annotations

import asyncio

import pytest

from decimal_web3_sdk import AgentContext, AgentOrchestrator, AgentResult, TransactionPolicy


class FastAgent:
    name = "fast"

    async def run(self, context: AgentContext) -> AgentResult:
        return AgentResult(self.name, True, {"ok": True})


class SlowAgent:
    name = "slow"

    async def run(self, context: AgentContext) -> AgentResult:
        await asyncio.sleep(0.05)
        return AgentResult(self.name, True)


class FailingAgent:
    name = "failing"

    async def run(self, context: AgentContext) -> AgentResult:
        return AgentResult(self.name, False, error="boom")


@pytest.mark.asyncio
async def test_parallel_orchestrator_collects_timings() -> None:
    orchestrator = AgentOrchestrator([FastAgent(), SlowAgent()], default_timeout_seconds=1)

    result = await orchestrator.run_parallel(AgentContext())

    assert result.success is True
    assert [item.name for item in result.results] == ["fast", "slow"]
    assert result.metrics["count"] == 2
    assert result.metrics["success"] == 2


@pytest.mark.asyncio
async def test_sequential_orchestrator_stops_on_error() -> None:
    orchestrator = AgentOrchestrator([FailingAgent(), FastAgent()], default_timeout_seconds=1)

    result = await orchestrator.run_sequential(AgentContext(), stop_on_error=True)

    assert result.success is False
    assert [item.name for item in result.results] == ["failing"]


@pytest.mark.asyncio
async def test_agent_timeout_is_reported() -> None:
    orchestrator = AgentOrchestrator([SlowAgent()], default_timeout_seconds=0.001)

    result = await orchestrator.run_parallel(AgentContext())

    assert result.success is False
    assert result.results[0].name == "slow"
    assert "timed out" in str(result.results[0].error)


def test_transaction_policy_rejects_impossible_budget() -> None:
    policy = TransactionPolicy(
        target_total_seconds=1,
        build_timeout_seconds=1,
        estimate_timeout_seconds=1,
        broadcast_timeout_seconds=1,
        receipt_poll_seconds=1,
    )

    with pytest.raises(ValueError):
        policy.validate()

