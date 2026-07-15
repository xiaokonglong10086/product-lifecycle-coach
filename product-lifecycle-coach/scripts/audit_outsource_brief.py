#!/usr/bin/env python3
"""Audit an outsourcing engineering brief for product, security, delivery, and handover completeness."""
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


GROUPS = {
    "business": ["业务目标", "用户结果"],
    "scope": ["本期范围", "明确不做", "必须保留"],
    "flow": ["用户流程", "验收"],
    "permissions": ["角色与权限"],
    "data_security": ["数据", "安全"],
    "delivery": ["技术交付要求", "部署", "测试"],
    "milestones": ["里程碑", "付款验收"],
    "handover": ["最终移交", "完整源码", "部署"],
    "ownership": ["知识产权", "账号", "密钥"],
    "maintenance": ["质保", "维护", "故障响应"],
}


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("brief")
    p.add_argument("--json", action="store_true")
    p.add_argument("--strict", action="store_true")
    return p.parse_args()


def audit(text: str) -> tuple[str, list[Finding]]:
    findings: list[Finding] = []
    for key, terms in GROUPS.items():
        missing = [t for t in terms if t not in text]
        if missing:
            severity = "HIGH" if key in {"scope", "data_security", "milestones", "handover", "ownership"} else "MEDIUM"
            findings.append(Finding(severity, f"MISSING_{key.upper()}", "缺少：" + "、".join(missing)))

    placeholders = sorted(set(re.findall(r"\[[^\]\n]{1,80}\]|\b(?:TBD|TODO|FIXME)\b", text, re.I)))
    if placeholders:
        findings.append(Finding("HIGH", "UNRESOLVED_PLACEHOLDERS", "仍存在模板占位符：" + "、".join(placeholders[:8])))
    blank_fields = len(re.findall(r"^\s*[-*]?\s*[^#|\n]{1,40}[：:]\s*$", text, re.M))
    if blank_fields >= 5:
        findings.append(Finding("HIGH", "BRIEF_NOT_FILLED", f"仍有约 {blank_fields} 个空白字段，不能作为正式外包交接。"))
    if not re.search(r"\|\s*[^|\n]+\|\s*[^|\n]+\|\s*[^|\n]+\|\s*\d+%?\s*\|", text):
        findings.append(Finding("MEDIUM", "MILESTONE_ROWS_MISSING", "里程碑表没有填写可验收交付和付款节点。"))

    high = [f for f in findings if f.severity == "HIGH"]
    medium = [f for f in findings if f.severity == "MEDIUM"]
    verdict = "FAIL" if high else ("PASS WITH CONCERNS" if medium else "PASS")
    return verdict, findings


def main() -> int:
    args = parse_args()
    path = Path(args.brief).expanduser().resolve()
    if not path.exists():
        raise SystemExit(f"外包说明不存在：{path}")
    verdict, findings = audit(path.read_text(encoding="utf-8"))
    payload = {"verdict": verdict, "file": str(path), "findings": [asdict(f) for f in findings]}
    if args.json:
        print(json.dumps(payload, ensure_ascii=False, indent=2))
    else:
        print(f"# 外包工程交接检查：{path.name}\n")
        print(f"**结论：** {verdict}\n")
        for f in findings:
            print(f"- **[{f.severity}] {f.code}：** {f.message}")
        if not findings:
            print("- 业务、范围、工程风险、里程碑和最终移交要求完整。")
    return 1 if args.strict and verdict != "PASS" else 0


if __name__ == "__main__":
    raise SystemExit(main())
