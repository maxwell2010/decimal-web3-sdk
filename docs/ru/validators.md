# Валидаторы
[Оглавление](README.md) | [Все примеры валидаторов](transactions/validators.md)
| [API](reference/decimal.md)

validator_status возвращает числовой статус контракта; validator_is_active и
validator_is_member возвращают bool. REST validators/validator и
validator_delegations дают индексированные данные, не права управления.

pause_self_validator/unpause_self_validator относятся к валидатору подписанта.
pause_validator/unpause_validator принимают целевой адрес и требуют полномочий
контракта. Это настоящие действия оператора; тестировать на рабочем валидаторе
нельзя. Во всех примерах отправка отключена.

Создание/удаление валидаторов, изменение метаданных/комиссии, штрафы и полный
набор административных операций не реализованы высокоуровневыми методами.
ContractCallRequest позволяет явно вызвать проверенный ABI, но это не заявление
о протестированном высокоуровневом workflow.
