# Historical Transaction Evidence

Reconciled on 2026-09-16. This is a coverage record, not a broadcast plan.
Existing receipts and offline regressions should be reused before proposing paid
retests. A network receipt, a fee estimate, an offline test and a transaction from
another application are different levels of evidence.

## SDK Transactions

| Scenario | Network | Evidence | Scope |
| --- | --- | --- | --- |
| Native DEL self-transfer | Testnet | `0x807320c65fdfe97c6bf348bb0eaa5a6da8867e1a0f560deab7e03170e6379501`, block 20785269, status 1, gasUsed 21000 | Saved transaction/receipt from 2026-06-16; not a fresh testnet read |
| Direct DEL self-transfer with memo | Mainnet | `0xf119a764fc998d1e684b5e07c916ef73addee6ebf85d564736ecc28a39b299c3`, block 33537085, status 1 | Re-read without signing; direct recipient and UTF-8 memo confirmed |
| DEL withdrawal with matured-hold reset | Mainnet | `0xc1dac6b3c70b0c689c6d0f1cb19c5bba57e93bc7f254788128d860dc238b492a`, block 33232007, status 1 | Re-read and decoded as withdrawWithReset, 4.21 DEL, hold key 1787078776; not proof of every staking operation or final payout |
| Native DEL self-transfer | Mainnet | `0x26a228cd649caa9832db8a0f43d0d17c68b1293ad046d54f33f2050c5365596e`, block 33662402 | New-network smoke of an already tested operation; no routine repeat needed |
| Direct DEL self-transfer with memo | Mainnet | `0x334d95a0ba1e5ade1b1e327322bb8947e52d0f4b0e64ed57636b875fc484e7e3`, block 33662479 | Same core scenario as the earlier successful mainnet memo transfer |
| DEL multisend with memo, two self-address rows | Mainnet | `0x727817ecf135777eaec2d6bc234fcc294203bed8d929f81d232deeda2f12a2f8`, block 33662483 | Successful receipt, decoded payouts/memo and balance reconciliation |
| ERC20 self-transfer | Mainnet | `0x44a0bae55937696ba16db9a34929dfba2ed7d5c915644a5501f9c8b3f2e8330e`, block 33662489 | Successful receipt, matching Transfer event and unchanged token balance |

This identifies seven successful SDK receipts across five scenario variants,
not seven unique SDK methods and not complete lifecycle coverage.

## Existing Application And Protocol References

Re-read on mainnet without credentials, signing or broadcast:

- Token approve: `0x67db80a346b1ffcd63122283dc4185eee39564160a4afa1f9f96475db74322fd`, block 32714056, status 1.
- MINTCANDY multisend from the multisend service: `0xe54d546cddf34fe3d1a3bd12cd139b1c3fde8f7d183fc2f02f49cba5f2726f35`, block 32714057, status 1. Seventeen transferFrom calls followed by memo; 17 logs.
- CASHBACK protocol reference: `0x08203fc823f37083affde27b650b8eef24c0540b591192297546ac211363278d`, block 32688022, status 1. One permit, 26 transferFrom calls and memo in one aggregate; 27 logs.

These prove working on-chain formats. They are not attributed to the current
Python SDK's end-to-end workflow. Reuse their calldata for encoding/regression
checks; they do not by themselves establish FRIDAYCOIN permit compatibility.

## Do Not Count As Successful Contract Coverage

- Testnet createTokenReserveless: `0xfda34fac18f557fc57b4ea5ccd64474d258c56b6a49ee0cc5c1a5f68fca866e4`, block 20785435. Earlier investigation found no contract at the target and no token created. EVM status 1 was a no-op, not successful token creation.
- Historical testnet multisend: `0x40e681c38d36a88b3488c179b66ca55ccbdaef45fe020e993473604cd656b65e`, block 20785359. The old manifest calls this successful, but its saved gasUsed 23376 equals intrinsic calldata gas, and the saved self-transfer balance delta includes value as well as the fee. Contract execution/payout is not independently established. Retain as unverified until historical code/trace or payout evidence is available; do not fix uncertainty by sending another transaction.

The testnet multisend calldata contains one payout plus memo, not a multi-recipient
test. The saved TokenCenter sample has gasUsed equal to intrinsic gas as well.
Current SDK code checks prevent calls to empty contract addresses; that does not
retroactively validate old receipts.

## Existing Simulations And Remaining Work

Historical FRIDAYCOIN/Freedom checks passed estimateGas for regular withdrawal,
matured-hold withdrawal, regular/hold stake transfer and withdrawWithReset. They
were not broadcast and should remain labelled as simulations. Historical state
and fee quotes are not current balances or current prices.

NFT, Safe, validator administration, checks, bridge and TokenCenter lifecycles do
not have successful SDK end-to-end receipts in the reviewed history. Offline
coverage and typed method availability must not be presented as live coverage.

## Offline Replay Against The Current SDK

Seven mainnet examples are stored in tests/fixtures/mined_mainnet_transactions.json.
The collector reads existing transactions/receipts only, checks identity and block,
and has an RPC allowlist that forbids signing, sending and batch requests. It never
loads wallet credentials. Outer transaction signatures and raw signed transactions
are excluded; the already-used permit inside public mined calldata is retained.

tests/test_historical_transactions.py rebuilds payloads byte-for-byte using the
current SDK and verifies Transfer logs against recipients and exact raw amounts.
Signing, outbound RPC and HTTP are blocked during these offline tests. The test
sender is substituted locally; no private key for a historical account is needed.

Verified encoding paths:

- Direct DEL memo, including the single-recipient multisend shortcut.
- Two-row native multisend plus memo, without token approval/permit calls.
- DEL withdrawWithReset with the original amount and hold timestamp.
- ERC20 transfer and exact-amount approve.
- Seventeen-recipient ERC20 multisend with existing allowance or a separate approve.
- Permit plus 26 transferFrom calls and memo as one aggregate.

This validates calldata, not a new broadcast or the full EIP-1559 envelope. Permit
signature generation/domain discovery is stubbed with the already-mined permit;
compatibility of another token's permit is not established. Old token/staking state
is not recreated. Some historical eth_getCode calls failed because state was pruned;
the fixtures record unavailable code rather than pretending it was empty.

The CASHBACK example exposed a receipt interpretation bug: type 2, no
effectiveGasPrice, tx.gasPrice equal to maxFeePerGas (4234300000000 wei), and no
baseFeePerGas in the historical block. The previous generic fallback treated a fee
ceiling as the paid price. The fix included in the 2026-09-16 refresh permits fallback only for fixed-price
type 0/1 without dynamic-fee fields. Missing actual fees remain unknown while the
successful receipt, hash and block remain available. Explicit effective prices
are still used, and legacy receipts retain their existing fallback.

Validation: 41 new offline tests; 329 total tests passed. No new signatures or
broadcasts were used to collect/replay these fixtures. These checks are included
in the maintainer-requested refresh of v0.1.2 without a package version change.

The Console companion check reproduced the same ceiling fallback in ethers
6.17.0 for both JsonRpcProvider and BrowserProvider. Its current UI and normalized
history do not consume that derived receipt fee, and successful receipts remain
successful. Five offline regression tests were added; all 170 Console tests passed.
No Console runtime change or deployment was needed. Future actual-fee displays
must inspect the raw receipt rather than trust the ethers-derived fee blindly.

Reproduce the offline checks without a network connection:

```shell
python -m pytest tests/test_historical_transactions.py -q
```

Refreshing evidence is optional and performs public read-only requests. Choose a
new output path to avoid replacing existing evidence silently:

```shell
python scripts/collect_transaction_fixtures.py --manifest tests/fixtures/transaction_sources.json --output reports/mined-mainnet-refresh.json
```

For future testing:

1. Start with this evidence and the existing regression suite, not a new transfer.
2. Compare selectors/calldata, receipts, events and public state using read-only calls.
3. Retest on-chain only for a documented uncovered scenario or a change that cannot
   be validated adequately offline. Record the reason, fixture and cost first.
4. Mainnet scenarios still require separate approval. Prior approval is not a
   standing instruction to repeat an already verified transaction.
