# Сборка и Публикация
[Оглавление](README.md) | [Руководство PyPA](https://packaging.python.org/en/latest/tutorials/packaging-projects/)

Нельзя публиковать stable, пока не закрыты ограничения status.md.
Скрипты не загружают пакет в PyPI и не меняют видимость приватного репозитория.

## Локальная Проверка
```shell
python -m venv .venv-release
```
Активируйте окружение, затем выполните:
```shell
python -m pip install -e ".[dev]"
python scripts/generate_reference.py --check
python scripts/audit_release.py
python -m pytest -q
python -m ruff check src tests scripts examples
python -m build
python -m twine check dist/*.whl dist/*.tar.gz
python scripts/audit_release.py dist/decimal_web3_sdk-0.1.1-py3-none-any.whl dist/decimal_web3_sdk-0.1.1.tar.gz
python scripts/verify_artifacts.py
```

Собирайте проверенный снимок. Не загружайте посторонние старые файлы из dist.
Тесты и документация входят в sdist для воспроизводимости; в wheel только
runtime-код, ресурсы и лицензии. Без dw, баз, отчетов с кошельками, рабочих dotenv,
ключей и адресов собственных узлов.

## Установка Без Git
Основной источник: публичный GitHub `maxwell2010/decimal-web3-sdk`.
После публикации установите wheel конкретной версии без Git:
```shell
python -m pip install "https://github.com/maxwell2010/decimal-web3-sdk/releases/download/v0.1.1/decimal_web3_sdk-0.1.1-py3-none-any.whl"
```
Либо исходный архив по тегу, также без Git:
```shell
python -m pip install "https://github.com/maxwell2010/decimal-web3-sdk/archive/refs/tags/v0.1.1.zip"
```
См. [требования и зависимости](install.md).

## Правила Версий
Существующий тег `v0.1` содержит пакет `0.1.0` и сохраняется. Это обновление:
пакет `0.1.1` / тег `v0.1.1` в запрошенной серии 0.1. Единственный источник
версии пакета: `_version.py`. Опубликованные теги и файлы не заменяются;
исправления получают новую версию и SHA256SUMS. Для эксплуатации фиксируйте версии.
На GitHub релиз отмечается prerelease, пока остаются открытые проверки.
Это не меняет PEP 440: версия пакета `0.1.1` не содержит суффикса rc.
В релиз прикладываются только проверенные wheel, sdist и SHA256SUMS.
Публичный экспорт использует историю публичного репозитория, не приватные коммиты.
После публикации проверяются анонимная загрузка и установка через pip.

## Отдельная Публикация В PyPI
Выберите свободную версию в src/decimal_web3_sdk/_version.py, пересоберите
и проверьте пакет. Настройте проект PyPI и права на имя пакета.
Предпочтительна Trusted Publishing; иначе токен только через менеджер секретов,
не исходники и не историю команд.
Сначала загрузите два проверенных файла в TestPyPI:
`python -m twine upload --repository testpypi <wheel> <sdist>`.
После проверки production-загрузка:
`python -m twine upload <wheel> <sdist>`.
В этой подготовке эти команды не исполняются.

После публикации пользователи смогут выполнить
`python -m pip install decimal-web3-sdk==0.1.1`.
Не рекламируйте команду до появления версии в индексе.
Тег создается после проверки. Исходный приватный репозиторий остается приватным;
публичный экспорт проверяется отдельно от старой приватной истории Git.
