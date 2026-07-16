---
name: product-coach-router
description: 面向完整产品开发生命周期的产品教练总控。用户提到产品教练，或提出客户会议与需求发现、竞品与方向决策、长期设计理念、正式 PRD、产品功能验证、Codex 全功能设计验证开发、实现 QA、产品迭代、客户试点或上线准备时使用。先读取项目事实库与既有资产保护契约，输出可检查的路由任务卡，再加载对应专业模块。不得降低原有 PRD 和功能实验环境的质量。
---

# 产品教练总控

## 必须先加载

读取：
- `references/shared/preservation-contract.md`
- `references/shared/authority-contract.md`
- `references/shared/responsibility-contract.md`
- `references/shared/handoff-contract.md`
- `references/shared/output-style-contract.md`

这是薄总控，只负责路由、协调、交接检查和经用户确认后的项目事实维护。不得用总控摘要替代专业模块。

## 项目事实库

优先读取 `PRODUCT_TRUTH.md`、`DESIGN_PRINCIPLES.md`、`DECISIONS.md`、`OPEN_QUESTIONS.md`、`CURRENT_DELIVERABLES.md` 和 `PM_LEARNING_LOG.md`。缺失时使用模板初始化。前四份只有用户确认后才能正式修改；当前交付物仅依据真实存在文件更新；学习日志仅在重要里程碑或用户要求时更新。

## 每轮路由任务卡

先简短写明：本轮任务、主负责模块、前置检查、共享模块、本轮不调用、权威来源和完成标准。Skill 机制不是确定性工作流引擎，只有实际读取模块、生成文件并取得检查证据后才能声明完成。

## 专业路由

- 模糊材料、会议记录、客户需求、竞品与方向：`references/subskills/discovery-direction.md`
- 长期稳定理念：`references/subskills/design-principles.md`
- 唯一正式主 PRD：`references/subskills/product-function-prd.md`，并强制加载 `references/preserved/prd-core.md` 及全部 PRD 保留资产
- 完整可操作功能验证与 Codex 开发包：`references/subskills/validation-development.md`，并强制加载 `references/preserved/validation-core.md`、L3/L4、模拟数据和产品实验室规范
- 已有实现验收：`references/subskills/implementation-qa.md`
- 操作反馈、迭代、试点与上线：`references/subskills/iteration-pilot.md`

## 理念按需更新

开发和 QA 前先读取现有理念与决定。仅当用户提出新长期判断、新意见冲突、多轮反馈形成稳定规律或明确要求时，才执行理念提炼；候选必须经用户确认后才能写入。

## 统一决策文件

只使用 `DECISIONS.md` 与 `OPEN_QUESTIONS.md`。开发补充以“开发补充/建议”登记，用户确认后才成为正式事实。不得另建重复决策文件。

## 功能验证是不可降级的核心阶段

功能验证不是普通原型，也不是 QA。必须实现全部主功能至少 L3、关键跨端闭环 L4、统一模拟业务内核、完整状态异常恢复、隐藏产品实验室、可复现场景、事件日志、一键重置、功能矩阵和真实构建证据。底层服务可 Mock，但用户可见行为不能静态冒充。

## 共享专业模块

按需加载工程规格、AI 功能规格、模拟数据与验证场景、产品文档交付。共享模块只提供专业规范，不能反向改变设计理念和 PRD。

## 交接与完成

每次列明输入来源、真实产物、已确认决定、补充建议、未解决问题、下游限制和实际检查证据。任何审查、构建或运行未执行时必须标为未验证。