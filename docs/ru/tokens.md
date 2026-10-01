# Токены
[Оглавление](README.md) | [Все примеры транзакций](transactions/tokens.md)
| [ERC20 API](reference/erc20.md) | [Token API](reference/token.md)

Чтение ERC20: info(address) возвращает name/symbol/decimals; balance(token, owner)
возвращает TokenBalance с raw/formatted и точным as_dict();
allowance(token, owner, spender) возвращает лимит в минимальных единицах.
`client.token.properties(token)` читает свойства резервного или безрезервного
контракта. Для резервного токена возвращаются `creator`, `min_total_supply_raw`
и `max_total_supply_raw`; минимальная эмиссия - порог погашения и может быть
больше текущего `total_supply_raw`. Для безрезервного токена возвращаются
`owner`, `cap_raw`, `mintable` и `burnable`; `uint256.max` в `cap_raw` означает
отсутствие ограничения (`unlimited_cap=True`). `owner` отражает текущие права,
а не обязательно исторического создателя. `as_dict()` сохраняет все суммы
строками, без `float`.

```python
properties = await client.token.properties(token_address)
balance = await client.erc20.balance(token_address, wallet_address)
print(properties.as_dict()["total_supply"]["raw"])  # эмиссия, не баланс
print(balance.raw_string)                         # доступно кошельку
```

Для поиска полученных безрезервных токенов требуется перечень адресов контрактов
из каталога сети; SDK не выводит владение из `creator` или `totalSupply`.
Неудачный RPC-запрос или ошибка чтения `decimals()` не означают нулевой баланс.
Изменение `identity` у существующего безрезервного токена не гарантируется:
вызывайте setter только после проверки ABI конкретной реализации.
build_transfer_data, build_transfer_from_data, build_approve_data,
build_permit_data только кодируют ABI. permit_signature создает типизированную
подпись EIP-2612, не транзакцию сети. Одного наличия nonces недостаточно для
гарантии permit: нестандартные domain/version/варианты требуют проверки.

Доступны transfer, transferFrom, approve, multisend, покупка/продажа/обмен
резервных токенов, burn, mint, обновление данных и создание токенов.
Правила создания и расчет начального резерва являются снимком; сверяйте их
с действующим контрактом. Резерв и комиссия создания не равны gas-комиссии.
min_amount_out и min_amount_del_out_wei ограничивают проскальзывание.
Выпуск, метаданные и лимиты эмиссии обычно требуют прав эмитента.

Достаточный allowance избавляет от нового approve. Совместимый permit позволяет
совместить разрешение и основную операцию, в том числе multisend с memo.
Обычный approve внутри multicall не выдает разрешение от кошелька:
msg.sender будет контрактом multicall. Отдельная комиссия approve должна быть видна.
auto_approve=False теперь значение по умолчанию для мультисенда, конвертации
и делегирования. Если permit нет и allowance недостаточен, SDK вернет
extra_steps_required без отправки approve. Только явный auto_approve=True
разрешает два шага; при отправке нужен wait_receipt=True.
prefer_permit управляет выбором permit. Задавайте короткий permit_deadline.

Прямой ERC20 transfer не принимает memo, ERC20 multisend принимает.
DEL не требует разрешения. Не все exact-in/out варианты, setters и калькуляторы
резерва реализованы: [границы покрытия](status.md).
