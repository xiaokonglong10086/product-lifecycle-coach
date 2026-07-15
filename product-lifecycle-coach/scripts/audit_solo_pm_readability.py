#!/usr/bin/env python3
"""Check whether a user-facing product report is understandable to a solo PM."""
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


REQUIRED_GROUPS = {
    "current_judgment": ["当前判断", "结论"],
    "reason": ["为什么", "判断依据"],
    "next_steps": ["下一步任务", "下一步"],
}
OWNER_TERMS = ["你来做", "Codex", "外包工程师"]
JARGON = {
    "基线": ["当前产品方向", "当前产品规则", "当前代码现状", "当前版本"],
    "门禁": ["进入下一步的条件", "是否可以开始", "检查条件"],
    "artifact": ["工作文档", "交付物"],
    "traceability": ["需求对应关系", "需求追踪"],
    "program map": ["产品全景", "当前开发地图"],
    "vertical slice": ["纵向切片", "端到端小闭环", "可演示的小闭环"],
    "SLA": ["服务承诺", "响应时间", "可用性"],
    "UAT": ["客户验收", "用户验收"],
    "RBAC": ["角色权限", "按角色授权"],
    "P50/P95": ["多数请求", "较慢请求", "延迟分位"],
}


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("file")
    p.add_argument("--json", action="store_true")
    p.add_argument("--strict", action="store_true")
    return p.parse_args()


def contains_any(text: str, terms: list[str]) -> bool:
    return any(term.lower() in text.lower() for term in terms)


def audit(text: str) -> tuple[str, list[Finding], dict[str, object]]:
    findings: list[Finding] = []
    for key, terms in REQUIRED_GROUPS.items():
        if not contains_any(text, terms):
            findings.append(Finding("HIGH", f"MISSING_{key.upper()}", f"面向用户的报告缺少“{terms[0]}”层。"))

    if not contains_any(text, OWNER_TERMS):
        findings.append(Finding("HIGH", "OWNERSHIP_MISSING", "没有说明哪些工作由用户、Codex 或外包工程师承担。"))
    else:
        if "Codex" in text and "你来做" not in text:
            findings.append(Finding("MEDIUM", "USER_ROLE_UNCLEAR", "提到了 Codex，但没有说明产品经理自己需要做什么。"))
        if re.search(r"安全|权限|数据库|部署|多租户|敏感数据|生产", text) and "外包工程师" not in text:
            findings.append(Finding("MEDIUM", "OUTSOURCE_BOUNDARY_UNCLEAR", "涉及生产工程风险，但没有说明是否需要外包工程师。"))

    unexplained = []
    for term, explanations in JARGON.items():
        if term.lower() in text.lower() and not contains_any(text, explanations):
            unexplained.append(term)
    if unexplained:
        findings.append(Finding("MEDIUM", "UNEXPLAINED_JARGON", "存在对新手不友好的专业词，且没有给出通俗解释。", "、".join(unexplained)))


    if re.search(r"开发|Codex|试点|上线|生产|发布", text) and not contains_any(text, ["产品成熟度", "可交互 Demo", "内部可用", "客户试点", "正式生产"]):
        findings.append(Finding("MEDIUM", "MATURITY_LEVEL_MISSING", "涉及开发或发布，但没有说明当前是 Demo、试点还是正式生产阶段。"))

    if contains_any(text, ["你需要做的决定", "需要用户决定"]) and not contains_any(text, ["我的建议", "推荐", "建议选择", "无需决定"]):
        findings.append(Finding("MEDIUM", "DECISION_RECOMMENDATION_MISSING", "要求用户决定，但没有提供选项、取舍或推荐。"))

    task_rows = len(re.findall(r"^\|\s*\d+\s*\|", text, re.MULTILINE))
    bullet_tasks = len(re.findall(r"^\s*[-*]\s+(?:\[.\]\s*)?(?:任务|下一步|第\s*\d+|\d+[\.、])", text, re.MULTILINE))
    estimated_tasks = max(task_rows, bullet_tasks)
    if estimated_tasks > 5:
        findings.append(Finding("MEDIUM", "TOO_MANY_ACTIVE_TASKS", f"一次给出了约 {estimated_tasks} 个活跃任务，可能超出独立产品经理的执行负荷。"))

    long_paragraphs = []
    for paragraph in re.split(r"\n\s*\n", text):
        plain = re.sub(r"[`#>*_|\-]", "", paragraph).strip()
        if len(plain) > 650 and "|" not in paragraph:
            long_paragraphs.append(len(plain))
    if long_paragraphs:
        findings.append(Finding("MEDIUM", "LONG_PARAGRAPH", "存在过长段落，建议先给结论，再分层展开。", "最长约 " + str(max(long_paragraphs)) + " 字"))

    high = [f for f in findings if f.severity in {"BLOCKER", "HIGH"}]
    medium = [f for f in findings if f.severity == "MEDIUM"]
    verdict = "FAIL" if high else ("PASS WITH CONCERNS" if medium else "PASS")
    return verdict, findings, {"characters": len(text), "estimated_active_tasks": estimated_tasks}


def main() -> int:
    args = parse_args()
    path = Path(args.file).expanduser().resolve()
    if not path.exists():
        raise SystemExit(f"文件不存在：{path}")
    verdict, findings, stats = audit(path.read_text(encoding="utf-8"))
    payload = {"verdict": verdict, "file": str(path), "stats": stats, "findings": [asdict(f) for f in findings]}
    if args.json:
        print(json.dumps(payload, ensure_ascii=False, indent=2))
    else:
        print(f"# 独立产品经理可读性检查：{path.name}\n")
        print(f"**结论：** {verdict}\n")
        for finding in findings:
            evidence = f" 证据：{finding.evidence}" if finding.evidence else ""
            print(f"- **[{finding.severity}] {finding.code}：** {finding.message}{evidence}")
        if not findings:
            print("- 面向用户的结构、用词和责任边界清楚。")
    if args.strict and verdict != "PASS":
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
