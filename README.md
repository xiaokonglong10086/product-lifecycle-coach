# 产品教练（Product Coach Router）

这是面向完整产品开发生命周期的 ChatGPT Skill。用户只安装一个入口：`product-coach-router`，中文显示名为“产品教练”。

它负责根据当前任务读取项目事实库、判断所处阶段、选择对应专业模块，并完成从需求发现到试点上线的真实产品工作。总控只负责路由、权威管理与交接检查，不用摘要替代专业产物。

## 当前能力

- 客户会议、用户访谈、需求发现与产品方向判断
- 长期产品设计理念的提炼、冲突检查与确认后维护
- 唯一正式产品功能 PRD
- 产品工程规格与 AI 功能规格
- 全功能产品设计验证与 Codex 开发包
- L3 主功能、L4 关键跨端闭环与隐藏产品实验室
- 实现 QA、反馈分类、产品迭代、客户试点与上线准备
- 产品经理学习日志与关键判断复盘

## 核心原则

1. 用户本轮明确决定优先，未经确认不得修改产品事实。
2. 先读取已有资料、设计理念、决定和当前实现，再提出问题或生成新文档。
3. PRD、工程规格、AI 规格、模拟数据和 QA 各自负责自己的内容，不互相越权。
4. 功能验证不是静态 Demo：用户可见行为必须真实可操作，底层服务才允许模拟。
5. 所有主功能至少达到 L3，关键跨端闭环达到 L4，并覆盖加载、空、失败、取消、重试、撤销和刷新恢复。
6. 完成声明必须有真实文件、命令、构建、审查或运行证据。
7. 公开仓库只保存通用规则、模板、脚本和虚构示例，不保存真实客户资料或完整私有 PRD。

## 仓库中的正式 Skill

```text
product-coach-suite/
└─ product-coach-router/
   ├─ SKILL.md
   ├─ agents/openai.yaml
   ├─ references/
   │  ├─ shared/       # 权威、职责、保留、交接与输出规范
   │  ├─ subskills/    # 六个生命周期专业模块
   │  ├─ modules/      # 工程、AI、模拟数据、文档交付模块
   │  └─ preserved/    # 已验证的 PRD、功能验证与 QA 核心资产
   ├─ assets/
   │  ├─ templates/    # PRD、Codex、QA、迭代与项目事实库模板
   │  └─ project-state-templates/
   ├─ scripts/         # 结构、PRD、保留资产和开发任务审查
   └─ tests/
```

根目录不再保留旧版 `product-lifecycle-coach` Skill。历史内容仍可通过 Git 记录查看，但不再作为当前运行入口。

## 安装

1. 打开仓库的 **Actions**。
2. 进入 **Build Product Coach Skill** 的最新成功运行。
3. 下载 `product-coach-skill-installable` 构建工件。
4. 将下载的 ZIP 上传到 ChatGPT 的 `/skills` 页面。
5. 安装后使用“调用产品教练”或直接提出调研、PRD、功能验证、QA、迭代、试点等任务。

Skill 的正式名称必须显示为：

```yaml
name: product-coach-router
```

## 使用示例

```text
调用产品教练。整理这次客户会议，区分事实、观点、诉求、决定和待确认问题，并判断是否已经可以进入产品设计。
```

```text
调用产品教练。基于当前权威资料生成唯一正式产品功能 PRD，不得修改已经确认的页面、字段、流程、AI 规则和数据去向。
```

```text
调用产品教练。基于主 PRD 和当前代码生成全功能设计验证开发包，主功能达到 L3，关键跨端闭环达到 L4，并建立可复现的产品实验室。
```

```text
调用产品教练。实际运行并验收当前项目，区分产品问题、实现缺陷、体验问题和生产能力差距。
```

## 本地验证

```bash
python product-coach-suite/product-coach-router/scripts/validate_skill.py product-coach-suite/product-coach-router
python product-coach-suite/product-coach-router/scripts/self_test.py
python product-coach-suite/product-coach-router/scripts/package_skill.py
```

## 隐私与公开边界

本仓库不会上传完整“小阿平台 PRD”或其他真实项目文档。PRD 质量通过通用质量规约、虚构正反例、审查脚本和可选的私有临时校准实现。临时提供的私有样本只用于当轮校准，不自动写回公开仓库，也不定义未来质量上限。

## 许可

MIT License。详见 `LICENSE`。