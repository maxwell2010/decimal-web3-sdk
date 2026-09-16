import json
from unittest.mock import Mock

import pytest
from requests.exceptions import ReadTimeout
from eth_abi import encode
from web3 import Web3

from decimal_web3_sdk import DecimalClient, NetworkConfig
from decimal_web3_sdk.decimal import DelegationTokenType
from decimal_web3_sdk.rpc import RpcPool


def stub_http(provider, name, calls, *, broken=False):
    def post(url, payload, **kwargs):
        request = json.loads(payload)
        method = request["method"]
        calls.append((name, method))
        if broken and method == "eth_blockNumber":
            raise ReadTimeout("test timeout")
        result = "0x4b" if method == "eth_chainId" else "0x64"
        return json.dumps({"jsonrpc": "2.0", "id": request["id"], "result": result}).encode()
    provider._request_session_manager.make_post_request = Mock(side_effect=post)
    retry = provider.exception_retry_configuration
    if retry is not None:
        retry.backoff_factor = 0


async def test_timeout_attempts_each_endpoint_once_then_returns_fallback(monkeypatch):
    pool = RpcPool(["https://primary.example.invalid", "https://backup.example.invalid"], chain_id=75)
    primary = pool._create_web3(pool._urls[0])
    backup = pool._create_web3(pool._urls[1])
    calls = []
    stub_http(primary.provider, "primary", calls, broken=True)
    stub_http(backup.provider, "backup", calls)
    clients = dict(zip(pool._urls, (primary, backup)))
    monkeypatch.setattr(pool, "_create_web3", clients.__getitem__)
    assert await pool.call(lambda w3: w3.eth.block_number) == 100
    assert calls == [
        ("primary", "eth_chainId"), ("primary", "eth_blockNumber"),
        ("backup", "eth_chainId"), ("backup", "eth_blockNumber"),
    ]


async def test_single_endpoint_does_not_multiply_timeout(monkeypatch):
    pool = RpcPool(["https://primary.example.invalid"])
    client = pool.web3
    calls = []
    stub_http(client.provider, "primary", calls, broken=True)
    with pytest.raises(RuntimeError, match="All Decimal") as caught:
        await pool.call(lambda w3: w3.eth.block_number)
    assert isinstance(caught.value.__cause__, ReadTimeout)
    assert calls == [("primary", "eth_blockNumber")]


@pytest.mark.parametrize("operation", [
    "allowance", "stake", "hold", "validator", "validator_active", "validator_member",
    "nft_owner", "nft_balance", "nft_approval", "nft1155_balance", "nft1155_approval", "token_lookup", "checks_nonce",
])
async def test_contract_reads_rebind_to_fallback(operation, monkeypatch):
    urls = ["https://primary.example.invalid", "https://backup.example.invalid"]
    client = DecimalClient(NetworkConfig.custom(web3_urls=urls, chain_id=75))
    clients = {url: client.rpc._create_web3(url) for url in urls}
    account = Web3.to_checksum_address("0x" + "11" * 20)
    outputs = {
        "allowance": (["uint256"], [7]),
        "stake": (["(address,address,address,uint256,uint256,uint8,uint256)"], [(account, account, account, 7, 0, int(DelegationTokenType.DRC20), 0)]),
        "hold": (["(address,address,address,uint256,uint256,uint8,uint256)"], [(account, account, account, 7, 0, int(DelegationTokenType.DRC20), 1000)]),
        "validator": (["uint8"], [1]),
        "validator_active": (["bool"], [True]),
        "validator_member": (["bool"], [True]),
        "nft_owner": (["address"], [account]),
        "nft_balance": (["uint256"], [7]),
        "nft_approval": (["bool"], [True]),
        "nft1155_balance": (["uint256"], [7]),
        "nft1155_approval": (["bool"], [True]),
        "token_lookup": (["address"], [account]),
        "checks_nonce": (["uint256"], [7]),
    }
    contract_calls = []

    def post(url, payload, **kwargs):
        request = json.loads(payload)
        if request["method"] == "eth_call":
            contract_calls.append((url, request["params"]))
            if url == urls[0]:
                raise ReadTimeout("primary unavailable")
            result = "0x" + encode(*outputs[operation]).hex()
        else:
            result = "0x4b"
        return json.dumps({"jsonrpc": "2.0", "id": request["id"], "result": result}).encode()

    for w3 in clients.values():
        w3.provider._request_session_manager.make_post_request = Mock(side_effect=post)
    monkeypatch.setattr(client.rpc, "_create_web3", clients.__getitem__)
    calls = {
        "allowance": lambda: client.erc20.allowance(account, account, account),
        "stake": lambda: client.decimal.get_stake(account, account, account, block_identifier=100),
        "hold": lambda: client.decimal.get_hold_stake(account, account, account, 1000, block_identifier=100),
        "validator": lambda: client.decimal.validator_status(account),
        "validator_active": lambda: client.decimal.validator_is_active(account),
        "validator_member": lambda: client.decimal.validator_is_member(account),
        "nft_owner": lambda: client.nft.owner_of(account, 1),
        "nft_balance": lambda: client.nft.balance_of(account, account),
        "nft_approval": lambda: client.nft.is_approved_for_all("erc721", account, account, account),
        "nft1155_balance": lambda: client.nft.balance_of(account, account, token_id=1, kind="erc1155"),
        "nft1155_approval": lambda: client.nft.is_approved_for_all("erc1155", account, account, account),
        "token_lookup": lambda: client.token.token_address_by_symbol("TEST"),
        "checks_nonce": lambda: client.checks._nonce(account),
    }
    try:
        result = await calls[operation]()
        assert result is not None
        assert [url for url, params in contract_calls] == urls
        if operation in ("stake", "hold"):
            assert result.amount_raw == 7
            assert all(params[1] == "0x64" for _, params in contract_calls)
    finally:
        await client.close()
