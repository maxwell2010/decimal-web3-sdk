# Tokens
[Guide](README.md) | [All token transaction examples](transactions/tokens.md)
| [ERC20 API](reference/erc20.md) | [Token API](reference/token.md)

ERC20 reads: info(address) returns name/symbol/decimals; balance(token, owner)
returns TokenBalance with raw/formatted fields and precision-safe as_dict();
allowance(token, owner, spender) returns raw integer allowance.
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
auto_approve=False allows callers to handle it explicitly; prefer_permit controls
permit selection. Set a short permit_deadline instead of an unlimited deadline.

Direct ERC20 transfer does not accept memo. ERC20 multisend does. DEL needs no
token permission. Exact-in/out variants, some metadata setters and reserve
calculators are not all implemented; see [scope](status.md).
