# Токены
[Оглавление](README.md) | [Все примеры транзакций](transactions/tokens.md)
| [ERC20 API](reference/erc20.md) | [Token API](reference/token.md)

Чтение ERC20: info(address) возвращает name/symbol/decimals; balance(token, owner)
возвращает TokenBalance с raw/formatted и точным as_dict();
allowance(token, owner, spender) возвращает лимит в минимальных единицах.
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
auto_approve=False передает управление разрешением приложению;
prefer_permit управляет выбором permit. Задавайте короткий permit_deadline.

Прямой ERC20 transfer не принимает memo, ERC20 multisend принимает.
DEL не требует разрешения. Не все exact-in/out варианты, setters и калькуляторы
резерва реализованы: [границы покрытия](status.md).
