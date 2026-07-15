#!/usr/bin/env python3
"""Audit a product-function PRD against the user's readability and preservation contract."""
from __future__ import annotations

import argparse
import json
import re
from dataclasses import asdict, dataclass
from pathlib import Path

HEADING_RE = re.compile(r"^(#{1,6})\s+(.+?)\s*$", re.MULTILINE)
MERMAID_RE = re.compile(r"```mermaid\s+.+?```", re.IGNORECASE | re.DOTALL)
IMAGE_RE = re.compile(r"!\[[^\]]*\]\([^\)]+\)")
PROCESS_RESIDUE = [
    r"\bV\d+(?:\.\d+)?\b", r"上一版", r"原版本", r"本版变更", r"变更摘要",
    r"功能完整性对照", r"沿用.{0,8}规则", r"恢复.{0,8}功能", r"原规则",
]
ENGINEERING_SIGNALS = [
    "uuid", "checksum", "payload_hash", "数据库表", "索引", "ddl", "/api/",
    "http endpoint", "消息队列实现", "代码结构", "typescript interface",
]
VAGUE_TERMS = ["合理处理", "视情况", "后续优化", "灵活处理", "尽可能", "体验良好"]

REQUIRED_CONCEPTS = {
    "PRODUCT_OVERVIEW": ["产品概述"],
    "STRUCTURE": ["产品结构", "页面关系"],
    "COMPLETE_FLOW": ["完整产品流程", "产品完整流程"],
    "INTERNAL_LOGIC": ["产品内部运作逻辑", "内部运作逻辑"],
    "COMMON_RULES": ["通用组件", "交互规则"],
    "CROSS_RULES": ["跨功能业务规则", "异常处理"],
    "QUALITY": ["质量监控", "成功标准", "质量目标"],
    "NFR": ["非功能需求"],
    "OPEN_QUESTIONS": ["待确认问题"],
}
DETAIL_MARKERS = [
    "功能作用", "页面位置", "进入条件", "操作流程", "操作过程", "展示内容",
    "产品规则", "交互反馈", "状态", "异常", "数据去向", "验收标准",
]

@dataclass
class Finding:
    severity: str
    code: str
    message: str
    evidence: str = ""


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Audit a product-function PRD Markdown file.")
    p.add_argument("prd")
    p.add_argument("--strict", action="store_true")
    p.add_argument("--json", action="store_true")
    return p.parse_args()


def audit(text: str) -> tuple[str, list[Finding], dict[str, object]]:
    findings: list[Finding] = []
    headings = [m.group(2).strip() for m in HEADING_RE.finditer(text)]

    for code, alternatives in REQUIRED_CONCEPTS.items():
        if not any(term in text for term in alternatives):
            findings.append(Finding("HIGH", f"MISSING_{code}", f"缺少必要内容：{' / '.join(alternatives)}。"))

    flow_section = "\n".join(h for h in headings if "流程" in h)
    flow_count = len(MERMAID_RE.findall(text)) + len(IMAGE_RE.findall(text))
    if flow_count < 2:
        findings.append(Finding("HIGH", "INSUFFICIENT_FLOWS", "至少需要一张完整产品流程和一张核心任务流程。", str(flow_count)))
    if "完整产品流程" not in text and "产品完整流程" not in text:
        findings.append(Finding("HIGH", "NO_COMPLETE_OVERVIEW_FLOW", "没有明确标识完整产品总流程。"))

    residues = [p for p in PROCESS_RESIDUE if re.search(p, text, re.IGNORECASE)]
    if residues:
        findings.append(Finding("HIGH", "VERSION_PROCESS_RESIDUE", "正式 PRD 残留版本修订或恢复语言。", "、".join(residues)))

    engineering_hits = [s for s in ENGINEERING_SIGNALS if s.lower() in text.lower()]
    if len(engineering_hits) >= 4:
        findings.append(Finding("MEDIUM", "ENGINEERING_NOISE", "主 PRD 混入较多工程实现细节，应转移到工程规格。", "、".join(engineering_hits[:8])))

    marker_hits = [m for m in DETAIL_MARKERS if m in text]
    if len(marker_hits) < 7:
        findings.append(Finding("HIGH", "FUNCTION_DETAIL_TOO_THIN", "功能正文缺少足够的操作、规则、状态、异常、数据去向或验收信息。", "已有：" + "、".join(marker_hits)))

    # Detect over-compression: too many table lines and too little continuous explanation.
    lines = [x for x in text.splitlines() if x.strip()]
    table_lines = [x for x in lines if x.lstrip().startswith("|")]
    prose_lines = [x for x in lines if not x.lstrip().startswith(("|", "#", "-", "*", "```"))]
    if len(table_lines) > max(40, len(prose_lines) * 2):
        findings.append(Finding("MEDIUM", "TABLE_OVERUSE", "表格占比过高，可能把复杂功能压缩成摘要表。", f"表格行 {len(table_lines)} / 连续正文行 {len(prose_lines)}"))

    vague = [v for v in VAGUE_TERMS if v in text]
    if vague:
        findings.append(Finding("MEDIUM", "VAGUE_LANGUAGE", "存在不可直接判断或验收的模糊表达。", "、".join(vague)))

    # Main product modules should be substantial, not one-line summaries.
    substantial_sections = 0
    matches = list(HEADING_RE.finditer(text))
    for i, m in enumerate(matches):
        title = m.group(2).strip()
        level = len(m.group(1))
        if re.search(r"工具|模块|功能", title) and not any(x in title for x in ["功能结构", "AI 功能", "非功能"]):
            end = len(text)
            for later in matches[i + 1:]:
                if len(later.group(1)) <= level:
                    end = later.start()
                    break
            body = text[m.end():end].strip()
            if len(body) >= 120:
                substantial_sections += 1
    if substantial_sections < 2:
        findings.append(Finding("HIGH", "NO_SUBSTANTIAL_MODULES", "未检测到至少两个有充分细节的业务模块或核心功能章节。", str(substantial_sections)))

    highs = [f for f in findings if f.severity == "HIGH"]
    mediums = [f for f in findings if f.severity == "MEDIUM"]
    verdict = "FAIL" if highs else ("PASS WITH CONCERNS" if mediums else "PASS")
    stats = {
        "characters": len(text),
        "headings": len(headings),
        "flow_assets": flow_count,
        "detail_markers": marker_hits,
        "substantial_modules": substantial_sections,
        "table_lines": len(table_lines),
        "prose_lines": len(prose_lines),
    }
    return verdict, findings, stats


def main() -> int:
    args = parse_args()
    text = Path(args.prd).read_text(encoding="utf-8")
    verdict, findings, stats = audit(text)
    payload = {"verdict": verdict, "stats": stats, "findings": [asdict(f) for f in findings]}
    if args.json:
        print(json.dumps(payload, ensure_ascii=False, indent=2))
    else:
        print(verdict)
        for f in findings:
            print(f"[{f.severity}] {f.code}: {f.message} {f.evidence}")
    return 0 if (not args.strict or verdict == "PASS") else 1


if __name__ == "__main__":
    raise SystemExit(main())
