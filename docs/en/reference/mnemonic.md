# mnemonic

[Index](../api.md)

Signatures are generated from the release source. Required fields have no default.

## FromMnemonicMixin

Frommnemonicmixin; types, defaults and return value are specified below.

### from_mnemonic

Derive the technical signing key locally; pass request fields as keyword arguments.

```python
from_mnemonic(*, mnemonic: 'str', passphrase: 'str' = '', account_path: 'str' = "m/44'/60'/0'/0/0", account_index: 'int | None' = None, **kwargs) -> 'T'
```
