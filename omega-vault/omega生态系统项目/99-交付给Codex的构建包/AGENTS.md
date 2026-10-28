# Omega Project — AGENTS.md（Codex 自动读取）

> **此文件会被 Codex CLI 在启动时自动加载。** 它定义了 Omega 项目的约定、文件结构和构建目标。

## 0. 你的身份和任务

你是 Codex 构建 Agent。具体模型、effort 与版本必须从当前运行时发现，不得在项目配置中固定。你的任务是：**根据 Omega 系统设计蓝图，在一台全新 Windows 电脑上从零构建 Omega MFE（最小功能生态）系统。**

你需要的所有设计文档在 `../omega-vault/omega生态系统项目/` 目录中。主构建规范在 `../omega-vault/omega生态系统项目/00-总览/Omega 构建指导书 — 给 Codex 的系统构造规范.md`。

**构建主线**：Codex CLI 当前会话。OpenAI API 是 Omega 运行时次主链；OpenRouter/国产 Claude Messages 兼容端点仅作备用。禁止原生 Anthropic 账号、密钥与 `api.anthropic.com`；NotebookLM 排除；本地模型仅可由用户显式启用为灾备。

## 1. 项目约定

- **语言**: Python 3.12，所有代码用英文，所有注释用英文，面向用户的输出用中文
- **类型注解**: 所有 Python 函数必须带完整类型注解
- **文档字符串**: 所有公共模块/类/函数必须有 docstring（Google style）
- **路径**: 所有路径统一用正斜杠 `/`，Python 代码中用 `pathlib.Path`
- **安全**: 不硬编码任何密钥/Token/密码。所有敏感值从环境变量或 `.env` 读取
- **测试**: 每个模块对应一个 `tests/test_模块名.py`，pytest 格式
- **Git 提交**: Conventional Commits 格式（`feat:`, `fix:`, `chore:`, `docs:`, `test:`）
- **配置优先于代码**: 可变的行为参数放在 YAML 配置文件中，不硬编码在 Python 里

### 1.1 强制技术选型（MFE 阶段固定，不允许摇摆）

```
语言：        Python 3.12（主机运行时，唯一后端语言）。Docker 沙箱镜像使用 python:3.11-slim-bookworm
              （Debian 稳定版兼容性——沙箱内 Python 版本独立于主机，不影响主机 3.12 代码）
包管理：      pip + venv（不使用 Poetry/uv/conda）
CLI 框架：    Click + Rich
配置：        YAML + Pydantic v2
编排：        先自定义轻量 orchestrator（不用 LangGraph 直接上）
数据库：      Docker PostgreSQL 17 + pgvector（不使用 SQLite 起步）
向量库：      Docker Qdrant v1.14.1
浏览器：      Playwright MCP（@playwright/mcp@latest）
沙箱：        Docker（双沙箱策略：omega-sandbox 无网络执行 + omega-sandbox-net 有限网络安装）
测试：        pytest ≥ 8.0
代码风格：    Black + Ruff + mypy（strict mode）
AI 引擎：     集中能力角色——Codex 当前会话 → OpenAI API → OpenRouter/国产 Claude Messages 备用
              → 国产 OpenAI-compatible 备用 → 显式本地灾备。具体模型运行时动态发现
引擎解析：     Language Engine Resolver（app/router/engine_resolver.py）——运行时按 engine_resolution.yaml
              按 model_capabilities.yaml 能力角色解析，不硬编码模型版本；未知 ID/设置/历史原样保留
构建 Agent：  Codex CLI 当前会话主链；Claude Code 仅允许连接 OpenRouter/国产兼容端点作为备用
用户交互：     所有需要用户手动操作的步骤，指引用户查看 build-package/USER_ACTIONS.md 对应编号
Windows路径： 默认 OMEGA_HOME=D:\Omega-System\（代码内用 {OMEGA_HOME} 或 pathlib，支持自定义部署路径）。
              构建前先确认 OMEGA_HOME，所有路径从此变量派生

注：Runtime Architecture 文档（Omega Runtime Architecture.md）中提及的 Typer/LangGraph/SQLite
属于早期设计探索，MFE 阶段以本文件的技术栈为准。阶段 2+ 可重新评估。
```

### 1.2 凭据处理规则（违反即停止构建）

```
规则 1: 永远不将 API Key/Token/密码写入任何代码文件（.py, .yaml, .json, .md, .toml）
规则 2: 永远不将 API Key/Token/密码提交到 Git
规则 3: 永远不将 API Key/Token/密码打印到终端或日志
规则 4: 启动时按 api_tiers.yaml 确认 Codex 会话和可选运行时 provider，原子生成 active_engines.yaml
        Codex 会话足以构建；独立运行时 API 可以 deferred，不得索要 ANTHROPIC_API_KEY
规则 5: 如有任何必需变量缺失 → 停止构建 → 明确提示用户：
         - 变量名
         - 用途
         - 获取 URL
         - 降级方案（该引擎不可用时的替代选项）
规则 6: 所有敏感值仅从 os.environ 或 python-dotenv 读取
```

### 1.3 Codex 构建边界（不允许做的事，无论任何情况）

```
禁止自动执行：
  ❌ 删除用户的旧知识库或任何非 Omega 系统文件
  ❌ 上传数据到外部服务器
  ❌ 自动发表内容（论文、博客、推文）
  ❌ 自动提交投稿表单
  ❌ 自动替换系统级配置（环境变量、注册表、Windows 服务）
  ❌ 自动安装来源不明或未签名的软件到主机
  ❌ 修改 Docker Desktop 或 Windows 防火墙设置
  ❌ 执行任何需要用户密码的 sudo/管理员操作（build-package/scripts/setup.ps1 除外）
  ❌ 直接将 AI 生成内容写入 Omega vault 的 wiki/ 目录（必须先经过候审区质量检查）

允许自动执行：
  ✅ 写代码、建目录、生成配置文件
  ✅ pip install / npm install（在虚拟环境内）
  ✅ git init / git add / git commit
  ✅ 读写 {OMEGA_HOME}\ 下的所有文件
  ✅ docker compose up / down（仅限 omega 项目容器）
  ✅ pytest / python 脚本（仅限 omega 项目代码）
  ✅ winget install（仅限 build-package/scripts/setup.ps1 中列出的包）
  ✅ 将 AI 生成内容写入 omega-workspace/review/ 候审区（不直接写 wiki/）
```

### 1.4 知识库防污染协议（KB Anti-Pollution Protocol）

**核心原则**：AI 生成的内容不能直接写入 Omega vault 的 `wiki/` 目录。所有 AI 输出必须先进入 `omega-workspace/review/` 候审区，通过 6 项自动质量检查后，由 `knowledge_steward` Agent 合并到正式知识库。

**6 项自动检查**（`KnowledgeBaseGuard.stage_content()`）：
1. `min_length` — 内容 ≥100 字符（非占位符空壳）
2. `has_frontmatter` — 包含 YAML frontmatter
3. `has_sections` — 包含 `## ` Markdown 标题
4. `no_hallucination_markers` — 不含常见 AI 幻觉标记（如 "as an AI language model"）
5. `has_source_attribution` — 包含 `[[wikilink]]` 或 `doi:` 引用
6. `not_duplicate` — 内容哈希与已有页面不重复

**处理逻辑**：
- `quality_score ≥ 5/6` → `auto_approved` → `knowledge_steward` 自动合并
- `quality_score < 0.5`（<3/6 通过）→ 标记需人工审查 → 通知用户（`omega review list`）
- 中间状态 → 合并但标记 `#needs-review` 标签

**Codex 例外**：构建过程中生成的 `wiki/` 页面（来源摘要页、实体页、概念页等）可以是 Codex 直接写入——这些是 ingest 管道的核心产物，已通过 `质量评级/信息精炼协议` 验证。本协议主要针对运行时 AI 自由生成的洞察和分析内容。

### 1.5 Toolsmith 工具隔离与签名协议（Quarantine & Signing Protocol）

**核心原则**：Toolsmith 发现的外部工具不得直接进入正式工具注册表。所有新工具必须经过隔离区（quarantine）的三步验收流程。

**三步验收流程**（`QuarantineManager.run_acceptance_tests()`）：
1. **功能测试** — 在 `omega-sandbox` 中 `import` 并运行基本 smoke test
2. **安全检查** — 静态分析包的导入依赖、网络调用、文件写入模式
3. **依赖冲突检测** — `pip check` 验证与现有工具集无冲突

**状态转换**：
```
PENDING → TESTING → PASSED → SIGNED → PROMOTED（进入正式 config/tools.yaml）
                   → REJECTED（报告用户，不进入注册表）
```

**禁止行为**：
- ❌ 跳过隔离区直接将发现的工具写入 `config/tools.yaml`
- ❌ 签名未通过任一验收测试的工具
- ❌ 推广（promote）UNSIGNED 状态的工具

### 1.6 模拟构建优先协议（Simulate-First Protocol）

**核心原则**：Codex 在执行任何升级阶段前，必须先运行 `omega simulate <phase>` 生成模拟报告（DAG + 文件变更清单 + 风险表 + 预计耗时），展示给用户审查，确认后才开始修改代码。

**模拟报告包含**（`BuildSimulator.simulate_phase()`）：
- 📋 文件变更清单（路径/操作类型/风险等级/是否可回滚）
- ⚠️ 风险评估（风险描述/概率/影响/缓解措施）
- 📊 预估（修改文件数/预计耗时/回滚命令）

**Codex 执行纪律**：
```
每阶段必做：SIMULATE → SHOW → CONFIRM → BUILD
跳过任意一步视为违反协议。
```

**两阶段模拟**：
- **升级阶段模拟**：Codex 先 `omega simulate phase-N` → 用户确认 → 开始写代码
- **任务执行模拟**：运行时 `omega task "..." --dry-run` → 展示 DAG/工具选择/成本预估 → 用户确认 → 执行

### 1.7 溯源与飞行记录协议（Provenance & Flight Recording Protocol）

**核心原则**：每个 Omega 任务的输入、路由、工具调用、成本、产物来源必须完整记录。每个结论必须可追溯至原始来源。

**飞行记录仪**（`FlightRecorder`）记录内容：
- 任务：goal / task_type / task_id
- 路由：selected_tools / fallback_chain / engine_used / agent_assigned
- 步骤：step_id / tool / success / duration_ms / error
- 成本：total_api_calls / estimated_cost_usd / total_duration_ms
- 产出：output_files / output_pages

**溯源水印**（`ProvenanceWatermark`）链接类型：
- `literature` — DOI/PubMed ID
- `code` — 文件路径 + commit hash
- `data` — 数据文件路径 + SHA256
- `model_call` — 模型名称 + prompt hash
- `web_search` — URL + 检索时间戳
- `tool_output` — 工具名称 + 执行 ID

**水印格式**：以 HTML 注释嵌入每个成果页底部，可被 Obsidian 忽略显示但被 lint 工具解析。

### 1.8 显式本地灾备协议（Explicit Local Disaster-Recovery Protocol）

**核心原则**：本地模型永不自动接管。只有所有在线 provider 不可用且用户明确启用 `OMEGA_LOCAL_DR_ENABLED=true` 时，Omega 才进入本地灾备；否则清晰报告不可用。

**降级触发条件**（满足任一）：
- Engine Resolver 检测到 `active_engines.yaml` 中所有在线语言引擎标记为 `unavailable_confirmed`，且用户已显式授权本地灾备
- 连续 3 次 API 调用超时或返回 5xx
- 用户明确设置 `omega budget offline` 或 `OMEGA_LOCAL_DR_ENABLED=true`

**本地引擎接入方式**（按优先级排序）：

| 优先级 | 引擎 | 接入方式 | 能力 | 限制 |
|--------|------|---------|------|------|
| 1 | Ollama | `OLLAMA_HOST` 环境变量 → `http://localhost:11434` | 文本生成、代码生成、摘要（质量因模型而异） | 需用户预先安装 Ollama 并拉取模型 |
| 2 | LM Studio | `LMSTUDIO_HOST` 环境变量 → `http://localhost:1234` | 同上，支持更多模型格式 | 需用户预先安装 LM Studio |
| 3 | llama-cpp-python | Python 包内嵌，纯离线 | 文件处理、格式转换、索引（不含生成） | 小模型能力有限 |
| 4 | 纯脚本模式 | 无语言引擎，仅 Python 沙箱 | CSV 分析、文件转换、基准测试、索引同步 | 无自然语言理解和生成能力 |

**离线模式下的功能矩阵**：

| 功能 | API 模式 | Ollama/LM Studio | 纯脚本 |
|------|:--:|:--:|:--:|
| 文献检索（PubMed API） | ✅ | ✅ | ❌ |
| 数据分析（CSV/统计） | ✅ | ✅ | ✅ |
| 代码生成 | ✅ | ⚠️ 质量降低 | ❌ |
| 学术写作 | ✅ | ⚠️ 质量降低 | ❌ |
| 知识库索引更新 | ✅ | ✅ | ✅ |
| 知识库 lint 检查 | ✅ | ✅ | ✅ |
| 工具隔离验收测试 | ✅ | ✅ | ✅ |
| 浏览器自动化 | ✅ | ✅ | ❌ |

**Codex 构建要求**：
- `.env.example` 中新增 `OLLAMA_HOST` 和 `LMSTUDIO_HOST` 可选变量
- `engine_resolution.yaml` 新增 `local_fallback` 策略链
- 部署时不强制要求本地模型——标记为可选增强

### 1.9 上下文管理协议（防 258k 限制）

Omega 构建预计 ~14 小时，远超单次会话的上下文窗口。以下机制确保重启后无缝继续：

**每迭代维护的文件**（放在 `omega-runtime/` 下）：

| 文件 | 用途 | 更新频率 |
|------|------|---------|
| `BUILD_STATE.md` | 当前进度、阻塞点、下一步、已修改文件清单 | 每步更新 |
| `DECISIONS.md` | 关键设计决策及理由（不可逆决策必须记录） | 每次决策后 |
| `ITERATION_N_REPORT.md` | 迭代完成报告：改了什么、测试结果、未完成项 | 每迭代结束 |
| `logs/simulations/` | 模拟构建报告（DAG/风险/变更清单） | 每阶段模拟后 |
| `logs/flights/` | 任务飞行记录（JSON，完整审计记录） | 每任务结束后 |

**Git 提交纪律**：
- 每个功能点/文件完成后立即提交（不攒到迭代末）
- 提交信息用 Conventional Commits + 文件路径摘要
- 重启用 `git log --oneline -20` 和 `git diff HEAD~1` 恢复上下文

**重启恢复流程**（每次上下文丢失后执行）：
```
1. 读取 build-package/AGENTS.md（本文件）
2. 读取 omega-runtime/BUILD_STATE.md（当前进度）
3. 读取 omega-runtime/DECISIONS.md（设计决策）
4. 读取 build-package/BUILD_CHECKLIST.md（目标清单）
5. 执行 git status + git log --oneline -10
6. 检查 omega-runtime/logs/simulations/ 中最近模拟报告
7. 继续 BUILD_STATE.md 中标记的 in_progress 步骤
8. 当前阶段如有未执行的模拟 → 先 `omega simulate <phase>` 再继续
```

**用户交互时的暂停保护**：
- 需要用户操作时，更新 BUILD_STATE.md 的 `Blocked On` 字段
- 提示用户查看 `build-package/USER_ACTIONS.md` 对应步骤（如 `USER_ACTIONS.md` §2-1）
- 用户完成操作后，先读 BUILD_STATE.md 恢复状态再继续

## 2. 关键文件位置

| 用途 | 路径（相对于 omega-runtime/） |
|------|---------------------------|
| 主构建规范 | `../omega-vault/omega生态系统项目/00-总览/Omega 构建指导书 — 给 Codex 的系统构造规范.md` |
| Codex 启动提示词 | `../build-package/CODEX_RUN_PROMPT.md` |
| 构建验收清单 | `../build-package/BUILD_CHECKLIST.md` |
| 系统总方法论 | `../omega-vault/omega生态系统项目/01-方法论/` |
| 架构设计 | `../omega-vault/omega生态系统项目/02-架构/` |
| 能力矩阵 | `../omega-vault/omega生态系统项目/03-能力矩阵/` |
| 运行时设计 | `../omega-vault/omega生态系统项目/08-运行时与原型/` |
| 基准任务定义 | `../omega-vault/omega生态系统项目/09-功能基准任务花园/` |
| 外部工具档案 | `../omega-vault/omega生态系统项目/10-外部AI与工具注册表/` |
| 创意生产域 | `../omega-vault/omega生态系统项目/11-创意与科学可视化/` |
| 种子工具注册表 | `../build-package/config/tools.yaml` |
| 种子 Agent 注册表 | `../build-package/config/agents.yaml` |
| 环境变量模板 | `../build-package/config/.env.example` |
| 冷启动路由表 | `../build-package/config/routing_table.yaml` |
| 阶段权重表 | `../build-package/config/stage_weights.yaml` |
| 风险策略 | `../build-package/config/risk_policy.yaml` |
| 引擎解析策略 | `../build-package/config/engine_resolution.yaml` |
| 模型能力角色真相源 | `../build-package/config/model_capabilities.yaml` |
| API 分层部署协议 | `../build-package/config/api_tiers.yaml` |
| JSON Schema | `../build-package/schemas/` |
| 验收测试数据 | `../build-package/fixtures/` |
| Docker 模板 | `../build-package/templates/docker-compose.yml` |
| Sandbox Dockerfile | `../build-package/templates/Dockerfile.sandbox` + `Dockerfile.sandbox-net` |
| MCP 配置模板 | `../build-package/templates/mcp-config.json` |
| 构建状态模板 | `../build-package/templates/BUILD_STATE.md` |
| 决策日志模板 | `../build-package/templates/DECISIONS.md` |
| 用户操作指南 | `../build-package/USER_ACTIONS.md` |
| 系统配置 | `./omega.yaml`（你要创建） |

## 3. 构建方式

你是 AI Agent，不是人类运维人员。你可以自主写代码、生成配置、执行 `pip install`、`npm install`、`git init`。

你需要用户做的事（停下来，明确提示，附带获取 URL 和 USER_ACTIONS.md 步骤编号）：
- 部署时按 api_tiers.yaml 确认可选运行时 provider → 见 USER_ACTIONS.md §🅱
  · 主链：Codex 当前会话；OpenAI API → https://platform.openai.com/
  · 备用：OpenRouter 或国产 Claude Messages 兼容端点（不得连接 api.anthropic.com）
  · 国内 OpenAI-compatible provider 可作后续备用；本地模型仅显式灾备
- 设置 PostgreSQL 密码（任意强密码）→ 见 USER_ACTIONS.md §🅱
- 确认高风险操作（文件删除、系统配置修改）→ 见 USER_ACTIONS.md §2-2
- 启动 Docker Desktop → 见 USER_ACTIONS.md §🅰
- 提供 Zotero API Key（可选，不提供则退化为 BibTeX/RIS 手动导出）
- 提供 GitHub Token / Brave API Key / Perplexity API Key（全部可选，按需提供）

> **注意**：Codex 当前会话凭据由宿主管理，不要求 `OPENAI_API_KEY`。`OPENAI_API_KEY` 仅用于 Omega 独立运行时次主链；模型从运行时发现，不假定固定版本。

**用户交互原则**：
- 需要用户操作时，展示清晰的选项编号和默认选项
- 每个交互附带操作截图描述（做什么 → 怎么做 → 如何确认成功）
- 指引用户查看 `build-package/USER_ACTIONS.md` 对应编号
- 禁止对自己展示的建议自问自答——展示完等用户回应

## 4. 构建前强制检查（不通过不许开始）

```
□ OMEGA_HOME 已确认？         → 默认 D:\Omega-System，可由用户自定义。所有路径从此变量派生
□ {OMEGA_HOME}\.env 存在？    → 不存在则提示用户创建（模板在 build-package/config/.env.example）
□ Codex 当前会话可用？       → 是则满足构建要求；独立运行时 API 可 deferred
□ Provider 配置安全？        → OpenAI 主；OpenRouter/国产 Claude Messages 仅备用；拒绝 api.anthropic.com
    · 再检查国内 OpenAI-compatible 备用（DeepSeek/通义/智谱/Kimi/硅基流动）
    · 确定后生成 active_engines.yaml（记录 available/deferred/unavailable_confirmed）
    · Codex 当前会话为内置构建能力，不要求 OPENAI_API_KEY，不固定模型版本
□ POSTGRES_PASSWORD 非空？   → 为空则提示设置任意强密码
□ omega-vault/omega生态系统项目/ 存在且含 20+ 个 .md？ → 不存在则提示用户复制
□ Python 3.12 可用？         → python --version
□ Node.js 22 可用？          → node --version（npm/npx 依赖项）
□ Docker Desktop 运行中？     → docker ps
□ codex --version 成功？     → 验证 Codex CLI 可用；具体模型从当前运行时发现
□ build-package/MANIFEST.yaml 中 required 文件全部存在？ → 逐项检查，缺失则停止
```

> 注：部署时按 api_tiers.yaml 验证 provider、动态发现模型并原子更新配置。禁止原生 Anthropic；NotebookLM 明确排除。Codex 当前会话不依赖 OPENAI_API_KEY。
> 用户已预装 Node.js、Git、WSL2、Docker Desktop、Zotero、Obsidian 等软件。

## 5. 构建顺序（严格遵守）

```
迭代 0: 骨架搭建 → 迭代 1: 路由与规划 → 迭代 2: 执行与安全 → 迭代 3: 闭环验证
```

每个迭代完成后，对照 `build-package/BUILD_CHECKLIST.md` 逐项检查。只有全部通过才能进入下一迭代。

### MFE 验收范围说明

> **闭环命名唯一权威源**：`templates/BENCHMARK_CATALOG.yaml`。所有闭环引用使用稳定字符串 `catalog_id`，**不使用数字编号**（不同文档中"闭环 1"含义不同，以 BENCHMARK_CATALOG 的 `legacy_numbers` 映射为准）。

MFE 阶段按五层验收体系分步递进：

| 层级 | 闭环数 | 阶段 |
|------|--------|------|
| **MFE-Alpha** | 4 (`literature_ingestion` `csv_analysis` `tool_comparison` `tool_gap_learning`) | 迭代 0-3（初始构建目标） |
| **MFE-Methodology** | 6（严格等于方法论 §13.3 的 6 闭环） | MFE 构建完成后 |
| **MFE-Plus** | 9（Methodology + `code_generation` `tool_comparison` `quality_improvement`） | Phase 2-9 升级后 |
| **Full-Core** | 12 | Phase 2-11 升级后 |
| **Full-Extended** | 13+（含 `knowledge_base_health` 等扩展闭环） | 持续演化 |

完整 Omega 定义了 13+ 个基准闭环（见 `templates/BENCHMARK_CATALOG.yaml`），超出 MFE-Alpha 的 4 个属于后续阶段范围，MFE 阶段**不需要实现**。

## 6. 每迭代完成后的 Git 提交

```bash
git add -A
git commit -m "feat: complete iteration N — <简短描述>"
```

## 7. 构建前必读的设计文件（优先级排序）

1. `Omega 构建指导书 — 给 Codex 的系统构造规范.md`（主施工图）
2. `Omega运行形态与本体文件说明.md`（三层架构 + 完整目录树）
3. `Omega Runtime Architecture.md`（11 组件数据流 + 技术选型——注意 MFE 差异标注）
4. `Omega 最终完整方法论.md`（当前系统总纲）
5. `Tool-Agent Router：最佳工具与最佳执行者选择器.md`（12 维评分算法）
6. `Dynamic Task Planner：动态任务规划器.md`（7 步规划 + DAG）
7. `tools.yaml`（种子工具注册表——当前 28 个工具，每条必须符合 tool_card.schema.json）
8. `agents.yaml`（种子 Agent 注册表——注意 preferred_engine 由 Engine Resolver 解析）
9. `routing_table.yaml`（冷启动路由表——16 种任务类型，language_engine 引用由 Resolver 解析）
10. `stage_weights.yaml`（阶段权重表——8 阶段 × 12 维度动态覆盖）
11. `risk_policy.yaml`（四域风险升级策略——Auto/Notify/Confirm/Emergency）
12. `model_capabilities.yaml`（能力角色/provider 链/动态发现/原子迁移的唯一真相源）
13. `engine_resolution.yaml`（只按能力角色解析，不固定模型版本）
14. `api_tiers.yaml`（Codex/OpenAI 主链及兼容备用 provider 部署协议）
15. `docker-compose.yml` + `Dockerfile.sandbox` + `Dockerfile.sandbox-net`（Docker 模板——双沙箱策略）
16. `mcp-config.json`（MCP Server 配置模板——8 个 MCP Server，2 个阶段 2 启用）
17. `USER_ACTIONS.md`（用户手动操作指南——构建 Agent 需在提示用户时引用其步骤编号）
18. `BUILD_STATE.md` + `DECISIONS.md`（上下文管理模板——用于构建 Agent 状态恢复）
19. `BENCHMARK_CATALOG.yaml`（闭环目录唯一权威源——构建验收时按 catalog_id 和 tier 判断，不用数字）
20. `DEPLOYMENT_CONTRACT.md`（部署契约——构建前自检：哪些自动/哪些需确认/哪些永不自动做）
21. `VISION_TRACE.yaml`（方法论原则→代码追踪矩阵——每 Phase 完成后更新状态，四条件全部满足才标记 implemented）
22. `OMEGA_TERMINAL.md`（🆕 Omega Terminal 设计规范——统一操作窗口的完整 UI 蓝图，Phase 10 实现依据）

## 8. 设计文档目录缺口说明

> **给 Codex 的透明提醒**：Omega 项目按方法论九层架构组织文档，但并非每个目录都有完整设计文件。以下是 `omega生态系统项目/` 中**有目录名但缺独立设计文档**的位置：

| 目录 | 状态 | 说明 |
|------|------|------|
| `05-知识库与记忆/` | ⚠️ 空目录 | 知识库结构由 `CLAUDE.md`（vault 配置）定义；记忆层设计分散在 Runtime Architecture（PostgreSQL+Qdrant）和 Best-Practice Harvester 中 |
| `06-安全与权限/` | ⚠️ 空目录 | 安全设计分散在多个文件中：`risk_policy.yaml`（四级风险策略）、代码中的 `guardian.py`/`privacy.py`、方法论文档的安全红线章节 |
| `07-部署与迁移/` | ⚠️ 空目录 | 部署逻辑主要在 `构建指导书`（附录 A setup.ps1）、`api_tiers.yaml`（分层部署协议）、`deployment_profiles.yaml`（4 种方案）中 |
| `12-UI与可视化/` | ⚠️ 空目录 | 可视化设计在 `11-创意与科学可视化/` 中（科学动画生产系统 + Creative Tool Router）；Web UI 只在构建指导书 Phase 10 中有实现规范 |

**对 Codex 的影响**：这些目录在设计文档索引（附录 A）中可能看起来是"缺失的文件"——实际上它们的内容分散在其他文档中。构建时不需要在这些目录中寻找独立文件。如果未来需要集中规范，可以在这些目录中新增文档。

## 9. 版本信息

*AGENTS.md 版本：v3.2 — 2026-08-23*
*变更 v3.2：Codex-first 能力角色；禁止原生 Anthropic；NotebookLM 排除；动态发现、未知 ID 保留与原子迁移；本地仅显式灾备*
*变更 v2.1：新增 §1.9 设计文档目录缺口说明；§1.8 本地优先回退协议；§1.7 溯源与飞行记录协议；§1.6 模拟优先协议；§1.5 Toolsmith 隔离与签名协议；§1.4 知识库防污染协议*
*变更 v2.0：初始版本，定义项目约定、凭据规则、构建边界、必读设计文件*
