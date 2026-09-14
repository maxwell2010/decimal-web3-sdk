"""Completion and legacy penalty operations on fungible stakes."""

from __future__ import annotations

from dataclasses import dataclass

from ._contract_operations import ContractOperationRequest, ContractOperations, address, uint_list
from .transactions import TransactionResult


@dataclass(frozen=True)
class CompleteStakeRequest(ContractOperationRequest):
    """Indices from Delegation.getFrozenStakes, not hold timestamps or validator IDs."""

    indexes: tuple[int, ...]
    domain = "decimal"

    def to_contract_call(self, client):
        return self._encode(
            client,
            "delegation",
            client.config.contracts.delegation,
            "complete",
            [uint_list(self.indexes, "indexes")],
        )


@dataclass(frozen=True)
class ApplyStakePenaltyRequest(ContractOperationRequest):
    validator: str
    delegator: str
    token: str
    allow_legacy: bool = False
    domain = "decimal"

    def to_contract_call(self, client):
        if self.allow_legacy is not True:
            raise ValueError(
                "This penalty method is absent from the current Delegation ABI; legacy opt-in is required"
            )
        function = (
            "applyPenaltiesToStake"
            if isinstance(self, ApplyStakePenaltiesRequest)
            else "applyPenaltyToStake"
        )
        return self._encode(
            client,
            "legacy",
            client.config.contracts.delegation,
            function,
            [address(self.validator), address(self.delegator), address(self.token)],
        )


@dataclass(frozen=True)
class ApplyStakePenaltiesRequest(ApplyStakePenaltyRequest):
    """Legacy plural variant from the official JS SDK."""


class StakingOperations(ContractOperations):
    _operation_domain = "decimal"

    async def complete_stake(
        self, request: CompleteStakeRequest, broadcast: bool = False, wait_receipt: bool = False
    ) -> TransactionResult:
        return await self._send_operation(
            request, broadcast, wait_receipt, request_type=CompleteStakeRequest
        )

    async def apply_stake_penalty(
        self, request: ApplyStakePenaltyRequest, broadcast: bool = False, wait_receipt: bool = False
    ) -> TransactionResult:
        return await self._send_operation(
            request, broadcast, wait_receipt, request_type=ApplyStakePenaltyRequest
        )

    async def apply_stake_penalties(
        self,
        request: ApplyStakePenaltiesRequest,
        broadcast: bool = False,
        wait_receipt: bool = False,
    ) -> TransactionResult:
        return await self._send_operation(
            request, broadcast, wait_receipt, request_type=ApplyStakePenaltiesRequest
        )
