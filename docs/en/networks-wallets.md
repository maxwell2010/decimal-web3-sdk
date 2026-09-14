# Networks and Wallets
[Guide](README.md) | [Configuration API](reference/config.md) | [Wallet API](reference/wallet.md)

| Preset | Chain ID | Official RPC |
| --- | --- | --- |
| mainnet (default) | 75 | https://node.decimalchain.com/web3/ |
| testnet | 202020 | https://testnet-val.decimalchain.com/web3/ |
| devnet | 202020 | https://devnet-val.decimalchain.com/web3/ |

Mapping follows the [official JS SDK](https://bitbucket.org/decimalteam/dsc-js-sdk/src/master/src/endpoints.ts).
Same chain ID does not mean the testnet and devnet deployments are interchangeable.
SystemContracts contains snapshots, not live discovery. Check contract compatibility.
The release check reached mainnet read-only; testnet was unavailable.

Mainnet indexed API default: https://api.decimalchain.com/api/v1/ .
Testnet/devnet use testnet-api/devnet-api subdomains. Legacy gate roots use
mainnet-gate/testnet-gate/devnet-gate with /api/. Old REST-node metadata uses
HTTP /rest/, following JS; never send credentials over HTTP. WS has no default.

Process environment overrides: DECIMAL_WEB3_URLS, DECIMAL_API_BASE,
DECIMAL_API_ROOT, DECIMAL_WS_URLS. For testnet/devnet use DECIMAL_TESTNET_
and DECIMAL_DEVNET_ prefixes. URL lists are comma-separated. The SDK does not
load arbitrary dotenv files on import. API keys are optional for your own API.

## Own Node
```python
import os
from dataclasses import replace
from decimal_web3_sdk import NetworkConfig

config = replace(NetworkConfig.testnet(), web3_urls=[os.environ["MY_TESTNET_RPC"]])
```

This preserves the selected chain and contract snapshot.
NetworkConfig.custom requires web3_urls for a working client; API/WS URLs are
needed only for those services. For a custom network supply SystemContracts
explicitly: its fallback is the mainnet snapshot, not discovery.
Placeholder URLs are not functioning nodes.

## Mnemonic and Address Indices
```python
import getpass
from decimal_web3_sdk import mnemonic_to_account, mnemonic_to_accounts

mnemonic = getpass.getpass("Mnemonic: ")
wallet = mnemonic_to_account(mnemonic, account_index=0)
print(wallet.address)
for index, account in enumerate(mnemonic_to_accounts(mnemonic, count=10)):
    print(index, account.address, account.derivation_path)
```

Indices 0..9 use `m/44'/60'/0'/0/i`. This is HD derivation, not transaction nonce.
BIP39 passphrase is optional and is not a PIN. Use either account_index or
account_path. Requests support from_mnemonic with the same settings.
generate_mnemonic_account creates new recovery material: secure its result.
eth-account labels its HD functionality unaudited.
