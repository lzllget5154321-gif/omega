---
type: insight
tags: [omega-ecosystem, runtime-architecture, agent-os, deployment, system-identity]
created: 2026-05-15
updated: 2026-05-15
knowledge_stability: evolving
parent: [[omega生态系统项目-总说明]]
related:
  - [[Omega生态系统项目-功能优先总方法论]]
  - [[Omega Runtime Architecture]]
---

# Omega 运行形态与本体文件说明

> **核心判断**：Omega 不是一个代码文件、不是一个普通程序、不是一个 Obsidian 插件。它是一个运行在 Windows/macOS/Linux 之上的 **AI Agent 行动操作层（Agent OS Layer）**——它不替代底层操作系统，而是替你协调电脑中的各种 AI、Agent、工具、文件、网页、数据库和创作软件。

---

## 一、Omega 是什么：三位一体的运行形态

Omega 的正确形态不是单一实体，而是**三层协同**：

```
┌─────────────────────────────────────────────────────────────┐
│                    Omega Agent OS Layer                      │
│                                                               │
│  ┌─────────────────┐  ┌──────────────┐  ┌─────────────────┐ │
│  │  知识本体层       │  │  运行时层     │  │  数据与工具层    │ │
│  │  (Knowledge)     │  │  (Runtime)   │  │  (Data+Tools)   │ │
│  │                  │  │              │  │                 │ │
│  │  Obsidian Vault  │  │  Git 代码仓库 │  │  PostgreSQL     │ │
│  │  Markdown 文档   │  │  Python/TS   │  │  Qdrant         │ │
│  │  方法论/架构/    │  │  YAML 配置   │  │  浏览器/Playwright│ │
│  │  Agent定义/Skill │  │  Docker 沙箱 │  │  Blender/Manim  │ │
│  │  工具注册表/     │  │  CLI入口     │  │  Python/R       │ │
│  │  任务契约/记忆   │  │  MCP Server  │  │  Zotero/Obsidian│ │
│  │                  │  │  Web 操作台  │  │  ffmpeg/其他工具 │ │
│  └─────────────────┘  └──────────────┘  └─────────────────┘ │
│                                                               │
│  作用：                 作用：              作用：             │
│  保存"是什么"和        真正执行任务——      保存状态、日志、     │
│  "为什么"——系统的      路由、调工具、      向量索引、输出成果， │
│  长期记忆和设计蓝图     跑脚本、操作浏览器   连接外部工具世界    │
└─────────────────────────────────────────────────────────────┘
```

### 1.1 知识本体层（Obsidian Vault）

| 内容 | 形式 | 作用 |
|------|------|------|
| 项目方法论与核心原则 | `01-方法论/*.md` | 定义 Omega 是什么、为什么 |
| 架构设计与组件定义 | `02-架构/*.md` | 九层架构、Router、Planner、循环 |
| Agent 定义与分工 | `02-架构/` + Agent 社会 | 谁负责什么任务 |
| Skill 库 | `05-Skill库/` | 已验证的"怎么做"程序 |
| 工具注册表 | `10-外部AI与工具注册表/` | 外部 AI 和工具的完整档案 |
| 任务契约模板 | `04-任务契约与成果包/` | 任务如何被定义和交付 |
| 行动记忆历史 | Action Memory 记录 | 历史任务的完整执行过程 |

### 1.2 运行时层（Git 代码仓库）

| 内容 | 形式 | 作用 |
|------|------|------|
| 系统入口 | `omega cli` / `omega daemon` / `omega web` | 用户与 Omega 交互的界面 |
| 任务路由引擎 | Python/TS 模块 | 执行 Tool-Agent Router 的评分和选择 |
| 工具适配器 | MCP Server / Python SDK 封装 | 将外部工具抽象为标准化能力 |
| 任务编排器 | LangGraph / Agents SDK | 管理多步骤任务的执行和状态 |
| 安全沙箱 | Docker 容器 | 隔离不信任代码的执行 |
| 浏览器自动化 | Playwright 脚本 | Computer Use-Lite 的实现 |
| 配置与清单 | `omega.yaml` / `tools.yaml` / `mcp-config.json` | 系统的自我定义和工具清单 |

### 1.3 数据与工具层（外部生态系统）

| 内容 | 形式 | 作用 |
|------|------|------|
| 结构化记忆 | PostgreSQL | 行动记忆、工具信誉、任务日志 |
| 语义搜索 | Qdrant | 向量索引——知识库语义检索 |
| 文件操作 | 本地文件系统 | 读取、写入、转换、组织文件 |
| 浏览器 | Playwright / Chrome | Computer Use——操作网页和封闭平台 |
| 代码执行 | Python / R / Node | 数据分析、脚本、自动化 |
| 3D/动画 | Blender / Manim | 科学可视化、动画制作 |
| 视频处理 | ffmpeg | 渲染、剪辑、格式转换 |
| 文献管理 | Zotero | 论文存储、引用管理、PDF 批注 |
| 外部 AI | Claude / GPT / NotebookLM / Perplexity | 语言理解、深度研究、代码生成 |

---

## 二、部署形态的演进路线

Omega 不需要第一天就建成完整形态。它按**生态演替**逐步从轻到重：

### 阶段 1：Omega-Lite（MFE 阶段）

```
Obsidian Vault + Claude Code + Python 脚本 + YAML 路由表 + Docker 沙箱 + Zotero + Playwright
```

**特点**：
- 还没有完整独立 App
- 但已经能通过 Claude Code 和脚本执行真实任务
- Tool-Agent Router 用静态 YAML 路由表
- 任务通过 Obsidian 笔记中的命令触发
- 成果写回 Obsidian

**适用场景**：在新电脑上快速搭建第一个可用版本，立即开始验证核心闭环。

### 阶段 2：Omega Local Runtime

```
本地后台服务 + Web/CLI 界面 + 数据库 + 工具适配器 + Agent 执行引擎
```

**新增**：
- `omega daemon` — 后台任务管理器（等待和执行任务）
- `omega cli` — 命令行入口（`omega task "帮我把这5篇PDF处理了"`）
- `omega web` — 本地网页操作台（任务状态/成果/审批）
- `omega.yaml` — 系统总配置
- `docker-compose.yml` — PostgreSQL + Qdrant + 沙箱服务

**适用场景**：MFE 验证通过后，将系统作为常驻后台服务运行。

### 阶段 3：Omega Desktop / Agent OS Shell

```
本地桌面应用（Tauri/Electron）或 Web 控制台
```

**包含的视图**：
- 任务输入区（自然语言 + 任务契约预览）
- 任务状态区（实时步骤 + 进度）
- 工具调用区（调用了哪些工具 + 状态）
- 成果包区（可交付成果 + 预览/下载）
- 审批区（需要确认的操作）
- 行动记忆区（历史任务复盘）
- Skill 晋升区（候选→活跃→退役管理）
- 工具雷达周报区（本周新发现）

**适用场景**：系统成熟后，作为完整的"AI 工作驾驶舱"使用。

---

## 三、Omega 的本体文件结构

新电脑上的完整项目目录：

```text
Omega-System/
│
├── omega-vault/                 ← Obsidian 知识本体（你当前的目录）
│   ├── CLAUDE.md
│   ├── .claude/
│   ├── .obsidian/
│   ├── wiki/
│   ├── raw/
│   ├── assets/
│   └── omega生态系统项目/       ← Omega 项目文件
│       ├── 00-总览/
│       ├── 01-方法论/
│       ├── 02-架构/
│       ├── 03-能力矩阵/
│       ├── 04-任务契约与成果包/
│       ├── 05-Skill库/
│       ├── 06-医学强化域/
│       ├── 07-旧版本归档/
│       ├── 08-运行时与原型/
│       ├── 09-功能基准任务花园/
│       ├── 10-外部AI与工具注册表/
│       └── 11-创意与科学可视化/
│
├── omega-runtime/               ← 真正运行的代码仓库（新建 Git 仓库）
│   ├── README.md
│   ├── pyproject.toml
│   ├── omega.yaml               ← 系统本体配置总表
│   ├── docker-compose.yml
│   ├── Makefile
│   ├── app/                     ← 应用入口
│   │   ├── cli.py               ← omega cli 命令
│   │   ├── daemon.py            ← omega daemon 后台服务
│   │   └── web/                 ← omega web 本地控制台
│   ├── agents/                  ← Agent 定义
│   │   ├── researcher.py
│   │   ├── data_analyst.py
│   │   ├── academic_writer.py
│   │   ├── coder.py
│   │   ├── critic.py
│   │   └── visualization/
│   ├── tools/                   ← 工具适配器
│   │   ├── pubmed_adapter.py
│   │   ├── zotero_adapter.py
│   │   ├── blender_adapter.py
│   │   ├── manim_adapter.py
│   │   └── browser_adapter.py
│   ├── routers/                 ← 路由引擎
│   │   ├── tool_agent_router.py
│   │   ├── stage_aware_router.py
│   │   └── routing_table.yaml
│   ├── planners/                ← 任务规划器
│   │   └── dynamic_task_planner.py
│   ├── mcp/                     ← MCP 配置
│   │   └── mcp-config.json
│   ├── schemas/                 ← 数据模式
│   │   ├── task_contract.py
│   │   ├── outcome_package.py
│   │   ├── action_memory.py
│   │   └── tool_registry.py
│   ├── skills/                  ← Skill 实现
│   │   └── *.py
│   ├── workflows/               ← Workflow 定义
│   │   └── *.yaml
│   ├── scripts/                 ← 独立脚本
│   │   ├── run_benchmark.py
│   │   ├── radar_scanner.py
│   │   └── import_zotero_pdfs.py
│   └── tests/                   ← 测试
│       ├── unit/
│       ├── integration/
│       └── benchmarks/
│
├── omega-data/                  ← 数据与记忆（独立于代码和 Vault）
│   ├── postgres/                ← PostgreSQL 数据目录
│   ├── qdrant/                  ← Qdrant 向量索引
│   ├── logs/                    ← 运行日志
│   │   ├── agent_logs/
│   │   ├── tool_logs/
│   │   └── system_logs/
│   ├── action-memory/           ← 行动记忆存储
│   ├── tool-reputation/         ← 工具信誉数据
│   └── vector-index/            ← 向量索引备份
│
├── omega-workspace/             ← 每次任务的工作区
│   ├── inbox/                   ← 未处理文件
│   ├── sandbox/                 ← Docker 沙箱挂载目录
│   ├── downloads/               ← 下载的临时文件
│   ├── outputs/                 ← 成果包输出
│   │   └── phagocytosis-demo/   ← 示例：细胞吞噬动画项目
│   ├── artifacts/               ← 中间产物
│   └── temp/                    ← 临时文件（自动清理）
│
├── omega-assets/                ← 媒体资产（图像/视频/3D）
│   ├── images/
│   ├── video/
│   ├── audio/
│   ├── blender/                 ← Blender 项目文件和资产
│   ├── manim/                   ← Manim 脚本和输出
│   └── generated/               ← AI 生成的视觉资产
│
└── backups/                     ← 定期备份
    ├── vault-backups/
    ├── data-backups/
    └── config-backups/
```

### 三层之间的关系

```
omega-vault/（知识本体）  ←── 方法论定义"要做什么"
        │                        │
        │  引用和指导              │  记录和沉淀
        ↓                        ↓
omega-runtime/（代码运行时） ←── 真正执行任务
        │                        │
        │  读写                    │  生成
        ↓                        ↓
omega-data/（数据记忆）     ←── 持久化状态
omega-workspace/（工作区）  ←── 任务产物
omega-assets/（媒体资产）   ←── 视觉/音频/3D资产
```

---

## 四、新旧电脑之间的迁移

将 Omega 从当前电脑迁移到新电脑时：

### 需要迁移的

| 内容 | 从 | 到 | 方式 |
|------|----|----|------|
| **知识本体（Vault）** | 当前 `D:\obsidian\lzl的个人知识库\` | 新电脑 `Omega-System/omega-vault/` | Git clone 或直接复制 |
| **项目蓝图** | `omega生态系统项目/` | `omega-vault/omega生态系统项目/` | 同上（已包含在 Vault 中） |
| **CLAUDE.md** | 当前 Vault 根 | 新 Vault 根 | 直接复制 + 路径适配 |

### 需要新创建的

| 内容 | 位置 | 说明 |
|------|------|------|
| `omega.yaml` | `omega-runtime/` | 系统本体配置——新电脑上从头写 |
| `omega-runtime/` 代码仓库 | `Omega-System/omega-runtime/` | Git init 新仓库 |
| `omega-data/` 目录 | `Omega-System/omega-data/` | 空目录初始化 |
| `omega-workspace/` 目录 | `Omega-System/omega-workspace/` | 空目录初始化 |
| `omega-assets/` 目录 | `Omega-System/omega-assets/` | 空目录初始化 |

### 不需要迁移的

- 当前电脑的系统路径配置（`D:\obsidian\...` → 新电脑使用新路径）
- `raw/09-archive/` 中的已处理文件（可选择性迁移）
- 临时文件、缓存
- `.obsidian/` 中的本地插件配置（在新电脑上重新配置）

---

## 五、核心原则重申

1. **Omega 不是程序，是操作系统层**——它运行在 OS 之上，协调下层工具
2. **三层协同，不可缺一**——知识本体（定义）+ 运行时（执行）+ 数据层（记忆）
3. **从轻到重演进**——Omega-Lite → Local Runtime → Desktop Shell
4. **Obsidian 是知识本体，不是唯一本体**——真正的 Omega 本体包括代码、配置、数据、工具
5. **新电脑上大胆设计**——不因当前电脑配置限制想象力，按"本地强工作站 + 云 API 混合"规划

---

## 六、相关页面

- [[Omega生态系统项目-功能优先总方法论]] — 完整的方法论定义
- [[Omega Runtime Architecture]] — 运行时层的详细架构设计
- [[Omega Manifest Schema]] — `omega.yaml` 的完整 schema 定义
- [[omega生态系统项目-总说明]] — 项目总览和快速导航
