# Current NFT Protocol
[Guide](README.md) | [Transactions](transactions/nft.md)

Protocol review started 2026-09-16. Version 0.1.3 includes these changes and
funded testnet creation, mint, transfer and burn of DRC721/DRC1155. See the
[testnet receipts](../validation/testnet-transaction-campaign-2026-09-24.md).
Untried NFT staking and mainnet compatibility are not implied.

## Collection Is Not An Instance
create_collection uses createDRC721/createDRC1155 for a reserved collection.
create_reserveless_collection uses their Reserveless variants. All use the tuple
creator, symbol, name, contractURI, refundable, burnable. Creation sends no reserve
and mints no NFTs. The symbol identifies the collection, not a reserve ERC20.

Inspect client.nft.created_collections(receipt) for NFTCreated events from the
configured NFTCenter. Match creator, kind, symbol, name and URI to the request;
do not select an arbitrary event from a multicall. A success receipt alone is not
proof of minting. The decoder never invents token ID 1 or an owned balance.
Use balance_of/owner_of for ownership and collection_state for registration/mode.

The observed transaction in the [evidence](../validation/nft-protocol-sync.md)
created an empty reserveless collection. It cannot be changed into a reserved
collection. Mint is a separate transaction and needs a separate confirmation.

## Reserves And Mint
- DEL: value_wei is the total native reserve; mint uses payable mintByDEL.
  Keep reserve_amount_raw zero and reserve_token the zero address. No approve.
- ERC20: reserve_amount_raw is the total raw token reserve, reserve_token is its
  contract address, value_wei is zero. NFTCenter.checkToken must accept it.
  The token needs allowance to the NFT collection, not NFTCenter.
- Reserveless: all reserve fields must be zero. Supplying them is rejected
  instead of silently creating an unbacked NFT.
- DRC721 creates one auto-assigned ID; amount=1 and token_id=None.
- DRC1155 amount counts copies of the same explicit ID (including ID 0).
  reserve_amount_raw/value_wei is TOTAL, not per copy.
- The reviewed MIN_RESERVE is 1000000000000000 raw units per new NFT/copy.
  It is not universally 0.001 display tokens; use the selected token's decimals.
  build_mint reads the live minimum and uses integer arithmetic.
- Existing DRC1155 IDs must retain reserve type AND token address, with total
  reserve equal to rate(id) * amount. get_reserve returns exact raw totals.

SDK guards preserve the token address even though the inspected contract only
checks reserve type and rate on additional mint. RPC/eligibility failures propagate;
they are not a successful check. Fresh estimateGas remains necessary because state
can change between reads and sending. Mint authority and gas/balance checks still apply.

## Unsigned Preparation
The example uses a seed only for local identity derivation. It never signs,
approves, uploads metadata or broadcasts:

```python
import asyncio
import os
from decimal_web3_sdk import DecimalClient, CreateNftCollectionRequest, MintNftRequest

async def main():
    mnemonic = os.environ["MNEMONIC"]
    async with DecimalClient() as client:
        create = CreateNftCollectionRequest.from_mnemonic(
            mnemonic=mnemonic, kind="erc1155", symbol="EXAMPLE", name="Example",
            contract_uri=os.environ["CONTRACT_URI"], refundable=True, burnable=True,
        )
        draft = await client.nft.build_create_collection(create)
        quote = await client.tx.calculate_fee(draft, exact=True)
        print(quote.estimated_fee_del)
        # NFT_ADDRESS must be a separately confirmed existing reserved collection.
        mint = MintNftRequest.from_mnemonic(
            mnemonic=mnemonic, kind="erc1155", nft=os.environ["NFT_ADDRESS"],
            to=os.environ["RECIPIENT"], token_uri=os.environ["TOKEN_URI"],
            token_id=0, amount=3, value_wei=3000000000000000,
        )
        mint_draft = await client.nft.build_mint(mint)
        mint_quote = await client.tx.calculate_fee(mint_draft, exact=True)
        print(mint_quote.estimated_fee_del)

asyncio.run(main())
```

For ERC20 inspect client.erc20.allowance(token, owner, collection). If insufficient,
prepare a separate Erc20ApproveRequest with spender=collection and the EXACT total
(format_units_string(total_raw, decimals)). build_erc20_approve and calculate_fee
do not send it. Confirm approval separately, then rebuild and re-estimate mint.
Without allowance a failed mint estimate is not zero gas or proof that approval's
fee covers both steps. No implicit infinite approval or automatic second signature.

## Shared Profile
Canonical ABIs are nft_center.json, nft_721.json and nft_1155.json under
src/decimal_web3_sdk/abi. Each records the official implementation/source digest.
Regenerate the Console profile from the SDK root:

```shell
python scripts/generate_nft_profile.py
python scripts/generate_nft_profile.py --check
```

Output: src/decimal_web3_sdk/profiles/candy_mainnet_v1.json. Its mainnet-only ABI
uses refundable, not allowMint. Contract factories and Python builders use these
same bundled ABIs. No runtime downloading or execution of remote ABI/source occurs.
set_token_uri is legacy-only: setTokenURI is absent in the reviewed current
implementations; allow_legacy=True is only for independently verified older code.
