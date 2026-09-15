import ast
import re
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).parents[1]


def test_markdown_links_and_python_examples():
    files = [ROOT / "README.md", ROOT / "README.ru.md", *ROOT.glob("docs/**/*.md")]
    for path in files:
        text = path.read_text(encoding="utf-8")
        for target in re.findall(r"\]\(([^)]+)\)", text):
            parsed = urlsplit(target)
            if parsed.scheme or not parsed.path:
                continue
            assert (path.parent / unquote(parsed.path)).exists(), (path, target)
        if "reference" not in path.parts:
            for example in re.findall(r"```python\n(.*?)```", text, re.S):
                ast.parse(example)


def test_bilingual_guides_have_same_sections():
    en = {path.relative_to(ROOT / "docs/en") for path in (ROOT / "docs/en").rglob("*.md")}
    ru = {path.relative_to(ROOT / "docs/ru") for path in (ROOT / "docs/ru").rglob("*.md")}
    assert en == ru


def test_documentation_uses_ascii_hyphens():
    files = [*ROOT.glob("*.md"), *ROOT.glob("docs/**/*.md"),
             *ROOT.glob("src/**/*.py"), *ROOT.glob("scripts/*.py"), ROOT / "pyproject.toml"]
    long_dashes = {chr(code) for code in (0x2013, 0x2014, 0x2015)}
    for path in files:
        assert not long_dashes.intersection(path.read_text(encoding="utf-8")), path


def test_latest_install_manifest_is_versioned_and_documented():
    from decimal_web3_sdk import __version__

    manifest = (ROOT / "requirements-latest.txt").read_text(encoding="utf-8")
    requirements = [line for line in manifest.splitlines() if line and not line.startswith("#")]
    assert requirements == [
        "decimal-web3-sdk @ https://github.com/maxwell2010/decimal-web3-sdk/releases/download/"
        f"v{__version__}/decimal_web3_sdk-{__version__}-py3-none-any.whl"
    ]
    command = ('python -m pip install --upgrade -r '
               '"https://raw.githubusercontent.com/maxwell2010/decimal-web3-sdk/main/requirements-latest.txt"')
    for name in ("README.md", "README.ru.md", "docs/en/install.md", "docs/ru/install.md"):
        assert command in (ROOT / name).read_text(encoding="utf-8"), name
