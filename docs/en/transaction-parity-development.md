# Additional Transactions: Development

Version **0.1.2.dev0**, unpublished. Release 0.1.1 is unchanged.
No new operation was broadcast on mainnet or testnet. No real mnemonic/private key was used.

## Added Operations

Typed counterparts cover the 24 previously missing JS operations. Two reserveless
NFT creation variants share one Python method with `kind`, yielding 23 methods.
The NFT feature branch adds `nft.reset_stake_holds`, for **79 catalog methods
instead of 55**. These are wrapper counts, not verified live scenarios or unique protocol types.

| Group | New methods |
| --- | --- |
| DEL | `tx.burn_del` |
| Tokens | `token.buy_exact`, `sell_for_exact_del`, `convert_to_del`, `update_min_supply` |
| Stakes | `decimal.complete_stake`, `apply_stake_penalty`, `apply_stake_penalties` |
| Validators | `decimal.add_validator_token`, `add_validator_del`, `remove_validator`, `update_validator_metadata` |
| NFT | `nft.create_reserveless_collection`, `add_token_reserve`, `stake_to_hold`, `reset_stake_hold`, `reset_stake_holds`, `withdraw_with_reset`, `transfer_with_reset`, `hold_with_reset`, `complete_stake` |
| Safe | `multisig.create`, `approve_transaction`, `execute` |

Complete examples and required fields: [DEL](transactions/del.md),
[tokens](transactions/tokens.md), [staking](transactions/staking.md),
[validators](transactions/validators.md), [NFT](transactions/nft.md), [Safe](transactions/multisig.md).

## Fees Before Signing

Additional contract operations share one encoding path for estimation and sending:
`request.to_contract_call(client)` -> `service.build_operation(request)` ->
`service.estimate_fee_for_operation(request, exact=True)`.
These preparation/estimate methods never sign, create permit signatures or send approvals.
Calling a write method with `broadcast=False` signs locally after preflight;
it is not an unsigned fee-only operation.

```python
import asyncio
import getpass
import os
from decimal_web3_sdk import DecimalClient, NetworkConfig, BuyExactTokenRequest

async def main():
    request = BuyExactTokenRequest.from_mnemonic(
        mnemonic=getpass.getpass("Seed: "),
        token=os.environ["TOKEN"],
        recipient=os.environ["RECIPIENT"],
        amount_out_raw=int(os.environ["TOKEN_AMOUNT_RAW"]),
        max_amount_del=os.environ["MAX_AMOUNT_DEL"],
    )
    async with DecimalClient(NetworkConfig.testnet()) as client:
        quote = await client.token.estimate_fee_for_operation(request, exact=True)
        print("ready:", quote.ok)
        print("estimated DEL:", str(quote.estimated_fee_del))
        print("required DEL:", str(quote.required_del))

asyncio.run(main())
```

For native burning use `tx.build_burn_del` / `tx.estimate_fee_for_burn_del`.
Burning is irreversible. Native DEL never requires token approval. `exact=False`
retains the existing gas-limit buffer, a spending limit rather than actual fee.
Contract state changes can change the eventual gas requirements.

`*_raw`, `*_wei`, NFT `token_id`, NFT `amount`, indices and timestamps require
Python integers and reject rounding/coercion from floats. NFT `amount` is a count,
not a token quantity with 18 decimals. DEL amount fields accept exact strings or
Decimal. `NftStake.as_dict()` returns large amounts and IDs as strings.

## Permissions

New methods do not hide extra submissions. Token-based candidate registration and
NFT token reserve additions without permit require existing allowance. Invalid
permissions must fail RPC simulation before signing. `AddTokenReserveNftRequest.permit`
accepts a prepared `PermitSignature` for the actual reserve token and NFT spender.
GasCenter `ConvertToDelRequest` requires a permit for GasCenter and is distinct
from ordinary token selling. Its `estimated_gas` is a contract argument, not the
outer transaction gas limit. Correct owner, spender, value, nonce, deadline and
token permit support are required.

## NFT Hold And Completion

JS feature commit `7dc2e4600ce4aa3dd8baf685d2f31b4f53bc08c7` directly follows the
pinned master `6790d35e2decb0cbb06a9149a9c476c834f99223`. It fixes `withReset`
gas estimation: both estimate and submission must target **delegation-nft**, not
fungible Delegation. Added batch `resetHolds` and read methods `get_stake`,
`get_stake_id`, `get_hold_stake`, `get_frozen_stake`, `get_frozen_stakes`,
`get_freeze_time`. Use an explicit `block_identifier` for a consistent read snapshot.

Testnet NFT Delegation is now the feature branch address
`0x07e2ad4dfc91412de09e33e4650254948b21a20c`, not the mainnet address.
This does not validate the other inherited testnet contract addresses.

Withdrawal/transfer creates a frozen stake. Hold expiry is not wallet credit:
after the freeze period call `complete_stake(indexes)`. Obtain indices from a
queue/indexer and recheck with `get_frozen_stakes(indexes)`; indices are neither
validator IDs nor timestamps. Do not mistake a UI row offset for a queue index.

The current frozen stake ABI returns four fields:
`stake`, `freezeStatus`, `freezeType`, `unfreezeTimestamp`. The feature-branch
example shows an older three-field shape. The SDK rejects that shape instead of
mistaking an operation type for a date. Status is preserved separately; unknown
values are not treated as completion. A past date alone does not prove completion
or eligibility: simulate `complete`. Unindexed full on-chain queue enumeration is
not claimed; the inspected ABI has no getter returning the entire queue.

## Weighted Safe

Decimal Safe uses `(owner, weight)[]`, not just owner addresses. Creation requires
`WeightedOwner` values, a weight threshold and explicit `salt_nonce`.
`SafeTransaction` carries the Safe nonce and inner execution parameters, distinct
from the outer wallet nonce and gas price. Use
`sign_safe_transaction(SignSafeTransactionRequest.from_mnemonic(...))` to sign
locally with EIP-712. Signatures bind chain ID, Safe address and all transaction fields.
Alternatively, `approve_transaction` sends an on-chain approval of the entire
transaction tuple, which costs gas.

`execute` checks nonce, weights, unique owners and signature ordering. EIP-712,
Safe eth_sign, approved-hash and contract signatures are supported. Authorization
of preapproved/contract signatures is checked by the contract via eth_call, not
assumed locally. Outer `status=1` does not prove inner success: the SDK checks
`ExecutionSuccess`/`ExecutionFailure` for the correct Safe and expected hash.
For a receipt retrieved later, use `multisig.check_execution_result`.
Creation exposes `result.events["safe_address"]` when a receipt includes ProxyCreation.

`multisig.build_transaction(safe, unsigned_call, nonce=...)` wraps prepared NFT
or other calls, replacing nine repetitive JS builders. Safe owners must authorize
execution; the target contract sees the Safe as caller, not the outer sender.

## Limits And Sources

**225 tests passed** on Windows/Python 3.12, covering 79 catalog methods,
unsigned fee-only calls, independent calldata checks, large integers, Safe
signatures and NFT responses. Lint and source audit passed. One upstream
websockets.legacy deprecation warning remains. Mock gas/price tests are not live fee quotes.
[Machine-readable report](../validation/transaction-parity-development.json).

SDK reads at mainnet block 33638332 verified chain ID 75, five deployed contracts
and NFT getters. Freeze periods were 2592000 seconds (30 days) for withdrawal
and 1296000 seconds (15 days) for transfer; these are observed values, not SDK constants.
The official testnet RPC could not connect; testnet submission checks remain unverified.

Three counterparts are legacy-only: `update_min_supply`, `apply_stake_penalty`,
`apply_stake_penalties`. They are absent from the inspected current ABIs and
disabled by default. Use `allow_legacy=True` only for a known compatible older
deployment. It does not bypass permissions, fees or RPC simulation.
Current NFTCenter metadata calls a boolean `refundable`, while the JS type calls
it `allowMint`. Reserveless creation encodes `refundable=False` plus `burnable`;
equivalence to the old `allowMint` behavior is not claimed.

Bundled ABI fragments come from the official [Contract API](https://api.decimalchain.com/api/v1/contracts/docs/index.html).
Each `src/decimal_web3_sdk/abi/*.json` records the exact source address and date.
The [JS NFT branch](https://bitbucket.org/decimalteam/dsc-js-sdk/src/7dc2e4600ce4aa3dd8baf685d2f31b4f53bc08c7/)
and [go-smart-node](https://bitbucket.org/decimalteam/go-smart-node/src/9e6c6d718d662083c4a524376a66d2c50bd4bc77/contracts/)
were checked separately. The node has a current fungible Delegation ABI, but some
NFT/token files lag behind published API ABIs. A node repository update does not
prove every bundled ABI is current. No running validator was modified.

Live submission tests and the pre-existing partial matches in the
[matrix](upstream-parity.md), including some token/NFT selectors, permit variants
and mixed-asset multisend, remain outstanding.

## Console Handoff

Next: a validator tab with current-wallet authority checks, a multisig tab, NFT
validation and avatar uploads for validators, tokens and NFTs. UI permissions
do not replace contract authorization; do not pause/remove real validators in tests.

Official JS lists `https://testnet-nft-ipfs.decimalchain.com/` for all networks,
marked TODO. Its `ipfs.ts` uses `POST /upload` for NFTs, `POST /upload-image`
for images, multipart field `uploading_files`, and `GET /ipfs/{cid}` for retrieval.
Keep upload base and gateway configurable separately, for example
`DECIMAL_IPFS_API_URL` and `DECIMAL_IPFS_GATEWAY_URL`.
A root HEAD request passed normal TLS validation and returned HTTP 404.
This result applies only to that request and client stack, not to upload support.
In a subsequent console integration check, Python 3.12/aiohttp on Windows rejected
`POST /upload-image` before sending the body with `SSLCertVerificationError:
certificate has expired`. This is a reported console result, not an independently
repeated SDK test.

Independent TLS diagnostics on 2026-09-15 reproduced the Python error and identified
a stale cross-signed `ISRG Root X2` certificate in the local Windows `CA` store,
issued by `ISRG Root X1`, expired on 2025-09-15 at 16:00:00 UTC. Its SHA-256 is
`8B:05:B6:8C:C6:59:E5:ED:0F:CB:38:F2:C9:42:FB:FD:20:0E:6F:2F:F9:F8:5D:63:C6:99:4E:F5:E0:B0:27:01`.
The server's domain certificate, issued by Let's Encrypt YE1, is valid from
2026-07-22 05:31:02 UTC through 2026-10-20 05:31:01 UTC; all certificates delivered
by the server were within their validity periods. Python passed validation with
an in-memory copy of the same trust bundle excluding only that expired local CA,
with `CERT_REQUIRED` and hostname checking enabled. It also passed with a certifi
bundle. No persistent trust-store or application TLS settings were changed.
The reproduced expiry error is therefore a local trust-chain issue, not evidence
that Decimal's domain certificate has expired. Upload and persistence/pinning
remain unverified. Keep certificate verification enabled and report upload failures
clearly. Do not expose upload credentials or mnemonics in client code.

### Verified Client Trust Fix

The unreleased SDK now uses certifi for owned REST/WSS sessions, with an explicit
`tls_ca_file` override also passed to RPC. No Windows CA entries are deleted and
no verification is disabled. Custom CA precedence is documented in
[networks and wallets](networks-wallets.md#tls-trust-unreleased).

After this change, 242 offline tests pass, including 17 TLS tests. Real in-memory
handshakes accept an explicitly trusted private CA and reject expired, untrusted
and wrong-host server certificates. Ruff and generated-reference checks pass.
On 2026-09-15 at 02:29 UTC, SDK REST and WS-owned HTTP sessions reached the Decimal
IPFS root with normal TLS validation and HTTP 404. Read-only mainnet RPC returned
block 33644205. This is not a live WebSocket or upload/pinning test. No files or
transactions were submitted and no public release was published.

Deploy console updates only after their tests and rollback checks. This does
not authorize publication of a new public SDK release.
