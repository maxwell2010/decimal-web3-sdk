from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal
from typing import Any

from web3 import Web3

from .transactions import (
    ContractCallRequest,
    Erc20ApproveRequest,
    FeePreflight,
    TransactionDraft,
    TransactionResult,
    _token_preflight_failure,
    user_message_from_error,
)
from .mnemonic import FromMnemonicMixin
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
    amount_del: Decimal | str | int | float
    private_key: str


@dataclass(frozen=True)
class HoldDelRequest(FromMnemonicMixin):
    validator: str
    amount_del: Decimal | str | int | float
    hold_timestamp: int
    private_key: str


@dataclass(frozen=True)
class UnbondDelRequest(FromMnemonicMixin):
    validator: str
    amount_del: Decimal | str | int | float
    private_key: str


@dataclass(frozen=True)
class WithdrawHoldDelRequest(FromMnemonicMixin):
    validator: str
    amount_del: Decimal | str | int | float
    hold_timestamp: int
    private_key: str


@dataclass(frozen=True)
class MultisendRecipient:
    to: str
    amount_del: Decimal | str | int | float


@dataclass(frozen=True)
class MultisendDelRequest(FromMnemonicMixin):
    recipients: list[MultisendRecipient]
    private_key: str
    memo: str | None = None


@dataclass(frozen=True)
class MultisendErc20Recipient:
    to: str
    amount: Decimal | str | int | float


@dataclass(frozen=True)
class MultisendErc20Request(FromMnemonicMixin):
    token: str
    recipients: list[MultisendErc20Recipient]
    private_key: str
    decimals: int | None = None
    memo: str | None = None
    auto_approve: bool = True
    prefer_permit: bool = True
    permit_deadline: int = 2**256 - 1


@dataclass(frozen=True)
class DelegateErc20Request(FromMnemonicMixin):
    token: str
    validator: str
    amount: Decimal | str | int | float
    private_key: str
    decimals: int | None = None
    auto_approve: bool = True
    prefer_permit: bool = True
    permit_deadline: int = 2**256 - 1


@dataclass(frozen=True)
class HoldErc20Request(FromMnemonicMixin):
    token: str
    validator: str
    amount: Decimal | str | int | float
    hold_timestamp: int
    private_key: str
    decimals: int | None = None
    auto_approve: bool = True
    prefer_permit: bool = True
    permit_deadline: int = 2**256 - 1


@dataclass(frozen=True)
class UnbondErc20Request(FromMnemonicMixin):
    token: str
    validator: str
    amount: Decimal | str | int | float
    private_key: str
    decimals: int | None = None


@dataclass(frozen=True)
class WithdrawHoldErc20Request(FromMnemonicMixin):
    token: str
    validator: str
    amount: Decimal | str | int | float
    hold_timestamp: int
    private_key: str
    decimals: int | None = None


@dataclass(frozen=True)
class TransferStakeErc20Request(FromMnemonicMixin):
    token: str
    validator: str
    new_validator: str
    amount: Decimal | str | int | float
    private_key: str
    decimals: int | None = None
    hold_timestamp: int | None = None


@dataclass(frozen=True)
class StakeTokenToHoldRequest(FromMnemonicMixin):
    token: str
    validator: str
    amount: Decimal | str | int | float
    old_hold_timestamp: int
    new_hold_timestamp: int
    private_key: str
    decimals: int | None = None


@dataclass(frozen=True)
class ResetStakeHoldRequest(FromMnemonicMixin):
    validator: str
    delegator: str
    private_key: str
    hold_timestamp: int
    token: str | None = None


@dataclass(frozen=True)
class WithdrawStakeWithResetRequest(FromMnemonicMixin):
    token: str
    validator: str
    amount: Decimal | str | int | float
    hold_timestamps_to_reset: list[int]
    private_key: str
    decimals: int | None = None


@dataclass(frozen=True)
class TransferStakeWithResetRequest(FromMnemonicMixin):
    token: str
    old_validator: str
    new_validator: str
    amount: Decimal | str | int | float
    hold_timestamps_to_reset: list[int]
    private_key: str
    decimals: int | None = None


@dataclass(frozen=True)
class HoldStakeWithResetRequest(FromMnemonicMixin):
    token: str
    validator: str
    amount: Decimal | str | int | float
    new_hold_timestamp: int
    hold_timestamps_to_reset: list[int]
    private_key: str
    decimals: int | None = None


@dataclass(frozen=True)
class ValidatorSelfPauseRequest(FromMnemonicMixin):
    private_key: str


@dataclass(frozen=True)
class ValidatorPauseRequest(FromMnemonicMixin):
    validator: str
    private_key: str


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
        return not self.extra_steps_required and self.actual_steps <= 1

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
        return Decimal(self.total_fee_wei) / Decimal(10**18)

    @property
    def tx_hash(self) -> str | None:
        return self.primary.tx_hash if self.primary else None

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
        return Decimal(self.fee_wei) / Decimal(10**18)


class DecimalService:
    def __init__(self, client) -> None:
        self._client = client

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
        return await self._send_contract(
            request.private_key,
            self._client.config.contracts.delegation,
            data,
            _del_to_wei(request.amount_del),
            broadcast,
            wait_receipt,
        )

    async def unbond_del(
        self,
        request: UnbondDelRequest,
        broadcast: bool = False,
        wait_receipt: bool = False,
    ) -> TransactionResult:
        data = self._delegation_contract().functions.withdraw(
            checksum(request.validator),
            checksum(self._client.config.contracts.del_token),
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
            checksum(self._client.config.contracts.del_token),
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

    async def multisend_del(
        self,
        request: MultisendDelRequest,
        broadcast: bool = False,
        wait_receipt: bool = False,
    ) -> TransactionResult:
        if not request.recipients:
            return TransactionResult(success=False, error="At least one recipient is required")

        draft = await self.build_multisend_del(request)
        return await self._client.tx.send_draft(draft, request.private_key, broadcast, wait_receipt)

    async def build_multisend_del(self, request: MultisendDelRequest) -> TransactionDraft:
        if not request.recipients:
            raise ValueError("At least one recipient is required")

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

    async def estimate_fee_for_multisend_del(self, request: MultisendDelRequest) -> FeePreflight:
        draft = await self.build_multisend_del(request)
        return await self._client.tx.calculate_fee(draft)

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
                            amount=Decimal(total_raw) / (Decimal(10) ** int(decimals)),
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

    async def transfer_stake_erc20(
        self,
        request: TransferStakeErc20Request,
        broadcast: bool = False,
        wait_receipt: bool = False,
    ) -> DecimalWorkflowResult:
        try:
            amount_raw = await self._erc20_amount_raw(request.token, request.amount, request.decimals)
            contract = self._delegation_contract()
            if request.hold_timestamp is None:
                data = contract.functions.transfer(
                    checksum(request.validator),
                    checksum(request.token),
                    amount_raw,
                    checksum(request.new_validator),
                )._encode_transaction_data()
                step = "transfer_stake_erc20"
            else:
                data = contract.functions.transferHold(
                    checksum(request.validator),
                    checksum(request.token),
                    amount_raw,
                    int(request.hold_timestamp),
                    checksum(request.new_validator),
                )._encode_transaction_data()
                step = "transfer_hold_stake_erc20"
            return await self._single_step_workflow(step, request.private_key, data, broadcast, wait_receipt)
        except Exception as exc:
            return _workflow_exception("transfer_stake_erc20", exc)

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
            return await self._single_step_workflow("stake_token_to_hold", request.private_key, data, broadcast, wait_receipt)
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
            return await self._single_step_workflow("hold_stake_with_reset", request.private_key, data, broadcast, wait_receipt)
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
        contract = self._master_validator_contract()
        return await self._client.rpc.call(
            lambda _w3: int(contract.functions.getValidatorStatus(checksum(validator)).call())
        )

    async def validator_is_active(self, validator: str) -> bool:
        contract = self._master_validator_contract()
        return await self._client.rpc.call(
            lambda _w3: bool(contract.functions.isActive(checksum(validator)).call())
        )

    async def validator_is_member(self, validator: str) -> bool:
        contract = self._master_validator_contract()
        return await self._client.rpc.call(
            lambda _w3: bool(contract.functions.isMember(checksum(validator)).call())
        )

    async def _erc20_stake_with_allowance(
        self,
        name: str,
        token: str,
        validator: str,
        amount: Decimal | str | int | float,
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
        amount: Decimal | str | int | float,
        decimals: int | None,
    ) -> int:
        if decimals is None:
            decimals = (await self._client.erc20.info(token)).decimals
        return _parse_units(amount, decimals)

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

    def _delegation_contract(self):
        return self._client.web3.eth.contract(
            address=checksum(self._client.config.contracts.delegation),
            abi=DELEGATION_ABI,
        )

    def _multicall_contract(self):
        return self._client.web3.eth.contract(
            address=checksum(self._client.config.contracts.multicall),
            abi=MULTICALL_ABI,
        )

    def _master_validator_contract(self):
        return self._client.web3.eth.contract(
            address=checksum(self._client.config.contracts.master_validator),
            abi=MASTER_VALIDATOR_ABI,
        )


def _del_to_wei(value: Decimal | str | int | float) -> int:
    return int(Web3.to_wei(Decimal(str(value)), "ether"))


def _parse_units(value: Decimal | str | int | float, decimals: int) -> int:
    return int(Decimal(str(value)) * (Decimal(10) ** int(decimals)))


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
