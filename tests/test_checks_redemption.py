"""Offline check hashing/signing tests; no funded credentials or broadcasts."""

from eth_abi import encode
from eth_account import Account
from eth_account.messages import encode_defunct
from hexbytes import HexBytes
import pytest
from web3 import Web3

from decimal_web3_sdk import DecimalClient, NetworkConfig
from decimal_web3_sdk.wallet import checksum


def test_created_check_hashes_reads_only_matching_successful_logs():
    client = DecimalClient(NetworkConfig.testnet())
    check_hash = Web3.keccak(text="test-check")
    details_hash = Web3.keccak(text="test-details")
    topic = Web3.keccak(text="CreatedCheck(bytes32,(bytes32,address,uint8))")
    log = {
        "address": checksum(client.config.contracts.checks),
        "topics": [topic],
        "data": HexBytes(encode(
            ["bytes32", "(bytes32,address,uint8)"],
            [check_hash, (details_hash, checksum("0x" + "11" * 20), 0)],
        )),
        "logIndex": 0,
    }
    receipt = {"status": 1, "logs": [log]}
    assert client.checks.created_check_hashes(receipt) == (Web3.to_hex(check_hash),)
    assert client.checks.created_check_hashes({"status": 1, "logs": [
        {**log, "address": checksum("0x" + "22" * 20)},
    ]}) == ()
    with pytest.raises(ValueError, match="successful receipt"):
        client.checks.created_check_hashes({"status": 0, "logs": [log]})


def test_redemption_signature_matches_check_and_redeemer(monkeypatch):
    signer = Account.create()
    redeemer = Account.create().address
    monkeypatch.setattr(
        "decimal_web3_sdk.checks.mnemonic_to_private_key",
        lambda mnemonic, **kwargs: signer.key.hex(),
    )
    check_hash = Web3.to_hex(Web3.keccak(text="test-check"))
    signature = DecimalClient(NetworkConfig.testnet()).checks.sign_redemption(
        check_hash, redeemer, "test-only-placeholder",
    )
    digest = Web3.solidity_keccak(["bytes32", "address"], [check_hash, redeemer])
    recovered = Account.recover_message(encode_defunct(primitive=digest), signature=signature)
    assert recovered == signer.address
    with pytest.raises(ValueError, match="32 bytes"):
        DecimalClient(NetworkConfig.testnet()).checks.sign_redemption(
            "0x1234", redeemer, "test-only-placeholder",
        )
