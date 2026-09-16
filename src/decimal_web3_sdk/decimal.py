from __future__ import annotations

from dataclasses import dataclass, field, replace
from datetime import datetime, timezone
from decimal import Decimal
from enum import IntEnum
from typing import Any

from web3 import Web3

from .erc20 import format_units, format_units_string, parse_units
from .transactions import (
    ContractCallRequest,
    Erc20ApproveRequest,
    FeePreflight,
    NativeTransferRequest,
    TransactionDraft,
    TransactionResult,
    _token_preflight_failure,
    user_message_from_error,
)
from .mnemonic import FromMnemonicMixin
from .validator_operations import ValidatorOperations
from .wallet import checksum, private_key_to_address


DELEGATION_ABI: list[dict[str, Any]] = [
    {
        "inputs": [{"internalType": "address", "name": "validator", "type": "address"}],
        "name": "delegateDEL",
        "outputs": [],
        "stateMutability": "payable",
        "type": "function",
    },
    {
        "inputs": [
            {"internalType": "address", "name": "validator", "type": "address"},
            {"internalType": "uint256", "name": "holdTimestamp", "type": "uint256"},
        ],
        "name": "delegateHoldDEL",
        "outputs": [],
        "stateMutability": "payable",
        "type": "function",
    },
    {
        "inputs": [
            {"internalType": "address", "name": "validator", "type": "address"},
            {"internalType": "address", "name": "token", "type": "address"},
            {"internalType": "uint256", "name": "amount", "type": "uint256"},
        ],
        "name": "delegate",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function",
    },
    {
        "inputs": [
            {"internalType": "address", "name": "validator", "type": "address"},
            {"internalType": "address", "name": "token", "type": "address"},
            {"internalType": "uint256", "name": "amount", "type": "uint256"},
            {"internalType": "uint256", "name": "holdTimestamp", "type": "uint256"},
        ],
        "name": "delegateHold",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function",
    },
    {
        "inputs": [
            {"internalType": "address", "name": "validator", "type": "address"},
            {"internalType": "address", "name": "token", "type": "address"},
            {"internalType": "uint256", "name": "amount", "type": "uint256"},
            {"internalType": "uint256", "name": "deadline", "type": "uint256"},
            {"internalType": "uint8", "name": "v", "type": "uint8"},
            {"internalType": "bytes32", "name": "r", "type": "bytes32"},
            {"internalType": "bytes32", "name": "s", "type": "bytes32"},
        ],
        "name": "delegateByPermit",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function",
    },
    {
        "inputs": [
            {"internalType": "address", "name": "validator", "type": "address"},
            {"internalType": "address", "name": "token", "type": "address"},
            {"internalType": "uint256", "name": "amount", "type": "uint256"},
            {"internalType": "uint256", "name": "holdTimestamp", "type": "uint256"},
            {"internalType": "uint256", "name": "deadline", "type": "uint256"},
            {"internalType": "uint8", "name": "v", "type": "uint8"},
            {"internalType": "bytes32", "name": "r", "type": "bytes32"},
            {"internalType": "bytes32", "name": "s", "type": "bytes32"},
        ],
        "name": "delegateHoldByPermit",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function",
    },
    {
        "inputs": [
            {"internalType": "address", "name": "validator", "type": "address"},
            {"internalType": "address", "name": "token", "type": "address"},
            {"internalType": "uint256", "name": "amount", "type": "uint256"},
        ],
        "name": "withdraw",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function",
    },
    {
        "inputs": [
            {"internalType": "address", "name": "validator", "type": "address"},
            {"internalType": "address", "name": "token", "type": "address"},
            {"internalType": "uint256", "name": "amount", "type": "uint256"},
            {"internalType": "uint256", "name": "holdTimestamp", "type": "uint256"},
        ],
        "name": "withdrawHold",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function",
    },
    {
        "inputs": [
            {"internalType": "address", "name": "validator", "type": "address"},
            {"internalType": "address", "name": "token", "type": "address"},
            {"internalType": "uint256", "name": "amount", "type": "uint256"},
            {"internalType": "address", "name": "newValidator", "type": "address"},
        ],
        "name": "transfer",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function",
    },
    {
        "inputs": [
            {"internalType": "address", "name": "validator", "type": "address"},
            {"internalType": "address", "name": "token", "type": "address"},
            {"internalType": "uint256", "name": "amount", "type": "uint256"},
            {"internalType": "uint256", "name": "holdTimestamp", "type": "uint256"},
            {"internalType": "address", "name": "newValidator", "type": "address"},
        ],
        "name": "transferHold",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function",
    },
    {
        "inputs": [
            {"internalType": "address", "name": "validator", "type": "address"},
            {"internalType": "address", "name": "token", "type": "address"},
            {"internalType": "uint256", "name": "amount", "type": "uint256"},
            {"internalType": "uint256", "name": "oldHoldTimestamp", "type": "uint256"},
            {"internalType": "uint256", "name": "newHoldTimestamp", "type": "uint256"},
        ],
        "name": "hold",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function",
    },
    {
        "inputs": [
            {"internalType": "address", "name": "validator", "type": "address"},
            {"internalType": "address", "name": "delegator", "type": "address"},
            {"internalType": "address", "name": "token", "type": "address"},
            {"internalType": "uint256", "name": "holdTimestamp", "type": "uint256"},
        ],
        "name": "resetHold",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function",
    },
    {
        "inputs": [
            {"internalType": "address", "name": "validator", "type": "address"},
            {"internalType": "address", "name": "delegator", "type": "address"},
            {"internalType": "uint256", "name": "holdTimestamp", "type": "uint256"},
        ],
        "name": "resetHoldDEL",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function",
    },
    {
        "inputs": [
            {"internalType": "address", "name": "validator", "type": "address"},
            {"internalType": "address", "name": "token", "type": "address"},
            {"internalType": "uint256", "name": "amount", "type": "uint256"},
            {"internalType": "uint256[]", "name": "holdTimestampsToReset", "type": "uint256[]"},
        ],
        "name": "withdrawWithReset",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function",
    },
    {
        "inputs": [
            {"internalType": "address", "name": "oldValidator", "type": "address"},
            {"internalType": "address", "name": "token", "type": "address"},
            {"internalType": "uint256", "name": "amount", "type": "uint256"},
            {"internalType": "address", "name": "newValidator", "type": "address"},
            {"internalType": "uint256[]", "name": "holdTimestampsToReset", "type": "uint256[]"},
        ],
        "name": "transferWithReset",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function",
    },
    {
        "inputs": [
            {"internalType": "address", "name": "validator", "type": "address"},
            {"internalType": "address", "name": "token", "type": "address"},
            {"internalType": "uint256", "name": "amount", "type": "uint256"},
            {"internalType": "uint256", "name": "newHoldTimestamp", "type": "uint256"},
            {"internalType": "uint256[]", "name": "holdTimestampsToReset", "type": "uint256[]"},
        ],
        "name": "holdWithReset",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function",
    },
    {
        "inputs": [
            {"internalType": "address", "name": "validator", "type": "address"},
            {"internalType": "address", "name": "delegator", "type": "address"},
            {"internalType": "address", "name": "token", "type": "address"},
        ],
        "name": "getStake",
        "outputs": [
            {
                "components": [
                    {"internalType": "address", "name": "validator", "type": "address"},
                    {"internalType": "address", "name": "delegator", "type": "address"},
                    {"internalType": "address", "name": "token", "type": "address"},
                    {"internalType": "uint256", "name": "amount", "type": "uint256"},
                    {"internalType": "uint256", "name": "tokenId", "type": "uint256"},
                    {"internalType": "uint8", "name": "tokenType", "type": "uint8"},
                    {"internalType": "uint256", "name": "holdTimestamp", "type": "uint256"},
                ],
                "internalType": "struct IDecimalDelegationCommon.Stake",
                "name": "",
                "type": "tuple",
            }
        ],
        "stateMutability": "view",
        "type": "function",
    },
    {
        "inputs": [
            {"internalType": "address", "name": "validator", "type": "address"},
            {"internalType": "address", "name": "delegator", "type": "address"},
            {"internalType": "address", "name": "token", "type": "address"},
            {"internalType": "uint256", "name": "holdTimestamp", "type": "uint256"},
        ],
        "name": "getHoldStake",
        "outputs": [
            {
                "components": [
                    {"internalType": "address", "name": "validator", "type": "address"},
                    {"internalType": "address", "name": "delegator", "type": "address"},
                    {"internalType": "address", "name": "token", "type": "address"},
                    {"internalType": "uint256", "name": "amount", "type": "uint256"},
                    {"internalType": "uint256", "name": "tokenId", "type": "uint256"},
                    {"internalType": "uint8", "name": "tokenType", "type": "uint8"},
                    {"internalType": "uint256", "name": "holdTimestamp", "type": "uint256"},
                ],
                "internalType": "struct IDecimalDelegationCommon.Stake",
                "name": "",
                "type": "tuple",
            }
        ],
        "stateMutability": "view",
        "type": "function",
    },
]


MULTICALL_ABI: list[dict[str, Any]] = [
    {
        "inputs": [
            {
                "components": [
                    {"internalType": "address", "name": "target", "type": "address"},
                    {"internalType": "uint256", "name": "value", "type": "uint256"},
                    {"internalType": "bytes", "name": "callData", "type": "bytes"},
                ],
                "internalType": "struct MultiCall.Call[]",
                "name": "calls",
                "type": "tuple[]",
            }
        ],
        "name": "aggregate",
        "outputs": [
            {"internalType": "uint256", "name": "blockNumber", "type": "uint256"},
            {"internalType": "bytes[]", "name": "returnData", "type": "bytes[]"},
        ],
        "stateMutability": "payable",
        "type": "function",
    }
]


MASTER_VALIDATOR_ABI: list[dict[str, Any]] = [
    {"inputs": [], "name": "pauseSelf", "outputs": [], "stateMutability": "nonpayable", "type": "function"},
    {"inputs": [], "name": "unpauseSelf", "outputs": [], "stateMutability": "nonpayable", "type": "function"},
    {
        "inputs": [{"internalType": "address", "name": "validator", "type": "address"}],
        "name": "pauseValidator",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function",
    },
    {
        "inputs": [{"internalType": "address", "name": "validator", "type": "address"}],
        "name": "unpauseValidator",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function",
    },
    {
        "inputs": [{"internalType": "address", "name": "validator", "type": "address"}],
        "name": "getValidatorStatus",
        "outputs": [{"internalType": "uint8", "name": "", "type": "uint8"}],
        "stateMutability": "view",
        "type": "function",
    },
    {
        "inputs": [{"internalType": "address", "name": "validator", "type": "address"}],
        "name": "isActive",
        "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
        "stateMutability": "view",
        "type": "function",
    },
    {
        "inputs": [{"internalType": "address", "name": "validator", "type": "address"}],
        "name": "isMember",
        "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
        "stateMutability": "view",
        "type": "function",
    },
]


@dataclass(frozen=True)
class DelegateDelRequest(FromMnemonicMixin):
    validator: str
    amount_del: Decimal | str | int
    private_key: str = field(repr=False)


@dataclass(frozen=True)
class HoldDelRequest(FromMnemonicMixin):
    validator: str
    amount_del: Decimal | str | int
    hold_timestamp: int
    private_key: str = field(repr=False)


@dataclass(frozen=True)
class UnbondDelRequest(FromMnemonicMixin):
    validator: str
    amount_del: Decimal | str | int
    private_key: str = field(repr=False)


@dataclass(frozen=True)
class WithdrawHoldDelRequest(FromMnemonicMixin):
    validator: str
    amount_del: Decimal | str | int
    hold_timestamp: int
    private_key: str = field(repr=False)


@dataclass(frozen=True)
class MultisendRecipient:
    to: str
    amount_del: Decimal | str | int


@dataclass(frozen=True)
class MultisendDelRequest(FromMnemonicMixin):
    recipients: list[MultisendRecipient]
    private_key: str = field(repr=False)
    memo: str | None = None


@dataclass(frozen=True)
class MultisendErc20Recipient:
    to: str
    amount: Decimal | str | int


@dataclass(frozen=True)
class MultisendErc20Request(FromMnemonicMixin):
    token: str
    recipients: list[MultisendErc20Recipient]
    private_key: str = field(repr=False)
    decimals: int | None = None
    memo: str | None = None
    auto_approve: bool = True
    prefer_permit: bool = True
    permit_deadline: int = 2**256 - 1


@dataclass(frozen=True)
class DelegateErc20Request(FromMnemonicMixin):
    token: str
    validator: str
    amount: Decimal | str | int
    private_key: str = field(repr=False)
    decimals: int | None = None
    auto_approve: bool = True
    prefer_permit: bool = True
    permit_deadline: int = 2**256 - 1


@dataclass(frozen=True)
class HoldErc20Request(FromMnemonicMixin):
    token: str
    validator: str
    amount: Decimal | str | int
    hold_timestamp: int
    private_key: str = field(repr=False)
    decimals: int | None = None
    auto_approve: bool = True
    prefer_permit: bool = True
    permit_deadline: int = 2**256 - 1


@dataclass(frozen=True)
class UnbondErc20Request(FromMnemonicMixin):
    token: str
    validator: str
    amount: Decimal | str | int
    private_key: str = field(repr=False)
    decimals: int | None = None


@dataclass(frozen=True)
class WithdrawHoldErc20Request(FromMnemonicMixin):
    token: str
    validator: str
    amount: Decimal | str | int
    hold_timestamp: int
    private_key: str = field(repr=False)
    decimals: int | None = None


@dataclass(frozen=True)
class TransferStakeErc20Request(FromMnemonicMixin):
    token: str
    validator: str
    new_validator: str
    amount: Decimal | str | int
    private_key: str = field(repr=False)
    decimals: int | None = None
    hold_timestamp: int | None = None


@dataclass(frozen=True)
class TransferStakeDelRequest(FromMnemonicMixin):
    validator: str
    new_validator: str
    amount_del: Decimal | str | int
    private_key: str = field(repr=False)
    hold_timestamp: int | None = None


@dataclass(frozen=True)
class StakeTokenToHoldRequest(FromMnemonicMixin):
    token: str
    validator: str
    amount: Decimal | str | int
    old_hold_timestamp: int
    new_hold_timestamp: int
    private_key: str = field(repr=False)
    decimals: int | None = None


@dataclass(frozen=True)
class ResetStakeHoldRequest(FromMnemonicMixin):
    validator: str
    delegator: str
    private_key: str = field(repr=False)
    hold_timestamp: int
    token: str | None = None


@dataclass(frozen=True)
class WithdrawStakeWithResetRequest(FromMnemonicMixin):
    token: str
    validator: str
    amount: Decimal | str | int
    hold_timestamps_to_reset: list[int]
    private_key: str = field(repr=False)
    decimals: int | None = None


@dataclass(frozen=True)
class WithdrawDelStakeWithResetRequest(FromMnemonicMixin):
    validator: str
    amount_del: Decimal | str | int
    hold_timestamps_to_reset: list[int]
    private_key: str = field(repr=False)


@dataclass(frozen=True)
class TransferStakeWithResetRequest(FromMnemonicMixin):
    token: str
    old_validator: str
    new_validator: str
    amount: Decimal | str | int
    hold_timestamps_to_reset: list[int]
    private_key: str = field(repr=False)
    decimals: int | None = None


@dataclass(frozen=True)
class TransferDelStakeWithResetRequest(FromMnemonicMixin):
    old_validator: str
    new_validator: str
    amount_del: Decimal | str | int
    hold_timestamps_to_reset: list[int]
    private_key: str = field(repr=False)


@dataclass(frozen=True)
class HoldStakeWithResetRequest(FromMnemonicMixin):
    token: str
    validator: str
    amount: Decimal | str | int
    new_hold_timestamp: int
    hold_timestamps_to_reset: list[int]
    private_key: str = field(repr=False)
    decimals: int | None = None


@dataclass(frozen=True)
class ValidatorSelfPauseRequest(FromMnemonicMixin):
    private_key: str = field(repr=False)


@dataclass(frozen=True)
class ValidatorPauseRequest(FromMnemonicMixin):
    validator: str
    private_key: str = field(repr=False)


class DelegationTokenType(IntEnum):
    UNKNOWN = 0
    DRC20 = 1
    DRC721 = 2
    DRC1155 = 3
    DEL = 4


@dataclass(frozen=True)
class DelegationStake:
    validator: str
    delegator: str
    token: str
    amount_raw: int
    token_id: int
    token_type: int
    hold_timestamp: int
    block_number: int | None = None

    @property
    def exists(self) -> bool:
        return self.amount_raw > 0

    @property
    def hold_time(self) -> str | None:
        if self.hold_timestamp <= 0:
            return None
        return _hold_time(self.hold_timestamp)

    @property
    def is_hold(self) -> bool:
        return self.hold_timestamp > 0

    @property
    def token_type_enum(self) -> DelegationTokenType:
        return DelegationTokenType(self.token_type)

    @property
    def is_native_del(self) -> bool:
        return self.token_type_enum is DelegationTokenType.DEL

    def is_matured(self, now_timestamp: int | None = None) -> bool:
        if not self.is_hold:
            return False
        now = (
            int(datetime.now(tz=timezone.utc).timestamp())
            if now_timestamp is None
            else int(now_timestamp)
        )
        return self.hold_timestamp <= now

    def amount_string(self, decimals: int = 18) -> str:
        return format_units_string(self.amount_raw, decimals)

    def amount(self, decimals: int = 18) -> Decimal:
        return format_units(self.amount_raw, decimals)

    def as_dict(self, decimals: int = 18) -> dict[str, object]:
        """Return a JSON-safe stake without exposing uint256 values as JSON numbers."""
        return {
            "validator": self.validator,
            "delegator": self.delegator,
            "token": self.token,
            "amount_raw": str(self.amount_raw),
            "amount": self.amount_string(decimals),
            "token_id": str(self.token_id),
            "token_type": int(self.token_type),
            "token_type_name": self.token_type_enum.name,
            "hold_timestamp": str(self.hold_timestamp),
            "hold_time": self.hold_time,
            "block_number": self.block_number,
            "exists": self.exists,
        }


@dataclass(frozen=True)
class DelegationStakeSnapshot:
    block_number: int
    regular: DelegationStake
    holds: tuple[DelegationStake, ...] = ()
    missing_hold_timestamps: tuple[int, ...] = ()

    @property
    def regular_amount_raw(self) -> int:
        return self.regular.amount_raw if self.regular.exists else 0

    @property
    def held_amount_raw(self) -> int:
        return sum(stake.amount_raw for stake in self.holds)

    @property
    def total_amount_raw(self) -> int:
        return self.regular_amount_raw + self.held_amount_raw

    def regular_amount(self, decimals: int = 18) -> Decimal:
        return format_units(self.regular_amount_raw, decimals)

    def held_amount(self, decimals: int = 18) -> Decimal:
        return format_units(self.held_amount_raw, decimals)

    def total_amount(self, decimals: int = 18) -> Decimal:
        return format_units(self.total_amount_raw, decimals)

    def matured_holds(self, now_timestamp: int | None = None) -> tuple[DelegationStake, ...]:
        return tuple(stake for stake in self.holds if stake.is_matured(now_timestamp))

    def as_dict(self, decimals: int = 18) -> dict[str, object]:
        return {
            "block_number": self.block_number,
            "regular_amount_raw": str(self.regular_amount_raw),
            "regular_amount": format_units_string(self.regular_amount_raw, decimals),
            "held_amount_raw": str(self.held_amount_raw),
            "held_amount": format_units_string(self.held_amount_raw, decimals),
            "total_amount_raw": str(self.total_amount_raw),
            "total_amount": format_units_string(self.total_amount_raw, decimals),
            "regular": self.regular.as_dict(decimals),
            "holds": [stake.as_dict(decimals) for stake in self.holds],
            "missing_hold_timestamps": [str(value) for value in self.missing_hold_timestamps],
        }


@dataclass(frozen=True)
class DecimalWorkflowResult:
    success: bool
    name: str
    steps: tuple[str, ...]
    expected_steps: int
    actual_steps: int
    extra_steps_required: bool
    primary: TransactionResult | None = None
    secondary: TransactionResult | None = None
    error: str | None = None
    user_message: str | None = None

    @property
    def requires_secondary_transaction(self) -> bool:
        return self.extra_steps_required

    @property
    def one_transaction(self) -> bool:
        if self.extra_steps_required:
            return False
        transaction_count = self.transaction_count
        if transaction_count:
            return transaction_count <= 1
        return self.actual_steps <= 1

    @property
    def transaction_count(self) -> int:
        return int(self.primary is not None) + int(self.secondary is not None)

    @property
    def total_fee_wei(self) -> int | None:
        fees = [
            item.fee_wei
            for item in (self.primary, self.secondary)
            if item is not None and item.fee_wei is not None
        ]
        if not fees:
            return None
        return sum(fees)

    @property
    def total_fee_del(self) -> Decimal | None:
        if self.total_fee_wei is None:
            return None
        return format_units(self.total_fee_wei, 18)

    @property
    def tx_hash(self) -> str | None:
        return self.primary.tx_hash if self.primary else None

    @property
    def hold_timestamp(self) -> int | None:
        return self.primary.hold_timestamp if self.primary else None

    @property
    def hold_time(self) -> str | None:
        return self.primary.hold_time if self.primary else None

    def __post_init__(self) -> None:
        if self.user_message is None:
            message = None
            if self.primary and self.primary.user_message:
                message = self.primary.user_message
            elif self.secondary and self.secondary.user_message:
                message = self.secondary.user_message
            else:
                message = user_message_from_error(self.error)
            object.__setattr__(self, "user_message", message)

    @property
    def gas(self) -> int | None:
        values = [item.gas for item in (self.secondary, self.primary) if item and item.gas is not None]
        return sum(values) if values else None

    @property
    def fee_wei(self) -> int | None:
        values = [item.fee_wei for item in (self.secondary, self.primary) if item and item.fee_wei is not None]
        return sum(values) if values else None

    @property
    def fee_del(self) -> Decimal | None:
        if self.fee_wei is None:
            return None
        return format_units(self.fee_wei, 18)


class DecimalService(ValidatorOperations):
    def __init__(self, client) -> None:
        self._client = client

    async def get_stake(
        self,
        validator: str,
        delegator: str,
        token: str,
        *,
        block_identifier: int | str | None = None,
    ) -> DelegationStake:
        validator_address = checksum(validator)
        delegator_address = checksum(delegator)
        token_address = checksum(token)
        def read(w3):
            call = self._delegation_contract(w3).functions.getStake(
                validator_address, delegator_address, token_address,
            )
            return call.call() if block_identifier is None else call.call(block_identifier=block_identifier)
        value = await self._client.rpc.call(read)
        return _delegation_stake(
            value,
            expected_validator=validator_address,
            expected_delegator=delegator_address,
            expected_token=token_address,
            expected_hold_timestamp=0,
            wdel=checksum(self._client.config.contracts.wdel),
            block_number=block_identifier if isinstance(block_identifier, int) else None,
        )

    async def get_hold_stake(
        self,
        validator: str,
        delegator: str,
        token: str,
        hold_timestamp: int,
        *,
        block_identifier: int | str | None = None,
    ) -> DelegationStake:
        hold_key = int(hold_timestamp)
        if hold_key <= 0:
            raise ValueError("hold_timestamp must be greater than zero")
        validator_address = checksum(validator)
        delegator_address = checksum(delegator)
        token_address = checksum(token)
        def read(w3):
            call = self._delegation_contract(w3).functions.getHoldStake(
                validator_address, delegator_address, token_address, hold_key,
            )
            return call.call() if block_identifier is None else call.call(block_identifier=block_identifier)
        value = await self._client.rpc.call(read)
        return _delegation_stake(
            value,
            expected_validator=validator_address,
            expected_delegator=delegator_address,
            expected_token=token_address,
            expected_hold_timestamp=hold_key,
            wdel=checksum(self._client.config.contracts.wdel),
            block_number=block_identifier if isinstance(block_identifier, int) else None,
        )

    async def get_stake_snapshot(
        self,
        validator: str,
        delegator: str,
        token: str,
        hold_timestamps: list[int] | tuple[int, ...] = (),
        *,
        block_number: int | None = None,
        max_hold_entries: int = 100,
    ) -> DelegationStakeSnapshot:
        """Read one regular stake and a bounded set of known hold keys at one block."""
        limit = min(max(1, int(max_hold_entries)), 100)
        hold_keys = tuple(dict.fromkeys(int(value) for value in hold_timestamps))
        if len(hold_keys) > limit:
            raise ValueError(f"At most {limit} hold timestamps can be read in one snapshot")
        if any(value <= 0 for value in hold_keys):
            raise ValueError("hold timestamps must be greater than zero")

        snapshot_block = (
            int(await self._client.block_number())
            if block_number is None
            else int(block_number)
        )
        regular = await self.get_stake(
            validator,
            delegator,
            token,
            block_identifier=snapshot_block,
        )
        holds: list[DelegationStake] = []
        missing: list[int] = []
        for hold_key in hold_keys:
            stake = await self.get_hold_stake(
                validator,
                delegator,
                token,
                hold_key,
                block_identifier=snapshot_block,
            )
            if stake.exists:
                holds.append(stake)
            else:
                missing.append(hold_key)
        return DelegationStakeSnapshot(
            block_number=snapshot_block,
            regular=regular,
            holds=tuple(holds),
            missing_hold_timestamps=tuple(missing),
        )

    async def delegate_del(
        self,
        request: DelegateDelRequest,
        broadcast: bool = False,
        wait_receipt: bool = False,
    ) -> TransactionResult:
        data = self._delegation_contract().functions.delegateDEL(
            checksum(request.validator)
        )._encode_transaction_data()
        return await self._send_contract(
            request.private_key,
            self._client.config.contracts.delegation,
            data,
            _del_to_wei(request.amount_del),
            broadcast,
            wait_receipt,
        )

    async def estimate_fee_for_delegate_del(
        self,
        request: DelegateDelRequest,
        *,
        exact: bool = False,
    ) -> FeePreflight:
        data = self._delegation_contract().functions.delegateDEL(
            checksum(request.validator)
        )._encode_transaction_data()
        return await self._estimate_delegation_call(
            request.private_key,
            data,
            value_wei=_del_to_wei(request.amount_del),
            exact=exact,
        )

    async def hold_del(
        self,
        request: HoldDelRequest,
        broadcast: bool = False,
        wait_receipt: bool = False,
    ) -> TransactionResult:
        data = self._delegation_contract().functions.delegateHoldDEL(
            checksum(request.validator),
            int(request.hold_timestamp),
        )._encode_transaction_data()
        result = await self._send_contract(
            request.private_key,
            self._client.config.contracts.delegation,
            data,
            _del_to_wei(request.amount_del),
            broadcast,
            wait_receipt,
        )
        return _with_hold_schedule(result, request.hold_timestamp)

    async def estimate_fee_for_hold_del(
        self,
        request: HoldDelRequest,
        *,
        exact: bool = False,
    ) -> FeePreflight:
        data = self._delegation_contract().functions.delegateHoldDEL(
            checksum(request.validator),
            int(request.hold_timestamp),
        )._encode_transaction_data()
        return await self._estimate_delegation_call(
            request.private_key,
            data,
            value_wei=_del_to_wei(request.amount_del),
            exact=exact,
        )

    async def unbond_del(
        self,
        request: UnbondDelRequest,
        broadcast: bool = False,
        wait_receipt: bool = False,
    ) -> TransactionResult:
        data = self._delegation_contract().functions.withdraw(
            checksum(request.validator),
            checksum(self._client.config.contracts.wdel),
            _del_to_wei(request.amount_del),
        )._encode_transaction_data()
        return await self._send_contract(
            request.private_key,
            self._client.config.contracts.delegation,
            data,
            0,
            broadcast,
            wait_receipt,
        )

    async def withdraw_hold_del(
        self,
        request: WithdrawHoldDelRequest,
        broadcast: bool = False,
        wait_receipt: bool = False,
    ) -> TransactionResult:
        data = self._delegation_contract().functions.withdrawHold(
            checksum(request.validator),
            checksum(self._client.config.contracts.wdel),
            _del_to_wei(request.amount_del),
            int(request.hold_timestamp),
        )._encode_transaction_data()
        return await self._send_contract(
            request.private_key,
            self._client.config.contracts.delegation,
            data,
            0,
            broadcast,
            wait_receipt,
        )

    async def estimate_fee_for_withdraw_hold_del(
        self,
        request: WithdrawHoldDelRequest,
        *,
        exact: bool = False,
    ) -> FeePreflight:
        data = self._delegation_contract().functions.withdrawHold(
            checksum(request.validator),
            checksum(self._client.config.contracts.wdel),
            _del_to_wei(request.amount_del),
            int(request.hold_timestamp),
        )._encode_transaction_data()
        return await self._estimate_delegation_call(request.private_key, data, exact=exact)

    async def estimate_fee_for_unbond_del(self, request: UnbondDelRequest, *, exact: bool = False) -> FeePreflight:
        data = self._delegation_contract().functions.withdraw(
            checksum(request.validator),
            checksum(self._client.config.contracts.wdel),
            _del_to_wei(request.amount_del),
        )._encode_transaction_data()
        draft = await self._client.tx.build_contract_call(
            ContractCallRequest(
                contract=self._client.config.contracts.delegation,
                private_key=request.private_key,
                data=data,
            )
        )
        return await self._client.tx.calculate_fee(draft, exact=exact)

    async def multisend_del(
        self,
        request: MultisendDelRequest,
        broadcast: bool = False,
        wait_receipt: bool = False,
    ) -> TransactionResult:
        if not request.recipients:
            return TransactionResult(success=False, error="At least one recipient is required")

        if len(request.recipients) == 1:
            recipient = request.recipients[0]
            return await self._client.tx.send_del(
                NativeTransferRequest(
                    to=recipient.to,
                    amount_del=recipient.amount_del,
                    private_key=request.private_key,
                    memo=request.memo,
                ),
                broadcast=broadcast,
                wait_receipt=wait_receipt,
            )

        draft = await self.build_multisend_del(request)
        return await self._client.tx.send_draft(draft, request.private_key, broadcast, wait_receipt)

    async def build_multisend_del(self, request: MultisendDelRequest) -> TransactionDraft:
        if not request.recipients:
            raise ValueError("At least one recipient is required")

        if len(request.recipients) == 1:
            recipient = request.recipients[0]
            return await self._client.tx.build_native_transfer(
                NativeTransferRequest(
                    to=recipient.to,
                    amount_del=recipient.amount_del,
                    private_key=request.private_key,
                    memo=request.memo,
                )
            )

        calls: list[tuple[str, int, bytes]] = []
        total_value = 0
        for recipient in request.recipients:
            value = _del_to_wei(recipient.amount_del)
            total_value += value
            calls.append((checksum(recipient.to), value, b""))
        if request.memo:
            calls.append(
                (
                    "0x0000000000000000000000000000000000000000",
                    0,
                    request.memo.encode("utf-8"),
                )
            )

        data = self._multicall_contract().functions.aggregate(calls)._encode_transaction_data()
        return await self._client.tx.build_contract_call(
            ContractCallRequest(
                contract=self._client.config.contracts.multicall,
                private_key=request.private_key,
                data=data,
                value_wei=total_value,
            )
        )

    async def estimate_fee_for_multisend_del(self, request: MultisendDelRequest, *, exact: bool = False) -> FeePreflight:
        draft = await self.build_multisend_del(request)
        return await self._client.tx.calculate_fee(draft, exact=exact)

    async def multisend_erc20(
        self,
        request: MultisendErc20Request,
        broadcast: bool = False,
        wait_receipt: bool = False,
    ) -> DecimalWorkflowResult:
        try:
            if not request.recipients:
                return DecimalWorkflowResult(
                    success=False,
                    name="multisend_erc20",
                    steps=(),
                    expected_steps=1,
                    actual_steps=0,
                    extra_steps_required=False,
                    error="At least one recipient is required",
                )
            decimals = request.decimals
            if decimals is None:
                decimals = (await self._client.erc20.info(request.token)).decimals
            owner = private_key_to_address(request.private_key)
            amounts = [_parse_units(item.amount, decimals) for item in request.recipients]
            total_raw = sum(amounts)
            balance = await self._client.erc20.balance(request.token, owner)
            if int(balance.raw) < total_raw:
                failure = _token_preflight_failure(int(balance.raw), total_raw)
                return DecimalWorkflowResult(
                    success=False,
                    name="multisend_erc20",
                    steps=("token_balance_preflight",),
                    expected_steps=1,
                    actual_steps=0,
                    extra_steps_required=False,
                    primary=failure,
                    error=failure.error,
                )

            spender = self._client.config.contracts.multicall
            calls: list[tuple[str, int, bytes]] = []
            steps: list[str] = []
            approve_result: TransactionResult | None = None
            allowance = await self._client.erc20.allowance(request.token, owner, spender)
            if allowance < total_raw:
                if request.prefer_permit:
                    permit = await self._client.erc20.permit_signature(
                        request.token,
                        owner,
                        spender,
                        total_raw,
                        request.permit_deadline,
                        request.private_key,
                    )
                    if permit is not None:
                        permit_data = self._client.erc20.build_permit_data(
                            request.token, owner, spender, total_raw, permit
                        )
                        calls.append((checksum(request.token), 0, bytes.fromhex(permit_data[2:])))
                        steps.append("permit_erc20")
                if not steps:
                    if not request.auto_approve:
                        return DecimalWorkflowResult(
                            success=False,
                            name="multisend_erc20",
                            steps=("approve_required",),
                            expected_steps=1,
                            actual_steps=0,
                            extra_steps_required=True,
                            error=f"ERC20 allowance is insufficient: allowance_raw={allowance}, required_raw={total_raw}",
                        )
                    approve_result = await self._client.tx.approve_erc20(
                        Erc20ApproveRequest(
                            token=request.token,
                            spender=spender,
                            amount=format_units(total_raw, decimals),
                            private_key=request.private_key,
                            decimals=decimals,
                        ),
                        broadcast=broadcast,
                        wait_receipt=wait_receipt,
                    )
                    steps.append("approve_erc20")
                    if not approve_result.success:
                        return DecimalWorkflowResult(
                            success=False,
                            name="multisend_erc20",
                            steps=tuple(steps),
                            expected_steps=1,
                            actual_steps=len(steps),
                            extra_steps_required=True,
                            secondary=approve_result,
                            error=approve_result.error,
                        )

            for recipient, amount_raw in zip(request.recipients, amounts):
                data = self._client.erc20.build_transfer_from_data(
                    request.token, owner, recipient.to, amount_raw
                )
                calls.append((checksum(request.token), 0, bytes.fromhex(data[2:])))
            if request.memo:
                calls.append(
                    (
                        "0x0000000000000000000000000000000000000000",
                        0,
                        request.memo.encode("utf-8"),
                    )
                )

            data = self._multicall_contract().functions.aggregate(calls)._encode_transaction_data()
            result = await self._send_contract(
                request.private_key,
                self._client.config.contracts.multicall,
                data,
                0,
                broadcast,
                wait_receipt,
            )
            steps.append("multisend_erc20")
            return DecimalWorkflowResult(
                success=result.success,
                name="multisend_erc20",
                steps=tuple(steps),
                expected_steps=1,
                actual_steps=len(steps),
                extra_steps_required=len(steps) > 1 and "permit_erc20" not in steps,
                primary=result,
                secondary=approve_result,
                error=result.error,
            )
        except Exception as exc:
            return _workflow_exception("multisend_erc20", exc)

    async def delegate_erc20(
        self,
        request: DelegateErc20Request,
        broadcast: bool = False,
        wait_receipt: bool = False,
    ) -> DecimalWorkflowResult:
        return await self._erc20_stake_with_allowance(
            name="delegate_erc20",
            token=request.token,
            validator=request.validator,
            amount=request.amount,
            private_key=request.private_key,
            decimals=request.decimals,
            auto_approve=request.auto_approve,
            prefer_permit=request.prefer_permit,
            permit_deadline=request.permit_deadline,
            broadcast=broadcast,
            wait_receipt=wait_receipt,
            hold_timestamp=None,
        )

    async def hold_erc20(
        self,
        request: HoldErc20Request,
        broadcast: bool = False,
        wait_receipt: bool = False,
    ) -> DecimalWorkflowResult:
        return await self._erc20_stake_with_allowance(
            name="hold_erc20",
            token=request.token,
            validator=request.validator,
            amount=request.amount,
            private_key=request.private_key,
            decimals=request.decimals,
            auto_approve=request.auto_approve,
            prefer_permit=request.prefer_permit,
            permit_deadline=request.permit_deadline,
            broadcast=broadcast,
            wait_receipt=wait_receipt,
            hold_timestamp=request.hold_timestamp,
        )

    async def unbond_erc20(
        self,
        request: UnbondErc20Request,
        broadcast: bool = False,
        wait_receipt: bool = False,
    ) -> DecimalWorkflowResult:
        try:
            decimals = request.decimals
            if decimals is None:
                decimals = (await self._client.erc20.info(request.token)).decimals
            amount_raw = _parse_units(request.amount, decimals)
            data = self._delegation_contract().functions.withdraw(
                checksum(request.validator),
                checksum(request.token),
                amount_raw,
            )._encode_transaction_data()
            result = await self._send_contract(
                request.private_key,
                self._client.config.contracts.delegation,
                data,
                0,
                broadcast,
                wait_receipt,
            )
            return DecimalWorkflowResult(
                success=result.success,
                name="unbond_erc20",
                steps=("unbond_erc20",),
                expected_steps=1,
                actual_steps=1,
                extra_steps_required=False,
                primary=result,
                error=result.error,
            )
        except Exception as exc:
            return _workflow_exception("unbond_erc20", exc)

    async def estimate_fee_for_unbond_erc20(self, request: UnbondErc20Request, *, exact: bool = False) -> FeePreflight:
        decimals = request.decimals
        if decimals is None:
            decimals = (await self._client.erc20.info(request.token)).decimals
        amount_raw = _parse_units(request.amount, decimals)
        data = self._delegation_contract().functions.withdraw(
            checksum(request.validator),
            checksum(request.token),
            amount_raw,
        )._encode_transaction_data()
        draft = await self._client.tx.build_contract_call(
            ContractCallRequest(
                contract=self._client.config.contracts.delegation,
                private_key=request.private_key,
                data=data,
            )
        )
        return await self._client.tx.calculate_fee(draft, exact=exact)

    async def withdraw_hold_erc20(
        self,
        request: WithdrawHoldErc20Request,
        broadcast: bool = False,
        wait_receipt: bool = False,
    ) -> DecimalWorkflowResult:
        try:
            decimals = request.decimals
            if decimals is None:
                decimals = (await self._client.erc20.info(request.token)).decimals
            amount_raw = _parse_units(request.amount, decimals)
            data = self._delegation_contract().functions.withdrawHold(
                checksum(request.validator),
                checksum(request.token),
                amount_raw,
                int(request.hold_timestamp),
            )._encode_transaction_data()
            result = await self._send_contract(
                request.private_key,
                self._client.config.contracts.delegation,
                data,
                0,
                broadcast,
                wait_receipt,
            )
            return DecimalWorkflowResult(
                success=result.success,
                name="withdraw_hold_erc20",
                steps=("withdraw_hold_erc20",),
                expected_steps=1,
                actual_steps=1,
                extra_steps_required=False,
                primary=result,
                error=result.error,
            )
        except Exception as exc:
            return _workflow_exception("withdraw_hold_erc20", exc)

    async def estimate_fee_for_withdraw_hold_erc20(
        self,
        request: WithdrawHoldErc20Request,
        *,
        exact: bool = False,
    ) -> FeePreflight:
        amount_raw = await self._erc20_amount_raw(request.token, request.amount, request.decimals)
        data = self._delegation_contract().functions.withdrawHold(
            checksum(request.validator),
            checksum(request.token),
            amount_raw,
            int(request.hold_timestamp),
        )._encode_transaction_data()
        return await self._estimate_delegation_call(request.private_key, data, exact=exact)

    async def transfer_stake_erc20(
        self,
        request: TransferStakeErc20Request,
        broadcast: bool = False,
        wait_receipt: bool = False,
    ) -> DecimalWorkflowResult:
        try:
            data = await self._transfer_stake_erc20_data(request)
            step = "transfer_hold_stake_erc20" if request.hold_timestamp is not None else "transfer_stake_erc20"
            return await self._single_step_workflow(step, request.private_key, data, broadcast, wait_receipt)
        except Exception as exc:
            return _workflow_exception("transfer_stake_erc20", exc)

    async def estimate_fee_for_transfer_stake_erc20(
        self,
        request: TransferStakeErc20Request,
        *,
        exact: bool = False,
    ) -> FeePreflight:
        return await self._estimate_delegation_call(
            request.private_key,
            await self._transfer_stake_erc20_data(request),
            exact=exact,
        )

    async def transfer_stake_del(
        self,
        request: TransferStakeDelRequest,
        broadcast: bool = False,
        wait_receipt: bool = False,
    ) -> DecimalWorkflowResult:
        try:
            data = self._transfer_stake_del_data(request)
            step = "transfer_hold_stake_del" if request.hold_timestamp is not None else "transfer_stake_del"
            return await self._single_step_workflow(step, request.private_key, data, broadcast, wait_receipt)
        except Exception as exc:
            return _workflow_exception("transfer_stake_del", exc)

    async def estimate_fee_for_transfer_stake_del(
        self,
        request: TransferStakeDelRequest,
        *,
        exact: bool = False,
    ) -> FeePreflight:
        return await self._estimate_delegation_call(
            request.private_key,
            self._transfer_stake_del_data(request),
            exact=exact,
        )

    async def stake_token_to_hold(
        self,
        request: StakeTokenToHoldRequest,
        broadcast: bool = False,
        wait_receipt: bool = False,
    ) -> DecimalWorkflowResult:
        try:
            amount_raw = await self._erc20_amount_raw(request.token, request.amount, request.decimals)
            data = self._delegation_contract().functions.hold(
                checksum(request.validator),
                checksum(request.token),
                amount_raw,
                int(request.old_hold_timestamp),
                int(request.new_hold_timestamp),
            )._encode_transaction_data()
            result = await self._single_step_workflow(
                "stake_token_to_hold",
                request.private_key,
                data,
                broadcast,
                wait_receipt,
            )
            return _workflow_with_hold_schedule(result, request.new_hold_timestamp)
        except Exception as exc:
            return _workflow_exception("stake_token_to_hold", exc)

    async def reset_stake_hold(
        self,
        request: ResetStakeHoldRequest,
        broadcast: bool = False,
        wait_receipt: bool = False,
    ) -> DecimalWorkflowResult:
        try:
            contract = self._delegation_contract()
            if request.token is None:
                data = contract.functions.resetHoldDEL(
                    checksum(request.validator),
                    checksum(request.delegator),
                    int(request.hold_timestamp),
                )._encode_transaction_data()
                step = "reset_stake_hold_del"
            else:
                data = contract.functions.resetHold(
                    checksum(request.validator),
                    checksum(request.delegator),
                    checksum(request.token),
                    int(request.hold_timestamp),
                )._encode_transaction_data()
                step = "reset_stake_hold_erc20"
            return await self._single_step_workflow(step, request.private_key, data, broadcast, wait_receipt)
        except Exception as exc:
            return _workflow_exception("reset_stake_hold", exc)

    async def withdraw_stake_with_reset(
        self,
        request: WithdrawStakeWithResetRequest,
        broadcast: bool = False,
        wait_receipt: bool = False,
    ) -> DecimalWorkflowResult:
        try:
            amount_raw = await self._erc20_amount_raw(request.token, request.amount, request.decimals)
            data = self._delegation_contract().functions.withdrawWithReset(
                checksum(request.validator),
                checksum(request.token),
                amount_raw,
                [int(item) for item in request.hold_timestamps_to_reset],
            )._encode_transaction_data()
            return await self._single_step_workflow("withdraw_stake_with_reset", request.private_key, data, broadcast, wait_receipt)
        except Exception as exc:
            return _workflow_exception("withdraw_stake_with_reset", exc)

    async def estimate_fee_for_withdraw_stake_with_reset(
        self,
        request: WithdrawStakeWithResetRequest,
        *,
        exact: bool = False,
    ) -> FeePreflight:
        amount_raw = await self._erc20_amount_raw(request.token, request.amount, request.decimals)
        data = self._delegation_contract().functions.withdrawWithReset(
            checksum(request.validator),
            checksum(request.token),
            amount_raw,
            [int(item) for item in request.hold_timestamps_to_reset],
        )._encode_transaction_data()
        return await self._estimate_delegation_call(request.private_key, data, exact=exact)

    async def withdraw_del_stake_with_reset(
        self,
        request: WithdrawDelStakeWithResetRequest,
        broadcast: bool = False,
        wait_receipt: bool = False,
    ) -> DecimalWorkflowResult:
        try:
            data = self._delegation_contract().functions.withdrawWithReset(
                checksum(request.validator),
                checksum(self._client.config.contracts.wdel),
                _del_to_wei(request.amount_del),
                [int(item) for item in request.hold_timestamps_to_reset],
            )._encode_transaction_data()
            return await self._single_step_workflow(
                "withdraw_del_stake_with_reset",
                request.private_key,
                data,
                broadcast,
                wait_receipt,
            )
        except Exception as exc:
            return _workflow_exception("withdraw_del_stake_with_reset", exc)

    async def estimate_fee_for_withdraw_del_stake_with_reset(
        self,
        request: WithdrawDelStakeWithResetRequest,
        *,
        exact: bool = False,
    ) -> FeePreflight:
        data = self._delegation_contract().functions.withdrawWithReset(
            checksum(request.validator),
            checksum(self._client.config.contracts.wdel),
            _del_to_wei(request.amount_del),
            [int(item) for item in request.hold_timestamps_to_reset],
        )._encode_transaction_data()
        draft = await self._client.tx.build_contract_call(
            ContractCallRequest(
                contract=self._client.config.contracts.delegation,
                private_key=request.private_key,
                data=data,
            )
        )
        return await self._client.tx.calculate_fee(draft, exact=exact)

    async def transfer_stake_with_reset(
        self,
        request: TransferStakeWithResetRequest,
        broadcast: bool = False,
        wait_receipt: bool = False,
    ) -> DecimalWorkflowResult:
        try:
            amount_raw = await self._erc20_amount_raw(request.token, request.amount, request.decimals)
            data = self._delegation_contract().functions.transferWithReset(
                checksum(request.old_validator),
                checksum(request.token),
                amount_raw,
                checksum(request.new_validator),
                [int(item) for item in request.hold_timestamps_to_reset],
            )._encode_transaction_data()
            return await self._single_step_workflow("transfer_stake_with_reset", request.private_key, data, broadcast, wait_receipt)
        except Exception as exc:
            return _workflow_exception("transfer_stake_with_reset", exc)

    async def estimate_fee_for_transfer_stake_with_reset(
        self,
        request: TransferStakeWithResetRequest,
        *,
        exact: bool = False,
    ) -> FeePreflight:
        amount_raw = await self._erc20_amount_raw(request.token, request.amount, request.decimals)
        data = self._delegation_contract().functions.transferWithReset(
            checksum(request.old_validator),
            checksum(request.token),
            amount_raw,
            checksum(request.new_validator),
            [int(item) for item in request.hold_timestamps_to_reset],
        )._encode_transaction_data()
        return await self._estimate_delegation_call(request.private_key, data, exact=exact)

    async def transfer_del_stake_with_reset(
        self,
        request: TransferDelStakeWithResetRequest,
        broadcast: bool = False,
        wait_receipt: bool = False,
    ) -> DecimalWorkflowResult:
        try:
            data = self._transfer_del_stake_with_reset_data(request)
            return await self._single_step_workflow(
                "transfer_del_stake_with_reset",
                request.private_key,
                data,
                broadcast,
                wait_receipt,
            )
        except Exception as exc:
            return _workflow_exception("transfer_del_stake_with_reset", exc)

    async def estimate_fee_for_transfer_del_stake_with_reset(
        self,
        request: TransferDelStakeWithResetRequest,
        *,
        exact: bool = False,
    ) -> FeePreflight:
        return await self._estimate_delegation_call(
            request.private_key,
            self._transfer_del_stake_with_reset_data(request),
            exact=exact,
        )

    async def hold_stake_with_reset(
        self,
        request: HoldStakeWithResetRequest,
        broadcast: bool = False,
        wait_receipt: bool = False,
    ) -> DecimalWorkflowResult:
        try:
            amount_raw = await self._erc20_amount_raw(request.token, request.amount, request.decimals)
            data = self._delegation_contract().functions.holdWithReset(
                checksum(request.validator),
                checksum(request.token),
                amount_raw,
                int(request.new_hold_timestamp),
                [int(item) for item in request.hold_timestamps_to_reset],
            )._encode_transaction_data()
            result = await self._single_step_workflow(
                "hold_stake_with_reset",
                request.private_key,
                data,
                broadcast,
                wait_receipt,
            )
            return _workflow_with_hold_schedule(result, request.new_hold_timestamp)
        except Exception as exc:
            return _workflow_exception("hold_stake_with_reset", exc)

    async def pause_self_validator(
        self,
        request: ValidatorSelfPauseRequest,
        broadcast: bool = False,
        wait_receipt: bool = False,
    ) -> DecimalWorkflowResult:
        try:
            data = self._master_validator_contract().functions.pauseSelf()._encode_transaction_data()
            return await self._single_contract_workflow(
                "pause_self_validator",
                self._client.config.contracts.master_validator,
                request.private_key,
                data,
                broadcast,
                wait_receipt,
            )
        except Exception as exc:
            return _workflow_exception("pause_self_validator", exc)

    async def unpause_self_validator(
        self,
        request: ValidatorSelfPauseRequest,
        broadcast: bool = False,
        wait_receipt: bool = False,
    ) -> DecimalWorkflowResult:
        try:
            data = self._master_validator_contract().functions.unpauseSelf()._encode_transaction_data()
            return await self._single_contract_workflow(
                "unpause_self_validator",
                self._client.config.contracts.master_validator,
                request.private_key,
                data,
                broadcast,
                wait_receipt,
            )
        except Exception as exc:
            return _workflow_exception("unpause_self_validator", exc)

    async def pause_validator(
        self,
        request: ValidatorPauseRequest,
        broadcast: bool = False,
        wait_receipt: bool = False,
    ) -> DecimalWorkflowResult:
        try:
            data = self._master_validator_contract().functions.pauseValidator(
                checksum(request.validator)
            )._encode_transaction_data()
            return await self._single_contract_workflow(
                "pause_validator",
                self._client.config.contracts.master_validator,
                request.private_key,
                data,
                broadcast,
                wait_receipt,
            )
        except Exception as exc:
            return _workflow_exception("pause_validator", exc)

    async def unpause_validator(
        self,
        request: ValidatorPauseRequest,
        broadcast: bool = False,
        wait_receipt: bool = False,
    ) -> DecimalWorkflowResult:
        try:
            data = self._master_validator_contract().functions.unpauseValidator(
                checksum(request.validator)
            )._encode_transaction_data()
            return await self._single_contract_workflow(
                "unpause_validator",
                self._client.config.contracts.master_validator,
                request.private_key,
                data,
                broadcast,
                wait_receipt,
            )
        except Exception as exc:
            return _workflow_exception("unpause_validator", exc)

    async def validator_status(self, validator: str) -> int:
        return await self._client.rpc.call(
            lambda w3: int(self._master_validator_contract(w3).functions.getValidatorStatus(checksum(validator)).call())
        )

    async def validator_is_active(self, validator: str) -> bool:
        return await self._client.rpc.call(
            lambda w3: bool(self._master_validator_contract(w3).functions.isActive(checksum(validator)).call())
        )

    async def validator_is_member(self, validator: str) -> bool:
        return await self._client.rpc.call(
            lambda w3: bool(self._master_validator_contract(w3).functions.isMember(checksum(validator)).call())
        )

    async def _erc20_stake_with_allowance(
        self,
        name: str,
        token: str,
        validator: str,
        amount: Decimal | str | int,
        private_key: str,
        decimals: int | None,
        auto_approve: bool,
        prefer_permit: bool,
        permit_deadline: int,
        broadcast: bool,
        wait_receipt: bool,
        hold_timestamp: int | None = None,
    ) -> DecimalWorkflowResult:
        try:
            if decimals is None:
                decimals = (await self._client.erc20.info(token)).decimals
            amount_raw = _parse_units(amount, decimals)
            owner = private_key_to_address(private_key)
            balance = await self._client.erc20.balance(token, owner)
            if int(balance.raw) < amount_raw:
                failure = _token_preflight_failure(int(balance.raw), amount_raw)
                return DecimalWorkflowResult(
                    success=False,
                    name=name,
                    steps=("token_balance_preflight",),
                    expected_steps=1,
                    actual_steps=0,
                    extra_steps_required=False,
                    primary=failure,
                    error=failure.error,
                )

            spender = self._client.config.contracts.delegation
            allowance = await self._client.erc20.allowance(token, owner, spender)
            approve_result: TransactionResult | None = None
            steps: list[str] = []
            if allowance < amount_raw:
                if prefer_permit:
                    permit = await self._client.erc20.permit_signature(
                        token,
                        owner,
                        self._client.config.contracts.delegation,
                        amount_raw,
                        permit_deadline,
                        private_key,
                    )
                    if permit is not None:
                        if hold_timestamp is None:
                            data = self._delegation_contract().functions.delegateByPermit(
                                checksum(validator),
                                checksum(token),
                                amount_raw,
                                permit.deadline,
                                permit.v,
                                permit.r,
                                permit.s,
                            )._encode_transaction_data()
                            step = "delegate_erc20_by_permit"
                        else:
                            data = self._delegation_contract().functions.delegateHoldByPermit(
                                checksum(validator),
                                checksum(token),
                                amount_raw,
                                int(hold_timestamp),
                                permit.deadline,
                                permit.v,
                                permit.r,
                                permit.s,
                            )._encode_transaction_data()
                            step = "hold_erc20_by_permit"
                        result = await self._send_contract(
                            private_key,
                            self._client.config.contracts.delegation,
                            data,
                            0,
                            broadcast,
                            wait_receipt,
                        )
                        if hold_timestamp is not None:
                            result = _with_hold_schedule(result, hold_timestamp)
                        return DecimalWorkflowResult(
                            success=result.success,
                            name=name,
                            steps=(step,),
                            expected_steps=1,
                            actual_steps=1,
                            extra_steps_required=False,
                            primary=result,
                            error=result.error,
                        )
                if not auto_approve:
                    return DecimalWorkflowResult(
                        success=False,
                        name=name,
                        steps=("approve_required",),
                        expected_steps=1,
                        actual_steps=0,
                        extra_steps_required=True,
                        error=f"ERC20 allowance is insufficient: allowance_raw={allowance}, required_raw={amount_raw}",
                    )
                approve_result = await self._client.tx.approve_erc20(
                    Erc20ApproveRequest(
                        token=token,
                        spender=spender,
                        amount=amount,
                        private_key=private_key,
                        decimals=decimals,
                    ),
                    broadcast=broadcast,
                    wait_receipt=wait_receipt,
                )
                steps.append("approve_erc20")
                if not approve_result.success:
                    return DecimalWorkflowResult(
                        success=False,
                        name=name,
                        steps=tuple(steps),
                        expected_steps=1,
                        actual_steps=len(steps),
                        extra_steps_required=True,
                        secondary=approve_result,
                        error=approve_result.error,
                    )

            if hold_timestamp is None:
                data = self._delegation_contract().functions.delegate(
                    checksum(validator),
                    checksum(token),
                    amount_raw,
                )._encode_transaction_data()
                step = "delegate_erc20"
            else:
                data = self._delegation_contract().functions.delegateHold(
                    checksum(validator),
                    checksum(token),
                    amount_raw,
                    int(hold_timestamp),
                )._encode_transaction_data()
                step = "hold_erc20"
            result = await self._send_contract(
                private_key,
                self._client.config.contracts.delegation,
                data,
                0,
                broadcast,
                wait_receipt,
            )
            if hold_timestamp is not None:
                result = _with_hold_schedule(result, hold_timestamp)
            steps.append(step)
            return DecimalWorkflowResult(
                success=result.success,
                name=name,
                steps=tuple(steps),
                expected_steps=1,
                actual_steps=len(steps),
                extra_steps_required=len(steps) > 1,
                primary=result,
                secondary=approve_result,
                error=result.error,
            )
        except Exception as exc:
            return _workflow_exception(name, exc)

    async def _erc20_amount_raw(
        self,
        token: str,
        amount: Decimal | str | int,
        decimals: int | None,
    ) -> int:
        if decimals is None:
            decimals = (await self._client.erc20.info(token)).decimals
        return _parse_units(amount, decimals)

    async def _transfer_stake_erc20_data(self, request: TransferStakeErc20Request) -> str:
        amount_raw = await self._erc20_amount_raw(request.token, request.amount, request.decimals)
        contract = self._delegation_contract()
        if request.hold_timestamp is None:
            return contract.functions.transfer(
                checksum(request.validator),
                checksum(request.token),
                amount_raw,
                checksum(request.new_validator),
            )._encode_transaction_data()
        return contract.functions.transferHold(
            checksum(request.validator),
            checksum(request.token),
            amount_raw,
            int(request.hold_timestamp),
            checksum(request.new_validator),
        )._encode_transaction_data()

    def _transfer_stake_del_data(self, request: TransferStakeDelRequest) -> str:
        contract = self._delegation_contract()
        if request.hold_timestamp is None:
            return contract.functions.transfer(
                checksum(request.validator),
                checksum(self._client.config.contracts.wdel),
                _del_to_wei(request.amount_del),
                checksum(request.new_validator),
            )._encode_transaction_data()
        return contract.functions.transferHold(
            checksum(request.validator),
            checksum(self._client.config.contracts.wdel),
            _del_to_wei(request.amount_del),
            int(request.hold_timestamp),
            checksum(request.new_validator),
        )._encode_transaction_data()

    def _transfer_del_stake_with_reset_data(self, request: TransferDelStakeWithResetRequest) -> str:
        return self._delegation_contract().functions.transferWithReset(
            checksum(request.old_validator),
            checksum(self._client.config.contracts.wdel),
            _del_to_wei(request.amount_del),
            checksum(request.new_validator),
            [int(item) for item in request.hold_timestamps_to_reset],
        )._encode_transaction_data()

    async def _estimate_delegation_call(
        self,
        private_key: str,
        data: str,
        *,
        value_wei: int = 0,
        exact: bool,
    ) -> FeePreflight:
        draft = await self._client.tx.build_contract_call(
            ContractCallRequest(
                contract=self._client.config.contracts.delegation,
                private_key=private_key,
                data=data,
                value_wei=value_wei,
            )
        )
        return await self._client.tx.calculate_fee(draft, exact=exact)

    async def _single_step_workflow(
        self,
        name: str,
        private_key: str,
        data: str,
        broadcast: bool,
        wait_receipt: bool,
    ) -> DecimalWorkflowResult:
        result = await self._send_contract(
            private_key,
            self._client.config.contracts.delegation,
            data,
            0,
            broadcast,
            wait_receipt,
        )
        return DecimalWorkflowResult(
            success=result.success,
            name=name,
            steps=(name,),
            expected_steps=1,
            actual_steps=1,
            extra_steps_required=False,
            primary=result,
            error=result.error,
        )

    async def _single_contract_workflow(
        self,
        name: str,
        contract: str,
        private_key: str,
        data: str,
        broadcast: bool,
        wait_receipt: bool,
    ) -> DecimalWorkflowResult:
        result = await self._send_contract(
            private_key,
            contract,
            data,
            0,
            broadcast,
            wait_receipt,
        )
        return DecimalWorkflowResult(
            success=result.success,
            name=name,
            steps=(name,),
            expected_steps=1,
            actual_steps=1,
            extra_steps_required=False,
            primary=result,
            error=result.error,
        )

    async def _send_contract(
        self,
        private_key: str,
        contract: str,
        data: str,
        value_wei: int,
        broadcast: bool,
        wait_receipt: bool,
    ) -> TransactionResult:
        draft = await self._client.tx.build_contract_call(
            ContractCallRequest(
                contract=contract,
                private_key=private_key,
                data=data,
                value_wei=value_wei,
            )
        )
        return await self._client.tx.send_draft(draft, private_key, broadcast, wait_receipt)

    def _delegation_contract(self, web3=None):
        return (web3 or self._client.web3).eth.contract(
            address=checksum(self._client.config.contracts.delegation),
            abi=DELEGATION_ABI,
        )

    def _multicall_contract(self):
        return self._client.web3.eth.contract(
            address=checksum(self._client.config.contracts.multicall),
            abi=MULTICALL_ABI,
        )

    def _master_validator_contract(self, web3=None):
        return (web3 or self._client.web3).eth.contract(
            address=checksum(self._client.config.contracts.master_validator),
            abi=MASTER_VALIDATOR_ABI,
        )


def _del_to_wei(value: Decimal | str | int) -> int:
    return parse_units(value, 18)


def _parse_units(value: Decimal | str | int, decimals: int) -> int:
    return parse_units(value, decimals)


def _hold_time(hold_timestamp: int) -> str:
    return datetime.fromtimestamp(int(hold_timestamp), tz=timezone.utc).isoformat().replace("+00:00", "Z")


def _delegation_stake(
    value: Any,
    *,
    expected_validator: str,
    expected_delegator: str,
    expected_token: str,
    expected_hold_timestamp: int,
    wdel: str,
    block_number: int | None = None,
) -> DelegationStake:
    if not isinstance(value, (list, tuple)) or len(value) < 7:
        raise ValueError("Unexpected Decimal delegation stake response")
    stake = DelegationStake(
        validator=checksum(value[0]),
        delegator=checksum(value[1]),
        token=checksum(value[2]),
        amount_raw=int(value[3]),
        token_id=int(value[4]),
        token_type=int(value[5]),
        hold_timestamp=int(value[6]),
        block_number=block_number,
    )
    zero_address = checksum("0x0000000000000000000000000000000000000000")
    is_empty = (
        stake.validator == zero_address
        and stake.delegator == zero_address
        and stake.token == zero_address
        and stake.amount_raw == 0
        and stake.token_id == 0
        and stake.token_type == DelegationTokenType.UNKNOWN
        and stake.hold_timestamp == 0
    )
    if is_empty:
        return stake
    if stake.amount_raw < 0:
        raise ValueError("Delegation stake amount cannot be negative")
    expected_identity = (
        checksum(expected_validator),
        checksum(expected_delegator),
        checksum(expected_token),
    )
    actual_identity = (stake.validator, stake.delegator, stake.token)
    if actual_identity != expected_identity:
        raise ValueError("Delegation stake identity does not match the requested position")
    if stake.token_id != 0:
        raise ValueError("Fungible delegation stake must have token_id=0")
    try:
        token_type = DelegationTokenType(stake.token_type)
    except ValueError as exc:
        raise ValueError(f"Unsupported delegation token type: {stake.token_type}") from exc
    if token_type not in (DelegationTokenType.DRC20, DelegationTokenType.DEL):
        raise ValueError(f"Unsupported fungible delegation token type: {token_type.name}")
    if token_type is DelegationTokenType.DEL and stake.token != checksum(wdel):
        raise ValueError("DEL delegation stake must use the configured WDEL contract")
    if token_type is DelegationTokenType.DRC20 and stake.token == checksum(wdel):
        raise ValueError("Configured WDEL contract must use delegation token type DEL")
    if stake.hold_timestamp != int(expected_hold_timestamp):
        raise ValueError("Delegation stake hold key does not match the requested position")
    return stake


def _with_hold_schedule(result: TransactionResult, hold_timestamp: int) -> TransactionResult:
    return replace(
        result,
        hold_timestamp=int(hold_timestamp),
        hold_time=_hold_time(hold_timestamp),
    )


def _workflow_with_hold_schedule(
    result: DecimalWorkflowResult,
    hold_timestamp: int,
) -> DecimalWorkflowResult:
    if result.primary is None:
        return result
    return replace(result, primary=_with_hold_schedule(result.primary, hold_timestamp))


def _workflow_exception(name: str, exc: Exception) -> DecimalWorkflowResult:
    return DecimalWorkflowResult(
        success=False,
        name=name,
        steps=(),
        expected_steps=1,
        actual_steps=0,
        extra_steps_required=False,
        error=str(exc),
    )
