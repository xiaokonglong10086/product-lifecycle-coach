#!/usr/bin/env python3
"""Structural audit for a product concept document.

The audit checks observable structure and approval evidence. It does not prove
that the chosen product direction is strategically correct; use reviewer rubrics
and user review for that judgment.
"""

from __future__ import annotations

import argparse
import json
import re
from dataclasses import asdict, dataclass
from pathlib import Path


HEADING_RE = re.compile(r"^#{1,6}\s+(.+?)\s*$", re.MULTILINE)
MERMAID_RE = re.compile(r"```mermaid\s+.+?```", re.IGNORECASE | re.DOTALL)
PLACEHOLDER_RE = re.compile(r"\[(?:负责人|确认人|日期|版本|变更摘要|场景名|产品/项目名称)\]|\b(?:TBD|TODO|FIXME)\b", re.IGNORECASE)


@dataclass
class Finding:
    severity: str
    code: str
    message: str
    evidence: str = ""


GROUPS = {
    "context": ["产品背景", "context", "背景与决策"],
    "problem": ["目标用户与问题", "用户与问题", "problem"],
    "thesis": ["产品主张", "product thesis", "产品概念"],
    "alternatives": ["方案比较", "方案探索", "alternatives", "approaches"],
    "selected": ["已选产品概念", "selected concept", "核心用户闭环"],
    "scope": ["当前范围", "scope", "明确不做"],
    "success": ["成功、失败与学习", "success", "learning"],
    "risks": ["风险与待确认", "risks", "open"],
    "approval": ["确认记录", "approval"],
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Audit a product concept document.")
    parser.add_argument("concept", help="Path to concept Markdown file.")
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--strict", action="store_true", help="Exit non-zero unless verdict is PASS.")
    parser.add_argument(
        "--require-approved",
        action="store_true",
        help="Treat a concept that is not explicitly approved as a blocker.",
    )
    return parser.parse_args()


def contains_any(text: str, terms: list[str]) -> bool:
    lowered = text.lower()
    return any(term.lower() in lowered for term in terms)


def audit(text: str, require_approved: bool = False) -> tuple[str, list[Finding], dict[str, object]]:
    findings: list[Finding] = []
    titles = HEADING_RE.findall(text)
    heading_text = "\n".join(titles)

    for key, terms in GROUPS.items():
        if not contains_any(heading_text, terms):
            severity = "HIGH" if key in {"problem", "thesis", "alternatives", "selected", "scope", "approval"} else "MEDIUM"
            findings.append(Finding(severity, f"MISSING_{key.upper()}", f"缺少 {key} 章节。"))

    if not MERMAID_RE.search(text):
        findings.append(Finding("MEDIUM", "NO_CORE_LOOP", "未检测到 Mermaid 核心用户闭环。"))

    # Count genuinely named alternatives rather than every mention of the word 方案.
    alternative_labels = set(re.findall(r"(?:方案|Approach)\s*([A-C1-3])\b", text, re.IGNORECASE))
    if len(alternative_labels) < 2:
        findings.append(Finding("HIGH", "ALTERNATIVES_TOO_THIN", "未检测到至少两个可比较的方案。"))

    if not contains_any(text, ["明确不做", "非目标", "out of scope", "non-goal"]):
        findings.append(Finding("HIGH", "NO_NON_GOALS", "缺少明确不做的范围。"))

    if not contains_any(text, ["最危险假设", "riskiest assumption", "学习问题"]):
        findings.append(Finding("MEDIUM", "NO_RISKIEST_ASSUMPTION", "缺少最危险假设或核心学习问题。"))

    approval_match = re.search(r"^\s*(?:-\s*)?(?:\*\*)?(?:决策|approval decision)\s*[:：](?:\*\*)?\s*([^\n]+)", text, re.IGNORECASE | re.MULTILINE)
    approval = approval_match.group(1).strip() if approval_match else ""
    approved = bool(re.search(r"已确认|approved", approval, re.IGNORECASE)) and not bool(
        re.search(r"未确认|需修改|暂缓|否决|not approved", approval, re.IGNORECASE)
    )
    if not approval_match:
        findings.append(Finding("HIGH", "NO_APPROVAL_RECORD", "缺少明确的概念确认记录。"))
    elif not approved:
        findings.append(
            Finding(
                "BLOCKER" if require_approved else "MEDIUM",
                "CONCEPT_NOT_APPROVED",
                "概念尚未明确批准；可继续完善，但不能作为落地 PRD 的已确认产品方向。",
                approval,
            )
        )

    placeholders = sorted(set(PLACEHOLDER_RE.findall(text)))
    if placeholders:
        findings.append(Finding("MEDIUM", "UNRESOLVED_PLACEHOLDERS", "仍存在模板占位符。", ", ".join(placeholders[:10])))

    high = [f for f in findings if f.severity in {"BLOCKER", "HIGH"}]
    medium = [f for f in findings if f.severity == "MEDIUM"]
    verdict = "FAIL" if high else ("PASS WITH CONCERNS" if medium else "PASS")
    stats = {
        "characters": len(text),
        "headings": len(titles),
        "alternative_labels": sorted(alternative_labels),
        "approved": approved,
        "approval_required": require_approved,
    }
    return verdict, findings, stats


def main() -> int:
    args = parse_args()
    path = Path(args.concept).expanduser().resolve()
    if not path.exists():
        raise SystemExit(f"Concept not found: {path}")
    verdict, findings, stats = audit(path.read_text(encoding="utf-8"), args.require_approved)
    payload = {
        "verdict": verdict,
        "file": str(path),
        "scope_note": "Structural and approval-evidence audit only; strategic product judgment is still required.",
        "stats": stats,
        "findings": [asdict(f) for f in findings],
    }
    if args.json:
        print(json.dumps(payload, ensure_ascii=False, indent=2))
    else:
        print(f"# Concept Audit: {path.name}\n")
        print(f"**Verdict:** {verdict}\n")
        print("**Scope:** Structural and approval-evidence audit only; strategic product judgment is still required.\n")
        for finding in findings:
            evidence = f" Evidence: {finding.evidence}" if finding.evidence else ""
            print(f"- **[{finding.severity}] {finding.code}:** {finding.message}{evidence}")
        if not findings:
            print("- No structural issues detected.")
    if args.strict and verdict != "PASS":
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
