# Checks and Bridge
[Guide](README.md) | [Check examples](transactions/checks.md) | [Bridge examples](transactions/bridge.md)

ChecksService: create_del creates equal-denomination checks; total value equals
amount_wei times signers count. create_token takes amount_raw and an optional
PermitSignature; without permit, allowance must already exist. It does not
silently approve tokens. redeem needs paired check hashes and signatures.
The checks nonce is the contract's nonce, not the wallet transaction nonce.

BridgeService: transfer_native sends amount_wei plus service_fee_wei;
transfer_token sends tokens with separately payable native service fee and
requires existing allowance. to_chain_id is the bridge protocol's uint16 chain
identifier, not automatically the EVM chain ID. complete_transfer requires a
valid encoded_vm supplied by the bridge. Source confirmation does not prove
destination completion. No relayer or proof service is bundled.

These methods require an explicit, verified contract address. Offline encoding
is tested; end-to-end bridge/check settlement was not executed in release QA.
Never publish redemption signatures, permit data or signed transactions.
