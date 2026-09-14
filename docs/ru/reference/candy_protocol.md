# candy_protocol

[Index](../api.md)

Сигнатуры сформированы из кода релиза. Обязательные поля не имеют значения по умолчанию.

## load_candy_profile

Публичная операция/свойство SDK. Ниже приведены точные типы, значения по умолчанию и тип результата; контекст использования дан в руководстве раздела.

```python
load_candy_profile() -> 'dict[str, Any]'
```

## build_unsigned_candy_burn

Подготовка calldata/черновика без отправки. Единицы и ограничения ABI описаны в руководстве раздела.

```python
build_unsigned_candy_burn(*, owner: 'str', amount_base: 'int', token_address: 'str | None' = None, chain_id: 'int' = 75) -> 'dict[str, Any]'
```

## build_unsigned_candy_call

Подготовка calldata/черновика без отправки. Единицы и ограничения ABI описаны в руководстве раздела.

```python
build_unsigned_candy_call(*, owner: 'str', contract_type: 'str', signature: 'str', args: 'list[Any]', address: 'str | None' = None, value_wei: 'int' = 0, chain_id: 'int' = 75) -> 'dict[str, Any]'
```
