#!/usr/bin/env python3
"""Build deterministic census ledgers for Security Audit audits.

The script is intentionally heuristic. It does not decide exploitability.
It creates the complete work queue that the audit must triage.
"""
from __future__ import annotations

import argparse
import hashlib
import os
import re
from dataclasses import dataclass
from pathlib import Path

EXCLUDED_DIRS = {
    ".git",
    ".hg",
    ".svn",
    ".next",
    ".nuxt",
    ".turbo",
    ".venv",
    "venv",
    "env",
    "__pycache__",
    "node_modules",
    "vendor",
    "dist",
    "build",
    "coverage",
    ".cache",
}

TEXT_EXTS = {
    ".py", ".pyi", ".js", ".jsx", ".mjs", ".cjs", ".ts", ".tsx", ".mts", ".cts",
    ".go", ".rb", ".php", ".java", ".kt", ".kts", ".rs", ".c", ".cc", ".cpp", ".h", ".hpp",
    ".cs", ".swift", ".scala", ".sh", ".bash", ".zsh", ".ps1", ".yml", ".yaml", ".json",
    ".toml", ".ini", ".cfg", ".conf", ".env", ".dockerfile", ".tf", ".tfvars", ".md",
    ".sql", ".graphql", ".gql", ".xml", ".html", ".css", ".scss", ".liquid",
}

PATTERNS: dict[str, list[tuple[str, re.Pattern[str]]]] = {
    "file_io": [
        ("file read/write/delete/copy/rename", re.compile(r"\b(readFile|writeFile|appendFile|createReadStream|createWriteStream|openSync|readFileSync|writeFileSync|copyFile|rename|unlink|rmSync|mkdir|ensureDir|sendFile|serveStatic|fileServerMiddleware)\b")),
    ],
    "path": [
        ("path construction / containment", re.compile(r"\b(joinPath|resolvePath|relativePath|normalize|path\.join|path\.resolve|startsWith|realpath|dirname|basename)\b")),
    ],
    "route": [
        ("route / middleware / request parameter", re.compile(r"\b(defineEventHandler|createRouter|router\.use|app\.(get|post|put|patch|delete)|loader\s*=|action\s*=|getRouterParams|getQuery|params|request\.json|request\.formData|req\.query|req\.params|Access-Control-Allow-Origin)\b")),
    ],
    "api_field": [
        ("API or remote-controlled field", re.compile(r"\b(ThemeAsset|asset\.key|fetchThemeAssets|response|remote|api|download|sync|pull|filename|fileName|remotePath|checksum|entry\.name|archive|key)\b", re.I)),
    ],
    "subprocess": [
        ("subprocess / shell / tool invocation", re.compile(r"\b(execSync|execFileSync|execFile|exec\(|spawn\(|spawnSync|execa|child_process|subprocess|Popen|os\.system|shell=True|sh -c)\b")),
    ],
    "secrets": [
        ("secret/token/key/password material", re.compile(r"\b(SECRET|TOKEN|API_KEY|PRIVATE_KEY|PASSWORD|Authorization|Bearer|accessToken|refreshToken|client_secret|signingSecret|github_token|GH_TOKEN|GITHUB_TOKEN)\b", re.I)),
        ("logging / output sink", re.compile(r"\b(console\.(log|error|warn|debug)|outputDebug|logger\.(info|debug|warn|error)|print\(|stdout|stderr)\b")),
    ],
    "network": [
        ("network fetch / download / upload", re.compile(r"\b(fetch\(|axios\.|request\(|httpx\.|requests\.|aiohttp|urllib|urlopen|curl|wget|download|upload|presigned|signed_url)\b")),
    ],
    "auth": [
        ("auth / session / identity", re.compile(r"\b(authenticate|authorize|verifyHmac|verify|sessionStorage|session|tenant|organization|userId|shop|accessToken|refreshToken|jwt|cookie|csrf|hmac|timingSafeEqual)\b", re.I)),
    ],
    "deserialize_archive": [
        ("deserialization / parse / archive", re.compile(r"\b(JSON\.parse|yaml\.load|YAML\.load|pickle\.load|pickle\.loads|cloudpickle|joblib\.load|torch\.load|np\.load|allow_pickle|deserialize|unserialize|tar|unzip|extract|extractall|gunzip|inflate)\b")),
    ],
    "crypto": [
        ("crypto / key / signature / randomness", re.compile(r"\b(crypto|createHash|createHmac|createCipheriv|createDecipheriv|randomBytes|Math\.random|AES|RSA|ECDSA|HMAC|sign\(|verify\(|jwt|bcrypt|scrypt|pbkdf2)\b", re.I)),
    ],
}

DISPOSITIONS = {
    "untriaged",
    "promoted",
    "false-positive",
    "hardening",
    "expected-behavior",
    "fixed",
    "out-of-scope",
    "blocked",
}


@dataclass(frozen=True)
class Hit:
    category: str
    file: str
    line: int
    signal: str
    snippet: str

    @property
    def key(self) -> tuple[str, str, int, str]:
        return (self.category, self.file, self.line, self.signal)


def is_excluded(path: Path, root: Path) -> bool:
    rel_parts = path.relative_to(root).parts
    return any(part in EXCLUDED_DIRS for part in rel_parts)


def is_text_candidate(path: Path) -> bool:
    if path.name in {"Dockerfile", "Containerfile", "Makefile", "Rakefile", "Gemfile", "Procfile"}:
        return True
    return path.suffix.lower() in TEXT_EXTS


def read_text(path: Path) -> str | None:
    try:
        data = path.read_bytes()
    except OSError:
        return None
    if b"\x00" in data[:4096]:
        return None
    try:
        return data.decode("utf-8")
    except UnicodeDecodeError:
        return data.decode("utf-8", errors="replace")


def iter_files(root: Path) -> list[Path]:
    files: list[Path] = []
    for dirpath, dirnames, filenames in os.walk(root):
        here = Path(dirpath)
        dirnames[:] = [d for d in dirnames if d not in EXCLUDED_DIRS]
        for name in filenames:
            path = here / name
            if is_excluded(path, root):
                continue
            files.append(path)
    return sorted(files)


def scan_file(root: Path, path: Path) -> list[Hit]:
    rel = path.relative_to(root).as_posix()
    text = read_text(path)
    if text is None:
        return []

    hits: list[Hit] = []
    for lineno, line in enumerate(text.splitlines(), 1):
        stripped = line.strip()
        if not stripped:
            continue
        for category, checks in PATTERNS.items():
            for signal, pattern in checks:
                if pattern.search(line):
                    hits.append(Hit(category, rel, lineno, signal, stripped[:220]))
                    break
    return hits


def parse_existing(path: Path) -> dict[tuple[str, str, int, str], tuple[str, str]]:
    """Preserve disposition/evidence for rows generated by prior runs."""
    if not path.exists():
        return {}
    preserved: dict[tuple[str, str, int, str], tuple[str, str]] = {}
    for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
        if not line.startswith("|") or line.startswith("|---"):
            continue
        cells = [c.strip().strip("`") for c in line.strip().strip("|").split("|")]
        if len(cells) < 7 or cells[0].lower() == "id":
            continue
        # Generic ledger shape: ID | Category | File | Line | Signal | ... | Disposition | Evidence
        if len(cells) >= 8 and cells[3].isdigit():
            key = (cells[1], cells[2], int(cells[3]), cells[4])
            preserved[key] = (cells[-2], cells[-1])
        elif len(cells) >= 9 and cells[2].isdigit():
            key = ("", cells[1], int(cells[2]), cells[3])
            preserved[key] = (cells[-2], cells[-1])
    return preserved


def stable_id(prefix: str, hit: Hit) -> str:
    digest = hashlib.sha1("|".join(map(str, hit.key)).encode()).hexdigest()[:8]
    return f"{prefix}-{digest}"


def md_escape(value: str) -> str:
    return value.replace("|", "\\|").replace("\n", " ").strip()


def write_file_inventory(root: Path, out: Path, files: list[Path]) -> None:
    rows = []
    for path in files:
        rel = path.relative_to(root).as_posix()
        kind = "text-candidate" if is_text_candidate(path) else "unsupported-or-binary"
        try:
            size = path.stat().st_size
        except OSError:
            size = 0
        rows.append(f"| `{md_escape(rel)}` | `{path.suffix or path.name}` | {size} | {kind} | unreviewed | |")

    text = [
        "# File Inventory",
        "",
        "| File | Extension | Bytes | Coverage class | Status | Evidence |",
        "|---|---:|---:|---|---|---|",
        *rows,
        "",
    ]
    (out / "ledgers" / "file-inventory.md").write_text("\n".join(text), encoding="utf-8")


def generic_ledger(out: Path, hits: list[Hit], filename: str, title: str) -> None:
    existing = parse_existing(out / "ledgers" / filename)
    rows: list[str] = []
    for hit in hits:
        disposition, evidence = existing.get(hit.key, existing.get(("", hit.file, hit.line, hit.snippet), ("untriaged", "")))
        if disposition not in DISPOSITIONS:
            disposition = "untriaged"
        rows.append(
            f"| {stable_id('C', hit)} | {hit.category} | `{md_escape(hit.file)}` | {hit.line} | "
            f"{md_escape(hit.signal)} | yes | {disposition} | {md_escape(evidence)} |"
        )
    if not rows:
        rows = ["| none | none | none | 0 | No matching rows found. | no | out-of-scope | census generated |"]

    text = [
        f"# {title}",
        "",
        "| ID | Category | File | Line | Signal | Privileged | Disposition | Evidence |",
        "|---|---|---|---:|---|---|---|---|",
        *rows,
        "",
    ]
    (out / "ledgers" / filename).write_text("\n".join(text), encoding="utf-8")


def typed_ledger(out: Path, hits: list[Hit], filename: str, title: str, columns: list[str], prefix: str) -> None:
    existing = parse_existing(out / "ledgers" / filename)
    rows: list[str] = []
    for hit in hits:
        disposition, evidence = existing.get(hit.key, ("untriaged", ""))
        if disposition not in DISPOSITIONS:
            disposition = "untriaged"
        base = [stable_id(prefix, hit), f"`{md_escape(hit.file)}`", str(hit.line), md_escape(hit.snippet)]
        fill_count = len(columns) - len(base) - 2
        filled = base + ["unknown" for _ in range(max(fill_count, 0))] + [disposition, md_escape(evidence)]
        rows.append("| " + " | ".join(filled[:len(columns)]) + " |")
    if not rows:
        empty = ["none", "none", "0", "No matching rows found."]
        fill_count = len(columns) - len(empty) - 2
        filled = empty + ["n/a" for _ in range(max(fill_count, 0))] + ["out-of-scope", "census generated"]
        rows = ["| " + " | ".join(filled[:len(columns)]) + " |"]

    text = [
        f"# {title}",
        "",
        "| " + " | ".join(columns) + " |",
        "|" + "|".join("---" for _ in columns) + "|",
        *rows,
        "",
    ]
    (out / "ledgers" / filename).write_text("\n".join(text), encoding="utf-8")


def select_route_file_hits(all_hits: list[Hit], by_file: dict[str, set[str]]) -> list[Hit]:
    out: list[Hit] = []
    for hit in all_hits:
        cats = by_file.get(hit.file, set())
        if "route" in cats and hit.category in {"route", "file_io", "path"}:
            out.append(hit)
    return out


def select_api_file_hits(all_hits: list[Hit], by_file: dict[str, set[str]]) -> list[Hit]:
    out: list[Hit] = []
    for hit in all_hits:
        cats = by_file.get(hit.file, set())
        if "api_field" in cats and hit.category in {"api_field", "file_io", "path"}:
            out.append(hit)
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", required=True, help="Repository root to scan")
    ap.add_argument("--out", required=True, help="Report bundle root where ledgers/ will be written")
    args = ap.parse_args()

    root = Path(args.root).expanduser().resolve()
    out = Path(args.out).expanduser().resolve()
    if not root.exists() or not root.is_dir():
        raise SystemExit(f"Repository root not found or not a directory: {root}")
    (out / "ledgers").mkdir(parents=True, exist_ok=True)

    files = iter_files(root)
    text_files = [p for p in files if is_text_candidate(p)]
    all_hits: list[Hit] = []
    by_file: dict[str, set[str]] = {}
    for path in text_files:
        hits = scan_file(root, path)
        all_hits.extend(hits)
        for hit in hits:
            by_file.setdefault(hit.file, set()).add(hit.category)

    write_file_inventory(root, out, files)
    generic_ledger(out, all_hits, "sink-census.md", "Sink Census")

    typed_ledger(
        out,
        select_route_file_hits(all_hits, by_file),
        "route-file-census.md",
        "Route / File Census",
        ["ID", "File", "Line", "Route/handler evidence", "Param/path/file operation", "Containment guard", "Exposure/CORS", "Disposition", "Evidence"],
        "RF",
    )
    typed_ledger(
        out,
        select_api_file_hits(all_hits, by_file),
        "api-response-file-census.md",
        "API-Response / File Census",
        ["ID", "File", "Line", "Source/field evidence", "Local path/file operation", "Guard", "Disposition", "Evidence"],
        "AF",
    )
    typed_ledger(
        out,
        [h for h in all_hits if h.category == "subprocess"],
        "subprocess-census.md",
        "Subprocess Census",
        ["ID", "File", "Line", "Command evidence", "Shell?", "Option injection possible?", "Privilege", "Disposition", "Evidence"],
        "SP",
    )
    typed_ledger(
        out,
        [h for h in all_hits if h.category == "secrets"],
        "secrets-logging-census.md",
        "Secrets / Logging Census",
        ["ID", "File", "Line", "Secret/log evidence", "Sink/source", "Masking/guard", "Runtime context", "Disposition", "Evidence"],
        "SL",
    )
    typed_ledger(
        out,
        [h for h in all_hits if h.category == "network"],
        "network-fetch-census.md",
        "Network Fetch Census",
        ["ID", "File", "Line", "Fetch evidence", "URL source", "Redirect/proxy/DNS guard", "Disposition", "Evidence"],
        "NF",
    )
    typed_ledger(
        out,
        [h for h in all_hits if h.category == "auth"],
        "auth-session-census.md",
        "Auth / Session Census",
        ["ID", "File", "Line", "Auth/session evidence", "Identity boundary", "Guard", "Disposition", "Evidence"],
        "AS",
    )
    typed_ledger(
        out,
        [h for h in all_hits if h.category == "deserialize_archive"],
        "deserialization-archive-census.md",
        "Deserialization / Archive Census",
        ["ID", "File", "Line", "Parse/archive evidence", "Input source", "Traversal/resource guard", "Disposition", "Evidence"],
        "DA",
    )
    typed_ledger(
        out,
        [h for h in all_hits if h.category == "crypto"],
        "crypto-census.md",
        "Crypto Census",
        ["ID", "File", "Line", "Crypto evidence", "Key/IV/signature source", "Guard/invariant", "Disposition", "Evidence"],
        "CR",
    )

    print(f"Scanned {len(files)} files ({len(text_files)} text candidates).")
    print(f"Wrote {len(all_hits)} census rows to {out / 'ledgers'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
