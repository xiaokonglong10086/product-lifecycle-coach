#!/usr/bin/env python3
"""Flag likely mixed product specifications and suggest companion artifacts."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

CATEGORIES = {
    "concept": ["定位", "价值主张", "产品愿景", "机会", "商业价值", "目标用户", "非目标", "成功标准"],
    "landing_prd": ["用户动线", "功能清单", "功能详细", "交互", "状态", "边界", "数据规范", "文案规范"],
    "ux": ["信息架构", "页面布局", "线框", "视觉", "响应式", "无障碍", "设计系统"],
    "ai_spec": ["模型", "prompt", "提示词", "置信度", "人工审核", "评估集", "黄金集", "幻觉", "降级"],
    "engineering": ["api", "接口", "schema", "数据库", "领域模型", "事件契约", "幂等", "异步", "架构", "错误码", "迁移"],
    "qa_release": ["qa", "验收用例", "测试计划", "上线门禁", "发布", "回滚", "监控", "sla"],
    "traceability": ["需求追踪", "需求矩阵", "requirement id", "需求 id", "映射"],
    "roadmap_ops": ["路线图", "运营", "试点", "迭代", "实验", "指标复盘"],
}

HEADING_RE = re.compile(r"^#{1,6}\s+(.+?)\s*$", re.M)


def normalize(s: str) -> str:
    return s.lower().strip()


def audit(text: str) -> dict:
    headings = HEADING_RE.findall(text)
    haystack = normalize("\n".join(headings) + "\n" + text[:20000])
    scores = {}
    hits = {}
    for category, words in CATEGORIES.items():
        found = [w for w in words if normalize(w) in haystack]
        hits[category] = found
        scores[category] = len(found)
    thresholds = {
        "concept": 2,
        "landing_prd": 2,
        "ux": 1,
        "ai_spec": 1,
        "engineering": 1,
        "qa_release": 1,
        "traceability": 1,
        "roadmap_ops": 1,
    }
    active = [k for k, v in scores.items() if v >= thresholds[k]]
    high_mix = "landing_prd" in active and any(k in active for k in ("engineering", "qa_release", "ai_spec"))
    suggestions = []
    if high_mix:
        suggestions.append("把产品行为保留在固定八节落地 PRD 中，并将工程、AI、QA 内容拆到对应工作文档。")
    if "engineering" in active:
        suggestions.append("创建或更新工程规格，并保留需求 ID 的对应关系。")
    if "ai_spec" in active:
        suggestions.append("创建或更新 AI 产品专项规格，补齐人工控制、评估、降级与线上监控。")
    if "qa_release" in active:
        suggestions.append("创建或更新 QA/发布计划，并让每个检查条件对应到需求 ID。")
    if scores["traceability"] >= 1:
        suggestions.append("把需求对应关系作为独立维护的工作文档，不要只放在一次性的附录里。")
    return {
        "heading_count": len(headings),
        "headings": headings,
        "scores": scores,
        "hits": hits,
        "active_categories": active,
        "mixed_product_spec": high_mix,
        "suggestions": suggestions,
    }


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("file", help="Markdown or plain-text specification")
    p.add_argument("--json", action="store_true", help="Emit JSON")
    args = p.parse_args()
    path = Path(args.file)
    result = audit(path.read_text(encoding="utf-8"))
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(f"混合型产品规格：{'是' if result['mixed_product_spec'] else '否'}")
        print("检测到的内容类型：" + ", ".join(result["active_categories"]))
        for category, words in result["hits"].items():
            if words:
                print(f"- {category}: {', '.join(words)}")
        for suggestion in result["suggestions"]:
            print(f"- 建议：{suggestion}")
    return 1 if result["mixed_product_spec"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
