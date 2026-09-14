# Official SDK Comparison

[JSON](../upstream-parity.json) | [Status](status.md)

Source snapshot checked on 2026-09-14. Counts are named high-level EVM write entry points, not unique protocol transaction types or transactions in a block. A workflow may submit approval and a main transaction. One Python method can combine several JS variants through parameters; these totals are not coverage percentages.

| SDK | Commit / version |
| --- | --- |
| dsc-js-sdk | [6790d35e2dec](https://bitbucket.org/decimalteam/dsc-js-sdk/src/6790d35e2decb0cbb06a9149a9c476c834f99223/) |
| dsc-go-sdk | [3ef4a089b602](https://bitbucket.org/decimalteam/dsc-go-sdk/src/3ef4a089b6020889e60783c2026df5725fb960e2/) |
| Python | 0.1.1 |

| Group | JS | Go | Python |
| --- | ---: | ---: | ---: |
| del | 2 | 2 | 1 |
| multisend | 1 | 0 | 2 |
| tokens | 17 | 11 | 11 |
| staking | 17 | 6 | 17 |
| nft | 16 | 12 | 10 |
| nft_staking | 27 | 14 | 4 |
| validators | 6 | 6 | 4 |
| checks | 3 | 0 | 3 |
| bridge | 3 | 0 | 3 |
| multisig | 3 | 2 | 0 |
| **Total** | **95** | **53** | **55** |

JS: 92 specialized public methods + 3 multisig writes (create, approveHash, executeTx). Separately: 1 generic multiCall, 23 Safe builders and 1 local signer. Go: 58 exported methods-package functions, comprising 53 writes and 5 build/sign helpers. Python: 55 catalog methods; generic contract executors, fee estimators and reads are excluded.

JS also declares 42 legacy catalog identifiers in txTypesNew.ts, including local check issuance and the EVM envelope. These are not 42 additional verified EVM operations and are not in the table. The commented-out JS mintNFT and diagnostic redeemChecksTest are excluded. Go scope is decimalevm/methods, not node code or Swagger wrappers.

## Mapping Limits

counterpart = a typed operation-level counterpart exists, not proof of live ABI compatibility. partial = incomplete counterpart or different ABI/route. missing = no dedicated typed counterpart. A generic contract call is not counted as implementing a transaction type.

- token-selector: Python buy/sell versus JS buyTokenForExactDEL/sellExactTokensForDEL.
- token-update-selector: Python updateDetails versus separate updateTokenIdentity/updateMaxTotalSupply.
- token-mint-selector: mint argument order/signature needs separate reconciliation.
- nft-del-selector: Python mintByETH versus upstream mintByDEL; needs ABI reconciliation.
- nft-collection-selector/nft-stake-variants/nft-standard-mint: collection types and legacy Delegation/DelegationNFT routes differ.
- mixed-assets: Python separates DEL and a single ERC20; JS accepts mixed assets in one multisend.
- signature-only: Python sign_permit signs locally rather than sending a standalone permit; not a PermitToken write counterpart.
- nft-permit-missing: token-reserve mint exists but the complete permit route is absent.

## Priority Gaps

Safe multisig; burn DEL; exact-output buy/sell; GasCenter.convertToDEL; minimum supply; validator creation/removal/metadata; stake complete/penalty; NFT token-reserve, hold/reset/complete and permit; mixed-asset multisend. Reconcile existing token/NFT ABIs before extending the method inventory.

## dsc-js-sdk

| Method | Python counterpart | Status / reason |
| --- | --- | --- |
| [multiSendToken](https://bitbucket.org/decimalteam/dsc-js-sdk/src/6790d35e2decb0cbb06a9149a9c476c834f99223/src/decimalevm/index.ts#lines-405) | `decimal.multisend_del`, `decimal.multisend_erc20` | partial: mixed-assets |
| [sendDEL](https://bitbucket.org/decimalteam/dsc-js-sdk/src/6790d35e2decb0cbb06a9149a9c476c834f99223/src/decimalevm/index.ts#lines-460) | `tx.send_del` | counterpart: network-abi-unverified |
| [burnDEL](https://bitbucket.org/decimalteam/dsc-js-sdk/src/6790d35e2decb0cbb06a9149a9c476c834f99223/src/decimalevm/index.ts#lines-473) | - | missing: no-typed-method |
| [createToken](https://bitbucket.org/decimalteam/dsc-js-sdk/src/6790d35e2decb0cbb06a9149a9c476c834f99223/src/decimalevm/index.ts#lines-477) | `token.create` | counterpart: network-abi-unverified |
| [createTokenReserveless](https://bitbucket.org/decimalteam/dsc-js-sdk/src/6790d35e2decb0cbb06a9149a9c476c834f99223/src/decimalevm/index.ts#lines-482) | `token.create_reserveless` | counterpart: network-abi-unverified |
| [convertToken](https://bitbucket.org/decimalteam/dsc-js-sdk/src/6790d35e2decb0cbb06a9149a9c476c834f99223/src/decimalevm/index.ts#lines-506) | `token.convert` | counterpart: network-abi-unverified |
| [approveToken](https://bitbucket.org/decimalteam/dsc-js-sdk/src/6790d35e2decb0cbb06a9149a9c476c834f99223/src/decimalevm/index.ts#lines-511) | `tx.approve_erc20` | counterpart: network-abi-unverified |
| [transferToken](https://bitbucket.org/decimalteam/dsc-js-sdk/src/6790d35e2decb0cbb06a9149a9c476c834f99223/src/decimalevm/index.ts#lines-517) | `tx.send_erc20` | counterpart: network-abi-unverified |
| [transferFromToken](https://bitbucket.org/decimalteam/dsc-js-sdk/src/6790d35e2decb0cbb06a9149a9c476c834f99223/src/decimalevm/index.ts#lines-523) | `tx.transfer_from_erc20` | counterpart: network-abi-unverified |
| [burnToken](https://bitbucket.org/decimalteam/dsc-js-sdk/src/6790d35e2decb0cbb06a9149a9c476c834f99223/src/decimalevm/index.ts#lines-529) | `token.burn` | counterpart: network-abi-unverified |
| [mintTokenReserveless](https://bitbucket.org/decimalteam/dsc-js-sdk/src/6790d35e2decb0cbb06a9149a9c476c834f99223/src/decimalevm/index.ts#lines-535) | `token.mint` | partial: token-mint-selector |
| [convertToDEL](https://bitbucket.org/decimalteam/dsc-js-sdk/src/6790d35e2decb0cbb06a9149a9c476c834f99223/src/decimalevm/index.ts#lines-541) | - | missing: no-typed-method |
| [buyTokenForExactDEL](https://bitbucket.org/decimalteam/dsc-js-sdk/src/6790d35e2decb0cbb06a9149a9c476c834f99223/src/decimalevm/index.ts#lines-547) | `token.buy` | partial: token-selector |
| [buyExactTokenForDEL](https://bitbucket.org/decimalteam/dsc-js-sdk/src/6790d35e2decb0cbb06a9149a9c476c834f99223/src/decimalevm/index.ts#lines-553) | - | missing: no-typed-method |
| [sellTokensForExactDEL](https://bitbucket.org/decimalteam/dsc-js-sdk/src/6790d35e2decb0cbb06a9149a9c476c834f99223/src/decimalevm/index.ts#lines-559) | - | missing: no-typed-method |
| [sellExactTokensForDEL](https://bitbucket.org/decimalteam/dsc-js-sdk/src/6790d35e2decb0cbb06a9149a9c476c834f99223/src/decimalevm/index.ts#lines-565) | `token.sell` | partial: token-selector |
| [updateTokenIdentity](https://bitbucket.org/decimalteam/dsc-js-sdk/src/6790d35e2decb0cbb06a9149a9c476c834f99223/src/decimalevm/index.ts#lines-571) | `token.update_details` | partial: token-update-selector |
| [updateTokenMaxTotalSupply](https://bitbucket.org/decimalteam/dsc-js-sdk/src/6790d35e2decb0cbb06a9149a9c476c834f99223/src/decimalevm/index.ts#lines-577) | `token.update_details` | partial: token-update-selector |
| [updateTokenMinTotalSupply](https://bitbucket.org/decimalteam/dsc-js-sdk/src/6790d35e2decb0cbb06a9149a9c476c834f99223/src/decimalevm/index.ts#lines-583) | - | missing: no-typed-method |
| [permitToken](https://bitbucket.org/decimalteam/dsc-js-sdk/src/6790d35e2decb0cbb06a9149a9c476c834f99223/src/decimalevm/index.ts#lines-589) | `erc20.sign_permit` | partial: signature-only |
| [createCollectionDRC721](https://bitbucket.org/decimalteam/dsc-js-sdk/src/6790d35e2decb0cbb06a9149a9c476c834f99223/src/decimalevm/index.ts#lines-595) | `nft.create_collection` | partial: nft-collection-selector |
| [createCollectionDRC1155](https://bitbucket.org/decimalteam/dsc-js-sdk/src/6790d35e2decb0cbb06a9149a9c476c834f99223/src/decimalevm/index.ts#lines-600) | `nft.create_collection` | partial: nft-collection-selector |
| [createCollectionDRC721Reserveless](https://bitbucket.org/decimalteam/dsc-js-sdk/src/6790d35e2decb0cbb06a9149a9c476c834f99223/src/decimalevm/index.ts#lines-605) | - | missing: no-typed-method |
| [createCollectionDRC1155Reserveless](https://bitbucket.org/decimalteam/dsc-js-sdk/src/6790d35e2decb0cbb06a9149a9c476c834f99223/src/decimalevm/index.ts#lines-610) | - | missing: no-typed-method |
| [approveNFT721](https://bitbucket.org/decimalteam/dsc-js-sdk/src/6790d35e2decb0cbb06a9149a9c476c834f99223/src/decimalevm/index.ts#lines-615) | `nft.approve` | counterpart: network-abi-unverified |
| [approveForAllNFT](https://bitbucket.org/decimalteam/dsc-js-sdk/src/6790d35e2decb0cbb06a9149a9c476c834f99223/src/decimalevm/index.ts#lines-623) | `nft.set_approval_for_all` | counterpart: network-abi-unverified |
| [mintReserveless](https://bitbucket.org/decimalteam/dsc-js-sdk/src/6790d35e2decb0cbb06a9149a9c476c834f99223/src/decimalevm/index.ts#lines-647) | `nft.mint` | counterpart: network-abi-unverified |
| [mintNFTWithDELReserve](https://bitbucket.org/decimalteam/dsc-js-sdk/src/6790d35e2decb0cbb06a9149a9c476c834f99223/src/decimalevm/index.ts#lines-661) | `nft.mint` | partial: nft-del-selector |
| [mintNFTWithTokenReserve](https://bitbucket.org/decimalteam/dsc-js-sdk/src/6790d35e2decb0cbb06a9149a9c476c834f99223/src/decimalevm/index.ts#lines-678) | `nft.mint` | partial: nft-permit-missing |
| [addDELReserveNFT](https://bitbucket.org/decimalteam/dsc-js-sdk/src/6790d35e2decb0cbb06a9149a9c476c834f99223/src/decimalevm/index.ts#lines-695) | `nft.add_del_reserve` | counterpart: network-abi-unverified |
| [addTokenReserveNFT](https://bitbucket.org/decimalteam/dsc-js-sdk/src/6790d35e2decb0cbb06a9149a9c476c834f99223/src/decimalevm/index.ts#lines-711) | - | missing: no-typed-method |
| [transferNFT](https://bitbucket.org/decimalteam/dsc-js-sdk/src/6790d35e2decb0cbb06a9149a9c476c834f99223/src/decimalevm/index.ts#lines-727) | `nft.transfer` | counterpart: network-abi-unverified |
| [transferBatchNFT1155](https://bitbucket.org/decimalteam/dsc-js-sdk/src/6790d35e2decb0cbb06a9149a9c476c834f99223/src/decimalevm/index.ts#lines-743) | `nft.transfer_batch_erc1155` | counterpart: network-abi-unverified |
| [disableMintNFT](https://bitbucket.org/decimalteam/dsc-js-sdk/src/6790d35e2decb0cbb06a9149a9c476c834f99223/src/decimalevm/index.ts#lines-751) | `nft.disable_mint` | counterpart: network-abi-unverified |
| [burnNFT](https://bitbucket.org/decimalteam/dsc-js-sdk/src/6790d35e2decb0cbb06a9149a9c476c834f99223/src/decimalevm/index.ts#lines-758) | `nft.burn` | counterpart: network-abi-unverified |
| [setTokenURINFT](https://bitbucket.org/decimalteam/dsc-js-sdk/src/6790d35e2decb0cbb06a9149a9c476c834f99223/src/decimalevm/index.ts#lines-781) | `nft.set_token_uri` | counterpart: network-abi-unverified |
| [delegateDEL](https://bitbucket.org/decimalteam/dsc-js-sdk/src/6790d35e2decb0cbb06a9149a9c476c834f99223/src/decimalevm/index.ts#lines-788) | `decimal.delegate_del` | counterpart: network-abi-unverified |
| [delegateDELHold](https://bitbucket.org/decimalteam/dsc-js-sdk/src/6790d35e2decb0cbb06a9149a9c476c834f99223/src/decimalevm/index.ts#lines-793) | `decimal.hold_del` | counterpart: network-abi-unverified |
| [delegateToken](https://bitbucket.org/decimalteam/dsc-js-sdk/src/6790d35e2decb0cbb06a9149a9c476c834f99223/src/decimalevm/index.ts#lines-798) | `decimal.delegate_erc20` | counterpart: network-abi-unverified |
| [delegateTokenHold](https://bitbucket.org/decimalteam/dsc-js-sdk/src/6790d35e2decb0cbb06a9149a9c476c834f99223/src/decimalevm/index.ts#lines-803) | `decimal.hold_erc20` | counterpart: network-abi-unverified |
| [transferStakeToken](https://bitbucket.org/decimalteam/dsc-js-sdk/src/6790d35e2decb0cbb06a9149a9c476c834f99223/src/decimalevm/index.ts#lines-808) | `decimal.transfer_stake_del`, `decimal.transfer_stake_erc20` | counterpart: network-abi-unverified |
| [transferStakeTokenHold](https://bitbucket.org/decimalteam/dsc-js-sdk/src/6790d35e2decb0cbb06a9149a9c476c834f99223/src/decimalevm/index.ts#lines-813) | `decimal.transfer_stake_del`, `decimal.transfer_stake_erc20` | counterpart: network-abi-unverified |
| [withdrawStakeToken](https://bitbucket.org/decimalteam/dsc-js-sdk/src/6790d35e2decb0cbb06a9149a9c476c834f99223/src/decimalevm/index.ts#lines-818) | `decimal.unbond_del`, `decimal.unbond_erc20` | counterpart: network-abi-unverified |
| [withdrawStakeTokenHold](https://bitbucket.org/decimalteam/dsc-js-sdk/src/6790d35e2decb0cbb06a9149a9c476c834f99223/src/decimalevm/index.ts#lines-823) | `decimal.withdraw_hold_del`, `decimal.withdraw_hold_erc20` | counterpart: network-abi-unverified |
| [stakeTokenToHold](https://bitbucket.org/decimalteam/dsc-js-sdk/src/6790d35e2decb0cbb06a9149a9c476c834f99223/src/decimalevm/index.ts#lines-828) | `decimal.stake_token_to_hold` | counterpart: network-abi-unverified |
| [stakeTokenResetHold](https://bitbucket.org/decimalteam/dsc-js-sdk/src/6790d35e2decb0cbb06a9149a9c476c834f99223/src/decimalevm/index.ts#lines-833) | `decimal.reset_stake_hold` | counterpart: network-abi-unverified |
| [stakeTokenResetHoldDEL](https://bitbucket.org/decimalteam/dsc-js-sdk/src/6790d35e2decb0cbb06a9149a9c476c834f99223/src/decimalevm/index.ts#lines-838) | `decimal.reset_stake_hold` | counterpart: network-abi-unverified |
| [withdrawTokenWithReset](https://bitbucket.org/decimalteam/dsc-js-sdk/src/6790d35e2decb0cbb06a9149a9c476c834f99223/src/decimalevm/index.ts#lines-843) | `decimal.withdraw_stake_with_reset`, `decimal.withdraw_del_stake_with_reset` | counterpart: network-abi-unverified |
| [transferTokenWithReset](https://bitbucket.org/decimalteam/dsc-js-sdk/src/6790d35e2decb0cbb06a9149a9c476c834f99223/src/decimalevm/index.ts#lines-848) | `decimal.transfer_stake_with_reset`, `decimal.transfer_del_stake_with_reset` | counterpart: network-abi-unverified |
| [holdTokenWithReset](https://bitbucket.org/decimalteam/dsc-js-sdk/src/6790d35e2decb0cbb06a9149a9c476c834f99223/src/decimalevm/index.ts#lines-853) | `decimal.hold_stake_with_reset` | counterpart: network-abi-unverified |
| [applyPenaltyToStakeToken](https://bitbucket.org/decimalteam/dsc-js-sdk/src/6790d35e2decb0cbb06a9149a9c476c834f99223/src/decimalevm/index.ts#lines-859) | - | missing: no-typed-method |
| [applyPenaltiesToStakeToken](https://bitbucket.org/decimalteam/dsc-js-sdk/src/6790d35e2decb0cbb06a9149a9c476c834f99223/src/decimalevm/index.ts#lines-864) | - | missing: no-typed-method |
| [completeStakeToken](https://bitbucket.org/decimalteam/dsc-js-sdk/src/6790d35e2decb0cbb06a9149a9c476c834f99223/src/decimalevm/index.ts#lines-868) | - | missing: no-typed-method |
| [delegateNFT](https://bitbucket.org/decimalteam/dsc-js-sdk/src/6790d35e2decb0cbb06a9149a9c476c834f99223/src/decimalevm/index.ts#lines-874) | `nft.delegate` | partial: nft-stake-variants |
| [delegateNFTHold](https://bitbucket.org/decimalteam/dsc-js-sdk/src/6790d35e2decb0cbb06a9149a9c476c834f99223/src/decimalevm/index.ts#lines-882) | `nft.hold` | partial: nft-stake-variants |
| [delegateNFTByPermit](https://bitbucket.org/decimalteam/dsc-js-sdk/src/6790d35e2decb0cbb06a9149a9c476c834f99223/src/decimalevm/index.ts#lines-890) | `nft.delegate` | partial: nft-stake-variants |
| [withdrawNFT](https://bitbucket.org/decimalteam/dsc-js-sdk/src/6790d35e2decb0cbb06a9149a9c476c834f99223/src/decimalevm/index.ts#lines-898) | `nft.withdraw` | partial: nft-stake-variants |
| [withdrawNFTHold](https://bitbucket.org/decimalteam/dsc-js-sdk/src/6790d35e2decb0cbb06a9149a9c476c834f99223/src/decimalevm/index.ts#lines-906) | `nft.withdraw` | partial: nft-stake-variants |
| [transferNFTStake](https://bitbucket.org/decimalteam/dsc-js-sdk/src/6790d35e2decb0cbb06a9149a9c476c834f99223/src/decimalevm/index.ts#lines-914) | `nft.transfer_stake` | partial: nft-stake-variants |
| [transferNFTStakeHold](https://bitbucket.org/decimalteam/dsc-js-sdk/src/6790d35e2decb0cbb06a9149a9c476c834f99223/src/decimalevm/index.ts#lines-922) | `nft.transfer_stake` | partial: nft-stake-variants |
| [delegateNFT1155](https://bitbucket.org/decimalteam/dsc-js-sdk/src/6790d35e2decb0cbb06a9149a9c476c834f99223/src/decimalevm/index.ts#lines-931) | `nft.delegate` | partial: nft-stake-variants |
| [delegateNFT1155Hold](https://bitbucket.org/decimalteam/dsc-js-sdk/src/6790d35e2decb0cbb06a9149a9c476c834f99223/src/decimalevm/index.ts#lines-939) | `nft.hold` | partial: nft-stake-variants |
| [withdrawNFT1155](https://bitbucket.org/decimalteam/dsc-js-sdk/src/6790d35e2decb0cbb06a9149a9c476c834f99223/src/decimalevm/index.ts#lines-947) | `nft.withdraw` | partial: nft-stake-variants |
| [withdrawNFT1155Hold](https://bitbucket.org/decimalteam/dsc-js-sdk/src/6790d35e2decb0cbb06a9149a9c476c834f99223/src/decimalevm/index.ts#lines-955) | `nft.withdraw` | partial: nft-stake-variants |
| [transferNFT1155Stake](https://bitbucket.org/decimalteam/dsc-js-sdk/src/6790d35e2decb0cbb06a9149a9c476c834f99223/src/decimalevm/index.ts#lines-963) | `nft.transfer_stake` | partial: nft-stake-variants |
| [transferNFT1155StakeHold](https://bitbucket.org/decimalteam/dsc-js-sdk/src/6790d35e2decb0cbb06a9149a9c476c834f99223/src/decimalevm/index.ts#lines-971) | `nft.transfer_stake` | partial: nft-stake-variants |
| [delegateDRC721](https://bitbucket.org/decimalteam/dsc-js-sdk/src/6790d35e2decb0cbb06a9149a9c476c834f99223/src/decimalevm/index.ts#lines-980) | `nft.delegate` | partial: nft-stake-variants |
| [delegateDRC721Hold](https://bitbucket.org/decimalteam/dsc-js-sdk/src/6790d35e2decb0cbb06a9149a9c476c834f99223/src/decimalevm/index.ts#lines-987) | `nft.hold` | partial: nft-stake-variants |
| [delegateDRC1155](https://bitbucket.org/decimalteam/dsc-js-sdk/src/6790d35e2decb0cbb06a9149a9c476c834f99223/src/decimalevm/index.ts#lines-994) | `nft.delegate` | partial: nft-stake-variants |
| [delegateDRC1155Hold](https://bitbucket.org/decimalteam/dsc-js-sdk/src/6790d35e2decb0cbb06a9149a9c476c834f99223/src/decimalevm/index.ts#lines-1001) | `nft.hold` | partial: nft-stake-variants |
| [transferStakeNFT](https://bitbucket.org/decimalteam/dsc-js-sdk/src/6790d35e2decb0cbb06a9149a9c476c834f99223/src/decimalevm/index.ts#lines-1008) | `nft.transfer_stake` | partial: nft-stake-variants |
| [transferStakeNFTHold](https://bitbucket.org/decimalteam/dsc-js-sdk/src/6790d35e2decb0cbb06a9149a9c476c834f99223/src/decimalevm/index.ts#lines-1015) | `nft.transfer_stake` | partial: nft-stake-variants |
| [withdrawStakeNFT](https://bitbucket.org/decimalteam/dsc-js-sdk/src/6790d35e2decb0cbb06a9149a9c476c834f99223/src/decimalevm/index.ts#lines-1022) | `nft.withdraw` | partial: nft-stake-variants |
| [withdrawStakeNFTHold](https://bitbucket.org/decimalteam/dsc-js-sdk/src/6790d35e2decb0cbb06a9149a9c476c834f99223/src/decimalevm/index.ts#lines-1029) | `nft.withdraw` | partial: nft-stake-variants |
| [stakeNFTToHold](https://bitbucket.org/decimalteam/dsc-js-sdk/src/6790d35e2decb0cbb06a9149a9c476c834f99223/src/decimalevm/index.ts#lines-1036) | - | missing: no-typed-method |
| [stakeNFTResetHold](https://bitbucket.org/decimalteam/dsc-js-sdk/src/6790d35e2decb0cbb06a9149a9c476c834f99223/src/decimalevm/index.ts#lines-1043) | - | missing: no-typed-method |
| [withdrawNFTWithReset](https://bitbucket.org/decimalteam/dsc-js-sdk/src/6790d35e2decb0cbb06a9149a9c476c834f99223/src/decimalevm/index.ts#lines-1050) | - | missing: no-typed-method |
| [transferNFTWithReset](https://bitbucket.org/decimalteam/dsc-js-sdk/src/6790d35e2decb0cbb06a9149a9c476c834f99223/src/decimalevm/index.ts#lines-1057) | - | missing: no-typed-method |
| [holdNFTWithReset](https://bitbucket.org/decimalteam/dsc-js-sdk/src/6790d35e2decb0cbb06a9149a9c476c834f99223/src/decimalevm/index.ts#lines-1064) | - | missing: no-typed-method |
| [completeStakeNFT](https://bitbucket.org/decimalteam/dsc-js-sdk/src/6790d35e2decb0cbb06a9149a9c476c834f99223/src/decimalevm/index.ts#lines-1071) | - | missing: no-typed-method |
| [addValidatorWithToken](https://bitbucket.org/decimalteam/dsc-js-sdk/src/6790d35e2decb0cbb06a9149a9c476c834f99223/src/decimalevm/index.ts#lines-1076) | - | missing: no-typed-method |
| [addValidatorWithETH](https://bitbucket.org/decimalteam/dsc-js-sdk/src/6790d35e2decb0cbb06a9149a9c476c834f99223/src/decimalevm/index.ts#lines-1083) | - | missing: no-typed-method |
| [removeValidator](https://bitbucket.org/decimalteam/dsc-js-sdk/src/6790d35e2decb0cbb06a9149a9c476c834f99223/src/decimalevm/index.ts#lines-1090) | - | missing: no-typed-method |
| [pauseValidator](https://bitbucket.org/decimalteam/dsc-js-sdk/src/6790d35e2decb0cbb06a9149a9c476c834f99223/src/decimalevm/index.ts#lines-1095) | `decimal.pause_validator` | counterpart: network-abi-unverified |
| [unpauseValidator](https://bitbucket.org/decimalteam/dsc-js-sdk/src/6790d35e2decb0cbb06a9149a9c476c834f99223/src/decimalevm/index.ts#lines-1100) | `decimal.unpause_validator` | counterpart: network-abi-unverified |
| [updateValidatorMeta](https://bitbucket.org/decimalteam/dsc-js-sdk/src/6790d35e2decb0cbb06a9149a9c476c834f99223/src/decimalevm/index.ts#lines-1105) | - | missing: no-typed-method |
| [approveHashMultiSig](https://bitbucket.org/decimalteam/dsc-js-sdk/src/6790d35e2decb0cbb06a9149a9c476c834f99223/src/decimalevm/index.ts#lines-1404) | - | missing: no-typed-method |
| [executeMultiSigTx](https://bitbucket.org/decimalteam/dsc-js-sdk/src/6790d35e2decb0cbb06a9149a9c476c834f99223/src/decimalevm/index.ts#lines-1433) | - | missing: no-typed-method |
| [createMultiSig](https://bitbucket.org/decimalteam/dsc-js-sdk/src/6790d35e2decb0cbb06a9149a9c476c834f99223/src/decimalevm/index.ts#lines-1439) | - | missing: no-typed-method |
| [bridgeTransferNative](https://bitbucket.org/decimalteam/dsc-js-sdk/src/6790d35e2decb0cbb06a9149a9c476c834f99223/src/decimalevm/index.ts#lines-1812) | `bridge.transfer_native` | counterpart: network-abi-unverified |
| [bridgeTransferTokens](https://bitbucket.org/decimalteam/dsc-js-sdk/src/6790d35e2decb0cbb06a9149a9c476c834f99223/src/decimalevm/index.ts#lines-1824) | `bridge.transfer_token` | counterpart: network-abi-unverified |
| [bridgeCompleteTransfer](https://bitbucket.org/decimalteam/dsc-js-sdk/src/6790d35e2decb0cbb06a9149a9c476c834f99223/src/decimalevm/index.ts#lines-1836) | `bridge.complete_transfer` | counterpart: network-abi-unverified |
| [createChecksDEL](https://bitbucket.org/decimalteam/dsc-js-sdk/src/6790d35e2decb0cbb06a9149a9c476c834f99223/src/decimalevm/index.ts#lines-1869) | `checks.create_del` | counterpart: network-abi-unverified |
| [createChecksToken](https://bitbucket.org/decimalteam/dsc-js-sdk/src/6790d35e2decb0cbb06a9149a9c476c834f99223/src/decimalevm/index.ts#lines-1876) | `checks.create_token` | counterpart: network-abi-unverified |
| [redeemChecks](https://bitbucket.org/decimalteam/dsc-js-sdk/src/6790d35e2decb0cbb06a9149a9c476c834f99223/src/decimalevm/index.ts#lines-1883) | `checks.redeem` | counterpart: network-abi-unverified |

## dsc-go-sdk

| Method | Python counterpart | Status / reason |
| --- | --- | --- |
| [SendDEL](https://bitbucket.org/decimalteam/dsc-go-sdk/src/3ef4a089b6020889e60783c2026df5725fb960e2/decimalevm/methods/del.go#lines-27) | `tx.send_del` | counterpart: network-abi-unverified |
| [BurnDEL](https://bitbucket.org/decimalteam/dsc-go-sdk/src/3ef4a089b6020889e60783c2026df5725fb960e2/decimalevm/methods/del.go#lines-115) | - | missing: no-typed-method |
| [CreateToken](https://bitbucket.org/decimalteam/dsc-go-sdk/src/3ef4a089b6020889e60783c2026df5725fb960e2/decimalevm/methods/tokens.go#lines-31) | `token.create` | counterpart: network-abi-unverified |
| [ApproveToken](https://bitbucket.org/decimalteam/dsc-go-sdk/src/3ef4a089b6020889e60783c2026df5725fb960e2/decimalevm/methods/tokens.go#lines-157) | `tx.approve_erc20` | counterpart: network-abi-unverified |
| [TransferToken](https://bitbucket.org/decimalteam/dsc-go-sdk/src/3ef4a089b6020889e60783c2026df5725fb960e2/decimalevm/methods/tokens.go#lines-255) | `tx.send_erc20` | counterpart: network-abi-unverified |
| [TransferFromToken](https://bitbucket.org/decimalteam/dsc-go-sdk/src/3ef4a089b6020889e60783c2026df5725fb960e2/decimalevm/methods/tokens.go#lines-354) | `tx.transfer_from_erc20` | counterpart: network-abi-unverified |
| [BurnToken](https://bitbucket.org/decimalteam/dsc-go-sdk/src/3ef4a089b6020889e60783c2026df5725fb960e2/decimalevm/methods/tokens.go#lines-452) | `token.burn` | counterpart: network-abi-unverified |
| [BuyTokenForExactDEL](https://bitbucket.org/decimalteam/dsc-go-sdk/src/3ef4a089b6020889e60783c2026df5725fb960e2/decimalevm/methods/tokens.go#lines-549) | `token.buy` | partial: token-selector |
| [BuyExactTokenForDEL](https://bitbucket.org/decimalteam/dsc-go-sdk/src/3ef4a089b6020889e60783c2026df5725fb960e2/decimalevm/methods/tokens.go#lines-658) | - | missing: no-typed-method |
| [SellTokensForExactDEL](https://bitbucket.org/decimalteam/dsc-go-sdk/src/3ef4a089b6020889e60783c2026df5725fb960e2/decimalevm/methods/tokens.go#lines-769) | - | missing: no-typed-method |
| [SellExactTokensForDEL](https://bitbucket.org/decimalteam/dsc-go-sdk/src/3ef4a089b6020889e60783c2026df5725fb960e2/decimalevm/methods/tokens.go#lines-880) | `token.sell` | partial: token-selector |
| [ConvertToken](https://bitbucket.org/decimalteam/dsc-go-sdk/src/3ef4a089b6020889e60783c2026df5725fb960e2/decimalevm/methods/tokens.go#lines-992) | `token.convert` | counterpart: network-abi-unverified |
| [PermitToken](https://bitbucket.org/decimalteam/dsc-go-sdk/src/3ef4a089b6020889e60783c2026df5725fb960e2/decimalevm/methods/tokens.go#lines-1185) | `erc20.sign_permit` | partial: signature-only |
| [DelegateDel](https://bitbucket.org/decimalteam/dsc-go-sdk/src/3ef4a089b6020889e60783c2026df5725fb960e2/decimalevm/methods/delegation.go#lines-15) | `decimal.delegate_del` | counterpart: network-abi-unverified |
| [DelegateDELHold](https://bitbucket.org/decimalteam/dsc-go-sdk/src/3ef4a089b6020889e60783c2026df5725fb960e2/decimalevm/methods/delegation.go#lines-79) | `decimal.hold_del` | counterpart: network-abi-unverified |
| [DelegateToken](https://bitbucket.org/decimalteam/dsc-go-sdk/src/3ef4a089b6020889e60783c2026df5725fb960e2/decimalevm/methods/delegation.go#lines-144) | `decimal.delegate_erc20` | counterpart: network-abi-unverified |
| [DelegateTokenHold](https://bitbucket.org/decimalteam/dsc-go-sdk/src/3ef4a089b6020889e60783c2026df5725fb960e2/decimalevm/methods/delegation.go#lines-236) | `decimal.hold_erc20` | counterpart: network-abi-unverified |
| [WithdrawStakeToken](https://bitbucket.org/decimalteam/dsc-go-sdk/src/3ef4a089b6020889e60783c2026df5725fb960e2/decimalevm/methods/delegation.go#lines-330) | `decimal.unbond_del`, `decimal.unbond_erc20` | counterpart: network-abi-unverified |
| [WithdrawStakeTokenHold](https://bitbucket.org/decimalteam/dsc-go-sdk/src/3ef4a089b6020889e60783c2026df5725fb960e2/decimalevm/methods/delegation.go#lines-392) | `decimal.withdraw_hold_del`, `decimal.withdraw_hold_erc20` | counterpart: network-abi-unverified |
| [DelegateDRC721](https://bitbucket.org/decimalteam/dsc-go-sdk/src/3ef4a089b6020889e60783c2026df5725fb960e2/decimalevm/methods/delegation.go#lines-455) | `nft.delegate` | partial: nft-stake-variants |
| [DelegateDRC721Hold](https://bitbucket.org/decimalteam/dsc-go-sdk/src/3ef4a089b6020889e60783c2026df5725fb960e2/decimalevm/methods/delegation.go#lines-558) | `nft.hold` | partial: nft-stake-variants |
| [DelegateDRC1155](https://bitbucket.org/decimalteam/dsc-go-sdk/src/3ef4a089b6020889e60783c2026df5725fb960e2/decimalevm/methods/delegation.go#lines-664) | `nft.delegate` | partial: nft-stake-variants |
| [DelegateDRC1155Hold](https://bitbucket.org/decimalteam/dsc-go-sdk/src/3ef4a089b6020889e60783c2026df5725fb960e2/decimalevm/methods/delegation.go#lines-769) | `nft.hold` | partial: nft-stake-variants |
| [WithdrawStakeNFT](https://bitbucket.org/decimalteam/dsc-go-sdk/src/3ef4a089b6020889e60783c2026df5725fb960e2/decimalevm/methods/delegation.go#lines-877) | `nft.withdraw` | partial: nft-stake-variants |
| [WithdrawStakeNFTHold](https://bitbucket.org/decimalteam/dsc-go-sdk/src/3ef4a089b6020889e60783c2026df5725fb960e2/decimalevm/methods/delegation.go#lines-954) | `nft.withdraw` | partial: nft-stake-variants |
| [CreateNftCollection](https://bitbucket.org/decimalteam/dsc-go-sdk/src/3ef4a089b6020889e60783c2026df5725fb960e2/decimalevm/methods/nft.go#lines-22) | `nft.create_collection` | partial: nft-collection-selector |
| [SetApprovalForAllNFT](https://bitbucket.org/decimalteam/dsc-go-sdk/src/3ef4a089b6020889e60783c2026df5725fb960e2/decimalevm/methods/nft.go#lines-111) | `nft.set_approval_for_all` | counterpart: network-abi-unverified |
| [MintNFT](https://bitbucket.org/decimalteam/dsc-go-sdk/src/3ef4a089b6020889e60783c2026df5725fb960e2/decimalevm/methods/nft.go#lines-173) | `nft.mint` | partial: nft-standard-mint |
| [TransferNFT](https://bitbucket.org/decimalteam/dsc-go-sdk/src/3ef4a089b6020889e60783c2026df5725fb960e2/decimalevm/methods/nft.go#lines-247) | `nft.transfer` | counterpart: network-abi-unverified |
| [DisableMintNFT](https://bitbucket.org/decimalteam/dsc-go-sdk/src/3ef4a089b6020889e60783c2026df5725fb960e2/decimalevm/methods/nft.go#lines-327) | `nft.disable_mint` | counterpart: network-abi-unverified |
| [BurnNFT](https://bitbucket.org/decimalteam/dsc-go-sdk/src/3ef4a089b6020889e60783c2026df5725fb960e2/decimalevm/methods/nft.go#lines-389) | `nft.burn` | counterpart: network-abi-unverified |
| [SetTokenURINFT](https://bitbucket.org/decimalteam/dsc-go-sdk/src/3ef4a089b6020889e60783c2026df5725fb960e2/decimalevm/methods/nft.go#lines-465) | `nft.set_token_uri` | counterpart: network-abi-unverified |
| [MintNFTWithDELReserve](https://bitbucket.org/decimalteam/dsc-go-sdk/src/3ef4a089b6020889e60783c2026df5725fb960e2/decimalevm/methods/nft.go#lines-527) | `nft.mint` | partial: nft-del-selector |
| [MintReserveless](https://bitbucket.org/decimalteam/dsc-go-sdk/src/3ef4a089b6020889e60783c2026df5725fb960e2/decimalevm/methods/nft.go#lines-624) | `nft.mint` | counterpart: network-abi-unverified |
| [AddDELReserveNFT](https://bitbucket.org/decimalteam/dsc-go-sdk/src/3ef4a089b6020889e60783c2026df5725fb960e2/decimalevm/methods/nft.go#lines-724) | `nft.add_del_reserve` | counterpart: network-abi-unverified |
| [AddTokenReserveNFT](https://bitbucket.org/decimalteam/dsc-go-sdk/src/3ef4a089b6020889e60783c2026df5725fb960e2/decimalevm/methods/nft.go#lines-786) | - | missing: no-typed-method |
| [TransferBatchNFT1155](https://bitbucket.org/decimalteam/dsc-go-sdk/src/3ef4a089b6020889e60783c2026df5725fb960e2/decimalevm/methods/nft.go#lines-874) | `nft.transfer_batch_erc1155` | counterpart: network-abi-unverified |
| [TransferStakeNFT](https://bitbucket.org/decimalteam/dsc-go-sdk/src/3ef4a089b6020889e60783c2026df5725fb960e2/decimalevm/methods/nft.go#lines-940) | `nft.transfer_stake` | partial: nft-stake-variants |
| [TransferStakeNFTHold](https://bitbucket.org/decimalteam/dsc-go-sdk/src/3ef4a089b6020889e60783c2026df5725fb960e2/decimalevm/methods/nft.go#lines-1019) | `nft.transfer_stake` | partial: nft-stake-variants |
| [StakeNFTToHold](https://bitbucket.org/decimalteam/dsc-go-sdk/src/3ef4a089b6020889e60783c2026df5725fb960e2/decimalevm/methods/nft.go#lines-1100) | - | missing: no-typed-method |
| [StakeNFTResetHold](https://bitbucket.org/decimalteam/dsc-go-sdk/src/3ef4a089b6020889e60783c2026df5725fb960e2/decimalevm/methods/nft.go#lines-1181) | - | missing: no-typed-method |
| [WithdrawNFTWithReset](https://bitbucket.org/decimalteam/dsc-go-sdk/src/3ef4a089b6020889e60783c2026df5725fb960e2/decimalevm/methods/nft.go#lines-1260) | - | missing: no-typed-method |
| [TransferNFTWithReset](https://bitbucket.org/decimalteam/dsc-go-sdk/src/3ef4a089b6020889e60783c2026df5725fb960e2/decimalevm/methods/nft.go#lines-1339) | - | missing: no-typed-method |
| [HoldNFTWithReset](https://bitbucket.org/decimalteam/dsc-go-sdk/src/3ef4a089b6020889e60783c2026df5725fb960e2/decimalevm/methods/nft.go#lines-1420) | - | missing: no-typed-method |
| [CompleteStakeNFT](https://bitbucket.org/decimalteam/dsc-go-sdk/src/3ef4a089b6020889e60783c2026df5725fb960e2/decimalevm/methods/nft.go#lines-1501) | - | missing: no-typed-method |
| [AddValidatorWithToken](https://bitbucket.org/decimalteam/dsc-go-sdk/src/3ef4a089b6020889e60783c2026df5725fb960e2/decimalevm/methods/validators.go#lines-17) | - | missing: no-typed-method |
| [AddValidatorWithETH](https://bitbucket.org/decimalteam/dsc-go-sdk/src/3ef4a089b6020889e60783c2026df5725fb960e2/decimalevm/methods/validators.go#lines-110) | - | missing: no-typed-method |
| [RemoveValidator](https://bitbucket.org/decimalteam/dsc-go-sdk/src/3ef4a089b6020889e60783c2026df5725fb960e2/decimalevm/methods/validators.go#lines-203) | - | missing: no-typed-method |
| [PauseValidator](https://bitbucket.org/decimalteam/dsc-go-sdk/src/3ef4a089b6020889e60783c2026df5725fb960e2/decimalevm/methods/validators.go#lines-288) | `decimal.pause_validator` | counterpart: network-abi-unverified |
| [UnpauseValidator](https://bitbucket.org/decimalteam/dsc-go-sdk/src/3ef4a089b6020889e60783c2026df5725fb960e2/decimalevm/methods/validators.go#lines-373) | `decimal.unpause_validator` | counterpart: network-abi-unverified |
| [UpdateValidatorMeta](https://bitbucket.org/decimalteam/dsc-go-sdk/src/3ef4a089b6020889e60783c2026df5725fb960e2/decimalevm/methods/validators.go#lines-458) | - | missing: no-typed-method |
| [CreateMultiSig](https://bitbucket.org/decimalteam/dsc-go-sdk/src/3ef4a089b6020889e60783c2026df5725fb960e2/decimalevm/methods/multisig.go#lines-18) | - | missing: no-typed-method |
| [ExecuteSafeTransaction](https://bitbucket.org/decimalteam/dsc-go-sdk/src/3ef4a089b6020889e60783c2026df5725fb960e2/decimalevm/methods/multisig.go#lines-440) | - | missing: no-typed-method |

## Reproduce

```shell
python -m pip install "tree-sitter==0.25.2" "tree-sitter-typescript==0.23.2" "tree-sitter-go==0.25.0"
python scripts/compare_upstream.py --fetch
```

Pinned source URLs and SHA256 hashes are stored in the JSON report. Upstream code is parsed, never executed.
