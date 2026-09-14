# Нативный DEL
[Оглавление](README.md) | [Полные примеры DEL](transactions/del.md)

client.balance_wei возвращает int, balance_del возвращает точный Decimal.
NativeTransferRequest.from_mnemonic принимает to, amount_del и необязательные
memo, gas, gas_price_wei. send_del использует прямой EVM value/data;
UTF-8 memo не превращает перевод в multicall.

MultisendDelRequest содержит непустой список MultisendRecipient(to, amount_del).
В multicall кодируются весь список и необязательное сообщение.
Нативный DEL никогда не требует approve или permit.
Мультисенд одному получателю может быть прямым переводом.
Поддержку memo проверяйте через memo_capabilities()/memo_supported_for().

До подписи используйте estimate_fee_for_native_transfer или
estimate_fee_for_multisend_del. Они учитывают реальное сообщение и получателей.
SDK не добавляет рекламное memo по умолчанию. Не путайте адрес токена и DEL.
Суммы задаются точными строками или Decimal; raw-числа в JSON передавайте строками.
