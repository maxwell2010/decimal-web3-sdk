"""Generate bilingual API signatures and complete transaction examples from the SDK."""
from __future__ import annotations

import ast
import dataclasses
import importlib
import inspect
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
import decimal_web3_sdk as sdk

SERVICES = {"tx": sdk.TransactionService, "decimal": sdk.DecimalService,
            "token": sdk.TokenService, "nft": sdk.NftService,
            "checks": sdk.ChecksService, "bridge": sdk.BridgeService}
DESCRIPTIONS = {
    "send_del": ("Transfer native DEL directly; memo is UTF-8 transaction data, not multicall.", "Прямой перевод DEL; memo записывается в data транзакции, без multicall."),
    "send_erc20": ("Transfer ERC20 tokens from the signer; no approval is needed.", "Перевод ERC20 от подписанта; approve не требуется."),
    "approve_erc20": ("Set a spender allowance; amount zero revokes it.", "Установить лимит расходования для spender; ноль отменяет разрешение."),
    "transfer_from_erc20": ("Transfer tokens using the owner's existing allowance to the signer.", "Перевод токенов владельца по ранее выданному разрешению подписанту."),
    "multisend_del": ("Distribute DEL to recipients in one transaction; no approval. Optional memo.", "Рассылка DEL одной транзакцией без approve, с необязательным memo."),
    "multisend_erc20": ("Distribute ERC20 via multicall; permit or separate approval may be needed. Optional memo.", "Рассылка ERC20 через multicall; при необходимости permit либо отдельный approve. Поддерживается memo."),
    "delegate_del": ("Delegate native DEL to a validator.", "Делегировать DEL валидатору."),
    "delegate_erc20": ("Delegate a reserve token; permission may be needed.", "Делегировать резервный токен; может потребоваться разрешение."),
    "hold_del": ("Delegate DEL with an explicit hold-end Unix timestamp.", "Делегировать DEL в hold с явным временем окончания в Unix-секундах."),
    "hold_erc20": ("Delegate ERC20 with a hold end; permission may be needed.", "Делегировать ERC20 в hold; может потребоваться разрешение."),
    "unbond_del": ("Request withdrawal from the regular DEL stake; this starts unbonding, not immediate payment.", "Инициировать отзыв обычного DEL-стейка; зачисление происходит после unbonding, не сразу."),
    "unbond_erc20": ("Request withdrawal from the regular token stake.", "Инициировать отзыв обычного токен-стейка."),
    "withdraw_hold_del": ("Withdraw a matured DEL hold using its exact hold key.", "Отозвать созревший DEL-hold по точному ключу времени окончания."),
    "withdraw_hold_erc20": ("Withdraw a matured ERC20 hold using its exact hold key.", "Отозвать созревший ERC20-hold по точному ключу времени окончания."),
    "transfer_stake_del": ("Move regular or held DEL stake to another validator.", "Перенести обычный или удерживаемый DEL-стейк другому валидатору."),
    "transfer_stake_erc20": ("Move regular or held token stake to another validator.", "Перенести обычный или удерживаемый токен-стейк другому валидатору."),
    "stake_token_to_hold": ("Move a token stake into a hold with a new end timestamp.", "Перевести токен-стейк в hold с новым сроком окончания."),
    "reset_stake_hold": ("Reset an eligible matured hold for the specified delegator.", "Сбросить доступный созревший hold указанного делегатора."),
    "withdraw_stake_with_reset": ("Reset selected matured token holds and request withdrawal.", "Сбросить выбранные созревшие token-hold и инициировать отзыв."),
    "withdraw_del_stake_with_reset": ("Reset selected matured DEL holds and request withdrawal.", "Сбросить выбранные созревшие DEL-hold и инициировать отзыв."),
    "transfer_stake_with_reset": ("Reset selected token holds and move stake to another validator.", "Сбросить выбранные token-hold и перенести стейк другому валидатору."),
    "transfer_del_stake_with_reset": ("Reset selected DEL holds and move stake to another validator.", "Сбросить выбранные DEL-hold и перенести стейк другому валидатору."),
    "hold_stake_with_reset": ("Reset eligible token holds and create a new hold schedule.", "Сбросить доступные token-hold и установить новый срок hold."),
    "pause_self_validator": ("Pause the signer's validator; requires operator authority.", "Приостановить собственный валидатор; нужны полномочия оператора."),
    "unpause_self_validator": ("Resume the signer's validator; requires operator authority.", "Возобновить работу собственного валидатора; нужны полномочия оператора."),
    "pause_validator": ("Pause a specified validator; requires contract-level authorization.", "Приостановить указанный валидатор; нужны права в контракте."),
    "unpause_validator": ("Resume a specified validator; requires contract-level authorization.", "Возобновить указанный валидатор; нужны права в контракте."),
    "buy": ("Buy reserve tokens with DEL and an explicit minimum output.", "Купить резервный токен за DEL с нижней границей выхода."),
    "sell": ("Sell reserve tokens for DEL with an explicit minimum output.", "Продать резервный токен за DEL с нижней границей выхода."),
    "convert": ("Convert tokens with a minimum output; may use permit or two transactions.", "Обменять токены с минимальным выходом; возможны permit или две транзакции."),
    "token.burn": ("Burn the signer's fungible tokens.", "Сжечь принадлежащие подписанту взаимозаменяемые токены."),
    "token.mint": ("Mint fungible tokens to a recipient; requires issuer rights.", "Выпустить токены получателю; нужны права эмитента."),
    "update_details": ("Update token identity and supply cap; requires issuer rights.", "Обновить identity и предел эмиссии токена; нужны права эмитента."),
    "create_reserveless": ("Create a token without reserve, with mint/burn flags and cap.", "Создать безрезервный токен с флагами выпуска/сжигания и пределом эмиссии."),
    "create": ("Create a reserve token; initial reserve and creation commission are not gas fees.", "Создать резервный токен; начальный резерв и комиссия создания не являются gas-комиссией."),
    "create_collection": ("Create an ERC721 or ERC1155 NFT collection.", "Создать NFT-коллекцию ERC721 или ERC1155."),
    "nft.mint": ("Mint an NFT with optional reserve; requires collection permissions.", "Выпустить NFT с необязательным резервом; нужны права коллекции."),
    "transfer": ("Transfer an ERC721 or ERC1155 NFT to a recipient.", "Передать NFT ERC721 или ERC1155 получателю."),
    "transfer_batch_erc1155": ("Transfer parallel lists of ERC1155 IDs and amounts in one call.", "Передать списки ID и количеств ERC1155 одним вызовом."),
    "set_approval_for_all": ("Grant or revoke an NFT operator's authority for the collection.", "Выдать или отменить полномочия NFT-оператора для коллекции."),
    "approve": ("Approve an operator for a single ERC721 ID.", "Разрешить оператору работу с одним ERC721 ID."),
    "nft.burn": ("Burn owned NFTs; refundable reserves depend on the collection contract.", "Сжечь NFT; возврат резерва зависит от контракта коллекции."),
    "disable_mint": ("Disable collection minting; may be irreversible.", "Отключить выпуск в коллекции; операция может быть необратимой."),
    "set_token_uri": ("Update an NFT metadata URI; requires contract permissions.", "Обновить URI метаданных NFT; нужны права контракта."),
    "add_del_reserve": ("Add native DEL to an NFT reserve.", "Пополнить резерв NFT нативным DEL."),
    "delegate": ("Delegate NFT stake; may require collection operator approval.", "Делегировать NFT; может потребоваться разрешение оператору коллекции."),
    "hold": ("Delegate NFT with a hold end; may require operator approval.", "Делегировать NFT в hold; может потребоваться разрешение оператору."),
    "transfer_stake": ("Move regular or held NFT stake to another validator.", "Перенести обычный или удерживаемый NFT-стейк другому валидатору."),
    "withdraw": ("Request withdrawal of regular or matured held NFT stake.", "Инициировать отзыв обычного или созревшего удерживаемого NFT-стейка."),
    "create_del": ("Create equal-value DEL checks for signer addresses; value is amount times count.", "Создать DEL-чеки одинакового номинала для адресов подписантов; value равен номиналу на число чеков."),
    "create_token": ("Create token checks using existing allowance or an explicitly supplied permit.", "Создать токен-чеки по существующему allowance или явно переданному permit."),
    "redeem": ("Redeem checks using matching check hashes and signatures.", "Погасить чеки по соответствующим хешам и подписям."),
    "transfer_native": ("Start a native bridge transfer; destination completion is a separate workflow.", "Начать мостовой перевод нативной монеты; завершение в целевой сети выполняется отдельно."),
    "transfer_token": ("Start a token bridge transfer; allowance and service fee are caller responsibilities.", "Начать мостовой перевод токена; allowance и сервисную комиссию обеспечивает вызывающий."),
    "complete_transfer": ("Complete a bridge transfer with a verified encoded VM from the bridge.", "Завершить мостовой перевод с проверенным encoded VM, полученным от моста."),
}


def transaction_catalog():
    rows = []
    for service, cls in SERVICES.items():
        for name, fn in inspect.getmembers(cls, inspect.iscoroutinefunction):
            params = inspect.signature(fn).parameters
            if "request" not in params or "broadcast" not in params or name.startswith("_"):
                continue
            request = params["request"].annotation.strip("'\"")
            group = service
            if service == "tx" or name.startswith("multisend"):
                group = "del" if name.endswith("del") else "tokens"
            elif service == "decimal":
                group = "validators" if "validator" in name else "staking"
            elif service == "token":
                group = "tokens"
            key = f"{service}.{name}"
            description = DESCRIPTIONS.get(key, DESCRIPTIONS.get(name))
            if description is None:
                raise ValueError(f"Missing transaction description: {key}")
            rows.append({"method": key, "request": request, "group": group,
                         "en": description[0], "ru": description[1]})
    return rows


def request_arguments(request_name: str) -> dict[str, str]:
    cls = getattr(sdk, request_name)
    values = {}
    for item in dataclasses.fields(cls):
        name = item.name
        if name == "private_key":
            continue
        required = item.default is dataclasses.MISSING and item.default_factory is dataclasses.MISSING
        if not required and name not in {"memo", "auto_approve", "prefer_permit", "permit_deadline"}:
            continue
        if name in {"to", "owner", "delegator", "creator"}:
            value = "wallet.address"
        elif "validator" in name:
            value = f'os.environ["{name.upper()}"]'
        elif name in {"token", "token_in", "token_out", "nft", "contract", "encoded_vm", "identity", "token_uri", "contract_uri", "operator", "spender"}:
            value = f'os.environ["{name.upper()}"]'
        elif name == "recipients":
            recipient = "MultisendRecipient" if request_name == "MultisendDelRequest" else "MultisendErc20Recipient"
            value = f'[{recipient}(wallet.address, "0.000001"), {recipient}(wallet.address, "0.000002")]'
        elif name == "signers":
            value = "[wallet.address]"
        elif name in {"checks", "signatures"}:
            value = f'json.loads(os.environ["{name.upper()}"])'
        elif name in {"hold_timestamps_to_reset"}:
            value = 'json.loads(os.environ["HOLD_TIMESTAMPS_TO_RESET"])'
        elif "hold_timestamp" in name or name == "due_block":
            value = f'int(os.environ["{name.upper()}"])'
        elif name == "permit_deadline":
            value = "int(time.time()) + 600"
        elif name in {"token_ids", "amounts"}:
            value = "[1, 2]" if name == "token_ids" else "[1, 1]"
        elif name in {"amount_del", "amount", "amount_in", "min_amount_out"}:
            value = '"0.000001"'
        elif name.endswith(("_wei", "_raw")):
            value = "1000000000000"
        elif name == "kind":
            value = '"erc721"'
        elif name in {"mintable", "burnable", "approved", "unwrap_weth"}:
            value = "False"
        elif name in {"auto_approve", "prefer_permit"}:
            value = "False"
        elif name in {"nonce", "to_chain_id", "crr", "token_id"}:
            value = f'int(os.environ["{name.upper()}"])'
        elif name == "symbol":
            value = '"EXAMPLE"'
        elif name == "name":
            value = '"Example token"'
        elif name == "memo":
            value = '"SDK example"'
        else:
            raise ValueError(f"Missing example argument: {request_name}.{name}")
        values[name] = value
    return values


def example(row):
    cls = row["request"]
    imports = ["DecimalClient", "NetworkConfig", "mnemonic_to_account", cls]
    if cls == "MultisendDelRequest": imports.append("MultisendRecipient")
    if cls == "MultisendErc20Request": imports.append("MultisendErc20Recipient")
    arguments = "\n".join(f"        {key}={value}," for key, value in request_arguments(cls).items())
    return f'''import asyncio
import getpass
import json
import os
import time
from decimal_web3_sdk import (
    {", ".join(imports)}
)


async def main():
    mnemonic = getpass.getpass("Mnemonic (local, hidden): ")
    wallet = mnemonic_to_account(mnemonic, account_index=0)
    expected = os.environ["EXPECTED_ADDRESS"]
    if wallet.address.lower() != expected.lower():
        raise ValueError("Unexpected signing account")
    request = {cls}.from_mnemonic(
        mnemonic=mnemonic,
        account_index=0,
{arguments}
    )
    async with DecimalClient(NetworkConfig.testnet()) as client:
        # Signs locally when preflight passes. NEVER broadcasts in this example.
        result = await client.{row["method"]}(
            request, broadcast=False, wait_receipt=False
        )
        print("success:", result.success)
        print("fee_DEL:", str(result.fee_del))
        print("message:", result.user_message)
        print("tx_hash:", result.tx_hash)


if __name__ == "__main__":
    asyncio.run(main())
'''


def describe(name, lang):
    if lang == "en":
        if name.startswith("estimate_fee_for_"): return "Estimate gas and balance requirements without signing; RPC simulation may revert."
        if name.startswith("build_"): return "Build transaction data/draft without broadcasting. See units and ABI constraints in the module guide."
        if name == "from_mnemonic": return "Derive the technical signing key locally; pass request fields as keyword arguments."
        if name in {"sign", "permit_signature"}: return "Create a local signature. Treat the returned payload as sensitive; no automatic network broadcast."
        if name in {"broadcast", "broadcast_with_fee_retry", "send_raw_transaction"}: return "Broadcast an already signed transaction; spends funds. Read fees and safety guidance first."
        return (name.replace("_", " ").capitalize() + "; types, defaults and return value are specified below.")
    if name.startswith("estimate_fee_for_"): return "Расчет gas и необходимого баланса без подписи; RPC-симуляция может завершиться revert."
    if name.startswith("build_"): return "Подготовка calldata/черновика без отправки. Единицы и ограничения ABI описаны в руководстве раздела."
    if name == "from_mnemonic": return "Локально получить технический ключ подписи; поля запроса передаются именованными аргументами."
    if name in {"sign", "permit_signature"}: return "Создать локальную подпись без автоматической отправки. Подписанные данные являются чувствительными."
    if name in {"broadcast", "broadcast_with_fee_retry", "send_raw_transaction"}: return "Отправить подписанную транзакцию; расходует средства. Сначала изучите комиссии и ограничения."
    return "Публичная операция/свойство SDK. Ниже приведены точные типы, значения по умолчанию и тип результата; контекст использования дан в руководстве раздела."


def reference(module_name, lang):
    module = importlib.import_module("decimal_web3_sdk." + module_name)
    source = ast.parse(inspect.getsource(module))
    lines = [f"# {module_name}", "", "[Index](../api.md)", "",
             ("Signatures are generated from the release source. Required fields have no default."
              if lang == "en" else "Сигнатуры сформированы из кода релиза. Обязательные поля не имеют значения по умолчанию."), ""]
    entries = []
    for node in source.body:
        if not isinstance(node, (ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef)) or node.name.startswith("_"):
            continue
        obj = getattr(module, node.name)
        entries.append(f"{module_name}.{node.name}")
        lines += [f"## {node.name}", "", describe(node.name, lang), ""]
        if dataclasses.is_dataclass(obj):
            lines += ["```python", node.name + str(inspect.signature(obj)), "```", ""]
            for field in dataclasses.fields(obj):
                default = "required" if field.default is dataclasses.MISSING else repr(field.default)
                if field.default_factory is not dataclasses.MISSING: default = "factory: " + field.default_factory.__name__
                if field.name == "private_key": default = "use from_mnemonic; technical field, hidden in repr"
                lines.append(f"- `{field.name}`: `{field.type}`; {default}.")
            lines.append("")
        elif not inspect.isclass(obj):
            lines += ["```python", ("async " if inspect.iscoroutinefunction(obj) else "") + node.name + str(inspect.signature(obj)), "```", ""]
        if inspect.isclass(obj):
            for name in sorted(set([n.name for n in node.body if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef)) and not n.name.startswith("_")] + (["from_mnemonic"] if hasattr(obj, "from_mnemonic") else []))):
                value = getattr(obj, name)
                entries.append(f"{module_name}.{node.name}.{name}")
                lines += [f"### {name}", "", describe(name, lang), "", "```python"]
                if isinstance(value, property):
                    lines.append(name + ": " + str(inspect.signature(value.fget).return_annotation))
                else:
                    lines.append(("async " if inspect.iscoroutinefunction(value) else "") + name + str(inspect.signature(value)))
                lines += ["```", ""]
    return "\n".join(lines), entries


def generated_files():
    rows = transaction_catalog()
    files = {}
    index = []
    modules = sorted(p.stem for p in (ROOT / "src/decimal_web3_sdk").glob("*.py") if not p.stem.startswith("_") and p.stem != "cli")
    for lang in ("en", "ru"):
        links = ["# API", "", "[Guide](README.md)", ""]
        for module in modules:
            content, entries = reference(module, lang)
            files[f"docs/{lang}/reference/{module}.md"] = content
            links.append(f"- [{module}](reference/{module}.md)")
            if lang == "en": index.extend(entries)
        files[f"docs/{lang}/api.md"] = "\n".join(links) + "\n"
        for group in sorted({row["group"] for row in rows}):
            content = [f"# {group}", "", "[Guide](../README.md)", "",
                       ("Complete examples below use testnet, require EXPECTED_ADDRESS and never broadcast. Other required environment variables appear in each example. They can sign locally; for unsigned fees use the fee guide. Auto-approval is disabled in examples. Contract-dependent methods require compatible deployed code and permissions."
                        if lang == "en" else "Полные примеры ниже используют testnet, требуют EXPECTED_ADDRESS и не отправляют транзакции. Остальные обязательные переменные окружения указаны в коде. Возможна локальная подпись; для расчета без подписи используйте раздел комиссий. Автоматический approve в примерах отключен. Контрактные методы требуют совместимого развернутого контракта и прав."), ""]
            for row in rows:
                if row["group"] != group: continue
                module = SERVICES[row["method"].split(".")[0]].__module__.rsplit(".", 1)[1]
                content += [f"## {row['method']}", "", row[lang], "",
                            f"[{row['request']}](../reference/{module}.md#{row['request'].lower()})", "",
                            "```python", example(row).rstrip(), "```", ""]
            files[f"docs/{lang}/transactions/{group}.md"] = "\n".join(content)
    files["docs/transaction-catalog.json"] = json.dumps(rows, ensure_ascii=False, indent=2) + "\n"
    files["docs/api-index.json"] = json.dumps({"exports": sorted(sdk.__all__), "members": index}, indent=2) + "\n"
    return files


def main():
    check = "--check" in sys.argv
    mismatches = []
    for name, content in generated_files().items():
        path = ROOT / name
        if check:
            if not path.exists() or path.read_text(encoding="utf-8") != content:
                mismatches.append(name)
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding="utf-8", newline="\n")
    if mismatches:
        raise SystemExit("Outdated reference: " + ", ".join(mismatches))
    print(f"API reference: {len(generated_files())} files; {len(transaction_catalog())} transaction entry points")


if __name__ == "__main__":
    main()
