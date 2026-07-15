# 独立审查量表

审查的目标是阻止下一阶段在错误或模糊基线上继续。先给门禁结论，再给分级问题；能直接修的细节应修进文档。

## 1. 证据与战略
- 目标用户、问题和现有替代是否具体；
- 事实、推断和假设是否分开；
- 是否存在反向证据；
- 产品目标是否与组织价值一致；
- 最强的“不做理由”是否被正视；
- 成功指标是否可解释、可采集且不易被游戏化。

## 2. 概念完整性
- 是否比较过机制不同的方案；
- 选定方案的价值机制是否成立；
- 核心闭环、角色、系统边界和信任模型是否清楚；
- MVP 是否仍然能验证假设；
- 非目标和拒绝方案是否记录；
- 风险与未决事项是否会使落地需求失去意义；
- 是否有明确确认记录。

## 3. 概念到落地的一致性
- PRD 是否引用明确的批准概念版本；
- 产品概述、目标用户、核心机制和范围是否保持一致；
- 新增内容是否属于细化，而不是未经批准的概念变更；
- 概念中的重要定性要求是否在功能、UX、规则或文案中得到承接；
- 被删除或变更的内容是否有决策记录。

## 4. 落地 PRD
- 主文档是否严格使用 1—8 固定结构，文档信息是否未编号；
- 是否混入第 9/10/11 节、工程规格、API、事件、QA 或大篇附录；
- 主流程和 1—2 个高影响异常是否可见；
- 功能树是否同时区分 🔴核心、🟡重要、⚪未来；
- 是否有一个清晰的关键页面 ASCII 线框；
- 每个核心功能是否固定按“功能描述与触发条件、交互细节、状态清单、边界条件、数据规范”展开；
- 状态是否覆盖默认、加载中、成功、失败、禁用、空状态；
- 边界是否覆盖空内容、超长、网络异常、无权限、并发、格式不符；
- 数据表是否只承载产品字段合同，而非数据库/API/代码实现；
- 第 6 节是否同时包含整体文案风格和终端用户最终文案；
- 第 7 节是否覆盖性能、权限、兼容性、数据安全和数据存储；
- `[待补充]` 是否有影响、负责人、阻塞节点和临时假设；
- 是否达到拆分条件：超过 8 个核心功能、跨三个端、正文超过可读阈值；
- 空白上下文团队是否仍需自行发明产品逻辑。

## 5. UX 与内容
- 每个重要需求是否落到页面/触点；
- 信息层级是否服务核心任务；
- 默认、首次、空、加载、处理中、成功、部分成功、失败、禁用、无权限和恢复是否覆盖；
- 移动端、键盘、无障碍和响应式是否按场景处理；
- 文案是否解释状态、影响和下一步；
- PRD、UX 规格和原型是否存在冲突。

## 6. 空白上下文工程师
- 产品行为与技术实现是否分界清楚；
- 数据语义、来源、校验、权限、历史和异常是否明确；
- 状态机、并发、幂等、重试和回滚是否按风险覆盖；
- 接口、依赖和兼容性是否可实施；
- 是否检查了现有代码和模式；
- 每个核心需求是否映射到任务与验证；
- 是否禁止无关重构和功能发明。

## 7. QA 与验收
- 主流程、替代流程、失败、边界、权限和恢复是否可测试；
- 验收条件是否可观察、可复现；
- 测试数据、环境和前置状态是否可构建；
- 回归范围是否覆盖受影响旧功能；
- 关键 NFR 是否有验证方式和阈值；
- 发布完成是否依赖真实证据而非开发自报。

## 8. AI 产品
- AI 是否真的必要；
- 输入、来源、新鲜度、权限和上下文组装是否明确；
- 确定性步骤和模型步骤是否分开；
- 输出 schema、证据、不确定性和禁止行为是否明确；
- 人工确认、覆盖、申诉和最终责任是否合理；
- 评估集、指标、阈值和错误严重性是否定义；
- 无证据、低质量、模型失败、工具失败和安全阻断是否有降级；
- 延迟、成本、隐私、提示注入、版本和审计是否处理；
- Agent 工具权限、停止条件和可逆性是否受控。

## 9. 运营与企业环境
- 买方、管理员、运营、支持、安全和审批角色是否覆盖；
- 配置、发布、升级、迁移、租户隔离和客户差异是否可管理；
- 审计、人工纠错和数据责任是否明确；
- 支持、告警、升级和事故响应是否可执行；
- 产品价值是否被高实施成本或人工服务成本抵消。

## 10. 产品经理成长适配
- 工作是否被 AI 全部包办而没有留下关键判断；
- 教练内容是否围绕当前决策而非泛化讲课；
- 用户是否知道为什么进入当前阶段、下一步是什么；
- 是否逐步让用户承担适合其水平的判断；
- 交付质量是否因教学而下降。

## 问题格式

```markdown
### [BLOCKER|HIGH|MEDIUM|LOW] 问题标题
- 审查视角：
- 证据：文档章节/需求 ID/来源
- 问题：
- 后果：
- 修正方案：
- 处理：已修复 / 需讨论 / 延后（负责人+条件） / 接受风险
```

## 门禁结论

- **PASS：** 可进入下一阶段；仅有不影响执行的细节。
- **PASS WITH CONCERNS：** 可继续，但风险有明确负责人、条件和截止节点。
- **FAIL：** 存在阻塞项，继续会产生高概率返工、错误实现或不可接受风险。

审查后重新检查受影响章节和跨文档一致性，不要只在末尾追加问题清单。

## Baseline integrity lens
- Were all material sources inventoried across available locations?
- Are content version, approval status, and authority distinguished from file timestamps?
- Are the current product direction, product rules, and code reality explicit?
- Are conflicts, superseded documents, and code drift recorded rather than silently merged?
- Does the next task follow the earliest unpassed gate?

## Artifact migration lens
- Does each source section have a destination or explicit archive/rejection reason?
- Are product behavior, AI rules, engineering mechanics, traceability, and QA gates separated without losing decisions?
- Are requirement IDs and old-to-new mappings preserved?
- Can a blank-context reader find the governing answer without reading the old mixed document?

## Complex program and slice lens
- Does the product map distinguish stable core rules, adjustable strategy, and experiments?
- Is the active slice independently valuable, demonstrable, testable, and reversible?
- Does it reduce a material uncertainty or unlock dependencies?
- Are out-of-scope domains protected from incidental changes?

## Code and portability lens
- Were actual code patterns and current behavior inspected?
- Are build failure categories distinguished: code, dependency, OS/native binding, packaging, configuration?
- Were bundled dependencies rejected as cross-platform proof?
- Are preserved implementation assets and forbidden refactors explicit?
