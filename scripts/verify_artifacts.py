"""Verify wheel/sdist contents and metadata; write local SHA256 checksums."""
import ast
import hashlib
import tarfile
import zipfile
from email.parser import BytesParser
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main():
    tree = ast.parse((ROOT / "src/decimal_web3_sdk/_version.py").read_text(encoding="utf-8"))
    version = ast.literal_eval(tree.body[0].value)
    wheel = ROOT / "dist" / f"decimal_web3_sdk-{version}-py3-none-any.whl"
    sdist = ROOT / "dist" / f"decimal_web3_sdk-{version}.tar.gz"
    expected = {"decimal_web3_sdk/" + str(path.relative_to(ROOT / "src/decimal_web3_sdk")).replace("\\", "/")
                for path in (ROOT / "src/decimal_web3_sdk").rglob("*")
                if path.is_file() and path.suffix in {".py", ".json", ".md"}}
    with zipfile.ZipFile(wheel) as handle:
        names = set(handle.namelist())
        assert expected <= names, "Wheel is missing runtime resources"
        assert all(name.startswith(("decimal_web3_sdk/", f"decimal_web3_sdk-{version}.dist-info/")) for name in names)
        metadata = BytesParser().parsebytes(handle.read(f"decimal_web3_sdk-{version}.dist-info/METADATA"))
        assert metadata["Name"] == "decimal-web3-sdk"
        assert metadata["Version"] == version
        assert metadata["License-Expression"] == "MIT"
        assert metadata["Requires-Python"] == ">=3.10"
        assert set(metadata.get_all("License-File")) == {"LICENSE", "THIRD_PARTY_NOTICES.md"}
        for name in expected:
            relative = name.removeprefix("decimal_web3_sdk/")
            assert handle.read(name) == (ROOT / "src/decimal_web3_sdk" / relative).read_bytes(), name
    with tarfile.open(sdist, "r:gz") as handle:
        names = {item.name.split("/", 1)[1] for item in handle if "/" in item.name and item.isfile()}
        for name in ("README.md", "README.ru.md", "LICENSE", "THIRD_PARTY_NOTICES.md", "pyproject.toml",
                     "docs/en/README.md", "docs/ru/README.md", "scripts/generate_reference.py", "tests/test_transaction_catalog.py"):
            assert name in names, name
        assert all(not any(part in {".git", ".env", "dw", ".idea", "node_modules", "reports"} for part in Path(name).parts) for name in names)
    checksums = "".join(f"{hashlib.sha256(path.read_bytes()).hexdigest()}  {path.name}\n" for path in (wheel, sdist))
    (ROOT / "dist/SHA256SUMS").write_text(checksums, encoding="ascii")
    print(f"Verified {len(expected)} runtime files, wheel/sdist metadata, documentation and licenses")
    print(checksums)


if __name__ == "__main__":
    main()
