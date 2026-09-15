"""Inventory pinned official source snapshots without executing upstream code.

Optional tooling: tree-sitter==0.25.2, tree-sitter-typescript==0.23.2,
tree-sitter-go==0.25.0. Not needed to install or use the SDK.
"""
from __future__ import annotations

import argparse
from collections import Counter
import hashlib
import json
import runpy
from pathlib import Path
from urllib.request import urlopen

ROOT = Path(__file__).resolve().parents[1]
VERSION = runpy.run_path(str(ROOT / "src/decimal_web3_sdk/_version.py"))["__version__"]
COMMITS = {
    "dsc-js-sdk": "6790d35e2decb0cbb06a9149a9c476c834f99223",
    "dsc-go-sdk": "3ef4a089b6020889e60783c2026df5725fb960e2",
}
FILES = {
    "dsc-js-sdk": ["src/decimalevm/index.ts", "src/decimalevm/call.ts", "src/txTypesNew.ts", "package.json"],
    "dsc-go-sdk": [f"decimalevm/methods/{name}.go" for name in
                   ("del", "tokens", "delegation", "nft", "validators", "multisig")],
}
GROUPS = {
    "del": "sendDEL burnDEL",
    "multisend": "multiSendToken",
    "tokens": "createToken createTokenReserveless convertToken approveToken transferToken transferFromToken burnToken mintTokenReserveless convertToDEL buyTokenForExactDEL buyExactTokenForDEL sellTokensForExactDEL sellExactTokensForDEL updateTokenIdentity updateTokenMaxTotalSupply updateTokenMinTotalSupply permitToken",
    "staking": "delegateDEL delegateDELHold delegateToken delegateTokenHold transferStakeToken transferStakeTokenHold withdrawStakeToken withdrawStakeTokenHold stakeTokenToHold stakeTokenResetHold stakeTokenResetHoldDEL withdrawTokenWithReset transferTokenWithReset holdTokenWithReset applyPenaltyToStakeToken applyPenaltiesToStakeToken completeStakeToken",
    "nft": "createCollectionDRC721 createCollectionDRC1155 createCollectionDRC721Reserveless createCollectionDRC1155Reserveless approveNFT721 approveForAllNFT mintReserveless mintNFTWithDELReserve mintNFTWithTokenReserve addDELReserveNFT addTokenReserveNFT transferNFT transferBatchNFT1155 disableMintNFT burnNFT setTokenURINFT",
    "nft_staking": "delegateNFT delegateNFTHold delegateNFTByPermit withdrawNFT withdrawNFTHold transferNFTStake transferNFTStakeHold delegateNFT1155 delegateNFT1155Hold withdrawNFT1155 withdrawNFT1155Hold transferNFT1155Stake transferNFT1155StakeHold delegateDRC721 delegateDRC721Hold delegateDRC1155 delegateDRC1155Hold transferStakeNFT transferStakeNFTHold withdrawStakeNFT withdrawStakeNFTHold stakeNFTToHold stakeNFTResetHold withdrawNFTWithReset transferNFTWithReset holdNFTWithReset completeStakeNFT",
    "validators": "addValidatorWithToken addValidatorWithETH removeValidator pauseValidator unpauseValidator updateValidatorMeta",
    "checks": "createChecksDEL createChecksToken redeemChecks",
    "bridge": "bridgeTransferNative bridgeTransferTokens bridgeCompleteTransfer",
    "multisig": "createMultiSig approveHashMultiSig executeMultiSigTx",
}

# This is an operation-level map, not a claim of live ABI equivalence.
RELATED = {
    "sendDEL": "tx.send_del", "multiSendToken": "decimal.multisend_del decimal.multisend_erc20",
    "createToken": "token.create", "createTokenReserveless": "token.create_reserveless",
    "convertToken": "token.convert", "approveToken": "tx.approve_erc20",
    "transferToken": "tx.send_erc20", "transferFromToken": "tx.transfer_from_erc20",
    "burnToken": "token.burn", "mintTokenReserveless": "token.mint",
    "buyTokenForExactDEL": "token.buy", "sellExactTokensForDEL": "token.sell",
    "updateTokenIdentity": "token.update_details", "updateTokenMaxTotalSupply": "token.update_details",
    "permitToken": "erc20.sign_permit",
    "delegateDEL": "decimal.delegate_del", "delegateDELHold": "decimal.hold_del",
    "delegateToken": "decimal.delegate_erc20", "delegateTokenHold": "decimal.hold_erc20",
    "transferStakeToken": "decimal.transfer_stake_del decimal.transfer_stake_erc20",
    "transferStakeTokenHold": "decimal.transfer_stake_del decimal.transfer_stake_erc20",
    "withdrawStakeToken": "decimal.unbond_del decimal.unbond_erc20",
    "withdrawStakeTokenHold": "decimal.withdraw_hold_del decimal.withdraw_hold_erc20",
    "stakeTokenToHold": "decimal.stake_token_to_hold", "stakeTokenResetHold": "decimal.reset_stake_hold",
    "stakeTokenResetHoldDEL": "decimal.reset_stake_hold",
    "withdrawTokenWithReset": "decimal.withdraw_stake_with_reset decimal.withdraw_del_stake_with_reset",
    "transferTokenWithReset": "decimal.transfer_stake_with_reset decimal.transfer_del_stake_with_reset",
    "holdTokenWithReset": "decimal.hold_stake_with_reset",
    "createCollectionDRC721": "nft.create_collection", "createCollectionDRC1155": "nft.create_collection",
    "approveNFT721": "nft.approve", "approveForAllNFT": "nft.set_approval_for_all",
    "mintReserveless": "nft.mint", "mintNFTWithDELReserve": "nft.mint", "mintNFTWithTokenReserve": "nft.mint",
    "addDELReserveNFT": "nft.add_del_reserve", "transferNFT": "nft.transfer",
    "transferBatchNFT1155": "nft.transfer_batch_erc1155", "disableMintNFT": "nft.disable_mint",
    "burnNFT": "nft.burn", "setTokenURINFT": "nft.set_token_uri",
    "pauseValidator": "decimal.pause_validator", "unpauseValidator": "decimal.unpause_validator",
    "createChecksDEL": "checks.create_del", "createChecksToken": "checks.create_token", "redeemChecks": "checks.redeem",
    "bridgeTransferNative": "bridge.transfer_native", "bridgeTransferTokens": "bridge.transfer_token",
    "bridgeCompleteTransfer": "bridge.complete_transfer",
}
for names, method in (
    ("delegateNFT delegateNFT1155 delegateDRC721 delegateDRC1155 delegateNFTByPermit", "nft.delegate"),
    ("delegateNFTHold delegateNFT1155Hold delegateDRC721Hold delegateDRC1155Hold", "nft.hold"),
    ("withdrawNFT withdrawNFTHold withdrawNFT1155 withdrawNFT1155Hold withdrawStakeNFT withdrawStakeNFTHold", "nft.withdraw"),
    ("transferNFTStake transferNFTStakeHold transferNFT1155Stake transferNFT1155StakeHold transferStakeNFT transferStakeNFTHold", "nft.transfer_stake"),
):
    RELATED.update({name: method for name in names.split()})
PARTIAL = {
    "multiSendToken": "mixed-assets",
    "buyTokenForExactDEL": "token-selector", "sellExactTokensForDEL": "token-selector",
    "mintTokenReserveless": "token-mint-selector",
    "updateTokenIdentity": "token-update-selector", "updateTokenMaxTotalSupply": "token-update-selector",
    "permitToken": "signature-only",
    "createCollectionDRC721": "nft-collection-selector", "createCollectionDRC1155": "nft-collection-selector",
    "mintNFTWithDELReserve": "nft-del-selector",
    "mintNFTWithTokenReserve": "nft-permit-missing",
}
PARTIAL.update({name: "nft-stake-variants" for name in GROUPS["nft_staking"].split() if name in RELATED})
RELATED.update({
    "burnDEL": "tx.burn_del", "convertToDEL": "token.convert_to_del",
    "buyExactTokenForDEL": "token.buy_exact", "sellTokensForExactDEL": "token.sell_for_exact_del",
    "updateTokenMinTotalSupply": "token.update_min_supply",
    "createCollectionDRC721Reserveless": "nft.create_reserveless_collection",
    "createCollectionDRC1155Reserveless": "nft.create_reserveless_collection",
    "addTokenReserveNFT": "nft.add_token_reserve",
    "applyPenaltyToStakeToken": "decimal.apply_stake_penalty",
    "applyPenaltiesToStakeToken": "decimal.apply_stake_penalties",
    "completeStakeToken": "decimal.complete_stake", "stakeNFTToHold": "nft.stake_to_hold",
    "stakeNFTResetHold": "nft.reset_stake_hold", "withdrawNFTWithReset": "nft.withdraw_with_reset",
    "transferNFTWithReset": "nft.transfer_with_reset", "holdNFTWithReset": "nft.hold_with_reset",
    "completeStakeNFT": "nft.complete_stake",
    "addValidatorWithToken": "decimal.add_validator_token", "addValidatorWithETH": "decimal.add_validator_del",
    "removeValidator": "decimal.remove_validator", "updateValidatorMeta": "decimal.update_validator_metadata",
    "approveHashMultiSig": "multisig.approve_transaction", "executeMultiSigTx": "multisig.execute",
    "createMultiSig": "multisig.create",
})
PARTIAL.update({name: "legacy-explicit-opt-in" for name in (
    "updateTokenMinTotalSupply", "applyPenaltyToStakeToken", "applyPenaltiesToStakeToken",
)})
PARTIAL.update({name: "current-nft-metadata" for name in (
    "createCollectionDRC721Reserveless", "createCollectionDRC1155Reserveless",
)})
GO_ALIASES = {
    "CreateNftCollection": "createCollectionDRC721", "SetApprovalForAllNFT": "approveForAllNFT",
    "MintNFT": "mintReserveless", "ExecuteSafeTransaction": "executeMultiSigTx",
}
GO_HELPERS = {"BuildSafeTransaction", "BuildMultiSigTxSendDEL", "BuildMultiSigTxSendToken",
              "BuildMultiSigTxSendNFT", "SignSafeTransaction"}


def extract(source_dir):
    from tree_sitter import Language, Parser
    import tree_sitter_go
    import tree_sitter_typescript

    parsers = {"dsc-js-sdk": Parser(Language(tree_sitter_typescript.language_typescript())),
               "dsc-go-sdk": Parser(Language(tree_sitter_go.language()))}
    groups = {name: group for group, names in GROUPS.items() for name in names.split()}
    folded = {name.lower(): name for name in groups}
    rows, sources, helpers, excluded = [], [], [], []
    for sdk, paths in FILES.items():
        for path in paths:
            data = (source_dir / sdk / path).read_bytes()
            url = f"https://bitbucket.org/decimalteam/{sdk}/src/{COMMITS[sdk]}/{path}"
            sources.append({"sdk": sdk, "path": path, "sha256": hashlib.sha256(data).hexdigest(), "url": url})
            if path.endswith("call.ts") or path.endswith("txTypesNew.ts") or path.endswith("package.json"):
                continue
            tree = parsers[sdk].parse(data)
            if tree.root_node.has_error:
                raise ValueError(f"Cannot parse {sdk}/{path}")
            if sdk == "dsc-js-sdk":
                export = next(n for n in tree.root_node.children if n.type == "export_statement")
                cls = next(n for n in export.children if n.type == "class_declaration")
                nodes = [n for n in cls.child_by_field_name("body").children if n.type == "method_definition"]
            else:
                nodes = [n for n in tree.root_node.children if n.type == "function_declaration"]
            for node in nodes:
                name = node.child_by_field_name("name").text.decode()
                signature = data[node.start_byte:node.child_by_field_name("body").start_byte].decode()
                if sdk == "dsc-js-sdk":
                    is_write = signature.startswith("public ") and "estimateGas" in signature
                    if name.startswith("buildMultiSig") or name == "signMultiSigTx":
                        helpers.append({"sdk": sdk, "name": name})
                    if name == "multiCall":
                        excluded.append({"sdk": sdk, "name": name, "reason": "generic-executor"})
                        continue
                    if not is_write and name not in GROUPS["multisig"].split():
                        continue
                    canonical = name
                else:
                    if not name[0].isupper():
                        continue
                    if name in GO_HELPERS:
                        helpers.append({"sdk": sdk, "name": name})
                        continue
                    canonical = GO_ALIASES.get(name, folded.get(name.lower(), name))
                if canonical not in groups:
                    raise ValueError(f"Unclassified operation: {sdk}/{name}")
                related = RELATED.get(canonical, "").split()
                reason = PARTIAL.get(canonical)
                if sdk == "dsc-go-sdk" and name == "MintNFT":
                    reason = "nft-standard-mint"
                if sdk == "dsc-go-sdk" and name == "CreateNftCollection":
                    reason = "nft-collection-selector"
                rows.append({"sdk": sdk, "name": name, "group": groups[canonical],
                             "line": node.start_point.row + 1, "path": path,
                             "url": url + f"#lines-{node.start_point.row + 1}",
                             "python": related,
                             "status": "partial" if reason else "counterpart" if related else "missing",
                             "reason": reason or ("network-abi-unverified" if related else "no-typed-method")})
    python_rows = json.loads((ROOT / "docs/transaction-catalog.json").read_text(encoding="utf-8"))
    for row in python_rows:
        if "multisend" in row["method"]:
            row["group"] = "multisend"
        if row["method"] in {"nft.delegate", "nft.hold", "nft.withdraw", "nft.transfer_stake", "nft.stake_to_hold",
                              "nft.reset_stake_hold", "nft.reset_stake_holds", "nft.withdraw_with_reset",
                              "nft.transfer_with_reset", "nft.hold_with_reset", "nft.complete_stake"}:
            row["group"] = "nft_staking"
    return {"checked_on": "2026-09-15", "python_version": VERSION, "commits": COMMITS,
            "release_channel": "prerelease",
            "additional_nft_source": "7dc2e4600ce4aa3dd8baf685d2f31b4f53bc08c7",
            "node_source": "9e6c6d718d662083c4a524376a66d2c50bd4bc77",
            "count_unit": "named high-level EVM write entry points; not unique protocol transaction types",
            "sources": sources, "operations": rows, "python_operations": python_rows,
            "helpers_excluded": helpers, "generic_excluded": excluded,
            "js_legacy_catalog_ids": 42}


def render(report, lang):
    ru = lang == "ru"
    header = "Сравнение С Официальными SDK" if ru else "Official SDK Comparison"
    intro = (
        "Срез исходников на 14.09.2026. Считаются именованные высокоуровневые EVM-методы отправки, "
        "а не уникальные типы протокола и не количество транзакций в блоке. Один workflow может отправить approve и основную транзакцию. "
        "Один Python-метод иногда объединяет несколько JS-методов параметрами; поэтому проценты покрытия из этих чисел считать нельзя."
        if ru else
        "Source snapshot checked on 2026-09-14. Counts are named high-level EVM write entry points, "
        "not unique protocol transaction types or transactions in a block. A workflow may submit approval and a main transaction. "
        "One Python method can combine several JS variants through parameters; these totals are not coverage percentages."
    )
    lines = [f"# {header}", "", "[JSON](../upstream-parity.json) | [Status](status.md)", "", intro, "",
             "| SDK | Commit / version |", "| --- | --- |"]
    for sdk, commit in COMMITS.items():
        lines.append(f"| {sdk} | [{commit[:12]}](https://bitbucket.org/decimalteam/{sdk}/src/{commit}/) |")
    lines += [f"| Python (preview) | {VERSION} |", "", "[Development notes](transaction-parity-development.md)", "",
              "| Group | JS | Go | Python |", "| --- | ---: | ---: | ---: |"]
    counts = {sdk: Counter(row["group"] for row in report["operations"] if row["sdk"] == sdk) for sdk in COMMITS}
    py = Counter(row["group"] for row in report["python_operations"])
    for group in GROUPS:
        lines.append(f"| {group} | {counts['dsc-js-sdk'][group]} | {counts['dsc-go-sdk'][group]} | {py[group]} |")
    lines += [f"| **Total** | **{sum(counts['dsc-js-sdk'].values())}** | **{sum(counts['dsc-go-sdk'].values())}** | **{sum(py.values())}** |", ""]
    lines += [
        "JS: 92 специализированных публичных метода + 3 операции multisig (create, approveHash, executeTx). "
        "Отдельно: 1 generic multiCall, 23 Safe-builder и 1 локальная подпись. "
        "Go: 58 экспортированных функций в methods, из них 53 отправки и 5 builder/sign-helper. "
        f"Python: {len(report['python_operations'])} методов из каталога; generic contract executors, оценки комиссий и чтение исключены. "
        "Дополнительно учтен пакетный сброс NFT-hold из feature-ветки; база JS в этой таблице остается закрепленным master."
        if ru else
        "JS: 92 specialized public methods + 3 multisig writes (create, approveHash, executeTx). "
        "Separately: 1 generic multiCall, 23 Safe builders and 1 local signer. "
        "Go: 58 exported methods-package functions, comprising 53 writes and 5 build/sign helpers. "
        f"Python: {len(report['python_operations'])} catalog methods; generic contract executors, fee estimators and reads are excluded. "
        "The NFT feature-branch batch reset is an extra Python method; the JS baseline remains pinned master.", "",
        "JS также содержит 42 идентификатора legacy-каталога txTypesNew.ts, включая локальное создание чека и EVM-envelope. "
        "Это не 42 дополнительных подтвержденных EVM-операции; в таблицу они не входят. Закомментированный JS mintNFT "
        "и диагностический redeemChecksTest не считаются. В Go проверен пакет decimalevm/methods, не код ноды или Swagger-обертки."
        if ru else
        "JS also declares 42 legacy catalog identifiers in txTypesNew.ts, including local check issuance and the EVM envelope. "
        "These are not 42 additional verified EVM operations and are not in the table. The commented-out JS mintNFT "
        "and diagnostic redeemChecksTest are excluded. Go scope is decimalevm/methods, not node code or Swagger wrappers.", "",
        "## Ограничения Сопоставления" if ru else "## Mapping Limits", "",
        "counterpart = есть типизированный аналог по назначению, но работоспособность текущего ABI в сети не доказана. "
        "partial = аналог неполный или отличается ABI/маршрут. missing = отдельного типизированного аналога нет. "
        "Общий вызов контракта не засчитывается как реализация типа транзакции."
        if ru else
        "counterpart = a typed operation-level counterpart exists, not proof of live ABI compatibility. "
        "partial = incomplete counterpart or different ABI/route. missing = no dedicated typed counterpart. "
        "A generic contract call is not counted as implementing a transaction type.", "",
        "- token-selector: Python buy/sell против JS buyTokenForExactDEL/sellExactTokensForDEL."
        if ru else "- token-selector: Python buy/sell versus JS buyTokenForExactDEL/sellExactTokensForDEL.",
        "- token-update-selector: Python updateDetails против отдельных updateTokenIdentity/updateMaxTotalSupply."
        if ru else "- token-update-selector: Python updateDetails versus separate updateTokenIdentity/updateMaxTotalSupply.",
        "- token-mint-selector: порядок/сигнатура mint требуют отдельной сверки."
        if ru else "- token-mint-selector: mint argument order/signature needs separate reconciliation.",
        "- nft-del-selector: Python mintByETH против mintByDEL upstream; нужен ABI-аудит."
        if ru else "- nft-del-selector: Python mintByETH versus upstream mintByDEL; needs ABI reconciliation.",
        "- nft-collection-selector/nft-stake-variants/nft-standard-mint: типы коллекций и маршруты старой Delegation/DelegationNFT различаются."
        if ru else "- nft-collection-selector/nft-stake-variants/nft-standard-mint: collection types and legacy Delegation/DelegationNFT routes differ.",
        "- mixed-assets: Python разделяет DEL и один ERC20; JS допускает разные активы одним multisend."
        if ru else "- mixed-assets: Python separates DEL and a single ERC20; JS accepts mixed assets in one multisend.",
        "- signature-only: Python sign_permit создает подпись, не отправляет standalone permit; это не аналог отправки PermitToken."
        if ru else "- signature-only: Python sign_permit signs locally rather than sending a standalone permit; not a PermitToken write counterpart.",
        "- nft-permit-missing: mint с токен-резервом есть, полный permit-маршрут отсутствует."
        if ru else "- nft-permit-missing: token-reserve mint exists but the complete permit route is absent.", "",
        "## Приоритетные Пробелы" if ru else "## Priority Gaps", "",
        "Добавленные методы проверены offline, но еще не сетевыми отправками. Остаются прежние частичные "
        "соответствия ABI, permit-варианты и смешанная рассылка. Три legacy-метода требуют явного opt-in; "
        "их нет в проверенных актуальных ABI. У безрезервных NFT текущий ABI использует refundable вместо JS allowMint."
        if ru else
        "New methods have offline checks, not broadcast verification. Existing partial ABI matches, permit variants "
        "and mixed-asset multisend remain. Three legacy methods require explicit opt-in and are absent from the "
        "inspected current ABIs. Reserveless NFT metadata uses the current refundable flag instead of JS allowMint.", "",
    ]
    for sdk in COMMITS:
        lines += [f"## {sdk}", "", "| Method | Python counterpart | Status / reason |", "| --- | --- | --- |"]
        for row in report["operations"]:
            if row["sdk"] == sdk:
                related = ", ".join(f"`{name}`" for name in row["python"]) or "-"
                lines.append(f"| [{row['name']}]({row['url']}) | {related} | {row['status']}: {row['reason']} |")
        lines.append("")
    lines += ["## Reproduce", "", "```shell",
              'python -m pip install "tree-sitter==0.25.2" "tree-sitter-typescript==0.23.2" "tree-sitter-go==0.25.0"',
              "python scripts/compare_upstream.py --fetch", "```", "",
              "Pinned source URLs and SHA256 hashes are stored in the JSON report. Upstream code is parsed, never executed.", ""]
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-dir", type=Path, default=ROOT / "reports/upstream")
    parser.add_argument("--fetch", action="store_true", help="Download pinned official public sources")
    args = parser.parse_args()
    if args.fetch:
        for sdk, paths in FILES.items():
            for path in paths:
                dest = args.source_dir / sdk / path
                dest.parent.mkdir(parents=True, exist_ok=True)
                url = f"https://api.bitbucket.org/2.0/repositories/decimalteam/{sdk}/src/{COMMITS[sdk]}/{path}"
                with urlopen(url, timeout=30) as response:
                    dest.write_bytes(response.read())
    report = extract(args.source_dir)
    (ROOT / "docs/upstream-parity.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
    for lang in ("en", "ru"):
        (ROOT / f"docs/{lang}/upstream-parity.md").write_text(render(report, lang), encoding="utf-8", newline="\n")
    for sdk in COMMITS:
        ops = [row for row in report["operations"] if row["sdk"] == sdk]
        print(sdk, len(ops), dict(Counter(row["group"] for row in ops)))
    print("python", len(report["python_operations"]))


if __name__ == "__main__":
    main()
