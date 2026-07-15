#!/usr/bin/env python3
"""Run lightweight regression checks for the bundled product-lifecycle auditors."""
from __future__ import annotations

import json
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"


def run(script: str, file: Path, expect_success: bool, extra: list[str] | None = None) -> dict[str, object]:
    cmd = [sys.executable, str(SCRIPTS / script), str(file), "--strict", "--json"]
    if extra:
        cmd.extend(extra)
    proc = subprocess.run(cmd, text=True, capture_output=True)
    passed = (proc.returncode == 0) == expect_success
    return {
        "script": script,
        "file": file.name,
        "expected_success": expect_success,
        "returncode": proc.returncode,
        "passed": passed,
        "stdout": proc.stdout[-1000:],
        "stderr": proc.stderr[-1000:],
    }


def main() -> int:
    with tempfile.TemporaryDirectory(prefix="plc-self-test-") as td:
        tmp = Path(td)
        ai_good = tmp / "ai-good.md"
        ai_good.write_text(
            """# 摘要助手｜轻量 AI 功能卡
- **适用深度：** Level A 轻量助手
## 1. 用户任务
用户任务是把长材料变成可编辑摘要，AI 必要性在于文本压缩。
## 2. AI 责任边界
AI 可以决定措辞；AI 禁止决定正式规则；用户必须能编辑、重试、拒绝。
## 3. 输入与输出
输入为已授权文本，输出为结构化摘要。
## 4. 交互与失败
失败时提供用户提示，最大重试 1 次，保留输入并给人工编辑替代方案。
## 5. 标准测试样例
原型阶段使用 10-20 条样例；测试标准是预期目标，不代表已经达到。
## 6. 验收标准
Given 有效材料 When 生成 Then 用户可编辑；Given 信息不足 When 生成 Then 不编造。
""",
            encoding="utf-8",
        )
        ai_bad = tmp / "ai-bad.md"
        ai_bad.write_text("# AI 功能\n调用模型生成内容。\n", encoding="utf-8")

        codex_good = tmp / "codex-good.md"
        codex_good.write_text(
            """# Codex 开发任务｜返回结果
## 角色设定
你是前端工程师，先读取代码，不自行补充产品规则。
## 项目背景
测试模块需要返回结果。
## 当前代码行为与问题
当前没有结果返回。
## 本轮唯一目标
完成一次测试后展示奖牌。
## 修改范围
只修改测试桥接和结果页。
## 禁止项
不改游戏玩法，不改未授权范围。
## 必须完成
接收结果并展示。
## 状态与异常
处理默认、加载、空、失败、重复和返回。
## 验收标准
Given 游戏完成 When 返回结果 Then 显示奖牌。
## 验证命令
测试 npm test；构建 npm run build；手工验收路径：首页到结果页。
## 输出格式
汇报修改文件列表、命令结果、手工验收路径、未解决问题、未授权范围。
""",
            encoding="utf-8",
        )
        codex_bad = tmp / "codex-bad.md"
        codex_bad.write_text("# 任务\n全面优化所有问题，自由发挥。\n", encoding="utf-8")

        outsource_good = tmp / "outsource-good.md"
        outsource_good.write_text(
            """# 登录与租户隔离外包说明
## 1. 业务目标
业务目标和用户结果明确。
## 2. 本期范围
本期范围：登录；明确不做：SSO；必须保留：现有前端。
## 3. 用户流程与验收
用户流程、角色与权限和验收场景明确。
## 4. 数据、AI 与安全
数据与安全、多租户隔离明确。
## 5. 技术交付要求
技术交付要求、部署和测试明确。
## 6. 里程碑与付款验收
| 里程碑 | 可运行交付 | 验收标准 | 付款比例 | 预计时间 |
|---|---|---|---:|---|
| M1 | 登录测试版 | 三角色通过 | 50% | 1周 |
| M2 | 正式移交 | 越权测试通过 | 50% | 1周 |
## 7. 最终移交
最终移交完整源码、部署文档；账号、密钥和知识产权归公司；提供质保、维护和故障响应。
## 8. 外包方方案
提交架构、风险、排期和维护成本。
""",
            encoding="utf-8",
        )
        outsource_bad = tmp / "outsource-bad.md"
        outsource_bad.write_text("# 需求\n把系统上线，代码你们保管。\n", encoding="utf-8")


        prd_good = tmp / "prd-good.md"
        prd_good.write_text(
            """# 示例产品 产品功能需求文档
## 1. 产品概述
产品帮助顾问完成录音处理和推报。
## 2. 产品结构与页面关系
包含入口、任务列表、确认页和推报页。
## 3. 完整产品流程与核心用户流程
### 3.1 完整产品流程
```mermaid
flowchart TD
A[进入]-->B{选择任务}
B-->C[录音处理]
B-->D[推报]
C-->E{成功?}
E--否-->F[提示并重试]
E--是-->G[人工确认]
```
### 3.2 录音处理流程
```mermaid
flowchart TD
A[选人]-->B[上传]-->C[处理]-->D[审核]-->E[回写]
```
## 4. 产品内部运作逻辑
任务登记、队列处理、AI 分模块生成、待确认草稿、通知、人工审核、正式写入和质量回流。
## 5. 通用组件与交互规则
搜索、编辑、返回、加载和错误反馈规则。
## 6. 工具一：录音处理
功能作用：整理沟通信息。页面位置：确认页。进入条件：录音上传成功。操作流程：选择候选人、上传、离开等待、收到通知、审核并确认。展示内容与产品规则：转录、纪要、标签、洞察和待办完整展示。交互反馈：处理中有阶段提示，失败可重试。状态与异常：空、处理、部分失败、成功和只读。数据去向：确认后分别写入沟通备注、标签和数据库。验收标准：确认前不写入，确认后结果一致。
## 7. 工具二：推报邮件
功能作用：生成推荐概述和邮件。页面位置：推报页。进入条件：已选候选人和项目。操作过程：选人、选项目、生成、编辑、复制。产品规则：简历与项目为主信息源，已确认沟通只补充最新信息。交互反馈：缺失资料阻止生成。异常：生成失败可重试。数据去向：仅用于当前邮件。验收标准：事实可追溯，邮件字段替换正确。
## 8. 跨功能业务规则与异常处理
未确认内容不能作为正式事实，外部服务失败保留成功结果。
## 9. 质量监控与成功标准
记录使用率、采纳率、投诉率并每周抽检。
## 10. 非功能需求
性能、兼容、隐私和恢复要求。
## 11. AI 功能与 Prompt 产品规格
AI 不编造，用户最终确认。
## 12. 待确认问题
通知渠道待确认。
""", encoding="utf-8")
        prd_bad = tmp / "prd-bad.md"
        prd_bad.write_text(
            """# 产品 PRD V4.1
## 产品概述
本版恢复 V3 原规则。
## 功能
| 功能 | 说明 |
|---|---|
| 全部功能 | AI 自动处理 |
""", encoding="utf-8")

        checks = [
            run("audit_ai_spec.py", ai_good, True, ["--level", "A"]),
            run("audit_ai_spec.py", ai_bad, False, ["--level", "A"]),
            run("audit_codex_task.py", codex_good, True),
            run("audit_codex_task.py", codex_bad, False),
            run("audit_outsource_brief.py", outsource_good, True),
            run("audit_outsource_brief.py", outsource_bad, False),
            run("audit_prd.py", prd_good, True),
            run("audit_prd.py", prd_bad, False),
        ]
        ok = all(c["passed"] for c in checks)
        print(json.dumps({"status": "PASS" if ok else "FAIL", "checks": checks}, ensure_ascii=False, indent=2))
        return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
