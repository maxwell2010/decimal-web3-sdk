from __future__ import annotations

from dataclasses import dataclass, field
from decimal import Decimal
from typing import Any

from web3 import Web3
from web3.logs import DISCARD

from .decimal import DecimalWorkflowResult
from .erc20 import parse_units
from .mnemonic import FromMnemonicMixin
from .token_operations import TokenOperations
from .transactions import ContractCallRequest, Erc20ApproveRequest, TransactionResult, _token_preflight_failure
from .wallet import checksum, private_key_to_address


TOKEN_CREATION_MIN_RESERVE_DEL = Decimal("1000")
TOKEN_CREATION_COMMISSION_BY_SYMBOL_LENGTH: dict[int, Decimal] = {
    3: Decimal("2500000"),
    4: Decimal("250000"),
    5: Decimal("25000"),
    6: Decimal("2500"),
}
TOKEN_CREATION_DEFAULT_COMMISSION_DEL = Decimal("250")


DECIMAL_TOKEN_ABI: list[dict[str, Any]] = [
    {
        "inputs": [
            {"internalType": "uint256", "name": "amountOutMin", "type": "uint256"},
            {"internalType": "address", "name": "recipient", "type": "address"},
        ],
        "name": "buy",
        "outputs": [],
        "stateMutability": "payable",
        "type": "function",
    },
    {
        "inputs": [
            {"internalType": "uint256", "name": "amountIn", "type": "uint256"},
            {"internalType": "uint256", "name": "amountOutMin", "type": "uint256"},
            {"internalType": "address", "name": "recipient", "type": "address"},
        ],
        "name": "sell",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function",
    },
    {
        "inputs": [{"internalType": "uint256", "name": "value", "type": "uint256"}],
        "name": "burn",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function",
    },
    {
        "inputs": [
            {"internalType": "address", "name": "to", "type": "address"},
            {"internalType": "uint256", "name": "amount", "type": "uint256"},
        ],
        "name": "mint",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function",
    },
    {
        "inputs": [
            {"internalType": "string", "name": "newIdentity", "type": "string"},
            {"internalType": "uint256", "name": "newMaxTotalSupply", "type": "uint256"},
        ],
        "name": "updateDetails",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function",
    },
]


TOKEN_CENTER_ABI: list[dict[str, Any]] = [
    {
        "anonymous": False,
        "inputs": [
            {
                "indexed": False,
                "internalType": "address",
                "name": "tokenAddress",
                "type": "address",
            }
        ],
        "name": "TokenDeployed",
        "type": "event",
    },
    {
        "anonymous": False,
        "inputs": [
            {
                "indexed": False,
                "internalType": "address",
                "name": "tokenAddress",
                "type": "address",
            }
        ],
        "name": "TokenReservelessDeployed",
        "type": "event",
    },
    {
        "inputs": [{"internalType": "string", "name": "symbol", "type": "string"}],
        "name": "tokens",
        "outputs": [{"internalType": "address", "name": "", "type": "address"}],
        "stateMutability": "view",
        "type": "function",
    },
    {
        "inputs": [{"internalType": "address", "name": "token", "type": "address"}],
        "name": "isTokenExists",
        "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
        "stateMutability": "view",
        "type": "function",
    },
    {
        "inputs": [
            {
                "components": [
                    {"internalType": "uint256", "name": "initialMint", "type": "uint256"},
                    {"internalType": "uint256", "name": "minTotalSupply", "type": "uint256"},
                    {"internalType": "uint256", "name": "maxTotalSupply", "type": "uint256"},
                    {"internalType": "address", "name": "creator", "type": "address"},
                    {"internalType": "uint8", "name": "crr", "type": "uint8"},
                    {"internalType": "string", "name": "identity", "type": "string"},
                    {"internalType": "string", "name": "symbol", "type": "string"},
                    {"internalType": "string", "name": "name", "type": "string"},
                ],
                "internalType": "struct DecimalTokenCenter.Meta",
                "name": "meta",
                "type": "tuple",
            }
        ],
        "name": "createToken",
        "outputs": [],
        "stateMutability": "payable",
        "type": "function",
    },
    {
        "inputs": [
            {"internalType": "address payable", "name": "tokenIn", "type": "address"},
            {"internalType": "address payable", "name": "tokenOut", "type": "address"},
            {"internalType": "uint256", "name": "amountIn", "type": "uint256"},
            {"internalType": "uint256", "name": "amountOutMin", "type": "uint256"},
            {"internalType": "address", "name": "recipient", "type": "address"},
        ],
        "name": "convert",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function",
    },
    {
        "inputs": [
            {"internalType": "address payable", "name": "tokenIn", "type": "address"},
            {"internalType": "address payable", "name": "tokenOut", "type": "address"},
            {"internalType": "uint256", "name": "amountIn", "type": "uint256"},
            {"internalType": "uint256", "name": "amountOutMin", "type": "uint256"},
            {"internalType": "address", "name": "recipient", "type": "address"},
            {"internalType": "uint256", "name": "deadline", "type": "uint256"},
            {"internalType": "uint8", "name": "v", "type": "uint8"},
            {"internalType": "bytes32", "name": "r", "type": "bytes32"},
            {"internalType": "bytes32", "name": "s", "type": "bytes32"},
        ],
        "name": "convert",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function",
    },
    {
        "inputs": [
            {"internalType": "string", "name": "name", "type": "string"},
            {"internalType": "string", "name": "symbol", "type": "string"},
            {"internalType": "bool", "name": "mintable", "type": "bool"},
            {"internalType": "bool", "name": "burnable", "type": "bool"},
            {"internalType": "uint256", "name": "initialMint", "type": "uint256"},
            {"internalType": "uint256", "name": "cap", "type": "uint256"},
            {"internalType": "string", "name": "identity", "type": "string"},
        ],
        "name": "createTokenReserveless",
        "outputs": [{"internalType": "address", "name": "", "type": "address"}],
        "stateMutability": "nonpayable",
        "type": "function",
    },
]


@dataclass(frozen=True)
class BuyTokenRequest(FromMnemonicMixin):
    token: str
    amount_del: Decimal | str | int
    private_key: str = field(repr=False)
    min_amount_out_raw: int = 0


@dataclass(frozen=True)
class SellTokenRequest(FromMnemonicMixin):
    token: str
    amount: Decimal | str | int
    private_key: str = field(repr=False)
    min_amount_del_out_wei: int = 1
    decimals: int | None = None


@dataclass(frozen=True)
class ConvertTokenRequest(FromMnemonicMixin):
    token_in: str
    token_out: str
    amount_in: Decimal | str | int
    min_amount_out: Decimal | str | int
    private_key: str = field(repr=False)
    token_in_decimals: int | None = None
    token_out_decimals: int | None = None
    auto_approve: bool = True
    prefer_permit: bool = True
    permit_deadline: int = 2**256 - 1


@dataclass(frozen=True)
class BurnTokenRequest(FromMnemonicMixin):
    token: str
    amount: Decimal | str | int
    private_key: str = field(repr=False)
    decimals: int | None = None


@dataclass(frozen=True)
class MintTokenRequest(FromMnemonicMixin):
    token: str
    to: str
    amount: Decimal | str | int
    private_key: str = field(repr=False)
    decimals: int | None = None


@dataclass(frozen=True)
class UpdateTokenDetailsRequest(FromMnemonicMixin):
    token: str
    identity: str
    max_total_supply_raw: int
    private_key: str = field(repr=False)


@dataclass(frozen=True)
class CreateReservelessTokenRequest(FromMnemonicMixin):
    name: str
    symbol: str
    mintable: bool
    burnable: bool
    initial_mint_raw: int
    cap_raw: int
    identity: str
    private_key: str = field(repr=False)


@dataclass(frozen=True)
class CreateTokenRequest(FromMnemonicMixin):
    name: str
    symbol: str
    initial_mint_raw: int
    min_total_supply_raw: int
    max_total_supply_raw: int
    crr: int
    identity: str
    private_key: str = field(repr=False)
    reserve_value_wei: int | None = None
    creator: str | None = None


class TokenService(TokenOperations):
    def __init__(self, client) -> None:
        self._client = client

    async def buy(
        self,
        request: BuyTokenRequest,
        broadcast: bool = False,
        wait_receipt: bool = False,
    ) -> TransactionResult:
        data = self._token_contract(request.token).functions.buy(
            int(request.min_amount_out_raw),
            private_key_to_address(request.private_key),
        )._encode_transaction_data()
        return await self._send_contract(
            request.private_key,
            request.token,
            data,
            _del_to_wei(request.amount_del),
            broadcast,
            wait_receipt,
        )

    async def sell(
        self,
        request: SellTokenRequest,
        broadcast: bool = False,
        wait_receipt: bool = False,
    ) -> TransactionResult:
        decimals = request.decimals
        if decimals is None:
            decimals = (await self._client.erc20.info(request.token)).decimals
        amount_raw = _parse_units(request.amount, decimals)
        owner = private_key_to_address(request.private_key)
        balance = await self._client.erc20.balance(request.token, owner)
        if int(balance.raw) < amount_raw:
            return _token_preflight_failure(int(balance.raw), amount_raw)
        data = self._token_contract(request.token).functions.sell(
            amount_raw,
            int(request.min_amount_del_out_wei),
            owner,
        )._encode_transaction_data()
        return await self._send_contract(request.private_key, request.token, data, 0, broadcast, wait_receipt)

    async def convert(
        self,
        request: ConvertTokenRequest,
        broadcast: bool = False,
        wait_receipt: bool = False,
    ) -> DecimalWorkflowResult:
        try:
            if checksum(request.token_in) == checksum(request.token_out):
                return _workflow_error("convert_erc20", "token_in and token_out must be different")
            in_decimals = request.token_in_decimals
            if in_decimals is None:
                in_decimals = (await self._client.erc20.info(request.token_in)).decimals
            out_decimals = request.token_out_decimals
            if out_decimals is None:
                out_decimals = (await self._client.erc20.info(request.token_out)).decimals
            amount_raw = _parse_units(request.amount_in, in_decimals)
            min_out_raw = _parse_units(request.min_amount_out, out_decimals)
            owner = private_key_to_address(request.private_key)
            balance = await self._client.erc20.balance(request.token_in, owner)
            if int(balance.raw) < amount_raw:
                failure = _token_preflight_failure(int(balance.raw), amount_raw)
                return DecimalWorkflowResult(False, "convert_erc20", ("token_balance_preflight",), 1, 0, False, failure, None, failure.error)

            spender = self._client.config.contracts.token_center
            allowance = await self._client.erc20.allowance(request.token_in, owner, spender)
            steps: list[str] = []
            approve_result: TransactionResult | None = None
            if allowance < amount_raw:
                if request.prefer_permit:
                    permit = await self._client.erc20.permit_signature(
                        request.token_in,
                        owner,
                        spender,
                        amount_raw,
                        request.permit_deadline,
                        request.private_key,
                    )
                    if permit is not None:
                        signature = "convert(address,address,uint256,uint256,address,uint256,uint8,bytes32,bytes32)"
                        function = self._token_center_contract().get_function_by_signature(signature)
                        data = function(
                            checksum(request.token_in),
                            checksum(request.token_out),
                            amount_raw,
                            min_out_raw,
                            owner,
                            permit.deadline,
                            permit.v,
                            permit.r,
                            permit.s,
                        )._encode_transaction_data()
                        result = await self._send_contract(
                            request.private_key,
                            spender,
                            data,
                            0,
                            broadcast,
                            wait_receipt,
                        )
                        return DecimalWorkflowResult(
                            result.success,
                            "convert_erc20",
                            ("convert_erc20_by_permit",),
                            1,
                            1,
                            False,
                            result,
                            None,
                            result.error,
                        )
                if not request.auto_approve:
                    return _workflow_error("convert_erc20", f"ERC20 allowance is insufficient: allowance_raw={allowance}, required_raw={amount_raw}", True)
                approve_result = await self._client.tx.approve_erc20(
                    Erc20ApproveRequest(
                        token=request.token_in,
                        spender=spender,
                        amount=request.amount_in,
                        private_key=request.private_key,
                        decimals=in_decimals,
                    ),
                    broadcast=broadcast,
                    wait_receipt=wait_receipt,
                )
                steps.append("approve_erc20")
                if not approve_result.success:
                    return DecimalWorkflowResult(False, "convert_erc20", tuple(steps), 1, len(steps), True, None, approve_result, approve_result.error)

            signature = "convert(address,address,uint256,uint256,address)"
            function = self._token_center_contract().get_function_by_signature(signature)
            data = function(
                checksum(request.token_in),
                checksum(request.token_out),
                amount_raw,
                min_out_raw,
                owner,
            )._encode_transaction_data()
            result = await self._send_contract(request.private_key, spender, data, 0, broadcast, wait_receipt)
            steps.append("convert_erc20")
            return DecimalWorkflowResult(
                result.success,
                "convert_erc20",
                tuple(steps),
                1,
                len(steps),
                len(steps) > 1,
                result,
                approve_result,
                result.error,
            )
        except Exception as exc:
            return _workflow_error("convert_erc20", str(exc))

    async def burn(self, request: BurnTokenRequest, broadcast: bool = False, wait_receipt: bool = False) -> TransactionResult:
        decimals = request.decimals
        if decimals is None:
            decimals = (await self._client.erc20.info(request.token)).decimals
        amount_raw = _parse_units(request.amount, decimals)
        owner = private_key_to_address(request.private_key)
        balance = await self._client.erc20.balance(request.token, owner)
        if int(balance.raw) < amount_raw:
            return _token_preflight_failure(int(balance.raw), amount_raw)
        data = self._token_contract(request.token).functions.burn(amount_raw)._encode_transaction_data()
        return await self._send_contract(request.private_key, request.token, data, 0, broadcast, wait_receipt)

    async def mint(self, request: MintTokenRequest, broadcast: bool = False, wait_receipt: bool = False) -> TransactionResult:
        decimals = request.decimals
        if decimals is None:
            decimals = (await self._client.erc20.info(request.token)).decimals
        amount_raw = _parse_units(request.amount, decimals)
        data = self._token_contract(request.token).functions.mint(checksum(request.to), amount_raw)._encode_transaction_data()
        return await self._send_contract(request.private_key, request.token, data, 0, broadcast, wait_receipt)

    async def update_details(self, request: UpdateTokenDetailsRequest, broadcast: bool = False, wait_receipt: bool = False) -> TransactionResult:
        data = self._token_contract(request.token).functions.updateDetails(
            request.identity,
            int(request.max_total_supply_raw),
        )._encode_transaction_data()
        return await self._send_contract(request.private_key, request.token, data, 0, broadcast, wait_receipt)

    async def create_reserveless(
        self,
        request: CreateReservelessTokenRequest,
        broadcast: bool = False,
        wait_receipt: bool = False,
    ) -> TransactionResult:
        data = self._token_center_contract().functions.createTokenReserveless(
            request.name,
            request.symbol,
            bool(request.mintable),
            bool(request.burnable),
            int(request.initial_mint_raw),
            int(request.cap_raw),
            request.identity,
        )._encode_transaction_data()
        result = await self._send_contract(
            request.private_key,
            self._client.config.contracts.token_center,
            data,
            0,
            broadcast,
            wait_receipt,
        )
        return await self._with_created_token_metadata(result, request.symbol)

    async def create(
        self,
        request: CreateTokenRequest,
        broadcast: bool = False,
        wait_receipt: bool = False,
    ) -> TransactionResult:
        creator = checksum(request.creator or private_key_to_address(request.private_key))
        meta = (
            int(request.initial_mint_raw),
            int(request.min_total_supply_raw),
            int(request.max_total_supply_raw),
            creator,
            int(request.crr),
            request.identity,
            request.symbol,
            request.name,
        )
        data = self._token_center_contract().functions.createToken(meta)._encode_transaction_data()
        result = await self._send_contract(
            request.private_key,
            self._client.config.contracts.token_center,
            data,
            int(request.reserve_value_wei)
            if request.reserve_value_wei is not None
            else token_creation_required_reserve_wei(request.symbol),
            broadcast,
            wait_receipt,
        )
        return await self._with_created_token_metadata(result, request.symbol)

    async def _send_contract(self, private_key: str, contract: str, data: str, value_wei: int, broadcast: bool, wait_receipt: bool) -> TransactionResult:
        draft = await self._client.tx.build_contract_call(
            ContractCallRequest(contract=contract, private_key=private_key, data=data, value_wei=value_wei)
        )
        return await self._client.tx.send_draft(draft, private_key, broadcast, wait_receipt)

    def _token_contract(self, token: str):
        return self._client.web3.eth.contract(address=checksum(token), abi=DECIMAL_TOKEN_ABI)

    def _token_center_contract(self):
        return self._client.web3.eth.contract(
            address=checksum(self._client.config.contracts.token_center),
            abi=TOKEN_CENTER_ABI,
        )

    async def token_address_by_symbol(self, symbol: str) -> str | None:
        """Resolve a token contract by symbol through TokenCenter, if the chain exposes it."""
        normalized = str(symbol).strip()
        if not normalized:
            raise ValueError("Token symbol is required")
        contract = self._token_center_contract()
        for candidate in (normalized, normalized.lower(), normalized.upper()):
            try:
                address = await self._client.rpc.call(lambda _w3, item=candidate: contract.functions.tokens(item).call())
            except Exception:
                continue
            if address and int(str(address), 16) != 0:
                return checksum(address)
        return None

    async def _with_created_token_metadata(self, result: TransactionResult, symbol: str) -> TransactionResult:
        token_address = self._extract_token_address(result)
        if token_address is None and result.status in {"success", "pending"}:
            token_address = await self.token_address_by_symbol(symbol)
        if token_address is None:
            return result
        events = dict(result.events or {})
        events.setdefault("token_created", {"tokenAddress": token_address, "symbol": symbol})
        return _replace_transaction_result(result, token_address=token_address, events=events)

    def _extract_token_address(self, result: TransactionResult) -> str | None:
        if not result.receipt:
            return None
        contract = self._token_center_contract()
        for event_name in ("TokenDeployed", "TokenReservelessDeployed"):
            try:
                event = getattr(contract.events, event_name)()
                logs = event.process_receipt(result.receipt, errors=DISCARD)
            except Exception:
                continue
            for log in logs:
                address = log.get("args", {}).get("tokenAddress")
                if address:
                    return checksum(address)
        return None


def _del_to_wei(value: Decimal | str | int) -> int:
    return parse_units(value, 18)


def _parse_units(value: Decimal | str | int, decimals: int) -> int:
    return parse_units(value, decimals)


def token_creation_commission_del(symbol: str) -> Decimal:
    """Return Decimal token creation symbol commission in DEL."""
    normalized = str(symbol).strip()
    if not normalized:
        raise ValueError("Token symbol is required")
    return TOKEN_CREATION_COMMISSION_BY_SYMBOL_LENGTH.get(
        len(normalized),
        TOKEN_CREATION_DEFAULT_COMMISSION_DEL,
    )


def token_creation_commission_wei(symbol: str) -> int:
    return _del_to_wei(token_creation_commission_del(symbol))


def token_creation_required_reserve_del(symbol: str, extra_reserve_del: Decimal | str | int = 0) -> Decimal:
    return TOKEN_CREATION_MIN_RESERVE_DEL + token_creation_commission_del(symbol) + Decimal(str(extra_reserve_del))


def token_creation_required_reserve_wei(symbol: str, extra_reserve_wei: int = 0) -> int:
    return _del_to_wei(TOKEN_CREATION_MIN_RESERVE_DEL + token_creation_commission_del(symbol)) + int(extra_reserve_wei)


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


def _replace_transaction_result(result: TransactionResult, **updates: Any) -> TransactionResult:
    data = {
        "success": result.success,
        "tx_hash": result.tx_hash,
        "status": result.status,
        "block_number": result.block_number,
        "transaction_index": result.transaction_index,
        "gas_used": result.gas_used,
        "effective_gas_price_wei": result.effective_gas_price_wei,
        "oracle_gas_price_wei": result.oracle_gas_price_wei,
        "effective_fee_wei": result.effective_fee_wei,
        "effective_fee_del": result.effective_fee_del,
        "fee_wei": result.fee_wei,
        "fee_del": result.fee_del,
        "gas": result.gas,
        "raw_tx_hex": result.raw_tx_hex,
        "receipt": result.receipt,
        "events": result.events,
        "token_address": result.token_address,
        "hold_timestamp": result.hold_timestamp,
        "hold_time": result.hold_time,
        "error": result.error,
        "user_message": result.user_message,
        "native_balance_wei": result.native_balance_wei,
        "required_wei": result.required_wei,
        "missing_wei": result.missing_wei,
        "token_balance_raw": result.token_balance_raw,
        "token_required_raw": result.token_required_raw,
        "token_missing_raw": result.token_missing_raw,
        "token_allowance_raw": result.token_allowance_raw,
        "token_allowance_required_raw": result.token_allowance_required_raw,
        "token_allowance_missing_raw": result.token_allowance_missing_raw,
    }
    data.update(updates)
    return TransactionResult(**data)
