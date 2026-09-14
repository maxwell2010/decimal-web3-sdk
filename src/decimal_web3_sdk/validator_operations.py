"""Validator registration and metadata management. No automatic approvals."""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from decimal import Decimal

from ._contract_operations import ContractOperationRequest, address, uint
from .erc20 import parse_units
from .staking_operations import StakingOperations
from .transactions import TransactionResult


@dataclass(frozen=True)
class ValidatorDescription:
    moniker: str
    identity: str = ""
    website: str = ""
    security_contact: str = ""
    details: str = ""


@dataclass(frozen=True)
class ValidatorMetadata:
    operator_address: str
    reward_address: str
    consensus_pubkey: str
    description: ValidatorDescription
    commission: str

    @classmethod
    def from_dict(cls, value: dict) -> "ValidatorMetadata":
        data = dict(value)
        data["description"] = ValidatorDescription(**data["description"])
        result = cls(**data)
        result.to_json()
        return result

    def to_json(self) -> str:
        address(self.operator_address)
        address(self.reward_address)
        if not isinstance(self.consensus_pubkey, str) or not self.consensus_pubkey.strip():
            raise ValueError("consensus_pubkey is required")
        if not isinstance(self.description, ValidatorDescription):
            raise TypeError("description must be ValidatorDescription")
        if any(not isinstance(value, str) for value in asdict(self.description).values()):
            raise TypeError("Validator description fields must be strings")
        if not self.description.moniker.strip():
            raise ValueError("Validator moniker is required")
        if not isinstance(self.commission, str):
            raise TypeError("commission must be an exact string")
        commission = Decimal(self.commission)
        if not commission.is_finite() or not 0 <= commission <= 100:
            raise ValueError("commission must be between 0 and 100")
        return json.dumps(asdict(self), ensure_ascii=False, separators=(",", ":"))


@dataclass(frozen=True)
class AddValidatorTokenRequest(ContractOperationRequest):
    metadata: ValidatorMetadata
    token: str
    amount_raw: int
    domain = "decimal"

    def to_contract_call(self, client):
        if not isinstance(self.metadata, ValidatorMetadata):
            raise TypeError("metadata must be ValidatorMetadata")
        return self._encode(
            client,
            "master_validator",
            client.config.contracts.master_validator,
            "addCandidate",
            [
                address(self.metadata.operator_address),
                self.metadata.to_json(),
                (address(self.token), uint(self.amount_raw, "amount_raw", positive=True)),
            ],
        )


@dataclass(frozen=True)
class AddValidatorDelRequest(ContractOperationRequest):
    metadata: ValidatorMetadata
    amount_del: Decimal | str | int
    domain = "decimal"

    def to_contract_call(self, client):
        if not isinstance(self.metadata, ValidatorMetadata):
            raise TypeError("metadata must be ValidatorMetadata")
        return self._encode(
            client,
            "master_validator",
            client.config.contracts.master_validator,
            "addCandidateDEL",
            [address(self.metadata.operator_address), self.metadata.to_json()],
            uint(parse_units(self.amount_del, 18), "amount_del", positive=True),
        )


@dataclass(frozen=True)
class RemoveValidatorRequest(ContractOperationRequest):
    validator: str
    domain = "decimal"

    def to_contract_call(self, client):
        return self._encode(
            client,
            "master_validator",
            client.config.contracts.master_validator,
            "removeValidator",
            [address(self.validator)],
        )


@dataclass(frozen=True)
class UpdateValidatorMetadataRequest(ContractOperationRequest):
    metadata: ValidatorMetadata
    domain = "decimal"

    def to_contract_call(self, client):
        if not isinstance(self.metadata, ValidatorMetadata):
            raise TypeError("metadata must be ValidatorMetadata")
        return self._encode(
            client,
            "master_validator",
            client.config.contracts.master_validator,
            "updateValidatorMeta",
            [address(self.metadata.operator_address), self.metadata.to_json()],
        )


class ValidatorOperations(StakingOperations):
    async def add_validator_token(
        self, request: AddValidatorTokenRequest, broadcast: bool = False, wait_receipt: bool = False
    ) -> TransactionResult:
        return await self._send_operation(
            request, broadcast, wait_receipt, request_type=AddValidatorTokenRequest
        )

    async def add_validator_del(
        self, request: AddValidatorDelRequest, broadcast: bool = False, wait_receipt: bool = False
    ) -> TransactionResult:
        return await self._send_operation(
            request, broadcast, wait_receipt, request_type=AddValidatorDelRequest
        )

    async def remove_validator(
        self, request: RemoveValidatorRequest, broadcast: bool = False, wait_receipt: bool = False
    ) -> TransactionResult:
        return await self._send_operation(
            request, broadcast, wait_receipt, request_type=RemoveValidatorRequest
        )

    async def update_validator_metadata(
        self,
        request: UpdateValidatorMetadataRequest,
        broadcast: bool = False,
        wait_receipt: bool = False,
    ) -> TransactionResult:
        return await self._send_operation(
            request, broadcast, wait_receipt, request_type=UpdateValidatorMetadataRequest
        )
