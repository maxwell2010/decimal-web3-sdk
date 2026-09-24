# Decimal Web3 SDK 0.1.3

GitHub preview for Python 3.10+. Testnet contract discovery and token/NFT
transaction compatibility were updated. The SDK now reports both fees and
transaction hashes for two-step token detail updates. A funded testnet campaign
confirmed DEL, ERC20, staking requests, DRC721 and DRC1155 paths.
Permit-compatible workflows remain one transaction; other approvals now require
explicit opt-in rather than an unexpected extra network submission.

This is not a full-parity or security-audited release. Pending stake requests
are not completed withdrawals. See [validation details](../validation/testnet-transaction-campaign-2026-09-24.md)
and [remaining limits](status.md).

Install without Git:

```shell
python -m pip install --upgrade -r "https://raw.githubusercontent.com/maxwell2010/decimal-web3-sdk/main/requirements-latest.txt"
```
