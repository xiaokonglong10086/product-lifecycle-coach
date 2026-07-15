#!/usr/bin/env python3
"""Inventory local product-project files and archives without trusting timestamps alone."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import zipfile
from pathlib import Path
from typing import Any

DOC_EXTS = {".docx", ".pdf", ".pptx", ".xlsx", ".md", ".txt"}
CODE_EXTS = {".ts", ".tsx", ".js", ".jsx", ".py", ".go", ".java", ".rs", ".vue", ".svelte"}
NATIVE_PATTERNS = (
    "@rollup/rollup-",
    "@rolldown/binding-",
    "esbuild-",
    "sharp-",
    ".node",
)
VERSION_RE = re.compile(r"(?:^|[_\-\s])(v?\d+(?:\.\d+){1,3})(?:[_\-\s.]|$)", re.I)


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def classify(path: Path) -> str:
    name = path.name.lower()
    ext = path.suffix.lower()
    if ext == ".zip":
        return "archive"
    if ext in DOC_EXTS:
        if "prd" in name or "需求" in name:
            return "product-spec"
        if "qa" in name or "验收" in name:
            return "qa"
        if "工程" in name or "接口" in name:
            return "engineering-spec"
        if "概念" in name or "brief" in name:
            return "concept"
        return "document"
    if ext in CODE_EXTS or path.name in {"package.json", "pyproject.toml", "Cargo.toml", "go.mod"}:
        return "code"
    return "other"


def version_hint(name: str) -> str:
    match = VERSION_RE.search(name)
    return match.group(1) if match else ""


def inspect_package_json_bytes(data: bytes) -> dict[str, Any]:
    try:
        obj = json.loads(data.decode("utf-8"))
    except Exception:
        return {"parse_error": True}
    return {
        "name": obj.get("name"),
        "version": obj.get("version"),
        "scripts": obj.get("scripts", {}),
        "package_manager": obj.get("packageManager"),
    }


def inspect_zip(path: Path) -> dict[str, Any]:
    result: dict[str, Any] = {
        "entries": 0,
        "has_node_modules": False,
        "has_package_json": False,
        "package_jsons": [],
        "native_binding_hints": [],
        "skill_entrypoints": [],
        "top_level": [],
        "error": None,
    }
    try:
        with zipfile.ZipFile(path) as zf:
            names = zf.namelist()
            result["entries"] = len(names)
            result["has_node_modules"] = any("/node_modules/" in f"/{n}" for n in names)
            result["skill_entrypoints"] = [n for n in names if n.endswith("/SKILL.md") or n == "SKILL.md"][:20]
            tops = sorted({n.strip("/").split("/")[0] for n in names if n.strip("/")})
            result["top_level"] = tops[:30]
            native = [n for n in names if any(p in n for p in NATIVE_PATTERNS)]
            result["native_binding_hints"] = native[:30]
            package_names = [n for n in names if n.endswith("package.json") and "/node_modules/" not in f"/{n}"]
            result["has_package_json"] = bool(package_names)
            for n in package_names[:20]:
                try:
                    result["package_jsons"].append({"path": n, **inspect_package_json_bytes(zf.read(n))})
                except Exception as exc:
                    result["package_jsons"].append({"path": n, "error": str(exc)})
    except Exception as exc:
        result["error"] = str(exc)
    return result


def inspect_directory(path: Path) -> dict[str, Any]:
    result: dict[str, Any] = {
        "files": 0,
        "has_node_modules": False,
        "package_jsons": [],
        "skill_entrypoints": [],
        "native_binding_hints": [],
    }
    native: list[str] = []
    for root, dirs, files in os.walk(path):
        root_path = Path(root)
        rel_root = root_path.relative_to(path)
        if "node_modules" in rel_root.parts:
            result["has_node_modules"] = True
            # Avoid walking huge dependency trees, but sample native bindings.
            for f in files:
                rel = str((rel_root / f).as_posix())
                if any(p in rel for p in NATIVE_PATTERNS):
                    native.append(rel)
            dirs[:] = []
            continue
        result["files"] += len(files)
        for f in files:
            p = root_path / f
            rel = str(p.relative_to(path).as_posix())
            if f == "SKILL.md":
                result["skill_entrypoints"].append(rel)
            if f == "package.json":
                try:
                    result["package_jsons"].append({"path": rel, **inspect_package_json_bytes(p.read_bytes())})
                except Exception as exc:
                    result["package_jsons"].append({"path": rel, "error": str(exc)})
    result["native_binding_hints"] = native[:30]
    return result


def gather(root: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for p in sorted(root.iterdir(), key=lambda x: x.name.lower()):
        row: dict[str, Any] = {
            "path": str(p),
            "name": p.name,
            "kind": "directory" if p.is_dir() else classify(p),
            "version_hint": version_hint(p.name),
            "size_bytes": p.stat().st_size if p.is_file() else None,
            "sha256": sha256(p) if p.is_file() else None,
        }
        if p.is_dir():
            row["inspection"] = inspect_directory(p)
        elif p.suffix.lower() == ".zip":
            row["inspection"] = inspect_zip(p)
        rows.append(row)
    return rows


def render_markdown(root: Path, rows: list[dict[str, Any]]) -> str:
    out = [
        "# Project Source Inventory",
        "",
        f"- **Scanned root:** `{root}`",
        "- **Note:** version hints come from filenames only and do not establish approval or freshness.",
        "",
        "## Sources",
        "",
        "| Source | Kind | Version hint | Size | SHA-256 | Key inspection |",
        "|---|---|---|---:|---|---|",
    ]
    for r in rows:
        ins = r.get("inspection") or {}
        facts: list[str] = []
        if ins.get("has_node_modules"):
            facts.append("bundles node_modules")
        if ins.get("skill_entrypoints"):
            facts.append(f"skills={len(ins['skill_entrypoints'])}")
        if ins.get("package_jsons"):
            names = [str(x.get("name") or x.get("path")) for x in ins["package_jsons"][:3]]
            facts.append("packages=" + ", ".join(names))
        if ins.get("native_binding_hints"):
            facts.append("OS-native bindings detected")
        if ins.get("error"):
            facts.append("ERROR: " + str(ins["error"]))
        size = "" if r["size_bytes"] is None else str(r["size_bytes"])
        digest = "" if not r["sha256"] else r["sha256"][:12]
        out.append(
            f"| `{r['name']}` | {r['kind']} | {r['version_hint']} | {size} | {digest} | {'; '.join(facts)} |"
        )
    out += [
        "",
        "## Portability warnings",
        "",
    ]
    warnings = []
    for r in rows:
        ins = r.get("inspection") or {}
        if ins.get("has_node_modules"):
            warnings.append(
                f"- `{r['name']}` includes `node_modules`. Treat it as source evidence only; delete dependencies and perform a clean install on the target OS before accepting build results."
            )
        if ins.get("native_binding_hints"):
            warnings.append(
                f"- `{r['name']}` contains platform-specific native package hints; archived dependencies may fail on another operating system or architecture."
            )
    out.extend(warnings or ["- No bundled dependency portability warning detected at this inventory depth."])
    out += [
        "",
        "## 后续需要人工与 AI 一起确认",
        "",
        "- 根据文档正文确认内容日期、文档状态、确认记录，以及哪些文档已经被新版替代。",
        "- 分别确认当前产品方向、当前产品规则和当前代码现状。",
        "- 把冲突记录到“当前版本对齐表”；不能只看文件名或版本号决定采用哪一版。",
    ]
    return "\n".join(out) + "\n"


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("path", help="Directory whose immediate children should be inventoried")
    p.add_argument("--json-out", help="Optional JSON output path")
    p.add_argument("--md-out", help="Optional Markdown output path")
    return p.parse_args()


def main() -> int:
    args = parse_args()
    root = Path(args.path).expanduser().resolve()
    if not root.is_dir():
        raise SystemExit(f"Not a directory: {root}")
    rows = gather(root)
    payload = {"root": str(root), "sources": rows}
    markdown = render_markdown(root, rows)
    if args.json_out:
        Path(args.json_out).write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    if args.md_out:
        Path(args.md_out).write_text(markdown, encoding="utf-8")
    if not args.json_out and not args.md_out:
        print(markdown, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
