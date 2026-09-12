from __future__ import annotations

import asyncio
from dataclasses import dataclass
from datetime import datetime, timezone
from decimal import Decimal, InvalidOperation
import time
from typing import Any

from .erc20 import format_units


@dataclass(frozen=True)
class Page:
    limit: int = 50
    offset: int = 0
    order: str = "desc"

    def params(self, max_limit: int = 100) -> dict[str, Any]:
        limit = min(max(1, int(self.limit)), max_limit)
        offset = max(0, int(self.offset))
        order = "asc" if self.order == "asc" else "desc"
        return {"limit": limit, "offset": offset, "order": order}


@dataclass(frozen=True)
class WalletStakeHold:
    amount: Decimal
    amount_raw: str
    hold_start_time: int | None = None
    hold_end_time: int | None = None
    is_active: bool = False
    is_expired: bool = False
    raw: dict[str, Any] | None = None

    @property
    def contract_hold_timestamp(self) -> int | None:
        return self.hold_end_time or self.hold_start_time


@dataclass(frozen=True)
class WalletStakePosition:
    validator: str
    validator_name: str
    symbol: str
    amount: Decimal
    amount_raw: str
    base_amount_del: Decimal
    base_amount_raw: str
    is_hold: bool = False
    is_native: bool = False
    stake_type: str | None = None
    token_address: str | None = None
    token: dict[str, Any] | None = None
    hold_amount: Decimal = Decimal(0)
    unlocked_amount: Decimal = Decimal(0)
    holds: tuple[WalletStakeHold, ...] = ()
    raw: dict[str, Any] | None = None

    @property
    def held_amount(self) -> Decimal:
        return self.hold_amount if self.hold_amount > 0 else Decimal(0)

    @property
    def matured_hold_amount(self) -> Decimal:
        return sum((hold.amount for hold in self.holds if hold.is_expired), Decimal(0))

    @property
    def available_to_unbond(self) -> Decimal:
        if self.held_amount > 0 or self.is_hold:
            return self.unlocked_amount
        return self.amount

    @property
    def api_unlocked_delta(self) -> Decimal:
        return self.unlocked_amount

    @property
    def held_base_amount_del(self) -> Decimal:
        return self._base_share(self.held_amount)

    @property
    def available_base_amount_del(self) -> Decimal:
        return self._base_share(self.available_to_unbond)

    @property
    def can_unbond(self) -> bool:
        return self.available_to_unbond > 0

    @property
    def can_withdraw_hold(self) -> bool:
        return self.matured_hold_amount > 0

    def _base_share(self, amount: Decimal) -> Decimal:
        if amount <= 0 or self.amount <= 0 or self.base_amount_del <= 0:
            return Decimal(0)
        return self.base_amount_del * amount / self.amount


@dataclass(frozen=True)
class WalletUnstakePosition:
    validator: str
    validator_name: str
    symbol: str
    amount: Decimal
    amount_raw: str
    completion_time: str | None = None
    unfreeze_timestamp: int | None = None
    raw: dict[str, Any] | None = None


@dataclass(frozen=True)
class WalletStakeWithdrawal:
    validator: str
    validator_name: str
    symbol: str
    amount: Decimal
    amount_raw: str
    available_timestamp: int | None = None
    available_time: str | None = None
    tx_hash: str | None = None
    block: int | None = None
    created_timestamp: int | None = None
    source: str = "api"
    is_completed: bool = False
    raw: dict[str, Any] | None = None


@dataclass(frozen=True)
class WalletStakingSummary:
    address: str
    total_del: Decimal
    coin_total_del: Decimal
    nft_hold_total_del: Decimal
    positions: tuple[WalletStakePosition, ...]
    unstakes: tuple[WalletUnstakePosition, ...] = ()
    raw_stakes: dict[str, Any] | None = None
    raw_unstakes: dict[str, Any] | None = None

    @property
    def held_positions(self) -> tuple[WalletStakePosition, ...]:
        return tuple(position for position in self.positions if position.held_amount > 0)

    @property
    def available_positions(self) -> tuple[WalletStakePosition, ...]:
        return tuple(position for position in self.positions if position.can_unbond)

    @property
    def delegated_by_symbol(self) -> dict[str, Decimal]:
        return _sum_positions_by_symbol(self.positions, "amount")

    @property
    def held_by_symbol(self) -> dict[str, Decimal]:
        return _sum_positions_by_symbol(self.positions, "held_amount")

    @property
    def available_to_unbond_by_symbol(self) -> dict[str, Decimal]:
        return _sum_positions_by_symbol(self.available_positions, "available_to_unbond")


def _sum_positions_by_symbol(positions: tuple[WalletStakePosition, ...], attr: str) -> dict[str, Decimal]:
    totals: dict[str, Decimal] = {}
    for position in positions:
        amount = getattr(position, attr)
        if amount <= 0:
            continue
        symbol = position.symbol.upper()
        totals[symbol] = totals.get(symbol, Decimal(0)) + amount
    return totals


def _unwrap_result(payload: dict[str, Any]) -> dict[str, Any]:
    result = payload.get("Result") if isinstance(payload.get("Result"), dict) else payload.get("result")
    return result if isinstance(result, dict) else payload


def _decimal_18(value: Any) -> Decimal:
    if value in (None, ""):
        return Decimal(0)
    try:
        raw = Decimal(str(value))
        numerator, denominator = raw.as_integer_ratio()
        if denominator != 1:
            raise ValueError("Base-unit amount must be an integer")
        return format_units(numerator, 18)
    except (InvalidOperation, ValueError, TypeError) as exc:
        raise ValueError(f"Invalid 18-decimal base-unit amount: {value!r}") from exc


def _int_or_none(value: Any) -> int | None:
    try:
        if value in (None, ""):
            return None
        return int(value)
    except (ValueError, TypeError):
        return None


def _timestamp_or_none(value: Any) -> int | None:
    if value in (None, "", "0", 0):
        return None
    if isinstance(value, (int, float)):
        stamp = int(value)
        return stamp // 1000 if stamp > 10_000_000_000 else stamp
    raw = str(value).strip()
    if raw.isdigit():
        stamp = int(raw)
        return stamp // 1000 if stamp > 10_000_000_000 else stamp
    try:
        parsed = datetime.fromisoformat(raw.replace("Z", "+00:00"))
        if parsed.tzinfo is None:
            parsed = parsed.replace(tzinfo=timezone.utc)
        return int(parsed.timestamp())
    except ValueError:
        return None


def _iso_from_timestamp(value: int | None) -> str | None:
    if value is None:
        return None
    return datetime.fromtimestamp(value, tz=timezone.utc).isoformat().replace("+00:00", "Z")


def _display_symbol(symbol: Any) -> str:
    value = str(symbol or "DEL").strip() or "DEL"
    return "DEL" if value.upper() == "WDEL" else value


def _tx_items(payload: dict[str, Any] | None) -> list[dict[str, Any]]:
    if not isinstance(payload, dict):
        return []
    root = _unwrap_result(payload)
    for key in ("data", "items", "txs"):
        value = root.get(key)
        if isinstance(value, list):
            return [item for item in value if isinstance(item, dict)]
    data = root.get("data")
    if isinstance(data, dict):
        for key in ("items", "txs"):
            value = data.get(key)
            if isinstance(value, list):
                return [item for item in value if isinstance(item, dict)]
    return []


def _stake_holds(item: dict[str, Any]) -> tuple[WalletStakeHold, ...]:
    nested = item.get("stake") if isinstance(item.get("stake"), dict) else {}
    raw_holds = item.get("holds") or nested.get("holds") or []
    holds: list[WalletStakeHold] = []
    for hold in raw_holds:
        if not isinstance(hold, dict):
            continue
        raw_amount = str(hold.get("amount") or "0")
        holds.append(
            WalletStakeHold(
                amount=_decimal_18(raw_amount),
                amount_raw=raw_amount,
                hold_start_time=_int_or_none(hold.get("hold_start_time")),
                hold_end_time=_int_or_none(hold.get("hold_end_time")),
                is_active=bool(hold.get("is_active")),
                is_expired=bool(hold.get("is_expired")),
                raw=hold,
            )
        )
    if not holds and bool(item.get("is_hold")):
        hold_timestamp = _timestamp_or_none(
            item.get("hold_timestamp")
            or item.get("hold_end_time")
            or item.get("hold_end_at")
            or item.get("unlock_date")
        )
        if hold_timestamp is not None:
            raw_amount = str(
                item.get("hold_amount")
                or item.get("delegatedCoins")
                or item.get("amount")
                or "0"
            )
            now_timestamp = int(datetime.now(tz=timezone.utc).timestamp())
            holds.append(
                WalletStakeHold(
                    amount=_decimal_18(raw_amount),
                    amount_raw=raw_amount,
                    hold_end_time=hold_timestamp,
                    is_active=hold_timestamp > now_timestamp,
                    is_expired=hold_timestamp <= now_timestamp,
                    raw=item,
                )
            )
    return tuple(holds)


def _validator_identity(item: dict[str, Any]) -> tuple[str, str]:
    validator = item.get("validator") if isinstance(item.get("validator"), dict) else {}
    address = str(
        validator.get("evmAddress")
        or validator.get("address")
        or validator.get("operator_address")
        or item.get("validator")
        or ""
    )
    name = str(
        validator.get("name")
        or validator.get("moniker")
        or validator.get("title")
        or address
        or ""
    )
    return address, name


def _coin_symbol(item: dict[str, Any]) -> str:
    coin = item.get("coin") if isinstance(item.get("coin"), dict) else {}
    return str(
        item.get("symbol")
        or item.get("coin_symbol")
        or coin.get("symbol")
        or coin.get("coin_symbol")
        or "DEL"
    )


def _coins_items(payload: dict[str, Any] | None) -> list[dict[str, Any]]:
    if not isinstance(payload, dict):
        return []
    result = _unwrap_result(payload)
    if isinstance(result.get("coin"), dict):
        return [result["coin"]]
    for key in ("coins", "items", "tokens"):
        value = result.get(key)
        if isinstance(value, list):
            return [item for item in value if isinstance(item, dict)]
    return []


def _coin_registry(payload: dict[str, Any] | None) -> dict[str, dict[str, Any]]:
    registry: dict[str, dict[str, Any]] = {}
    for coin in _coins_items(payload):
        symbol = str(coin.get("denom") or coin.get("symbol") or coin.get("coin_symbol") or "").strip()
        if not symbol:
            continue
        registry.setdefault(symbol, coin)
        registry.setdefault(symbol.lower(), coin)
        registry.setdefault(symbol.upper(), coin)
    return registry


def _token_address_from_coin(coin: dict[str, Any] | None) -> str | None:
    if not isinstance(coin, dict):
        return None
    value = (
        coin.get("drc20_address")
        or coin.get("contract_address")
        or coin.get("token_address")
        or coin.get("address")
    )
    return str(value) if value else None


def _staking_symbols(stakes_payload: dict[str, Any]) -> list[str]:
    stakes = _unwrap_result(stakes_payload)
    symbols: list[str] = []
    seen: set[str] = set()
    for group in stakes.get("items") or []:
        if not isinstance(group, dict):
            continue
        for coin in group.get("items") or []:
            if not isinstance(coin, dict):
                continue
            symbol = _coin_symbol(coin).strip()
            key = symbol.lower()
            if not symbol or key == "del" or key in seen:
                continue
            seen.add(key)
            symbols.append(symbol)
    return symbols


def _merge_coin_payloads(payloads: list[dict[str, Any] | None]) -> dict[str, Any]:
    coins: list[dict[str, Any]] = []
    for payload in payloads:
        coins.extend(_coins_items(payload))
    return {"coins": coins}


def normalize_wallet_staking_summary(
    address: str,
    stakes_payload: dict[str, Any],
    unstakes_payload: dict[str, Any] | None = None,
    coins_payload: dict[str, Any] | None = None,
) -> WalletStakingSummary:
    stakes = _unwrap_result(stakes_payload)
    unstakes_result = _unwrap_result(unstakes_payload or {})
    registry = _coin_registry(coins_payload)
    positions: list[WalletStakePosition] = []
    for group in stakes.get("items") or []:
        if not isinstance(group, dict):
            continue
        validator_address, validator_name = _validator_identity(group)
        for coin in group.get("items") or []:
            if not isinstance(coin, dict):
                continue
            raw_amount = str(coin.get("delegatedCoins") or coin.get("amount") or "0")
            raw_base = str(coin.get("delegatedBaseCoins") or "0")
            symbol = _coin_symbol(coin)
            is_native = symbol.lower() == "del"
            token = registry.get(symbol) or registry.get(symbol.lower()) or registry.get(symbol.upper())
            holds = _stake_holds(coin)
            positions.append(
                WalletStakePosition(
                    validator=validator_address,
                    validator_name=validator_name,
                    symbol=symbol,
                    amount=_decimal_18(raw_amount),
                    amount_raw=raw_amount,
                    base_amount_del=_decimal_18(raw_base),
                    base_amount_raw=raw_base,
                    is_hold=bool(coin.get("is_hold")),
                    is_native=is_native,
                    stake_type=coin.get("stake_type"),
                    token_address=None
                    if is_native
                    else coin.get("token_address") or coin.get("contract_address") or _token_address_from_coin(token),
                    token=token,
                    hold_amount=_decimal_18(coin.get("hold_amount")),
                    unlocked_amount=_decimal_18(coin.get("unlocked_amount")),
                    holds=holds,
                    raw=coin,
                )
            )

    unstaked: list[WalletUnstakePosition] = []
    for item in unstakes_result.get("unstakes") or []:
        if not isinstance(item, dict):
            continue
        validator_address, validator_name = _validator_identity(item)
        raw_amount = str(item.get("amount") or item.get("delegatedCoins") or "0")
        unstaked.append(
            WalletUnstakePosition(
                validator=validator_address,
                validator_name=validator_name,
                symbol=_coin_symbol(item),
                amount=_decimal_18(raw_amount),
                amount_raw=raw_amount,
                completion_time=item.get("completion_time"),
                unfreeze_timestamp=item.get("unfreeze_timestamp"),
                raw=item,
            )
        )

    total = _decimal_18(stakes.get("base_steaks") or stakes.get("total_steaks"))
    if total == 0:
        total = sum((position.base_amount_del for position in positions), Decimal(0))
    return WalletStakingSummary(
        address=address,
        total_del=total,
        coin_total_del=_decimal_18(stakes.get("coin_steaks")) or total,
        nft_hold_total_del=_decimal_18(stakes.get("nft_hold_steaks")),
        positions=tuple(positions),
        unstakes=tuple(unstaked),
        raw_stakes=stakes_payload,
        raw_unstakes=unstakes_payload,
    )


def normalize_wallet_stake_withdrawals(
    address: str,
    *,
    unstakes_payload: dict[str, Any] | None = None,
    txs_payload: dict[str, Any] | None = None,
    tx_payloads: list[dict[str, Any] | None] | None = None,
    include_completed: bool = False,
    recent_days: int | None = None,
    unbonding_days: int = 15,
    now_timestamp: int | None = None,
) -> tuple[WalletStakeWithdrawal, ...]:
    now = int(time.time()) if now_timestamp is None else int(now_timestamp)
    cutoff = None if recent_days is None else now - max(0, int(recent_days)) * 24 * 60 * 60
    rows: list[WalletStakeWithdrawal] = []
    seen: set[tuple[Any, ...]] = set()

    def add(row: WalletStakeWithdrawal) -> None:
        if not include_completed:
            if row.available_timestamp is not None and row.available_timestamp <= now:
                return
            if row.available_timestamp is None and row.is_completed:
                return
        if cutoff is not None and row.available_timestamp is not None and row.available_timestamp < cutoff:
            return
        key = (
            (row.tx_hash or "").lower(),
            row.validator.lower(),
            row.symbol.upper(),
            row.amount_raw,
            row.available_timestamp,
        )
        if key in seen:
            return
        seen.add(key)
        rows.append(row)

    unstakes_result = _unwrap_result(unstakes_payload or {})
    for item in unstakes_result.get("unstakes") or []:
        if not isinstance(item, dict):
            continue
        validator_address, validator_name = _validator_identity(item)
        raw_amount = str(item.get("amount") or item.get("delegatedCoins") or "0")
        available_at = _timestamp_or_none(item.get("unfreeze_timestamp") or item.get("completion_time"))
        symbol = _display_symbol(_coin_symbol(item))
        add(
            WalletStakeWithdrawal(
                validator=validator_address,
                validator_name=validator_name,
                symbol=symbol,
                amount=_decimal_18(raw_amount),
                amount_raw=raw_amount,
                available_timestamp=available_at,
                available_time=_iso_from_timestamp(available_at) or item.get("completion_time"),
                source="unstakes",
                is_completed=bool(available_at is not None and available_at <= now),
                raw=item,
            )
        )

    tx_sources = _tx_items(txs_payload)
    for payload in tx_payloads or []:
        if not isinstance(payload, dict):
            continue
        tx_sources.append(_unwrap_result(payload))

    wanted_types = {"withdraw_with_reset", "withdraw_hold", "delegation_withdraw", "withdraw", "unbond_del"}
    address_key = address.lower()
    for tx in tx_sources:
        tx_type = str(tx.get("transaction_type") or tx.get("type") or "").strip().lower().replace("-", "_")
        if tx_type not in wanted_types:
            continue
        from_address = str(tx.get("from_address") or "").lower()
        if from_address and from_address != address_key:
            continue
        raw = tx.get("raw_data") if isinstance(tx.get("raw_data"), dict) else {}
        meta = {**raw, **tx}
        validator = str(raw.get("validator") or tx.get("validator") or "")
        validator_name = str(raw.get("validator_name") or tx.get("validator_name") or validator)
        symbol = _display_symbol(meta.get("token_symbol") or meta.get("denom") or meta.get("symbol") or "DEL")
        amount = meta.get("amount") if meta.get("amount") not in (None, "") else meta.get("value_dct")
        if amount in (None, ""):
            continue
        created_at = _timestamp_or_none(tx.get("timestamp") or raw.get("timestamp"))
        available_at = _timestamp_or_none(meta.get("unbonding_time") or meta.get("unlock_date") or meta.get("completion_time"))
        if available_at is None and created_at is not None and tx_type in {"withdraw_with_reset", "delegation_withdraw", "withdraw", "unbond_del"}:
            available_at = created_at + max(0, int(unbonding_days)) * 24 * 60 * 60
        add(
            WalletStakeWithdrawal(
                validator=validator,
                validator_name=validator_name,
                symbol=symbol,
                amount=_decimal_plain(amount),
                amount_raw=str(amount),
                available_timestamp=available_at,
                available_time=_iso_from_timestamp(available_at),
                tx_hash=tx.get("tx_hash"),
                block=_int_or_none(tx.get("block")),
                created_timestamp=created_at,
                source="txs",
                is_completed=bool(available_at is not None and available_at <= now),
                raw=tx,
            )
        )

    return tuple(sorted(rows, key=lambda item: (item.available_timestamp or 2**63 - 1, item.validator_name, item.symbol)))


def _decimal_plain(value: Any) -> Decimal:
    if value in (None, ""):
        return Decimal(0)
    try:
        return Decimal(str(value))
    except (InvalidOperation, ValueError, TypeError):
        return Decimal(0)


class RestClient:
    def __init__(self, client) -> None:
        self._client = client

    @property
    def _max_limit(self) -> int:
        return int(self._client.config.safety.rest_max_limit)

    async def health(self) -> dict[str, Any]:
        return await self._client.rest_root_get("/health")

    async def latest_block(self) -> dict[str, Any]:
        return await self._client.rest_get("/blocks/latest")

    async def block(self, height: int) -> dict[str, Any]:
        return await self._client.rest_get(f"/blocks/{height}")

    async def block_txs(self, height: int, page: Page | None = None) -> dict[str, Any]:
        return await self._client.rest_get(
            f"/blocks/{height}/txs", **(page or Page()).params(self._max_limit)
        )

    async def tx(self, tx_hash: str) -> dict[str, Any]:
        return await self._client.rest_get(f"/txs/{tx_hash}")

    async def txs(self, page: Page | None = None, **filters: Any) -> dict[str, Any]:
        params = (page or Page()).params(self._max_limit)
        params.update({key: value for key, value in filters.items() if value is not None})
        return await self._client.rest_get("/txs", **params)

    async def address(self, address: str) -> dict[str, Any]:
        return await self._client.rest_get(f"/addresses/{address}")

    async def address_full(
        self,
        address: str,
        with_erc20: bool = True,
        symbols: str | None = None,
    ) -> dict[str, Any]:
        params: dict[str, Any] = {"with_erc20": int(with_erc20)}
        if symbols:
            params["symbols"] = symbols
        return await self._client.rest_get(f"/addresses/{address}/full", **params)

    async def wallet_balances(
        self,
        address: str,
        limit: int = 300,
        offset: int = 0,
        include_bank: bool = True,
        prefer_bank: bool = True,
    ) -> dict[str, Any]:
        """Fast full wallet balance: DEL + bank-module balances + indexed DRC20/ERC20 balances."""
        safe_limit = min(max(1, int(limit)), max(self._max_limit, 300))
        return await self._client.rest_get(
            f"/erc20/balances/{address}",
            limit=safe_limit,
            offset=max(0, int(offset)),
            include_bank=int(include_bank),
            prefer_bank=int(prefer_bank),
        )

    async def address_txs(self, address: str, page: Page | None = None) -> dict[str, Any]:
        return await self._client.rest_get(
            f"/addresses/{address}/txs", **(page or Page()).params(self._max_limit)
        )

    async def coins(self, with_price: bool = False, limit: int = 100) -> dict[str, Any]:
        safe_limit = min(max(1, int(limit)), self._max_limit)
        return await self._client.rest_get(
            "/coins", with_price=int(with_price), **{"pagination.limit": safe_limit}
        )

    async def coin_registry(self, with_price: bool = False, limit: int = 500) -> dict[str, Any]:
        """Fetch a larger coin registry page for symbol-to-DRC20 address enrichment."""
        safe_limit = min(max(1, int(limit)), max(self._max_limit, 500))
        return await self._client.rest_get(
            "/coins", with_price=int(with_price), **{"pagination.limit": safe_limit}
        )

    async def coin(self, denom: str) -> dict[str, Any]:
        return await self._client.rest_get(f"/coins/{denom}")

    async def coin_registry_for_symbols(self, symbols: list[str], with_price: bool = False) -> dict[str, Any]:
        """Resolve selected symbols through `/coins/{denom}` and return a registry-like payload."""
        unique: list[str] = []
        seen: set[str] = set()
        for symbol in symbols:
            normalized = str(symbol or "").strip()
            key = normalized.lower()
            if not normalized or key == "del" or key in seen:
                continue
            seen.add(key)
            unique.append(normalized)
        if not unique:
            return {"coins": []}

        async def one(symbol: str) -> dict[str, Any] | None:
            try:
                return await self._client.rest_get(f"/coins/{symbol}", with_price=int(with_price))
            except Exception:
                return None

        payloads = await asyncio.gather(*(one(symbol) for symbol in unique))
        return _merge_coin_payloads(list(payloads))

    async def coin_prices(self) -> dict[str, Any]:
        return await self._client.rest_get("/coins/prices")

    async def validators(self) -> dict[str, Any]:
        return await self._client.rest_get("/validators")

    async def validator(self, validator: str) -> dict[str, Any]:
        return await self._client.rest_get(f"/validators/{validator}")

    async def validator_delegations(self, validator: str) -> dict[str, Any]:
        return await self._client.rest_get(f"/validators/{validator}/delegations")

    async def wallet_stakes(self, address: str) -> dict[str, Any]:
        """Active coin delegations grouped by validator for an EVM wallet."""
        return await self._client.rest_get(f"/validators/wallet/{address}/stakes/coins")

    async def wallet_unstakes(self, address: str) -> dict[str, Any]:
        """Pending coin undelegations/unbond entries for an EVM wallet."""
        return await self._client.rest_get(f"/validators/{address}/unstakes/coins")

    async def wallet_stake_withdrawals(
        self,
        address: str,
        *,
        page: Page | None = None,
        include_completed: bool = False,
        recent_days: int | None = None,
        tx_hashes: list[str] | None = None,
        unbonding_days: int = 15,
    ) -> tuple[WalletStakeWithdrawal, ...]:
        """Stake withdrawal history for an EVM wallet, normalized for wallet UIs."""
        known_hashes = tuple(dict.fromkeys(tx_hashes or []))
        if len(known_hashes) > self._max_limit:
            raise ValueError(
                f"At most {self._max_limit} transaction hashes can be read in one request"
            )
        tasks: list[Any] = [
            self.wallet_unstakes(address),
            self.txs(page or Page(limit=100), address=address),
        ]
        for tx_hash in known_hashes:
            tasks.append(self.tx(tx_hash))
        results = await asyncio.gather(*tasks, return_exceptions=True)
        if all(isinstance(item, Exception) for item in results):
            raise results[0]
        unstakes_payload = None if isinstance(results[0], Exception) else results[0]
        txs_payload = None if isinstance(results[1], Exception) else results[1]
        tx_payloads = [item for item in results[2:] if not isinstance(item, Exception)]
        return normalize_wallet_stake_withdrawals(
            address,
            unstakes_payload=unstakes_payload,
            txs_payload=txs_payload,
            tx_payloads=tx_payloads,
            include_completed=include_completed,
            recent_days=recent_days,
            unbonding_days=unbonding_days,
        )

    async def wallet_stake_transfers(self, address: str) -> dict[str, Any]:
        """Pending stake transfer/redelegation entries for an EVM wallet, when the API exposes them."""
        return await self._client.rest_get(f"/validators/wallet/{address}/transfer/coins")

    async def wallet_staking_summary(
        self,
        address: str,
        *,
        include_unstakes: bool = True,
        enrich_tokens: bool = True,
        coin_lookup_limit: int = 500,
    ) -> WalletStakingSummary:
        tasks = [self.wallet_stakes(address)]
        if include_unstakes:
            tasks.append(self.wallet_unstakes(address))
        results = await asyncio.gather(*tasks, return_exceptions=True)

        stakes_result = results[0]
        if isinstance(stakes_result, Exception):
            raise stakes_result
        unstakes_payload: dict[str, Any] | None = None
        coins_payload: dict[str, Any] | None = None
        if include_unstakes:
            value = results[1]
            if not isinstance(value, Exception):
                unstakes_payload = value
        if enrich_tokens:
            bulk_task = self.coin_registry(with_price=True, limit=coin_lookup_limit)
            targeted_task = self.coin_registry_for_symbols(_staking_symbols(stakes_result), with_price=True)
            bulk_value, targeted_value = await asyncio.gather(bulk_task, targeted_task, return_exceptions=True)
            payloads: list[dict[str, Any] | None] = []
            if not isinstance(bulk_value, Exception):
                payloads.append(bulk_value)
            if not isinstance(targeted_value, Exception):
                payloads.append(targeted_value)
            coins_payload = _merge_coin_payloads(payloads)
        return normalize_wallet_staking_summary(address, stakes_result, unstakes_payload, coins_payload)

    async def rewards_delegator(self, delegator: str) -> dict[str, Any]:
        return await self._client.rest_get(f"/rewards/delegators/{delegator}")
