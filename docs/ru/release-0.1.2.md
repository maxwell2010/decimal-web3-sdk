# Decimal Web3 SDK 0.1.2

Предварительный релиз GitHub серии 0.1. Python 3.10+, MIT, поддержка Windows/Linux.
[English notes](https://github.com/maxwell2010/decimal-web3-sdk/blob/v0.1.2/docs/en/release-0.1.2.md)

## Изменения
- Исправлена проверка HTTPS/WSS через certifi. Свой CA-файл можно настроить;
  проверка сертификата и имени домена не отключается этим исправлением.
- Добавлены 24 типизированных метода weighted Safe, NFT-стейкинга, валидаторов,
  токенов и стейкинга. Каталог содержит 79 высокоуровневых транзакционных методов.
- Сохранены точные суммы и неподписанный расчет комиссии до локальной подписи.
- Обновлены RU/EN документация, требования установки и сравнение официальных SDK.
- Добавлены постоянная команда обновления pip и проверка отсутствия длинных тире.

## Установка Или Обновление
Git и вход в GitHub не требуются:
```shell
python -m pip install --upgrade -r "https://raw.githubusercontent.com/maxwell2010/decimal-web3-sdk/main/requirements-latest.txt"
```
Команда выбирает последний опубликованный предварительный релиз. Обновление происходит
только при ее запуске. Указатель ведет на версионный wheel, не на изменения разработки.

Для фиксации конкретной версии:
```shell
python -m pip install "https://github.com/maxwell2010/decimal-web3-sdk/releases/download/v0.1.2/decimal_web3_sdk-0.1.2-py3-none-any.whl"
```

## Проверки И Ограничения
Локально проходят 244 офлайн-теста, включая 17 TLS-тестов. Линтер, генерация справочника,
проверка исходников/архивов на секреты и проверка wheel/sdist обязательны перед выпуском.
Рабочие ключи не загружались, транзакции не отправлялись. Mainnet и IPFS HTTPS проверялись
только чтением; testnet был недоступен. Новые операции не подтверждены живыми receipt.
Три legacy-метода требуют opt-in; сохраняются partial-различия ABI/permit.
Это не stable, не полное совпадение с официальными SDK и не публикация в PyPI.

[Ограничения](https://github.com/maxwell2010/decimal-web3-sdk/blob/v0.1.2/docs/ru/status.md)
| [CI](https://github.com/maxwell2010/decimal-web3-sdk/actions/workflows/ci.yml)
| [Документация](https://github.com/maxwell2010/decimal-web3-sdk/blob/v0.1.2/docs/ru/README.md)

Проект [MintCandy](https://mintcandy.ru/), автор [@Maxwell2019](https://t.me/Maxwell2019).
Прежние релизы сохранены. К файлам новой версии приложен SHA256SUMS.
