# Documentation

Version 0.1.2, GitHub preview. [Russian](../ru/README.md) | [Package](../../README.md)

Start with [installation, OS support and dependencies](install.md).

1. [Networks and wallets](networks-wallets.md)
2. [Fees, signing and results](fees-results.md)
3. [DEL](del.md)
4. [Tokens](tokens.md)
5. [Delegation and holds](staking.md)
6. [NFT](nft.md)
7. [Validators](validators.md)
8. [Checks and bridge](checks-bridge.md)
9. [Data, CLI and advanced APIs](data-advanced.md)
10. [All public API signatures](api.md)
11. [Coverage and limitations](status.md)
12. [Build and publish](releasing.md)
13. [Official JS/Go comparison](upstream-parity.md)
14. [Additional operations, Safe and updated NFT sources](transaction-parity-development.md)

Required request fields have no default. Optional fields are listed in the
reference. `*_wei` means DEL base units, `*_raw` means token base units;
`amount_del`, `amount`, `amount_in` use human units. One DEL is 10^18 base units.
Read token decimals from its contract. Rebase does not justify dividing twice.
Exception: NFT `amount` is an integer count, not an 18-decimal fungible amount.

Every transaction has a standalone example. Set the environment variables
referenced by that example first. Mnemonics are entered through a hidden prompt;
testnet is selected and broadcasting disabled. See [Security](../../SECURITY.md).
