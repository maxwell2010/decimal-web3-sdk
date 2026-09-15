# config

[Index](../api.md)

Сигнатуры сформированы из кода релиза. Обязательные поля не имеют значения по умолчанию.

## SystemContracts

Публичная операция/свойство SDK. Ниже приведены точные типы, значения по умолчанию и тип результата; контекст использования дан в руководстве раздела.

```python
SystemContracts(contract_center: 'str' = '0xc108715a06f76caa96fa2c943ebf05159c29a87d', delegation: 'str' = '0xa16c34ed1c0601c0e749e17ebef19752a15faa01', delegation_nft: 'str' = '0xe45adfcc739a0d10ce9462b58866c9a1a06035e2', master_validator: 'str' = '0x630B03FF9EeD4C4A468dA9f481DF23F542070Aa4', nft_center: 'str' = '0x443cc8ac24630be9257483a09c34ffa81608eace', token_center: 'str' = '0x9113ba675aa8f2ef0c068cee2cdabab95b6437fb', wdel: 'str' = '0x1c5d8992da64c8d56ea413dd6f723061c29a7c0b', multicall: 'str' = '0x7b23eb47587ca6482fc16cb3d9d426ec64d4b5fc', del_token: 'str' = '0x16049a46126d69211de7c042465122badefa360c', checks: 'str' = '0x9c3326594b49AFa24db9b988Cda1258d0dcb4e40', gas_center: 'str' = '0xeF21c8573715F9c6b644d209B1E860Dbd2f7A947', safe: 'str' = '0x15949c33775154549D073168C1094C5f3b28b5CB', safe_factory: 'str' = '0x92466f09D5c82e8DdB8AaA7c5AdC63d43111F6c1', multi_send: 'str' = '0x72b80471AAFabd1469ed1C51453DC9ca66068bC0') -> None
```

- `contract_center`: `str`; '0xc108715a06f76caa96fa2c943ebf05159c29a87d'.
- `delegation`: `str`; '0xa16c34ed1c0601c0e749e17ebef19752a15faa01'.
- `delegation_nft`: `str`; '0xe45adfcc739a0d10ce9462b58866c9a1a06035e2'.
- `master_validator`: `str`; '0x630B03FF9EeD4C4A468dA9f481DF23F542070Aa4'.
- `nft_center`: `str`; '0x443cc8ac24630be9257483a09c34ffa81608eace'.
- `token_center`: `str`; '0x9113ba675aa8f2ef0c068cee2cdabab95b6437fb'.
- `wdel`: `str`; '0x1c5d8992da64c8d56ea413dd6f723061c29a7c0b'.
- `multicall`: `str`; '0x7b23eb47587ca6482fc16cb3d9d426ec64d4b5fc'.
- `del_token`: `str`; '0x16049a46126d69211de7c042465122badefa360c'.
- `checks`: `str`; '0x9c3326594b49AFa24db9b988Cda1258d0dcb4e40'.
- `gas_center`: `str`; '0xeF21c8573715F9c6b644d209B1E860Dbd2f7A947'.
- `safe`: `str`; '0x15949c33775154549D073168C1094C5f3b28b5CB'.
- `safe_factory`: `str`; '0x92466f09D5c82e8DdB8AaA7c5AdC63d43111F6c1'.
- `multi_send`: `str`; '0x72b80471AAFabd1469ed1C51453DC9ca66068bC0'.

## NetworkConfig

Публичная операция/свойство SDK. Ниже приведены точные типы, значения по умолчанию и тип результата; контекст использования дан в руководстве раздела.

```python
NetworkConfig(chain_id: 'int' = 75, web3_urls: 'list[str]' = <factory>, rest_urls: 'list[str]' = <factory>, ws_urls: 'list[str]' = <factory>, api_root_url: 'str' = '', api_base_url: 'str' = '', api_fallback_base_urls: 'list[str]' = <factory>, api_key: 'str | None' = None, name: 'str' = 'decimal-mainnet', contracts: 'SystemContracts' = <factory>, safety: 'SafetyLimits' = <factory>, tls_ca_file: 'str | None' = None) -> None
```

- `chain_id`: `int`; 75.
- `web3_urls`: `list[str]`; factory: list.
- `rest_urls`: `list[str]`; factory: list.
- `ws_urls`: `list[str]`; factory: list.
- `api_root_url`: `str`; ''.
- `api_base_url`: `str`; ''.
- `api_fallback_base_urls`: `list[str]`; factory: list.
- `api_key`: `str | None`; None.
- `name`: `str`; 'decimal-mainnet'.
- `contracts`: `SystemContracts`; factory: SystemContracts.
- `safety`: `SafetyLimits`; factory: SafetyLimits.
- `tls_ca_file`: `str | None`; None.

### custom

Публичная операция/свойство SDK. Ниже приведены точные типы, значения по умолчанию и тип результата; контекст использования дан в руководстве раздела.

```python
custom(*, chain_id: 'int' = 75, web3_urls: 'list[str] | None' = None, rest_urls: 'list[str] | None' = None, ws_urls: 'list[str] | None' = None, api_root_url: 'str' = '', api_base_url: 'str' = '', api_fallback_base_urls: 'list[str] | None' = None, api_key: 'str | None' = None, name: 'str' = 'decimal-custom', contracts: 'SystemContracts | None' = None, safety: 'SafetyLimits | None' = None, tls_ca_file: 'str | None' = None) -> "'NetworkConfig'"
```

### devnet

Публичная операция/свойство SDK. Ниже приведены точные типы, значения по умолчанию и тип результата; контекст использования дан в руководстве раздела.

```python
devnet() -> "'NetworkConfig'"
```

### mainnet

Публичная операция/свойство SDK. Ниже приведены точные типы, значения по умолчанию и тип результата; контекст использования дан в руководстве раздела.

```python
mainnet() -> "'NetworkConfig'"
```

### testnet

Публичная операция/свойство SDK. Ниже приведены точные типы, значения по умолчанию и тип результата; контекст использования дан в руководстве раздела.

```python
testnet() -> "'NetworkConfig'"
```
