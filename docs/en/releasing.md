# Build and Publish
[Guide](README.md) | [PyPA packaging guide](https://packaging.python.org/en/latest/tutorials/packaging-projects/)

Do not publish a stable version while the gates in status.md remain unresolved.
No script in this repository automatically uploads to PyPI or changes visibility
of a private repository.

## Local Verification
```shell
python -m venv .venv-release
```
Activate that environment, then:
```shell
python -m pip install -e ".[dev]"
python scripts/generate_reference.py --check
python scripts/audit_release.py
python -m pytest -q
python -m ruff check src tests scripts examples
python -m build
python -m twine check dist/*.whl dist/*.tar.gz
python scripts/audit_release.py --dist
python scripts/verify_artifacts.py
```

Build starts from a reviewed, clean snapshot. Do not upload unrelated stale files
from dist. Tests and documentation belong in the sdist for reproducibility; only
runtime code/resources and license metadata belong in the wheel. No dw,
databases, reports with wallets, real dotenv, private keys or local node addresses.

## Install Without Git
Primary distribution is the public GitHub repository `maxwell2010/decimal-web3-sdk`.
After publication, install the pinned wheel without Git:
```shell
python -m pip install "https://github.com/maxwell2010/decimal-web3-sdk/releases/download/v0.1.2/decimal_web3_sdk-0.1.2-py3-none-any.whl"
```
Or install the tagged source archive, also without Git:
```shell
python -m pip install "https://github.com/maxwell2010/decimal-web3-sdk/archive/refs/tags/v0.1.2.zip"
```
See [requirements and dependencies](install.md).

For the latest published preview, use a permanent manifest URL:
```shell
python -m pip install --upgrade -r "https://raw.githubusercontent.com/maxwell2010/decimal-web3-sdk/main/requirements-latest.txt"
```
GitHub's `releases/latest` does not select prereleases. This manifest deliberately
includes our preview channel while referencing an immutable wheel, not source on main.
It updates only when a maintainer publishes a reviewed version. pip does not monitor
releases in the background. Use the pinned command above for controlled deployments.

## Version Policy
The existing tag `v0.1` contains package `0.1.0` and is preserved. This update is
also separate from the preserved `v0.1.1` release. The new version is
package `0.1.2` / tag `v0.1.2` in the requested 0.1 series. `_version.py` is the
single package-version source. Never overwrite published tags or artifacts;
fixes receive a new version and SHA256SUMS. Do not install moving branches for production.
GitHub marks this as a prerelease while the status gates remain open. That flag
does not change PEP 440: package version `0.1.2` has no rc suffix.
Only the reviewed wheel, sdist and SHA256SUMS are attached to a GitHub release.
Public exports must use public repository history, never private Git ancestry.
Verify anonymous downloads and pip installation after publication.

For each release, update `_version.py`, regenerate documentation and
`requirements-latest.txt` with `scripts/generate_reference.py`, then run all checks.
Publish a release branch and wait for CI. Upload the reviewed wheel, sdist and
SHA256SUMS under a new tag. Verify their anonymous availability before advancing
main and its latest manifest. Never point main's manifest at missing release assets.

## Optional PyPI Publication
Choose an unused version in src/decimal_web3_sdk/_version.py, rebuild and verify.
Create/configure the PyPI project and verify that you control the package name.
Prefer PyPI Trusted Publishing; otherwise supply an API token through a secret
manager, never source or command history.
First upload the two reviewed artifacts to TestPyPI with
`python -m twine upload --repository testpypi <wheel> <sdist>`.
After verification, production upload is
`python -m twine upload <wheel> <sdist>`.
These are maintainer actions, not steps executed by this preparation.

Once published, users can install the candidate with
`python -m pip install decimal-web3-sdk==0.1.2`.
Do not advertise that command before the version exists.
Tag only after verification. Keep the original private repository private.
A public source export must be reviewed independently of old private Git history.
