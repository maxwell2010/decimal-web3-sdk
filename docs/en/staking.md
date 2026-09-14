# Delegation, Holds and Withdrawals
[Guide](README.md) | [All staking examples](transactions/staking.md)
| [Contract reads](reference/decimal.md) | [Indexer reads](reference/rest.md)

Workflow: delegate -> regular stake or hold -> maturity -> withdraw/transfer.
withdraw/unbond requests start an unbonding period; they do not promise immediate
wallet credit. Transferring stake to another validator is not a wallet transfer.

Use get_stake(validator, delegator, token) for regular stake.
get_hold_stake additionally requires the exact hold-end timestamp, not its start.
get_stake_snapshot reads regular and known hold keys at one block, with exact
integer aggregation. It does not scan all validators or discover unknown holds.

```python
import asyncio
import json
import os
from decimal_web3_sdk import DecimalClient, NetworkConfig

async def main():
    async with DecimalClient(NetworkConfig.mainnet()) as client:
        snapshot = await client.decimal.get_stake_snapshot(
            os.environ["VALIDATOR"], os.environ["WALLET_ADDRESS"],
            client.config.contracts.wdel,
            hold_timestamps=json.loads(os.environ["HOLD_TIMESTAMPS"]),
        )
        print(json.dumps(snapshot.as_dict(), indent=2))

asyncio.run(main())
```

Native DEL in Delegation uses WDEL address and token_type DEL=4; DRC20=1
is different. Token ID and token type must match the queried position.
Do not substitute an API delta for a verified regular stake amount.
Indexer amounts have the API's 18-base-unit schema, not arbitrary token decimals.

wallet_staking_summary discovers indexed positions and optional unstakes.
wallet_stake_withdrawals combines current indexed unstakes and bounded withdrawal
history. Its output distinguishes is_matured from explicit is_completed.
completion_estimated marks a date inferred with configurable unbonding_days
(default 15); it is not a network guarantee. Unknown token raw units remain None.
include_completed includes entries explicitly marked complete; recent_days narrows
history and may omit still-relevant old entries.

Indexer flags and available_to_unbond are advisory. Verify contract snapshot and
estimate the exact withdrawal first. Store result.hold_timestamp/hold_time and
transaction hash in your application's database after confirmation; the SDK
has no persistent wallet database. A reset/with-reset operation is not required
for every hold: use the compatible contract method and simulate it.
