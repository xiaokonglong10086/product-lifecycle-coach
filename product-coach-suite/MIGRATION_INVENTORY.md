# 既有资产迁移清单

状态：待盘点 / 已定位 / 已迁移 / 已验证 / 存在冲突

| 资产 | 原来源 | 新位置 | 状态 | 验证方式 |
|---|---|---|---|---|
| 产品功能 PRD 主规则 | product-function-prd/SKILL.md | references/preserved/prd-core.md | 已迁移 | 内容对照 + PRD 审查 |
| PRD 权威与语义冻结 | authority-and-freeze.md | references/preserved/prd-authority-and-freeze.md | 已迁移 | 规则对照 |
| PRD 输出合同 | prd-contract.md | references/preserved/prd-contract.md | 已迁移 | 禁词与结构测试 |
| 三类流程图与功能细节 | flow-and-function-standard.md | references/preserved/prd-flow-and-function-standard.md | 已迁移 | 流程图与模块覆盖检查 |
| DOCX 质量门 | docx-quality-gate.md | references/preserved/docx-quality-gate.md | 已迁移 | 渲染与门禁检查 |
| 黄金 PRD 表达模式 | xiao-a-gold-pattern.md | references/preserved/prd-gold-pattern.md | 已迁移 | 输出风格对照 |
| PRD 模板 | PRODUCT_FUNCTION_PRD.md | assets/templates/PRODUCT_FUNCTION_PRD.md | 已迁移 | 模板结构检查 |
| PRD 结构审查脚本 | audit_prd.py | scripts/audit_prd.py | 已迁移 | Python 编译 + 正反例 |
| PRD 来源覆盖脚本 | audit_prd_coverage.py | scripts/audit_prd_coverage.py | 已迁移 | Python 编译 + 覆盖测试 |
| 全功能验证主规则 | design-validation-codex/SKILL.md | references/preserved/validation-core.md | 已迁移 | 能力覆盖检查 |
| L3/L4 与产品实验室 | design-validation-standard.md | references/preserved/design-validation-standard.md | 已迁移 | 必填项审查 |
| 模拟数据规范 | mock-data-standard.md | references/preserved/mock-data-standard.md | 已迁移 | 数据场景审查 |
| Codex 总任务模板 | CODEX_MASTER_TASK.md | assets/templates/CODEX_MASTER_TASK.md | 已迁移并升级命名 | 严格任务审查 |
| 设计验证审查脚本 | audit_design_validation_task.py | scripts/audit_design_validation_task.py | 已迁移并升级命名 | Python 编译 + 正反例 |
| 设计理念规则 | product-design-principles | references/preserved/design-principles-core.md | 已迁移 | 理念审查 |
| 设计理念模板 | PRODUCT_DESIGN_PRINCIPLES.md | assets/templates/DESIGN_PRINCIPLES.md | 已迁移并统一命名 | 结构检查 |
| 理念审查脚本 | audit_design_principles.py | scripts/audit_design_principles.py | 已迁移并统一命名 | Python 编译 + 正反例 |
| 实现 QA 规则 | product-implementation-qa | references/preserved/implementation-qa-core.md | 已迁移 | QA 覆盖检查 |
| QA 模板 | QA_REPORT.md | assets/templates/QA_REPORT.md | 已迁移 | 模板检查 |
| 迭代规则 | product-iteration-coach | references/preserved/iteration-core.md | 已迁移 | 反馈分类检查 |
| 迭代模板 | ITERATION_CHANGE_MAP.md | assets/templates/ITERATION_CHANGE_MAP.md | 已迁移 | 模板检查 |
| 产品方向判断标准 | decision-standard.md | references/preserved/direction-standard.md | 已迁移并扩充调研发现 | 场景测试 |

旧资产未完成“已验证”前，不得删除或宣称新 Skill 已完全替代旧 Skill。
