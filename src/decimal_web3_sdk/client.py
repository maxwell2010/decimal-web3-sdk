from __future__ import annotations

import aiohttp
from web3 import Web3

from .bridge import BridgeService
from .checks import ChecksService
from .config import NetworkConfig
from .contracts import AbiRegistry
from .decimal import DecimalService
from .erc20 import Erc20Service
from .limits import AsyncRateLimiter
from .monitoring import DecimalMonitor
from .nft import NftService
from .policy import TransactionPolicy
from .rest import RestClient
from .rpc import RpcPool
from .token import TokenService
from .transactions import TransactionService
from .wallet import checksum, mnemonic_to_account, mnemonic_to_private_key, private_key_to_address
from .ws import DecimalWsClient


class DecimalClient:
    def __init__(self, config: NetworkConfig | None = None) -> None:
        self.config = config or NetworkConfig.mainnet()
        self.rpc = RpcPool(
            self.config.web3_urls,
            min_interval_seconds=self.config.safety.rpc_min_interval_seconds,
        )
        self.abi = AbiRegistry()
        self.rest = RestClient(self)
        self.tx = TransactionService(self)
        self.decimal = DecimalService(self)
        self.erc20 = Erc20Service(self)
        self.token = TokenService(self)
        self.nft = NftService(self)
        self.checks = ChecksService(self)
        self.bridge = BridgeService(self)
        self.ws = DecimalWsClient(self.config)
        self._rest_limiter = AsyncRateLimiter(self.config.safety.rest_min_interval_seconds)
        self._session: aiohttp.ClientSession | None = None

    async def __aenter__(self) -> "DecimalClient":
        await self.connect()
        return self

    async def __aexit__(self, exc_type, exc, tb) -> None:
        await self.close()

    async def connect(self) -> bool:
        return await self.rpc.connect()

    async def close(self) -> None:
        if self._session is not None:
            await self._session.close()
            self._session = None
        await self.ws.close()

    @property
    def web3(self) -> Web3:
        return self.rpc.web3

    async def block_number(self) -> int:
        return await self.rpc.call(lambda w3: w3.eth.block_number)

    async def balance_wei(self, address: str) -> int:
        account = checksum(address)
        return await self.rpc.call(lambda w3: w3.eth.get_balance(account))

    async def balance_del(self, address: str) -> float:
        balance = await self.balance_wei(address)
        return float(Web3.from_wei(balance, "ether"))

    async def transaction_count(self, address: str) -> int:
        account = checksum(address)
        return await self.rpc.call(lambda w3: w3.eth.get_transaction_count(account))

    async def gas_price(self) -> int:
        return await self.rpc.call(lambda w3: int(w3.eth.gas_price))

    async def estimate_gas(self, tx: dict) -> int:
        return await self.rpc.call(lambda w3: int(w3.eth.estimate_gas(tx)))

    async def send_raw_transaction(self, raw_tx: bytes) -> str:
        tx_hash = await self.rpc.call(lambda w3: w3.eth.send_raw_transaction(raw_tx))
        return tx_hash.hex() if hasattr(tx_hash, "hex") else str(tx_hash)

    async def transaction_receipt(self, tx_hash: str) -> dict | None:
        try:
            receipt = await self.rpc.call(lambda w3: w3.eth.get_transaction_receipt(tx_hash))
        except Exception:
            return None
        if receipt is None:
            return None
        return dict(receipt)

    async def address_from_private_key(self, private_key: str) -> str:
        return private_key_to_address(private_key)

    async def private_key_from_mnemonic(
        self,
        mnemonic: str,
        *,
        passphrase: str = "",
        account_path: str = "m/44'/60'/0'/0/0",
    ) -> str:
        return mnemonic_to_private_key(
            mnemonic,
            passphrase=passphrase,
            account_path=account_path,
        )

    async def address_from_mnemonic(
        self,
        mnemonic: str,
        *,
        passphrase: str = "",
        account_path: str = "m/44'/60'/0'/0/0",
    ) -> str:
        return mnemonic_to_account(
            mnemonic,
            passphrase=passphrase,
            account_path=account_path,
        ).address

    async def rest_get(self, path: str, **params) -> dict:
        last_error: Exception | None = None
        seen: set[str] = set()
        for base_url in [self.config.api_base_url, *self.config.api_fallback_base_urls]:
            if not base_url or base_url in seen:
                continue
            seen.add(base_url)
            try:
                return await self._rest_get_from_base(base_url, path, **params)
            except Exception as exc:
                last_error = exc
        if last_error:
            raise last_error
        raise RuntimeError("No REST API base URLs configured")

    async def rest_root_get(self, path: str, **params) -> dict:
        if not self.config.api_root_url:
            raise RuntimeError("No REST API root URL configured")
        return await self._rest_get_from_base(self.config.api_root_url, path, **params)

    async def _rest_get_from_base(self, base_url: str, path: str, **params) -> dict:
        if not base_url:
            raise RuntimeError("No REST API base URL configured")
        await self._rest_limiter.wait()
        session = await self._get_session()
        base = base_url.rstrip("/")
        url = f"{base}/{path.lstrip('/')}"
        headers = {"X-API-Key": self.config.api_key} if self.config.api_key else None
        async with session.get(url, params=params, headers=headers, timeout=aiohttp.ClientTimeout(total=20)) as response:
            response.raise_for_status()
            return await response.json()

    async def latest_block_info(self) -> dict:
        return await self.rest_get("/blocks/latest")

    def monitor(self, policy: TransactionPolicy | None = None) -> DecimalMonitor:
        return DecimalMonitor(self, policy)

    async def _get_session(self) -> aiohttp.ClientSession:
        if self._session is None:
            self._session = aiohttp.ClientSession()
        return self._session
