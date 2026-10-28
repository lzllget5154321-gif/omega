# Omega 构建包 — 给 Codex 的完整系统构造套件

> **这个文件夹是交给新电脑上 Codex 的构建包。Claude Code 仅可通过 OpenRouter/国产兼容端点作为备用。**
> Codex 会读取 `AGENTS.md`（自动）和构建指导书（手动指定），然后从零构建整个 Omega MFE 系统。

## 这个包能构建出什么

```
Omega-Lite (MFE / 最小功能生态)
─────────────────────────────────
✅ 文献检索与知识摄取（PubMed → wiki/来源/）
✅ 数据分析（Python 沙箱 + 统计 + 图表）
✅ 代码生成与执行（Codex CLI 主链）
✅ 医学研究流程（选题→检索→评估→写作）
✅ 浏览器自动化（Playwright MCP）
✅ 工具自主学习与注册（Toolsmith-Lite）
✅ 自动升级与替换（四域风险模型）
✅ CLI 命令行入口（omega task "..." ）
❌ 暂不含：3D 动画 / Web 界面 / 常驻后台
─────────────────────────────────
```

## 你需要做的事（在新电脑上）

### 第一步：复制文件

将以下内容复制到新电脑（默认部署到 `D:\Omega-System\`，可自定义其他 D 盘路径）：

```
当前电脑                              新电脑（{OMEGA_HOME} 默认为 D:\Omega-System）
──────────────────────────────       ──────────────────────────────────────────
omega生态系统项目/  (整个目录)    →   {OMEGA_HOME}\omega-vault\omega生态系统项目\
CLAUDE.md                        →   {OMEGA_HOME}\omega-vault\CLAUDE.md
wiki/  (如果你想迁移知识库)       →   {OMEGA_HOME}\omega-vault\wiki\
本文件夹 (99-交付给Codex的构建包) →   {OMEGA_HOME}\build-package\
```

> **自定义路径**：Codex 构建前会先确认 `OMEGA_HOME`。所有路径从 `OMEGA_HOME` 派生，可以部署到任意 D 盘目录。

### 第二步：确认基础软件已安装

> 如果你已按用户习惯预装以下软件，此步可跳过。仅需验证 Docker Desktop 正在运行。

在 PowerShell 中逐项验证：

```powershell
python --version     # 应输出 Python 3.12.x
node --version       # 应输出 v22.x.x
git --version        # 应输出 git version 2.x
docker --version     # 应输出 Docker version 27.x
docker ps            # 确认 Docker Desktop 在运行（鲸鱼图标绿色）
codex --version      # 验证 Codex CLI 当前运行时
```

> **注意**：具体 Codex 模型从当前运行时发现，不固定版本。禁止原生 Anthropic；NotebookLM 排除。
> 能力契约保持 provider-neutral，但生产优先级明确为 Codex-first；Claude Code 不与 Codex 平级。

如果某项缺失，用 winget 补充安装：

```powershell
winget install Python.Python.3.12 --silent
winget install OpenJS.NodeJS.LTS.22 --silent
winget install Git.Git --silent
winget install Docker.DockerDesktop --silent
# ⚠️ Docker Desktop 安装后需手动启动，等待鲸鱼图标变绿
```

> 其他软件（WSL2、Ubuntu、VS Code、Notepad++、Zotero、Obsidian、CCswitch）已由用户预先安装，本构建流程不重复处理。

### 第三步：确认构建 Agent 已安装

用户已预装以下两种构建 Agent，此步仅需验证：

```powershell
codex --version      # Codex CLI 主链（模型从当前运行时发现）
```

> **构建主线：Codex CLI 当前会话**。OpenAI API 次主；OpenRouter/国产 Claude Messages 仅备用；本地模型仅显式灾备。
> 能力契约可迁移，但默认且受验收支持的构建主线是 Codex。

### 第四步：填写 API Key

> Codex 构建时会自动检查 `config/.env.example` 中标记为 `[REQUIRED]` 的变量。无需手动创建 .env——Codex 会提示你。

如果你想提前准备，复制模板并填写：

```powershell
copy $env:OMEGA_HOME\build-package\config\.env.example $env:OMEGA_HOME\.env
notepad $env:OMEGA_HOME\.env
```

至少需要填写（分层降级——至少一个语言引擎 Key）：
- `OPENAI_API_KEY`（Omega 独立运行时主 provider，可选）
- `OPENROUTER_API_KEY` 或 `DOMESTIC_CLAUDE_API_KEY`（Claude Messages 备用，可选）
- 国内 OpenAI-compatible provider keys（后续备用，可选）
- `POSTGRES_PASSWORD`（必需 — 任意强密码 16 位以上）

> **注意**：部署时 Codex 按 api_tiers.yaml 协议逐层询问你可用 API，确认后自动配置 active_engines.yaml。
> 任何一层可用都能完整运行 Omega——仅在质量与成本上有差异。

### 第五步：启动构建

**构建主线：Codex CLI 当前会话**

Codex 已由你预装并配置会话凭据，无需固定模型版本或额外设置 API Key。直接在 PowerShell 中启动：

```powershell
$env:OMEGA_HOME = "D:\Omega-System"   # 或你的自定义路径
cd $env:OMEGA_HOME
mkdir omega-runtime -Force
cd omega-runtime

# 验证 Codex 可用（应输出版本号）
codex --version

# 启动构建（auto-edit 模式——每步展示 diff，等你确认）
codex --approval-mode auto-edit "OMEGA_HOME=$env:OMEGA_HOME。按照 $env:OMEGA_HOME/build-package/CODEX_RUN_PROMPT.md 的指示构建 Omega MFE 系统。先读取 AGENTS.md 和 BUILD_CHECKLIST.md，然后从迭代 0 开始。"
```

**备用方案：Claude Code + OpenRouter/国产 Claude Messages 兼容端点**

```powershell
$env:OMEGA_HOME = "D:\Omega-System"
cd $env:OMEGA_HOME
mkdir omega-runtime -Force
cd omega-runtime

# Claude Code 仅可通过非 Anthropic 的兼容 endpoint 接入
claude "OMEGA_HOME=$env:OMEGA_HOME。按照 $env:OMEGA_HOME/build-package/CODEX_RUN_PROMPT.md 的指示构建 Omega MFE 系统。先读取 AGENTS.md 和 BUILD_CHECKLIST.md，然后从迭代 0 开始。"
```

> ⚠️ **路径约定**：通过 `OMEGA_HOME` 环境变量指定部署根目录（默认 `D:\Omega-System`）。Codex 构建前会先确认此变量，所有路径从 `OMEGA_HOME` 派生。

### 第六步：逐迭代推进

Codex 每完成一个迭代会停下来。你审查后说"继续"即可。

预期总时间：Codex 构建 ~14 小时 + 人工审查 ~2 小时。

### 🆕 从 MFE 升级到完全体（v0.3.0 → v1.0.0）

如果 Omega MFE 已在当前电脑上构建完成（`omega bench --all` 返回 7/7），使用升级包将其升级为完全体：

```powershell
$env:OMEGA_HOME = "D:\Omega-System"   # 或你的自定义路径
cd $env:OMEGA_HOME\omega-runtime

# Codex 升级主线
codex "OMEGA_HOME=$env:OMEGA_HOME。按照 $env:OMEGA_HOME/omega-vault/omega生态系统项目/99-交付给Codex的构建包/CODEX_UPGRADE_PROMPT.md 的指示升级 Omega 到 v1.0.0-full。先读取 UPGRADE_GUIDE.md、UPGRADE_CHECKLIST.md 和 OMEGA_FINAL_FORM.md，然后从 Phase 2 开始。"
```

升级预计：Codex ~10-14 小时 + 人工审查 ~1.5 小时（11 个 Phase × 每阶段 ~1 小时）。

## 文件夹内容（共 58 个文件，含 13 个根文件 + 45 个子目录文件）

### 核心构建文件

| 文件 | 用途 |
|------|------|
| `AGENTS.md` | Codex 自动读取——项目约定、凭据规则、构建边界、上下文管理 |
| `CODEX_RUN_PROMPT.md` | 给 Codex 的优化初始提示词——可直接复制使用（MFE 构建） |
| `BUILD_CHECKLIST.md` | 四迭代逐项验收清单——逐条通过才能进入下一迭代 |
| `USER_ACTIONS.md` | **你的手动操作指南**——每步含"做什么→怎么做→确认成功"的可视化指引 |
| `README.md` | 你看的这个文件 |
| `MANIFEST.yaml` | 完整文件清单——构建 Agent 构建前交叉验证 |
| `PRODUCTION_IDENTITY_LEDGER.yaml` | 当前 realclaudian `main.js`、Omega 生产镜像及有效 receipts 的独立状态账本（无密钥） |

### 🆕 MFE → Full 升级包（4 个）

| 文件 | 用途 |
|------|------|
| `UPGRADE_GUIDE.md` | **Omega 完整升级指南**——11 阶段从 MFE 升级到完全体，含代码骨架、验证方法、设计文档索引 |
| `CODEX_UPGRADE_PROMPT.md` | **Codex 升级启动提示词**——可直接复制给 Codex 启动升级 |
| `UPGRADE_CHECKLIST.md` | **逐阶段验收清单**——11 个 Phase 逐项检查，全部通过才能进入下一阶段 |
| `OMEGA_FINAL_FORM.md` | **Omega 最终形态描述**——升级后你将拥有的完整系统长什么样 |

### JSON Schema（10 个）

| 文件 | 用途 |
|------|------|
| `schemas/task_contract.schema.json` | 任务契约字段约束 |
| `schemas/tool_card.schema.json` | 工具注册表字段约束 |
| `schemas/agent_card.schema.json` | Agent 注册表字段约束 |
| `schemas/legacy_agent_card.schema.json` | 只读旧 Agent 输入；未知字段/模型 ID 无损保留但不得直接进入 current |
| `schemas/model_policy.schema.json` | Codex-first provider 与原生 Anthropic 禁令约束 |
| `schemas/production_identity_ledger.schema.json` | 生产身份账本、SHA 与 receipt supersession 约束 |
| `schemas/outcome_package.schema.json` | 多模态成果包结构约束 |
| `schemas/skill.schema.json` | Skill 沉淀记录字段约束 |
| `schemas/action_memory.schema.json` | 行动记忆记录字段约束 |
| `schemas/terminal_event.schema.json` | 🆕 Omega Terminal 统一事件协议——13 种事件类型（含 task_replay），确保"任何反馈都能进窗口" |

### 种子配置（12 个）

| 文件 | 用途 |
|------|------|
| `config/model_capabilities.yaml` | Codex-first 能力角色、provider 链、动态发现与迁移规则的单一真相源 |
| `config/agent_role_mapping.yaml` | 概念 Agent 到 11 个 current runtime Agent 的引用映射 |
| `config/tools.yaml` | Codex/OpenAI 主链、兼容 Claude Messages 与国内备用工具注册表 |
| `config/agents.yaml` | Agent 绑定稳定能力角色，具体模型由 Engine Resolver 解析 |
| `config/.env.example` | 16 个环境变量模板——含 [REQUIRED-TIER0/1/2] 分层标记和获取 URL |
| `config/routing_table.yaml` | 16 种任务类型 × 多阶段工具/Agent 冷启动路由（质量敏感/成本敏感分策略） |
| `config/stage_weights.yaml` | 8 阶段 × 12 维度动态权重覆盖 |
| `config/risk_policy.yaml` | 四域风险升级策略 + 替换决策矩阵 + 回滚规则 |
| `config/engine_resolution.yaml` | 语言引擎解析策略——分层降级，质量敏感/成本敏感分策略 |
| `config/api_tiers.yaml` | **新增**：API 分层部署协议——部署时 Codex 逐层询问用户可用 API，生成 active_engines.yaml |
| `config/deployment_profiles.yaml` | **新增**：4 种预置部署方案（full_power/balanced/domestic_enhanced/minimal），Codex 按用户 API 可用性自动匹配 |
| `config/HERMES_ORCHESTRATOR_PROMPT.md` | 兼容文件名下的 Codex-first Orchestrator 提示词；旧固定团队叙述已 superseded |

### 验收测试数据（5 个）

| 文件 | 用途 |
|------|------|
| `fixtures/tasks/literature_ingestion_task.md` | 闭环 1 验收：文献搜索与知识摄取（Zotero 条件同步） |
| `fixtures/tasks/data_analysis_task.md` | 闭环 3 验收：数据分析 + 图表 + 报告 |
| `fixtures/tasks/tool_comparison_task.md` | 闭环 10 验收：Blender vs Manim 工具对比 |
| `fixtures/tasks/tool_learning_task.md` | 闭环 11 验收：双沙箱工具学习与注册 |
| `fixtures/data/sample_clinical.csv` | 20 行模拟临床数据（含缺失值） |

### Docker 与 MCP 模板（4 个）

| 文件 | 用途 |
|------|------|
| `templates/docker-compose.yml` | PostgreSQL + Qdrant + 双沙箱完整编排 |
| `templates/Dockerfile.sandbox` | Execution Sandbox（无网络/只读/非root） |
| `templates/Dockerfile.sandbox-net` | Toolsmith Sandbox（有限网络/可写） |
| `templates/mcp-config.json` | 8 个 MCP Server 配置模板（2 个禁用，阶段 2 启用） |

### 上下文管理与运行时模板（3 个 + 2 个 🆕 质量模板）

| 文件 | 用途 |
|------|------|
| `templates/BUILD_STATE.md` | 构建状态模板——构建 Agent 每步更新，重启后恢复上下文 |
| `templates/DECISIONS.md` | 关键决策日志模板——记录不可逆设计决策及理由 |
| `templates/active_engines.yaml` | 活跃引擎注册表模板——记录 available/deferred/unavailable_confirmed，Engine Resolver 运行时读取 |
| `templates/VISION_TRACE.yaml` | 🆕 方法论原则→代码追踪矩阵——防止"理念很美代码漏掉"，CI 接入四条件验证 |
| `templates/BENCHMARK_CATALOG.yaml` | 🆕 闭环目录唯一权威源——稳定字符串 ID，五层验收定义，跨文档编号映射 |

### 🆕 部署契约（1 个）

| 文件 | 用途 |
|------|------|
| `DEPLOYMENT_CONTRACT.md` | 全权部署边界——Codex 可自动/需确认/永不自动三类操作定义 |

### 🆕 Omega Terminal 设计规范（1 个）

| 文件 | 用途 |
|------|------|
| `OMEGA_TERMINAL.md` | 🆕 Omega Terminal 统一操作窗口设计蓝图——16 节完整规范，含 9 层上传安全防护、任务回放、命令面板一等功能、高风险动作强制 terminal_event。Phase 10 实现依据 |

### 脚本（6 个）与对抗测试（3 个）

| 文件 | 用途 |
|------|------|
| `scripts/setup.ps1` | Windows 环境一键配置脚本（6 步自动化） |
| `scripts/endpoint_policy.ps1` | fail-closed 端点解析/规范化及环境变量策略 |
| `scripts/assemble_package.ps1` | 交付前完整性检查脚本 |
| `scripts/sandbox-net-filter.sh` | omega-sandbox-net 网络过滤（iptables） |
| `scripts/model_policy_runtime.py` | 动态端点验证、无损迁移、原子替换与回滚 CLI |
| `scripts/package_gate.py` | MANIFEST/parse/schema/reference/登记/对抗测试总门禁 |
| `tests/test_model_policy_runtime.py` | URL、redirect、迁移、原子性与回滚对抗测试 |
| `tests/test_package_gate.py` | required 缺失与未登记活动文件的负例测试 |
| `tests/test_endpoint_policy.ps1` | PowerShell URL/环境变量混淆负例测试 |

交付前必须执行：

```powershell
python .\scripts\package_gate.py --package .
.\scripts\assemble_package.ps1 -CheckOnly
```

Engine resolver/migrator 的稳定契约：`resolve <policy> <capability_role> <health>`、`validate <path>`、`migrate <legacy> <current>`、`restore <envelope> <target>`、`rollback <target>`。解析器按能力角色和实时健康状态选择候选，不固定模型 ID；迁移先完整验证候选，再以同目录临时文件和原子替换提交，失败不得改写 current。

## 需要配套复制的内容

下列文件不在本文件夹中（它们在 Omega 项目的其他位置），需要你手动复制：

- [ ] `omega生态系统项目/` — 全部 24 个设计文件（00~11 目录）
- [ ] `CLAUDE.md` — Claude 行为配置（如果也用 Claude Code）
- [ ] `wiki/` — 已有知识库（可选，迁移时附带）
