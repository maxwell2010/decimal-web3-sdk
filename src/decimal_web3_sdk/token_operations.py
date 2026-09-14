"""Exact-output trading and optional legacy Decimal token calls."""

from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal

from ._contract_operations import (
    ContractOperationRequest,
    ContractOperations,
    address,
    permit_values,
    uint,
)
from .erc20 import PermitSignature, parse_units
from .transactions import TransactionResult


@dataclass(frozen=True)
class BuyExactTokenRequest(ContractOperationRequest):
    token: str
    recipient: str
    amount_out_raw: int
    max_amount_del: Decimal | str | int
    domain = "token"

    def to_contract_call(self, client):
        value = uint(parse_units(self.max_amount_del, 18), "max_amount_del", positive=True)
        return self._encode(
            client,
            "token",
            self.token,
            "buyExactTokenForDEL",
            [uint(self.amount_out_raw, "amount_out_raw", positive=True), address(self.recipient)],
            value,
        )


@dataclass(frozen=True)
class SellForExactDelRequest(ContractOperationRequest):
    token: str
    recipient: str
    amount_out_del: Decimal | str | int
    max_amount_in_raw: int
    domain = "token"

    def to_contract_call(self, client):
        output = uint(parse_units(self.amount_out_del, 18), "amount_out_del", positive=True)
        return self._encode(
            client,
            "token",
            self.token,
            "sellTokensForExactDEL",
            [
                output,
                uint(self.max_amount_in_raw, "max_amount_in_raw", positive=True),
                address(self.recipient),
            ],
        )


@dataclass(frozen=True)
class ConvertToDelRequest(ContractOperationRequest):
    """GasCenter conversion using an owner-supplied permit; not ordinary token selling."""

    owner: str
    token: str
    amount_raw: int
    estimated_gas: int
    permit: PermitSignature
    domain = "token"

    def to_contract_call(self, client):
        args = [
            address(self.owner),
            address(self.token),
            uint(self.amount_raw, "amount_raw", positive=True),
            uint(self.estimated_gas, "estimated_gas", positive=True),
            *permit_values(self.permit),
        ]
        return self._encode(
            client, "gas_center", client.config.contracts.gas_center, "convertToDEL", args
        )


@dataclass(frozen=True)
class UpdateTokenMinSupplyRequest(ContractOperationRequest):
    token: str
    min_total_supply_raw: int
    allow_legacy: bool = False
    domain = "token"

    def to_contract_call(self, client):
        if self.allow_legacy is not True:
            raise ValueError(
                "updateMinTotalSupply is absent from the inspected current token ABI; legacy opt-in is required"
            )
        return self._encode(
            client,
            "legacy",
            self.token,
            "updateMinTotalSupply",
            [uint(self.min_total_supply_raw, "min_total_supply_raw")],
        )


class TokenOperations(ContractOperations):
    _operation_domain = "token"

    async def buy_exact(
        self, request: BuyExactTokenRequest, broadcast: bool = False, wait_receipt: bool = False
    ) -> TransactionResult:
        return await self._send_operation(
            request, broadcast, wait_receipt, request_type=BuyExactTokenRequest
        )

    async def sell_for_exact_del(
        self, request: SellForExactDelRequest, broadcast: bool = False, wait_receipt: bool = False
    ) -> TransactionResult:
        return await self._send_operation(
            request, broadcast, wait_receipt, request_type=SellForExactDelRequest
        )

    async def convert_to_del(
        self, request: ConvertToDelRequest, broadcast: bool = False, wait_receipt: bool = False
    ) -> TransactionResult:
        return await self._send_operation(
            request, broadcast, wait_receipt, request_type=ConvertToDelRequest
        )

    async def update_min_supply(
        self,
        request: UpdateTokenMinSupplyRequest,
        broadcast: bool = False,
        wait_receipt: bool = False,
    ) -> TransactionResult:
        return await self._send_operation(
            request, broadcast, wait_receipt, request_type=UpdateTokenMinSupplyRequest
        )
