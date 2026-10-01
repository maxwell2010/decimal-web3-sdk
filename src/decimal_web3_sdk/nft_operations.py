"""Current delegation-nft calls and exact, typed stake reads."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal
from hexbytes import HexBytes
from web3 import Web3

from ._contract_operations import (
    ContractOperationRequest,
    ContractOperations,
    ZERO_ADDRESS,
    address,
    permit_values,
    uint,
    uint_list,
)
from .decimal import DelegationStake
from .erc20 import PermitSignature
from .transactions import TransactionResult


@dataclass(frozen=True)
class CreateReservelessNftCollectionRequest(ContractOperationRequest):
    kind: Literal["erc721", "erc1155"]
    creator: str
    symbol: str
    name: str
    contract_uri: str
    burnable: bool = True
    domain = "nft"

    def to_contract_call(self, client):
        if self.kind not in ("erc721", "erc1155"):
            raise ValueError("kind must be erc721 or erc1155")
        if type(self.burnable) is not bool:
            raise TypeError("burnable must be a bool")
        if not all(
            isinstance(item, str) and item.strip()
            for item in (self.symbol, self.name, self.contract_uri)
        ):
            raise ValueError("symbol, name and contract_uri are required")
        function = (
            "createDRC721Reserveless" if self.kind == "erc721" else "createDRC1155Reserveless"
        )
        # The deployed ABI calls this boolean refundable, not the JS type's allowMint.
        meta = (
            address(self.creator),
            self.symbol,
            self.name,
            self.contract_uri,
            False,
            self.burnable,
        )
        return self._encode(
            client, "nft_center", client.config.contracts.nft_center, function, [meta]
        )


@dataclass(frozen=True)
class AddTokenReserveNftRequest(ContractOperationRequest):
    nft: str
    token_id: int
    reserve_amount_raw: int
    permit: PermitSignature | None = None
    domain = "nft"

    def to_contract_call(self, client):
        args = [
            uint(self.token_id, "token_id"),
            uint(self.reserve_amount_raw, "reserve_amount_raw", positive=True),
        ]
        function = "addReserve"
        if self.permit is not None:
            function = "addReserveByPermit"
            args.extend(permit_values(self.permit))
        return self._encode(client, "nft_reserve", self.nft, function, args)


@dataclass(frozen=True)
class NftStakeOperationRequest(ContractOperationRequest):
    validator: str
    nft: str
    token_id: int
    domain = "nft"

    def _stake_args(self):
        return [address(self.validator), address(self.nft), uint(self.token_id, "token_id")]

    def _stake_call(self, client, function, args):
        if client.config.contracts.delegation_nft.lower() == client.config.contracts.delegation.lower():
            raise NotImplementedError(
                "This legacy NFT staking operation is not available on the unified Delegation contract"
            )
        return self._encode(
            client, "delegation_nft", client.config.contracts.delegation_nft, function, args
        )


@dataclass(frozen=True)
class StakeNftToHoldRequest(NftStakeOperationRequest):
    amount: int
    old_hold_timestamp: int
    new_hold_timestamp: int

    def to_contract_call(self, client):
        old = uint(self.old_hold_timestamp, "old_hold_timestamp")
        new = uint(self.new_hold_timestamp, "new_hold_timestamp", positive=True)
        if new <= old:
            raise ValueError("new_hold_timestamp must be later than old_hold_timestamp")
        return self._stake_call(
            client,
            "hold",
            [*self._stake_args(), uint(self.amount, "amount", positive=True), old, new],
        )


@dataclass(frozen=True)
class ResetNftStakeHoldRequest(NftStakeOperationRequest):
    delegator: str
    hold_timestamp: int

    def to_contract_call(self, client):
        return self._stake_call(
            client,
            "resetHold",
            [
                address(self.validator),
                address(self.delegator),
                address(self.nft),
                uint(self.token_id, "token_id"),
                uint(self.hold_timestamp, "hold_timestamp", positive=True),
            ],
        )


@dataclass(frozen=True)
class ResetNftStakeHoldsRequest(NftStakeOperationRequest):
    delegator: str
    hold_timestamps: tuple[int, ...]

    def to_contract_call(self, client):
        return self._stake_call(
            client,
            "resetHolds",
            [
                address(self.validator),
                address(self.delegator),
                address(self.nft),
                uint(self.token_id, "token_id"),
                uint_list(self.hold_timestamps, "hold_timestamps"),
            ],
        )


@dataclass(frozen=True)
class WithdrawNftWithResetRequest(NftStakeOperationRequest):
    amount: int
    hold_timestamps_to_reset: tuple[int, ...]

    def to_contract_call(self, client):
        return self._stake_call(
            client,
            "withdrawWithReset",
            [
                *self._stake_args(),
                uint(self.amount, "amount", positive=True),
                uint_list(self.hold_timestamps_to_reset, "hold_timestamps_to_reset"),
            ],
        )


@dataclass(frozen=True)
class TransferNftWithResetRequest(WithdrawNftWithResetRequest):
    new_validator: str

    def to_contract_call(self, client):
        if address(self.validator) == address(self.new_validator):
            raise ValueError("new_validator must differ from validator")
        return self._stake_call(
            client,
            "transferWithReset",
            [
                *self._stake_args(),
                uint(self.amount, "amount", positive=True),
                address(self.new_validator),
                uint_list(self.hold_timestamps_to_reset, "hold_timestamps_to_reset"),
            ],
        )


@dataclass(frozen=True)
class HoldNftWithResetRequest(WithdrawNftWithResetRequest):
    new_hold_timestamp: int

    def to_contract_call(self, client):
        return self._stake_call(
            client,
            "holdWithReset",
            [
                *self._stake_args(),
                uint(self.amount, "amount", positive=True),
                uint(self.new_hold_timestamp, "new_hold_timestamp", positive=True),
                uint_list(self.hold_timestamps_to_reset, "hold_timestamps_to_reset"),
            ],
        )


@dataclass(frozen=True)
class CompleteNftStakeRequest(ContractOperationRequest):
    indexes: tuple[int, ...]
    domain = "nft"

    def to_contract_call(self, client):
        abi = (
            "delegation_nft_unified"
            if client.config.contracts.delegation_nft.lower() == client.config.contracts.delegation.lower()
            else "delegation_nft"
        )
        return self._encode(
            client,
            abi,
            client.config.contracts.delegation_nft,
            "complete",
            [uint_list(self.indexes, "indexes")],
        )


@dataclass(frozen=True)
class NftStake(DelegationStake):
    def amount_string(self, decimals: int = 0) -> str:
        return super().amount_string(decimals)

    def amount(self, decimals: int = 0):
        return super().amount(decimals)

    def as_dict(self, decimals: int = 0) -> dict:
        return super().as_dict(decimals)


@dataclass(frozen=True)
class FrozenNftStake:
    index: int
    stake: NftStake
    freeze_status: int
    freeze_type: int
    unfreeze_timestamp: int

    def as_dict(self) -> dict:
        return {
            "index": str(self.index),
            "stake": self.stake.as_dict(),
            "freeze_status": self.freeze_status,
            "freeze_type": self.freeze_type,
            "unfreeze_timestamp": str(self.unfreeze_timestamp),
        }


@dataclass(frozen=True)
class NftCollectionState:
    active: bool
    kind: Literal["erc721", "erc1155"]
    with_reserve: bool


@dataclass(frozen=True)
class NftReserve:
    token: str
    amount_raw: int
    reserve_type: int


@dataclass(frozen=True)
class CreatedNftCollection:
    nft_address: str
    kind: Literal["erc721", "erc1155"]
    creator: str
    symbol: str
    name: str
    contract_uri: str
    refundable: bool
    burnable: bool


class NftOperations(ContractOperations):
    _operation_domain = "nft"

    async def _read_nft_call(self, target, abi_name, function, args=(), block_identifier="latest"):
        abi = self._client.abi.load(abi_name)
        target = address(target)
        return await self._client.rpc.call(
            lambda w3: w3.eth.contract(address=target, abi=abi)
            .get_function_by_name(function)(*args).call(block_identifier=block_identifier)
        )

    async def collection_state(self, nft: str, *, block_identifier="latest") -> NftCollectionState:
        """Read collection registration, standard and reserve mode, not minted balance."""
        active, kind, reserved = await self._read_nft_call(
            self._client.config.contracts.nft_center, "nft_center", "getNFTState",
            [address(nft)], block_identifier,
        )
        if type(active) is not bool or type(reserved) is not bool or type(kind) is not int or kind not in (0, 1):
            raise ValueError("Unsupported NFT collection state")
        return NftCollectionState(active, "erc721" if kind == 0 else "erc1155", reserved)

    async def check_reserve_token(self, token: str, *, block_identifier="latest") -> bool:
        """Check NFTCenter eligibility; reverts and RPC errors propagate, never imply success."""
        await self._read_nft_call(
            self._client.config.contracts.nft_center, "nft_center", "checkToken",
            [address(token)], block_identifier,
        )
        return True

    async def get_reserve(self, nft: str, token_id: int, *, block_identifier="latest") -> NftReserve:
        """Read reserve type, token address and exact total raw amount for an ID."""
        token, amount, kind = await self._read_nft_call(
            nft, "nft_721", "getReserve", [uint(token_id, "token_id")], block_identifier,
        )
        if type(kind) is not int or kind not in (0, 1, 2):
            raise ValueError("Unsupported NFT reserve type")
        return NftReserve(Web3.to_checksum_address(token), uint(amount, "reserve amount"), kind)

    def created_collections(self, receipt: dict) -> tuple[CreatedNftCollection, ...]:
        """Decode NFTCenter creation events. These identify collections, not minted IDs."""
        status = receipt.get("status")
        if (int(status, 0) if isinstance(status, str) else status) != 1:
            raise ValueError("A successful receipt is required")
        contract = self._client.web3.eth.contract(abi=self._client.abi.load("nft_center"))
        event = contract.events.NFTCreated()
        topic = Web3.keccak(text="NFTCreated(address,uint8,(address,string,string,string,bool,bool))")
        result = []
        for log in receipt.get("logs", []):
            if log["address"].lower() != self._client.config.contracts.nft_center.lower():
                continue
            if not log.get("topics") or HexBytes(log["topics"][0]) != topic:
                continue
            normalized = {field: receipt.get(field) for field in ("blockHash", "blockNumber", "transactionHash", "transactionIndex")}
            normalized.update(log)
            normalized.setdefault("logIndex", 0)
            args = event.process_log(normalized)["args"]
            if args["nftType"] not in (0, 1):
                raise ValueError("Unsupported NFT collection type in receipt")
            meta = args["nft"]
            result.append(CreatedNftCollection(
                address(args["tokenAddress"]), "erc721" if args["nftType"] == 0 else "erc1155",
                address(meta["creator"]), meta["symbol"], meta["name"], meta["contractURI"],
                meta["refundable"], meta["burnable"],
            ))
        return tuple(result)

    async def create_reserveless_collection(
        self,
        request: CreateReservelessNftCollectionRequest,
        broadcast: bool = False,
        wait_receipt: bool = False,
    ) -> TransactionResult:
        return await self._send_operation(
            request, broadcast, wait_receipt, request_type=CreateReservelessNftCollectionRequest
        )

    async def add_token_reserve(
        self,
        request: AddTokenReserveNftRequest,
        broadcast: bool = False,
        wait_receipt: bool = False,
    ) -> TransactionResult:
        return await self._send_operation(
            request, broadcast, wait_receipt, request_type=AddTokenReserveNftRequest
        )

    async def stake_to_hold(
        self, request: StakeNftToHoldRequest, broadcast: bool = False, wait_receipt: bool = False
    ) -> TransactionResult:
        return await self._send_operation(
            request, broadcast, wait_receipt, request_type=StakeNftToHoldRequest
        )

    async def reset_stake_hold(
        self, request: ResetNftStakeHoldRequest, broadcast: bool = False, wait_receipt: bool = False
    ) -> TransactionResult:
        return await self._send_operation(
            request, broadcast, wait_receipt, request_type=ResetNftStakeHoldRequest
        )

    async def reset_stake_holds(
        self,
        request: ResetNftStakeHoldsRequest,
        broadcast: bool = False,
        wait_receipt: bool = False,
    ) -> TransactionResult:
        return await self._send_operation(
            request, broadcast, wait_receipt, request_type=ResetNftStakeHoldsRequest
        )

    async def withdraw_with_reset(
        self,
        request: WithdrawNftWithResetRequest,
        broadcast: bool = False,
        wait_receipt: bool = False,
    ) -> TransactionResult:
        return await self._send_operation(
            request, broadcast, wait_receipt, request_type=WithdrawNftWithResetRequest
        )

    async def transfer_with_reset(
        self,
        request: TransferNftWithResetRequest,
        broadcast: bool = False,
        wait_receipt: bool = False,
    ) -> TransactionResult:
        return await self._send_operation(
            request, broadcast, wait_receipt, request_type=TransferNftWithResetRequest
        )

    async def hold_with_reset(
        self, request: HoldNftWithResetRequest, broadcast: bool = False, wait_receipt: bool = False
    ) -> TransactionResult:
        return await self._send_operation(
            request, broadcast, wait_receipt, request_type=HoldNftWithResetRequest
        )

    async def complete_stake(
        self, request: CompleteNftStakeRequest, broadcast: bool = False, wait_receipt: bool = False
    ) -> TransactionResult:
        return await self._send_operation(
            request, broadcast, wait_receipt, request_type=CompleteNftStakeRequest
        )

    async def _read_stake_call(self, function: str, args: list, block_identifier="latest"):
        abi_name = "delegation_nft_unified" if self._unified_delegation else "delegation_nft"
        abi = self._client.abi.load(abi_name)
        target = address(self._client.config.contracts.delegation_nft)
        return await self._client.rpc.call(
            lambda w3: (
                w3.eth.contract(address=target, abi=abi)
                .get_function_by_name(function)(*args)
                .call(block_identifier=block_identifier)
            )
        )

    async def get_stake(
        self, validator: str, delegator: str, nft: str, token_id: int, *, block_identifier="latest"
    ) -> NftStake:
        function = "getNFTStake" if self._unified_delegation else "getStake"
        args = (
            [address(nft), uint(token_id, "token_id"), address(delegator), address(validator), 0]
            if self._unified_delegation
            else [address(validator), address(delegator), address(nft), uint(token_id, "token_id")]
        )
        values = await self._read_stake_call(
            function, args,
            block_identifier,
        )
        return self._checked_stake(values, validator, delegator, nft, token_id, 0, block_identifier, self._unified_delegation)

    async def get_stake_id(
        self, validator: str, delegator: str, nft: str, token_id: int, *, block_identifier="latest"
    ) -> str:
        function = "getNFTStakeId" if self._unified_delegation else "getStakeId"
        args = (
            [address(nft), uint(token_id, "token_id"), address(delegator), address(validator), 0]
            if self._unified_delegation
            else [address(validator), address(delegator), address(nft), uint(token_id, "token_id")]
        )
        value = await self._read_stake_call(
            function, args,
            block_identifier,
        )
        return "0x" + bytes(value).hex()

    async def get_hold_stake(
        self,
        validator: str,
        delegator: str,
        nft: str,
        token_id: int,
        hold_timestamp: int,
        *,
        block_identifier="latest",
    ) -> NftStake:
        hold_key = uint(hold_timestamp, "hold_timestamp", positive=True)
        function = "getNFTStake" if self._unified_delegation else "getHoldStake"
        args = (
            [address(nft), uint(token_id, "token_id"), address(delegator), address(validator), hold_key]
            if self._unified_delegation
            else [address(validator), address(delegator), address(nft), uint(token_id, "token_id"), hold_key]
        )
        values = await self._read_stake_call(function, args, block_identifier)
        return self._checked_stake(
            values, validator, delegator, nft, token_id, hold_timestamp, block_identifier, self._unified_delegation
        )

    @staticmethod
    def _checked_stake(
        values, validator, delegator, nft, token_id, hold_timestamp, block_identifier,
        unified=False,
    ):
        if unified:
            if len(values) != 10 or type(values[9]) is not bool:
                raise ValueError("Unsupported unified NFT stake format")
            values = (
                (values[5], values[4], values[0], values[2], values[1], values[3], values[8])
                if values[9]
                else (ZERO_ADDRESS, ZERO_ADDRESS, ZERO_ADDRESS, 0, 0, 0, 0)
            )
        elif len(values) != 7:
            raise ValueError("Unsupported NFT stake format")
        stake = NftStake(
            *values, block_number=block_identifier if type(block_identifier) is int else None
        )
        empty = (ZERO_ADDRESS, ZERO_ADDRESS, ZERO_ADDRESS, 0, 0, 0, 0)
        if tuple(values) == empty:
            return stake
        keys = (
            address(stake.validator),
            address(stake.delegator),
            address(stake.token),
            stake.token_id,
            stake.hold_timestamp,
        )
        expected = (address(validator), address(delegator), address(nft), token_id, hold_timestamp)
        if keys != expected or stake.token_type not in (2, 3):
            raise ValueError(
                "NFT stake response does not match the requested owner, validator, NFT, ID or hold key"
            )
        return stake

    async def get_frozen_stake(self, index: int, *, block_identifier="latest") -> FrozenNftStake:
        values = await self._read_stake_call(
            "getFrozenStake", [uint(index, "index")], block_identifier
        )
        return self._frozen_stake(index, values, self._unified_delegation)

    async def get_frozen_stakes(
        self, indexes: tuple[int, ...], *, block_identifier="latest"
    ) -> tuple[FrozenNftStake, ...]:
        indexes = uint_list(indexes, "indexes")
        values = await self._read_stake_call("getFrozenStakes", [indexes], block_identifier)
        if len(values) != len(indexes):
            raise ValueError("Unexpected number of frozen stakes in the contract response")
        return tuple(self._frozen_stake(index, value, self._unified_delegation) for index, value in zip(indexes, values))

    async def get_freeze_time(
        self, freeze_type: Literal[1, 2], *, block_identifier="latest"
    ) -> int:
        if type(freeze_type) is not int or freeze_type not in (1, 2):
            raise ValueError("freeze_type must be 1 (withdraw) or 2 (transfer)")
        return int(await self._read_stake_call("getFreezeTime", [freeze_type], block_identifier))

    @staticmethod
    def _frozen_stake(index, values, unified=False):
        if len(values) != 4:
            raise ValueError(
                "Unsupported frozen stake format; expected stake, status, type, timestamp"
            )
        stake, status, kind, timestamp = values
        if unified:
            if len(stake) != 8:
                raise ValueError("Unsupported unified frozen NFT stake format")
            stake = stake[:7]
        return FrozenNftStake(index, NftStake(*stake), int(status), int(kind), int(timestamp))
