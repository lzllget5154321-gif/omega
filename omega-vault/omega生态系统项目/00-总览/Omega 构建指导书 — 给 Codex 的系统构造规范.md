---
type: concept
tags: [omega-ecosystem, construction-guide, deployment, codex, mfe, bootstrap]
created: 2026-05-15
updated: 2026-05-15
knowledge_stability: evolving
parent: [[omega生态系统项目-总说明]]
related:
  - [[Omega运行形态与本体文件说明]]
  - [[Omega Runtime Architecture]]
  - [[omega.yaml]]
  - [[MFE最小功能生态]]
---

# Omega 构建指导书 — 给 Codex 的系统构造规范

> **本文档的读者是 AI 构建 Agent（Codex / Claude Code）**。它定义了如何在一个全新的 Windows 电脑上，从零构建 Omega 系统的 MFE（最小功能生态）版本。
>
> **关键前提**：这不是传统软件的部署手册（已有代码→安装→配置→运行）。这是**AI 辅助构造规范**——目前只有完整的设计蓝图（24 个 Markdown 文件），需要在你的帮助下从 `git init` 开始构建整个运行时。

---

## 0. 构建前必读

### 0.1 你要构建的到底是什么

Omega 是一个三层 Agent OS Layer：

```
知识本体层（Obsidian Vault）  ← 24 个设计文件已就绪，你正在读
运行时层（omega-runtime/）    ← 你要构建的：Python 包 + CLI + Agent 引擎 + MCP 配置
数据与工具层（外部生态）       ← 你要配置的：Docker 服务 + 外部 API + 工具适配器
```

### 0.2 约束原则

1. **所有路径必须在 D 盘**：`D:\Omega-System\`
2. **MFE 优先**：不是一次性构建全部 24 个文件描述的所有功能，而是先构建能跑通 6 个基准闭环的最小版本
3. **代码即文档**：你写的每个 Python 模块必须有 docstring 和类型注解
4. **可复现优先**：所有依赖锁定精确版本，所有配置写成文件
5. **安全边界不可逾越**：不自动提交表单、不绕过认证、不存储明文密钥

### 0.3 你需要先读完的文件（按优先级）

| 优先级 | 文件 | 原因 |
|--------|------|------|
| P0 | `AGENTS.md`（build-package/） | 项目约定、凭据规则、技术栈锁定、构建边界 |
| P0 | `omega生态系统项目-功能优先总方法论.md` | 理解系统总纲 |
| P0 | `Omega运行形态与本体文件说明.md` | 理解三层架构 + 目录树 |
| P0 | `Omega Runtime Architecture.md` | 理解 11 组件数据流 |
| P0 | `config/tools.yaml` + `config/agents.yaml` | 种子工具和 Agent 注册表——每条必须符合 schema |
| P0 | `config/.env.example` | 检查 REQUIRED 环境变量是否已设置 |
| P1 | `omega.yaml` + `Omega Manifest Schema.md` | 理解系统配置 |
| P1 | `Tool-Agent Router：最佳工具与最佳执行者选择器.md` | 核心路由算法 |
| P1 | `Dynamic Task Planner：动态任务规划器.md` | 任务分解算法 |
| P2 | `Auto-Upgrade Policy.md` | 工具替换安全规则 |
| P2 | `External AI Rolebook.md` | 外部 AI 生态位 |
| — | `BUILD_CHECKLIST.md`（build-package/） | 每迭代完成后逐项检查——不读则无法验收 |

---

## 1. 前置要求：用户必须在你开始前完成的操作

> ⚠️ **这些操作 Codex 无法替用户做——需要人工操作或凭据。**

### 1.1 基础软件安装

```powershell
# 在 PowerShell（管理员）中执行：

# 1. 安装 winget（Windows 11 自带，Windows 10 需手动安装）
# 验证: winget --version

# 2. 安装 Python 3.12
winget install Python.Python.3.12 --silent
# 验证: python --version  → Python 3.12.x

# 3. 安装 Node.js 22 LTS
winget install OpenJS.NodeJS.LTS.22 --silent
# 验证: node --version  → v22.x.x

# 4. 安装 Git
winget install Git.Git --silent
# 验证: git --version

# 5. 安装 Docker Desktop
winget install Docker.DockerDesktop --silent
# 手动操作：启动 Docker Desktop，等待鲸鱼图标变绿
# 验证: docker --version

# 6. 安装 Visual Studio Code（推荐，非必须）
winget install Microsoft.VisualStudioCode --silent
```

### 1.2 用户必须提供的凭据和账号

| 凭据 | 用途 | 用户操作 |
|------|------|---------|
| **Anthropic API Key** | Claude API（核心语言引擎） | 访问 https://console.anthropic.com/ → 创建 API Key |
| **OpenAI API Key** | 备选引擎 + Codex CLI（如用户选择用 Codex） | 访问 https://platform.openai.com/api-keys |
| **GitHub Personal Access Token** | GitHub MCP Server + 私有仓库访问 | GitHub → Settings → Developer settings → Tokens (classic) → repo + workflow 权限 |
| **PubMed API Key**（可选） | 学术文献检索（无 Key 则限速 3 req/s） | 访问 https://www.ncbi.nlm.nih.gov/account/ → API Key Management |
| **Zotero 账号**（如使用 Zotero 同步） | 文献管理同步 | Zotero → Preferences → Sync |

> 用户应将以上 Key 写入 `D:\Omega-System\.env` 文件（不提交到 Git）：
> ```ini
> ANTHROPIC_API_KEY=sk-ant-...
> OPENAI_API_KEY=sk-...
> GITHUB_TOKEN=ghp_...
> PUBMED_API_KEY=...
> ```

### 1.3 构建 Agent 选择（二选一）

**方案 A：Claude Code + Windows 原生（推荐）**

```powershell
# Claude Code 原生支持 Windows，无需 WSL2
npm install -g @anthropic-ai/claude-code
# 验证: claude --version
```

> Claude Code 可以接入 DeepSeek API 作为后端引擎，不强制需要 Anthropic API Key。
> 详见 `build-package/config/.env.example` 中的 DEEPSEEK_API_KEY 配置。

**方案 B：Codex CLI + WSL2**

```powershell
wsl --install -d Ubuntu-24.04
# 重启电脑
# 在 Ubuntu 中:
npm install -g @openai/codex
```

> **推荐方案 A**。本构建包同时兼容两种 Agent。如用户已预装 WSL2 + Ubuntu + Node.js，方案 B 同样可用。

---

## 2. D 盘目录结构：你要创建的一切

```
D:\Omega-System\
├── .env                          ← 环境变量（不入 Git）
├── .gitignore
│
├── omega-vault\                  ← 知识本体层（Obsidian Vault）
│   ├── .obsidian\                ← Obsidian 配置（用户自行初始化）
│   ├── CLAUDE.md                 ← Claude 行为配置（从此项目复制）
│   ├── .claude\                  ← Claude Code 系统配置
│   │   └── skills\               ← Skill 定义
│   ├── wiki\                     ← 知识库（用户迁移）
│   ├── assets\                   ← 媒体资源
│   ├── raw\                      ← 原始资料
│   └── omega生态系统项目\        ← Omega 设计蓝图（24 个文件）
│
├── omega-runtime\                ← 运行时层（你要构建的核心）⚠️ 新建 Git 仓库
│   ├── .git\
│   ├── README.md
│   ├── pyproject.toml            ← Python 包定义
│   ├── omega.yaml                ← 系统本体配置（从设计文档照写）
│   ├── Makefile                  ← 常用命令快捷方式
│   ├── docker-compose.yml        ← 本地服务编排
│   │
│   ├── app\                      ← 应用主目录
│   │   ├── __init__.py
│   │   ├── main.py               ← CLI 入口：omega 命令
│   │   ├── config.py             ← 配置加载器（读 omega.yaml + .env）
│   │   │
│   │   ├── gateway\              ← Task Gateway
│   │   │   ├── __init__.py
│   │   │   ├── task_gateway.py   ← 自然语言 → Task Contract
│   │   │   └── contract.py       ← Task Contract 数据类
│   │   │
│   │   ├── planner\              ← Dynamic Task Planner
│   │   │   ├── __init__.py
│   │   │   ├── planner.py        ← 7 步规划流程
│   │   │   ├── templates\        ← 任务模板 YAML
│   │   │   │   ├── review_synthesis.yaml
│   │   │   │   ├── data_analysis.yaml
│   │   │   │   ├── code_generation.yaml
│   │   │   │   └── medical_research.yaml
│   │   │   └── dag.py            ← DAG 生成器
│   │   │
│   │   ├── router\               ← Tool-Agent Router
│   │   │   ├── __init__.py
│   │   │   ├── router.py         ← 12 维评分引擎
│   │   │   ├── stage_router.py   ← Stage-Aware 权重覆盖
│   │   │   ├── creative_router.py ← 创意 5 维追加
│   │   │   └── routing_table.yaml ← 冷启动静态路由表
│   │   │
│   │   ├── safety\               ← Safety Enforcer
│   │   │   ├── __init__.py
│   │   │   ├── enforcer.py       ← 四域风险检查
│   │   │   └── sandbox.py        ← Docker 沙箱管理
│   │   │
│   │   ├── executor\             ← Agent 执行引擎
│   │   │   ├── __init__.py
│   │   │   ├── agent_runner.py   ← Agent 调度和状态管理
│   │   │   ├── claude_agent.py   ← Claude API 调用封装
│   │   │   ├── codex_agent.py    ← Codex CLI 调用封装
│   │   │   └── tool_adapter.py   ← 外部工具适配器基类
│   │   │
│   │   ├── toolsmith\            ← Toolsmith-Lite
│   │   │   ├── __init__.py
│   │   │   ├── learner.py        ← 工具学习闭环
│   │   │   └── adapter_gen.py    ← Adapter 生成器
│   │   │
│   │   ├── outcome\              ← Outcome Package
│   │   │   ├── __init__.py
│   │   │   ├── assembler.py      ← 成果组装
│   │   │   └── validator.py      ← 成果验证
│   │   │
│   │   ├── memory\               ← 记忆层
│   │   │   ├── __init__.py
│   │   │   ├── action_memory.py  ← 行动记忆（PostgreSQL）
│   │   │   └── knowledge_graph.py ← 知识图谱查询
│   │   │
│   │   ├── radar\                ← AI 工具生态雷达
│   │   │   ├── __init__.py
│   │   │   ├── scanner.py        ← 8 源扫描器
│   │   │   └── prelearn.py       ← 预学习队列
│   │   │
│   │   └── mcp\                  ← MCP 管理
│   │       ├── __init__.py
│   │       └── mcp_manager.py    ← MCP Server 生命周期
│   │
│   ├── mcp-servers\              ← MCP Server 配置
│   │   ├── mcp-config.json       ← Claude/Codex MCP 配置
│   │   └── servers.yaml          ← 自托管 MCP Server 列表
│   │
│   ├── schemas\                  ← 数据模式定义
│   │   ├── task_contract.json
│   │   ├── agent_message.json
│   │   └── outcome_package.json
│   │
│   ├── workflows\                ← LangGraph 工作流定义
│   │   ├── __init__.py
│   │   ├── ingest.py             ← /ingest 工作流
│   │   ├── research.py           ← 学术研究工作流
│   │   └── creative.py           ← 创意生产工作流
│   │
│   ├── scripts\                  ← 独立脚本
│   │   ├── setup.ps1             ← Windows 一键环境配置
│   │   ├── verify.ps1            ← 部署验证脚本
│   │   ├── run_benchmark.py      ← 基准任务执行器
│   │   └── backup.py             ← 备份脚本
│   │
│   └── tests\                    ← 测试
│       ├── __init__.py
│       ├── test_router.py
│       ├── test_planner.py
│       ├── test_safety.py
│       ├── test_gateway.py
│       └── benchmarks\           ← 基准测试
│           ├── test_bench_i1.py  ← 医学信息图基准
│           ├── test_bench_c1.py  ← 代码生成基准
│           └── ...
│
├── omega-data\                   ← 数据与状态层
│   ├── postgres\                 ← PostgreSQL 数据目录
│   ├── qdrant\                   ← Qdrant 向量数据
│   └── logs\                     ← 日志
│
├── omega-workspace\              ← 工作区
│   ├── temp\                     ← 临时文件
│   ├── sandbox\                  ← Docker 沙箱挂载点
│   └── outputs\                  ← 最终产出
│
└── omega-assets\                 ← 全局资产
    ├── zotero\                   ← Zotero PDF 本地副本
    ├── templates\                ← 通用模板
    └── fonts\                    ← 字体
```

### 精确的 `.gitignore`

```gitignore
# 环境
.env
*.pyc
__pycache__/
*.egg-info/
dist/
build/

# 数据
omega-data/
*.db
*.sqlite3

# 工作区
omega-workspace/

# IDE
.vscode/
.idea/

# Docker
postgres-data/
qdrant-data/

# OS
.DS_Store
Thumbs.db
```

---

## 3. MFE 分阶段构建计划

按 Omega 路线图的阶段 1（先锋物种 / MFE），分 **4 个迭代**，每个迭代 ~1 周：

```
迭代 0: 骨架搭建         ← 目录结构 + 配置 + Python 包 + CLI 入口
迭代 1: 核心路由与规划     ← Router + Planner + Task Gateway
迭代 2: 执行与安全         ← Safety Enforcer + Agent Runner + Docker 配置
迭代 3: 闭环验证          ← 6 个基准闭环全部跑通 + 文档
```

### 迭代 0：骨架搭建

**目标**：`omega --version` 能返回版本号，`omega.yaml` 能被正确解析。

**构建步骤**：

1. 创建完整目录结构（见上）
2. 写入 `pyproject.toml`
3. 写入 `omega.yaml`（从设计文档照写，端口/路径适配 Windows）
4. 写入 `app/config.py`（读取 omega.yaml + .env）
5. 写入 `app/main.py`（CLI 入口 + 基础命令）
6. 写入 `Makefile`
7. 写入 `README.md`
8. `pip install -e .` 安装到开发模式
9. 验证：`omega --version` 返回 `omega v0.1.0-mfe`

### 迭代 1：核心路由与规划

**目标**：给定一个自然语言任务，Planner 能分解为步骤 DAG，Router 能为每个步骤选择工具。

**构建步骤**：

1. 写入 `app/gateway/` — Task Contract 数据类 + 自然语言→结构化 Contract
2. 写入 `app/planner/` — 模板加载 + 7 步规划 + DAG 生成
3. 写入 `app/planner/templates/` — 4 个初始任务模板 YAML
4. 写入 `app/router/` — 12 维评分引擎 + Stage-Aware 覆盖 + 冷启动路由表
5. 写入 `app/router/routing_table.yaml`
6. 单元测试：`test_router.py` + `test_planner.py`
7. 验证：`omega task "搜5篇SGLT2抑制剂的文献" --dry-run` → 输出步骤 DAG + 每步工具选择

### 迭代 2：执行与安全

**目标**：Router 选出的工具能被实际调用，风险操作被拦截。

**构建步骤**：

1. 写入 `app/safety/` — 四域风险检查 + Docker 沙箱管理
2. 写入 `app/executor/` — Agent 调度器 + Claude API 封装 + 工具适配器基类
3. 写入 `docker-compose.yml` — PostgreSQL + Qdrant + Sandbox
4. 写入 `app/mcp/` — MCP Server 生命周期管理
5. 写入 `mcp-servers/mcp-config.json`
6. 写入 `app/toolsmith/` — 工具学习闭环（简化版）
7. 集成测试：完整执行一个 knowledge_ingestion 任务
8. 验证：`omega task "把这篇PDF转为Markdown" --execute` → 成功产出文件

### 迭代 3：闭环验证

**目标**：6 个基准闭环全部跑通，`omega bench --all` 通过率 ≥ 80%。

**构建步骤**：

1. 写入 `app/outcome/` — 成果组装 + 验证
2. 写入 `app/memory/` — 行动记忆（PostgreSQL schema + CRUD）
3. 写入 `app/radar/` — 简化版扫描器
4. 写入 `workflows/` — LangGraph 工作流定义（至少 ingest + research）
5. 写入 `scripts/` — setup.ps1 + verify.ps1 + run_benchmark.py
6. 写入 `tests/benchmarks/` — 6 个基准测试
7. 执行全部基准测试
8. 写入部署验证脚本

---

## 4. 关键文件的精确构建指令

### 4.1 `pyproject.toml`（精确版本）

```toml
[build-system]
requires = ["setuptools>=75.0", "wheel"]
build-backend = "setuptools.build_meta"

[project]
name = "omega-agent-os"
version = "0.1.0"
description = "Omega Personal AI Action Ecology — Agent OS Layer"
readme = "README.md"
license = {text = "MIT"}
requires-python = ">=3.12"
authors = [{name = "Omega User"}]

dependencies = [
    "langgraph>=1.0.6,<2.0",
    "langchain-core>=1.4.0,<2.0",
    "langchain-anthropic>=0.3.0",
    "langchain-openai>=0.3.0",
    "pydantic>=2.10.0",
    "pyyaml>=6.0",
    "httpx>=0.28.0",
    "rich>=13.0",
    "click>=8.0",
    "python-dotenv>=1.0",
    "psycopg2-binary>=2.9",
    "qdrant-client>=1.14.0",
    "docker>=7.0",
    "lxml>=5.0",
    "pypdf>=5.0",
    "pandas>=2.2",
    "matplotlib>=3.9",
]

[project.optional-dependencies]
dev = [
    "pytest>=8.0",
    "pytest-asyncio>=0.24",
    "pytest-cov>=6.0",
    "black>=24.0",
    "ruff>=0.9",
    "mypy>=1.13",
]
all = [
    "playwright>=1.50",
    "sentence-transformers>=3.0",
    "torch>=2.5",
]

[project.scripts]
omega = "app.main:cli"

[tool.black]
line-length = 100

[tool.ruff]
line-length = 100

[tool.mypy]
python_version = "3.12"
strict = true

[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = ["test_*.py"]
```

### 4.2 `omega.yaml`（完整配置——放入 D:\Omega-System\）

```yaml
omega:
  name: "omega生态系统项目"
  full_name: "Omega Personal AI Action Ecology"
  mode: function_first
  owner: user
  version: "0.1.0-mfe"

paths:
  home: "D:/Omega-System"
  vault: "D:/Omega-System/omega-vault"
  runtime: "D:/Omega-System/omega-runtime"
  data: "D:/Omega-System/omega-data"
  workspace: "D:/Omega-System/omega-workspace"
  assets: "D:/Omega-System/omega-assets"
  sandbox: "D:/Omega-System/omega-workspace/sandbox"
  outputs: "D:/Omega-System/omega-workspace/outputs"
  temp: "D:/Omega-System/omega-workspace/temp"

runtime:
  orchestrator: langgraph
  primary_executor: claude_code
  fallback_executor: codex
  browser_automation: playwright
  sandbox: docker
  sandbox_image: "omega-sandbox:latest"
  sandbox_memory_limit: "4GB"
  sandbox_cpu_limit: "2"
  sandbox_timeout: 600
  max_concurrent_tasks: 3

memory:
  obsidian:
    enabled: true
    vault_path: "D:/Omega-System/omega-vault"
  postgres:
    enabled: true
    host: "127.0.0.1"
    port: 5432
    database: "omega"
    user: "omega"
    password: "${POSTGRES_PASSWORD}"
    min_connections: 2
    max_connections: 10
  qdrant:
    enabled: true
    host: "127.0.0.1"
    port: 6333
    collection: "omega_knowledge"
    vector_size: 1536
  zotero:
    enabled: true
    pdf_assets_path: "D:/Omega-System/omega-assets/zotero"

routing:
  router: tool_agent_router
  mode: static_then_scored
  cold_start_table: "app/router/routing_table.yaml"
  scoring_dimensions:
    - task_fit: 0.20
    - success_rate: 0.18
    - output_quality: 0.15
    - reputation: 0.12
    - cost: 0.10
    - speed: 0.08
    - controllability: 0.06
    - batch_reproducibility: 0.05
    - safety: 0.04
    - documentation_quality: 0.02
  stage_overrides:
    enabled: true
  creative_dimensions:
    enabled: true

planning:
  planner: dynamic_task_planner
  max_depth: 8
  parallelization: true
  gap_precheck: true
  template_library: "app/planner/templates/"

safety:
  principle: "risk_changes_path_not_goal"
  risk_levels:
    low: {action: auto}
    medium: {action: sandbox}
    high: {action: confirm}
    critical: {action: confirm_with_preview}
  sandbox:
    enabled: true
    image: "omega-sandbox:latest"
    network: none
    read_only_root: true
    tmpfs_size: "512M"

evolution:
  auto_upgrade:
    enabled: true
    low_risk: auto
    medium_risk: notify
    high_risk: confirm
  lifecycle:
    enabled: true
    observation_periods:
      low_risk: {uses: 10, days: 3, task_types: 2}
      medium_risk: {uses: 20, days: 7, task_types: 3}
      high_risk: {uses: 30, days: 14, task_types: 5}

domains:
  medical_research:
    enabled: true
  scientific_visualization:
    enabled: false     # 阶段 2 启用
  creative_production:
    enabled: false     # 阶段 2 启用

logging:
  level: INFO
  file: "D:/Omega-System/omega-data/logs/omega.log"
  max_size_mb: 100
  backup_count: 5
```

### 4.3 `docker-compose.yml`

```yaml
version: "3.9"

services:
  postgres:
    image: pgvector/pgvector:pg17
    container_name: omega-postgres
    restart: unless-stopped
    environment:
      POSTGRES_USER: omega
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD:-omega_dev_password}
      POSTGRES_DB: omega
    ports:
      - "127.0.0.1:5432:5432"
    volumes:
      - D:/Omega-System/omega-data/postgres:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U omega"]
      interval: 10s
      timeout: 5s
      retries: 5

  qdrant:
    image: qdrant/qdrant:v1.14.1
    container_name: omega-qdrant
    restart: unless-stopped
    ports:
      - "127.0.0.1:6333:6333"
      - "127.0.0.1:6334:6334"
    volumes:
      - D:/Omega-System/omega-data/qdrant:/qdrant/storage
    environment:
      QDRANT__SERVICE__HOST: 0.0.0.0
      QDRANT__SERVICE__API_KEY: ${QDRANT_API_KEY:-}
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:6333/collections"]
      interval: 10s
      timeout: 5s
      retries: 5

  sandbox:
    build:
      context: .
      dockerfile: Dockerfile.sandbox
    image: omega-sandbox:latest
    container_name: omega-sandbox
    restart: "no"
    network_mode: none
    read_only: true
    tmpfs:
      - /tmp:size=512M,exec
    volumes:
      - D:/Omega-System/omega-workspace/sandbox:/workspace:rw
    security_opt:
      - no-new-privileges:true
    cap_drop:
      - ALL
    mem_limit: 4GB
    cpus: 2
```

### 4.4 `app/main.py`（CLI 入口结构）

```python
"""Omega CLI — Agent OS Layer 命令行入口."""

import click
from rich.console import Console
from app.config import Config

console = Console()
cfg = Config.from_yaml("omega.yaml")


@click.group()
@click.version_option(version=cfg.version, prog_name="omega")
def cli():
    """Omega Personal AI Action Ecology — 功能优先的个人 AI Agent 行动生态."""
    pass


@cli.command()
@click.argument("goal", nargs=-1)
@click.option("--dry-run", is_flag=True, help="仅展示规划，不实际执行")
@click.option("--quality", type=click.Choice(["speed_first", "balanced", "highest_quality"]),
              default="balanced")
@click.option("--autonomy", type=click.Choice(["L0", "L1", "L2"]), default="L2")
def task(goal, dry_run, quality, autonomy):
    """执行一个任务。例如: omega task "搜5篇SGLT2抑制剂文献" """
    goal_text = " ".join(goal)
    # 1. Task Gateway → Contract
    # 2. Dynamic Task Planner → DAG
    # 3. Tool-Agent Router → 工具选择
    # 4. Safety Enforcer → 风险检查
    # 5. Agent Runner → 执行
    # 6. Outcome Package → 组装交付
    raise NotImplementedError("迭代 1-3 实现")


@cli.command()
def status():
    """查看系统状态"""
    raise NotImplementedError("迭代 0 实现")


@cli.command()
@click.argument("task_id")
def approve(task_id):
    """批准一个等待确认的任务"""
    raise NotImplementedError("迭代 2 实现")


@cli.command()
def bench():
    """运行基准测试"""
    raise NotImplementedError("迭代 3 实现")


@cli.command()
def radar():
    """查看 AI 工具生态雷达报告"""
    raise NotImplementedError("迭代 3 实现")


if __name__ == "__main__":
    cli()
```

### 4.5 `app/router/routing_table.yaml`（冷启动路由表）

```yaml
# Omega 冷启动路由表 — 当 Tool Reputation Ledger 数据不足时使用
# 评分基于 External AI Rolebook + 设计文档中的工具生态位定义

task_types:
  knowledge_ingestion:
    primary:
      tool: claude_api
      agent: researcher
    alternatives: [gpt4_api]
    forbidden: [codex_cli]

  literature_search:
    primary:
      tool: pubmed_api
      agent: researcher
    alternatives: [semantic_scholar_api, openalex_api]
    fallback: perplexity_api

  data_analysis:
    primary:
      tool: python_sandbox
      agent: data_analyst
    alternatives: [r_sandbox]
    forbidden: [bare_execution]

  academic_writing:
    primary:
      tool: claude_api
      agent: writer
    alternatives: [gpt4_api]
    stage_overrides:
      extraction: {tool: claude_api}
      synthesis: {tool: claude_api}
      delivery: {tool: pandoc}

  code_generation:
    primary:
      tool: claude_code
      agent: coder
    alternatives: [codex_cli, gpt4_code_interpreter]
    stage_overrides:
      execution: {tool: python_sandbox}

  medical_research:
    primary:
      tool: claude_api
      agent: medical_research_assistant
    alternatives: [deep_research, notebooklm]
    stage_overrides:
      literature_search: {tool: pubmed_api}
      evidence_assessment: {tool: claude_api}
      writing: {tool: claude_api}

  browser_automation:
    primary:
      tool: playwright_mcp
      agent: browser_agent
    alternatives: [puppeteer]
    forbidden: [manual_browser]

  tool_learning:
    primary:
      tool: toolsmith_lite
      agent: toolsmith
    alternatives: [manual_search]

capability_tool_map:
  ReadFile: [claude_code, python_sandbox]
  WriteFile: [claude_code, python_sandbox]
  ExecutePythonSandbox: [python_sandbox, docker_sandbox]
  ExecuteRSandbox: [r_sandbox]
  NetworkFetch: [httpx, curl]
  SearchAPI: [pubmed_api, semantic_scholar_api, perplexity_api]
  BrowserControl: [playwright_mcp]
  ReadDocumentation: [claude_api, perplexity_api]
  GenerateChart: [python_matplotlib, r_ggplot2]
  FormatCSL: [pandoc, zotero]
  OCR: [tesseract, easyocr]
```

### 4.6 `mcp-servers/mcp-config.json`

```json
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem", "D:/Omega-System/omega-workspace"]
    },
    "github": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": {
        "GITHUB_PERSONAL_ACCESS_TOKEN": "${GITHUB_TOKEN}"
      }
    },
    "postgres": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-postgres", "${DATABASE_URL}"]
    },
    "playwright": {
      "command": "npx",
      "args": [
        "-y", "@playwright/mcp@latest",
        "--headless",
        "--browser", "msedge",
        "--output-dir", "D:/Omega-System/omega-workspace/outputs/screenshots",
        "--isolated"
      ]
    },
    "sequential-thinking": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-sequential-thinking"]
    },
    "memory": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-memory"]
    },
    "brave-search": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-brave-search"],
      "env": {
        "BRAVE_API_KEY": "${BRAVE_API_KEY}"
      }
    }
  }
}
```

---

## 5. Windows 特定适配（Codex 容易踩的坑）

### 5.1 路径分隔符
- Python 代码内部：统一使用正斜杠 `/` 或 `pathlib.Path`
- YAML 配置：使用正斜杠 `D:/Omega-System/...`
- Shell 脚本：PowerShell 用 `\` 或 `/` 均可，但含空格的路径必须加引号
- `docker-compose.yml` 的 volumes：Windows 绝对路径用 `D:/Omega-System/...`

### 5.2 编码问题
- 所有 Python 文件第一行：`# -*- coding: utf-8 -*-`
- PowerShell 脚本第一行：`[Console]::OutputEncoding = [Text.Encoding]::UTF8`
- `pyproject.toml` 不用 BOM

### 5.3 Docker Desktop
- 必须确认 Docker Desktop 的 File Sharing 设置中包含了 `D:\`
- WSL2 backend 性能远好于 Hyper-V backend
- `docker-compose.yml` 中 volumes 的 Windows 路径映射：`D:\Omega-System\omega-data\postgres:/var/lib/postgresql/data`

### 5.4 进程管理
- Python 脚本可注册为 Windows Service（用 `nssm`）
- 或者用 Docker Compose 管理所有服务（推荐 MFE 阶段）

---

## 6. 外部工具和技能补充推荐

> 以下工具可以直接丰富 Omega 的能力矩阵。优先级按 MFE 阶段排序。

### 6.1 必须接入（MFE 阶段）

| 工具 | 接入方式 | 用途 |
|------|---------|------|
| **Claude API** (Anthropic) | `langchain-anthropic` | 核心语言引擎 |
| **GPT-4 API** (OpenAI) | `langchain-openai` | 备选引擎 + 交叉验证 |
| **PostgreSQL + pgvector** | Docker + `psycopg2` | 结构化记忆 + 向量搜索 |
| **Qdrant** | Docker + `qdrant-client` | 语义搜索 |
| **Playwright MCP** | `@playwright/mcp` | 浏览器自动化 |
| **Filesystem MCP** | `@modelcontextprotocol/server-filesystem` | 安全文件操作 |
| **GitHub MCP** | `@modelcontextprotocol/server-github` | 代码仓库 + 工具发现 |

### 6.2 推荐接入（MFE 阶段或稍后）

| 工具 | 接入方式 | 用途 | 优先级 |
|------|---------|------|--------|
| **Perplexity API** | HTTP API | 实时信息检索 | 高 |
| **Semantic Scholar API** | HTTP API（免费，无需 Key） | 学术文献检索 | 高 |
| **PubMed Entrez API** | `biopython` | 医学文献检索 | 高 |
| **Zotero** | Better BibTeX + `pyzotero` | 文献管理 | 高 |
| **Brave Search MCP** | `@modelcontextprotocol/server-brave-search` | 网页搜索（需 API Key） | 中 |
| **Sequential Thinking MCP** | `@modelcontextprotocol/server-sequential-thinking` | 复杂推理辅助 | 中 |
| **Memory MCP** | `@modelcontextprotocol/server-memory` | 知识图谱记忆 | 中 |
| **Exa Search API** | HTTP API | 高质量语义搜索 | 低 |
| **Tavily Search API** | HTTP API | Agent 专用搜索 | 低 |

### 6.3 优质开源 RAG 补充（阶段 2）

| 工具 | 特点 | 适用场景 |
|------|------|---------|
| **piragi** | 零配置、本地 Ollama、HyDE + Cross-encoder reranking、PostgreSQL 支持 | Omega 知识库的语义检索增强 |
| **RAGLite** | DuckDB/PostgreSQL 双后端、Adaptive RAG、FlashRank reranking、内置 MCP server | 轻量知识库 RAG |
| **pgai (Timescale)** | PostgreSQL 原生、声明式 embedding pipeline、自动同步 | 生产级向量管理 |

### 6.4 创意域工具（阶段 2 才启用）

| 工具 | 安装命令 | 用途 |
|------|---------|------|
| **Blender** | `winget install BlenderFoundation.Blender` | 3D 科学动画 |
| **Manim** | `pip install manim` | 2D 数学/科学动画 |
| **ffmpeg** | `winget install Gyan.FFmpeg` | 视频处理 |
| **ImageMagick** | `winget install ImageMagick.ImageMagick` | 图像处理 |
| **Nano Banana Pro** | Google Cloud API | AI 图像生成（文字准确） |
| **ComfyUI** | Git clone + `pip install` | 可控 AI 图像工作流 |

---

## 7. 验证标准

### 7.1 迭代 0 验收

- [ ] `omega --version` 返回 `omega v0.1.0-mfe`
- [ ] `omega --help` 显示所有命令
- [ ] `omega.yaml` 被正确解析（`omega status` 显示路径信息）
- [ ] `.env` 中的 API Key 被正确加载（不打印到日志）

### 7.2 迭代 1 验收

- [ ] `omega task "搜5篇SGLT2抑制剂的文献" --dry-run` 输出结构化 JSON DAG
- [ ] DAG 包含至少 3 个阶段（检索→筛选→输出）
- [ ] Router 为每个步骤推荐了具体工具（含主选+备选）
- [ ] `test_router.py` 全部通过

### 7.3 迭代 2 验收

- [ ] Docker Desktop 启动后 `docker compose up -d` 成功启动 PostgreSQL + Qdrant
- [ ] PostgreSQL 可用：`docker exec omega-postgres pg_isready`
- [ ] Qdrant 可用：`curl http://localhost:6333/collections`
- [ ] Safety Enforcer 拒绝了裸 `os.system("rm -rf /")` 调用
- [ ] Sandbox 中的代码无法访问外网

### 7.4 迭代 3 验收（6 个基准闭环）

- [ ] **闭环 1（知识摄取）**: PDF → wiki/来源/ 页面，含质量评级和稳定性标注
- [ ] **闭环 3（数据分析）**: CSV → 统计分析 + 图表 + Markdown 报告
- [ ] **闭环 7（科学可视化）**: 至少产出 60 秒动画草稿（含分镜稿 + TTS 旁白）
- [ ] **闭环 10（工具对比报告）**: 生成 ≥ 8 维度对比的 wiki/对比/ 页面
- [ ] **闭环 11（工具学习）**: 自动安装+试用一个未知工具 + 生成评估报告
- [ ] `omega bench --all` 通过率 ≥ 80%

---

## 8. 故障排除

| 症状 | 可能原因 | 解决 |
|------|---------|------|
| `omega` 命令找不到 | `pip install -e .` 未执行 | 在 `omega-runtime/` 中执行 `pip install -e .` |
| PostgreSQL 无法连接 | Docker 未启动 或 端口冲突 | `docker ps` 检查；修改 `docker-compose.yml` 端口 |
| Qdrant 无法连接 | Docker Desktop File Sharing 未包含 D 盘 | Docker Desktop → Settings → Resources → File Sharing → 添加 `D:\` |
| Claude API 调用失败 | API Key 错误 | 检查 `.env` 中的 `ANTHROPIC_API_KEY` |
| Playwright MCP 无响应 | 浏览器未安装 | `npx playwright install msedge` |
| Docker 拉取镜像失败 | 国内网络限制 | 配置镜像加速器（见附录 B） |
| Windows 路径错误 | 路径含空格或反斜杠 | 统一使用正斜杠 + `pathlib.Path` |

### 附录 A：`scripts/setup.ps1`（Windows 一键环境配置）

```powershell
# Omega Windows 环境配置脚本
# 以管理员身份运行

Write-Host "=== Omega 系统环境配置 ===" -ForegroundColor Cyan

# 1. 检查基础软件
$required = @("python", "node", "git", "docker")
foreach ($cmd in $required) {
    try {
        $null = Get-Command $cmd -ErrorAction Stop
        Write-Host "[OK] $cmd" -ForegroundColor Green
    } catch {
        Write-Host "[MISSING] $cmd — 请先安装" -ForegroundColor Red
        exit 1
    }
}

# 2. 创建目录结构
$dirs = @(
    "D:\Omega-System",
    "D:\Omega-System\omega-data\postgres",
    "D:\Omega-System\omega-data\qdrant",
    "D:\Omega-System\omega-data\logs",
    "D:\Omega-System\omega-workspace\temp",
    "D:\Omega-System\omega-workspace\sandbox",
    "D:\Omega-System\omega-workspace\outputs",
    "D:\Omega-System\omega-assets\zotero",
    "D:\Omega-System\omega-assets\templates",
    "D:\Omega-System\omega-assets\fonts"
)
foreach ($dir in $dirs) {
    New-Item -ItemType Directory -Path $dir -Force | Out-Null
    Write-Host "[CREATED] $dir" -ForegroundColor Green
}

# 3. 检查 .env 文件
if (-not (Test-Path "D:\Omega-System\.env")) {
    Write-Host "[WARNING] .env 文件不存在，创建模板..." -ForegroundColor Yellow
    @"
ANTHROPIC_API_KEY=your_key_here
OPENAI_API_KEY=your_key_here
GITHUB_TOKEN=your_token_here
POSTGRES_PASSWORD=change_me
"@ | Out-File -FilePath "D:\Omega-System\.env" -Encoding UTF8
    Write-Host "请编辑 D:\Omega-System\.env 填入真实的 API Key" -ForegroundColor Yellow
}

# 4. 配置 Python 虚拟环境
python -m venv D:\Omega-System\.venv
Write-Host "[OK] Python 虚拟环境创建完成" -ForegroundColor Green

Write-Host "`n=== 环境配置完成 ===" -ForegroundColor Cyan
Write-Host "下一步: cd D:\Omega-System\omega-runtime && pip install -e ." -ForegroundColor White
```

### 附录 B：Docker 镜像加速器（中国大陆用户）

编辑 `C:\Users\<用户名>\.docker\daemon.json`：

```json
{
  "registry-mirrors": [
    "https://docker.1ms.run",
    "https://docker.xuanyuan.me"
  ]
}
```

重启 Docker Desktop。

---

## 9. 给用户的说明

### 你在新电脑上的操作顺序

```
步骤 1（手动 30 分钟）：
  安装 Python 3.12 + Node.js 22 + Git + Docker Desktop
  → 运行 scripts/setup.ps1 验证

步骤 2（手动 15 分钟）：
  复制 omega-vault/ 到 D:\Omega-System\omega-vault\
  → 包含 24 个 Omega 设计文件 + CLAUDE.md + wiki/

步骤 3（手动 5 分钟）：
  填写 D:\Omega-System\.env 中的 API Key
  → Anthropic / OpenAI / GitHub Token

步骤 4（交给 Codex 或 Claude Code）：
  启动 Codex 或 Claude Code，工作目录设到 D:\Omega-System\omega-runtime\
  给出指令：
    "按照 ../omega-vault/omega生态系统项目/00-总览/Omega 构建指导书 — 给 Codex 的系统构造规范.md
     完成迭代 0——目录结构 + Python 包 + CLI 入口。
     完成后运行 omega --version 验证。"

步骤 5（逐步推进）：
  迭代 0 验证通过后，继续迭代 1、2、3
  每迭代完成后运行验证命令

步骤 6（最终验证）：
  omega bench --all 通过率 ≥ 80%
  docker compose ps 确认所有服务运行
```

### 构建所需的总时间估算

| 迭代 | Codex/Claude Code 构建 | 人工操作 |
|------|:---------------------:|:------:|
| 迭代 0（骨架） | ~2 小时 | ~30 分钟环境确认 |
| 迭代 1（路由规划） | ~3 小时 | ~15 分钟审查 |
| 迭代 2（执行安全） | ~4 小时 | ~30 分钟 Docker 确认 |
| 迭代 3（闭环验证） | ~5 小时 | ~1 小时测试审查 |
| **总计** | **~14 小时** | **~2 小时** |

---

*构建指导书版本：v1.0 — 2026-05-15*
*此文档应随 Omega 设计文档的更新而更新。*
