# Native DEL
[Guide](README.md) | [All DEL transaction examples](transactions/del.md)

client.balance_wei returns an integer; balance_del returns exact Decimal.
NativeTransferRequest.from_mnemonic accepts to, amount_del and optional memo,
gas and gas_price_wei. send_del uses direct EVM value/data; a UTF-8 memo does not
turn it into a multicall. The recipient still receives one native transaction.

MultisendDelRequest contains a nonempty list of MultisendRecipient(to, amount_del).
The full list and optional memo are encoded for one multicall.
Native DEL never needs approve or permit. One-recipient multisend may be encoded
as a direct transfer. Read memo_capabilities()/memo_supported_for() for allowed formats.

Use estimate_fee_for_native_transfer or estimate_fee_for_multisend_del before
signing. Both include the actual message and recipients. No default marketing
message is injected by this SDK. Do not pass a token contract as native DEL.
Amounts must be exact strings or Decimal; raw integer JSON values should be strings.
