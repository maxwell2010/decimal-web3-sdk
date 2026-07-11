from __future__ import annotations

from .agents import AgentContext, AgentResult
from .transactions import NativeTransferRequest


class BuildNativeTransferAgent:
    name = "tx_build_native_transfer"

    async def run(self, context: AgentContext) -> AgentResult:
        client = context.client
        request = context.data.get("request")
        if client is None or not isinstance(request, NativeTransferRequest):
            return AgentResult(self.name, False, error="Client and NativeTransferRequest are required")
        draft = await client.tx.build_native_transfer(request)
        context.data["draft"] = draft
        return AgentResult(self.name, True, {"from": draft.from_address, "to": draft.to_address})


class EstimateGasAgent:
    name = "tx_estimate_gas"

    async def run(self, context: AgentContext) -> AgentResult:
        client = context.client
        draft = context.data.get("draft")
        if client is None or draft is None:
            return AgentResult(self.name, False, error="Client and draft are required")
        draft = await client.tx.estimate(draft)
        context.data["draft"] = draft
        return AgentResult(self.name, True, {"gas": draft.gas, "fee_wei": draft.fee_wei})


class SignTransactionAgent:
    name = "tx_sign"

    async def run(self, context: AgentContext) -> AgentResult:
        client = context.client
        request = context.data.get("request")
        draft = context.data.get("draft")
        if client is None or not isinstance(request, NativeTransferRequest) or draft is None:
            return AgentResult(self.name, False, error="Client, request and draft are required")
        draft = await client.tx.sign(draft, request.private_key)
        context.data["draft"] = draft
        return AgentResult(self.name, True, {"signed": draft.raw_tx is not None})


class BroadcastTransactionAgent:
    name = "tx_broadcast"

    async def run(self, context: AgentContext) -> AgentResult:
        client = context.client
        draft = context.data.get("draft")
        if client is None or draft is None:
            return AgentResult(self.name, False, error="Client and draft are required")
        request = context.data.get("request")
        private_key = getattr(request, "private_key", None)
        if private_key:
            draft = await client.tx.broadcast_with_fee_retry(draft, private_key)
        else:
            draft = await client.tx.broadcast(draft)
        context.data["draft"] = draft
        return AgentResult(self.name, True, {"tx_hash": draft.tx_hash})


class ReceiptPollAgent:
    name = "tx_receipt_poll"

    async def run(self, context: AgentContext) -> AgentResult:
        client = context.client
        draft = context.data.get("draft")
        if client is None or draft is None:
            return AgentResult(self.name, False, error="Client and draft are required")
        draft = await client.tx.wait_receipt(
            draft,
            timeout_seconds=context.policy.receipt_poll_seconds,
        )
        context.data["draft"] = draft
        return AgentResult(
            self.name,
            True,
            {"confirmed": draft.receipt is not None, "tx_hash": draft.tx_hash},
        )
