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

## TLS Trust

From version `0.1.2`, SDK-owned REST and WebSocket sessions use
certifi's CA bundle instead of automatically loading the Windows certificate cache.
Certificate validity, trusted issuer and hostname checks remain enabled. Missing or
invalid custom CA files fail closed; there is no retry with verification disabled.
RPC already uses Requests' verified CA handling.

For a private CA, set `tls_ca_file` to a PEM CA bundle containing all roots required
for your endpoints. It replaces the default trust bundle for REST, WSS and RPC:

```python
import os
from dataclasses import replace
from decimal_web3_sdk import NetworkConfig

config = replace(NetworkConfig.mainnet(), tls_ca_file=os.environ["MY_CA_BUNDLE"])
```

`NetworkConfig.custom(tls_ca_file=...)` is also supported. Presets read
`DECIMAL_TLS_CA_FILE`; testnet/devnet first check `DECIMAL_TESTNET_TLS_CA_FILE` /
`DECIMAL_DEVNET_TLS_CA_FILE`, then the shared variable. These do not change Windows
or global Python settings. SDK-owned aiohttp sessions honor `SSL_CERT_FILE` and/or
`SSL_CERT_DIR` when no `tls_ca_file` is specified; a custom-only directory does not
implicitly add public roots. RPC retains Requests' `REQUESTS_CA_BUNDLE` /
`CURL_CA_BUNDLE` behavior without an explicit SDK CA file. A caller-supplied
`DecimalWsClient` session retains its own TLS policy and ownership.

This follows [aiohttp's verified certifi configuration](https://docs.aiohttp.org/en/stable/client_advanced.html#ssl-control-for-tcp-sockets).

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
