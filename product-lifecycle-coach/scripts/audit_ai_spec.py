#!/usr/bin/env python3
"""Audit an AI product document with requirements scaled to Level A/B/C.

Level A can be a compact AI function card. Level B adds a single-Agent workflow,
model story, evaluation, cost, and monitoring. Level C adds multi-Agent/high-impact
workflow, tool action control, security, audit, and rollback.
"""
from __future__ import annotations

import argparse
import json
import re
from dataclasses import asdict, dataclass
from pathlib import Path

HEADING_RE = re.compile(r"^#{1,6}\s+(.+?)\s*$", re.MULTILINE)
MERMAID_RE = re.compile(r"```mermaid\s+.+?```", re.IGNORECASE | re.DOTALL)
PLACEHOLDER_RE = re.compile(r"\[(?:功能/需求 ID|负责人|版本|AI 功能名称|Agent/AI 角色|任务名称)\]|\b(?:TBD|TODO|FIXME)\b", re.IGNORECASE)


@dataclass
class Finding:
    severity: str
    code: str
    message: str
    evidence: str = ""


LEVEL_A = {
    "task_value": ["用户任务", "AI 必要性", "用户任务与 AI 必要性"],
    "boundary": ["AI 责任边界", "AI 功能卡"],
    "input_output": ["输入与输出", "输入合同", "输出合同"],
    "user_control": ["用户必须能", "人工责任", "人工确认", "人机责任"],
    "failure": ["失败", "替代方案", "降级"],
    "golden": ["标准测试样例", "黄金测试集", "Golden Set"],
    "acceptance": ["验收标准", "验收场景"],
}

LEVEL_B = {
    "model_story": ["模型故事"],
    "user_journey": ["用户旅程"],
    "context": ["输入与上下文", "上下文信息"],
    "processing": ["处理边界", "处理流程", "确定性边界"],
    "output_contract": ["输出合同"],
    "states": ["状态与交互", "状态清单"],
    "prompt": ["Prompt 设计策略", "提示词设计策略"],
    "evaluation": ["确定性测试", "概率性评估"],
    "latency_cost": ["延迟、成本", "性能、成本", "成本与容量"],
    "monitoring": ["线上监控", "持续改进"],
    "version": ["版本规划", "版本与回退"],
}

LEVEL_C = {
    "agent_workflow": ["Agent 工作流"],
    "agent_roles": ["Agent 职责表", "Agent 职责"],
    "tool_control": ["工具与行动控制", "Agent 工具与行动控制"],
    "security": ["数据、安全", "安全与审计"],
    "audit": ["审计", "操作日志"],
    "rollback": ["回滚", "撤销", "补偿"],
}

MODEL_STORY_TERMS = ["上下文信息", "能力支持", "工具清单", "输出格式", "决策规则", "约束条件", "失败与降级"]


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("spec")
    p.add_argument("--level", choices=["A", "B", "C"])
    p.add_argument("--json", action="store_true")
    p.add_argument("--strict", action="store_true")
    return p.parse_args()


def normalized(text: str) -> str:
    return text.lower().replace(" ", "")


def contains_any(text: str, terms: list[str]) -> bool:
    low = normalized(text)
    return any(normalized(t) in low for t in terms)


def declared_level(text: str) -> str | None:
    m = re.search(r"(?:规格深度|适用深度)\s*[：:]\s*(?:Level\s*)?([ABC])\b", text, re.IGNORECASE)
    if m:
        return m.group(1).upper()
    for level in ("C", "B", "A"):
        if re.search(rf"\bLevel\s*{level}\b", text, re.IGNORECASE):
            return level
    return None


def require_groups(findings: list[Finding], text: str, groups: dict[str, list[str]], severity: str) -> None:
    for key, terms in groups.items():
        if not contains_any(text, terms):
            findings.append(Finding(severity, f"MISSING_{key.upper()}", f"缺少“{terms[0]}”内容。"))


def audit(text: str, level_override: str | None = None) -> tuple[str, list[Finding], dict[str, object]]:
    findings: list[Finding] = []
    headings = HEADING_RE.findall(text)
    level = level_override or declared_level(text)
    if level is None:
        level = "B"
        findings.append(Finding("HIGH", "LEVEL_NOT_DECLARED", "未声明 AI 规格深度；已按 Level B 检查。"))

    require_groups(findings, text, LEVEL_A, "HIGH")
    if level in {"B", "C"}:
        require_groups(findings, text, LEVEL_B, "HIGH")
    if level == "C":
        require_groups(findings, text, LEVEL_C, "HIGH")

    if not contains_any(text, ["允许决定", "AI 可以决定"]):
        findings.append(Finding("HIGH", "ALLOWED_DECISION_MISSING", "没有明确 AI 可以决定什么。"))
    if not contains_any(text, ["禁止决定", "AI 禁止决定"]):
        findings.append(Finding("HIGH", "FORBIDDEN_DECISION_MISSING", "没有明确 AI 禁止决定什么。"))

    if level in {"B", "C"}:
        missing_story = [term for term in MODEL_STORY_TERMS if term not in text]
        if missing_story:
            findings.append(Finding("HIGH", "MODEL_STORY_INCOMPLETE", "模型故事不完整。", "缺少：" + "、".join(missing_story)))
        if not MERMAID_RE.search(text):
            findings.append(Finding("MEDIUM", "USER_FLOW_DIAGRAM_MISSING", "未检测到用户旅程或处理流程的 Mermaid 图。"))

    if level == "C" and len(MERMAID_RE.findall(text)) < 2:
        findings.append(Finding("HIGH", "USER_AND_AGENT_FLOW_NOT_SEPARATE", "Level C 应分别展示用户旅程和 Agent 工作流。"))

    if not re.search(r"10\s*[-—至]\s*20|10-20", text):
        findings.append(Finding("MEDIUM", "PROTOTYPE_TESTSET_NOT_STATED", "没有说明原型阶段可从 10-20 条真实标准样例开始。"))

    if level in {"B", "C"}:
        for term, code, message in [
            ("最大重试", "MAX_RETRY_MISSING", "没有定义最大重试次数。"),
            ("用户提示", "FAILURE_COPY_MISSING", "没有定义失败时用户看到什么。"),
            ("P50/P95", "LATENCY_PERCENTILE_MISSING", "没有用 P50/P95 或等价方式定义延迟目标。"),
            ("单次成本", "COST_LIMIT_MISSING", "没有定义单次成本或试点成本上限。"),
            ("阻断", "RELEASE_BLOCKING_THRESHOLD_MISSING", "没有定义试点/上线阻断条件。"),
        ]:
            if term not in text:
                findings.append(Finding("MEDIUM", code, message))

    if level == "C":
        for term, code in [
            ("人工批准", "HUMAN_APPROVAL_MISSING"),
            ("不可逆", "IRREVERSIBLE_ACTION_MISSING"),
            ("幂等", "IDEMPOTENCY_MISSING"),
            ("日志", "AUDIT_LOG_MISSING"),
            ("回滚", "ROLLBACK_MISSING"),
        ]:
            if term not in text:
                findings.append(Finding("HIGH", code, f"Level C 缺少“{term}”要求。"))

    if not contains_any(text, ["测试标准是目标", "不得写成已经达到", "预期目标"]):
        findings.append(Finding("MEDIUM", "TARGET_VS_ACTUAL_UNCLEAR", "没有区分预期质量目标和已经跑测得到的实际成绩。"))

    placeholders = sorted(set(PLACEHOLDER_RE.findall(text)))
    if placeholders:
        findings.append(Finding("MEDIUM", "UNRESOLVED_PLACEHOLDERS", "仍存在模板占位符。", "、".join(placeholders[:10])))

    high = [f for f in findings if f.severity in {"BLOCKER", "HIGH"}]
    medium = [f for f in findings if f.severity == "MEDIUM"]
    verdict = "FAIL" if high else ("PASS WITH CONCERNS" if medium else "PASS")
    stats = {"level": level, "characters": len(text), "headings": len(headings), "mermaid_flows": len(MERMAID_RE.findall(text))}
    return verdict, findings, stats


def main() -> int:
    args = parse_args()
    path = Path(args.spec).expanduser().resolve()
    if not path.exists():
        raise SystemExit(f"AI 规格文件不存在：{path}")
    verdict, findings, stats = audit(path.read_text(encoding="utf-8"), args.level)
    payload = {
        "verdict": verdict,
        "file": str(path),
        "scope_note": "本检查只验证规格完整性；AI 质量仍需运行真实测试样例集。",
        "stats": stats,
        "findings": [asdict(f) for f in findings],
    }
    if args.json:
        print(json.dumps(payload, ensure_ascii=False, indent=2))
    else:
        print(f"# AI 产品文档检查：{path.name}\n")
        print(f"**结论：** {verdict}\n")
        for f in findings:
            evidence = f" 证据：{f.evidence}" if f.evidence else ""
            print(f"- **[{f.severity}] {f.code}：** {f.message}{evidence}")
        if not findings:
            print("- 文档深度与 AI 风险匹配，责任、测试和失败处理完整。")
    return 1 if args.strict and verdict != "PASS" else 0


if __name__ == "__main__":
    raise SystemExit(main())
