import json
from collections import Counter
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
REPORT = json.loads((ROOT / "docs/upstream-parity.json").read_text(encoding="utf-8"))


@pytest.mark.parametrize("sdk,count", [("dsc-js-sdk", 95), ("dsc-go-sdk", 53)])
def test_upstream_inventory_has_unique_operations(sdk, count):
    rows = [row for row in REPORT["operations"] if row["sdk"] == sdk]
    assert len(rows) == count
    assert len({row["name"] for row in rows}) == count
    for row in rows:
        assert REPORT["commits"][sdk] in row["url"]
        assert row["status"] in {"counterpart", "partial", "missing"}


def test_python_inventory_matches_current_catalog():
    catalog = json.loads((ROOT / "docs/transaction-catalog.json").read_text(encoding="utf-8"))
    methods = {row["method"] for row in catalog}
    assert {row["method"] for row in REPORT["python_operations"]} == methods
    assert len(methods) == 79
    for row in REPORT["operations"]:
        assert set(row["python"]) <= methods | {"erc20.sign_permit"}


def test_helpers_not_counted_as_writes():
    assert Counter(row["sdk"] for row in REPORT["helpers_excluded"]) == {"dsc-js-sdk": 24, "dsc-go-sdk": 5}
    assert REPORT["generic_excluded"] == [{"sdk": "dsc-js-sdk", "name": "multiCall", "reason": "generic-executor"}]
    assert not any(row["name"] == "mintNFT" for row in REPORT["operations"])


def test_known_abi_differences_are_not_claimed_as_equivalent():
    methods = {row["name"]: row for row in REPORT["operations"] if row["sdk"] == "dsc-js-sdk"}
    for name in ("buyTokenForExactDEL", "sellExactTokensForDEL", "mintNFTWithDELReserve", "permitToken"):
        assert methods[name]["status"] == "partial"
    assert methods["completeStakeNFT"]["status"] == "counterpart"
    for name in ("updateTokenMinTotalSupply", "applyPenaltyToStakeToken", "applyPenaltiesToStakeToken"):
        assert methods[name]["status"] == "partial"
        assert methods[name]["reason"] == "legacy-explicit-opt-in"
    assert methods["addDELReserveNFT"]["status"] == "counterpart"


def test_release_versions_and_github_install_urls_match():
    from decimal_web3_sdk import __version__
    assert REPORT["python_version"] == __version__
    # The development branch must not advertise an unpublished wheel URL.
    assert __version__ == "0.1.2.dev0"
    assert REPORT["unreleased"] is True
    url = "https://github.com/maxwell2010/decimal-web3-sdk/releases/download/v0.1.1/decimal_web3_sdk-0.1.1-py3-none-any.whl"
    for name in ("README.md", "README.ru.md", "docs/en/releasing.md", "docs/ru/releasing.md"):
        assert url in (ROOT / name).read_text(encoding="utf-8")
