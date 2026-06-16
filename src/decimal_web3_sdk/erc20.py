from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal
from typing import Any

from eth_account import Account
from eth_account.messages import encode_typed_data
from web3 import Web3

from .wallet import checksum, normalize_private_key


ERC20_ABI: list[dict[str, Any]] = [
    {
        "constant": True,
        "inputs": [{"name": "account", "type": "address"}],
        "name": "balanceOf",
        "outputs": [{"name": "", "type": "uint256"}],
        "type": "function",
    },
    {
        "constant": True,
        "inputs": [],
        "name": "decimals",
        "outputs": [{"name": "", "type": "uint8"}],
        "type": "function",
    },
    {
        "constant": True,
        "inputs": [],
        "name": "symbol",
        "outputs": [{"name": "", "type": "string"}],
        "type": "function",
    },
    {
        "constant": True,
        "inputs": [],
        "name": "name",
        "outputs": [{"name": "", "type": "string"}],
        "type": "function",
    },
    {
        "constant": True,
        "inputs": [
            {"name": "owner", "type": "address"},
            {"name": "spender", "type": "address"},
        ],
        "name": "allowance",
        "outputs": [{"name": "", "type": "uint256"}],
        "type": "function",
    },
    {
        "constant": True,
        "inputs": [{"name": "owner", "type": "address"}],
        "name": "nonces",
        "outputs": [{"name": "", "type": "uint256"}],
        "type": "function",
    },
    {
        "constant": True,
        "inputs": [],
        "name": "version",
        "outputs": [{"name": "", "type": "string"}],
        "type": "function",
    },
    {
        "constant": False,
        "inputs": [
            {"name": "to", "type": "address"},
            {"name": "value", "type": "uint256"},
        ],
        "name": "transfer",
        "outputs": [{"name": "", "type": "bool"}],
        "type": "function",
    },
    {
        "constant": False,
        "inputs": [
            {"name": "from", "type": "address"},
            {"name": "to", "type": "address"},
            {"name": "value", "type": "uint256"},
        ],
        "name": "transferFrom",
        "outputs": [{"name": "", "type": "bool"}],
        "type": "function",
    },
    {
        "constant": False,
        "inputs": [
            {"name": "owner", "type": "address"},
            {"name": "spender", "type": "address"},
            {"name": "value", "type": "uint256"},
            {"name": "deadline", "type": "uint256"},
            {"name": "v", "type": "uint8"},
            {"name": "r", "type": "bytes32"},
            {"name": "s", "type": "bytes32"},
        ],
        "name": "permit",
        "outputs": [],
        "type": "function",
    },
    {
        "constant": False,
        "inputs": [
            {"name": "spender", "type": "address"},
            {"name": "value", "type": "uint256"},
        ],
        "name": "approve",
        "outputs": [{"name": "", "type": "bool"}],
        "type": "function",
    },
]


@dataclass(frozen=True)
class TokenInfo:
    address: str
    name: str | None
    symbol: str | None
    decimals: int


@dataclass(frozen=True)
class TokenBalance:
    token: TokenInfo
    owner: str
    raw: int
    formatted: Decimal


@dataclass(frozen=True)
class PermitSignature:
    deadline: int
    v: int
    r: bytes
    s: bytes


class Erc20Service:
    def __init__(self, client) -> None:
        self._client = client

    async def info(self, token_address: str) -> TokenInfo:
        address = checksum(token_address)
        contract = self._contract(address)
        decimals = await self._call(lambda: contract.functions.decimals().call())
        name = await self._safe_call(lambda: contract.functions.name().call())
        symbol = await self._safe_call(lambda: contract.functions.symbol().call())
        return TokenInfo(address=address, name=name, symbol=symbol, decimals=int(decimals))

    async def balance(self, token_address: str, owner: str) -> TokenBalance:
        token = await self.info(token_address)
        owner_address = checksum(owner)
        contract = self._contract(token.address)
        raw = await self._call(lambda: contract.functions.balanceOf(owner_address).call())
        return TokenBalance(
            token=token,
            owner=owner_address,
            raw=int(raw),
            formatted=format_units(int(raw), token.decimals),
        )

    async def allowance(self, token_address: str, owner: str, spender: str) -> int:
        contract = self._contract(token_address)
        return int(
            await self._call(
                lambda: contract.functions.allowance(checksum(owner), checksum(spender)).call()
            )
        )

    async def permit_signature(
        self,
        token_address: str,
        owner: str,
        spender: str,
        value_raw: int,
        deadline: int,
        private_key: str,
    ) -> PermitSignature | None:
        contract = self._contract(token_address)
        owner = checksum(owner)
        spender = checksum(spender)
        try:
            nonce = int(await self._call(lambda: contract.functions.nonces(owner).call()))
        except Exception:
            return None
        name = await self._safe_call(lambda: contract.functions.name().call()) or "Token"
        version = await self._safe_call(lambda: contract.functions.version().call()) or "1"
        chain_id = int(self._client.config.chain_id)
        message = {
            "types": {
                "EIP712Domain": [
                    {"name": "name", "type": "string"},
                    {"name": "version", "type": "string"},
                    {"name": "chainId", "type": "uint256"},
                    {"name": "verifyingContract", "type": "address"},
                ],
                "Permit": [
                    {"name": "owner", "type": "address"},
                    {"name": "spender", "type": "address"},
                    {"name": "value", "type": "uint256"},
                    {"name": "nonce", "type": "uint256"},
                    {"name": "deadline", "type": "uint256"},
                ],
            },
            "primaryType": "Permit",
            "domain": {
                "name": str(name),
                "version": str(version),
                "chainId": chain_id,
                "verifyingContract": checksum(token_address),
            },
            "message": {
                "owner": owner,
                "spender": spender,
                "value": int(value_raw),
                "nonce": nonce,
                "deadline": int(deadline),
            },
        }
        try:
            signable = encode_typed_data(full_message=message)
            signed = Account.sign_message(signable, normalize_private_key(private_key))
            return PermitSignature(
                deadline=int(deadline),
                v=int(signed.v),
                r=int(signed.r).to_bytes(32, "big"),
                s=int(signed.s).to_bytes(32, "big"),
            )
        except Exception:
            return None

    def build_transfer_data(self, token_address: str, to: str, amount_raw: int) -> str:
        contract = self._contract(token_address)
        return contract.functions.transfer(checksum(to), int(amount_raw))._encode_transaction_data()

    def build_approve_data(self, token_address: str, spender: str, amount_raw: int) -> str:
        contract = self._contract(token_address)
        return contract.functions.approve(checksum(spender), int(amount_raw))._encode_transaction_data()

    def build_transfer_from_data(self, token_address: str, owner: str, to: str, amount_raw: int) -> str:
        contract = self._contract(token_address)
        return contract.functions.transferFrom(
            checksum(owner), checksum(to), int(amount_raw)
        )._encode_transaction_data()

    def build_permit_data(
        self,
        token_address: str,
        owner: str,
        spender: str,
        value_raw: int,
        permit: PermitSignature,
    ) -> str:
        contract = self._contract(token_address)
        return contract.functions.permit(
            checksum(owner),
            checksum(spender),
            int(value_raw),
            int(permit.deadline),
            int(permit.v),
            permit.r,
            permit.s,
        )._encode_transaction_data()

    def _contract(self, token_address: str):
        return self._client.web3.eth.contract(address=checksum(token_address), abi=ERC20_ABI)

    async def _call(self, fn):
        return await self._client.rpc.call(lambda _w3: fn())

    async def _safe_call(self, fn):
        try:
            return await self._call(fn)
        except Exception:
            return None


def format_units(value: int, decimals: int) -> Decimal:
    return Decimal(value) / (Decimal(10) ** int(decimals))


def parse_units(value: Decimal | str | int | float, decimals: int) -> int:
    return int(Decimal(str(value)) * (Decimal(10) ** int(decimals)))
