from __future__ import annotations

from decimal import Decimal

from decimal_web3_sdk.rest import normalize_wallet_stake_withdrawals, normalize_wallet_staking_summary


def test_normalize_wallet_staking_summary_groups_validator_coin_positions() -> None:
    payload = {
        "Ok": True,
        "Result": {
            "base_steaks": "4928137898764178640630",
            "coin_steaks": "4928137898764178640630",
            "nft_hold_steaks": "0",
            "items": [
                {
                    "validator": {
                        "evmAddress": "0x1111111111111111111111111111111111111111",
                        "name": "MAKAROVSKY",
                    },
                    "items": [
                        {
                            "delegatedCoins": "72800000000000000000",
                            "delegatedBaseCoins": "8065399478233629240",
                            "symbol": "byacademy",
                            "stake_type": "STAKE_TYPE_COIN",
                            "is_hold": True,
                            "hold_amount": "20000000000000000000",
                            "unlocked_amount": "52800000000000000000",
                            "holds": [
                                {
                                    "amount": "20000000000000000000",
                                    "hold_start_time": 1700000000,
                                    "hold_end_time": 1710000000,
                                    "is_active": False,
                                    "is_expired": True,
                                }
                            ],
                        },
                        {
                            "delegatedCoins": "2727242864461120814609",
                            "delegatedBaseCoins": "2727242864461120814609",
                            "symbol": "DEL",
                            "stake_type": "STAKE_TYPE_COIN",
                            "is_hold": True,
                            "hold_amount": "2720000000000000000000",
                            "unlocked_amount": "7242864461120814609",
                        },
                    ],
                }
            ],
        },
    }
    coins = {
        "coins": [
            {
                "denom": "byacademy",
                "drc20_address": "0xaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
                "current_price_del": "0.110788454371340142",
            }
        ]
    }
    unstakes = {
        "Ok": True,
        "Result": {
            "unstakes": [
                {
                    "validator": {"address": "0x2222222222222222222222222222222222222222", "moniker": "Spacebot"},
                    "amount": "1000000000000000000",
                    "coin": {"symbol": "DEL"},
                    "completion_time": "2026-08-18T10:00:00Z",
                    "unfreeze_timestamp": 1787047200,
                }
            ]
        },
    }

    summary = normalize_wallet_staking_summary("0xWallet", payload, unstakes, coins)

    assert summary.total_del == Decimal("4928.13789876417864063")
    assert summary.coin_total_del == summary.total_del
    assert summary.nft_hold_total_del == 0
    assert len(summary.positions) == 2
    assert summary.positions[0].validator_name == "MAKAROVSKY"
    assert summary.positions[0].symbol == "byacademy"
    assert summary.positions[0].token_address == "0xaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
    assert summary.positions[0].token is not None
    assert summary.positions[0].amount == Decimal("72.8")
    assert summary.positions[0].base_amount_del == Decimal("8.06539947823362924")
    assert summary.positions[0].is_hold is True
    assert summary.positions[0].hold_amount == Decimal("20")
    assert summary.positions[0].held_amount == Decimal("20")
    assert summary.positions[0].matured_hold_amount == Decimal("20")
    assert summary.positions[0].available_to_unbond == Decimal("52.8")
    assert summary.positions[0].can_unbond is True
    assert summary.positions[0].can_withdraw_hold is True
    assert summary.positions[0].holds[0].contract_hold_timestamp == 1710000000
    assert summary.positions[1].symbol == "DEL"
    assert summary.positions[1].is_native is True
    assert summary.positions[1].token_address is None
    assert summary.positions[1].amount == Decimal("2727.242864461120814609")
    assert summary.positions[1].api_unlocked_delta == Decimal("7.242864461120814609")
    assert summary.positions[1].available_to_unbond == Decimal("7.242864461120814609")
    assert summary.positions[1].can_unbond is True
    assert summary.delegated_by_symbol["BYACADEMY"] == Decimal("72.8")
    assert summary.held_by_symbol["BYACADEMY"] == Decimal("20")
    assert summary.available_to_unbond_by_symbol["BYACADEMY"] == Decimal("52.8")
    assert summary.available_to_unbond_by_symbol["DEL"] == Decimal("7.242864461120814609")
    assert len(summary.unstakes) == 1
    assert summary.unstakes[0].validator_name == "Spacebot"
    assert summary.unstakes[0].amount == Decimal("1")


def test_normalize_wallet_staking_summary_sums_positions_when_total_missing() -> None:
    payload = {
        "items": [
            {
                "validator": "0x3333333333333333333333333333333333333333",
                "items": [
                    {"delegatedCoins": "1000000000000000000", "delegatedBaseCoins": "2500000000000000000", "coin_symbol": "TEST"}
                ],
            }
        ]
    }

    summary = normalize_wallet_staking_summary("0xWallet", payload)

    assert summary.total_del == Decimal("2.5")
    assert summary.positions[0].validator == "0x3333333333333333333333333333333333333333"
    assert summary.positions[0].symbol == "TEST"
    assert summary.positions[0].held_amount == Decimal("0")
    assert summary.positions[0].available_to_unbond == Decimal("1")
    assert summary.positions[0].can_unbond is True


def test_staking_summary_formats_large_raw_values_without_decimal_context_rounding() -> None:
    raw = "123456789012345678901234567890"
    payload = {
        "items": [
            {
                "validator": "0x3333333333333333333333333333333333333333",
                "items": [
                    {
                        "delegatedCoins": raw,
                        "delegatedBaseCoins": raw,
                        "coin_symbol": "DEL",
                    }
                ],
            }
        ]
    }

    summary = normalize_wallet_staking_summary("0xWallet", payload)

    assert summary.positions[0].amount_raw == raw
    assert summary.positions[0].amount == Decimal("123456789012.34567890123456789")


def test_staking_summary_uses_hold_timestamp_not_permit_deadline() -> None:
    payload = {
        "items": [
            {
                "validator": "0x3333333333333333333333333333333333333333",
                "items": [
                    {
                        "delegatedCoins": "100000000000000000000",
                        "delegatedBaseCoins": "100000000000000000000",
                        "symbol": "FRIDAYCOIN",
                        "is_hold": True,
                        "hold_timestamp": 1_787_933_707,
                        "deadline": 1_787_850_912,
                    }
                ],
            }
        ]
    }

    summary = normalize_wallet_staking_summary("0xWallet", payload)

    assert summary.positions[0].holds[0].contract_hold_timestamp == 1_787_933_707
    assert summary.positions[0].holds[0].amount == Decimal("100")


def test_normalize_wallet_stake_withdrawals_reads_pending_unstakes() -> None:
    payload = {
        "Ok": True,
        "Result": {
            "unstakes": [
                {
                    "validator": {"address": "0x2222222222222222222222222222222222222222", "moniker": "Spacebot"},
                    "amount": "1404000000000000000000",
                    "coin": {"symbol": "monolit"},
                    "completion_time": "2026-09-21T00:00:00Z",
                },
                {
                    "validator": {"address": "0x3333333333333333333333333333333333333333", "moniker": "Old"},
                    "amount": "1000000000000000000",
                    "coin": {"symbol": "DEL"},
                    "completion_time": "2026-01-01T00:00:00Z",
                    "is_completed": True,
                },
            ]
        },
    }

    withdrawals = normalize_wallet_stake_withdrawals(
        "0xWallet",
        unstakes_payload=payload,
        now_timestamp=1_787_148_222,
    )

    assert len(withdrawals) == 1
    assert withdrawals[0].validator_name == "Spacebot"
    assert withdrawals[0].symbol == "monolit"
    assert withdrawals[0].amount == Decimal("1404")
    assert withdrawals[0].available_time == "2026-09-21T00:00:00Z"
    assert withdrawals[0].is_completed is False


def test_normalize_wallet_stake_withdrawals_derives_withdraw_with_reset_release() -> None:
    tx_hash = "0x" + "12" * 32
    payload = {
        "data": [
            {
                "tx_hash": tx_hash,
                "transaction_type": "withdraw_with_reset",
                "block": 33232007,
                "timestamp": 1_787_148_222,
                "from_address": "0xddd81a0c34c28eaf7b1377dab8b50c9e859c8e39",
                "token_symbol": "WDEL",
                "amount": "4.21",
                "raw_data": {
                    "validator": "0x8ff2f220fb80b3f26cd96652aecbf3129983c115",
                    "validator_name": "MAKAROVSKY",
                    "hold_timestamps": [1_787_078_776],
                },
            },
            {
                "transaction_type": "simple_transfer",
                "from_address": "0xddd81a0c34c28eaf7b1377dab8b50c9e859c8e39",
                "amount": "1",
            },
        ]
    }

    withdrawals = normalize_wallet_stake_withdrawals(
        "0xDDd81A0c34c28EAf7B1377DAB8B50c9E859C8e39",
        txs_payload=payload,
        now_timestamp=1_787_148_222,
    )

    assert len(withdrawals) == 1
    assert withdrawals[0].tx_hash == tx_hash
    assert withdrawals[0].validator_name == "MAKAROVSKY"
    assert withdrawals[0].symbol == "DEL"
    assert withdrawals[0].amount == Decimal("4.21")
    assert withdrawals[0].available_timestamp == 1_788_444_222
    assert withdrawals[0].available_time == "2026-09-03T14:03:42Z"
