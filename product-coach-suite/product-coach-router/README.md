# 产品教练 Skill

`product-coach-router` 是本仓库唯一正式安装入口，中文显示名为“产品教练”。

它通过一个薄总控协调六个生命周期专业模块：

1. 产品调研、需求发现与方向决策
2. 产品设计理念提炼
3. 产品功能 PRD
4. 产品功能验证与设计验证开发
5. 产品实现 QA
6. 产品迭代、试点与上线

并按需加载四个共享专业模块：产品工程规格、AI 功能规格、模拟数据与验证场景、产品文档交付。

## 使用原则

- 先读取项目事实库与已确认决定，再执行本轮任务。
- 总控只负责路由、协调和交接检查，不替代专业模块。
- 未经用户确认，不得修改正式产品事实。
- 正式 PRD 必须保持来源忠实、流程完整、功能可实现、异常可恢复。
- 功能验证必须覆盖主功能 L3、关键跨端闭环 L4、统一模拟业务内核和产品实验室。
- 任何完成声明都必须对应真实产物与检查证据。

## 入口文件

- `SKILL.md`：总控与模块路由
- `agents/openai.yaml`：ChatGPT 显示信息
- `references/shared/`：权威、职责、保留、交接与输出规则
- `references/subskills/`：六个生命周期专业模块
- `references/modules/`：四个共享专业模块
- `references/preserved/`：经验证保留的 PRD、功能验证、QA 与迭代资产
- `assets/templates/`：正式交付模板
- `assets/project-state-templates/`：项目事实库模板
- `scripts/`：结构与质量审查脚本
- `tests/`：回归测试资料

## 安装与验证

通过仓库 Actions 中的 **Build Product Coach Skill** 下载最新成功构建工件 `product-coach-skill-installable`，然后上传到 ChatGPT `/skills`。

本地验证：

```bash
python scripts/validate_skill.py .
python scripts/self_test.py
python scripts/package_skill.py
```

公开仓库不保存真实客户资料或完整私有 PRD。优秀私有文档只允许用于临时校准，不自动写回仓库，也不限制未来质量上限。
