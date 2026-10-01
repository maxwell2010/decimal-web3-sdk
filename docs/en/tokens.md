# Tokens
[Guide](README.md) | [All token transaction examples](transactions/tokens.md)
| [ERC20 API](reference/erc20.md) | [Token API](reference/token.md)

ERC20 reads: info(address) returns name/symbol/decimals; balance(token, owner)
returns TokenBalance with raw/formatted fields and precision-safe as_dict();
allowance(token, owner, spender) returns raw integer allowance.
`client.token.properties(token)` reads reserve or reserveless contract properties.
Reserve tokens expose `creator`, `min_total_supply_raw` and
`max_total_supply_raw`; the minimum is a redemption threshold and may exceed
current `total_supply_raw`. Reserveless tokens expose `owner`, `cap_raw`,
`mintable` and `burnable`; `uint256.max` means no cap (`unlimited_cap=True`).
`owner` denotes current control, not necessarily the historical creator.
`as_dict()` keeps amounts as exact strings, never floats.

```python
properties = await client.token.properties(token_address)
balance = await client.erc20.balance(token_address, wallet_address)
print(properties.as_dict()["total_supply"]["raw"])  # issued supply, not a wallet balance
print(balance.raw_string)                         # spendable wallet balance
```

Discovering received reserveless tokens requires a network catalog of contract
addresses; holdings cannot be inferred from `creator` or `totalSupply`.
An RPC or `decimals()` failure must not be treated as a zero balance.
Updating the `identity` of an existing reserveless token is not guaranteed:
verify a setter on that exact contract implementation before exposing it.
build_transfer_data, build_transfer_from_data, build_approve_data and
build_permit_data only encode ABI data. permit_signature creates an EIP-2612
typed signature, not a network transaction. A nonces method alone is not proof
of permit compatibility: custom domain/version/permit variants need validation.

Transaction operations: transfer, transferFrom, approve, multisend, reserve-token
buy/sell/convert, burn, mint, details update, reserve/reserveless token creation.
Creation limits and reserve helpers are snapshot rules; verify current on-chain
requirements. Creation commission/reserve is separate from gas.
min_amount_out and min_amount_del_out_wei are slippage limits, not estimates.
Most metadata/supply/mint operations require issuer permissions.

Existing sufficient allowance avoids a new approval. Compatible permit can combine
authorization and the primary operation, including multisend memo, in one transaction.
An ordinary ERC20 approve cannot authorize the wallet by calling it from multicall:
msg.sender would be the multicall contract. Separate approval fees must remain visible.
auto_approve=False is the default for multisend, conversion and delegation.
If permit is unsupported and allowance is insufficient, the SDK returns
extra_steps_required without broadcasting an approval. Explicit auto_approve=True
permits a two-transaction workflow and requires wait_receipt=True for broadcast.
prefer_permit controls permit selection. Set a short permit_deadline instead of
an unlimited deadline.

Direct ERC20 transfer does not accept memo. ERC20 multisend does. DEL needs no
token permission. Exact-in/out variants, some metadata setters and reserve
calculators are not all implemented; see [scope](status.md).
