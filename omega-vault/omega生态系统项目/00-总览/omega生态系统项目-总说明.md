---
type: insight
tags: [omega-ecosystem, project-overview, entry-point]
created: 2026-05-15
updated: 2026-05-15
knowledge_stability: evolving
version: v3.1
---

# omega生态系统项目 — 总说明

> **一句话**：omega生态系统项目是一个**功能优先的个人 AI Agent 行动生态系统**——它强在感知外部世界、学习新工具、协调外部工具、操作软件平台、沉淀经验、形成 Skill、持续进化。

---

## 快速导航

| 你想了解什么 | 去这里 |
|-----------|--------|
| **项目是什么、理念、原则、架构** | → [[omega生态系统项目-功能优先总方法论]] |
| **Omega 到底是什么运行形态** | → [[Omega运行形态与本体文件说明]] |
| **版本怎么从 V2 演化为 Omega** | → [[omega生态系统项目-版本演化图]] |
| **第一版（MFE）需要什么** | → [[MFE最小功能生态]] |
| **怎么接入外部工具** | → [[Capability Fabric]] |
| **怎么学会新工具** | → [[Toolsmith-Lite与Skillsmith]] |
| **Agent 怎么分工** | → [[Productive Agent Society]] |
| **医学研究怎么做** | → [[医学研究生产系统]] |
| **创意/动画/可视化怎么做** | → [[科学动画生产系统]] + [[Creative Tool Router]] |
| **安全怎么保障** | → [[Safety-as-Enabler]] |
| **任务怎么被执行的** | → [[Ω行动中枢]] + [[Action Brain]] |
| **怎么拆解复杂任务** | → [[Dynamic Task Planner：动态任务规划器]] |
| **怎么选最佳工具和 Agent** | → [[Tool-Agent Router：最佳工具与最佳执行者选择器]] + [[Stage-Aware Tool-Agent Router]] |
| **系统不会时怎么自己求助** | → [[自我解惑与外援调用循环]] |
| **怎么跟踪 AI 世界的新工具** | → [[AI工具生态雷达]] |
| **怎么评估工具真实能力** | → [[Tool Benchmark Cards]] |
| **工具/模型怎么自动升级替换** | → [[Model and Tool Lifecycle Manager]] + [[Auto-Upgrade Policy]] |
| **怎么从社交平台提取可信信号** | → [[Social Signal Validator]] |
| **怎么找到并使用工具的最佳实践** | → [[Best-Practice Harvester：最佳实践采集器]] |
| **外部 AI 工具谁擅长什么** | → [[External AI Rolebook]] |
| **工具信息怎么分权威等级** | → [[SOTA Source Hierarchy：顶尖工具来源分级]] |
| **任务成果怎么交付** | → [[Multimodal Outcome Package]] |
| **在新电脑上怎么从零构建 Omega** | → [[Omega 构建指导书 — 给 Codex 的系统构造规范]] 🆕 |
| **交给 Codex 的完整构建包在哪** | → [[../99-交付给Codex的构建包/README]] 🆕（含 schema/config/fixtures/scripts） |
| **旧版文档在哪** | → [[07-旧版本归档/]] |

---

## 项目结构

```
omega生态系统项目/
├── 00-总览/              ← 你在这里
│   ├── omega生态系统项目-总说明.md
│   ├── Omega运行形态与本体文件说明.md
│   ├── omega生态系统项目-版本演化图.md
│   └── Omega 构建指导书 — 给 Codex 的系统构造规范.md  🆕 v3.0
├── 01-方法论/             ← 核心方法论文档
│   └── omega生态系统项目-功能优先总方法论.md (2000+ 行深度报告)
├── 02-架构/               ← 九层架构各层详解
│   ├── Tool-Agent Router：最佳工具与最佳执行者选择器.md
│   ├── Stage-Aware Tool-Agent Router.md
│   ├── Dynamic Task Planner：动态任务规划器.md
│   ├── Best-Practice Harvester：最佳实践采集器.md  🆕 v3.0
│   └── 自我解惑与外援调用循环.md
├── 03-能力矩阵/           ← MFE、工具图谱、封闭平台策略
│   ├── AI工具生态雷达.md
│   ├── SOTA Source Hierarchy：顶尖工具来源分级.md  🆕 v3.0
│   ├── Model and Tool Lifecycle Manager.md  🆕 v3.0
│   └── Social Signal Validator.md  🆕 v3.0
├── 04-任务契约与成果包/    ← 任务契约模板、成果包协议、行动记忆
│   └── Multimodal Outcome Package.md
├── 05-Skill库/            ← Skill Schema 和候选记录
├── 06-医学强化域/          ← 医学研究生产系统
├── 07-旧版本归档/          ← V2-V6 研究文档归档
├── 08-运行时与原型/        ← 实际脚本、CLI 原型、MCP 配置
│   ├── omega.yaml
│   ├── Omega Manifest Schema.md
│   ├── Omega Runtime Architecture.md
│   └── Auto-Upgrade Policy.md  🆕 v3.0
├── 09-功能基准任务花园/     ← 系统能力基准测试集（含非学术任务）
│   ├── README.md
│   └── Tool Benchmark Cards.md  🆕 v3.0
├── 10-外部AI与工具注册表/   ← 外部 AI 平台和工具档案
│   ├── README.md
│   └── External AI Rolebook.md  🆕 v3.0
├── 11-创意与科学可视化/     ← 科学动画与创意生产域
│   ├── 科学动画生产系统.md
│   └── Creative Tool Router.md  🆕 v3.0
├── 99-交付给Codex的构建包/   🆕 ← 交给新电脑 Codex 的完整构建套件（53 文件）
│   ├── AGENTS.md              ← Codex 自动读取的项目约定+凭据规则+构建边界
│   ├── CODEX_RUN_PROMPT.md    ← 给 Codex 的优化初始提示词模板
│   ├── BUILD_CHECKLIST.md     ← 四迭代逐项验收清单（双沙箱策略）
│   ├── README.md              ← 人类可读的交付说明（Windows 原生 + WSL2 双路径）
│   ├── MANIFEST.yaml          ← 53 个文件的完整性清单
│   ├── config/
│   │   ├── tools.yaml         ← 17 个种子工具注册表（含凭据获取指引）
│   │   ├── agents.yaml        ← 11 个种子 Agent 注册表
│   │   ├── .env.example       ← 16 个环境变量模板（[REQUIRED]/[OPTIONAL] + 获取 URL）
│   │   ├── routing_table.yaml ← 11 种任务类型 × 多阶段冷启动路由表
│   │   ├── stage_weights.yaml ← 8 阶段 × 12 维度动态权重覆盖
│   │   └── risk_policy.yaml   ← 四域风险升级策略 + 替换决策矩阵 + 回滚规则
│   ├── schemas/
│   │   ├── task_contract.schema.json      ← 任务契约 JSON Schema
│   │   ├── tool_card.schema.json          ← 工具卡 JSON Schema
│   │   ├── agent_card.schema.json         ← Agent 卡 JSON Schema
│   │   ├── outcome_package.schema.json    ← 多模态成果包 JSON Schema
│   │   ├── skill.schema.json              ← Skill 沉淀记录 JSON Schema
│   │   └── action_memory.schema.json      ← 行动记忆 JSON Schema
│   ├── fixtures/
│   │   ├── tasks/
│   │   │   ├── literature_ingestion_task.md ← 闭环 1 验收（Zotero 条件同步）
│   │   │   ├── data_analysis_task.md        ← 闭环 3 验收
│   │   │   ├── tool_comparison_task.md      ← 闭环 10 验收
│   │   │   └── tool_learning_task.md        ← 闭环 11 验收（双沙箱策略）
│   │   └── data/
│   │       └── sample_clinical.csv          ← 20 行模拟临床数据（含缺失值）
│   ├── templates/
│   │   ├── docker-compose.yml               ← PostgreSQL+Qdrant+双沙箱编排
│   │   ├── Dockerfile.sandbox               ← Execution Sandbox（无网络）
│   │   ├── Dockerfile.sandbox-net           ← Toolsmith Sandbox（有限网络）
│   │   └── mcp-config.json                  ← 7 个 MCP Server 配置模板
│   └── scripts/
│       ├── setup.ps1          ← Windows 环境一键配置脚本（6 步）
│       ├── assemble_package.ps1 ← 交付前完整性检查脚本
│       └── sandbox-net-filter.sh ← omega-sandbox-net 网络过滤（iptables）
```

---

## 核心简记

- **主干**：感知 → 工具 → 行动 → 产出 → 沉淀 → 进化
- **后台**：权限 → 沙箱 → 谱系 → 评估 → 主权保护 → 回滚
- **第一原则**：风险改变执行路径，不取消功能目标
- **第一目标**：证明自己像一个真正会使用工具工作的智能生态

---

## 版本

- 当前版本：v3.1（2026-05-15）
- v1.0：功能优先总方法论发布（2007 行）
- v1.1：三大核心机制补全——Tool-Agent Router、自我解惑与外援调用循环、AI 工具生态雷达
- v2.0：Agent OS Layer 化——运行形态定义、omega.yaml 本体配置、Stage-Aware Router、Dynamic Task Planner、创意与科学可视化域、多模态成果包、非学术基准任务
- v3.0：信息质量与生态演化机制补全——SOTA 来源四级体系、Best-Practice 自动采集器、工具/模型全生命周期管理、社交信号验证器、工具基准任务卡、创意专用路由器、外部 AI 角色手册、自动升级替换策略。共 8 个关键机制页面，覆盖"如何评估信息质量 → 如何使用工具的最佳方式 → 如何自动跟踪和替换工具 → 如何客观评测工具能力"的全闭环
- v3.1：Codex 构建包全面升级——新增 schema/（3→6 个 JSON Schema）、config/（3→6 个：新增 routing_table/stage_weights/risk_policy）、fixtures/（新增 tool_learning_task.md）、templates/（4 个：docker-compose + 双 Dockerfile + mcp-config）、BUILD_CHECKLIST.md（双沙箱策略）、CODEX_RUN_PROMPT.md、scripts/（含 sandbox-net-filter.sh）。修复：Codex Windows 原生安装说明、Zotero 条件同步、双沙箱网络隔离。构建包从 3 个文件扩展到 28 个文件完整交付套件
- 前身：AI Agent生态系统终极研究 V2→V3→V4→V5→V6
- 纠偏文档：[[omega生态系统项目-优化方法论-v0.1]]
