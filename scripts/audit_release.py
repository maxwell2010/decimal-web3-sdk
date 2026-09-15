"""Audit the release snapshot and archives without printing matched secret values."""
from __future__ import annotations

import argparse
import ast
import ipaddress
import re
import subprocess
import tarfile
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SECRET_NAME = re.compile(r"private.?key|mnemonic|seed|api.?key|password|secret", re.I)
HEX_SECRET = re.compile(r"(?:0x)?[a-fA-F0-9]{64}\Z")
LOCAL_PATH = re.compile(r"(?:[A-Z]:[/\\](?:Users|home|Projects)[/\\]|/" + r"home/[^\s/]+/)", re.I)
IP_URL = re.compile(r"https?://((?:\d{1,3}\.){3}\d{1,3})(?=[:/\s]|$)")
FORBIDDEN = {".env", ".git", ".idea", "__pycache__", "node_modules", "dw", "reports", "backups"}


def scan_text(name: str, source: str) -> list[str]:
    findings = []
    for number, line in enumerate(source.splitlines(), 1):
        if LOCAL_PATH.search(line):
            findings.append(f"{name}:{number}: local path")
        for match in IP_URL.finditer(line):
            try:
                ipaddress.ip_address(match.group(1))
            except ValueError:
                continue
            findings.append(f"{name}:{number}: literal IP endpoint")
        if re.search(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----", line):
            findings.append(f"{name}:{number}: private key block")
        if re.search(r"\b(?:gh[pousr]_[A-Za-z0-9]{30,}|github_pat_[A-Za-z0-9_]{40,})\b", line):
            findings.append(f"{name}:{number}: access token")
        if SECRET_NAME.search(line):
            if re.search(r"[\"'](?:0x)?[a-fA-F0-9]{64}[\"']", line):
                findings.append(f"{name}:{number}: embedded credential")
    try:
        from eth_account.hdaccount import Mnemonic
        from eth_account.types import Language
        words = set(Mnemonic(Language.ENGLISH).wordlist)
    except (ImportError, AttributeError):
        raise RuntimeError("Install development dependencies before the secret scan") from None
    # Check word runs in any text, not just Python assignments.
    run = []
    for match in re.finditer(r"[a-z]+|[^a-z\s]", source.lower()):
        word = match.group()
        if word in words:
            run.append(word)
            if len(run) >= 12:
                findings.append(f"{name}: possible mnemonic word sequence")
                break
        else:
            run = []
    if name.endswith(".py"):
        try:
            tree = ast.parse(source)
        except SyntaxError:
            findings.append(f"{name}: invalid Python syntax")
        else:
            for node in ast.walk(tree):
                if isinstance(node, ast.Constant) and isinstance(node.value, str):
                    if HEX_SECRET.fullmatch(node.value):
                        # Hashes/selectors are not keys. Review new long literals explicitly.
                        findings.append(f"{name}:{node.lineno}: 32-byte literal requires review")
    return sorted(set(findings))


def snapshot() -> list[tuple[str, bytes]]:
    output = subprocess.check_output(
        ["git", "ls-files", "--cached", "--others", "--exclude-standard", "-z"], cwd=ROOT
    )
    return [(name, (ROOT / name).read_bytes())
            for name in sorted(set(output.decode().split("\0")))
            if name and (ROOT / name).is_file()]


def archive(path: Path) -> list[tuple[str, bytes]]:
    if path.suffix == ".whl":
        with zipfile.ZipFile(path) as handle:
            return [(name, handle.read(name)) for name in handle.namelist() if not name.endswith("/")]
    with tarfile.open(path, "r:gz") as handle:
        return [(item.name, handle.extractfile(item).read()) for item in handle if item.isfile()]


def audit(items: list[tuple[str, bytes]]) -> list[str]:
    findings = []
    for name, content in items:
        parts = Path(name).parts
        if any(part in FORBIDDEN or (part.startswith(".env.") and part != ".env.example") for part in parts):
            findings.append(f"{name}: forbidden release file")
        if name.endswith((".pyc", ".key", ".pem", ".p12", ".db", ".sqlite", ".log")):
            findings.append(f"{name}: forbidden release extension")
        try:
            source = content.decode("utf-8-sig")
        except UnicodeDecodeError:
            findings.append(f"{name}: binary file requires review")
            continue
        findings.extend(scan_text(name, source))
    return findings


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("archives", nargs="*", type=Path)
    parser.add_argument("--dist", action="store_true", help="Audit both artifacts for the current package version")
    args = parser.parse_args()
    if args.dist:
        version_tree = ast.parse((ROOT / "src/decimal_web3_sdk/_version.py").read_text(encoding="utf-8"))
        version = ast.literal_eval(version_tree.body[0].value)
        args.archives.extend([
            ROOT / "dist" / f"decimal_web3_sdk-{version}-py3-none-any.whl",
            ROOT / "dist" / f"decimal_web3_sdk-{version}.tar.gz",
        ])
    collections = [("snapshot", snapshot())] + [(str(path.name), archive(path)) for path in args.archives]
    failed = False
    for label, items in collections:
        findings = audit(items)
        print(f"{label}: {len(items)} files, {len(findings)} findings")
        for finding in findings:
            print(finding)
        failed |= bool(findings)
    raise SystemExit(1 if failed else 0)


if __name__ == "__main__":
    main()
