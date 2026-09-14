# Сравнение С Официальными SDK

[JSON](../upstream-parity.json) | [Status](status.md)

Срез исходников на 14.09.2026. Считаются именованные высокоуровневые EVM-методы отправки, а не уникальные типы протокола и не количество транзакций в блоке. Один workflow может отправить approve и основную транзакцию. Один Python-метод иногда объединяет несколько JS-методов параметрами; поэтому проценты покрытия из этих чисел считать нельзя.

| SDK | Commit / version |
| --- | --- |
| dsc-js-sdk | [6790d35e2dec](https://bitbucket.org/decimalteam/dsc-js-sdk/src/6790d35e2decb0cbb06a9149a9c476c834f99223/) |
| dsc-go-sdk | [3ef4a089b602](https://bitbucket.org/decimalteam/dsc-go-sdk/src/3ef4a089b6020889e60783c2026df5725fb960e2/) |
| Python (unreleased) | 0.1.2.dev0 |

[Development notes](transaction-parity-development.md)

| Group | JS | Go | Python |
| --- | ---: | ---: | ---: |
| del | 2 | 2 | 2 |
| multisend | 1 | 0 | 2 |
| tokens | 17 | 11 | 15 |
| staking | 17 | 6 | 20 |
| nft | 16 | 12 | 12 |
| nft_staking | 27 | 14 | 11 |
| validators | 6 | 6 | 8 |
| checks | 3 | 0 | 3 |
| bridge | 3 | 0 | 3 |
| multisig | 3 | 2 | 3 |
| **Total** | **95** | **53** | **79** |

JS: 92 специализированных публичных метода + 3 операции multisig (create, approveHash, executeTx). Отдельно: 1 generic multiCall, 23 Safe-builder и 1 локальная подпись. Go: 58 экспортированных функций в methods, из них 53 отправки и 5 builder/sign-helper. Python: 79 методов из каталога; generic contract executors, оценки комиссий и чтение исключены. Дополнительно учтен пакетный сброс NFT-hold из feature-ветки; база JS в этой таблице остается закрепленным master.

JS также содержит 42 идентификатора legacy-каталога txTypesNew.ts, включая локальное создание чека и EVM-envelope. Это не 42 дополнительных подтвержденных EVM-операции; в таблицу они не входят. Закомментированный JS mintNFT и диагностический redeemChecksTest не считаются. В Go проверен пакет decimalevm/methods, не код ноды или Swagger-обертки.

## Ограничения Сопоставления

counterpart = есть типизированный аналог по назначению, но работоспособность текущего ABI в сети не доказана. partial = аналог неполный или отличается ABI/маршрут. missing = отдельного типизированного аналога нет. Общий вызов контракта не засчитывается как реализация типа транзакции.

- token-selector: Python buy/sell против JS buyTokenForExactDEL/sellExactTokensForDEL.
- token-update-selector: Python updateDetails против отдельных updateTokenIdentity/updateMaxTotalSupply.
- token-mint-selector: порядок/сигнатура mint требуют отдельной сверки.
- nft-del-selector: Python mintByETH против mintByDEL upstream; нужен ABI-аудит.
- nft-collection-selector/nft-stake-variants/nft-standard-mint: типы коллекций и маршруты старой Delegation/DelegationNFT различаются.
- mixed-assets: Python разделяет DEL и один ERC20; JS допускает разные активы одним multisend.
- signature-only: Python sign_permit создает подпись, не отправляет standalone permit; это не аналог отправки PermitToken.
- nft-permit-missing: mint с токен-резервом есть, полный permit-маршрут отсутствует.

## Приоритетные Пробелы

Добавленные методы проверены offline, но еще не сетевыми отправками. Остаются прежние частичные соответствия ABI, permit-варианты и смешанная рассылка. Три legacy-метода требуют явного opt-in; их нет в проверенных актуальных ABI. У безрезервных NFT текущий ABI использует refundable вместо JS allowMint.

## dsc-js-sdk

| Method | Python counterpart | Status / reason |
| --- | --- | --- |
| [multiSendToken](https://bitbucket.org/decimalteam/dsc-js-sdk/src/6790d35e2decb0cbb06a9149a9c476c834f99223/src/decimalevm/index.ts#lines-405) | `decimal.multisend_del`, `decimal.multisend_erc20` | partial: mixed-assets |
| [sendDEL](https://bitbucket.org/decimalteam/dsc-js-sdk/src/6790d35e2decb0cbb06a9149a9c476c834f99223/src/decimalevm/index.ts#lines-460) | `tx.send_del` | counterpart: network-abi-unverified |
| [burnDEL](https://bitbucket.org/decimalteam/dsc-js-sdk/src/6790d35e2decb0cbb06a9149a9c476c834f99223/src/decimalevm/index.ts#lines-473) | `tx.burn_del` | counterpart: network-abi-unverified |
| [createToken](https://bitbucket.org/decimalteam/dsc-js-sdk/src/6790d35e2decb0cbb06a9149a9c476c834f99223/src/decimalevm/index.ts#lines-477) | `token.create` | counterpart: network-abi-unverified |
| [createTokenReserveless](https://bitbucket.org/decimalteam/dsc-js-sdk/src/6790d35e2decb0cbb06a9149a9c476c834f99223/src/decimalevm/index.ts#lines-482) | `token.create_reserveless` | counterpart: network-abi-unverified |
| [convertToken](https://bitbucket.org/decimalteam/dsc-js-sdk/src/6790d35e2decb0cbb06a9149a9c476c834f99223/src/decimalevm/index.ts#lines-506) | `token.convert` | counterpart: network-abi-unverified |
| [approveToken](https://bitbucket.org/decimalteam/dsc-js-sdk/src/6790d35e2decb0cbb06a9149a9c476c834f99223/src/decimalevm/index.ts#lines-511) | `tx.approve_erc20` | counterpart: network-abi-unverified |
| [transferToken](https://bitbucket.org/decimalteam/dsc-js-sdk/src/6790d35e2decb0cbb06a9149a9c476c834f99223/src/decimalevm/index.ts#lines-517) | `tx.send_erc20` | counterpart: network-abi-unverified |
| [transferFromToken](https://bitbucket.org/decimalteam/dsc-js-sdk/src/6790d35e2decb0cbb06a9149a9c476c834f99223/src/decimalevm/index.ts#lines-523) | `tx.transfer_from_erc20` | counterpart: network-abi-unverified |
| [burnToken](https://bitbucket.org/decimalteam/dsc-js-sdk/src/6790d35e2decb0cbb06a9149a9c476c834f99223/src/decimalevm/index.ts#lines-529) | `token.burn` | counterpart: network-abi-unverified |
| [mintTokenReserveless](https://bitbucket.org/decimalteam/dsc-js-sdk/src/6790d35e2decb0cbb06a9149a9c476c834f99223/src/decimalevm/index.ts#lines-535) | `token.mint` | partial: token-mint-selector |
| [convertToDEL](https://bitbucket.org/decimalteam/dsc-js-sdk/src/6790d35e2decb0cbb06a9149a9c476c834f99223/src/decimalevm/index.ts#lines-541) | `token.convert_to_del` | counterpart: network-abi-unverified |
| [buyTokenForExactDEL](https://bitbucket.org/decimalteam/dsc-js-sdk/src/6790d35e2decb0cbb06a9149a9c476c834f99223/src/decimalevm/index.ts#lines-547) | `token.buy` | partial: token-selector |
| [buyExactTokenForDEL](https://bitbucket.org/decimalteam/dsc-js-sdk/src/6790d35e2decb0cbb06a9149a9c476c834f99223/src/decimalevm/index.ts#lines-553) | `token.buy_exact` | counterpart: network-abi-unverified |
| [sellTokensForExactDEL](https://bitbucket.org/decimalteam/dsc-js-sdk/src/6790d35e2decb0cbb06a9149a9c476c834f99223/src/decimalevm/index.ts#lines-559) | `token.sell_for_exact_del` | counterpart: network-abi-unverified |
| [sellExactTokensForDEL](https://bitbucket.org/decimalteam/dsc-js-sdk/src/6790d35e2decb0cbb06a9149a9c476c834f99223/src/decimalevm/index.ts#lines-565) | `token.sell` | partial: token-selector |
| [updateTokenIdentity](https://bitbucket.org/decimalteam/dsc-js-sdk/src/6790d35e2decb0cbb06a9149a9c476c834f99223/src/decimalevm/index.ts#lines-571) | `token.update_details` | partial: token-update-selector |
| [updateTokenMaxTotalSupply](https://bitbucket.org/decimalteam/dsc-js-sdk/src/6790d35e2decb0cbb06a9149a9c476c834f99223/src/decimalevm/index.ts#lines-577) | `token.update_details` | partial: token-update-selector |
| [updateTokenMinTotalSupply](https://bitbucket.org/decimalteam/dsc-js-sdk/src/6790d35e2decb0cbb06a9149a9c476c834f99223/src/decimalevm/index.ts#lines-583) | `token.update_min_supply` | partial: legacy-explicit-opt-in |
| [permitToken](https://bitbucket.org/decimalteam/dsc-js-sdk/src/6790d35e2decb0cbb06a9149a9c476c834f99223/src/decimalevm/index.ts#lines-589) | `erc20.sign_permit` | partial: signature-only |
| [createCollectionDRC721](https://bitbucket.org/decimalteam/dsc-js-sdk/src/6790d35e2decb0cbb06a9149a9c476c834f99223/src/decimalevm/index.ts#lines-595) | `nft.create_collection` | partial: nft-collection-selector |
| [createCollectionDRC1155](https://bitbucket.org/decimalteam/dsc-js-sdk/src/6790d35e2decb0cbb06a9149a9c476c834f99223/src/decimalevm/index.ts#lines-600) | `nft.create_collection` | partial: nft-collection-selector |
| [createCollectionDRC721Reserveless](https://bitbucket.org/decimalteam/dsc-js-sdk/src/6790d35e2decb0cbb06a9149a9c476c834f99223/src/decimalevm/index.ts#lines-605) | `nft.create_reserveless_collection` | partial: current-nft-metadata |
| [createCollectionDRC1155Reserveless](https://bitbucket.org/decimalteam/dsc-js-sdk/src/6790d35e2decb0cbb06a9149a9c476c834f99223/src/decimalevm/index.ts#lines-610) | `nft.create_reserveless_collection` | partial: current-nft-metadata |
| [approveNFT721](https://bitbucket.org/decimalteam/dsc-js-sdk/src/6790d35e2decb0cbb06a9149a9c476c834f99223/src/decimalevm/index.ts#lines-615) | `nft.approve` | counterpart: network-abi-unverified |
| [approveForAllNFT](https://bitbucket.org/decimalteam/dsc-js-sdk/src/6790d35e2decb0cbb06a9149a9c476c834f99223/src/decimalevm/index.ts#lines-623) | `nft.set_approval_for_all` | counterpart: network-abi-unverified |
| [mintReserveless](https://bitbucket.org/decimalteam/dsc-js-sdk/src/6790d35e2decb0cbb06a9149a9c476c834f99223/src/decimalevm/index.ts#lines-647) | `nft.mint` | counterpart: network-abi-unverified |
| [mintNFTWithDELReserve](https://bitbucket.org/decimalteam/dsc-js-sdk/src/6790d35e2decb0cbb06a9149a9c476c834f99223/src/decimalevm/index.ts#lines-661) | `nft.mint` | partial: nft-del-selector |
| [mintNFTWithTokenReserve](https://bitbucket.org/decimalteam/dsc-js-sdk/src/6790d35e2decb0cbb06a9149a9c476c834f99223/src/decimalevm/index.ts#lines-678) | `nft.mint` | partial: nft-permit-missing |
| [addDELReserveNFT](https://bitbucket.org/decimalteam/dsc-js-sdk/src/6790d35e2decb0cbb06a9149a9c476c834f99223/src/decimalevm/index.ts#lines-695) | `nft.add_del_reserve` | counterpart: network-abi-unverified |
| [addTokenReserveNFT](https://bitbucket.org/decimalteam/dsc-js-sdk/src/6790d35e2decb0cbb06a9149a9c476c834f99223/src/decimalevm/index.ts#lines-711) | `nft.add_token_reserve` | counterpart: network-abi-unverified |
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
| [applyPenaltyToStakeToken](https://bitbucket.org/decimalteam/dsc-js-sdk/src/6790d35e2decb0cbb06a9149a9c476c834f99223/src/decimalevm/index.ts#lines-859) | `decimal.apply_stake_penalty` | partial: legacy-explicit-opt-in |
| [applyPenaltiesToStakeToken](https://bitbucket.org/decimalteam/dsc-js-sdk/src/6790d35e2decb0cbb06a9149a9c476c834f99223/src/decimalevm/index.ts#lines-864) | `decimal.apply_stake_penalties` | partial: legacy-explicit-opt-in |
| [completeStakeToken](https://bitbucket.org/decimalteam/dsc-js-sdk/src/6790d35e2decb0cbb06a9149a9c476c834f99223/src/decimalevm/index.ts#lines-868) | `decimal.complete_stake` | counterpart: network-abi-unverified |
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
| [stakeNFTToHold](https://bitbucket.org/decimalteam/dsc-js-sdk/src/6790d35e2decb0cbb06a9149a9c476c834f99223/src/decimalevm/index.ts#lines-1036) | `nft.stake_to_hold` | counterpart: network-abi-unverified |
| [stakeNFTResetHold](https://bitbucket.org/decimalteam/dsc-js-sdk/src/6790d35e2decb0cbb06a9149a9c476c834f99223/src/decimalevm/index.ts#lines-1043) | `nft.reset_stake_hold` | counterpart: network-abi-unverified |
| [withdrawNFTWithReset](https://bitbucket.org/decimalteam/dsc-js-sdk/src/6790d35e2decb0cbb06a9149a9c476c834f99223/src/decimalevm/index.ts#lines-1050) | `nft.withdraw_with_reset` | counterpart: network-abi-unverified |
| [transferNFTWithReset](https://bitbucket.org/decimalteam/dsc-js-sdk/src/6790d35e2decb0cbb06a9149a9c476c834f99223/src/decimalevm/index.ts#lines-1057) | `nft.transfer_with_reset` | counterpart: network-abi-unverified |
| [holdNFTWithReset](https://bitbucket.org/decimalteam/dsc-js-sdk/src/6790d35e2decb0cbb06a9149a9c476c834f99223/src/decimalevm/index.ts#lines-1064) | `nft.hold_with_reset` | counterpart: network-abi-unverified |
| [completeStakeNFT](https://bitbucket.org/decimalteam/dsc-js-sdk/src/6790d35e2decb0cbb06a9149a9c476c834f99223/src/decimalevm/index.ts#lines-1071) | `nft.complete_stake` | counterpart: network-abi-unverified |
| [addValidatorWithToken](https://bitbucket.org/decimalteam/dsc-js-sdk/src/6790d35e2decb0cbb06a9149a9c476c834f99223/src/decimalevm/index.ts#lines-1076) | `decimal.add_validator_token` | counterpart: network-abi-unverified |
| [addValidatorWithETH](https://bitbucket.org/decimalteam/dsc-js-sdk/src/6790d35e2decb0cbb06a9149a9c476c834f99223/src/decimalevm/index.ts#lines-1083) | `decimal.add_validator_del` | counterpart: network-abi-unverified |
| [removeValidator](https://bitbucket.org/decimalteam/dsc-js-sdk/src/6790d35e2decb0cbb06a9149a9c476c834f99223/src/decimalevm/index.ts#lines-1090) | `decimal.remove_validator` | counterpart: network-abi-unverified |
| [pauseValidator](https://bitbucket.org/decimalteam/dsc-js-sdk/src/6790d35e2decb0cbb06a9149a9c476c834f99223/src/decimalevm/index.ts#lines-1095) | `decimal.pause_validator` | counterpart: network-abi-unverified |
| [unpauseValidator](https://bitbucket.org/decimalteam/dsc-js-sdk/src/6790d35e2decb0cbb06a9149a9c476c834f99223/src/decimalevm/index.ts#lines-1100) | `decimal.unpause_validator` | counterpart: network-abi-unverified |
| [updateValidatorMeta](https://bitbucket.org/decimalteam/dsc-js-sdk/src/6790d35e2decb0cbb06a9149a9c476c834f99223/src/decimalevm/index.ts#lines-1105) | `decimal.update_validator_metadata` | counterpart: network-abi-unverified |
| [approveHashMultiSig](https://bitbucket.org/decimalteam/dsc-js-sdk/src/6790d35e2decb0cbb06a9149a9c476c834f99223/src/decimalevm/index.ts#lines-1404) | `multisig.approve_transaction` | counterpart: network-abi-unverified |
| [executeMultiSigTx](https://bitbucket.org/decimalteam/dsc-js-sdk/src/6790d35e2decb0cbb06a9149a9c476c834f99223/src/decimalevm/index.ts#lines-1433) | `multisig.execute` | counterpart: network-abi-unverified |
| [createMultiSig](https://bitbucket.org/decimalteam/dsc-js-sdk/src/6790d35e2decb0cbb06a9149a9c476c834f99223/src/decimalevm/index.ts#lines-1439) | `multisig.create` | counterpart: network-abi-unverified |
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
| [BurnDEL](https://bitbucket.org/decimalteam/dsc-go-sdk/src/3ef4a089b6020889e60783c2026df5725fb960e2/decimalevm/methods/del.go#lines-115) | `tx.burn_del` | counterpart: network-abi-unverified |
| [CreateToken](https://bitbucket.org/decimalteam/dsc-go-sdk/src/3ef4a089b6020889e60783c2026df5725fb960e2/decimalevm/methods/tokens.go#lines-31) | `token.create` | counterpart: network-abi-unverified |
| [ApproveToken](https://bitbucket.org/decimalteam/dsc-go-sdk/src/3ef4a089b6020889e60783c2026df5725fb960e2/decimalevm/methods/tokens.go#lines-157) | `tx.approve_erc20` | counterpart: network-abi-unverified |
| [TransferToken](https://bitbucket.org/decimalteam/dsc-go-sdk/src/3ef4a089b6020889e60783c2026df5725fb960e2/decimalevm/methods/tokens.go#lines-255) | `tx.send_erc20` | counterpart: network-abi-unverified |
| [TransferFromToken](https://bitbucket.org/decimalteam/dsc-go-sdk/src/3ef4a089b6020889e60783c2026df5725fb960e2/decimalevm/methods/tokens.go#lines-354) | `tx.transfer_from_erc20` | counterpart: network-abi-unverified |
| [BurnToken](https://bitbucket.org/decimalteam/dsc-go-sdk/src/3ef4a089b6020889e60783c2026df5725fb960e2/decimalevm/methods/tokens.go#lines-452) | `token.burn` | counterpart: network-abi-unverified |
| [BuyTokenForExactDEL](https://bitbucket.org/decimalteam/dsc-go-sdk/src/3ef4a089b6020889e60783c2026df5725fb960e2/decimalevm/methods/tokens.go#lines-549) | `token.buy` | partial: token-selector |
| [BuyExactTokenForDEL](https://bitbucket.org/decimalteam/dsc-go-sdk/src/3ef4a089b6020889e60783c2026df5725fb960e2/decimalevm/methods/tokens.go#lines-658) | `token.buy_exact` | counterpart: network-abi-unverified |
| [SellTokensForExactDEL](https://bitbucket.org/decimalteam/dsc-go-sdk/src/3ef4a089b6020889e60783c2026df5725fb960e2/decimalevm/methods/tokens.go#lines-769) | `token.sell_for_exact_del` | counterpart: network-abi-unverified |
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
| [AddTokenReserveNFT](https://bitbucket.org/decimalteam/dsc-go-sdk/src/3ef4a089b6020889e60783c2026df5725fb960e2/decimalevm/methods/nft.go#lines-786) | `nft.add_token_reserve` | counterpart: network-abi-unverified |
| [TransferBatchNFT1155](https://bitbucket.org/decimalteam/dsc-go-sdk/src/3ef4a089b6020889e60783c2026df5725fb960e2/decimalevm/methods/nft.go#lines-874) | `nft.transfer_batch_erc1155` | counterpart: network-abi-unverified |
| [TransferStakeNFT](https://bitbucket.org/decimalteam/dsc-go-sdk/src/3ef4a089b6020889e60783c2026df5725fb960e2/decimalevm/methods/nft.go#lines-940) | `nft.transfer_stake` | partial: nft-stake-variants |
| [TransferStakeNFTHold](https://bitbucket.org/decimalteam/dsc-go-sdk/src/3ef4a089b6020889e60783c2026df5725fb960e2/decimalevm/methods/nft.go#lines-1019) | `nft.transfer_stake` | partial: nft-stake-variants |
| [StakeNFTToHold](https://bitbucket.org/decimalteam/dsc-go-sdk/src/3ef4a089b6020889e60783c2026df5725fb960e2/decimalevm/methods/nft.go#lines-1100) | `nft.stake_to_hold` | counterpart: network-abi-unverified |
| [StakeNFTResetHold](https://bitbucket.org/decimalteam/dsc-go-sdk/src/3ef4a089b6020889e60783c2026df5725fb960e2/decimalevm/methods/nft.go#lines-1181) | `nft.reset_stake_hold` | counterpart: network-abi-unverified |
| [WithdrawNFTWithReset](https://bitbucket.org/decimalteam/dsc-go-sdk/src/3ef4a089b6020889e60783c2026df5725fb960e2/decimalevm/methods/nft.go#lines-1260) | `nft.withdraw_with_reset` | counterpart: network-abi-unverified |
| [TransferNFTWithReset](https://bitbucket.org/decimalteam/dsc-go-sdk/src/3ef4a089b6020889e60783c2026df5725fb960e2/decimalevm/methods/nft.go#lines-1339) | `nft.transfer_with_reset` | counterpart: network-abi-unverified |
| [HoldNFTWithReset](https://bitbucket.org/decimalteam/dsc-go-sdk/src/3ef4a089b6020889e60783c2026df5725fb960e2/decimalevm/methods/nft.go#lines-1420) | `nft.hold_with_reset` | counterpart: network-abi-unverified |
| [CompleteStakeNFT](https://bitbucket.org/decimalteam/dsc-go-sdk/src/3ef4a089b6020889e60783c2026df5725fb960e2/decimalevm/methods/nft.go#lines-1501) | `nft.complete_stake` | counterpart: network-abi-unverified |
| [AddValidatorWithToken](https://bitbucket.org/decimalteam/dsc-go-sdk/src/3ef4a089b6020889e60783c2026df5725fb960e2/decimalevm/methods/validators.go#lines-17) | `decimal.add_validator_token` | counterpart: network-abi-unverified |
| [AddValidatorWithETH](https://bitbucket.org/decimalteam/dsc-go-sdk/src/3ef4a089b6020889e60783c2026df5725fb960e2/decimalevm/methods/validators.go#lines-110) | `decimal.add_validator_del` | counterpart: network-abi-unverified |
| [RemoveValidator](https://bitbucket.org/decimalteam/dsc-go-sdk/src/3ef4a089b6020889e60783c2026df5725fb960e2/decimalevm/methods/validators.go#lines-203) | `decimal.remove_validator` | counterpart: network-abi-unverified |
| [PauseValidator](https://bitbucket.org/decimalteam/dsc-go-sdk/src/3ef4a089b6020889e60783c2026df5725fb960e2/decimalevm/methods/validators.go#lines-288) | `decimal.pause_validator` | counterpart: network-abi-unverified |
| [UnpauseValidator](https://bitbucket.org/decimalteam/dsc-go-sdk/src/3ef4a089b6020889e60783c2026df5725fb960e2/decimalevm/methods/validators.go#lines-373) | `decimal.unpause_validator` | counterpart: network-abi-unverified |
| [UpdateValidatorMeta](https://bitbucket.org/decimalteam/dsc-go-sdk/src/3ef4a089b6020889e60783c2026df5725fb960e2/decimalevm/methods/validators.go#lines-458) | `decimal.update_validator_metadata` | counterpart: network-abi-unverified |
| [CreateMultiSig](https://bitbucket.org/decimalteam/dsc-go-sdk/src/3ef4a089b6020889e60783c2026df5725fb960e2/decimalevm/methods/multisig.go#lines-18) | `multisig.create` | counterpart: network-abi-unverified |
| [ExecuteSafeTransaction](https://bitbucket.org/decimalteam/dsc-go-sdk/src/3ef4a089b6020889e60783c2026df5725fb960e2/decimalevm/methods/multisig.go#lines-440) | `multisig.execute` | counterpart: network-abi-unverified |

## Reproduce

```shell
python -m pip install "tree-sitter==0.25.2" "tree-sitter-typescript==0.23.2" "tree-sitter-go==0.25.0"
python scripts/compare_upstream.py --fetch
```

Pinned source URLs and SHA256 hashes are stored in the JSON report. Upstream code is parsed, never executed.
