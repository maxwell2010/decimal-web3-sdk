"""Estimate a DEL transfer without loading credentials, signing or broadcasting."""
import argparse
import asyncio

from decimal_web3_sdk import DecimalClient, NetworkConfig, TransactionDraft, encode_memo_data, format_units_string, parse_units
from decimal_web3_sdk.wallet import checksum


async def run(args):
    owner = checksum(args.address)
    recipient = checksum(args.to or args.address)
    async with DecimalClient(getattr(NetworkConfig, args.network)()) as client:
        tx = {
            "chainId": client.config.chain_id, "from": owner, "to": recipient,
            "value": parse_units(args.amount, 18), "data": encode_memo_data(args.memo),
            "nonce": await client.transaction_count(owner), "gasPrice": await client.gas_price(),
        }
        quote = await client.tx.calculate_fee(TransactionDraft(tx, owner, recipient, tx["value"]), exact=True)
        print("gas_price_gwei:", format_units_string(quote.gas_price_wei, 9))
        print("estimated_fee_del:", format(quote.fee_del, "f"))
        print("gas_limit_budget_del:", format(quote.gas_limit_fee_del, "f"))
        print("enough_balance:", quote.ok)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("address")
    parser.add_argument("--to")
    parser.add_argument("--amount", default="0.000001")
    parser.add_argument("--memo", default="SDK estimate")
    parser.add_argument("--network", choices=("mainnet", "testnet", "devnet"), default="mainnet")
    asyncio.run(run(parser.parse_args()))


if __name__ == "__main__":
    main()
