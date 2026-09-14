# Security

This is a release candidate, not a security-audited wallet. Never use a development
mnemonic with production funds. Review the target chain ID, address, calldata,
value, allowance and complete fee budget before signing or broadcasting.

Requests support `from_mnemonic(...)`: derivation and signing happen locally.
Neither RPC nor REST requests need the mnemonic or private key. Secrets are hidden
from wallet/request repr, but remain accessible as fields. Do not serialize
requests with `asdict`, `__dict__`, pickle or a generic JSON encoder. Do not log
signed transaction bytes or permit/check signatures either.

Use a hidden local prompt or a secret manager. A local `.env` is ignored by Git;
the SDK does not automatically load arbitrary dotenv files on import. Avoid
passing credentials as CLI arguments because process listings and shell history
may record them. Generating a wallet intentionally returns recovery material;
store it securely, offline. Browser/mobile applications must sign on the client
or through a trusted signer, not send seed phrases to an application server.

`broadcast=False` means no broadcast, NOT no signing. `calculate_fee` and the
`estimate_fee_for_*` methods are the unsigned estimation APIs. Permit creation is
also a signature. A network RPC can be unavailable, malicious or on the wrong
chain. The SDK checks configured chain IDs on RPC failover, but cannot establish
operator trust. Treat indexer stake availability as a hint; confirm contract state.

The snapshot/artifact scanner checks likely secrets, mnemonic word runs, private
key blocks, access tokens, IP endpoints and local paths without printing values.
It is a heuristic, not proof of absence. Git history is a separate audit surface:
a clean wheel or branch tip does not erase old commits. Do not make a private
repository public or push its history merely to publish an SDK package. Prefer
the reviewed wheel/sdist or a clean public export.

Report security issues privately to [@Maxwell2019](https://t.me/Maxwell2019).
Do not attach a mnemonic, private key, API credential or signed payload to an issue.
