# Omega v1.0.0-full — 最终形态

> **当 Codex 完成全部 11 个升级阶段后，Omega 将达到的完全体形态。**
> 这不是设计文档——是升级完成后你将实际拥有的系统。

---

## 一句话概括

**Omega v1.0.0-full 是一个具备自主感知-规划-执行-进化能力的个人 AI 研究操作系统。** 你用自然语言下达任务，Omega 自主选择最佳工具和 Agent、规划并行执行路线、记录经验、在沙箱中发现和测试新工具、自我演化升级——全部在本地 Docker 基础设施上运行。**但它不是"全自动 AI 科学家"：API Key 配置、外部账号登录、系统级变更、危险操作仍需你确认。**

---

## 核心能力矩阵

```
┌─────────────────────────────────────────────────────────────────┐
│                   Omega v1.0.0-full 能力全景                      │
│                                                                 │
│  📚 知识摄取    │  PubMed/PDF/Zotero/网页 → 结构化 wiki 知识库     │
│  📊 数据分析    │  CSV/SAS/Parquet → 统计建模 + 交互式图表          │
│  🔬 文献综述    │  自动搜索→筛选→全文提取→综合报告→PPT生成         │
│  🧪 工具学习    │  连接 PyPI/GitHub/npm → 沙箱安装→隔离验收→注册   │
│  ⚖️ 工具对比    │  多维度评分 → 对比wiki → 升级推荐                │
│  🔄 质量改进    │  检测弱项 → 搜索更好工具 → 重新生成 → 对比报告    │
│  🧬 科学可视化  │  matplotlib → plotly → (manim/blender 尽力而为)  │
│  🎨 创意工具    │  12 种创意任务 × 5 维创意评分                   │
│  🌐 浏览器自动化│  Playwright MCP — 表单/截图/数据提取             │
│  🧠 记忆学习    │  PostgreSQL 行动记忆 + Qdrant 语义记忆           │
│  📈 自我演化    │  定时检测过时工具 → 沙箱测试 → 受控升级建议      │
│  🖥️ Web 界面   │  FastAPI + 8420 端口 — 浏览器提交/查看任务       │
│  🪟 Omega终端   │  Omega Terminal — 统一操作窗口（类 VS Code 布局）  │
│  🔔 Obsidian通知│  任务完成自动写入 vault 通知文件                 │
│  🔍 模拟构建器  │  每阶段生成 DAG+风险+变更清单→用户审查后执行     │
│  ✈️ 飞行记录仪  │  每任务完整审计：输入/路由/模型/成本/产物来源    │
│  🔗 溯源水印    │  每个结论可追溯至文献 DOI/代码 commit/模型调用   │
│  💰 预算控制台  │  4 模式自动选择：省钱/高质量/离线/平衡           │
│  🛡️ 工具隔离    │  Toolsmith 新工具→隔离区验收→签名→正式注册       │
│  🚰 知识防污染  │  AI 输出→候审区→6 项自动检查→合并/拒绝          │
│  🔮 基准预言机  │  闭环运行→6 维质量指标 vs 金标准→偏差报告         │
│  🏠 显式本地灾备 │ 用户授权后启用（Ollama→LM Studio→纯脚本），默认关闭       │
│  📋 演化提案    │  ECP 审批流程：变更摘要→风险评估→回滚方案→审批    │
└─────────────────────────────────────────────────────────────────┘
```

---

## 用户交互方式

### 方式 1：Obsidian 内自然语言（日常使用）

在 Obsidian 中打开终端（或任何对话界面），用自然语言下指令：

```
"搜5篇SGLT2抑制剂在心衰中的最新文献，L3深度处理"

"分析 ukb_social_genomics/data/normalizedProtein.csv，做蛋白QC和PCA"

"对比一下当前文献中关于阿尔茨海默病血液生物标志物的诊断性能"

"帮我学一下这个新的Python包 textstat，测试后注册到工具库"

"重新生成第三个项目的PPT，用更好的模板，覆盖之前的结果"
```

**Omega 的响应流程**：
1. `classify_task()` 解析意图 → 确定 task_type
2. `DynamicScorer`（12 维评分）从工具注册表选最佳工具
3. `AgentDispatcher` 分配最合适的 Agent
4. `DynamicTaskPlanner` 生成并行 DAG 执行计划
5. 在 Docker 沙箱中安全执行
6. 结果写入 `wiki/` 或 `omega-workspace/outputs/`
7. `OutcomeBuilder` 组装成果包
8. `ScoreFeedbackLoop` 更新工具评分（学得更聪明）

### 方式 2：Omega Terminal（统一操作窗口）✨ 推荐

浏览器打开 `http://localhost:8420` 或独立桌面窗口（`omega web --electron`）：

```
┌──────────────────────────────────────────────────────────┐
│  ≡  Omega Terminal                        ─  □  ×        │
├──────────┬──────────────────────────┬────────────────────┤
│  📁 文件  │  💬 对话区               │  📋 上下文面板      │
│  浏览器   │  用户: 搜5篇SGLT2抑制剂  │  当前任务 / 进度    │
│          │  Omega: 🔍 检索中...      │  活跃工具 / 历史    │
├──────────┴──────────────────────────┴────────────────────┤
│  > 输入指令或 Ctrl+Shift+P 命令面板...                     │
└──────────────────────────────────────────────────────────┘
```

**核心功能**：
- 💬 自然语言输入——直接说"搜5篇糖尿病文献，L3处理"
- ⌨️ 命令面板（Ctrl+Shift+P）——所有 Omega 功能一键可达
- 📁 拖拽上传——PDF/CSV/PPTX 拖入窗口自动识别并建议处理方式
- 📊 实时监控——任务进度条、日志流、DAG 可视化
- 🔔 通知中心——所有 Omega 汇报/请求/警告汇聚一处
- ✅ 交互式确认——需要你决策的事项以对话框呈现（不再只是终端文字）
- 🎨 类 VS Code 布局——文件浏览器 | 对话区 | 上下文面板三段式

详见：`build-package/OMEGA_TERMINAL.md`

### 方式 3：Obsidian 内自然语言（日常轻量）

在 Obsidian/Claudian 中打开 Codex 对话界面，用自然语言下指令（与方式 2 共享同一后端）

### 方式 4：CLI 命令（脚本/自动化）

```bash
omega task "分析最近的临床试验数据" --execute
omega bench --all              # 验证系统完整性
omega status                   # 查看所有服务健康状态
omega evolve --check           # 检查可升级工具
omega evolve --upgrade numpy   # 升级特定工具
omega radar                    # 扫描工具生态新工具
omega web --port 8420          # 启动 Web 界面
omega service start            # 启动后台常驻服务

# 🆕 质量与安全命令（Phase 11）
omega simulate phase-3         # 模拟构建——查看 DAG/风险/变更清单（不修改代码）
omega flightlog <task_id>      # 查看任务完整审计记录（输入→路由→成本→产物）
omega budget cheap             # 切换省钱模式（economical_general 能力角色）
omega budget high_quality      # 切换高质量模式（quality_reasoning 能力角色，全验证）
omega quarantine list          # 查看工具隔离区（新工具等待验收）
omega quarantine promote <id>  # 推广已签名工具到正式注册表
omega review list              # 查看知识候审区（AI输出等待合并）
omega review approve <id>      # 手动批准候审内容写入知识库

# 🆕 基准预言机与演化控制（Phase 11 + ECP）
omega oracle run --all          # 运行全部闭环 vs 金标准，生成偏差报告
omega oracle report             # 查看最新偏差报告
omega oracle calibrate --loop 5 # 校准闭环阈值
omega provenance <claim_id>     # 验证指定结论的溯源链完整性
omega evolve --propose <tool>   # 为工具升级生成 ECP 变更提案
omega evolve approve <ecp_id>   # 审批 ECP
omega evolve list-ecps          # 列出所有演化决策历史
omega local-engine status       # 检查本地 AI 引擎（Ollama/LM Studio/llama.cpp）
```

---

## 运行时组件全景

```
┌─────────────────────────────────────────────────────────────────────┐
│                     Omega v1.0.0-full 运行时                          │
│                                                                      │
│  ┌──────────────┐  ┌──────────────┐  ┌────────────────────────────┐ │
│  │ Obsidian     │  │ Web UI       │  │ CLI (omega task "...")      │ │
│  │ (自然语言)    │  │ (8420端口)   │  │ (脚本/自动化)               │ │
│  └──────┬───────┘  └──────┬───────┘  └──────────────┬─────────────┘ │
│         │                 │                         │               │
│         └─────────────────┼─────────────────────────┘               │
│                           ▼                                         │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │                    Task Gateway                              │   │
│  │          classify_task() → TaskContract                      │   │
│  │          11 种 task_type 自然语言分类                          │   │
│  └─────────────────────────────┬───────────────────────────────┘   │
│                                ▼                                    │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │              Tool-Agent Router (动态评分)                     │   │
│  │    静态路由表 → DynamicScorer (12维) → Engine Resolver        │   │
│  │    自适应工具选择 + 分层降级引擎选择                            │   │
│  └─────────────────────────────┬───────────────────────────────┘   │
│                                ▼                                    │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │              Dynamic Task Planner (并行DAG)                    │   │
│  │    模板匹配→依赖分析→能力预检→并行化→资源估算→生成DAG          │   │
│  └─────────────────────────────┬───────────────────────────────┘   │
│                                ▼                                    │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │              Agent Dispatcher (11 Agents)                     │   │
│  │    researcher / writer / critic / planner / knowledge_steward │   │
│  │    medical_evidence_agent / domain_expert / tool_smith         │   │
│  │    browser_agent / code_builder / orchestrator                 │   │
│  │    每 Agent 含: 工具白名单/黑名单 + 自主级别(L0-L3) + 交接目标  │   │
│  └─────────────────────────────┬───────────────────────────────┘   │
│                                ▼                                    │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │                  Execution Layer                              │   │
│  │  ┌───────────────┐  ┌──────────────────┐  ┌───────────────┐  │   │
│  │  │ omega-sandbox  │  │ omega-sandbox-net│  │ MCP Servers   │  │   │
│  │  │ (离线/安全执行) │  │ (联网/工具安装)   │  │ (8 servers)   │  │   │
│  │  │ Python 3.11    │  │ Python + pip     │  │ filesystem    │  │   │
│  │  │ numpy/pandas   │  │ git/curl/node    │  │ postgres      │  │   │
│  │  │ scipy/sklearn  │  │ npm/PyPI 访问    │  │ qdrant        │  │   │
│  │  │ matplotlib     │  │                  │  │ playwright    │  │   │
│  │  │ network: none  │  │ network: bridge  │  │ github        │  │   │
│  │  └───────────────┘  └──────────────────┘  │ brave-search  │  │   │
│  │                                            │ sequential-   │  │   │
│  │                                            │ thinking      │  │   │
│  │                                            │ memory        │  │   │
│  │                                            └───────────────┘  │   │
│  └─────────────────────────────┬───────────────────────────────┘   │
│                                ▼                                    │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │                    Memory Layer                               │   │
│  │  ┌─────────────────────┐  ┌─────────────────────────────┐   │   │
│  │  │ PostgreSQL (行动记忆) │  │ Qdrant (语义记忆)            │   │   │
│  │  │ task_history        │  │ tool_descriptions (向量)     │   │   │
│  │  │ tool_executions     │  │ task_patterns (向量)         │   │   │
│  │  │ agent_decisions     │  │ source_pages (向量)          │   │   │
│  │  └─────────────────────┘  └─────────────────────────────┘   │   │
│  └─────────────────────────────┬───────────────────────────────┘   │
│                                ▼                                    │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │                  Output Layer                                 │   │
│  │  ┌────────────────┐ ┌────────────────┐ ┌──────────────────┐ │   │
│  │  │ wiki/知识库     │ │ outcomes/成果包 │ │ logs/omega.log   │ │   │
│  │  │ 来源/实体/概念   │ │ 报告+图表+脚本  │ │ 结构化运行日志    │ │   │
│  │  │ 对比/洞察       │ │ +质量报告      │ │                  │ │   │
│  │  └────────────────┘ └────────────────┘ └──────────────────┘ │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                                                                      │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │                  Evolution Engine (后台)                       │   │
│  │    定时扫描工具生态 → 发现新版本 → 沙箱测试 → 质量对比         │   │
│  │    LOW→auto / MEDIUM→sandbox_test / HIGH→confirm / CRITICAL→no│   │
│  │    🆕 ECP：非LOW变更→生成ECP提案→人类审批→执行→归档审计        │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                                                                      │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │                  Background Service                           │   │
│  │    定时: 工具更新扫描 + MCP 健康检查 + 异步任务队列处理         │   │
│  │    通知: Obsidian vault 通知.md                               │   │
│  └─────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────┘
```

---

## 11 个 Agent 及其角色

| Agent | 角色 | 自主级别 | 首选引擎 | 典型任务 |
|-------|------|---------|---------|---------|
| **researcher** | 信息检索与搜集 | L2 | economical_general | 文献搜索、网页浏览 |
| **writer** | 内容撰写与润色 | L1 | academic_writing | 报告写作、PPT文案 |
| **critic** | 质量评估与审校 | L2 | quality_reasoning | 质量评分、错误检测 |
| **planner** | 任务规划与分解 | L3 | quality_reasoning | 复杂任务DAG生成 |
| **knowledge_steward** | 知识库维护 | L3 | economical_general | wiki页面创建/更新 |
| **medical_evidence_agent** | 医学证据评估 | L1 | quality_reasoning | GRADE评估、PICO分析 |
| **domain_expert** | 领域深度分析 | L2 | quality_reasoning | 专业问题解答 |
| **tool_smith** | 工具发现与注册 | L3 | engineering_primary | PyPI搜索、沙箱测试 |
| **browser_agent** | 浏览器自动化 | L2 | economical_general | 网页截图、表单填写 |
| **code_builder** | 代码生成与测试 | L2 | engineering_primary | Python脚本、数据分析 |
| **orchestrator** | 全局协调调度 | L3 | quality_reasoning | 多Agent协作、异常处理 |

---

## Full-Core 12 个基准闭环 + Full-Extended 扩展闭环

> **分层说明**：
> - **Full-Core**（12 个闭环）— 对应 `BENCHMARK_CATALOG.yaml` 中 `full` tier，是 Omega v1.0.0 的核心能力基线
> - **Full-Extended**（+1 扩展闭环）— 对应 `full_extended` tier，在 Full-Core 基础上增加系统自维护能力
> - 下表中第 12 行为 Full-Extended 专属扩展（`knowledge_base_health`），其余 12 行为 Full-Core 闭环

### Full-Core 12 个基准闭环

| # | 闭环名称 | Catalog ID | 验证的能力 |
|---|---------|-----------|-----------|
| 1 | 文献检索与知识摄取 | `literature_ingestion` | PDF → PubMed → Zotero → wiki/来源/ 页面 |
| 2 | PDF 文献深度处理 | `pdf_deep_processing` | PubMed PDF → Zotero → L3 深度笔记 → 概念链接 |
| 3 | 数据分析与统计报告 | `csv_analysis` | CSV → QC → 统计 → 图表 → 报告 |
| 4 | 代码生成与执行 | `code_generation` | 需求 → Python脚本 → 沙箱测试 → 输出 |
| 5 | PPT 生成 | `ppt_generation` | 文献/数据 → 模板匹配 → 图表嵌入 → .pptx |
| 6 | 质量改进闭环 | `quality_improvement` | 检测弱项 → 搜索工具 → 重新生成 → 对比 |
| 7 | 服务健康自检 | `service_health` | Docker/PostgreSQL/Qdrant/MCP 健康扫描 |
| 8 | 科学可视化 | `scientific_visualization` | matplotlib/plotly/manim → 图表/动画 |
| 9 | 浏览器自动化 | `browser_prefill` | Playwright → 截图/表单/数据提取 |
| 10 | 工具对比分析 | `tool_comparison` | 多工具 × 多维度 → 对比 wiki + 推荐 |
| 11 | 工具自主学习 | `tool_gap_learning` | PyPI/GitHub → 沙箱安装 → 测试 → 注册 |
| 12 | 演化自动升级 | `evolution_upgrade` | 检测过时 → 沙箱测试新版 → 质量对比 |

### Full-Extended 扩展闭环

| # | 闭环名称 | Catalog ID | 验证的能力 |
|---|---------|-----------|-----------|
| ★ | 知识库健康检查 | `knowledge_base_health` | 死链检测、孤儿扫描、索引同步、冲突检测、内容一致性校验 |

> **总计**：Full-Core 12 + Full-Extended 1 = **13 个基准闭环**（全部通过）。`knowledge_base_health` 是系统自维护闭环，在 Full-Core 12 个全部验收后单独启用，不参与 MFE-Alpha/Methodology/Plus 验收。

---

## Docker 容器拓扑

```
┌──────────────────────────────────────────────────────────┐
│                    Docker Network                         │
│                                                          │
│  ┌──────────────────┐  ┌──────────────────┐             │
│  │ omega-postgres   │  │ omega-qdrant     │             │
│  │ PostgreSQL 17    │  │ Qdrant v1.14     │             │
│  │ Port: 5432       │  │ Port: 6333/6334  │             │
│  │ Volume: pgdata   │  │ Volume: qdrant   │             │
│  │ Network: bridge  │  │ Network: bridge  │             │
│  └──────────────────┘  └──────────────────┘             │
│                                                          │
│  ┌──────────────────┐  ┌──────────────────┐             │
│  │ omega-sandbox    │  │omega-sandbox-net │             │
│  │ Python 3.11      │  │ Python 3.11      │             │
│  │ numpy/pandas     │  │ pip/git/curl     │             │
│  │ scipy/sklearn    │  │ Node.js 22       │             │
│  │ matplotlib       │  │ npm access       │             │
│  │ Network: NONE ❌  │  │ Network: bridge  │             │
│  │ (绝对离线安全)    │  │ (仅PyPI/GitHub)  │             │
│  └──────────────────┘  └──────────────────┘             │
│                                                          │
│  ┌──────────────────┐                                   │
│  │ omega-web         │  ← Phase 10 新增                  │
│  │ FastAPI :8420     │                                   │
│  │ Network: bridge   │                                   │
│  └──────────────────┘                                   │
└──────────────────────────────────────────────────────────┘
```

---

## 数据流示例

### 示例 1：文献综述任务

```
用户: "系统性综述SGLT2抑制剂在心衰中的肾脏保护作用"

  ↓ Task Gateway: classify_task() → "literature_search"
  ↓ Router: DynamicScorer 评分 → PubMed + Semantic Scholar
  ↓ Planner: 生成并行 DAG
      ├─ [并行] PubMed 检索 (researcher Agent)
      ├─ [并行] Semantic Scholar 检索 (researcher Agent)  
      └─ [等待] 合并去重 (knowledge_steward Agent)
           ├─ [并行] 全文提取 (researcher Agent)
           │    └─ pdftotext 在 omega-sandbox 中
           ├─ [并行] 质量评估 (critic Agent)
           └─ [等待] 综合分析 (writer Agent)
                └─ 输出: wiki/来源/ + wiki/对比/ + wiki/洞察/
  ↓ Memory: 记录 task_history + tool_executions
  ↓ Outcome: 组装文献综述成果包
  ↓ Feedback: 更新 PubMed/Semantic Scholar 工具评分
  ↓ Notify: 写入 Obsidian 通知.md
```

### 示例 2：工具自主学习

```
系统: 检测到任务缺少 "readability" 能力
  ↓ Toolsmith: detect_gap() → "文本可读性分析"
  ↓ Toolsmith: discover() → 搜索 PyPI "textstat"
  ↓ Toolsmith: install() → docker exec omega-sandbox-net pip install textstat
  ↓ Toolsmith: test() → docker exec omega-sandbox python -c "import textstat; ..."
  ↓ Toolsmith: generate_adapter() → 创建 Omega 接口包装
  ↓ Toolsmith: register() → 写入 config/tools.yaml
  ↓ Toolsmith: package_skill() → 创建 Skill 目录
  ↓ Evolution: 记录新工具到 tool_executions
  ↓ Outcome: "工具 textstat 已注册，可读性分析能力已补全"
```

### 示例 3：自我演化

```
后台服务 cron: 每周日凌晨 3:00
  ↓ Evolution: 扫描 config/tools.yaml
  ↓ Evolution: 检查每个工具的 PyPI/npm 最新版本
  ↓ Evolution: 发现 numpy 1.26 → 2.0（MAJOR 升级）
  ↓ Evolution: risk_policy → MAJOR → MEDIUM → sandbox_test
  ↓ Evolution: docker exec omega-sandbox-net pip install numpy==2.0
  ↓ Evolution: 运行 numpy 测试套件
  ↓ Evolution: 对比新旧版本质量分数
  ↓ Evolution: 质量提升 → 建议升级
  ↓ Notify: "numpy 可升级 1.26→2.0，沙箱测试通过，质量提升 12%"
  ↓ 用户确认后 → 自动更新 config/tools.yaml + requirements.txt
```

---

## 目录结构（最终状态）

```
{OMEGA_HOME}/
├── .env                          # API Key 等敏感配置（不提交 git）
├── omega.yaml                    # Omega 配置文件
│
├── omega-runtime/                # Omega 运行时
│   ├── Dockerfile.sandbox        # 离线安全沙箱（Python 3.11）
│   ├── Dockerfile.sandbox-net    # 联网工具沙箱（Python + Node + pip）
│   ├── docker-compose.yml        # 6 容器编排
│   ├── requirements.txt          # Python 依赖
│   ├── app/
│   │   ├── main.py               # CLI 入口（20+ 命令）
│   │   ├── config.py             # Pydantic v2 配置模型
│   │   ├── logging_setup.py      # 结构化日志系统
│   │   ├── gateway/              # 任务网关（NL→TaskContract）
│   │   ├── router/               # 动态评分路由器
│   │   │   ├── router.py         #   ToolAgentRouter
│   │   │   ├── scorer.py         #   DynamicScorer（12维）
│   │   │   ├── feedback.py       #   ScoreFeedbackLoop
│   │   │   ├── engine_resolver.py#   Engine Resolver（4策略）
│   │   │   ├── budget_console.py #   预算与质量控制台（🆕 Phase 11）
│   │   │   └── local_engine.py   #   本地引擎回退管理（🆕 Phase 11）
│   │   ├── planner/              # 动态任务规划器
│   │   │   ├── planner.py        #   7 步规划流程
│   │   │   ├── dag.py            #   并行 DAG 生成
│   │   │   ├── dependency.py     #   依赖分析器
│   │   │   ├── gap_check.py      #   能力缺口预检
│   │   │   └── templates/        #   任务模板库（JSON）
│   │   ├── agents/               # Agent 运行时
│   │   │   ├── agent.py          #   AgentRuntime
│   │   │   ├── dispatcher.py     #   AgentDispatcher
│   │   │   └── capability.py     #   CapabilityChecker
│   │   ├── executor/             # 执行器
│   │   │   ├── closed_loop.py    #   闭环执行引擎（13 loops）
│   │   │   ├── ppt_generator.py  #   PPT 生成与 8 维分析
│   │   │   ├── tool_discovery.py #   工具发现引擎
│   │   │   ├── viz_executor.py   #   科学可视化管线
│   │   │   ├── browser_executor.py#  浏览器自动化
│   │   │   ├── creative_router.py#   创意任务路由器
│   │   │   └── benchmark_oracle.py#  基准预言机（🆕 Phase 11.7）
│   │   ├── mcp/                  # MCP 服务器管理器
│   │   │   └── manager.py        #   8 MCP Server 生命周期
│   │   ├── toolsmith/            # 工具锻造系统
│   │   │   ├── smith.py          #   完整 7 步闭环
│   │   │   ├── adapter.py        #   工具适配器
│   │   │   └── quarantine.py     #   工具隔离与签名（🆕 Phase 11）
│   │   ├── memory/               # 记忆层
│   │   │   ├── action_store.py   #   PostgreSQL 行动记忆
│   │   │   ├── semantic_store.py #   Qdrant 语义记忆
│   │   │   ├── flight_recorder.py#   任务飞行记录仪（🆕 Phase 11）
│   │   │   └── schema.sql        #   DDL
│   │   ├── evolution/            # 演化引擎
│   │   │   ├── engine.py         #   自动升级 + 风险策略
│   │   │   └── ecp.py            #   Evolution Change Proposal 管理器（🆕 Phase 8）
│   │   ├── outcome/              # 成果包组装器
│   │   │   ├── builder.py        #   8 种模态成果包
│   │   │   └── provenance.py     #   溯源水印（🆕 Phase 11）
│   │   ├── safety/               # 安全守卫
│   │   │   ├── privacy.py        #   数据隐私分级
│   │   │   ├── guardian.py       #   文件访问控制
│   │   │   ├── codex_guard.py    #   Codex 安全验证
│   │   │   ├── simulator.py      #   模拟构建器（🆕 Phase 11）
│   │   │   ├── kb_guard.py       #   知识防污染守卫（🆕 Phase 11）
│   │   │   └── flight_recorder.py#   任务飞行记录仪（🆕 Phase 11）
│   │   ├── web/                  # Omega Terminal（🆕 Phase 10 扩展）
│   │   │   ├── app.py            #   FastAPI + WebSocket + 静态挂载
│   │   │   ├── ws.py             #   WebSocket 管理器
│   │   │   ├── api/              #   API 子模块
│   │   │   │   ├── task_api.py   #   任务 CRUD
│   │   │   │   ├── upload_api.py #   文件上传 + 识别
│   │   │   │   ├── notify_api.py #   通知推送
│   │   │   │   └── vault_api.py  #   文件浏览/搜索
│   │   │   └── terminal/         #   React SPA（dist 挂载）
│   │   ├── service.py            # 后台常驻服务 + 任务队列
│   │   └── notify.py             # 双通道通知（WebSocket + vault）
│   ├── config/                   # 运行时配置
│   │   ├── agents.yaml           #   11 个 Agent 定义
│   │   ├── tools.yaml            #   工具注册表（持续增长）
│   │   ├── routing_table.yaml    #   任务路由表
│   │   └── active_engines.yaml   #   活跃引擎注册
│   │   └── benchmark_oracle.yaml  #   基准预言机配置（🆕 Phase 11.7）
│   ├── tests/                    # 测试套件（140+ tests）
│   ├── logs/                     # 运行日志
│   │   └── omega.log
│   └── ITERATION_*_REPORT.md     # 升级报告
│
├── omega-workspace/              # 工作空间
│   ├── sandbox/                  # 沙箱挂载（共享给容器）
│   ├── projects/                 # 项目目录
│   ├── outputs/                  # 任务输出
│   ├── outcomes/                 # 成果包输出（Phase 8）
│   ├── state/                    # 状态文件
│   │   ├── tool_scores.json      # 动态评分数据
│   │   └── ecps/                 # ECP 演化提案归档（🆕 Phase 8）
│   ├── review/                   # 知识候审区（🆕 Phase 11）
│   ├── quarantine/               # 工具隔离区（🆕 Phase 11）
│   └── gold_standard/            # 闭环金标准数据（🆕 Phase 11.8）
│
└── omega-vault/                  # 知识库
    ├── CLAUDE.md
    ├── wiki/                     # 知识页面
    │   ├── index.md
    │   ├── log.md
    │   ├── 来源/
    │   ├── 实体/
    │   ├── 概念/
    │   ├── 对比/
    │   └── 洞察/
    └── omega生态系统项目/         # 设计文档
        └── 99-交付给Codex的构建包/
            ├── UPGRADE_GUIDE.md            # 本升级指南
            ├── CODEX_UPGRADE_PROMPT.md     # Codex 启动提示词
            ├── UPGRADE_CHECKLIST.md        # 逐阶段验收清单
            └── OMEGA_FINAL_FORM.md          # 本文件：最终形态描述
```

---

## 与 v0.3.0-mfe 的关键差异

| 维度 | v0.3.0-mfe | v1.0.0-full |
|------|-----------|-------------|
| **工具选择** | 静态路由表查表 | 12 维动态评分 + 反馈学习 |
| **Agent** | 字符串注解，无约束 | 11 个 Agent 运行时，白名单/黑名单/自主级别门控 |
| **规划** | 线性 DAG（单链） | 并行 DAG（7 步流程 + 模板匹配 + 能力预检） |
| **沙箱** | qdrant 镜像（无 Python） | python:3.11-slim（numpy/pandas/scipy/matplotlib + pip + node） |
| **工具学习** | 仅发现步骤 | 完整 7 步闭环（发现→安装→适配→测试→注册→Skill） |
| **MCP** | JSON 配置，无代码 | 8 MCP Server 生命周期管理 |
| **记忆** | 无状态 | PostgreSQL 行动记忆 + Qdrant 语义记忆 |
| **演化** | YAML 定义，未使用 | 自动检测 + 沙箱测试 + 质量对比 + 建议升级 |
| **成果包** | 无 | 8 种模态自动组装 |
| **日志** | 无 | 结构化日志系统 |
| **可视化** | matplotlib 基础 | 4 路线（matplotlib/plotly/manim/blender） |
| **浏览器** | 无 | Playwright 自动化 |
| **Omega Terminal** | 无 | 统一操作窗口（类 VS Code/React/WebSocket/拖拽上传/命令面板/通知中心） |
| **Web UI** | 无 | FastAPI 后端 + React SPA + WebSocket（:8420） |
| **后台服务** | 无 | 常驻进程 + 定时扫描 + 异步队列 |
| **通知** | 无 | Obsidian 通知.md |
| **模拟构建** | 无 | 每阶段 DAG+风险+变更清单→审查后执行 |
| **飞行记录** | 无 | 每任务完整审计（输入/路由/成本/产物来源） |
| **溯源水印** | 无 | 每个结论可追溯至文献 DOI/代码 commit/模型调用 |
| **预算控制** | 无 | 4 模式：省钱/高质量/离线/平衡 |
| **工具隔离** | 无 | 新工具→隔离验收→签名→正式注册 |
| **知识防污染** | 无 | AI 输出→候审区→6 项检查→合并/拒绝 |
| **基准预言机** | 无 | 闭环 vs 金标准 6 维质量度量 + 偏差报告 |
| **本地灾备** | 仅 Cloud API | 默认关闭，用户显式授权后启用 Ollama/LM Studio/纯脚本 |
| **演化提案** | 无 | ECP 审批流程（变更摘要→风险评估→回滚→审批）|
| **闭环数** | 4 loops (MFE-Alpha) | 12 Full-Core + 1 Full-Extended = 13 loops |
| **测试数** | 72 tests | 140+ tests |
| **总文件** | ~25 源文件 | ~98+ 源文件 |
| **版本号** | v0.3.0-mfe | v1.0.0-full |

---

## 现实边界：Omega 能做什么、不能做什么

> **这不是一个"全自动 AI 科学家"。** Omega 是一个工程上可运行、可验收、可继续进化的个人 AI 研究操作系统。但真正的"完全体"不是一次构建完成的静态软件——需要在你的真实工作流里持续校准。

### Omega 能可靠做到的事

| 能力 | 把握度 | 说明 |
|------|--------|------|
| 文献检索与知识摄取 | 高 | PubMed/Semantic Scholar API + Zotero 集成 |
| 数据分析（CSV/SAS/Parquet） | 高 | Python 沙箱 + numpy/pandas/scipy/matplotlib |
| 代码生成与测试 | 高 | Codex CLI 主链；兼容 Claude Code 仅备用 |
| 浏览器自动化 | 高 | Playwright MCP（表单/截图/数据提取） |
| CLI 命令行入口 | 高 | 20+ 命令，Click + Rich |
| 文献综述报告 | 中高 | 依赖引擎质量，质量因 API 而异 |
| 12 维动态评分路由 | 中高 | 冷启动后需真实任务数据校准 |
| 工具自主学习（Python 包） | 中 | PyPI 搜索→沙箱安装→测试→注册，成功率因包而异 |
| 行动记忆（PostgreSQL） | 中 | 数据库可运行，但"记得有用、检索准确"需迭代 |
| 语义记忆（Qdrant） | 中 | 向量索引可运行，但检索质量需要真实数据调优 |
| 科学可视化线（matplotlib/plotly） | 中高 | 统计图表可靠生成 |

### 需要你参与的边界

| 边界 | 为什么 |
|------|--------|
| **API Key 配置** | Omega 不能替你注册和付费 |
| **外部账号（Zotero/GitHub/PubMed）** | 需要你授权 |
| **系统级操作（环境变量/注册表/防火墙）** | 安全边界，必须人工确认 |
| **上传/投稿/发表** | 不能自动提交表单到外部 |
| **Docker 卷删除** | 数据不可恢复，必须你确认 |
| **自动升级的 HIGH/CRITICAL 级别** | 可能破坏现有功能 |
| **manim/blender 安装与配置** | 需要特定的运行时/字体/GPU 环境 |

### 需要多轮真实任务打磨的能力

| 能力 | 现状 | 打磨方向 |
|------|------|---------|
| 长期记忆质量 | 能存储，但检索精准度未知 | 真实任务反馈 → 调整向量索引参数 |
| 自动演化安全性 | 框架已就，但"不受控地改核心"危险 | 保守策略：仅自动升级 LOW 域，其余需确认 |
| 学术写作质量 | 依赖运行时能力 | academic_writing 角色动态选择并以独立 critic 复核 |
| 跨文献综合洞察 | 由 Omega 检索与证据综合管道完成（NotebookLM 已排除） | 任务卡片迭代 |
| 知识库长期一致性 | lint + 冲突检测已就 | 需持续使用发现边界情况 |

---

## 一句话总结

**Omega v1.0.0-full** 不是一个你"使用"的工具——它是一个你"居住其中"的 AI 研究操作系统。你用自然语言描述想做什么，Omega 自主完成从搜索、分析、写作、可视化到自我改进的全流程——结果直接落入你的 Obsidian 知识库，成为你"第二大脑"持续生长的新枝。但它是**受控自主**的：安全边界需要你，关键决策需要你，打磨进化需要你。

---

*最终形态版本：v1.2 — 2026-05-17*
*此文档描述的是 CODE UPGRADE GUIDE 中 11 个 Phase 全部完成后的系统状态。*
*变更 v1.2：新增基准预言机（Benchmark Oracle）、本地引擎回退（Local-First Fallback）、ECP 演化提案审批流程；能力矩阵/CLI/差异对比表/目录结构同步更新*
*变更 v1.1：新增 Phase 11（质量与安全加固——6 项安全特性），新增现实边界说明，语言更加务实。*
