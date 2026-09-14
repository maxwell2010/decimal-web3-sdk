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

Mainnet NFT addresses were aligned with the reviewed protocol profile and code
presence checked. Legacy typed NFT ABIs and current deployed variants still need
method-by-method live compatibility tests. Reserve mint variants, resets and
completion are not full JS parity. The compatibility adapter candy_protocol
has a separate allowlisted mainnet ABI; it is not a replacement for all NFT APIs.
Do not infer live support from an offline ABI encoding test.
