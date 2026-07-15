#!/usr/bin/env python3
"""Audit whether a Codex development task is bounded, implementable, and verifiable."""
from __future__ import annotations

import argparse
import json
import re
from dataclasses import asdict, dataclass
from pathlib import Path


@dataclass
class Finding:
    severity: str
    code: str
    message: str
    evidence: str = ""


REQUIRED = {
    "role": ["角色设定"],
    "background": ["项目背景"],
    "current": ["当前代码行为与问题", "当前问题"],
    "goal": ["本轮唯一目标", "本轮目标"],
    "scope": ["修改范围", "允许修改"],
    "forbidden": ["禁止项", "禁止改动"],
    "must": ["必须完成"],
    "states": ["状态与异常", "状态清单"],
    "acceptance": ["验收标准"],
    "commands": ["验证命令", "测试与构建"],
    "output": ["输出格式"],
}


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("task")
    p.add_argument("--json", action="store_true")
    p.add_argument("--strict", action="store_true")
    return p.parse_args()


def contains(text: str, terms: list[str]) -> bool:
    low = text.lower().replace(" ", "")
    return any(t.lower().replace(" ", "") in low for t in terms)


def audit(text: str) -> tuple[str, list[Finding], dict[str, object]]:
    findings: list[Finding] = []
    for key, terms in REQUIRED.items():
        if not contains(text, terms):
            severity = "HIGH" if key in {"goal", "scope", "forbidden", "acceptance", "commands"} else "MEDIUM"
            findings.append(Finding(severity, f"MISSING_{key.upper()}", f"缺少“{terms[0]}”部分。"))

    if not re.search(r"npm\s+run\s+build|pnpm\s+(?:run\s+)?build|yarn\s+build|构建命令", text, re.I):
        findings.append(Finding("HIGH", "BUILD_COMMAND_MISSING", "没有要求运行构建命令或说明项目无构建步骤。"))

    for term, code, message in [
        ("修改文件列表", "CHANGED_FILES_MISSING", "没有要求 Codex 汇报修改文件。"),
        ("未解决问题", "UNRESOLVED_RISKS_MISSING", "没有要求汇报未解决问题和风险。"),
        ("手工验收路径", "MANUAL_ACCEPTANCE_MISSING", "没有给出或要求手工验收路径。"),
        ("未授权范围", "SCOPE_REPORT_MISSING", "没有要求说明是否改动未授权范围。"),
    ]:
        if term not in text:
            findings.append(Finding("MEDIUM", code, message))

    if not re.search(r"Given\b.+When\b.+Then\b|给定.+当.+则", text, re.I | re.S):
        findings.append(Finding("MEDIUM", "ACCEPTANCE_NOT_TESTABLE", "验收标准没有使用可观察的 Given/When/Then 或等价场景表达。"))

    broad_phrases = ["全面优化", "整体重构", "全部完善", "所有问题", "尽可能优化", "自由发挥"]
    found_broad = [p for p in broad_phrases if p in text]
    if found_broad:
        findings.append(Finding("HIGH", "SCOPE_TOO_BROAD", "任务包含容易导致失控的宽泛表达。", "、".join(found_broad)))

    if "先读取代码" not in text and "先读代码" not in text and "先检查当前代码" not in text:
        findings.append(Finding("MEDIUM", "CODE_INSPECTION_NOT_REQUIRED", "没有要求 Codex 在修改前读取真实代码。"))

    if "自行补充产品规则" not in text and "自行决定产品" not in text:
        findings.append(Finding("MEDIUM", "PRODUCT_DECISION_BOUNDARY_MISSING", "没有明确禁止 Codex 自行补产品规则。"))


    placeholders = sorted(set(re.findall(r"\[[^\]\n]{1,80}\]|\b(?:TBD|TODO|FIXME)\b", text, re.I)))
    if placeholders:
        findings.append(Finding("MEDIUM", "UNRESOLVED_PLACEHOLDERS", "仍存在模板占位符，任务还没有填写完成。", "、".join(placeholders[:8])))

    blank_fields = len(re.findall(r"^\s*[-*]?\s*[^#|\n]{1,40}[：:]\s*$", text, re.M))
    if blank_fields >= 3:
        findings.append(Finding("MEDIUM", "TOO_MANY_BLANK_FIELDS", f"仍有约 {blank_fields} 个空白字段。"))

    high = [f for f in findings if f.severity in {"BLOCKER", "HIGH"}]
    medium = [f for f in findings if f.severity == "MEDIUM"]
    verdict = "FAIL" if high else ("PASS WITH CONCERNS" if medium else "PASS")
    return verdict, findings, {"characters": len(text)}


def main() -> int:
    args = parse_args()
    path = Path(args.task).expanduser().resolve()
    if not path.exists():
        raise SystemExit(f"任务文件不存在：{path}")
    verdict, findings, stats = audit(path.read_text(encoding="utf-8"))
    payload = {"verdict": verdict, "file": str(path), "stats": stats, "findings": [asdict(f) for f in findings]}
    if args.json:
        print(json.dumps(payload, ensure_ascii=False, indent=2))
    else:
        print(f"# Codex 任务检查：{path.name}\n")
        print(f"**结论：** {verdict}\n")
        for f in findings:
            evidence = f" 证据：{f.evidence}" if f.evidence else ""
            print(f"- **[{f.severity}] {f.code}：** {f.message}{evidence}")
        if not findings:
            print("- 任务范围、产品规则、验证和汇报要求完整。")
    return 1 if args.strict and verdict != "PASS" else 0


if __name__ == "__main__":
    raise SystemExit(main())
