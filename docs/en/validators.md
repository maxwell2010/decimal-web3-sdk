# Validators
[Guide](README.md) | [All validator examples](transactions/validators.md)
| [API](reference/decimal.md)

validator_status returns the contract's numeric status; validator_is_active and
validator_is_member return booleans. REST validators/validator and
validator_delegations return indexed metadata, not authority to operate a validator.

pause_self_validator and unpause_self_validator affect the signer's validator.
pause_validator/unpause_validator take a target address and require contract
authorization. They are real operator actions: do not use a production validator
for a test. All examples disable broadcast.

Creating/removing validators, changing metadata/commission, penalties and the
complete admin surface are not implemented as high-level methods.
Generic ContractCallRequest is an escape hatch with an explicitly reviewed ABI,
not a claim that those workflows have been tested.
