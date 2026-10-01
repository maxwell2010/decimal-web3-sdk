from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Literal

from .decimal import DecimalWorkflowResult
from .contracts import AbiRegistry
from .mnemonic import FromMnemonicMixin
from .nft_operations import NftOperations
from ._contract_operations import ContractOperationRequest, ZERO_ADDRESS, address, uint
from .transactions import ContractCallRequest, TransactionDraft, TransactionResult
from .wallet import checksum, private_key_to_address


NftKind = Literal["erc721", "erc1155"]


NFT_CENTER_ABI = AbiRegistry().load("nft_center")


DELEGATION_NFT_ABI: list[dict[str, Any]] = [
    {
        "inputs": [
            {"internalType": "address", "name": "validator", "type": "address"},
            {"internalType": "address", "name": "nft", "type": "address"},
            {"internalType": "uint256", "name": "tokenId", "type": "uint256"},
        ],
        "name": "delegateDRC721",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function",
    },
    {
        "inputs": [
            {"internalType": "address", "name": "validator", "type": "address"},
            {"internalType": "address", "name": "nft", "type": "address"},
            {"internalType": "uint256", "name": "tokenId", "type": "uint256"},
            {"internalType": "uint256", "name": "amount", "type": "uint256"},
        ],
        "name": "delegateDRC1155",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function",
    },
    {
        "inputs": [
            {"internalType": "address", "name": "validator", "type": "address"},
            {"internalType": "address", "name": "nft", "type": "address"},
            {"internalType": "uint256", "name": "tokenId", "type": "uint256"},
            {"internalType": "uint256", "name": "holdTimestamp", "type": "uint256"},
        ],
        "name": "delegateHoldDRC721",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function",
    },
    {
        "inputs": [
            {"internalType": "address", "name": "validator", "type": "address"},
            {"internalType": "address", "name": "nft", "type": "address"},
            {"internalType": "uint256", "name": "tokenId", "type": "uint256"},
            {"internalType": "uint256", "name": "amount", "type": "uint256"},
            {"internalType": "uint256", "name": "holdTimestamp", "type": "uint256"},
        ],
        "name": "delegateHoldDRC1155",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function",
    },
    {
        "inputs": [
            {"internalType": "address", "name": "validator", "type": "address"},
            {"internalType": "address", "name": "nft", "type": "address"},
            {"internalType": "uint256", "name": "tokenId", "type": "uint256"},
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
            {"internalType": "address", "name": "nft", "type": "address"},
            {"internalType": "uint256", "name": "tokenId", "type": "uint256"},
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
            {"internalType": "address", "name": "nft", "type": "address"},
            {"internalType": "uint256", "name": "tokenId", "type": "uint256"},
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
            {"internalType": "address", "name": "nft", "type": "address"},
            {"internalType": "uint256", "name": "tokenId", "type": "uint256"},
            {"internalType": "uint256", "name": "amount", "type": "uint256"},
            {"internalType": "uint256", "name": "holdTimestamp", "type": "uint256"},
            {"internalType": "address", "name": "newValidator", "type": "address"},
        ],
        "name": "transferHold",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function",
    },
]


ERC721_ABI = AbiRegistry().load("nft_721")
ERC1155_ABI = AbiRegistry().load("nft_1155")


@dataclass(frozen=True)
class CreateNftCollectionRequest(FromMnemonicMixin):
    kind: NftKind
    symbol: str
    name: str
    contract_uri: str
    private_key: str = field(repr=False)
    refundable: bool = False
    creator: str | None = None
    burnable: bool = True


@dataclass(frozen=True)
class MintNftRequest(FromMnemonicMixin):
    kind: NftKind
    nft: str
    to: str
    token_uri: str
    private_key: str = field(repr=False)
    token_id: int | None = None
    amount: int = 1
    reserve_amount_raw: int = 0
    reserve_token: str = "0x0000000000000000000000000000000000000000"
    value_wei: int = 0


@dataclass(frozen=True)
class NftTransferRequest(FromMnemonicMixin):
    kind: NftKind
    nft: str
    to: str
    token_id: int
    private_key: str = field(repr=False)
    amount: int = 1
    data: bytes = b""


@dataclass(frozen=True)
class NftBatchTransferRequest(FromMnemonicMixin):
    nft: str
    to: str
    token_ids: list[int]
    amounts: list[int]
    private_key: str = field(repr=False)
    data: bytes = b""


@dataclass(frozen=True)
class NftApprovalRequest(FromMnemonicMixin):
    kind: NftKind
    nft: str
    operator: str
    approved: bool
    private_key: str = field(repr=False)


@dataclass(frozen=True)
class NftApproveRequest(FromMnemonicMixin):
    nft: str
    to: str
    token_id: int
    private_key: str = field(repr=False)


@dataclass(frozen=True)
class BurnNftRequest(FromMnemonicMixin):
    kind: NftKind
    nft: str
    token_id: int
    private_key: str = field(repr=False)
    amount: int = 1


@dataclass(frozen=True)
class DisableMintNftRequest(FromMnemonicMixin):
    kind: NftKind
    nft: str
    private_key: str = field(repr=False)


@dataclass(frozen=True)
class SetTokenUriNftRequest(FromMnemonicMixin):
    kind: NftKind
    nft: str
    token_id: int
    token_uri: str
    private_key: str = field(repr=False)
    allow_legacy: bool = False


@dataclass(frozen=True)
class AddDelReserveNftRequest(FromMnemonicMixin):
    kind: NftKind
    nft: str
    token_id: int
    reserve_wei: int
    private_key: str = field(repr=False)


@dataclass(frozen=True)
class DelegateNftRequest(FromMnemonicMixin):
    kind: NftKind
    nft: str
    validator: str
    token_id: int
    private_key: str = field(repr=False)
    amount: int = 1
    auto_approve: bool = False


@dataclass(frozen=True)
class HoldNftRequest(FromMnemonicMixin):
    kind: NftKind
    nft: str
    validator: str
    token_id: int
    hold_timestamp: int
    private_key: str = field(repr=False)
    amount: int = 1
    auto_approve: bool = False


@dataclass(frozen=True)
class TransferNftStakeRequest(FromMnemonicMixin):
    nft: str
    validator: str
    new_validator: str
    token_id: int
    private_key: str = field(repr=False)
    amount: int = 1
    hold_timestamp: int | None = None


@dataclass(frozen=True)
class WithdrawNftRequest(FromMnemonicMixin):
    nft: str
    validator: str
    token_id: int
    private_key: str = field(repr=False)
    amount: int = 1
    hold_timestamp: int | None = None


class NftService(NftOperations):
    def __init__(self, client) -> None:
        self._client = client

    async def owner_of(self, nft: str, token_id: int) -> str:
        return await self._client.rpc.call(lambda w3: self._erc721_contract(nft, w3).functions.ownerOf(int(token_id)).call())

    async def balance_of(self, nft: str, owner: str, token_id: int | None = None, kind: NftKind = "erc721") -> int:
        if kind == "erc721":
            return int(await self._client.rpc.call(lambda w3: self._erc721_contract(nft, w3).functions.balanceOf(checksum(owner)).call()))
        if token_id is None:
            raise ValueError("token_id is required for ERC1155 balanceOf")
        return int(await self._client.rpc.call(lambda w3: self._erc1155_contract(nft, w3).functions.balanceOf(checksum(owner), int(token_id)).call()))

    async def is_approved_for_all(self, kind: NftKind, nft: str, owner: str, operator: str) -> bool:
        return bool(
            await self._client.rpc.call(
                lambda w3: self._nft_contract(kind, nft, w3).functions.isApprovedForAll(checksum(owner), checksum(operator)).call()
            )
        )

    async def create_collection(
        self,
        request: CreateNftCollectionRequest,
        broadcast: bool = False,
        wait_receipt: bool = False,
    ) -> TransactionResult:
        draft = await self.build_create_collection(request)
        return await self._client.tx.send_draft(draft, request.private_key, broadcast, wait_receipt)

    async def build_create_collection(self, request: CreateNftCollectionRequest) -> TransactionDraft:
        """Build reserved collection creation only; no NFT is minted or reserve deposited."""
        self._validate_kind(request.kind)
        if type(request.refundable) is not bool or type(request.burnable) is not bool:
            raise TypeError("refundable and burnable must be bools")
        if not all(isinstance(value, str) and value.strip() for value in (request.symbol, request.name, request.contract_uri)):
            raise ValueError("symbol, name and contract_uri are required")
        creator = address(request.creator or private_key_to_address(request.private_key))
        meta = (creator, request.symbol, request.name, request.contract_uri, request.refundable, request.burnable)
        function = "createDRC721" if request.kind == "erc721" else "createDRC1155"
        data = self._nft_center_contract().get_function_by_name(function)(meta)._encode_transaction_data()
        return await self._client.tx.build_contract_call(
            ContractCallRequest(contract=self._client.config.contracts.nft_center, private_key=request.private_key, data=data)
        )

    async def mint(self, request: MintNftRequest, broadcast: bool = False, wait_receipt: bool = False) -> TransactionResult:
        """Mint separately from creation/approval. Never automatically approve a token."""
        draft = await self.build_mint(request)
        return await self._client.tx.send_draft(draft, request.private_key, broadcast, wait_receipt)

    async def build_mint(self, request: MintNftRequest) -> TransactionDraft:
        """Validate reserve semantics and build mint without approvals, signing or broadcast."""
        self._validate_kind(request.kind)
        address(request.to)
        address(request.nft)
        quantity = uint(request.amount, "amount", positive=True)
        value = uint(request.value_wei, "value_wei")
        reserve = uint(request.reserve_amount_raw, "reserve_amount_raw")
        token = checksum(request.reserve_token)
        if not isinstance(request.token_uri, str) or not request.token_uri.strip():
            raise ValueError("token_uri is required")
        if request.kind == "erc721":
            if quantity != 1 or request.token_id is not None:
                raise ValueError("ERC721 mint creates one auto-assigned ID; amount must be 1 and token_id omitted")
        else:
            uint(request.token_id, "token_id")
        if value and (reserve or token != ZERO_ADDRESS):
            raise ValueError("Choose DEL value_wei or ERC20 reserve, not both")
        state = await self.collection_state(request.nft)
        if not state.active or state.kind != request.kind:
            raise ValueError("NFT collection is inactive or has a different standard")
        if not state.with_reserve:
            if value or reserve or token != ZERO_ADDRESS:
                raise ValueError("A reserveless collection cannot accept a reserve")
        else:
            total = value or reserve
            reserve_type = 1 if value else 2
            if not value:
                address(token)
                if not reserve:
                    raise ValueError("A token reserve must be positive")
                await self.check_reserve_token(token)
            existing = await self.get_reserve(request.nft, request.token_id) if request.kind == "erc1155" else None
            if existing is not None and existing.reserve_type:
                if existing.reserve_type != reserve_type or existing.token != token:
                    raise ValueError("An existing NFT ID must keep its reserve type and token address")
                rate = await self._read_nft_call(request.nft, "nft_1155", "rate", [request.token_id])
                if total != uint(rate, "reserve rate") * quantity:
                    raise ValueError("Existing ID requires total reserve = rate(token_id) * amount")
            else:
                minimum = await self._read_nft_call(request.nft, "nft_721", "MIN_RESERVE")
                if total // quantity < uint(minimum, "minimum reserve", positive=True):
                    raise ValueError("Reserve per NFT is below the contract minimum in raw asset units")
        contract = self._nft_contract(request.kind, request.nft)
        if request.kind == "erc721":
            if request.value_wei:
                data = contract.functions.mintByDEL(checksum(request.to), request.token_uri)._encode_transaction_data()
            else:
                data = contract.functions.mint(
                    checksum(request.to),
                    request.token_uri,
                    int(request.reserve_amount_raw),
                    checksum(request.reserve_token),
                )._encode_transaction_data()
        else:
            if request.token_id is None:
                raise ValueError("token_id is required for ERC1155 mint")
            if request.value_wei:
                data = contract.functions.mintByDEL(
                    checksum(request.to),
                    int(request.token_id),
                    int(request.amount),
                    request.token_uri,
                )._encode_transaction_data()
            else:
                data = contract.functions.mint(
                    checksum(request.to),
                    int(request.token_id),
                    int(request.amount),
                    request.token_uri,
                    int(request.reserve_amount_raw),
                    checksum(request.reserve_token),
                )._encode_transaction_data()
        return await self._client.tx.build_contract_call(
            ContractCallRequest(contract=request.nft, private_key=request.private_key, data=data, value_wei=value)
        )

    async def transfer(
        self,
        request: NftTransferRequest,
        broadcast: bool = False,
        wait_receipt: bool = False,
    ) -> TransactionResult:
        owner = private_key_to_address(request.private_key)
        preflight_error = await self._ownership_error(request.kind, request.nft, owner, request.token_id, request.amount)
        if preflight_error:
            return TransactionResult(success=False, error=preflight_error)
        contract = self._nft_contract(request.kind, request.nft)
        if request.kind == "erc721":
            data = contract.functions.safeTransferFrom(
                owner,
                checksum(request.to),
                int(request.token_id),
            )._encode_transaction_data()
        else:
            data = contract.functions.safeTransferFrom(
                owner,
                checksum(request.to),
                int(request.token_id),
                int(request.amount),
                request.data,
            )._encode_transaction_data()
        return await self._send_contract(request.private_key, request.nft, data, 0, broadcast, wait_receipt)

    async def transfer_batch_erc1155(
        self,
        request: NftBatchTransferRequest,
        broadcast: bool = False,
        wait_receipt: bool = False,
    ) -> TransactionResult:
        if len(request.token_ids) != len(request.amounts):
            return TransactionResult(
                success=False,
                error="ERC1155 batch transfer requires matching token_ids and amounts lengths",
                user_message="Количество NFT и количеств должно совпадать.",
            )
        if not request.token_ids:
            return TransactionResult(
                success=False,
                error="ERC1155 batch transfer requires at least one token",
                user_message="Добавьте хотя бы один NFT для отправки.",
            )
        owner = private_key_to_address(request.private_key)
        for token_id, amount in zip(request.token_ids, request.amounts, strict=True):
            balance = await self.balance_of(request.nft, owner, int(token_id), "erc1155")
            if balance < int(amount):
                return TransactionResult(
                    success=False,
                    error=(
                        "Insufficient ERC1155 balance: "
                        f"token_id={int(token_id)}, balance={balance}, required={int(amount)}, "
                        f"missing={int(amount) - balance}"
                    ),
                    user_message="Недостаточно NFT на балансе.",
                )
        data = self._erc1155_contract(request.nft).functions.safeBatchTransferFrom(
            owner,
            checksum(request.to),
            [int(item) for item in request.token_ids],
            [int(item) for item in request.amounts],
            request.data,
        )._encode_transaction_data()
        return await self._send_contract(request.private_key, request.nft, data, 0, broadcast, wait_receipt)

    async def set_approval_for_all(
        self,
        request: NftApprovalRequest,
        broadcast: bool = False,
        wait_receipt: bool = False,
    ) -> TransactionResult:
        data = self._nft_contract(request.kind, request.nft).functions.setApprovalForAll(
            checksum(request.operator),
            bool(request.approved),
        )._encode_transaction_data()
        return await self._send_contract(request.private_key, request.nft, data, 0, broadcast, wait_receipt)

    async def approve(
        self,
        request: NftApproveRequest,
        broadcast: bool = False,
        wait_receipt: bool = False,
    ) -> TransactionResult:
        owner = private_key_to_address(request.private_key)
        preflight_error = await self._ownership_error("erc721", request.nft, owner, request.token_id, 1)
        if preflight_error:
            return TransactionResult(success=False, error=preflight_error)
        data = self._erc721_contract(request.nft).functions.approve(
            checksum(request.to),
            int(request.token_id),
        )._encode_transaction_data()
        return await self._send_contract(request.private_key, request.nft, data, 0, broadcast, wait_receipt)

    async def burn(
        self,
        request: BurnNftRequest,
        broadcast: bool = False,
        wait_receipt: bool = False,
    ) -> TransactionResult:
        owner = private_key_to_address(request.private_key)
        preflight_error = await self._ownership_error(request.kind, request.nft, owner, request.token_id, request.amount)
        if preflight_error:
            return TransactionResult(success=False, error=preflight_error)
        contract = self._nft_contract(request.kind, request.nft)
        if request.kind == "erc721":
            data = contract.functions.burn(int(request.token_id))._encode_transaction_data()
        else:
            data = contract.functions.burn(int(request.token_id), int(request.amount))._encode_transaction_data()
        return await self._send_contract(request.private_key, request.nft, data, 0, broadcast, wait_receipt)

    async def disable_mint(
        self,
        request: DisableMintNftRequest,
        broadcast: bool = False,
        wait_receipt: bool = False,
    ) -> TransactionResult:
        data = self._nft_contract(request.kind, request.nft).functions.disableMint()._encode_transaction_data()
        return await self._send_contract(request.private_key, request.nft, data, 0, broadcast, wait_receipt)

    async def set_token_uri(
        self,
        request: SetTokenUriNftRequest,
        broadcast: bool = False,
        wait_receipt: bool = False,
    ) -> TransactionResult:
        if request.allow_legacy is not True:
            raise ValueError("setTokenURI is absent from current reviewed NFT ABIs; legacy opt-in is required")
        self._validate_kind(request.kind)
        contract = self._client.web3.eth.contract(address=address(request.nft), abi=self._client.abi.load("legacy"))
        data = contract.functions.setTokenURI(
            uint(request.token_id, "token_id"),
            request.token_uri,
        )._encode_transaction_data()
        return await self._send_contract(request.private_key, request.nft, data, 0, broadcast, wait_receipt)

    async def add_del_reserve(
        self,
        request: AddDelReserveNftRequest,
        broadcast: bool = False,
        wait_receipt: bool = False,
    ) -> TransactionResult:
        data = self._nft_contract(request.kind, request.nft).functions.addReserveByDEL(
            int(request.token_id),
        )._encode_transaction_data()
        return await self._send_contract(
            request.private_key,
            request.nft,
            data,
            int(request.reserve_wei),
            broadcast,
            wait_receipt,
        )

    async def delegate(
        self,
        request: DelegateNftRequest,
        broadcast: bool = False,
        wait_receipt: bool = False,
    ) -> DecimalWorkflowResult:
        return await self._delegate_or_hold(request, None, broadcast, wait_receipt)

    async def hold(
        self,
        request: HoldNftRequest,
        broadcast: bool = False,
        wait_receipt: bool = False,
    ) -> DecimalWorkflowResult:
        return await self._delegate_or_hold(request, request.hold_timestamp, broadcast, wait_receipt)

    async def transfer_stake(
        self,
        request: TransferNftStakeRequest,
        broadcast: bool = False,
        wait_receipt: bool = False,
    ) -> TransactionResult:
        draft = await self.build_transfer_stake(request)
        return await self._client.tx.send_draft(draft, request.private_key, broadcast, wait_receipt)

    async def build_transfer_stake(self, request: TransferNftStakeRequest) -> TransactionDraft:
        contract = self._delegation_nft_contract()
        if self._unified_delegation:
            kind = (await self.collection_state(request.nft)).kind
            if kind == "erc721" and request.amount != 1:
                raise ValueError("ERC721 stake amount must be 1")
            await self._check_unified_stake_amount(request)
            name = "transferNFT" if kind == "erc721" else "transferNFT1155"
            if request.hold_timestamp is not None:
                name = "transferNFTHold" if kind == "erc721" else "transferNFT1155Hold"
            args = [checksum(request.validator), checksum(request.nft),
                    uint(request.token_id, "token_id")]
            if request.hold_timestamp is not None:
                args.append(uint(request.hold_timestamp, "hold_timestamp", positive=True))
            args.append(checksum(request.new_validator))
            data = contract.encode_abi(name, args=args)
            return await self._client.tx.build_contract_call(ContractCallRequest(
                contract=self._client.config.contracts.delegation_nft,
                private_key=request.private_key, data=data,
            ))
        if request.hold_timestamp is None:
            data = contract.functions.transfer(
                checksum(request.validator),
                checksum(request.nft),
                uint(request.token_id, "token_id"),
                uint(request.amount, "amount", positive=True),
                checksum(request.new_validator),
            )._encode_transaction_data()
        else:
            data = contract.functions.transferHold(
                checksum(request.validator),
                checksum(request.nft),
                uint(request.token_id, "token_id"),
                uint(request.amount, "amount", positive=True),
                uint(request.hold_timestamp, "hold_timestamp"),
                checksum(request.new_validator),
            )._encode_transaction_data()
        return await self._client.tx.build_contract_call(ContractCallRequest(
            contract=self._client.config.contracts.delegation_nft, private_key=request.private_key, data=data,
        ))

    async def withdraw(
        self,
        request: WithdrawNftRequest,
        broadcast: bool = False,
        wait_receipt: bool = False,
    ) -> TransactionResult:
        draft = await self.build_withdraw(request)
        return await self._client.tx.send_draft(draft, request.private_key, broadcast, wait_receipt)

    async def build_withdraw(self, request: WithdrawNftRequest) -> TransactionDraft:
        contract = self._delegation_nft_contract()
        if self._unified_delegation:
            kind = (await self.collection_state(request.nft)).kind
            if kind == "erc721" and request.amount != 1:
                raise ValueError("ERC721 stake amount must be 1")
            await self._check_unified_stake_amount(request)
            name = "withdrawNFT" if kind == "erc721" else "withdrawNFT1155"
            if request.hold_timestamp is not None:
                name = "withdrawNFTHold" if kind == "erc721" else "withdrawNFT1155Hold"
            args = [checksum(request.validator), checksum(request.nft),
                    uint(request.token_id, "token_id")]
            if request.hold_timestamp is not None:
                args.append(uint(request.hold_timestamp, "hold_timestamp", positive=True))
            data = contract.encode_abi(name, args=args)
            return await self._client.tx.build_contract_call(ContractCallRequest(
                contract=self._client.config.contracts.delegation_nft,
                private_key=request.private_key, data=data,
            ))
        if request.hold_timestamp is None:
            data = contract.functions.withdraw(
                checksum(request.validator),
                checksum(request.nft),
                uint(request.token_id, "token_id"),
                uint(request.amount, "amount", positive=True),
            )._encode_transaction_data()
        else:
            data = contract.functions.withdrawHold(
                checksum(request.validator),
                checksum(request.nft),
                uint(request.token_id, "token_id"),
                uint(request.amount, "amount", positive=True),
                uint(request.hold_timestamp, "hold_timestamp"),
            )._encode_transaction_data()
        return await self._client.tx.build_contract_call(ContractCallRequest(
            contract=self._client.config.contracts.delegation_nft, private_key=request.private_key, data=data,
        ))

    async def build_operation(self, request: ContractOperationRequest | WithdrawNftRequest | TransferNftStakeRequest | CreateNftCollectionRequest | MintNftRequest) -> TransactionDraft:
        if isinstance(request, CreateNftCollectionRequest):
            return await self.build_create_collection(request)
        if isinstance(request, MintNftRequest):
            return await self.build_mint(request)
        if isinstance(request, WithdrawNftRequest):
            return await self.build_withdraw(request)
        if isinstance(request, TransferNftStakeRequest):
            return await self.build_transfer_stake(request)
        return await super().build_operation(request)

    async def _delegate_or_hold(
        self,
        request: DelegateNftRequest | HoldNftRequest,
        hold_timestamp: int | None,
        broadcast: bool,
        wait_receipt: bool,
    ) -> DecimalWorkflowResult:
        name = "hold_nft" if hold_timestamp is not None else "delegate_nft"
        owner = private_key_to_address(request.private_key)
        preflight_error = await self._ownership_error(request.kind, request.nft, owner, request.token_id, request.amount)
        if preflight_error:
            return _workflow_error(name, preflight_error)
        operator = self._client.config.contracts.delegation_nft
        approval_result: TransactionResult | None = None
        steps: list[str] = []
        if not await self.is_approved_for_all(request.kind, request.nft, owner, operator):
            if not request.auto_approve:
                return DecimalWorkflowResult(
                    success=False,
                    name=name,
                    steps=("approval_required",),
                    expected_steps=2,
                    actual_steps=0,
                    extra_steps_required=True,
                    error="NFT approval is required for delegation contract",
                    user_message="Для делегирования NFT сначала нужно разрешение оператору.",
                )
            if broadcast and not wait_receipt:
                return DecimalWorkflowResult(
                    success=False,
                    name=name,
                    steps=("approval_required",),
                    expected_steps=2,
                    actual_steps=0,
                    extra_steps_required=True,
                    error="Two-step NFT approval requires wait_receipt=True",
                    user_message="Для двухшаговой операции дождитесь подтверждения разрешения.",
                )
            approval_result = await self.set_approval_for_all(
                NftApprovalRequest(
                    kind=request.kind,
                    nft=request.nft,
                    operator=operator,
                    approved=True,
                    private_key=request.private_key,
                ),
                broadcast=broadcast,
                wait_receipt=wait_receipt,
            )
            steps.append("set_approval_for_all")
            if not approval_result.success:
                return DecimalWorkflowResult(False, name, tuple(steps), 1, len(steps), True, None, approval_result, approval_result.error)

        contract = self._delegation_nft_contract()
        if self._unified_delegation:
            if request.kind == "erc721" and request.amount != 1:
                return _workflow_error(name, "ERC721 stake amount must be 1")
            function = ("delegateNFT" if hold_timestamp is None else "delegateNFTHold")
            if request.kind == "erc1155":
                function = "delegateNFT1155" if hold_timestamp is None else "delegateNFT1155Hold"
            args = [checksum(request.validator), checksum(request.nft), int(request.token_id)]
            if request.kind == "erc1155":
                args.append(uint(request.amount, "amount", positive=True))
            if hold_timestamp is not None:
                args.append(uint(hold_timestamp, "hold_timestamp", positive=True))
            data = contract.encode_abi(function, args=args)
            result = await self._send_contract(request.private_key, operator, data, 0, broadcast, wait_receipt)
            steps.append(name)
            return DecimalWorkflowResult(result.success, name, tuple(steps), 1, len(steps), len(steps) > 1, result, approval_result, result.error)
        if request.kind == "erc721":
            if hold_timestamp is None:
                data = contract.functions.delegateDRC721(
                    checksum(request.validator),
                    checksum(request.nft),
                    int(request.token_id),
                )._encode_transaction_data()
            else:
                data = contract.functions.delegateHoldDRC721(
                    checksum(request.validator),
                    checksum(request.nft),
                    int(request.token_id),
                    int(hold_timestamp),
                )._encode_transaction_data()
        elif hold_timestamp is None:
            data = contract.functions.delegateDRC1155(
                checksum(request.validator),
                checksum(request.nft),
                int(request.token_id),
                int(request.amount),
            )._encode_transaction_data()
        else:
            data = contract.functions.delegateHoldDRC1155(
                checksum(request.validator),
                checksum(request.nft),
                int(request.token_id),
                int(request.amount),
                int(hold_timestamp),
            )._encode_transaction_data()
        result = await self._send_contract(request.private_key, operator, data, 0, broadcast, wait_receipt)
        steps.append(name)
        return DecimalWorkflowResult(result.success, name, tuple(steps), 1, len(steps), len(steps) > 1, result, approval_result, result.error)

    async def _ownership_error(self, kind: NftKind, nft: str, owner: str, token_id: int, amount: int) -> str | None:
        if kind == "erc721":
            token_owner = await self.owner_of(nft, token_id)
            if checksum(token_owner) != checksum(owner):
                return f"NFT owner mismatch: owner={token_owner}, expected={checksum(owner)}"
            return None
        balance = await self.balance_of(nft, owner, token_id, "erc1155")
        if balance < int(amount):
            return f"Insufficient ERC1155 balance: balance={balance}, required={int(amount)}, missing={int(amount) - balance}"
        return None

    async def _send_contract(self, private_key: str, contract: str, data: str, value_wei: int, broadcast: bool, wait_receipt: bool) -> TransactionResult:
        draft = await self._client.tx.build_contract_call(
            ContractCallRequest(contract=contract, private_key=private_key, data=data, value_wei=value_wei)
        )
        return await self._client.tx.send_draft(draft, private_key, broadcast, wait_receipt)

    def _nft_center_contract(self):
        return self._client.web3.eth.contract(address=checksum(self._client.config.contracts.nft_center), abi=NFT_CENTER_ABI)

    def _delegation_nft_contract(self):
        abi = self._client.abi.load("delegation_nft_unified") if self._unified_delegation else DELEGATION_NFT_ABI
        return self._client.web3.eth.contract(address=checksum(self._client.config.contracts.delegation_nft), abi=abi)

    async def _check_unified_stake_amount(
        self, request: WithdrawNftRequest | TransferNftStakeRequest,
    ) -> None:
        amount = uint(request.amount, "amount", positive=True)
        owner = private_key_to_address(request.private_key)
        stake = (
            await self.get_stake(request.validator, owner, request.nft, request.token_id)
            if request.hold_timestamp is None
            else await self.get_hold_stake(
                request.validator, owner, request.nft, request.token_id, request.hold_timestamp,
            )
        )
        if not stake.exists or stake.amount_raw != amount:
            raise ValueError(
                "Unified NFT transfer/withdraw moves the entire stake; amount must equal the current stake"
            )

    @property
    def _unified_delegation(self) -> bool:
        contracts = self._client.config.contracts
        return contracts.delegation_nft.lower() == contracts.delegation.lower()

    def _nft_contract(self, kind: NftKind, nft: str, web3=None):
        self._validate_kind(kind)
        return self._erc721_contract(nft, web3) if kind == "erc721" else self._erc1155_contract(nft, web3)

    @staticmethod
    def _validate_kind(kind):
        if kind not in ("erc721", "erc1155"):
            raise ValueError("kind must be erc721 or erc1155")

    def _erc721_contract(self, nft: str, web3=None):
        return (web3 or self._client.web3).eth.contract(address=checksum(nft), abi=ERC721_ABI)

    def _erc1155_contract(self, nft: str, web3=None):
        return (web3 or self._client.web3).eth.contract(address=checksum(nft), abi=ERC1155_ABI)


def _workflow_error(name: str, error: str, extra_steps_required: bool = False) -> DecimalWorkflowResult:
    return DecimalWorkflowResult(
        success=False,
        name=name,
        steps=(),
        expected_steps=1,
        actual_steps=0,
        extra_steps_required=extra_steps_required,
        error=error,
    )
