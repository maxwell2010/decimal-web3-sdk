# erc20

[Index](../api.md)

Сигнатуры сформированы из кода релиза. Обязательные поля не имеют значения по умолчанию.

## TokenInfo

Публичная операция/свойство SDK. Ниже приведены точные типы, значения по умолчанию и тип результата; контекст использования дан в руководстве раздела.

```python
TokenInfo(address: 'str', name: 'str | None', symbol: 'str | None', decimals: 'int') -> None
```

- `address`: `str`; required.
- `name`: `str | None`; required.
- `symbol`: `str | None`; required.
- `decimals`: `int`; required.

## TokenBalance

Публичная операция/свойство SDK. Ниже приведены точные типы, значения по умолчанию и тип результата; контекст использования дан в руководстве раздела.

```python
TokenBalance(token: 'TokenInfo', owner: 'str', raw: 'int', formatted: 'Decimal') -> None
```

- `token`: `TokenInfo`; required.
- `owner`: `str`; required.
- `raw`: `int`; required.
- `formatted`: `Decimal`; required.

### as_dict

Публичная операция/свойство SDK. Ниже приведены точные типы, значения по умолчанию и тип результата; контекст использования дан в руководстве раздела.

```python
as_dict(self) -> 'dict[str, object]'
```

### formatted_string

Публичная операция/свойство SDK. Ниже приведены точные типы, значения по умолчанию и тип результата; контекст использования дан в руководстве раздела.

```python
formatted_string: str
```

### raw_string

Публичная операция/свойство SDK. Ниже приведены точные типы, значения по умолчанию и тип результата; контекст использования дан в руководстве раздела.

```python
raw_string: str
```

## PermitSignature

Публичная операция/свойство SDK. Ниже приведены точные типы, значения по умолчанию и тип результата; контекст использования дан в руководстве раздела.

```python
PermitSignature(deadline: 'int', v: 'int', r: 'bytes', s: 'bytes') -> None
```

- `deadline`: `int`; required.
- `v`: `int`; required.
- `r`: `bytes`; required.
- `s`: `bytes`; required.

## Erc20Service

Публичная операция/свойство SDK. Ниже приведены точные типы, значения по умолчанию и тип результата; контекст использования дан в руководстве раздела.

### allowance

Публичная операция/свойство SDK. Ниже приведены точные типы, значения по умолчанию и тип результата; контекст использования дан в руководстве раздела.

```python
async allowance(self, token_address: 'str', owner: 'str', spender: 'str') -> 'int'
```

### balance

Публичная операция/свойство SDK. Ниже приведены точные типы, значения по умолчанию и тип результата; контекст использования дан в руководстве раздела.

```python
async balance(self, token_address: 'str', owner: 'str') -> 'TokenBalance'
```

### build_approve_data

Подготовка calldata/черновика без отправки. Единицы и ограничения ABI описаны в руководстве раздела.

```python
build_approve_data(self, token_address: 'str', spender: 'str', amount_raw: 'int') -> 'str'
```

### build_permit_data

Подготовка calldata/черновика без отправки. Единицы и ограничения ABI описаны в руководстве раздела.

```python
build_permit_data(self, token_address: 'str', owner: 'str', spender: 'str', value_raw: 'int', permit: 'PermitSignature') -> 'str'
```

### build_transfer_data

Подготовка calldata/черновика без отправки. Единицы и ограничения ABI описаны в руководстве раздела.

```python
build_transfer_data(self, token_address: 'str', to: 'str', amount_raw: 'int') -> 'str'
```

### build_transfer_from_data

Подготовка calldata/черновика без отправки. Единицы и ограничения ABI описаны в руководстве раздела.

```python
build_transfer_from_data(self, token_address: 'str', owner: 'str', to: 'str', amount_raw: 'int') -> 'str'
```

### info

Публичная операция/свойство SDK. Ниже приведены точные типы, значения по умолчанию и тип результата; контекст использования дан в руководстве раздела.

```python
async info(self, token_address: 'str') -> 'TokenInfo'
```

### permit_signature

Создать локальную подпись без автоматической отправки. Подписанные данные являются чувствительными.

```python
async permit_signature(self, token_address: 'str', owner: 'str', spender: 'str', value_raw: 'int', deadline: 'int', private_key: 'str') -> 'PermitSignature | None'
```

## format_units_string

Публичная операция/свойство SDK. Ниже приведены точные типы, значения по умолчанию и тип результата; контекст использования дан в руководстве раздела.

```python
format_units_string(value: 'int', decimals: 'int') -> 'str'
```

## format_units

Публичная операция/свойство SDK. Ниже приведены точные типы, значения по умолчанию и тип результата; контекст использования дан в руководстве раздела.

```python
format_units(value: 'int', decimals: 'int') -> 'Decimal'
```

## parse_units

Публичная операция/свойство SDK. Ниже приведены точные типы, значения по умолчанию и тип результата; контекст использования дан в руководстве раздела.

```python
parse_units(value: 'Decimal | str | int', decimals: 'int') -> 'int'
```
