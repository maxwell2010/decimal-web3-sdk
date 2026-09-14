"""Shared unsigned preparation for the additional Decimal contract operations."""

from __future__ import annotations

from dataclasses import dataclass, field, replace
from typing import ClassVar

from .erc20 import PermitSignature
from .mnemonic import FromMnemonicMixin
from .transactions import (
    ContractCallRequest,
    FeePreflight,
    TransactionDraft,
    TransactionResult,
    _exception_failure,
)
from .wallet import checksum

ZERO_ADDRESS = "0x" + "00" * 20


def uint(value: int, name: str, *, positive: bool = False) -> int:
    if isinstance(value, bool) or not isinstance(value, int):
        raise TypeError(f"{name} must be an integer, not a rounded amount")
    if not (1 if positive else 0) <= value < 2**256:
        raise ValueError(f"{name} is outside the uint256 range")
    return value


def uint_list(values, name: str) -> list[int]:
    result = [uint(value, name) for value in values]
    if not result or len(set(result)) != len(result):
        raise ValueError(f"{name} must be nonempty and contain no duplicates")
    return result


def address(value: str) -> str:
    result = checksum(value)
    if result == ZERO_ADDRESS:
        raise ValueError("A nonzero address is required")
    return result


def permit_values(permit: PermitSignature) -> list:
    if not isinstance(permit, PermitSignature):
        raise TypeError("A PermitSignature is required")
    if type(permit.v) is not int or permit.v not in (27, 28):
        raise ValueError("Permit v must be 27 or 28")
    for item in (permit.r, permit.s):
        if not isinstance(item, bytes) or len(item) != 32 or int.from_bytes(item, "big") == 0:
            raise ValueError("Permit r and s must be nonzero 32-byte values")
    return [uint(permit.deadline, "deadline", positive=True), permit.v, permit.r, permit.s]


@dataclass(frozen=True, kw_only=True)
class ContractOperationRequest(FromMnemonicMixin):
    private_key: str = field(repr=False)
    domain: ClassVar[str]

    def to_contract_call(self, client) -> ContractCallRequest:
        """Encode an unsigned call. Never sign or send a transaction."""
        raise NotImplementedError

    def _encode(
        self, client, abi: str, target: str, function: str, args: list, value_wei: int = 0
    ) -> ContractCallRequest:
        contract = client.web3.eth.contract(address=address(target), abi=client.abi.load(abi))
        return ContractCallRequest(
            contract=contract.address,
            private_key=self.private_key,
            data=contract.encode_abi(function, args=args),
            value_wei=uint(value_wei, "value_wei"),
        )


class ContractOperations:
    _operation_domain: str

    async def build_operation(self, request: ContractOperationRequest) -> TransactionDraft:
        """Build one of this service's additional typed operations without signing."""
        if (
            not isinstance(request, ContractOperationRequest)
            or request.domain != self._operation_domain
        ):
            raise TypeError("This request belongs to a different service")
        return await self._client.tx.build_contract_call(request.to_contract_call(self._client))

    async def estimate_fee_for_operation(
        self, request: ContractOperationRequest, *, exact: bool = False
    ) -> FeePreflight:
        """Estimate this exact call without signing, approvals, or broadcasting."""
        return await self._client.tx.calculate_fee(await self.build_operation(request), exact=exact)

    async def _send_operation(
        self, request, broadcast: bool, wait_receipt: bool, *, request_type
    ) -> TransactionResult:
        try:
            if type(request) is not request_type:
                raise TypeError(f"Expected {request_type.__name__} for this operation")
            draft = await self.build_operation(request)
            result = await self._client.tx.send_draft(
                draft, request.private_key, broadcast, wait_receipt
            )
            timestamp = getattr(request, "new_hold_timestamp", None)
            if timestamp is not None and result.success:
                from datetime import datetime, timezone

                try:
                    hold_time = datetime.fromtimestamp(timestamp, timezone.utc).isoformat()
                except (ValueError, OverflowError, OSError):
                    hold_time = None
                result = replace(result, hold_timestamp=timestamp, hold_time=hold_time)
            return result
        except Exception as exc:
            return _exception_failure(exc)
