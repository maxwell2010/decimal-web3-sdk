# Fees and Results
[Guide](README.md) | [API](reference/transactions.md)

Build a draft, calculate_fee, review the quote, then sign and broadcast explicitly.
estimate_fee_for_* methods never sign. High-level broadcast=False prevents
broadcasting but can sign locally. Do not log raw_tx_hex.

## Fee Only, No Mnemonic
```python
import asyncio
import os
from decimal_web3_sdk import DecimalClient, NetworkConfig, TransactionDraft, encode_memo_data, parse_units

async def main():
    owner = os.environ["WALLET_ADDRESS"]
    async with DecimalClient(NetworkConfig.testnet()) as client:
        tx = {
            "chainId": client.config.chain_id, "from": owner, "to": owner,
            "value": parse_units("0.000001", 18),
            "data": encode_memo_data("Fee example"),
            "nonce": await client.transaction_count(owner),
            "gasPrice": await client.gas_price(),
        }
        draft = TransactionDraft(tx, owner, owner, tx["value"])
        quote = await client.tx.calculate_fee(draft, exact=True)
        print("estimated DEL:", format(quote.fee_del, "f"))
        print("buffered budget DEL:", format(quote.gas_limit_fee_del, "f"))
        print("enough balance:", quote.ok)

asyncio.run(main())
```

Typed helpers such as estimate_fee_for_native_transfer accept mnemonic-derived
requests without signing them. For methods without a dedicated helper use
build_contract_call with the exact ABI calldata and calculate_fee.
Do not change recipients, amounts or memo between estimation and sending.
Simulation may require balance/allowance; a revert is not a zero fee.

## Quote Fields
- gas_price_wei: price per gas unit; divide by 10^9 for gwei.
- estimated_gas: RPC simulation; gas_limit: buffered limit.
- estimated_fee_wei: estimated gas times price.
- gas_limit_fee_wei: gas-limit budget, not necessarily the final charge.
- required_wei: value plus selected fee budget.
- native_balance_wei, missing_wei, ok: balance preflight.

Default gas-limit multiplier is 1.10. exact=True selects unbuffered gas while
retaining the buffered budget field. This does not guarantee the final charge.
Oracle price and chain state can change. Default gas price has no hard cap.
Optional MAX_GAS_PRICE_* limits the initial price; an explicit minimum-global-fee
rejection can trigger one retry at the network-required price.

Approve and the main operation have separate fees unless permit or existing
allowance makes one transaction possible. Dry-run does not change allowance
for the second simulation. An approval-only estimate is NOT a full workflow quote.

## Result
TransactionResult.success describes the SDK step. is_successful means successful
receipt; is_pending means broadcast without confirmation. Receipt fields:
tx_hash, block_number, gas_used, effective_gas_price_wei, effective_fee_wei,
effective_fee_del. fee_wei/fee_del are the submitted budget.
Signed-only results have no network hash. For workflows inspect primary,
secondary, transaction_count, total_fee_del, extra_steps_required and both receipts.

Receipt defaults: 7 seconds, 3-second polling. Timeout means pending, not failure.
Display user_message; do not expose raw technical error messages.
Builders and read methods may raise exceptions directly.
Use format(value, "f") for amounts and str(raw_integer) for JSON base units:
JavaScript Number cannot preserve every uint256. Never serialize secret-bearing
requests with asdict or __dict__.
