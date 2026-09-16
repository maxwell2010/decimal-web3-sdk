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

    @property
    def raw_string(self) -> str:
        return str(self.raw)

    @property
    def formatted_string(self) -> str:
        return format_units_string(self.raw, self.token.decimals)

    def as_dict(self) -> dict[str, object]:
        """Return a JSON-safe balance without converting amounts to float."""
        return {
            "token": {
                "address": self.token.address,
                "name": self.token.name,
                "symbol": self.token.symbol,
                "decimals": self.token.decimals,
            },
            "owner": self.owner,
            "raw": self.raw_string,
            "formatted": self.formatted_string,
        }


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
        decimals = await self._call(lambda w3: self._contract(address, w3).functions.decimals().call())
        name = await self._safe_call(lambda w3: self._contract(address, w3).functions.name().call())
        symbol = await self._safe_call(lambda w3: self._contract(address, w3).functions.symbol().call())
        return TokenInfo(address=address, name=name, symbol=symbol, decimals=int(decimals))

    async def balance(self, token_address: str, owner: str) -> TokenBalance:
        token = await self.info(token_address)
        owner_address = checksum(owner)
        raw = await self._call(lambda w3: self._contract(token.address, w3).functions.balanceOf(owner_address).call())
        return TokenBalance(
            token=token,
            owner=owner_address,
            raw=int(raw),
            formatted=format_units(int(raw), token.decimals),
        )

    async def allowance(self, token_address: str, owner: str, spender: str) -> int:
        return int(
            await self._call(
                lambda w3: self._contract(token_address, w3).functions.allowance(checksum(owner), checksum(spender)).call()
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
        owner = checksum(owner)
        spender = checksum(spender)
        try:
            nonce = int(await self._call(lambda w3: self._contract(token_address, w3).functions.nonces(owner).call()))
        except Exception:
            return None
        name = await self._safe_call(lambda w3: self._contract(token_address, w3).functions.name().call()) or "Token"
        version = await self._safe_call(lambda w3: self._contract(token_address, w3).functions.version().call()) or "1"
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

    def _contract(self, token_address: str, web3=None):
        return (web3 or self._client.web3).eth.contract(address=checksum(token_address), abi=ERC20_ABI)

    async def _call(self, fn):
        return await self._client.rpc.call(fn)

    async def _safe_call(self, fn):
        try:
            return await self._call(fn)
        except Exception:
            return None


def format_units_string(value: int, decimals: int) -> str:
    """Format integer base units exactly, without Decimal context rounding."""
    if not isinstance(value, int) or isinstance(value, bool):
        raise TypeError("value must be an integer")
    integer = int(value)
    if integer != value:
        raise ValueError("value must be an integer")
    places = _decimal_places(decimals)
    if places == 0:
        return str(integer)

    digits = str(abs(integer)).rjust(places + 1, "0")
    whole = digits[:-places]
    fraction = digits[-places:].rstrip("0")
    formatted = whole if not fraction else f"{whole}.{fraction}"
    if integer < 0:
        return f"-{formatted}"
    return formatted


def format_units(value: int, decimals: int) -> Decimal:
    return Decimal(format_units_string(value, decimals))


def parse_units(value: Decimal | str | int, decimals: int) -> int:
    places = _decimal_places(decimals)
    if isinstance(value, (float, bool)):
        raise TypeError("Use str, int or Decimal for exact amounts, not float or bool")
    amount = Decimal(str(value))
    if not amount.is_finite():
        raise ValueError("Amount must be finite")
    numerator, denominator = amount.as_integer_ratio()
    scaled_numerator = numerator * (10**places)
    if scaled_numerator % denominator:
        raise ValueError(f"Amount has more than {places} decimal places")
    return scaled_numerator // denominator


def _decimal_places(decimals: int) -> int:
    if not isinstance(decimals, int) or isinstance(decimals, bool) or not 0 <= decimals <= 255:
        raise ValueError("decimals must be an integer between 0 and 255")
    return decimals


def _sum_amounts(values) -> Decimal:
    items = [Decimal(value) for value in values]
    if not items:
        return Decimal(0)
    if any(not value.is_finite() for value in items):
        raise ValueError("Amounts must be finite")
    exponent = min(value.as_tuple().exponent for value in items)
    total = 0
    for value in items:
        sign, digits, scale = value.as_tuple()
        coefficient = int("".join(map(str, digits)))
        total += (-coefficient if sign else coefficient) * 10 ** (scale - exponent)
    return Decimal((int(total < 0), tuple(map(int, str(abs(total)))), exponent))
