"""Versioned unsigned contract-call bridge shared with CandyConsole.

No private key, signer, HTTP call or broadcast is accepted by this module.
Consumers must do fresh chain/owner/balance checks and gas estimation before
asking their wallet to sign. Existing token.py/nft.py workflows are unchanged.
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from web3 import Web3


def load_candy_profile() -> dict[str, Any]:
    path = Path(__file__).with_name("profiles") / "candy_mainnet_v1.json"
    return json.loads(path.read_text(encoding="utf-8"))


def build_unsigned_candy_burn(
    *, owner: str, amount_base: int, token_address: str | None = None,
    chain_id: int = 75,
) -> dict[str, Any]:
    """Explicit irreversible burn: native DEL to zero, ERC20 burn(uint256).

    No approval, swap, arbitrary recipient, signing or broadcast. token_address
    omitted means native DEL, NOT WDEL. Validate live balance, token support and
    gas before asking the user to confirm. Amount is an integer in base units.
    """
    if isinstance(amount_base, bool) or not isinstance(amount_base, int) or not 0 < amount_base < 2**256:
        raise ValueError("amount_base must be a positive uint256")
    if token_address is not None:
        return build_unsigned_candy_call(owner=owner, contract_type="token", address=token_address,
                                         signature="burn(uint256)", args=[amount_base], chain_id=chain_id)
    profile = load_candy_profile()
    if chain_id != profile["chainId"] or not Web3.is_address(owner) or int(owner, 16) == 0:
        raise ValueError("Decimal Mainnet and a nonzero sender are required")
    return {"chainId": chain_id, "from": Web3.to_checksum_address(owner),
            "to": profile["nativeBurnAddress"], "data": "0x", "value": str(amount_base)}


def build_unsigned_candy_call(
    *, owner: str, contract_type: str, signature: str,
    args: list[Any], address: str | None = None, value_wei: int = 0,
    chain_id: int = 75,
) -> dict[str, Any]:
    """Encode an allowlisted ABI method. Amounts are integers in base units.

    `owner` is only an asserted sender, NOT proof of authority. The caller must
    authenticate the signing wallet and verify chain 75 before submission.
    Returns JSON-safe strings for uint256 value; never signs a transaction.
    """
    profile = load_candy_profile()
    if chain_id != profile["chainId"]:
        raise ValueError("This reviewed protocol profile is Decimal Mainnet only")
    if contract_type not in profile["abi"]:
        raise ValueError("Unsupported contract type")
    target = profile.get(contract_type) if contract_type in {"tokenCenter", "nftCenter", "nftDelegation"} else address
    if not target or not Web3.is_address(target) or int(target, 16) == 0:
        raise ValueError("A nonzero contract address is required")
    if address and contract_type in {"tokenCenter", "nftCenter", "nftDelegation"} and address.lower() != target.lower():
        raise ValueError("Cannot override a reviewed system contract")
    if not Web3.is_address(owner) or int(owner, 16) == 0:
        raise ValueError("A nonzero sender address is required")
    if isinstance(value_wei, bool) or not isinstance(value_wei, int) or not 0 <= value_wei < 2**256:
        raise ValueError("value_wei must be uint256")
    contract = Web3().eth.contract(address=Web3.to_checksum_address(target), abi=profile["abi"][contract_type])
    fn = contract.get_function_by_signature(signature)
    if fn.abi.get("stateMutability") not in {"payable", "nonpayable"}:
        raise ValueError("Use the SDK read API for view methods")
    if value_wei and fn.abi["stateMutability"] != "payable":
        raise ValueError("Cannot attach DEL to a nonpayable method")
    return {"chainId": chain_id, "from": Web3.to_checksum_address(owner),
            "to": contract.address, "data": fn(*args)._encode_transaction_data(), "value": str(value_wei)}
