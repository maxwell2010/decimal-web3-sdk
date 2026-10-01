from decimal_web3_sdk import NetworkConfig


def test_testnet_system_contracts_use_testnet_deployments():
    config = NetworkConfig.testnet()
    mainnet = NetworkConfig.mainnet()

    assert config.chain_id == 202020
    assert config.contracts.delegation_nft.lower() == config.contracts.delegation.lower()
    expected = {
        "contract_center": "0xbc96b61f137f28f0da47cc4ef06e5f984b565a2e",
        "delegation": "0x0d8e8ce36dade42682dd8cc6288d6a8d324bac2c",
        "master_validator": "0x5dbe5eb59d73f596e19a8f64f226c71bbc8ea36f",
        "nft_center": "0x11ae5297d0b5886914661938fcb8aedc08622194",
        "token_center": "0xb8f9c4a26b91a65ac0d3f34e230a4c9ad09aef4a",
        "wdel": "0x0e7c2cd8dc3a8ae787a8142f45b268ec27feeb8b",
    }
    for name, address in expected.items():
        assert getattr(config.contracts, name).lower() == address
        assert getattr(config.contracts, name).lower() != getattr(mainnet.contracts, name).lower()
