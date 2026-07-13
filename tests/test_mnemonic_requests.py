from __future__ import annotations

import pytest

from decimal_web3_sdk.wallet import generate_mnemonic_account

from decimal_web3_sdk import (
    AddDelReserveNftRequest,
    BridgeCompleteTransferRequest,
    BridgeTransferNativeRequest,
    BridgeTransferTokenRequest,
    BurnNftRequest,
    BurnTokenRequest,
    BuyTokenRequest,
    ConvertTokenRequest,
    CreateChecksDelRequest,
    CreateChecksTokenRequest,
    CreateNftCollectionRequest,
    CreateReservelessTokenRequest,
    CreateTokenRequest,
    DelegateDelRequest,
    DelegateErc20Request,
    DelegateNftRequest,
    DisableMintNftRequest,
    HoldDelRequest,
    HoldErc20Request,
    HoldNftRequest,
    HoldStakeWithResetRequest,
    MintNftRequest,
    NftBatchTransferRequest,
    MintTokenRequest,
    MultisendDelRequest,
    MultisendErc20Request,
    MultisendRecipient,
    NftApprovalRequest,
    NftApproveRequest,
    NftTransferRequest,
    RedeemChecksRequest,
    ResetStakeHoldRequest,
    SellTokenRequest,
    SetTokenUriNftRequest,
    StakeTokenToHoldRequest,
    TransferNftStakeRequest,
    TransferStakeErc20Request,
    TransferStakeWithResetRequest,
    UnbondDelRequest,
    UnbondErc20Request,
    UpdateTokenDetailsRequest,
    ValidatorPauseRequest,
    ValidatorSelfPauseRequest,
    WithdrawHoldDelRequest,
    WithdrawHoldErc20Request,
    WithdrawNftRequest,
    WithdrawStakeWithResetRequest,
)


TEST_ACCOUNT = generate_mnemonic_account()
MNEMONIC = TEST_ACCOUNT.mnemonic or ""
PRIVATE_KEY = TEST_ACCOUNT.private_key
ADDRESS = "0x" + "1" * 40
TOKEN = "0x" + "2" * 40
VALIDATOR = "0x" + "3" * 40


REQUEST_CASES = [
    (DelegateDelRequest, {"validator": VALIDATOR, "amount_del": "1"}),
    (HoldDelRequest, {"validator": VALIDATOR, "amount_del": "1", "hold_timestamp": 1}),
    (UnbondDelRequest, {"validator": VALIDATOR, "amount_del": "1"}),
    (WithdrawHoldDelRequest, {"validator": VALIDATOR, "amount_del": "1", "hold_timestamp": 1}),
    (MultisendDelRequest, {"recipients": [MultisendRecipient(to=ADDRESS, amount_del="1")], "memo": "daily payout"}),
    (MultisendErc20Request, {"token": TOKEN, "recipients": [], "decimals": 18}),
    (DelegateErc20Request, {"token": TOKEN, "validator": VALIDATOR, "amount": "1"}),
    (HoldErc20Request, {"token": TOKEN, "validator": VALIDATOR, "amount": "1", "hold_timestamp": 1}),
    (UnbondErc20Request, {"token": TOKEN, "validator": VALIDATOR, "amount": "1"}),
    (WithdrawHoldErc20Request, {"token": TOKEN, "validator": VALIDATOR, "amount": "1", "hold_timestamp": 1}),
    (TransferStakeErc20Request, {"token": TOKEN, "validator": VALIDATOR, "new_validator": ADDRESS, "amount": "1"}),
    (StakeTokenToHoldRequest, {"token": TOKEN, "validator": VALIDATOR, "amount": "1", "old_hold_timestamp": 1, "new_hold_timestamp": 2}),
    (ResetStakeHoldRequest, {"validator": VALIDATOR, "delegator": ADDRESS, "hold_timestamp": 1}),
    (WithdrawStakeWithResetRequest, {"token": TOKEN, "validator": VALIDATOR, "amount": "1", "hold_timestamps_to_reset": [1]}),
    (TransferStakeWithResetRequest, {"token": TOKEN, "old_validator": VALIDATOR, "new_validator": ADDRESS, "amount": "1", "hold_timestamps_to_reset": [1]}),
    (HoldStakeWithResetRequest, {"token": TOKEN, "validator": VALIDATOR, "amount": "1", "new_hold_timestamp": 2, "hold_timestamps_to_reset": [1]}),
    (ValidatorSelfPauseRequest, {}),
    (ValidatorPauseRequest, {"validator": VALIDATOR}),
    (BuyTokenRequest, {"token": TOKEN, "amount_del": "1"}),
    (SellTokenRequest, {"token": TOKEN, "amount": "1"}),
    (ConvertTokenRequest, {"token_in": TOKEN, "token_out": ADDRESS, "amount_in": "1", "min_amount_out": "1"}),
    (BurnTokenRequest, {"token": TOKEN, "amount": "1"}),
    (MintTokenRequest, {"token": TOKEN, "to": ADDRESS, "amount": "1"}),
    (UpdateTokenDetailsRequest, {"token": TOKEN, "identity": "ipfs://meta", "max_total_supply_raw": 100}),
    (CreateReservelessTokenRequest, {"name": "Test", "symbol": "TEST", "mintable": True, "burnable": True, "initial_mint_raw": 1, "cap_raw": 100, "identity": "ipfs://meta"}),
    (CreateTokenRequest, {"name": "Test", "symbol": "TEST", "initial_mint_raw": 1, "min_total_supply_raw": 1, "max_total_supply_raw": 100, "crr": 50, "identity": "ipfs://meta"}),
    (CreateNftCollectionRequest, {"kind": "erc721", "symbol": "NFT", "name": "NFT", "contract_uri": "ipfs://collection"}),
    (MintNftRequest, {"kind": "erc721", "nft": TOKEN, "to": ADDRESS, "token_uri": "ipfs://token"}),
    (NftTransferRequest, {"kind": "erc721", "nft": TOKEN, "to": ADDRESS, "token_id": 1}),
    (NftBatchTransferRequest, {"nft": TOKEN, "to": ADDRESS, "token_ids": [1], "amounts": [1]}),
    (NftApprovalRequest, {"kind": "erc721", "nft": TOKEN, "operator": ADDRESS, "approved": True}),
    (NftApproveRequest, {"nft": TOKEN, "to": ADDRESS, "token_id": 1}),
    (BurnNftRequest, {"kind": "erc721", "nft": TOKEN, "token_id": 1}),
    (DisableMintNftRequest, {"kind": "erc721", "nft": TOKEN}),
    (SetTokenUriNftRequest, {"kind": "erc721", "nft": TOKEN, "token_id": 1, "token_uri": "ipfs://new-token"}),
    (AddDelReserveNftRequest, {"kind": "erc721", "nft": TOKEN, "token_id": 1, "reserve_wei": 123}),
    (DelegateNftRequest, {"kind": "erc721", "nft": TOKEN, "validator": VALIDATOR, "token_id": 1}),
    (HoldNftRequest, {"kind": "erc721", "nft": TOKEN, "validator": VALIDATOR, "token_id": 1, "hold_timestamp": 1}),
    (TransferNftStakeRequest, {"nft": TOKEN, "validator": VALIDATOR, "new_validator": ADDRESS, "token_id": 1}),
    (WithdrawNftRequest, {"nft": TOKEN, "validator": VALIDATOR, "token_id": 1}),
    (CreateChecksDelRequest, {"contract": TOKEN, "signers": [ADDRESS], "amount_wei": 1, "due_block": 100}),
    (CreateChecksTokenRequest, {"contract": TOKEN, "token": ADDRESS, "signers": [ADDRESS], "amount_raw": 1, "due_block": 100}),
    (RedeemChecksRequest, {"contract": TOKEN, "signatures": ["0x12"], "checks": ["0x" + "0" * 64]}),
    (BridgeTransferNativeRequest, {"contract": TOKEN, "to": ADDRESS, "amount_wei": 1, "service_fee_wei": 0, "to_chain_id": 1, "nonce": 1}),
    (BridgeTransferTokenRequest, {"contract": TOKEN, "token": ADDRESS, "to": ADDRESS, "amount_raw": 1, "service_fee_wei": 0, "to_chain_id": 1, "nonce": 1}),
    (BridgeCompleteTransferRequest, {"contract": TOKEN, "encoded_vm": "0x12", "unwrap_weth": False}),
]


@pytest.mark.parametrize(("request_cls", "kwargs"), REQUEST_CASES)
def test_high_level_request_can_be_created_from_mnemonic(request_cls, kwargs) -> None:
    request = request_cls.from_mnemonic(mnemonic=MNEMONIC, **kwargs)

    assert request.private_key == PRIVATE_KEY


def test_from_mnemonic_rejects_private_key_argument() -> None:
    with pytest.raises(ValueError, match="mnemonic or private_key"):
        DelegateDelRequest.from_mnemonic(
            mnemonic=MNEMONIC,
            validator=VALIDATOR,
            amount_del="1",
            private_key=PRIVATE_KEY,
        )
