# Комиссии и Результаты
[Оглавление](README.md) | [API](reference/transactions.md)

Подготовьте черновик, вызовите calculate_fee, проверьте оценку, затем явно
подпишите и отправьте. estimate_fee_for_* не подписывают транзакции.
broadcast=False запрещает отправку, но допускает локальную подпись.
Нельзя писать raw_tx_hex в логи.

## Только Комиссия, Без Сид-Фразы
```python
import asyncio
import os
from decimal_web3_sdk import DecimalClient, NetworkConfig, TransactionDraft, encode_memo_data, parse_units

async def main():
    owner = os.environ["WALLET_ADDRESS"]
    async with DecimalClient(NetworkConfig.testnet()) as client:
        tx = {
            "chainId": client.config.chain_id, "from": owner, "to": owner,
            "value": parse_units("0.000001", 18),
            "data": encode_memo_data("Fee example"),
            "nonce": await client.transaction_count(owner),
            "gasPrice": await client.gas_price(),
        }
        draft = TransactionDraft(tx, owner, owner, tx["value"])
        quote = await client.tx.calculate_fee(draft, exact=True)
        print("estimated DEL:", format(quote.fee_del, "f"))
        print("buffered budget DEL:", format(quote.gas_limit_fee_del, "f"))
        print("enough balance:", quote.ok)

asyncio.run(main())
```

estimate_fee_for_native_transfer и другие типизированные методы принимают
mnemonic-запросы без подписи. Если отдельного метода нет, используйте
build_contract_call с точным ABI calldata и calculate_fee.
Получатели, суммы и memo должны совпадать с будущей отправкой.
Для симуляции может требоваться баланс/allowance; revert не означает нулевую комиссию.

## Поля Оценки
- gas_price_wei: цена единицы gas; для gwei разделите на 10^9.
- estimated_gas: симуляция RPC; gas_limit: лимит с запасом.
- estimated_fee_wei: оценка gas, умноженная на цену.
- gas_limit_fee_wei: бюджет лимита, не обязательно итоговое списание.
- required_wei: value плюс выбранный gas-бюджет.
- native_balance_wei, missing_wei, ok: проверка баланса.

Запас gas-limit по умолчанию 1.10. exact=True выбирает gas без запаса,
сохраняя отдельное поле бюджета с запасом. Итоговое списание не гарантируется:
оракул и состояние сети могут измениться. По умолчанию потолка gasPrice нет.
MAX_GAS_PRICE_* ограничивает начальную цену; при явном minimum-global-fee
возможен один retry по необходимой сети цене.

Approve и основная операция имеют отдельные комиссии, кроме совместимого permit
или достаточного allowance. Dry-run не меняет allowance для второй симуляции.
Оценка только approve НЕ является полной стоимостью workflow.
По умолчанию SDK не отправляет автоматически двухшаговый approve: проверяйте
extra_steps_required и user_message. Для NFT-делегирования требуется уже
выданное разрешение оператору; в проверенном NFT ABI нет permit. Операциям
с нативным DEL approve не нужен.

## Результат
TransactionResult.success описывает шаг SDK; is_successful означает успешный
receipt, is_pending означает отправку без подтверждения. Поля сети:
tx_hash, block_number, gas_used, effective_gas_price_wei, effective_fee_wei,
effective_fee_del. fee_wei/fee_del описывают бюджет отправки.
Явные синонимы: actual_fee_wei/actual_fee_del - фактически списанная
комиссия, fee_budget_wei/fee_budget_del - максимальный бюджет отправки.
actual_fee_del равна None до receipt либо когда сеть не дала надежную цену газа.
При локальной подписи хеша сети нет. Для workflow проверяйте primary,
secondary, transaction_count, total_fee_del, extra_steps_required и оба receipt.
total_fee_del - сумма бюджетов; total_actual_fee_del - фактическая сумма,
которая доступна только после подтверждения всех шагов.

```python
result = await client.decimal.delegate_erc20(request, broadcast=True, wait_receipt=True)
step = result.primary
print("Резерв DEL:", step.fee_budget_del)
print("Списано DEL:", step.actual_fee_del)  # None, если receipt еще не получен
```

Например, при gasLimit 228556 и gasUsed 205011 по цене 1190.475 gwei
резерв равен 0.2720902041 DEL, а фактическая комиссия 0.244060470225 DEL.
Разница не списывается. Эксплорер, умножающий gasLimit на gasPrice,
может ошибочно показать резерв как комиссию.

Правка receipt в обновлении от 2026-09-16: если effectiveGasPrice отсутствует,
для транзакций с фиксированной ценой type 0/1 допустим gasPrice из отправленного
черновика. Для динамической цены (включая type 2) gasPrice/maxFeePerGas может быть
только потолком. Без надежной фактической цены effective_gas_price_wei,
effective_fee_wei и effective_fee_del остаются None, а не нулем. Успешный статус
receipt при этом не меняется. Нельзя подставлять fee_del или maxFeePerGas вместо
фактически списанной комиссии. Правка касается результата, не цены при подписи.

Ожидание по умолчанию: 7 секунд, опрос 3 секунды. Таймаут означает pending,
не неудачу. Показывайте user_message, не публикуйте технический error.
Builders и чтение могут выбрасывать исключения.
Для сумм используйте format(value, "f"), для raw в JSON str(raw_integer):
JavaScript Number не сохраняет произвольный uint256 точно. Нельзя сериализовать
запросы с секретами через asdict или __dict__.
