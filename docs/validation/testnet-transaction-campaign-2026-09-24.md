# Testnet transaction campaign, 2026-09-24

Network: Decimal testnet, chain ID 202020. All submissions below were made by
the SDK after an unsigned fee estimate. The configured mnemonic was checked
against the expected testnet address in process and was not logged or packaged.
No mainnet transaction was submitted. Fee estimates are gas-limit ceilings,
not promises of the final fee. Actual fees use receipt gasUsed multiplied by
the confirmed legacy transaction gasPrice (1190.475 gwei).

Main test wallet native balance: 999.894086627411764793 tDEL before the
campaign, 984.697150421111333249 tDEL after. The change also includes
intentional token reserves, NFT reserves and a 1 tDEL transfer to a second
derived test address; it is not just transaction fees.

| Operation | Transaction hash | Estimated fee, tDEL | Actual fee, tDEL | Result |
| --- | --- | ---: | ---: | --- |
| Create reserveless ERC20 | `0x817271911ec3c520264243bbf67162566cba3e743703a1e49d652d899c8923c8` | 0.6007089231 | 0.531503039925 | success |
| Create reserve ERC20, 50% CRR | `0x6b51e3cb71e8b01412eae583156c48a7cc58c3a2d1c24eb205578781598c09e7` | 0.702126678825 | 0.628912466325 | success |
| ERC20 multisend with permit and memo | `0x80109b2167d1a7f4ce341eaab4f49e8a2fd8f765fb3ae16e530a0c96d8f00b35` | 0.2380759524 | 0.216431926425 | success, one transaction |
| Fund second derived address | `0x96a3cf0e8a939429f94e670c44d67f4ad75a0dea1cfe9e4daec943caf91c17e8` | 0.0274999725 | 0.024999975 | success |
| ERC20 transfer | `0x1b475e0e585631b8838be44da4d5c8e26e9d6441047bb272a2925af43d190014` | 0.0693285021 | 0.0628285086 | success |
| ERC20 approve | `0xd8c1a167d2a614bf2b715172c0593abe1706dc1086b76997508a18666e183352` | 0.0849665817 | 0.076822542225 | success |
| ERC20 transferFrom | `0xd71f7870a7d5648eeff2b584f570df9f10e3c22c2cd76dfa6658a514e499a5a7` | 0.077377303575 | 0.070039215675 | success |
| Buy reserve ERC20 | `0xa26819271656577eeb765fcd3833416d2b0de17c7d20e46a1cf083e2da2bc0ab` | 0.08943562485 | 0.080760633525 | success |
| Sell reserve ERC20 | `0x12d90bd8ce7c4c1d5d582ab0a0eb19c1546667b2f19baf30c7570da52bf99c73` | 0.098808234525 | 0.08679908445 | success |
| Mint reserveless ERC20 | `0x7dc6829848f4225e0bbc2f70d1bd827db1ef7002be896376b743a229775b92b2` | 0.077896350675 | 0.07049278665 | success |
| Burn reserveless ERC20 | `0x1919f07e884695d12d6890991b22c567a061652f62acc160f5e3d0ad68584741` | 0.071289214425 | 0.06457374495 | success |
| Create reserve ERC20, 30% CRR | `0xdda312473bd06edde1a0e46b90647d5f886b8b0fabc29f6400eb288e14cb0f6a` | 0.7340040279 | 0.6574421997 | success |
| Convert between reserve ERC20s | `0xf81ec6e238e52a8d51566fcdcaba102de515f49e0bd458b87300c1e0d1cb333d` | 0.294310419975 | 0.2629283085 | success, permit path |
| Delegate reserve ERC20 | `0xbe4093044ac792280da8ee44bb40c8d3b914c50f44500417673c8caa0fc4ae2a` | 0.466384057425 | 0.417467439675 | success, stake read back |
| Request stake transfer | `0x76678e9af0ac481b369409ad2f5eddadecd81242bd90f591cd4eddd28f00e99f` | 0.38828294505 | 0.34802108055 | request accepted, pending |
| Request stake unbond | `0xd74a61ec17386ef6431a98ecb50de5afd9ea97d6f2a6821b833bbed136cdeec0` | 0.375148434375 | 0.336260378025 | request accepted, pending |
| Create DRC721 collection | `0xbe225157434ff522d359b67a70a7109dc33d60e242d37b43f9fdca3da784b47a` | 0.5624565804 | 0.50392568655 | success |
| Mint DRC721 ID 1 | `0x603a91a3b248a1feccdc0a45af1a767ebb845c60628e57add674e73f95d0f571` | 0.342124657875 | 0.306988978725 | success |
| Transfer DRC721 ID 1 | `0x5d6bb19fb582550003b04d4123007ec9edab3681bfe330ead78e4704c95f034f` | 0.108067749075 | 0.097512997725 | success |
| Burn DRC721 ID 1 | `0x585320287f619564c950770ff4e2eaf03c43b3cb677bcce56b31860530483216` | 0.1161046458 | 0.102082040775 | success |
| Create DRC1155 collection | `0xf9a66f5b2bfdd51df988ad6df0120c1124cc17cd380b84fce8a9e0603835340d` | 0.600722018325 | 0.538174461825 | success |
| Mint DRC1155 ID 1, quantity 2 | `0x928fa7ec17552147c095d688ffaa21825041099f626982c2bc6642f0c90a327d` | 0.3197853945 | 0.2869949511 | success |
| Mint DRC1155 ID 2, quantity 1 | `0x5ddb5a1df409288dbaada86f969cfebf1f70cf2f5c96bec01a44285b606aceba` | 0.297036607725 | 0.2666378286 | success |
| Transfer both DRC1155 IDs in one batch | `0x69395a0cd52881e306e59dfd2bb4a9ed4028b3c5401717aa9242efc500172355` | 0.143189142525 | 0.128967728175 | success |
| Burn DRC1155 ID 1 | `0x9132426d92ac637cd59d62a54cda23fd56bf4ee40940e859454a3fc0b54e1896` | 0.11944988055 | 0.1050856092 | success |
| Burn DRC1155 ID 2 | `0xec9f5b1560116e8a83fd75002e26a7d0a9b6c1457ec5197cdff3e1c1e0f8701f` | 0.11944988055 | 0.1050856092 | success |
| Update token identity | `0xa7d689f807eb4c2ead0f94020a842e9916bd2883e542d9b6f6f56474bd4b0ee4` | 0.06594041025 | 0.0597380355 | success |
| Update token maximum supply | `0x962bbcc7fc83c1903004b156271331d117483614e32b9fae1ee12141d7b42a75` | 0.0552666114 | 0.050177330775 | success |
| One-recipient DEL with memo | `0x48bc34e76ceea271c38a43a2def1e384e8ae2d8e8cfaef9c491c2a24cdef2252` | 0.0279618768 | 0.0254190222 | success, direct transfer |
| Two-recipient DEL with memo | `0x88616679923342499b5031dab2eef01b6f824b69115a3e106abf092defafdd7e` | 0.1001713284 | 0.09106419465 | success, aggregate |

Three fungible tokens with different reserve/minting parameters were created.
Reserve token buy, sell and conversion balances matched the receipts. ERC20
allowance decreased from 0.5 to 0.25 after transferFrom. DRC1155 holdings after
batch transfer were 1/0 and 0/1 for IDs 1/2 on source/recipient respectively;
after burn, only source ID 1 remained. All 30 listed transaction receipts had
status 1.

Staking transfer and unbond emitted freezeStatus=1 requests. They are **not**
settled withdrawals. Their cooldown completion and any withdraw-with-reset must
be verified separately after maturity. NFT staking/hold, validator administration,
checks, bridge and multisig were not broadcast in this campaign. They retain
offline tests and some read-only checks only. No claim of complete JS/Go parity.
