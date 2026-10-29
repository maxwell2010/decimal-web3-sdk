# NFT
[Guide](README.md) | [All NFT examples](transactions/nft.md) | [API](reference/nft.md)

Reads: owner_of for ERC721; balance_of for ERC721 or ERC1155 (with token ID);
is_approved_for_all for collection operator permission.
Requests distinguish kind="erc721"/"erc1155", token_id and amount.
ERC1155 batch token_ids/amounts must be parallel nonempty lists.

Implemented entry points cover collection creation, mint, transfer/batch transfer,
single-ID or collection approval, burn, disable mint, metadata URI, DEL reserve,
delegation/hold/withdrawal and validator-to-validator NFT stake movement.
Read the generated request fields: raw reserve units, native value_wei and NFT
quantity are different. Approved operator access may require a separate transaction.
There is no general promise of NFT permit support.

## ERC-1155 Reserve

For the reviewed Decimal implementation, mint takes the total reserve, not the
amount per NFT. For a new ID, the contract checks the minimum using integer
division of the total by the quantity. For an existing ID, the exact total is
`rate(token_id) * amount`; `rate` is the ID reserve divided by `totalSupply`,
rounded down. Use integer base units, not `float`. `value_wei` is the total DEL;
`reserve_amount_raw` is the total ERC-20 reserve. Do not set both reserve types.

Validation on 2026-10-29: on a local mainnet fork (block 34334329), collection
`0x40C3341CBEfE853ed5fdA22c95440DD43427994a`, ID 1, had a nonzero rate of
`8333333333333333333333` base units. For three NFTs, the exact ERC-20 reserve
was `24999999999999999999999` base units. After funding and approval only on
the fork, the exact `eth_call` succeeded; one unit less returned
`InvalidReserve`. The preparation transfers and approval were not sent to
mainnet. A new ID was also checked with DEL in a mainnet `eth_call` and ERC-20
on the fork; a below-minimum amount returned `InvalidMinReserve`. These checks
do not establish compatibility with every collection or a successful mainnet
mint transaction.

Mainnet NFT addresses were aligned with the reviewed protocol profile and code
presence checked. Legacy typed NFT ABIs and current deployed variants still need
method-by-method live compatibility tests. Reserve mint variants, resets and
completion are not full JS parity. The compatibility adapter candy_protocol
has a separate allowlisted mainnet ABI; it is not a replacement for all NFT APIs.
Do not infer live support from an offline ABI encoding test.
