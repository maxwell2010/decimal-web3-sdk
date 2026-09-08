import pytest
from decimal_web3_sdk.candy_protocol import build_unsigned_candy_call, load_candy_profile

OWNER = "0x1111111111111111111111111111111111111111"
RECIPIENT = "0x2222222222222222222222222222222222222222"
NFT = "0x3333333333333333333333333333333333333333"

def test_shared_erc721_calldata_without_keys_or_network():
    draft = build_unsigned_candy_call(owner=OWNER, address=NFT, contract_type="nft", signature="safeTransferFrom(address,address,uint256)", args=[OWNER, RECIPIENT, 2])
    assert draft["data"] == "0x42842e0e" + OWNER[2:].zfill(64) + RECIPIENT[2:].zfill(64) + "2".zfill(64)
    assert draft["value"] == "0" and draft["chainId"] == 75
    assert set(draft) == {"from", "to", "data", "value", "chainId"}

def test_reviewed_system_contracts_and_chain_cannot_be_overridden():
    profile = load_candy_profile()
    assert profile["nftCenter"] != profile["tokenCenter"]
    assert profile["nftDelegation"] == "0xe45adfcc739a0d10ce9462b58866c9a1a06035e2"
    with pytest.raises(ValueError):
        build_unsigned_candy_call(owner=OWNER, contract_type="nft", address=NFT, signature="disableMint()", args=[], chain_id=1)
    with pytest.raises(ValueError):
        build_unsigned_candy_call(owner=OWNER, contract_type="nftDelegation", address=NFT, signature="withdraw(address,address,uint256,uint256)", args=[RECIPIENT,NFT,2,1])

def test_nonpayable_and_read_methods_rejected_as_value_transactions():
    with pytest.raises(ValueError):
        build_unsigned_candy_call(owner=OWNER, contract_type="nft", address=NFT, signature="disableMint()", args=[], value_wei=1)
    with pytest.raises(ValueError):
        build_unsigned_candy_call(owner=OWNER, contract_type="nft", address=NFT, signature="creator()", args=[])
