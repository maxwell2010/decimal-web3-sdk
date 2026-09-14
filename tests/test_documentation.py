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
