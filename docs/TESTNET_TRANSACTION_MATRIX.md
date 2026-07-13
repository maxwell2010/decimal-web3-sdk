# Testnet Transaction Matrix

Дата: 2026-06-16

Цель: перед broadcast считать комиссию, затем отправлять минимальную testnet-транзакцию, получать `tx_hash`, `status`, `block`, `gasUsed`, фактическую комиссию и визуальный баланс test-wallet до/после.

Test wallet:

- address: `0xb92Bd490c8e9e5D9C46d71666418d4e7Ae4534e9`
- network: `decimal-testnet`
- chain id: `202020`

## Подтверждено в testnet

| Type | Hash | Block | Preflight fee | Effective fee | Result |
| --- | --- | ---: | ---: | ---: | --- |
| `native_del_transfer` | `0x807320c65fdfe97c6bf348bb0eaa5a6da8867e1a0f560deab7e03170e6379501` | `20785269` | `17.9738382352941027 tDEL` | see receipt/gas price fallback | success |
| `multisend_del` with memo | `0x40e681c38d36a88b3488c179b66ca55ccbdaef45fe020e993473604cd656b65e` | `20785359` | `20.007760882352924538 tDEL` | `18.188590588235278992 tDEL` | success |

## Важное исправление testnet system contracts

Старый статический `token_center=0x9113...37Fb` в testnet оказался пустым адресом без bytecode. Транзакции к нему могут получать EVM `status=1`, но фактически не вызывают TokenCenter и не создают токен.

Проверочный no-op:

- hash `0xfda34fac18f557fc57b4ea5ccd64474d258c56b6a49ee0cc5c1a5f68fca866e4`;
- block `20785435`;
- status `1`;
- logs `[]`;
- token contract was not created.

SDK теперь блокирует contract-call к адресу без bytecode до подписи и broadcast:

```text
success=False
user_message=Контракт сети недоступен. Проверьте сеть или адрес контракта.
tx_hash=None
balance_before=999894.08662741176479396 tDEL
balance_after=999894.08662741176479396 tDEL
nonce_before=6
nonce_after=6
```

Из официального JS SDK перенесены known network-specific адреса для `multi-call`, `checks`, `gas-center`, `multi-sig`. Для `token-center`, `delegation`, `delegation-nft`, `master-validator`, `nft-center` в testnet нужен доступный `contract-center`/subgraph/API источник; публичные Decimal API/subgraph из текущего окружения отдают `403`.

tx-reader corpus:

- `reports/tx_reader_samples/decimal-testnet_807320c65fdfe97c6bf348bb0eaa5a6da8867e1a0f560deab7e03170e6379501.json`
- `reports/tx_reader_samples/decimal-testnet_40e681c38d36a88b3488c179b66ca55ccbdaef45fe020e993473604cd656b65e.json`
- `reports/tx_reader_samples/decimal-testnet_fda34fac18f557fc57b4ea5ccd64474d258c56b6a49ee0cc5c1a5f68fca866e4.json`
- `reports/tx_reader_samples/decimal-testnet_manifest.json`

## Следующие live-тесты

| Group | Types | Need before broadcast | Status |
| --- | --- | --- | --- |
| DEL staking | `delegate_del`, `hold_del`, `unbond_del`, `withdraw_hold_del`, `transfer_stake` | real testnet Delegation + active validator address and safe minimal amount | blocked by public discovery `403` |
| ERC20 base | `approve`, `transfer`, `transfer_from` | testnet ERC20 with positive wallet balance or created test token | blocked until real TokenCenter/test token is available |
| ERC20 workflows | `delegate_erc20`, `hold_erc20`, `unbond_erc20`, `withdraw_hold_erc20`, `multisend_erc20` | test token, real Delegation, validator, allowance/permit behavior | blocked until TokenCenter + Delegation are discovered |
| Token center | `create_token`, `buy`, `sell`, `convert`, `burn`, `mint`, `update_details` | real testnet TokenCenter address with bytecode | blocked by public discovery `403` |
| NFT | ERC721/ERC1155 create/mint/transfer/approve/delegate/hold/withdraw/burn | real testnet NftCenter + disposable test collection | blocked by public discovery `403` |
| Checks | DEL checks, token checks, redeem | minimal check amount and recipient flow | ready for live test after choosing safe checks contract flow |
| Bridge | native/token/complete | test bridge contract availability and safe params | not live-tested; requires bridge contract confirmation |
| Validator admin | pause/unpause self or validator | do not run on real validators without explicit approval | blocked by safety |

## Реализовано, но не подтверждено live broadcast

Эти группы покрыты unit/dry-run тестами SDK, но не имеют честного testnet broadcast результата из-за недоступного discovery системных контрактов или отсутствия безопасных параметров:

- Token Center: `create_token`, `create_reserveless_token`, `buy`, `sell`, `convert`, `burn`, `mint`, `update_details`.
- ERC20 base/workflows: `approve`, `transfer`, `transfer_from`, `multisend_erc20`, `delegate_erc20`, `hold_erc20`, `unbond_erc20`, `withdraw_hold_erc20`, `transfer_stake_erc20`, reset/hold-with-reset flows.
- DEL staking: `delegate_del`, `hold_del`, `unbond_del`, `withdraw_hold_del`.
- NFT: ERC721/ERC1155 collection create, mint, transfer, approve, burn, delegate, hold, transfer stake, withdraw.
- Checks: create DEL check, create token check, redeem.
- Bridge: native transfer, token transfer, complete transfer.
- Validator admin: pause/unpause self and pause/unpause validator. Do not live-test without explicit approval.

## Следующий порядок тестов

1. Unit/package gates: `pytest -q`, `python -m build`, `python -m twine check dist\*`.
2. Read-only network gates: `eth_chainId`, wallet balance, `contract_code_exists()` for every configured system contract.
3. Safe live tests already possible: native DEL transfer, DEL multisend with memo.
4. Contract tests after discovery: TokenCenter -> disposable token -> ERC20 transfer/approve -> token workflows.
5. Staking tests only after real testnet Delegation + active validator address.
6. NFT/checks/bridge tests after confirming their testnet system contracts and safe minimal params.

## Endpoint notes

- `https://testnet-val.decimalchain.com/web3/` returned `403` from this environment.
- `https://testnet-api.decimalchain.com/api/` returned `403`, so validator/token discovery via public API is currently unavailable here.
- `https://testnet-thegraph.decimalchain.com/subgraphs/name/contract-center` returned `403`, so official JS-style contract discovery is unavailable from this environment.
