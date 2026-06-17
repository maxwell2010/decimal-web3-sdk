# dsc-js-sdk Transaction Parity

Дата: 2026-06-16

Reference: https://bitbucket.org/decimalteam/dsc-js-sdk/src/master/

Scanned revisions:

- `dsc-js-sdk`: `6790d35`
- `dsc-go-sdk`: `3ef4a08`

## Scope

Официальный `dsc-js-sdk` содержит два разных слоя:

- legacy Cosmos/protobuf transaction layer: `src/transaction.ts`, `src/txTypes.ts`, `src/txTypesNew.ts`;
- Decimal EVM contract layer: `src/decimalevm/call.ts`, `src/decimalevm/index.ts`, `src/contract/*`.

Наш `decimal-web3-sdk` сейчас является EVM/Web3 SDK. Поэтому parity считается по EVM layer, а legacy Cosmos операции фиксируются отдельно как compatibility backlog.

## EVM Transaction Parity

| dsc-js-sdk operation group | JS methods | Python SDK status | Python API |
|---|---|---|---|
| Native DEL transfer | generic EVM tx, multisig send DEL builders | Supported | `NativeTransferRequest`, `client.tx.send_del()` |
| Generic contract call | `DecimalContractEVM.populateTransaction/signTransaction/sendTransaction` | Supported | `ContractCallRequest`, `client.tx.build_contract_call()`, `send_draft()` |
| ERC20 transfer | `transferToken` | Supported | `Erc20TransferRequest`, `client.tx.send_erc20()` |
| ERC20 transferFrom | `transferFromToken` | Supported | `Erc20TransferFromRequest`, `client.tx.transfer_from_erc20()` |
| ERC20 approve | `approveToken` | Supported | `Erc20ApproveRequest`, `client.tx.approve_erc20()` |
| ERC20 permit | `permitToken`, `getSignPermitToken` | Supported as helper | `client.erc20.permit_signature()`, `build_permit_data()` |
| Token create | `createToken` | Supported | `CreateTokenRequest`, `client.token.create()` |
| Token create reserveless | `createTokenReserveless` | Supported | `CreateReservelessTokenRequest`, `client.token.create_reserveless()` |
| Token mint | `mintTokenReserveless` | Supported | `MintTokenRequest`, `client.token.mint()` |
| Token burn | `burnToken` | Supported | `BurnTokenRequest`, `client.token.burn()` |
| Token buy | `buyTokenForExactDEL`, `buyExactTokenForDEL` | Partially supported | `BuyTokenRequest`, current API covers buy with DEL value and `amountOutMin` |
| Token sell | `sellTokensForExactDEL`, `sellExactTokensForDEL` | Partially supported | `SellTokenRequest`, current API covers sell exact token amount with `min_amount_del_out_wei` |
| Token convert | `convertToken` | Supported | `ConvertTokenRequest`, `client.token.convert()` |
| Token update identity/max/min supply | `updateTokenIdentity`, `updateTokenMaxTotalSupply`, `updateTokenMinTotalSupply` | Partial | `UpdateTokenDetailsRequest` currently covers identity + max total supply shape |
| Token read/calculation helpers | `calculateBuyOutput/Input`, `calculateSellInput/Output`, `allowanceToken`, `balanceOfToken` | Partial | ERC20 reads supported; bonding/reserve calculators are backlog |
| DEL delegate | `delegateDEL` | Supported | `DelegateDelRequest`, `client.decimal.delegate_del()` |
| DEL hold delegate | `delegateDELHold` | Supported | `HoldDelRequest`, `client.decimal.hold_del()` |
| ERC20 delegate | `delegateToken` | Supported | `DelegateErc20Request`, `client.decimal.delegate_erc20()` |
| ERC20 hold delegate | `delegateTokenHold` | Supported | `HoldErc20Request`, `client.decimal.hold_erc20()` |
| ERC20 withdraw/unbond | `withdrawStakeToken` | Supported | `UnbondErc20Request`, `client.decimal.unbond_erc20()` |
| ERC20 withdraw hold | `withdrawStakeTokenHold` | Supported | `WithdrawHoldErc20Request`, `client.decimal.withdraw_hold_erc20()` |
| Stake transfer/redelegate | `transferStakeToken`, `transferStakeTokenHold` | Supported | `TransferStakeErc20Request`, `client.decimal.transfer_stake_erc20()` |
| Stake hold/reset helpers | `stakeTokenToHold`, `stakeTokenResetHold*`, `withdraw/transfer/hold*WithReset` | Supported | `StakeTokenToHoldRequest`, `ResetStakeHoldRequest`, with-reset request classes |
| Stake complete/penalty | `completeStakeToken`, penalties | Backlog | Low-level validator/operator workflows |
| DEL/Token multisend | `multicall`, multisig builders | Supported for direct multisend | `MultisendDelRequest`, `MultisendErc20Request` |
| NFT create collection | `createCollection` | Supported | `CreateNftCollectionRequest`, `client.nft.create_collection()` |
| NFT mint | `mintNFT`, `mintNFTWithDELReserve`, `mintNFTWithTokenReserve`, `mintReserveless` | Partial | `MintNftRequest`, base mint supported; reserve variants need parity expansion |
| NFT disable mint | `disableMintNFT` | Supported | `DisableMintNftRequest`, `client.nft.disable_mint()` |
| NFT transfer | `transferNFT`, `transferBatchNFT1155` | Supported | `NftTransferRequest`, `NftBatchTransferRequest` |
| NFT token URI | `setTokenURINFT` | Supported | `SetTokenUriNftRequest`, `client.nft.set_token_uri()` |
| NFT DEL reserve | `addDELReserveNFT` | Supported | `AddDelReserveNftRequest`, `client.nft.add_del_reserve()` |
| NFT burn | `burnNFT` | Supported | `BurnNftRequest`, `client.nft.burn()` |
| NFT approval | `setApprovalForAllNFT`, `approveNFT721` | Supported | `NftApprovalRequest`, `NftApproveRequest` |
| NFT delegate/hold | `delegateNFT`, `delegateDRC721/1155`, hold variants | Supported | `DelegateNftRequest`, `HoldNftRequest` |
| NFT withdraw | `withdrawNFT`, `withdrawStakeNFT` | Supported | `WithdrawNftRequest` |
| NFT stake transfer | `transferNFTStake`, `transferStakeNFT` | Supported | `TransferNftStakeRequest` |
| NFT hold reset/complete | `stakeNFTToHold`, `stakeNFTResetHold`, `completeStakeNFT` | Backlog | Advanced stake lifecycle |
| Validator management | `addValidatorWithToken/ETH`, `removeValidator`, `pause/unpause`, `updateValidatorMeta` | Backlog | Operator/admin workflows |
| Bridge | `bridgeTransferNative`, `bridgeTransferTokens`, `bridgeCompleteTransfer` | Supported with explicit contract | `BridgeTransferNativeRequest`, `BridgeTransferTokenRequest`, `BridgeCompleteTransferRequest` |
| Checks | `createChecksDEL`, `createChecksToken`, `redeemChecks` | Supported with explicit contract | `CreateChecksDelRequest`, `CreateChecksTokenRequest`, `RedeemChecksRequest` |
| Multisig Safe | `createMultiSig`, `buildMultiSigTx*`, `signMultiSigTx`, `executeMultiSigTx` | Backlog | Safe-style multisig parity |
| Contract verification/IPFS | `verifyContract`, IPFS upload helpers | Backlog | Tooling, not core transaction sending |

## Legacy Cosmos Compatibility Backlog

These JS SDK methods create legacy/protobuf Decimal transactions. They are not covered by the current EVM-first release:

- coin: `sendCoin`, `burnCoins`, `updateCoin`, `createCoin`, `multiSendCoin`, `buyCoins`, `sellCoins`, `sellAllCoins`;
- checks: `issueCheck`, `redeemCheck`;
- multisig: `createWallet`, `multisigCreateTx`, `multisigSignTx`;
- legacy NFT: `mintNft`, `transferNft`, `burnNft`, `nftUpdateReserve`, `nftEditMetadata`;
- swap: `msgSwapInit`, `msgSwapRedeem`;
- validator: `delegate`, `unbond`, `cancelUnbonding`, `redelegate`, `cancelRedelegation`, `createValidator`, `editValidator`, `setOnline`, `setOffline`;
- NFT staking legacy: `delegateNft`, `unbondNft`, `redelegateNft`, cancel variants;
- governance/admin: proposal/software/fee update transaction types;
- `returnLegacy`;
- EIP712 data builders for legacy send/delegate/unbond/redelegate.

## Immediate Parity Gaps To Close Next

1. Token reserve calculators and exact-in/exact-out naming parity.
2. NFT token reserve helpers and base URI helpers.
3. Stake complete/penalty operator workflows.
4. Validator operator workflows.
5. Safe-style multisig helpers.
6. Optional legacy Cosmos/protobuf compatibility package, if we decide to support pre-EVM tx formats.
