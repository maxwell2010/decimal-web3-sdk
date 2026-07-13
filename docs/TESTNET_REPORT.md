# Testnet Report

Дата: 2026-06-13

## Endpoint Status

Checked from the current workstation:

- `https://node.decimalchain.com/web3/` responds with `eth_chainId = 0x4b` for mainnet.
- `https://testnet-val.decimalchain.com/web3/` is the official `dsc-js-sdk` testnet Web3 URL, but returned `403` from this environment.
- `https://devnet-val.decimalchain.com/web3/` is the official `dsc-js-sdk` devnet Web3 URL, but the TLS handshake failed from this environment.
- `https://testnet-api.decimalchain.com/api/` and `https://testnet-gate.decimalchain.com/api/` returned `403` from this environment.
- Decimal API Swagger testnet paths follow the production service paths with the `testnet-` prefix, for example `https://testnet-api.decimalchain.com/api/v1/blocks/docs/index.html`. From this environment those docs endpoints also returned `403`, so they are recorded as official references but not relied on for automated live tests yet.

## SDK Policy

The SDK defaults use official Decimal endpoints and can be overridden:

```powershell
$env:DECIMAL_TESTNET_CHAIN_ID="202020"
$env:DECIMAL_TESTNET_WEB3_URLS="https://testnet-val.decimalchain.com/web3/"
$env:DECIMAL_TESTNET_API_ROOT="https://testnet-gate.decimalchain.com/api/"
$env:DECIMAL_TESTNET_API_BASE="https://testnet-api.decimalchain.com/api/"
```

For production or CI, prefer your own Decimal testnet/devnet node or explicitly supplied Decimal public endpoint.

## Generated Test Wallet

Address:

```text
0xE49d9951F755f2a6775f6fac08707A9d80169b1A
```

Observed through testnet RPC:

```text
balance: 0 tDEL
nonce: 0
```

Private key was generated for this test session only and must not be committed to repository files.

## Faucet Status

- The official `dsc-js-sdk` repository does not expose a faucet helper or faucet API.
- Broadcast tests remain blocked until the generated address is funded manually through a web faucet or by a known funded testnet account.

## Broadcast Matrix To Complete

- [ ] DEL transfer
- [ ] ERC20 transfer
- [ ] ERC20 approve
- [ ] Token buy
- [ ] Token sell
- [ ] Token convert
- [ ] DEL delegate
- [ ] DEL unbond
- [ ] DEL withdraw hold
- [ ] ERC20 delegate
- [ ] ERC20 unbond
- [ ] Multisend DEL
- [ ] Multisend ERC20
- [ ] NFT create collection
- [ ] NFT mint
- [ ] NFT transfer
- [ ] NFT delegate
- [ ] Checks DEL
- [ ] Checks token
- [ ] Checks redeem
- [ ] Bridge native
- [ ] Bridge token
- [ ] Bridge complete transfer

## Command Template

```powershell
$env:DECIMAL_TEST_PRIVATE_KEY="0x..."
$env:DECIMAL_TEST_TO="0x..."
$env:DECIMAL_TEST_DEL_AMOUNT="0.001"
$env:DECIMAL_TEST_BROADCAST="0"
decimal-sdk train-env
```

Switch `DECIMAL_TEST_BROADCAST` to `1` only when a funded testnet/devnet wallet is ready.
