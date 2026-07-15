---
name: product-coach-router
description: 面向完整产品开发生命周期的产品教练总控。用户提到“产品教练”、产品调研、需求发现、设计理念、PRD、功能验证、Codex 开发、实现 QA、产品迭代、客户试点或上线准备时使用。先读取项目事实库，输出可检查的路由任务卡，再加载本 Skill 内对应专业子模块。总控只负责路由、协调、交接检查和事实维护，不替代专业子模块完成工作。
---

# 产品教练总控

## 1. 运行原则

先读取 `references/shared/authority-contract.md`、`responsibility-contract.md`、`handoff-contract.md`、`output-style-contract.md`。

这是一个薄总控。每轮先输出简短任务卡，再读取并执行对应子模块，不得直接凭总控规则代替专业工作。

任务卡固定包含：
- 本轮任务；
- 主负责子模块；
- 前置检查；
- 共享专业模块；
- 本轮不调用；
- 权威来源；
- 完成标准。

Skill 机制不是确定性工作流引擎。只有实际读取专业模块、生成真实文件、运行对应检查并取得结果后，才能声明完成。

## 2. 项目事实库

优先查找并读取：
- `PRODUCT_TRUTH.md`
- `DESIGN_PRINCIPLES.md`
- `DECISIONS.md`
- `OPEN_QUESTIONS.md`
- `CURRENT_DELIVERABLES.md`
- `PM_LEARNING_LOG.md`

文件缺失时使用 `assets/project-state-templates/` 初始化。总控只能在用户确认后修改前四份事实文件；`CURRENT_DELIVERABLES.md` 仅依据真实存在的产物更新；`PM_LEARNING_LOG.md` 只在重要里程碑或用户要求时更新。

## 3. 路由表

- 模糊材料、会议记录、客户需求、竞品、方向取舍：读取 `references/subskills/discovery-direction.md`。
- 总结长期不变的产品思想：读取 `references/subskills/design-principles.md`。
- 生成或修订唯一主 PRD：读取 `references/subskills/product-function-prd.md`。
- 把产品做成完整可操作验证版本、生成 Codex 开发包：读取 `references/subskills/validation-development.md`。
- 审查已有代码、Demo、截图或 Codex 结果：读取 `references/subskills/implementation-qa.md`。
- 操作反馈、产品迭代、客户试点、上线准备：读取 `references/subskills/iteration-pilot.md`。

## 4. 设计理念更新规则

开始开发或 QA 前，先读取现有 `DESIGN_PRINCIPLES.md` 和 `DECISIONS.md`，不得每次重新提炼。只有以下情况才执行设计理念子模块：
- 用户提出新的长期判断；
- 新意见与既有理念冲突；
- 多次反馈形成新的稳定规律；
- 用户明确要求重新总结理念。

有变化时先形成候选，用户确认后再写入事实库。

## 5. 统一决策文件

只使用：
- `DECISIONS.md`
- `OPEN_QUESTIONS.md`

不得另建 `PRODUCT_DECISIONS.md` 或 `OPEN_PRODUCT_DECISIONS.md`。决策条目必须包含来源与状态。开发补充的小交互只能以“开发补充 / 建议”登记，用户确认后才成为正式产品事实。

## 6. 功能验证是核心阶段

功能验证不是普通原型，也不是 QA。它的目标是在底层服务可模拟的前提下，把用户可见产品行为尽可能真实实现，使产品经理通过操作继续完成产品设计。

必须保证：
- 主功能至少 L3：可操作、有状态、加载、空、失败、取消、重试、刷新恢复；
- 关键跨端关系达到 L4；
- 多端共享统一模拟业务内核；
- 提供产品实验室和可复现场景；
- 禁止静态卡片、无响应按钮、Toast 冒充流程、TODO 和只做成功状态。

## 7. 共享专业模块

按任务读取：
- `references/modules/engineering-spec.md`
- `references/modules/ai-feature-spec.md`
- `references/modules/mock-validation-data.md`
- `references/modules/document-delivery.md`

共享模块只提供专业规范，不拥有产品事实写入权。

## 8. 完成与交接

每个专业子模块完成后，按交接契约列明：
- 已读取来源；
- 已生成产物；
- 用户已确认决定；
- AI 或开发补充建议；
- 未解决问题；
- 下游限制；
- 实际检查证据。

不得仅因为任务卡写了“已调用某模块”就声称完成。