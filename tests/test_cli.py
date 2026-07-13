from __future__ import annotations

from decimal_web3_sdk.cli import _build_parser, _fee_quote, _tx_result
from decimal_web3_sdk.transactions import FeePreflight
from decimal_web3_sdk.transactions import TransactionResult
from decimal_web3_sdk.wallet import generate_mnemonic_account


def test_cli_parses_block_number_command() -> None:
    parser = _build_parser()
    args = parser.parse_args(["block-number"])

    assert args.command == "block-number"


def test_cli_wallet_from_mnemonic_parses_default_path() -> None:
    parser = _build_parser()
    account = generate_mnemonic_account()
    args = parser.parse_args(["wallet-from-mnemonic", account.mnemonic or ""])

    assert args.command == "wallet-from-mnemonic"
    assert args.path == "m/44'/60'/0'/0/0"
    assert args.include_mnemonic is False


def test_cli_validator_self_toggle_defaults_to_dry_run() -> None:
    parser = _build_parser()
    args = parser.parse_args(["validator-offline-self", "--private-key", "0x" + "1" * 64])

    assert args.command == "validator-offline-self"
    assert args.broadcast is False


def test_cli_validator_address_toggle_parses_validator() -> None:
    parser = _build_parser()
    args = parser.parse_args(
        [
            "validator-online",
            "--validator",
            "0x" + "3" * 40,
            "--private-key",
            "0x" + "1" * 64,
        ]
    )

    assert args.command == "validator-online"
    assert args.validator == "0x" + "3" * 40


def test_cli_send_del_defaults_to_dry_run() -> None:
    parser = _build_parser()
    args = parser.parse_args(
        [
            "send-del",
            "--to",
            "0x" + "2" * 40,
            "--amount",
            "1",
            "--private-key",
            "0x" + "1" * 64,
        ]
    )

    assert args.command == "send-del"
    assert args.broadcast is False
    assert args.wait_receipt is False


def test_cli_fee_del_has_no_broadcast_flag() -> None:
    parser = _build_parser()
    args = parser.parse_args(
        [
            "fee-del",
            "--to",
            "0x" + "2" * 40,
            "--amount",
            "1",
            "--private-key",
            "0x" + "1" * 64,
        ]
    )

    assert args.command == "fee-del"
    assert not hasattr(args, "broadcast")


def test_cli_fee_quote_serializes_balance_and_fee() -> None:
    payload = _fee_quote(
        FeePreflight(
            ok=False,
            from_address="0x" + "1" * 40,
            native_balance_wei=1,
            value_wei=10,
            fee_wei=20,
            required_wei=30,
            missing_wei=29,
            gas=10,
            gas_price_wei=2,
        )
    )

    assert payload["ok"] is False
    assert payload["gas"] == 10
    assert payload["fee_wei"] == 20
    assert payload["missing_wei"] == 29


def test_cli_transfer_from_erc20_defaults_to_dry_run() -> None:
    parser = _build_parser()
    args = parser.parse_args(
        [
            "transfer-from-erc20",
            "--token",
            "0x" + "5" * 40,
            "--owner",
            "0x" + "6" * 40,
            "--to",
            "0x" + "7" * 40,
            "--amount",
            "1",
            "--private-key",
            "0x" + "1" * 64,
        ]
    )

    assert args.command == "transfer-from-erc20"
    assert args.broadcast is False
    assert args.wait_receipt is False


def test_cli_delegate_del_defaults_to_dry_run() -> None:
    parser = _build_parser()
    args = parser.parse_args(
        [
            "delegate-del",
            "--validator",
            "0x" + "3" * 40,
            "--amount",
            "1",
            "--private-key",
            "0x" + "1" * 64,
        ]
    )

    assert args.command == "delegate-del"
    assert args.broadcast is False


def test_cli_multisend_del_accepts_multiple_recipients() -> None:
    parser = _build_parser()
    args = parser.parse_args(
        [
            "multisend-del",
            "--recipient",
            "0x" + "4" * 40 + ":0.1",
            "--recipient",
            "0x" + "5" * 40 + ":0.2",
            "--private-key",
            "0x" + "1" * 64,
        ]
    )

    assert args.command == "multisend-del"
    assert len(args.recipient) == 2


def test_cli_hold_erc20_parses_auto_approve_flag() -> None:
    parser = _build_parser()
    args = parser.parse_args(
        [
            "hold-erc20",
            "--token",
            "0x" + "5" * 40,
            "--validator",
            "0x" + "3" * 40,
            "--amount",
            "1",
            "--hold-timestamp",
            "1800000000",
            "--private-key",
            "0x" + "1" * 64,
            "--no-auto-approve",
        ]
    )

    assert args.command == "hold-erc20"
    assert args.no_auto_approve is True


def test_cli_multisend_erc20_accepts_recipients() -> None:
    parser = _build_parser()
    args = parser.parse_args(
        [
            "multisend-erc20",
            "--token",
            "0x" + "5" * 40,
            "--recipient",
            "0x" + "4" * 40 + ":0.1",
            "--private-key",
            "0x" + "1" * 64,
            "--memo",
            "daily payout",
        ]
    )

    assert args.command == "multisend-erc20"
    assert args.recipient == ["0x" + "4" * 40 + ":0.1"]
    assert args.memo == "daily payout"


def test_cli_convert_token_parses_auto_approve_flag() -> None:
    parser = _build_parser()
    args = parser.parse_args(
        [
            "convert-token",
            "--token-in",
            "0x" + "5" * 40,
            "--token-out",
            "0x" + "6" * 40,
            "--amount-in",
            "1",
            "--min-amount-out",
            "0.9",
            "--private-key",
            "0x" + "1" * 64,
            "--no-auto-approve",
        ]
    )

    assert args.command == "convert-token"
    assert args.no_auto_approve is True


def test_cli_create_reserveless_token_parses_flags() -> None:
    parser = _build_parser()
    args = parser.parse_args(
        [
            "create-reserveless-token",
            "--name",
            "Training",
            "--symbol",
            "TRN",
            "--mintable",
            "--burnable",
            "--initial-mint-raw",
            "1000",
            "--cap-raw",
            "10000",
            "--identity",
            "sdk-test",
            "--private-key",
            "0x" + "1" * 64,
        ]
    )

    assert args.command == "create-reserveless-token"
    assert args.mintable is True
    assert args.burnable is True


def test_cli_create_token_parses_reserve_meta() -> None:
    parser = _build_parser()
    args = parser.parse_args(
        [
            "create-token",
            "--name",
            "Reserve",
            "--symbol",
            "RSV",
            "--initial-mint-raw",
            "1000",
            "--min-total-supply-raw",
            "1",
            "--max-total-supply-raw",
            "1000000",
            "--crr",
            "50",
            "--identity",
            "reserve-token",
            "--private-key",
            "0x" + "1" * 64,
        ]
    )

    assert args.command == "create-token"
    assert args.crr == 50
    assert args.reserve_value_wei is None


def test_cli_delegate_nft_parses_auto_approve_flag() -> None:
    parser = _build_parser()
    args = parser.parse_args(
        [
            "delegate-nft",
            "--kind",
            "erc721",
            "--nft",
            "0x" + "8" * 40,
            "--validator",
            "0x" + "3" * 40,
            "--token-id",
            "1",
            "--private-key",
            "0x" + "1" * 64,
            "--no-auto-approve",
        ]
    )

    assert args.command == "delegate-nft"
    assert args.no_auto_approve is True


def test_cli_mint_erc1155_requires_token_fields() -> None:
    parser = _build_parser()
    args = parser.parse_args(
        [
            "mint-nft",
            "--kind",
            "erc1155",
            "--nft",
            "0x" + "8" * 40,
            "--to",
            "0x" + "4" * 40,
            "--token-uri",
            "ipfs://token",
            "--token-id",
            "7",
            "--amount",
            "10",
            "--private-key",
            "0x" + "1" * 64,
        ]
    )

    assert args.command == "mint-nft"
    assert args.token_id == 7
    assert args.amount == 10


def test_cli_tx_result_serializes_fee() -> None:
    result = TransactionResult(success=True, fee_del="1")

    payload = _tx_result(result)

    assert payload["success"] is True
    assert payload["fee_del"] == "1"
