from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Literal

from .decimal import DecimalWorkflowResult
from .mnemonic import FromMnemonicMixin
from .transactions import ContractCallRequest, TransactionResult
from .wallet import checksum, private_key_to_address


NftKind = Literal["erc721", "erc1155"]


NFT_CENTER_ABI: list[dict[str, Any]] = [
    {
        "inputs": [
            {
                "components": [
                    {"internalType": "address", "name": "creator", "type": "address"},
                    {"internalType": "string", "name": "symbol", "type": "string"},
                    {"internalType": "string", "name": "name", "type": "string"},
                    {"internalType": "string", "name": "contractURI", "type": "string"},
                    {"internalType": "bool", "name": "refundable", "type": "bool"},
                ],
                "internalType": "struct DecimalNFTCenter.NFT",
                "name": "meta",
                "type": "tuple",
            }
        ],
        "name": "createERC721",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function",
    },
    {
        "inputs": [
            {
                "components": [
                    {"internalType": "address", "name": "creator", "type": "address"},
                    {"internalType": "string", "name": "symbol", "type": "string"},
                    {"internalType": "string", "name": "name", "type": "string"},
                    {"internalType": "string", "name": "contractURI", "type": "string"},
                    {"internalType": "bool", "name": "refundable", "type": "bool"},
                ],
                "internalType": "struct DecimalNFTCenter.NFT",
                "name": "meta",
                "type": "tuple",
            }
        ],
        "name": "createERC1155",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function",
    },
]


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


ERC721_ABI: list[dict[str, Any]] = [
    {
        "inputs": [{"internalType": "address", "name": "owner", "type": "address"}],
        "name": "balanceOf",
        "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
        "stateMutability": "view",
        "type": "function",
    },
    {
        "inputs": [{"internalType": "uint256", "name": "tokenId", "type": "uint256"}],
        "name": "ownerOf",
        "outputs": [{"internalType": "address", "name": "", "type": "address"}],
        "stateMutability": "view",
        "type": "function",
    },
    {
        "inputs": [
            {"internalType": "address", "name": "owner", "type": "address"},
            {"internalType": "address", "name": "operator", "type": "address"},
        ],
        "name": "isApprovedForAll",
        "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
        "stateMutability": "view",
        "type": "function",
    },
    {
        "inputs": [{"internalType": "uint256", "name": "tokenId", "type": "uint256"}],
        "name": "getApproved",
        "outputs": [{"internalType": "address", "name": "", "type": "address"}],
        "stateMutability": "view",
        "type": "function",
    },
    {
        "inputs": [
            {"internalType": "address", "name": "operator", "type": "address"},
            {"internalType": "bool", "name": "approved", "type": "bool"},
        ],
        "name": "setApprovalForAll",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function",
    },
    {
        "inputs": [
            {"internalType": "address", "name": "to", "type": "address"},
            {"internalType": "uint256", "name": "tokenId", "type": "uint256"},
        ],
        "name": "approve",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function",
    },
    {
        "inputs": [
            {"internalType": "address", "name": "from", "type": "address"},
            {"internalType": "address", "name": "to", "type": "address"},
            {"internalType": "uint256", "name": "tokenId", "type": "uint256"},
        ],
        "name": "safeTransferFrom",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function",
    },
    {
        "inputs": [
            {"internalType": "address", "name": "recipient", "type": "address"},
            {"internalType": "string", "name": "tokenURI", "type": "string"},
            {"internalType": "uint256", "name": "reserveAmount", "type": "uint256"},
            {"internalType": "address", "name": "reserveToken", "type": "address"},
        ],
        "name": "mint",
        "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
        "stateMutability": "nonpayable",
        "type": "function",
    },
    {
        "inputs": [
            {"internalType": "address", "name": "recipient", "type": "address"},
            {"internalType": "string", "name": "tokenURI", "type": "string"},
        ],
        "name": "mintByETH",
        "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
        "stateMutability": "payable",
        "type": "function",
    },
    {
        "inputs": [{"internalType": "uint256", "name": "tokenId", "type": "uint256"}],
        "name": "burn",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function",
    },
    {
        "inputs": [
            {"internalType": "uint256", "name": "tokenId", "type": "uint256"},
            {"internalType": "string", "name": "tokenURI", "type": "string"},
        ],
        "name": "setTokenURI",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function",
    },
    {
        "inputs": [{"internalType": "uint256", "name": "tokenId", "type": "uint256"}],
        "name": "addReserveByDEL",
        "outputs": [],
        "stateMutability": "payable",
        "type": "function",
    },
    {"inputs": [], "name": "disableMint", "outputs": [], "stateMutability": "nonpayable", "type": "function"},
]


ERC1155_ABI: list[dict[str, Any]] = [
    {
        "inputs": [
            {"internalType": "address", "name": "account", "type": "address"},
            {"internalType": "uint256", "name": "id", "type": "uint256"},
        ],
        "name": "balanceOf",
        "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
        "stateMutability": "view",
        "type": "function",
    },
    {
        "inputs": [
            {"internalType": "address", "name": "account", "type": "address"},
            {"internalType": "address", "name": "operator", "type": "address"},
        ],
        "name": "isApprovedForAll",
        "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
        "stateMutability": "view",
        "type": "function",
    },
    {
        "inputs": [
            {"internalType": "address", "name": "operator", "type": "address"},
            {"internalType": "bool", "name": "approved", "type": "bool"},
        ],
        "name": "setApprovalForAll",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function",
    },
    {
        "inputs": [
            {"internalType": "address", "name": "from", "type": "address"},
            {"internalType": "address", "name": "to", "type": "address"},
            {"internalType": "uint256", "name": "id", "type": "uint256"},
            {"internalType": "uint256", "name": "value", "type": "uint256"},
            {"internalType": "bytes", "name": "data", "type": "bytes"},
        ],
        "name": "safeTransferFrom",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function",
    },
    {
        "inputs": [
            {"internalType": "address", "name": "from", "type": "address"},
            {"internalType": "address", "name": "to", "type": "address"},
            {"internalType": "uint256[]", "name": "ids", "type": "uint256[]"},
            {"internalType": "uint256[]", "name": "values", "type": "uint256[]"},
            {"internalType": "bytes", "name": "data", "type": "bytes"},
        ],
        "name": "safeBatchTransferFrom",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function",
    },
    {
        "inputs": [
            {"internalType": "address", "name": "recipient", "type": "address"},
            {"internalType": "uint256", "name": "tokenId", "type": "uint256"},
            {"internalType": "uint256", "name": "amountToMint", "type": "uint256"},
            {"internalType": "string", "name": "tokenURI", "type": "string"},
            {"internalType": "uint256", "name": "reserveAmount", "type": "uint256"},
            {"internalType": "address", "name": "reserveToken", "type": "address"},
        ],
        "name": "mint",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function",
    },
    {
        "inputs": [
            {"internalType": "address", "name": "recipient", "type": "address"},
            {"internalType": "uint256", "name": "tokenId", "type": "uint256"},
            {"internalType": "uint256", "name": "amountToMint", "type": "uint256"},
            {"internalType": "string", "name": "tokenURI", "type": "string"},
        ],
        "name": "mintByETH",
        "outputs": [],
        "stateMutability": "payable",
        "type": "function",
    },
    {
        "inputs": [
            {"internalType": "uint256", "name": "tokenId", "type": "uint256"},
            {"internalType": "uint256", "name": "amount", "type": "uint256"},
        ],
        "name": "burn",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function",
    },
    {
        "inputs": [
            {"internalType": "uint256", "name": "tokenId", "type": "uint256"},
            {"internalType": "string", "name": "tokenURI", "type": "string"},
        ],
        "name": "setTokenURI",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function",
    },
    {
        "inputs": [{"internalType": "uint256", "name": "tokenId", "type": "uint256"}],
        "name": "addReserveByDEL",
        "outputs": [],
        "stateMutability": "payable",
        "type": "function",
    },
    {"inputs": [], "name": "disableMint", "outputs": [], "stateMutability": "nonpayable", "type": "function"},
]


@dataclass(frozen=True)
class CreateNftCollectionRequest(FromMnemonicMixin):
    kind: NftKind
    symbol: str
    name: str
    contract_uri: str
    private_key: str = field(repr=False)
    refundable: bool = False
    creator: str | None = None


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
    auto_approve: bool = True


@dataclass(frozen=True)
class HoldNftRequest(FromMnemonicMixin):
    kind: NftKind
    nft: str
    validator: str
    token_id: int
    hold_timestamp: int
    private_key: str = field(repr=False)
    amount: int = 1
    auto_approve: bool = True


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


class NftService:
    def __init__(self, client) -> None:
        self._client = client

    async def owner_of(self, nft: str, token_id: int) -> str:
        contract = self._erc721_contract(nft)
        return await self._client.rpc.call(lambda _w3: contract.functions.ownerOf(int(token_id)).call())

    async def balance_of(self, nft: str, owner: str, token_id: int | None = None, kind: NftKind = "erc721") -> int:
        if kind == "erc721":
            contract = self._erc721_contract(nft)
            return int(await self._client.rpc.call(lambda _w3: contract.functions.balanceOf(checksum(owner)).call()))
        if token_id is None:
            raise ValueError("token_id is required for ERC1155 balanceOf")
        contract = self._erc1155_contract(nft)
        return int(await self._client.rpc.call(lambda _w3: contract.functions.balanceOf(checksum(owner), int(token_id)).call()))

    async def is_approved_for_all(self, kind: NftKind, nft: str, owner: str, operator: str) -> bool:
        contract = self._nft_contract(kind, nft)
        return bool(
            await self._client.rpc.call(
                lambda _w3: contract.functions.isApprovedForAll(checksum(owner), checksum(operator)).call()
            )
        )

    async def create_collection(
        self,
        request: CreateNftCollectionRequest,
        broadcast: bool = False,
        wait_receipt: bool = False,
    ) -> TransactionResult:
        creator = checksum(request.creator or private_key_to_address(request.private_key))
        meta = (creator, request.symbol, request.name, request.contract_uri, bool(request.refundable))
        contract = self._nft_center_contract()
        function = contract.functions.createERC721 if request.kind == "erc721" else contract.functions.createERC1155
        data = function(meta)._encode_transaction_data()
        return await self._send_contract(
            request.private_key,
            self._client.config.contracts.nft_center,
            data,
            0,
            broadcast,
            wait_receipt,
        )

    async def mint(self, request: MintNftRequest, broadcast: bool = False, wait_receipt: bool = False) -> TransactionResult:
        contract = self._nft_contract(request.kind, request.nft)
        if request.kind == "erc721":
            if request.value_wei:
                data = contract.functions.mintByETH(checksum(request.to), request.token_uri)._encode_transaction_data()
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
                data = contract.functions.mintByETH(
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
        return await self._send_contract(request.private_key, request.nft, data, int(request.value_wei), broadcast, wait_receipt)

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
        data = self._nft_contract(request.kind, request.nft).functions.setTokenURI(
            int(request.token_id),
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
        contract = self._delegation_nft_contract()
        if request.hold_timestamp is None:
            data = contract.functions.transfer(
                checksum(request.validator),
                checksum(request.nft),
                int(request.token_id),
                int(request.amount),
                checksum(request.new_validator),
            )._encode_transaction_data()
        else:
            data = contract.functions.transferHold(
                checksum(request.validator),
                checksum(request.nft),
                int(request.token_id),
                int(request.amount),
                int(request.hold_timestamp),
                checksum(request.new_validator),
            )._encode_transaction_data()
        return await self._send_contract(request.private_key, self._client.config.contracts.delegation_nft, data, 0, broadcast, wait_receipt)

    async def withdraw(
        self,
        request: WithdrawNftRequest,
        broadcast: bool = False,
        wait_receipt: bool = False,
    ) -> TransactionResult:
        contract = self._delegation_nft_contract()
        if request.hold_timestamp is None:
            data = contract.functions.withdraw(
                checksum(request.validator),
                checksum(request.nft),
                int(request.token_id),
                int(request.amount),
            )._encode_transaction_data()
        else:
            data = contract.functions.withdrawHold(
                checksum(request.validator),
                checksum(request.nft),
                int(request.token_id),
                int(request.amount),
                int(request.hold_timestamp),
            )._encode_transaction_data()
        return await self._send_contract(request.private_key, self._client.config.contracts.delegation_nft, data, 0, broadcast, wait_receipt)

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
                return _workflow_error(name, "NFT approval is required for delegation contract", True)
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
        return self._client.web3.eth.contract(address=checksum(self._client.config.contracts.delegation_nft), abi=DELEGATION_NFT_ABI)

    def _nft_contract(self, kind: NftKind, nft: str):
        return self._erc721_contract(nft) if kind == "erc721" else self._erc1155_contract(nft)

    def _erc721_contract(self, nft: str):
        return self._client.web3.eth.contract(address=checksum(nft), abi=ERC721_ABI)

    def _erc1155_contract(self, nft: str):
        return self._client.web3.eth.contract(address=checksum(nft), abi=ERC1155_ABI)


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
