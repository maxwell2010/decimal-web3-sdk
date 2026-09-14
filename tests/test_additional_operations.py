"""Independent calldata, precision and unsigned-fee regressions. No live accounts."""

from dataclasses import replace
from decimal import localcontext
from types import SimpleNamespace
from unittest.mock import AsyncMock, Mock

import pytest
from eth_abi import decode, encode
from eth_account import Account
from eth_account.messages import encode_defunct
from hexbytes import HexBytes
from web3 import Web3
from web3.providers.base import BaseProvider

import decimal_web3_sdk as sdk
from decimal_web3_sdk._contract_operations import ZERO_ADDRESS
from test_transaction_catalog import account, offline_client, make_request, reference


NEW_REQUESTS = {
    "BurnDelRequest",
    "BuyExactTokenRequest",
    "SellForExactDelRequest",
    "ConvertToDelRequest",
    "UpdateTokenMinSupplyRequest",
    "CompleteStakeRequest",
    "ApplyStakePenaltyRequest",
    "ApplyStakePenaltiesRequest",
    "AddValidatorTokenRequest",
    "AddValidatorDelRequest",
    "RemoveValidatorRequest",
    "UpdateValidatorMetadataRequest",
    "CreateReservelessNftCollectionRequest",
    "AddTokenReserveNftRequest",
    "StakeNftToHoldRequest",
    "ResetNftStakeHoldRequest",
    "ResetNftStakeHoldsRequest",
    "WithdrawNftWithResetRequest",
    "TransferNftWithResetRequest",
    "HoldNftWithResetRequest",
    "CompleteNftStakeRequest",
    "CreateMultisigRequest",
    "ApproveMultisigTransactionRequest",
    "ExecuteMultisigTransactionRequest",
}
NEW_CASES = [row for row in reference.transaction_catalog() if row["request"] in NEW_REQUESTS]
HUGE = 10**60 + 100000000000000001
ADDRESS = "0x" + "11" * 20
OTHER = "0x" + "22" * 20
SAFE = "0x" + "33" * 20


@pytest.mark.parametrize("row", NEW_CASES, ids=lambda row: row["method"])
async def test_all_new_operations_estimate_without_any_signature(
    row, offline_client, account, monkeypatch
):
    request = make_request(row, account, monkeypatch)
    signing = Mock(side_effect=AssertionError("Fee estimation must not sign"))
    monkeypatch.setattr(Account, "sign_transaction", signing)
    monkeypatch.setattr(Account, "sign_message", signing)
    service = getattr(offline_client, row["method"].split(".")[0])
    if isinstance(request, sdk.BurnDelRequest):
        draft = await service.build_burn_del(request)
        fee = await service.estimate_fee_for_burn_del(request, exact=True)
    else:
        draft = await service.build_operation(request)
        fee = await service.estimate_fee_for_operation(request, exact=True)
    assert fee.estimated_fee_wei == 120000 * 20 * 10**9
    assert draft.raw_tx is None and draft.tx_hash is None
    estimated_call = offline_client.estimate_gas.call_args.args[0]
    assert estimated_call["to"] == draft.tx["to"]
    assert estimated_call["data"] == draft.tx["data"]
    assert estimated_call["value"] == draft.tx["value"]
    signing.assert_not_called()
    offline_client.send_raw_transaction.assert_not_called()


def decode_call(call, signature, kinds):
    data = HexBytes(call.data)
    assert data[:4] == Web3.keccak(text=signature)[:4]
    return decode(kinds, data[4:])


def test_exact_output_buy_and_sell_preserve_units(offline_client, account):
    mnemonic = account[1]
    with localcontext() as context:
        context.prec = 3
        buy = sdk.BuyExactTokenRequest.from_mnemonic(
            mnemonic=mnemonic,
            token=ADDRESS,
            recipient=OTHER,
            amount_out_raw=HUGE,
            max_amount_del="0.100000000000000001",
        )
        call = buy.to_contract_call(offline_client)
        assert call.value_wei == 100000000000000001
        assert decode_call(
            call, "buyExactTokenForDEL(uint256,address)", ["uint256", "address"]
        ) == (HUGE, OTHER)
        sell = sdk.SellForExactDelRequest.from_mnemonic(
            mnemonic=mnemonic,
            token=ADDRESS,
            recipient=OTHER,
            max_amount_in_raw=HUGE,
            amount_out_del="0.100000000000000001",
        )
        call = sell.to_contract_call(offline_client)
        assert call.value_wei == 0
        assert decode_call(
            call,
            "sellTokensForExactDEL(uint256,uint256,address)",
            ["uint256", "uint256", "address"],
        ) == (100000000000000001, HUGE, OTHER)


@pytest.mark.parametrize("value", [True, 1.25, "1", -1, 2**256])
def test_raw_amounts_never_coerce_or_round(value, offline_client, account):
    request = sdk.BuyExactTokenRequest.from_mnemonic(
        mnemonic=account[1],
        token=ADDRESS,
        recipient=OTHER,
        amount_out_raw=value,
        max_amount_del="1",
    )
    with pytest.raises((TypeError, ValueError)):
        request.to_contract_call(offline_client)


async def test_native_burn_is_direct_zero_address_no_approve(offline_client, account):
    request = sdk.BurnDelRequest.from_mnemonic(
        mnemonic=account[1], amount_del="0.100000000000000001"
    )
    draft = await offline_client.tx.build_burn_del(request)
    assert draft.to_address == ZERO_ADDRESS
    assert draft.value_wei == 100000000000000001
    assert draft.tx["data"] == "0x"
    offline_client.erc20.allowance.assert_not_called()
    offline_client.erc20.permit_signature.assert_not_called()


@pytest.mark.parametrize(
    "cls,signature,kinds,tail",
    [
        (
            sdk.StakeNftToHoldRequest,
            "hold(address,address,uint256,uint256,uint256,uint256)",
            ["address", "address", "uint256", "uint256", "uint256", "uint256"],
            (HUGE, 1700000000, 1800000000),
        ),
        (
            sdk.WithdrawNftWithResetRequest,
            "withdrawWithReset(address,address,uint256,uint256,uint256[])",
            ["address", "address", "uint256", "uint256", "uint256[]"],
            (HUGE, (1700000000,)),
        ),
        (
            sdk.TransferNftWithResetRequest,
            "transferWithReset(address,address,uint256,uint256,address,uint256[])",
            ["address", "address", "uint256", "uint256", "address", "uint256[]"],
            (HUGE, OTHER, (1700000000,)),
        ),
        (
            sdk.HoldNftWithResetRequest,
            "holdWithReset(address,address,uint256,uint256,uint256,uint256[])",
            ["address", "address", "uint256", "uint256", "uint256", "uint256[]"],
            (HUGE, 1800000000, (1700000000,)),
        ),
    ],
)
def test_nft_calls_use_delegation_nft_and_exact_argument_order(
    cls, signature, kinds, tail, offline_client, account
):
    kwargs = dict(validator=ADDRESS, nft=OTHER, token_id=HUGE, amount=HUGE)
    if cls is sdk.StakeNftToHoldRequest:
        kwargs.update(old_hold_timestamp=1700000000, new_hold_timestamp=1800000000)
    else:
        kwargs["hold_timestamps_to_reset"] = (1700000000,)
    if cls is sdk.TransferNftWithResetRequest:
        kwargs["new_validator"] = OTHER
    if cls is sdk.HoldNftWithResetRequest:
        kwargs["new_hold_timestamp"] = 1800000000
    call = cls.from_mnemonic(mnemonic=account[1], **kwargs).to_contract_call(offline_client)
    assert call.contract.lower() == offline_client.config.contracts.delegation_nft.lower()
    assert call.contract.lower() != offline_client.config.contracts.delegation.lower()
    assert decode_call(call, signature, kinds) == (ADDRESS, OTHER, HUGE, *tail)


@pytest.mark.parametrize(
    "kind,function",
    [("erc721", "createDRC721Reserveless"), ("erc1155", "createDRC1155Reserveless")],
)
def test_reserveless_nft_uses_current_metadata(kind, function, offline_client, account):
    request = sdk.CreateReservelessNftCollectionRequest.from_mnemonic(
        mnemonic=account[1],
        kind=kind,
        creator=ADDRESS,
        symbol="NFT",
        name="Collection",
        contract_uri="https://example.org/nft",
        burnable=True,
    )
    call = request.to_contract_call(offline_client)
    values = decode_call(
        call,
        function + "((address,string,string,string,bool,bool))",
        ["(address,string,string,string,bool,bool)"],
    )
    assert values[0] == (ADDRESS, "NFT", "Collection", "https://example.org/nft", False, True)


def test_reserve_permit_does_not_send_approve(offline_client, account):
    permit = sdk.PermitSignature(1800000000, 27, bytes([3]) * 32, bytes([4]) * 32)
    request = sdk.AddTokenReserveNftRequest.from_mnemonic(
        mnemonic=account[1], nft=ADDRESS, token_id=HUGE, reserve_amount_raw=HUGE, permit=permit
    )
    data = decode_call(
        request.to_contract_call(offline_client),
        "addReserveByPermit(uint256,uint256,uint256,uint8,bytes32,bytes32)",
        ["uint256", "uint256", "uint256", "uint8", "bytes32", "bytes32"],
    )
    assert data == (HUGE, HUGE, permit.deadline, permit.v, permit.r, permit.s)
    offline_client.erc20.allowance.assert_not_called()
    offline_client.send_raw_transaction.assert_not_called()


@pytest.mark.parametrize("indexes", [(), (1, 1), (-1,), (1.0,), (True,), (2**256,)])
def test_invalid_complete_indices_rejected(indexes, offline_client, account):
    for cls in (sdk.CompleteStakeRequest, sdk.CompleteNftStakeRequest):
        with pytest.raises((ValueError, TypeError)):
            cls.from_mnemonic(mnemonic=account[1], indexes=indexes).to_contract_call(offline_client)


async def test_nft_reads_keep_status_separate_from_unfreeze_time(offline_client):
    stake = (ADDRESS, OTHER, ADDRESS, HUGE, HUGE + 1, 3, 1800000000)
    offline_client.nft._read_stake_call = AsyncMock(return_value=(stake, 2, 1, 1900000000))
    result = await offline_client.nft.get_frozen_stake(7)
    assert result.index == 7 and result.freeze_status == 2 and result.freeze_type == 1
    assert result.unfreeze_timestamp == 1900000000
    assert result.as_dict()["stake"]["amount"] == str(HUGE)
    assert result.as_dict()["stake"]["token_id"] == str(HUGE + 1)
    offline_client.nft._read_stake_call.return_value = (stake, 1, 1900000000)
    with pytest.raises(ValueError, match="format"):
        await offline_client.nft.get_frozen_stake(7)


async def test_nft_read_provider_and_block_are_forwarded(offline_client):
    stake = (ADDRESS, OTHER, ADDRESS, HUGE, HUGE, 3, 0)
    read = Mock(return_value=stake)
    function = Mock(return_value=SimpleNamespace(call=read))
    contract = SimpleNamespace(get_function_by_name=Mock(return_value=function))
    provider = SimpleNamespace(eth=SimpleNamespace(contract=Mock(return_value=contract)))

    async def rpc(fn):
        return fn(provider)

    offline_client.rpc.call = rpc
    result = await offline_client.nft.get_stake(ADDRESS, OTHER, ADDRESS, HUGE, block_identifier=123)
    assert result.amount_raw == HUGE
    read.assert_called_once_with(block_identifier=123)
    assert (
        provider.eth.contract.call_args.kwargs["address"].lower()
        == offline_client.config.contracts.delegation_nft.lower()
    )


def test_legacy_methods_are_fail_closed(offline_client, account):
    for request in (
        sdk.UpdateTokenMinSupplyRequest.from_mnemonic(
            mnemonic=account[1], token=ADDRESS, min_total_supply_raw=HUGE
        ),
        sdk.ApplyStakePenaltyRequest.from_mnemonic(
            mnemonic=account[1], validator=ADDRESS, delegator=OTHER, token=ADDRESS
        ),
        sdk.ApplyStakePenaltiesRequest.from_mnemonic(
            mnemonic=account[1], validator=ADDRESS, delegator=OTHER, token=ADDRESS
        ),
    ):
        with pytest.raises(ValueError, match="legacy opt-in"):
            request.to_contract_call(offline_client)


def test_weighted_safe_initializer(offline_client, account):
    request = sdk.CreateMultisigRequest.from_mnemonic(
        mnemonic=account[1],
        owners=(sdk.WeightedOwner(ADDRESS, 2), sdk.WeightedOwner(OTHER, 3)),
        weight_threshold=4,
        salt_nonce=HUGE,
    )
    call = request.to_contract_call(offline_client)
    safe, initializer, salt = decode_call(
        call, "createProxyWithNonce(address,bytes,uint256)", ["address", "bytes", "uint256"]
    )
    assert salt == HUGE and safe == offline_client.config.contracts.safe.lower()
    assert (
        initializer[:4]
        == Web3.keccak(
            text="setup((address,uint256)[],uint256,address,bytes,address,address,uint256,address)"
        )[:4]
    )
    args = decode(
        [
            "(address,uint256)[]",
            "uint256",
            "address",
            "bytes",
            "address",
            "address",
            "uint256",
            "address",
        ],
        initializer[4:],
    )
    assert args[:2] == (((ADDRESS, 2), (OTHER, 3)), 4)
    assert args[2:] == (ZERO_ADDRESS, b"", ZERO_ADDRESS, ZERO_ADDRESS, 0, ZERO_ADDRESS)


def test_safe_hash_matches_independent_eip712_encoding():
    tx = sdk.SafeTransaction(ADDRESS, nonce=7, value_wei=HUGE, data="0xabcdef", safe_tx_gas=80000)
    domain_type = Web3.keccak(text="EIP712Domain(uint256 chainId,address verifyingContract)")
    domain = Web3.keccak(encode(["bytes32", "uint256", "address"], [domain_type, 75, SAFE]))
    tx_type = Web3.keccak(
        text="SafeTx(address to,uint256 value,bytes data,uint8 operation,uint256 safeTxGas,uint256 baseGas,uint256 gasPrice,address gasToken,address refundReceiver,uint256 nonce)"
    )
    struct = Web3.keccak(
        encode(
            [
                "bytes32",
                "address",
                "uint256",
                "bytes32",
                "uint8",
                "uint256",
                "uint256",
                "uint256",
                "address",
                "address",
                "uint256",
            ],
            [
                tx_type,
                ADDRESS,
                HUGE,
                Web3.keccak(bytes.fromhex("abcdef")),
                0,
                80000,
                0,
                0,
                ZERO_ADDRESS,
                ZERO_ADDRESS,
                7,
            ],
        )
    )
    expected = Web3.keccak(b"\x19\x01" + domain + struct)
    assert HexBytes(sdk.safe_transaction_hash(SAFE, 75, tx)) == expected


def test_safe_signatures_sort_validate_and_bind_chain(account):
    tx = sdk.SafeTransaction(OTHER, 0, HUGE)
    a, b = Account.create(), Account.create()
    signatures = tuple(
        sdk.sign_safe_transaction(sdk.SignSafeTransactionRequest(SAFE, 75, tx, item.key.hex()))
        for item in (a, b)
    )
    packed = sdk.pack_safe_signatures(SAFE, 75, tx, signatures)
    ordered = sorted(signatures, key=lambda item: item.signer.lower())
    assert packed == b"".join(HexBytes(item.data) for item in ordered)
    with pytest.raises(ValueError, match="Duplicate"):
        sdk.pack_safe_signatures(SAFE, 75, tx, (signatures[0], signatures[0]))
    for safe, chain, changed in (
        (OTHER, 75, tx),
        (SAFE, 202020, tx),
        (SAFE, 75, replace(tx, nonce=1)),
    ):
        with pytest.raises(ValueError, match="does not match"):
            sdk.pack_safe_signatures(safe, chain, changed, signatures)


def test_safe_contract_and_eth_sign_signatures(account):
    tx = sdk.SafeTransaction(OTHER, 0)
    owner = account[0]
    digest = HexBytes(sdk.safe_transaction_hash(SAFE, 75, tx))
    signed = Account.sign_message(encode_defunct(primitive=digest), owner.key).signature
    eth_sig = sdk.SafeSignature(
        owner.address, "0x" + (signed[:-1] + bytes([signed[-1] + 4])).hex(), "eth_sign"
    )
    assert len(sdk.pack_safe_signatures(SAFE, 75, tx, (eth_sig,))) == 65
    contract_sig = sdk.SafeSignature(ADDRESS, "0xabcd", "contract")
    packed = sdk.pack_safe_signatures(SAFE, 75, tx, (contract_sig,))
    assert int.from_bytes(packed[32:64], "big") == 65 and packed[64] == 0
    assert int.from_bytes(packed[65:97], "big") == 2 and packed[97:] == bytes.fromhex("abcd")


async def test_safe_nonce_and_threshold_fail_before_signing(offline_client, account):
    request = sdk.ApproveMultisigTransactionRequest.from_mnemonic(
        mnemonic=account[1], safe=SAFE, transaction=sdk.SafeTransaction(OTHER, 9)
    )
    offline_client.tx.sign = AsyncMock(side_effect=AssertionError("Must not sign"))
    with pytest.raises(ValueError, match="nonce changed"):
        await offline_client.multisig.estimate_fee_for_operation(request)
    result = await offline_client.multisig.approve_transaction(request)
    assert not result.success
    tx = sdk.SafeTransaction(OTHER, 0)
    signature = sdk.sign_safe_transaction(
        sdk.SignSafeTransactionRequest.from_mnemonic(
            mnemonic=account[1], safe=SAFE, chain_id=75, transaction=tx
        )
    )
    execution = sdk.ExecuteMultisigTransactionRequest.from_mnemonic(
        mnemonic=account[1], safe=SAFE, transaction=tx, signatures=(signature,)
    )
    offline_client.multisig.state.return_value = replace(
        offline_client.multisig.state.return_value, weight_threshold=2
    )
    with pytest.raises(ValueError, match="weight"):
        await offline_client.multisig.build_operation(execution)
    offline_client.tx.sign.assert_not_called()


class ReadOnlyProvider(BaseProvider):
    def __init__(self, response):
        super().__init__()
        self.response = response
        self.calls = []

    def make_request(self, method, params):
        self.calls.append((method, params))
        if method == "eth_chainId":
            result = "0x4b"
        elif method == "eth_call":
            result = "0x" + encode(["bool"], [self.response]).hex()
        else:
            raise AssertionError(f"Unexpected RPC: {method}")
        return {"jsonrpc": "2.0", "id": 1, "result": result}


async def test_safe_inner_call_simulated_and_failure_blocks_send(offline_client, account):
    request = sdk.ExecuteMultisigTransactionRequest.from_mnemonic(
        mnemonic=account[1],
        safe=SAFE,
        transaction=sdk.SafeTransaction(OTHER, 0),
        signatures=(sdk.SafeSignature.preapproved(account[0].address),),
    )
    provider = ReadOnlyProvider(False)
    web3 = Web3(provider)

    async def call(fn):
        return fn(web3)

    offline_client.rpc.call = call
    del offline_client.multisig._simulate_execution
    with pytest.raises(ValueError, match="inner transaction"):
        await offline_client.multisig.build_operation(request)
    eth_call = next(params[0] for method, params in provider.calls if method == "eth_call")
    assert eth_call["to"].lower() == SAFE
    assert eth_call["from"] == account[0].address
    offline_client.send_raw_transaction.assert_not_called()


@pytest.mark.parametrize(
    "event,expected", [("ExecutionFailure", False), ("ExecutionSuccess", True)]
)
def test_safe_inner_receipt_overrides_outer_status_one(event, expected, offline_client):
    tx = sdk.SafeTransaction(OTHER, 0)
    safe_hash = HexBytes(sdk.safe_transaction_hash(SAFE, 75, tx))
    log = {
        "address": SAFE,
        "topics": [Web3.keccak(text=event + "(bytes32,uint256)"), safe_hash],
        "data": HexBytes(encode(["uint256"], [0])),
        "logIndex": 0,
        "transactionIndex": 0,
        "blockNumber": 100,
        "transactionHash": Web3.keccak(text="outer"),
        "blockHash": Web3.keccak(text="block"),
    }
    result = sdk.TransactionResult(True, status="success", receipt={"status": 1, "logs": [log]})
    checked = offline_client.multisig.check_execution_result(SAFE, tx, result)
    assert checked.success is expected
    assert result.success is True
    assert checked.status == ("success" if expected else "failed")


async def test_nft_operation_wraps_in_safe_without_signing(offline_client, account):
    request = sdk.CompleteNftStakeRequest.from_mnemonic(mnemonic=account[1], indexes=(0, 3))
    call = request.to_contract_call(offline_client)
    tx = await offline_client.multisig.build_transaction(SAFE, call, nonce=12)
    assert tx.to.lower() == offline_client.config.contracts.delegation_nft.lower()
    assert tx.data == call.data and tx.nonce == 12 and tx.operation == 0
    offline_client.multisig.state.assert_not_called()
    draft = await offline_client.nft.build_operation(request)
    assert (
        await offline_client.multisig.build_transaction(SAFE, draft, nonce=12)
    ).data == call.data


def test_testnet_nft_target_is_not_mainnet():
    config = sdk.NetworkConfig.testnet()
    assert config.contracts.delegation_nft.lower() == "0x07e2ad4dfc91412de09e33e4650254948b21a20c"
    assert config.contracts.delegation_nft != sdk.SystemContracts().delegation_nft


async def test_safe_creation_requires_real_singleton(offline_client, account):
    request = sdk.CreateMultisigRequest.from_mnemonic(
        mnemonic=account[1],
        owners=(sdk.WeightedOwner(ADDRESS, 1),),
        weight_threshold=1,
        salt_nonce=1,
    )
    offline_client.multisig._singleton_has_code.return_value = False
    with pytest.raises(ValueError, match="implementation has no contract code"):
        await offline_client.multisig.estimate_fee_for_operation(request)


@pytest.mark.parametrize(
    "position,value", [(0, OTHER), (1, ADDRESS), (2, OTHER), (4, 999), (5, 1), (6, 100)]
)
async def test_nft_read_rejects_wrong_stake_identity(position, value, offline_client):
    stake = [ADDRESS, OTHER, ADDRESS, HUGE, 0, 3, 0]
    stake[position] = value
    offline_client.nft._read_stake_call = AsyncMock(return_value=stake)
    with pytest.raises(ValueError, match="does not match"):
        await offline_client.nft.get_stake(ADDRESS, OTHER, ADDRESS, 0)


async def test_nft_empty_stake_is_an_empty_sentinel(offline_client):
    offline_client.nft._read_stake_call = AsyncMock(
        return_value=(ZERO_ADDRESS, ZERO_ADDRESS, ZERO_ADDRESS, 0, 0, 0, 0)
    )
    stake = await offline_client.nft.get_hold_stake(
        ADDRESS, OTHER, ADDRESS, 10, 1800000000, block_identifier=15
    )
    assert not stake.exists and stake.block_number == 15 and stake.amount_raw == 0


async def test_wrong_request_cannot_change_the_operation(offline_client, account):
    request = sdk.SellForExactDelRequest.from_mnemonic(
        mnemonic=account[1],
        token=ADDRESS,
        recipient=OTHER,
        amount_out_del="1",
        max_amount_in_raw=10**18,
    )
    offline_client.tx.sign = AsyncMock(side_effect=AssertionError("Must not sign"))
    result = await offline_client.token.buy_exact(request)
    assert not result.success
    offline_client.tx.sign.assert_not_called()


@pytest.mark.parametrize("transfer", [False, True])
@pytest.mark.parametrize("hold", [None, 1800000000])
async def test_existing_nft_stake_variants_build_unsigned_safe_calls(transfer, hold, offline_client, account, monkeypatch):
    cls = sdk.TransferNftStakeRequest if transfer else sdk.WithdrawNftRequest
    kwargs = {"nft": ADDRESS, "validator": OTHER, "token_id": HUGE, "amount": 2, "hold_timestamp": hold}
    if transfer:
        kwargs["new_validator"] = ADDRESS
    request = cls.from_mnemonic(mnemonic=account[1], **kwargs)
    signer = Mock(side_effect=AssertionError("Must not sign"))
    monkeypatch.setattr(Account, "sign_transaction", signer)
    draft = await offline_client.nft.build_operation(request)
    quote = await offline_client.nft.estimate_fee_for_operation(request, exact=True)
    safe_tx = await offline_client.multisig.build_transaction(SAFE, draft, nonce=17)
    kinds = ["address", "address", "uint256", "uint256"]
    values = [OTHER, ADDRESS, HUGE, 2]
    function = "transfer" if transfer else "withdraw"
    if hold is not None:
        function += "Hold"
        kinds.append("uint256")
        values.append(hold)
    if transfer:
        kinds.append("address")
        values.append(ADDRESS)
    signature = function + "(" + ",".join(kinds) + ")"
    assert HexBytes(safe_tx.data)[:4] == Web3.keccak(text=signature)[:4]
    assert decode(kinds, HexBytes(safe_tx.data)[4:]) == tuple(values)
    assert quote.ok and safe_tx.nonce == 17 and safe_tx.operation == 0
    assert draft.raw_tx is None
    signer.assert_not_called()
