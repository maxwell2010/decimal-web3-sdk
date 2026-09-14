from __future__ import annotations

import argparse
import getpass
import asyncio
import json
from decimal import Decimal
from typing import Any

from .client import DecimalClient
from .config import NetworkConfig
from .decimal import (
    DelegateDelRequest,
    DelegateErc20Request,
    HoldDelRequest,
    HoldErc20Request,
    MultisendDelRequest,
    MultisendErc20Recipient,
    MultisendErc20Request,
    MultisendRecipient,
    UnbondDelRequest,
    UnbondErc20Request,
    ValidatorPauseRequest,
    ValidatorSelfPauseRequest,
    WithdrawHoldErc20Request,
    WithdrawHoldDelRequest,
)
from .nft import (
    CreateNftCollectionRequest,
    DelegateNftRequest,
    HoldNftRequest,
    MintNftRequest,
    NftApprovalRequest,
    NftTransferRequest,
    TransferNftStakeRequest,
    WithdrawNftRequest,
)
from .test_harness import run_env_training
from .token import (
    BurnTokenRequest,
    BuyTokenRequest,
    ConvertTokenRequest,
    CreateReservelessTokenRequest,
    CreateTokenRequest,
    MintTokenRequest,
    SellTokenRequest,
    UpdateTokenDetailsRequest,
)
from .transactions import (
    ContractCallRequest,
    Erc20ApproveRequest,
    Erc20TransferFromRequest,
    Erc20TransferRequest,
    FeePreflight,
    NativeTransferRequest,
)
from .wallet import (
    DEFAULT_DERIVATION_PATH,
    generate_mnemonic_account,
    mnemonic_to_account,
    mnemonic_to_accounts,
)


def main() -> None:
    parser = _build_parser()
    args = parser.parse_args()
    try:
        result = asyncio.run(_run(args))
    except KeyboardInterrupt:
        raise SystemExit(130)
    if result is not None:
        print(_json(result))


async def _run(args: argparse.Namespace) -> Any:
    if args.command == "wallet-generate":
        wallet = generate_mnemonic_account(
            num_words=args.words,
            passphrase=args.passphrase or "",
            account_path=args.path,
        )
        return wallet.__dict__
    if args.command == "wallet-from-mnemonic":
        wallet = mnemonic_to_account(
            args.mnemonic or getpass.getpass("Mnemonic (local, hidden): "),
            passphrase=args.passphrase or "",
            account_path=args.path,
            account_index=args.index,
            include_mnemonic=args.include_mnemonic,
        )
        return {
            "address": wallet.address,
            "derivation_path": wallet.derivation_path,
            **({"private_key": wallet.private_key} if args.include_private_key else {}),
            **({"mnemonic": wallet.mnemonic} if args.include_mnemonic else {}),
        }
    if args.command == "wallet-sequence":
        wallets = mnemonic_to_accounts(
            args.mnemonic or getpass.getpass("Mnemonic (local, hidden): "),
            passphrase=args.passphrase or "",
            start_index=args.start_index,
            count=args.count,
        )
        return [
            {
                "index": args.start_index + offset,
                "address": wallet.address,
                "derivation_path": wallet.derivation_path,
                **({"private_key": wallet.private_key} if args.include_private_keys else {}),
            }
            for offset, wallet in enumerate(wallets)
        ]

    if hasattr(args, "private_key") and not args.private_key:
        args.private_key = mnemonic_to_account(
            getpass.getpass("Mnemonic (local, hidden): "), account_index=args.account_index
        ).private_key
    async with DecimalClient(getattr(NetworkConfig, args.network)()) as client:
        if args.command == "health":
            return await client.rest.health()
        if args.command == "monitor":
            snapshot = await client.monitor().snapshot()
            return {
                "healthy": snapshot.healthy,
                "metrics": snapshot.result.metrics,
                "results": [item.__dict__ for item in snapshot.result.results],
            }
        if args.command == "block":
            if args.height == "latest":
                return await client.rest.latest_block()
            return await client.rest.block(int(args.height))
        if args.command == "block-number":
            return {"block_number": await client.block_number()}
        if args.command == "balance":
            return {"address": args.address, "balance_del": await client.balance_del(args.address)}
        if args.command == "address":
            return await client.rest.address_full(args.address, with_erc20=args.erc20, symbols=args.symbols)
        if args.command == "tx":
            return await client.rest.tx(args.hash)
        if args.command == "txs":
            return await client.rest.txs(address=args.address, type=args.type)
        if args.command == "validators":
            return await client.rest.validators()
        if args.command == "validator":
            return await client.rest.validator(args.validator)
        if args.command == "wallet-staking":
            summary = await client.rest.wallet_staking_summary(args.address, include_unstakes=not args.no_unstakes)
            return {
                "address": summary.address,
                "total_del": str(summary.total_del),
                "coin_total_del": str(summary.coin_total_del),
                "nft_hold_total_del": str(summary.nft_hold_total_del),
                "positions": [position.__dict__ for position in summary.positions],
                "unstakes": [unstake.__dict__ for unstake in summary.unstakes],
            }
        if args.command == "coins":
            return await client.rest.coins(with_price=args.price, limit=args.limit)
        if args.command == "coin":
            return await client.rest.coin(args.denom)
        if args.command == "erc20-info":
            info = await client.erc20.info(args.token)
            return info.__dict__
        if args.command == "erc20-balance":
            balance = await client.erc20.balance(args.token, args.address)
            return balance.as_dict()
        if args.command == "send-del":
            _require_private_key(args.private_key)
            request = NativeTransferRequest(
                to=args.to,
                amount_del=Decimal(args.amount),
                private_key=args.private_key,
                memo=args.memo,
            )
            result = await client.tx.send_del(
                request,
                broadcast=args.broadcast,
                wait_receipt=args.wait_receipt,
            )
            return _tx_result(result)
        if args.command == "fee-del":
            _require_private_key(args.private_key)
            quote = await client.tx.estimate_fee_for_native_transfer(
                NativeTransferRequest(
                    to=args.to,
                    amount_del=Decimal(args.amount),
                    private_key=args.private_key,
                    memo=args.memo,
                ),
                exact=args.exact,
            )
            return _fee_quote(quote)
        if args.command == "send-erc20":
            _require_private_key(args.private_key)
            request = Erc20TransferRequest(
                token=args.token,
                to=args.to,
                amount=Decimal(args.amount),
                private_key=args.private_key,
                decimals=args.decimals,
            )
            result = await client.tx.send_erc20(
                request,
                broadcast=args.broadcast,
                wait_receipt=args.wait_receipt,
            )
            return _tx_result(result)
        if args.command == "fee-erc20":
            _require_private_key(args.private_key)
            quote = await client.tx.estimate_fee_for_erc20_transfer(
                Erc20TransferRequest(
                    token=args.token,
                    to=args.to,
                    amount=Decimal(args.amount),
                    private_key=args.private_key,
                    decimals=args.decimals,
                ),
                exact=args.exact,
            )
            return _fee_quote(quote)
        if args.command == "approve-erc20":
            _require_private_key(args.private_key)
            request = Erc20ApproveRequest(
                token=args.token,
                spender=args.spender,
                amount=Decimal(args.amount),
                private_key=args.private_key,
                decimals=args.decimals,
            )
            result = await client.tx.approve_erc20(
                request,
                broadcast=args.broadcast,
                wait_receipt=args.wait_receipt,
            )
            return _tx_result(result)
        if args.command == "fee-erc20-approve":
            _require_private_key(args.private_key)
            quote = await client.tx.estimate_fee_for_erc20_approve(
                Erc20ApproveRequest(
                    token=args.token,
                    spender=args.spender,
                    amount=Decimal(args.amount),
                    private_key=args.private_key,
                    decimals=args.decimals,
                ),
                exact=args.exact,
            )
            return _fee_quote(quote)
        if args.command == "transfer-from-erc20":
            _require_private_key(args.private_key)
            request = Erc20TransferFromRequest(
                token=args.token,
                owner=args.owner,
                to=args.to,
                amount=Decimal(args.amount),
                private_key=args.private_key,
                decimals=args.decimals,
            )
            result = await client.tx.transfer_from_erc20(
                request,
                broadcast=args.broadcast,
                wait_receipt=args.wait_receipt,
            )
            return _tx_result(result)
        if args.command == "fee-contract":
            _require_private_key(args.private_key)
            quote = await client.tx.estimate_fee_for_contract_call(
                ContractCallRequest(
                    contract=args.contract,
                    private_key=args.private_key,
                    data=args.data,
                    value_wei=args.value_wei,
                ),
                exact=args.exact,
            )
            return _fee_quote(quote)
        if args.command == "delegate-del":
            _require_private_key(args.private_key)
            result = await client.decimal.delegate_del(
                DelegateDelRequest(
                    validator=args.validator,
                    amount_del=Decimal(args.amount),
                    private_key=args.private_key,
                ),
                broadcast=args.broadcast,
                wait_receipt=args.wait_receipt,
            )
            return _tx_result(result)
        if args.command == "hold-del":
            _require_private_key(args.private_key)
            result = await client.decimal.hold_del(
                HoldDelRequest(
                    validator=args.validator,
                    amount_del=Decimal(args.amount),
                    hold_timestamp=args.hold_timestamp,
                    private_key=args.private_key,
                ),
                broadcast=args.broadcast,
                wait_receipt=args.wait_receipt,
            )
            return _tx_result(result)
        if args.command == "unbond-del":
            _require_private_key(args.private_key)
            result = await client.decimal.unbond_del(
                UnbondDelRequest(
                    validator=args.validator,
                    amount_del=Decimal(args.amount),
                    private_key=args.private_key,
                ),
                broadcast=args.broadcast,
                wait_receipt=args.wait_receipt,
            )
            return _tx_result(result)
        if args.command == "withdraw-hold-del":
            _require_private_key(args.private_key)
            result = await client.decimal.withdraw_hold_del(
                WithdrawHoldDelRequest(
                    validator=args.validator,
                    amount_del=Decimal(args.amount),
                    hold_timestamp=args.hold_timestamp,
                    private_key=args.private_key,
                ),
                broadcast=args.broadcast,
                wait_receipt=args.wait_receipt,
            )
            return _tx_result(result)
        if args.command == "multisend-del":
            _require_private_key(args.private_key)
            recipients = [
                MultisendRecipient(to=item.split(":", 1)[0], amount_del=Decimal(item.split(":", 1)[1]))
                for item in args.recipient
            ]
            result = await client.decimal.multisend_del(
                MultisendDelRequest(
                    recipients=recipients,
                    private_key=args.private_key,
                    memo=args.memo,
                ),
                broadcast=args.broadcast,
                wait_receipt=args.wait_receipt,
            )
            return _tx_result(result)
        if args.command == "delegate-erc20":
            _require_private_key(args.private_key)
            result = await client.decimal.delegate_erc20(
                DelegateErc20Request(
                    token=args.token,
                    validator=args.validator,
                    amount=Decimal(args.amount),
                    private_key=args.private_key,
                    decimals=args.decimals,
                    memo=args.memo,
                    auto_approve=not args.no_auto_approve,
                ),
                broadcast=args.broadcast,
                wait_receipt=args.wait_receipt,
            )
            return _workflow_result(result)
        if args.command == "multisend-erc20":
            _require_private_key(args.private_key)
            recipients = [
                MultisendErc20Recipient(to=item.split(":", 1)[0], amount=Decimal(item.split(":", 1)[1]))
                for item in args.recipient
            ]
            result = await client.decimal.multisend_erc20(
                MultisendErc20Request(
                    token=args.token,
                    recipients=recipients,
                    private_key=args.private_key,
                    decimals=args.decimals,
                    auto_approve=not args.no_auto_approve,
                ),
                broadcast=args.broadcast,
                wait_receipt=args.wait_receipt,
            )
            return _workflow_result(result)
        if args.command == "hold-erc20":
            _require_private_key(args.private_key)
            result = await client.decimal.hold_erc20(
                HoldErc20Request(
                    token=args.token,
                    validator=args.validator,
                    amount=Decimal(args.amount),
                    hold_timestamp=args.hold_timestamp,
                    private_key=args.private_key,
                    decimals=args.decimals,
                    auto_approve=not args.no_auto_approve,
                ),
                broadcast=args.broadcast,
                wait_receipt=args.wait_receipt,
            )
            return _workflow_result(result)
        if args.command == "unbond-erc20":
            _require_private_key(args.private_key)
            result = await client.decimal.unbond_erc20(
                UnbondErc20Request(
                    token=args.token,
                    validator=args.validator,
                    amount=Decimal(args.amount),
                    private_key=args.private_key,
                    decimals=args.decimals,
                ),
                broadcast=args.broadcast,
                wait_receipt=args.wait_receipt,
            )
            return _workflow_result(result)
        if args.command == "withdraw-hold-erc20":
            _require_private_key(args.private_key)
            result = await client.decimal.withdraw_hold_erc20(
                WithdrawHoldErc20Request(
                    token=args.token,
                    validator=args.validator,
                    amount=Decimal(args.amount),
                    hold_timestamp=args.hold_timestamp,
                    private_key=args.private_key,
                    decimals=args.decimals,
                ),
                broadcast=args.broadcast,
                wait_receipt=args.wait_receipt,
            )
            return _workflow_result(result)
        if args.command == "buy-token":
            _require_private_key(args.private_key)
            result = await client.token.buy(
                BuyTokenRequest(
                    token=args.token,
                    amount_del=Decimal(args.amount_del),
                    min_amount_out_raw=args.min_amount_out_raw,
                    private_key=args.private_key,
                ),
                broadcast=args.broadcast,
                wait_receipt=args.wait_receipt,
            )
            return _tx_result(result)
        if args.command == "sell-token":
            _require_private_key(args.private_key)
            result = await client.token.sell(
                SellTokenRequest(
                    token=args.token,
                    amount=Decimal(args.amount),
                    min_amount_del_out_wei=args.min_amount_del_out_wei,
                    private_key=args.private_key,
                    decimals=args.decimals,
                ),
                broadcast=args.broadcast,
                wait_receipt=args.wait_receipt,
            )
            return _tx_result(result)
        if args.command == "convert-token":
            _require_private_key(args.private_key)
            result = await client.token.convert(
                ConvertTokenRequest(
                    token_in=args.token_in,
                    token_out=args.token_out,
                    amount_in=Decimal(args.amount_in),
                    min_amount_out=Decimal(args.min_amount_out),
                    private_key=args.private_key,
                    token_in_decimals=args.token_in_decimals,
                    token_out_decimals=args.token_out_decimals,
                    auto_approve=not args.no_auto_approve,
                ),
                broadcast=args.broadcast,
                wait_receipt=args.wait_receipt,
            )
            return _workflow_result(result)
        if args.command == "burn-token":
            _require_private_key(args.private_key)
            result = await client.token.burn(
                BurnTokenRequest(
                    token=args.token,
                    amount=Decimal(args.amount),
                    private_key=args.private_key,
                    decimals=args.decimals,
                ),
                broadcast=args.broadcast,
                wait_receipt=args.wait_receipt,
            )
            return _tx_result(result)
        if args.command == "mint-token":
            _require_private_key(args.private_key)
            result = await client.token.mint(
                MintTokenRequest(
                    token=args.token,
                    to=args.to,
                    amount=Decimal(args.amount),
                    private_key=args.private_key,
                    decimals=args.decimals,
                ),
                broadcast=args.broadcast,
                wait_receipt=args.wait_receipt,
            )
            return _tx_result(result)
        if args.command == "update-token-details":
            _require_private_key(args.private_key)
            result = await client.token.update_details(
                UpdateTokenDetailsRequest(
                    token=args.token,
                    identity=args.identity,
                    max_total_supply_raw=args.max_total_supply_raw,
                    private_key=args.private_key,
                ),
                broadcast=args.broadcast,
                wait_receipt=args.wait_receipt,
            )
            return _tx_result(result)
        if args.command == "create-reserveless-token":
            _require_private_key(args.private_key)
            result = await client.token.create_reserveless(
                CreateReservelessTokenRequest(
                    name=args.name,
                    symbol=args.symbol,
                    mintable=args.mintable,
                    burnable=args.burnable,
                    initial_mint_raw=args.initial_mint_raw,
                    cap_raw=args.cap_raw,
                    identity=args.identity,
                    private_key=args.private_key,
                ),
                broadcast=args.broadcast,
                wait_receipt=args.wait_receipt,
            )
            return _tx_result(result)
        if args.command == "create-token":
            _require_private_key(args.private_key)
            result = await client.token.create(
                CreateTokenRequest(
                    name=args.name,
                    symbol=args.symbol,
                    initial_mint_raw=args.initial_mint_raw,
                    min_total_supply_raw=args.min_total_supply_raw,
                    max_total_supply_raw=args.max_total_supply_raw,
                    crr=args.crr,
                    identity=args.identity,
                    reserve_value_wei=args.reserve_value_wei,
                    creator=args.creator,
                    private_key=args.private_key,
                ),
                broadcast=args.broadcast,
                wait_receipt=args.wait_receipt,
            )
            return _tx_result(result)
        if args.command == "create-nft":
            _require_private_key(args.private_key)
            result = await client.nft.create_collection(
                CreateNftCollectionRequest(
                    kind=args.kind,
                    symbol=args.symbol,
                    name=args.name,
                    contract_uri=args.contract_uri,
                    refundable=args.refundable,
                    creator=args.creator,
                    private_key=args.private_key,
                ),
                broadcast=args.broadcast,
                wait_receipt=args.wait_receipt,
            )
            return _tx_result(result)
        if args.command == "mint-nft":
            _require_private_key(args.private_key)
            result = await client.nft.mint(
                MintNftRequest(
                    kind=args.kind,
                    nft=args.nft,
                    to=args.to,
                    token_uri=args.token_uri,
                    token_id=args.token_id,
                    amount=args.amount,
                    reserve_amount_raw=args.reserve_amount_raw,
                    reserve_token=args.reserve_token,
                    value_wei=args.value_wei,
                    private_key=args.private_key,
                ),
                broadcast=args.broadcast,
                wait_receipt=args.wait_receipt,
            )
            return _tx_result(result)
        if args.command == "transfer-nft":
            _require_private_key(args.private_key)
            result = await client.nft.transfer(
                NftTransferRequest(
                    kind=args.kind,
                    nft=args.nft,
                    to=args.to,
                    token_id=args.token_id,
                    amount=args.amount,
                    private_key=args.private_key,
                ),
                broadcast=args.broadcast,
                wait_receipt=args.wait_receipt,
            )
            return _tx_result(result)
        if args.command == "approve-nft":
            _require_private_key(args.private_key)
            result = await client.nft.set_approval_for_all(
                NftApprovalRequest(
                    kind=args.kind,
                    nft=args.nft,
                    operator=args.operator,
                    approved=not args.revoke,
                    private_key=args.private_key,
                ),
                broadcast=args.broadcast,
                wait_receipt=args.wait_receipt,
            )
            return _tx_result(result)
        if args.command == "delegate-nft":
            _require_private_key(args.private_key)
            result = await client.nft.delegate(
                DelegateNftRequest(
                    kind=args.kind,
                    nft=args.nft,
                    validator=args.validator,
                    token_id=args.token_id,
                    amount=args.amount,
                    private_key=args.private_key,
                    auto_approve=not args.no_auto_approve,
                ),
                broadcast=args.broadcast,
                wait_receipt=args.wait_receipt,
            )
            return _workflow_result(result)
        if args.command == "hold-nft":
            _require_private_key(args.private_key)
            result = await client.nft.hold(
                HoldNftRequest(
                    kind=args.kind,
                    nft=args.nft,
                    validator=args.validator,
                    token_id=args.token_id,
                    hold_timestamp=args.hold_timestamp,
                    amount=args.amount,
                    private_key=args.private_key,
                    auto_approve=not args.no_auto_approve,
                ),
                broadcast=args.broadcast,
                wait_receipt=args.wait_receipt,
            )
            return _workflow_result(result)
        if args.command == "transfer-nft-stake":
            _require_private_key(args.private_key)
            result = await client.nft.transfer_stake(
                TransferNftStakeRequest(
                    nft=args.nft,
                    validator=args.validator,
                    new_validator=args.new_validator,
                    token_id=args.token_id,
                    amount=args.amount,
                    hold_timestamp=args.hold_timestamp,
                    private_key=args.private_key,
                ),
                broadcast=args.broadcast,
                wait_receipt=args.wait_receipt,
            )
            return _tx_result(result)
        if args.command == "withdraw-nft":
            _require_private_key(args.private_key)
            result = await client.nft.withdraw(
                WithdrawNftRequest(
                    nft=args.nft,
                    validator=args.validator,
                    token_id=args.token_id,
                    amount=args.amount,
                    hold_timestamp=args.hold_timestamp,
                    private_key=args.private_key,
                ),
                broadcast=args.broadcast,
                wait_receipt=args.wait_receipt,
            )
            return _tx_result(result)
        if args.command == "validator-offline-self":
            _require_private_key(args.private_key)
            result = await client.decimal.pause_self_validator(
                ValidatorSelfPauseRequest(private_key=args.private_key),
                broadcast=args.broadcast,
                wait_receipt=args.wait_receipt,
            )
            return _workflow_result(result)
        if args.command == "validator-online-self":
            _require_private_key(args.private_key)
            result = await client.decimal.unpause_self_validator(
                ValidatorSelfPauseRequest(private_key=args.private_key),
                broadcast=args.broadcast,
                wait_receipt=args.wait_receipt,
            )
            return _workflow_result(result)
        if args.command == "validator-offline":
            _require_private_key(args.private_key)
            result = await client.decimal.pause_validator(
                ValidatorPauseRequest(validator=args.validator, private_key=args.private_key),
                broadcast=args.broadcast,
                wait_receipt=args.wait_receipt,
            )
            return _workflow_result(result)
        if args.command == "validator-online":
            _require_private_key(args.private_key)
            result = await client.decimal.unpause_validator(
                ValidatorPauseRequest(validator=args.validator, private_key=args.private_key),
                broadcast=args.broadcast,
                wait_receipt=args.wait_receipt,
            )
            return _workflow_result(result)
        if args.command == "validator-status":
            return {
                "validator": args.validator,
                "status": await client.decimal.validator_status(args.validator),
                "active": await client.decimal.validator_is_active(args.validator),
                "member": await client.decimal.validator_is_member(args.validator),
            }
        if args.command == "train-env":
            records = await run_env_training()
            return [record.__dict__ for record in records]
    raise SystemExit(f"Unknown command: {args.command}")


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="decimal-sdk")
    parser.add_argument("--network", choices=("mainnet", "testnet", "devnet"), default="mainnet",
                        help="Decimal network (default: mainnet)")
    parser.add_argument("--account-index", type=int, default=0)
    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("health")
    sub.add_parser("monitor")
    sub.add_parser("block-number")

    wallet_generate = sub.add_parser("wallet-generate")
    wallet_generate.add_argument("--words", type=int, default=12, choices=[12, 15, 18, 21, 24])
    wallet_generate.add_argument("--passphrase")
    wallet_generate.add_argument("--path", default=DEFAULT_DERIVATION_PATH)

    wallet_from_mnemonic = sub.add_parser("wallet-from-mnemonic")
    wallet_from_mnemonic.add_argument("mnemonic", nargs="?")
    wallet_from_mnemonic.add_argument("--include-private-key", action="store_true")
    wallet_from_mnemonic.add_argument("--passphrase")
    wallet_from_mnemonic.add_argument("--path", default=DEFAULT_DERIVATION_PATH)
    wallet_from_mnemonic.add_argument("--index", type=int)
    wallet_from_mnemonic.add_argument("--include-mnemonic", action="store_true")

    wallet_sequence = sub.add_parser("wallet-sequence")
    wallet_sequence.add_argument("mnemonic", nargs="?")
    wallet_sequence.add_argument("--passphrase")
    wallet_sequence.add_argument("--start-index", type=int, default=0)
    wallet_sequence.add_argument("--count", type=int, default=10)
    wallet_sequence.add_argument("--include-private-keys", action="store_true")

    block = sub.add_parser("block")
    block.add_argument("height", help="Block height or 'latest'")

    balance = sub.add_parser("balance")
    balance.add_argument("address")

    address = sub.add_parser("address")
    address.add_argument("address")
    address.add_argument("--erc20", action="store_true")
    address.add_argument("--symbols")

    tx = sub.add_parser("tx")
    tx.add_argument("hash")

    txs = sub.add_parser("txs")
    txs.add_argument("--address")
    txs.add_argument("--type")

    sub.add_parser("validators")
    validator = sub.add_parser("validator")
    validator.add_argument("validator")

    wallet_staking = sub.add_parser("wallet-staking")
    wallet_staking.add_argument("address")
    wallet_staking.add_argument("--no-unstakes", action="store_true")

    coins = sub.add_parser("coins")
    coins.add_argument("--price", action="store_true")
    coins.add_argument("--limit", type=int, default=50)

    coin = sub.add_parser("coin")
    coin.add_argument("denom")

    erc20_info = sub.add_parser("erc20-info")
    erc20_info.add_argument("token")

    erc20_balance = sub.add_parser("erc20-balance")
    erc20_balance.add_argument("token")
    erc20_balance.add_argument("address")

    send_del = sub.add_parser("send-del")
    send_del.add_argument("--to", required=True)
    send_del.add_argument("--amount", required=True)
    send_del.add_argument("--private-key", default=None, help="Technical key override; omit for a hidden mnemonic prompt")
    send_del.add_argument("--memo")
    _broadcast_flags(send_del)

    fee_del = sub.add_parser("fee-del")
    fee_del.add_argument("--to", required=True)
    fee_del.add_argument("--amount", required=True)
    fee_del.add_argument("--private-key", default=None, help="Technical key override; omit for a hidden mnemonic prompt")
    fee_del.add_argument("--memo")
    fee_del.add_argument("--exact", action="store_true", help="Show exact estimateGas fee instead of buffered gas-limit fee")

    send_erc20 = sub.add_parser("send-erc20")
    send_erc20.add_argument("--token", required=True)
    send_erc20.add_argument("--to", required=True)
    send_erc20.add_argument("--amount", required=True)
    send_erc20.add_argument("--private-key", default=None, help="Technical key override; omit for a hidden mnemonic prompt")
    send_erc20.add_argument("--decimals", type=int)
    _broadcast_flags(send_erc20)

    fee_erc20 = sub.add_parser("fee-erc20")
    fee_erc20.add_argument("--token", required=True)
    fee_erc20.add_argument("--to", required=True)
    fee_erc20.add_argument("--amount", required=True)
    fee_erc20.add_argument("--private-key", default=None, help="Technical key override; omit for a hidden mnemonic prompt")
    fee_erc20.add_argument("--decimals", type=int)
    fee_erc20.add_argument("--exact", action="store_true", help="Show exact estimateGas fee instead of buffered gas-limit fee")

    approve_erc20 = sub.add_parser("approve-erc20")
    approve_erc20.add_argument("--token", required=True)
    approve_erc20.add_argument("--spender", required=True)
    approve_erc20.add_argument("--amount", required=True)
    approve_erc20.add_argument("--private-key", default=None, help="Technical key override; omit for a hidden mnemonic prompt")
    approve_erc20.add_argument("--decimals", type=int)
    _broadcast_flags(approve_erc20)

    fee_erc20_approve = sub.add_parser("fee-erc20-approve")
    fee_erc20_approve.add_argument("--token", required=True)
    fee_erc20_approve.add_argument("--spender", required=True)
    fee_erc20_approve.add_argument("--amount", required=True)
    fee_erc20_approve.add_argument("--private-key", default=None, help="Technical key override; omit for a hidden mnemonic prompt")
    fee_erc20_approve.add_argument("--decimals", type=int)
    fee_erc20_approve.add_argument("--exact", action="store_true", help="Show exact estimateGas fee instead of buffered gas-limit fee")

    transfer_from_erc20 = sub.add_parser("transfer-from-erc20")
    transfer_from_erc20.add_argument("--token", required=True)
    transfer_from_erc20.add_argument("--owner", required=True)
    transfer_from_erc20.add_argument("--to", required=True)
    transfer_from_erc20.add_argument("--amount", required=True)
    transfer_from_erc20.add_argument("--private-key", default=None, help="Technical key override; omit for a hidden mnemonic prompt")
    transfer_from_erc20.add_argument("--decimals", type=int)
    _broadcast_flags(transfer_from_erc20)

    fee_contract = sub.add_parser("fee-contract")
    fee_contract.add_argument("--contract", required=True)
    fee_contract.add_argument("--data", required=True)
    fee_contract.add_argument("--private-key", default=None, help="Technical key override; omit for a hidden mnemonic prompt")
    fee_contract.add_argument("--value-wei", type=int, default=0)
    fee_contract.add_argument("--exact", action="store_true", help="Show exact estimateGas fee instead of buffered gas-limit fee")

    delegate_del = sub.add_parser("delegate-del")
    delegate_del.add_argument("--validator", required=True)
    delegate_del.add_argument("--amount", required=True)
    delegate_del.add_argument("--private-key", default=None, help="Technical key override; omit for a hidden mnemonic prompt")
    _broadcast_flags(delegate_del)

    hold_del = sub.add_parser("hold-del")
    hold_del.add_argument("--validator", required=True)
    hold_del.add_argument("--amount", required=True)
    hold_del.add_argument("--hold-timestamp", required=True, type=int)
    hold_del.add_argument("--private-key", default=None, help="Technical key override; omit for a hidden mnemonic prompt")
    _broadcast_flags(hold_del)

    unbond_del = sub.add_parser("unbond-del")
    unbond_del.add_argument("--validator", required=True)
    unbond_del.add_argument("--amount", required=True)
    unbond_del.add_argument("--private-key", default=None, help="Technical key override; omit for a hidden mnemonic prompt")
    _broadcast_flags(unbond_del)

    withdraw_hold_del = sub.add_parser("withdraw-hold-del")
    withdraw_hold_del.add_argument("--validator", required=True)
    withdraw_hold_del.add_argument("--amount", required=True)
    withdraw_hold_del.add_argument("--hold-timestamp", required=True, type=int)
    withdraw_hold_del.add_argument("--private-key", default=None, help="Technical key override; omit for a hidden mnemonic prompt")
    _broadcast_flags(withdraw_hold_del)

    multisend_del = sub.add_parser("multisend-del")
    multisend_del.add_argument("--recipient", action="append", required=True, help="Format: 0xaddress:amount")
    multisend_del.add_argument("--private-key", default=None, help="Technical key override; omit for a hidden mnemonic prompt")
    multisend_del.add_argument("--memo")
    _broadcast_flags(multisend_del)

    delegate_erc20 = sub.add_parser("delegate-erc20")
    delegate_erc20.add_argument("--token", required=True)
    delegate_erc20.add_argument("--validator", required=True)
    delegate_erc20.add_argument("--amount", required=True)
    delegate_erc20.add_argument("--private-key", default=None, help="Technical key override; omit for a hidden mnemonic prompt")
    delegate_erc20.add_argument("--decimals", type=int)
    delegate_erc20.add_argument("--no-auto-approve", action="store_true")
    _broadcast_flags(delegate_erc20)

    multisend_erc20 = sub.add_parser("multisend-erc20")
    multisend_erc20.add_argument("--token", required=True)
    multisend_erc20.add_argument("--recipient", action="append", required=True, help="Format: 0xaddress:amount")
    multisend_erc20.add_argument("--private-key", default=None, help="Technical key override; omit for a hidden mnemonic prompt")
    multisend_erc20.add_argument("--decimals", type=int)
    multisend_erc20.add_argument("--memo")
    multisend_erc20.add_argument("--no-auto-approve", action="store_true")
    _broadcast_flags(multisend_erc20)

    hold_erc20 = sub.add_parser("hold-erc20")
    hold_erc20.add_argument("--token", required=True)
    hold_erc20.add_argument("--validator", required=True)
    hold_erc20.add_argument("--amount", required=True)
    hold_erc20.add_argument("--hold-timestamp", required=True, type=int)
    hold_erc20.add_argument("--private-key", default=None, help="Technical key override; omit for a hidden mnemonic prompt")
    hold_erc20.add_argument("--decimals", type=int)
    hold_erc20.add_argument("--no-auto-approve", action="store_true")
    _broadcast_flags(hold_erc20)

    unbond_erc20 = sub.add_parser("unbond-erc20")
    unbond_erc20.add_argument("--token", required=True)
    unbond_erc20.add_argument("--validator", required=True)
    unbond_erc20.add_argument("--amount", required=True)
    unbond_erc20.add_argument("--private-key", default=None, help="Technical key override; omit for a hidden mnemonic prompt")
    unbond_erc20.add_argument("--decimals", type=int)
    _broadcast_flags(unbond_erc20)

    withdraw_hold_erc20 = sub.add_parser("withdraw-hold-erc20")
    withdraw_hold_erc20.add_argument("--token", required=True)
    withdraw_hold_erc20.add_argument("--validator", required=True)
    withdraw_hold_erc20.add_argument("--amount", required=True)
    withdraw_hold_erc20.add_argument("--hold-timestamp", required=True, type=int)
    withdraw_hold_erc20.add_argument("--private-key", default=None, help="Technical key override; omit for a hidden mnemonic prompt")
    withdraw_hold_erc20.add_argument("--decimals", type=int)
    _broadcast_flags(withdraw_hold_erc20)

    buy_token = sub.add_parser("buy-token")
    buy_token.add_argument("--token", required=True)
    buy_token.add_argument("--amount-del", required=True)
    buy_token.add_argument("--min-amount-out-raw", type=int, default=0)
    buy_token.add_argument("--private-key", default=None, help="Technical key override; omit for a hidden mnemonic prompt")
    _broadcast_flags(buy_token)

    sell_token = sub.add_parser("sell-token")
    sell_token.add_argument("--token", required=True)
    sell_token.add_argument("--amount", required=True)
    sell_token.add_argument("--min-amount-del-out-wei", type=int, default=1)
    sell_token.add_argument("--private-key", default=None, help="Technical key override; omit for a hidden mnemonic prompt")
    sell_token.add_argument("--decimals", type=int)
    _broadcast_flags(sell_token)

    convert_token = sub.add_parser("convert-token")
    convert_token.add_argument("--token-in", required=True)
    convert_token.add_argument("--token-out", required=True)
    convert_token.add_argument("--amount-in", required=True)
    convert_token.add_argument("--min-amount-out", required=True)
    convert_token.add_argument("--private-key", default=None, help="Technical key override; omit for a hidden mnemonic prompt")
    convert_token.add_argument("--token-in-decimals", type=int)
    convert_token.add_argument("--token-out-decimals", type=int)
    convert_token.add_argument("--no-auto-approve", action="store_true")
    _broadcast_flags(convert_token)

    burn_token = sub.add_parser("burn-token")
    burn_token.add_argument("--token", required=True)
    burn_token.add_argument("--amount", required=True)
    burn_token.add_argument("--private-key", default=None, help="Technical key override; omit for a hidden mnemonic prompt")
    burn_token.add_argument("--decimals", type=int)
    _broadcast_flags(burn_token)

    mint_token = sub.add_parser("mint-token")
    mint_token.add_argument("--token", required=True)
    mint_token.add_argument("--to", required=True)
    mint_token.add_argument("--amount", required=True)
    mint_token.add_argument("--private-key", default=None, help="Technical key override; omit for a hidden mnemonic prompt")
    mint_token.add_argument("--decimals", type=int)
    _broadcast_flags(mint_token)

    update_token_details = sub.add_parser("update-token-details")
    update_token_details.add_argument("--token", required=True)
    update_token_details.add_argument("--identity", required=True)
    update_token_details.add_argument("--max-total-supply-raw", required=True, type=int)
    update_token_details.add_argument("--private-key", default=None, help="Technical key override; omit for a hidden mnemonic prompt")
    _broadcast_flags(update_token_details)

    create_reserveless = sub.add_parser("create-reserveless-token")
    create_reserveless.add_argument("--name", required=True)
    create_reserveless.add_argument("--symbol", required=True)
    create_reserveless.add_argument("--mintable", action="store_true")
    create_reserveless.add_argument("--burnable", action="store_true")
    create_reserveless.add_argument("--initial-mint-raw", required=True, type=int)
    create_reserveless.add_argument("--cap-raw", required=True, type=int)
    create_reserveless.add_argument("--identity", required=True)
    create_reserveless.add_argument("--private-key", default=None, help="Technical key override; omit for a hidden mnemonic prompt")
    _broadcast_flags(create_reserveless)

    create_token = sub.add_parser("create-token")
    create_token.add_argument("--name", required=True)
    create_token.add_argument("--symbol", required=True)
    create_token.add_argument("--initial-mint-raw", required=True, type=int)
    create_token.add_argument("--min-total-supply-raw", required=True, type=int)
    create_token.add_argument("--max-total-supply-raw", required=True, type=int)
    create_token.add_argument("--crr", required=True, type=int)
    create_token.add_argument("--identity", required=True)
    create_token.add_argument("--reserve-value-wei", type=int)
    create_token.add_argument("--creator")
    create_token.add_argument("--private-key", default=None, help="Technical key override; omit for a hidden mnemonic prompt")
    _broadcast_flags(create_token)

    create_nft = sub.add_parser("create-nft")
    create_nft.add_argument("--kind", choices=["erc721", "erc1155"], required=True)
    create_nft.add_argument("--symbol", required=True)
    create_nft.add_argument("--name", required=True)
    create_nft.add_argument("--contract-uri", required=True)
    create_nft.add_argument("--refundable", action="store_true")
    create_nft.add_argument("--creator")
    create_nft.add_argument("--private-key", default=None, help="Technical key override; omit for a hidden mnemonic prompt")
    _broadcast_flags(create_nft)

    mint_nft = sub.add_parser("mint-nft")
    mint_nft.add_argument("--kind", choices=["erc721", "erc1155"], required=True)
    mint_nft.add_argument("--nft", required=True)
    mint_nft.add_argument("--to", required=True)
    mint_nft.add_argument("--token-uri", required=True)
    mint_nft.add_argument("--token-id", type=int)
    mint_nft.add_argument("--amount", type=int, default=1)
    mint_nft.add_argument("--reserve-amount-raw", type=int, default=0)
    mint_nft.add_argument("--reserve-token", default="0x0000000000000000000000000000000000000000")
    mint_nft.add_argument("--value-wei", type=int, default=0)
    mint_nft.add_argument("--private-key", default=None, help="Technical key override; omit for a hidden mnemonic prompt")
    _broadcast_flags(mint_nft)

    transfer_nft = sub.add_parser("transfer-nft")
    transfer_nft.add_argument("--kind", choices=["erc721", "erc1155"], required=True)
    transfer_nft.add_argument("--nft", required=True)
    transfer_nft.add_argument("--to", required=True)
    transfer_nft.add_argument("--token-id", required=True, type=int)
    transfer_nft.add_argument("--amount", type=int, default=1)
    transfer_nft.add_argument("--private-key", default=None, help="Technical key override; omit for a hidden mnemonic prompt")
    _broadcast_flags(transfer_nft)

    approve_nft = sub.add_parser("approve-nft")
    approve_nft.add_argument("--kind", choices=["erc721", "erc1155"], required=True)
    approve_nft.add_argument("--nft", required=True)
    approve_nft.add_argument("--operator", required=True)
    approve_nft.add_argument("--revoke", action="store_true")
    approve_nft.add_argument("--private-key", default=None, help="Technical key override; omit for a hidden mnemonic prompt")
    _broadcast_flags(approve_nft)

    delegate_nft = sub.add_parser("delegate-nft")
    delegate_nft.add_argument("--kind", choices=["erc721", "erc1155"], required=True)
    delegate_nft.add_argument("--nft", required=True)
    delegate_nft.add_argument("--validator", required=True)
    delegate_nft.add_argument("--token-id", required=True, type=int)
    delegate_nft.add_argument("--amount", type=int, default=1)
    delegate_nft.add_argument("--private-key", default=None, help="Technical key override; omit for a hidden mnemonic prompt")
    delegate_nft.add_argument("--no-auto-approve", action="store_true")
    _broadcast_flags(delegate_nft)

    hold_nft = sub.add_parser("hold-nft")
    hold_nft.add_argument("--kind", choices=["erc721", "erc1155"], required=True)
    hold_nft.add_argument("--nft", required=True)
    hold_nft.add_argument("--validator", required=True)
    hold_nft.add_argument("--token-id", required=True, type=int)
    hold_nft.add_argument("--hold-timestamp", required=True, type=int)
    hold_nft.add_argument("--amount", type=int, default=1)
    hold_nft.add_argument("--private-key", default=None, help="Technical key override; omit for a hidden mnemonic prompt")
    hold_nft.add_argument("--no-auto-approve", action="store_true")
    _broadcast_flags(hold_nft)

    transfer_nft_stake = sub.add_parser("transfer-nft-stake")
    transfer_nft_stake.add_argument("--nft", required=True)
    transfer_nft_stake.add_argument("--validator", required=True)
    transfer_nft_stake.add_argument("--new-validator", required=True)
    transfer_nft_stake.add_argument("--token-id", required=True, type=int)
    transfer_nft_stake.add_argument("--amount", type=int, default=1)
    transfer_nft_stake.add_argument("--hold-timestamp", type=int)
    transfer_nft_stake.add_argument("--private-key", default=None, help="Technical key override; omit for a hidden mnemonic prompt")
    _broadcast_flags(transfer_nft_stake)

    withdraw_nft = sub.add_parser("withdraw-nft")
    withdraw_nft.add_argument("--nft", required=True)
    withdraw_nft.add_argument("--validator", required=True)
    withdraw_nft.add_argument("--token-id", required=True, type=int)
    withdraw_nft.add_argument("--amount", type=int, default=1)
    withdraw_nft.add_argument("--hold-timestamp", type=int)
    withdraw_nft.add_argument("--private-key", default=None, help="Technical key override; omit for a hidden mnemonic prompt")
    _broadcast_flags(withdraw_nft)

    validator_offline_self = sub.add_parser("validator-offline-self")
    validator_offline_self.add_argument("--private-key", default=None, help="Technical key override; omit for a hidden mnemonic prompt")
    _broadcast_flags(validator_offline_self)

    validator_online_self = sub.add_parser("validator-online-self")
    validator_online_self.add_argument("--private-key", default=None, help="Technical key override; omit for a hidden mnemonic prompt")
    _broadcast_flags(validator_online_self)

    validator_offline = sub.add_parser("validator-offline")
    validator_offline.add_argument("--validator", required=True)
    validator_offline.add_argument("--private-key", default=None, help="Technical key override; omit for a hidden mnemonic prompt")
    _broadcast_flags(validator_offline)

    validator_online = sub.add_parser("validator-online")
    validator_online.add_argument("--validator", required=True)
    validator_online.add_argument("--private-key", default=None, help="Technical key override; omit for a hidden mnemonic prompt")
    _broadcast_flags(validator_online)

    validator_status = sub.add_parser("validator-status")
    validator_status.add_argument("validator")

    sub.add_parser("train-env")

    return parser


def _broadcast_flags(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--broadcast", action="store_true", help="Actually broadcast transaction")
    parser.add_argument("--wait-receipt", action="store_true", help="Poll receipt after broadcast")


def _require_private_key(private_key: str) -> None:
    if not private_key:
        raise SystemExit("Private key is required")


def _tx_result(result) -> dict[str, Any]:
    return {
        "success": result.success,
        "tx_hash": result.tx_hash,
        "fee_wei": result.fee_wei,
        "fee_del": str(result.fee_del) if result.fee_del is not None else None,
        "gas": result.gas,
        "oracle_gas_price_wei": result.oracle_gas_price_wei,
        "raw_tx_hex": result.raw_tx_hex,
        "receipt": result.receipt,
        "error": result.error,
        "user_message": result.user_message,
        "native_balance_wei": result.native_balance_wei,
        "required_wei": result.required_wei,
        "missing_wei": result.missing_wei,
        "token_balance_raw": result.token_balance_raw,
        "token_required_raw": result.token_required_raw,
        "token_missing_raw": result.token_missing_raw,
    }


def _workflow_result(result) -> dict[str, Any]:
    return {
        "success": result.success,
        "name": result.name,
        "steps": list(result.steps),
        "expected_steps": result.expected_steps,
        "actual_steps": result.actual_steps,
        "extra_steps_required": result.extra_steps_required,
        "primary": _tx_result(result.primary) if result.primary else None,
        "secondary": _tx_result(result.secondary) if result.secondary else None,
        "error": result.error,
        "user_message": result.user_message,
    }


def _fee_quote(quote: FeePreflight) -> dict[str, Any]:
    return {
        "ok": quote.ok,
        "from_address": quote.from_address,
        "native_balance_wei": quote.native_balance_wei,
        "native_balance_del": str(quote.native_balance_del),
        "value_wei": quote.value_wei,
        "value_del": str(quote.value_del),
        "gas": quote.gas,
        "estimated_gas": quote.estimated_gas,
        "gas_limit": quote.gas_limit,
        "gas_price_wei": quote.gas_price_wei,
        "effective_gas_price_wei": quote.gas_price_wei,
        "oracle_gas_price_wei": quote.oracle_gas_price_wei,
        "fee_wei": quote.fee_wei,
        "fee_del": str(quote.fee_del),
        "estimated_fee_wei": quote.estimated_fee_wei,
        "estimated_fee_del": str(quote.estimated_fee_del) if quote.estimated_fee_del is not None else None,
        "gas_limit_fee_wei": quote.gas_limit_fee_wei,
        "gas_limit_fee_del": str(quote.gas_limit_fee_del) if quote.gas_limit_fee_del is not None else None,
        "exact": quote.exact,
        "minimum_fee_wei": quote.minimum_fee_wei,
        "minimum_fee_del": str(quote.minimum_fee_del),
        "required_wei": quote.required_wei,
        "required_del": str(quote.required_del),
        "missing_wei": quote.missing_wei,
        "missing_del": str(quote.missing_del),
    }


def _json(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, indent=2, default=str)


if __name__ == "__main__":
    main()
