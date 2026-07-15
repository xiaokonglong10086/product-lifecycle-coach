#!/usr/bin/env python3
"""Check requirement-ID coverage across PRD, tasks, engineering, and QA artifacts.

This is an identifier-presence audit. It cannot prove that an implementation task
or test semantically satisfies the requirement; a reviewer must still inspect the
mapped behavior and evidence.
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


REQ_RE = re.compile(r"\b(?:F-\d{3}(?:-\d{2})?|[A-Z][A-Z0-9]*(?:-[A-Z0-9]+)*-\d{3})\b")
DEFAULT_IGNORED_PREFIXES = {"DEC", "E", "UJ", "SC", "TASK", "QA"}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Audit requirement-ID presence across product artifacts.")
    parser.add_argument("--prd", required=True, help="PRD Markdown path.")
    parser.add_argument("--tasks", required=True, help="Implementation tasks Markdown path.")
    parser.add_argument("--qa", help="QA or acceptance Markdown path.")
    parser.add_argument("--engineering", help="Engineering specification Markdown path.")
    parser.add_argument("--ignore-prefix", action="append", default=[], help="Requirement prefix to ignore; repeatable.")
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--strict", action="store_true", help="Exit non-zero on missing coverage or absent PRD IDs.")
    return parser.parse_args()


def prefix_of(requirement_id: str) -> str:
    return requirement_id.split("-", 1)[0]


def read_ids(path_value: str | None, ignored: set[str]) -> tuple[Path | None, set[str]]:
    if not path_value:
        return None, set()
    path = Path(path_value).expanduser().resolve()
    if not path.exists():
        raise SystemExit(f"Artifact not found: {path}")
    ids = set(REQ_RE.findall(path.read_text(encoding="utf-8")))
    filtered = {rid for rid in ids if prefix_of(rid) not in ignored}
    return path, filtered


def extract_section(text: str, heading_patterns: list[str]) -> str:
    """Return a level-2 section including all nested content."""
    headings = list(re.finditer(r"^##\s+(.+?)\s*$", text, re.MULTILINE))
    for index, match in enumerate(headings):
        title = match.group(1).lower()
        if any(pattern.lower() in title for pattern in heading_patterns):
            end = headings[index + 1].start() if index + 1 < len(headings) else len(text)
            return text[match.start():end]
    return ""


def read_prd_ids(path_value: str, ignored: set[str]) -> tuple[Path, set[str], str]:
    path = Path(path_value).expanduser().resolve()
    if not path.exists():
        raise SystemExit(f"Artifact not found: {path}")
    text = path.read_text(encoding="utf-8")
    # Current-scope requirements live in detailed behavior, cross-cutting rules,
    # NFRs, and AI requirements. Feature-tree future items are intentionally
    # excluded unless they are expanded into one of these sections.
    scoped = "\n".join(
        filter(
            None,
            [
                extract_section(text, ["功能详细描述", "detailed requirements", "functional detail"]),
                extract_section(text, ["全局业务规则", "业务规则、角色权限", "cross-cutting rules"]),
                extract_section(text, ["非功能性需求", "non-functional"]),
                extract_section(text, ["ai 产品专项", "ai product"]),
            ],
        )
    )
    source_text = scoped or text
    ids = set(REQ_RE.findall(source_text))
    filtered = {rid for rid in ids if prefix_of(rid) not in ignored}
    return path, filtered, "current-scope sections" if scoped else "whole PRD fallback"


def main() -> int:
    args = parse_args()
    ignored = DEFAULT_IGNORED_PREFIXES | {value.upper() for value in args.ignore_prefix}
    prd_path, prd_ids, prd_id_source = read_prd_ids(args.prd, ignored)
    tasks_path, task_ids = read_ids(args.tasks, ignored)
    engineering_path, engineering_ids = read_ids(args.engineering, ignored)
    qa_path, qa_ids = read_ids(args.qa, ignored)

    missing_tasks = sorted(prd_ids - task_ids)
    missing_engineering = sorted(prd_ids - engineering_ids) if engineering_path else []
    missing_qa = sorted(prd_ids - qa_ids) if qa_path else []
    orphan_tasks = sorted(task_ids - prd_ids)
    orphan_engineering = sorted(engineering_ids - prd_ids) if engineering_path else []
    orphan_qa = sorted(qa_ids - prd_ids) if qa_path else []

    no_prd_ids = not prd_ids
    fail = bool(no_prd_ids or missing_tasks or missing_engineering or missing_qa)
    verdict = "FAIL" if fail else "PASS"
    result = {
        "verdict": verdict,
        "scope_note": "ID-presence audit only; semantic requirement satisfaction must be reviewed separately.",
        "artifacts": {
            "prd": str(prd_path),
            "tasks": str(tasks_path),
            "engineering": str(engineering_path) if engineering_path else None,
            "qa": str(qa_path) if qa_path else None,
        },
        "prd_id_source": prd_id_source,
        "counts": {
            "prd_requirements": len(prd_ids),
            "task_references": len(task_ids),
            "engineering_references": len(engineering_ids),
            "qa_references": len(qa_ids),
        },
        "missing": {
            "tasks": missing_tasks,
            "engineering": missing_engineering,
            "qa": missing_qa,
        },
        "orphan": {
            "tasks": orphan_tasks,
            "engineering": orphan_engineering,
            "qa": orphan_qa,
        },
        "issues": ["PRD contains no auditable requirement IDs."] if no_prd_ids else [],
        "ignored_prefixes": sorted(ignored),
    }

    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print("# Traceability Audit\n")
        print(f"**Verdict:** {verdict}\n")
        print("**Scope:** ID-presence audit only; semantic requirement satisfaction must be reviewed separately.\n")
        if no_prd_ids:
            print("- **[HIGH]** PRD contains no auditable requirement IDs.\n")
        print(f"**PRD ID source:** {prd_id_source}\n")
        print("## Coverage")
        for key, value in result["counts"].items():
            print(f"- **{key}:** {value}")
        print("\n## Missing requirement coverage")
        for artifact, ids in result["missing"].items():
            print(f"- **{artifact}:** {', '.join(ids) if ids else 'none'}")
        print("\n## Orphan references")
        for artifact, ids in result["orphan"].items():
            print(f"- **{artifact}:** {', '.join(ids) if ids else 'none'}")

    if args.strict and fail:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
