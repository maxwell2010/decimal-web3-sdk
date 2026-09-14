# client

[Index](../api.md)

Signatures are generated from the release source. Required fields have no default.

## DecimalClient

Decimalclient; types, defaults and return value are specified below.

### address_from_mnemonic

Address from mnemonic; types, defaults and return value are specified below.

```python
async address_from_mnemonic(self, mnemonic: 'str', *, passphrase: 'str' = '', account_path: 'str' = "m/44'/60'/0'/0/0", account_index: 'int | None' = None) -> 'str'
```

### address_from_private_key

Address from private key; types, defaults and return value are specified below.

```python
async address_from_private_key(self, private_key: 'str') -> 'str'
```

### balance_del

Balance del; types, defaults and return value are specified below.

```python
async balance_del(self, address: 'str') -> 'Decimal'
```

### balance_wei

Balance wei; types, defaults and return value are specified below.

```python
async balance_wei(self, address: 'str') -> 'int'
```

### block_number

Block number; types, defaults and return value are specified below.

```python
async block_number(self) -> 'int'
```

### close

Close; types, defaults and return value are specified below.

```python
async close(self) -> 'None'
```

### connect

Connect; types, defaults and return value are specified below.

```python
async connect(self) -> 'bool'
```

### contract_code

Contract code; types, defaults and return value are specified below.

```python
async contract_code(self, address: 'str') -> 'bytes'
```

### contract_code_exists

Contract code exists; types, defaults and return value are specified below.

```python
async contract_code_exists(self, address: 'str') -> 'bool'
```

### estimate_gas

Estimate gas; types, defaults and return value are specified below.

```python
async estimate_gas(self, tx: 'dict') -> 'int'
```

### gas_price

Gas price; types, defaults and return value are specified below.

```python
async gas_price(self) -> 'int'
```

### latest_block_info

Latest block info; types, defaults and return value are specified below.

```python
async latest_block_info(self) -> 'dict'
```

### monitor

Monitor; types, defaults and return value are specified below.

```python
monitor(self, policy: 'TransactionPolicy | None' = None) -> 'DecimalMonitor'
```

### private_key_from_mnemonic

Private key from mnemonic; types, defaults and return value are specified below.

```python
async private_key_from_mnemonic(self, mnemonic: 'str', *, passphrase: 'str' = '', account_path: 'str' = "m/44'/60'/0'/0/0", account_index: 'int | None' = None) -> 'str'
```

### rest_get

Rest get; types, defaults and return value are specified below.

```python
async rest_get(self, path: 'str', **params) -> 'dict'
```

### rest_root_get

Rest root get; types, defaults and return value are specified below.

```python
async rest_root_get(self, path: 'str', **params) -> 'dict'
```

### send_raw_transaction

Broadcast an already signed transaction; spends funds. Read fees and safety guidance first.

```python
async send_raw_transaction(self, raw_tx: 'bytes') -> 'str'
```

### transaction_count

Transaction count; types, defaults and return value are specified below.

```python
async transaction_count(self, address: 'str') -> 'int'
```

### transaction_receipt

Transaction receipt; types, defaults and return value are specified below.

```python
async transaction_receipt(self, tx_hash: 'str') -> 'dict | None'
```

### web3

Web3; types, defaults and return value are specified below.

```python
web3: Web3
```
