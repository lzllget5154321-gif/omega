---
type: concept
tags: [omega-ecosystem, runtime-architecture, deployment, system-design, agent-os]
created: 2026-05-15
updated: 2026-05-15
knowledge_stability: evolving
parent: [[Omega运行形态与本体文件说明]]
related:
  - [[Omega生态系统项目-功能优先总方法论]]
  - [[omega.yaml]]
  - [[Stage-Aware Tool-Agent Router]]
  - [[Dynamic Task Planner：动态任务规划器]]
---

# Omega Runtime Architecture

> **定位**：本文档定义 Omega 运行时层的完整架构——从 CLI 入口到 Agent 执行引擎，从任务队列到成果包输出。它是 `omega-runtime/` 代码仓库的设计蓝图。

---

## 一、运行时层总览

```
┌─────────────────────────────────────────────────────────────────┐
│                      Omega Runtime Layer                         │
│                                                                   │
│  ┌─────────┐   ┌──────────┐   ┌────────────┐   ┌─────────────┐ │
│  │  CLI    │   │  Web UI  │   │   Daemon   │   │  Obsidian   │ │
│  │ omega   │   │ :8420    │   │ 后台服务    │   │  命令面板   │ │
│  └────┬────┘   └────┬─────┘   └─────┬──────┘   └──────┬──────┘ │
│       │             │               │                  │        │
│       └─────────────┴───────────────┴──────────────────┘        │
│                            │                                      │
│                   ┌────────┴────────┐                            │
│                   │   Task Gateway  │  ← 统一任务入口             │
│                   └────────┬────────┘                            │
│                            │                                      │
│       ┌────────────────────┼────────────────────┐                │
│       ↓                    ↓                    ↓                │
│  ┌──────────┐     ┌──────────────┐     ┌──────────────┐        │
│  │ Dynamic  │     │ Stage-Aware │     │ Safety       │        │
│  │ Task     │────→│ Tool-Agent  │────→│ Enforcer     │        │
│  │ Planner  │     │ Router      │     │              │        │
│  └──────────┘     └──────────────┘     └──────────────┘        │
│                            │                                      │
│       ┌────────────────────┼────────────────────┐                │
│       ↓                    ↓                    ↓                │
│  ┌──────────┐     ┌──────────────┐     ┌──────────────┐        │
│  │ Capability│    │ Agent        │     │ Toolsmith    │        │
│  │ Fabric   │     │ Society      │     │ Lite         │        │
│  │ (工具调用) │     │ (Agent执行)  │     │ (工具学习)    │        │
│  └──────────┘     └──────────────┘     └──────────────┘        │
│                            │                                      │
│                   ┌────────┴────────┐                            │
│                   │ Outcome Package │  ← 成果组装与输出           │
│                   └────────┬────────┘                            │
│                            │                                      │
│       ┌────────────────────┼────────────────────┐                │
│       ↓                    ↓                    ↓                │
│  ┌──────────┐     ┌──────────────┐     ┌──────────────┐        │
│  │ Action    │    │ Skill        │     │ Evolution    │        │
│  │ Memory    │     │ Library     │     │ Loop         │        │
│  └──────────┘     └──────────────┘     └──────────────┘        │
│                                                                   │
└─────────────────────────────────────────────────────────────────┘
```

---

## 二、各组件详细设计

### 2.1 Task Gateway（统一任务入口）

**职责**：接收来自所有用户界面的任务请求，统一格式化为 Task Contract。

**支持的入口**：
- CLI：`omega task "帮我把这5篇PDF处理了"`
- Web UI：任务输入框
- Daemon：定时触发的任务或事件驱动的任务
- Obsidian 命令面板：在 Obsidian 中直接发起任务

**输入 → 输出**：
```
自然语言命令 → Task Gateway → 结构化 Task Contract
```

**Task Contract 格式**：

```yaml
task_contract:
  task_id: "omega-task-2026-0515-042"
  user_goal: "帮我把这5篇SGLT2抑制剂PDF处理并写综述初稿"
  task_type: "medical_research"
  complexity: "workflow"
  autonomy_level: "L2"
  expected_outcome:
    primary_deliverables:
      - "wiki/洞察/SGLT2抑制剂肾脏保护综述初稿.md"
      - "5个wiki/来源/页面"
    secondary_deliverables:
      - "Zotero条目"
      - "证据表"
      - "补充检索记录"
  required_capabilities:
    - "PDF文本提取"
    - "学术文献处理"
    - "GRADE评级"
    - "学术写作"
  safety_route: "医学内容需MEA审查"
  stop_conditions:
    - "PDF不可提取（付费墙）→ 仅基于摘要处理"
    - "数据不足以支持综述 → 标注为初步探索"
  fallback_plan:
    - "如果PubMed不可用 → 切换到Semantic Scholar"
  deadline: null
  priority: "normal"
```

### 2.2 Dynamic Task Planner（动态任务规划器）

**职责**：将任务契约中的用户目标分解为可执行的步骤 DAG。

详见：[[Dynamic Task Planner：动态任务规划器]]

### 2.3 Stage-Aware Tool-Agent Router（阶段感知路由器）

**职责**：为每个执行阶段选择最优工具和 Agent，考虑阶段特征。

详见：[[Stage-Aware Tool-Agent Router]]

### 2.4 Safety Enforcer（安全执行器）

**职责**：在执行前检查操作风险，必要时改变执行路径或请求确认。

详见：[[Safety-as-Enabler]]

### 2.5 Capability Fabric（工具调用层）

**职责**：统一的工具适配和调用接口。将外部工具抽象为标准化能力。

```python
# 伪代码示例
class CapabilityFabric:
    def __init__(self, config):
        self.adapters = self.load_adapters(config.tools.registry)
    
    def execute(self, capability: str, params: dict) -> ToolResult:
        adapter = self.adapters.get(capability)
        if not adapter:
            raise CapabilityNotFoundError(capability)
        
        # 安全检查
        SafetyEnforcer.check(capability, params)
        
        # 执行
        result = adapter.execute(params)
        
        # 记录
        ActionMemory.record_tool_use(capability, params, result)
        
        return result
```

### 2.6 Productive Agent Society（Agent 执行层）

**职责**：根据 Router 的选择，调度 Agent 执行任务。

```python
class AgentScheduler:
    def dispatch(self, task_step: TaskStep, assigned_agent: Agent) -> AgentResult:
        agent = self.agent_pool.get(assigned_agent.name)
        result = agent.execute(task_step)
        ActionMemory.record_agent_execution(assigned_agent, task_step, result)
        return result
```

### 2.7 Toolsmith-Lite（工具学习引擎）

**职责**：当 Capability Fabric 中无匹配工具时，搜索、试用和封装新工具。

详见：[[Toolsmith-Lite与Skillsmith]]

### 2.8 Outcome Package Builder（成果包组装器）

**职责**：组装任务的完整交付物包。

```python
class OutcomePackageBuilder:
    def build(self, task: TaskContract, results: list[StepResult]) -> OutcomePackage:
        return OutcomePackage(
            task_id=task.task_id,
            deliverables=self.collect_deliverables(results),
            intermediate_artifacts=self.collect_artifacts(results),
            tools_used=self.summarize_tools(results),
            agents_used=self.summarize_agents(results),
            risk_notes=self.collect_risk_notes(results),
            knowledge_writeback=self.collect_knowledge(results),
            skill_candidates=self.collect_skill_candidates(results),
            next_steps=self.suggest_next_steps(task, results)
        )
```

### 2.9 Action Memory（行动记忆）

**职责**：记录每次任务和每个步骤的完整执行过程。

### 2.10 Skill Library（Skill 库）

**职责**：管理已验证的 Skill——版本、晋升、退役。

### 2.11 Evolution Loop（进化循环）

**职责**：从行动记忆中提取改进机会，自动推进 Skill 升级和工具替换。

---

## 三、运行时数据流

一次完整任务的数据流：

```
1. 用户输入（自然语言）
   ↓
2. Task Gateway → Task Contract（YAML/JSON）
   ↓
3. Dynamic Task Planner → Task DAG（步骤 + 依赖 + 能力需求）
   ↓
4. Stage-Aware Router → 每个步骤 assigned Tool + Agent
   ↓
5. Safety Enforcer → 检查风险 → 改道或放行
   ↓
6. Capability Fabric.execute() / Agent.dispatch()
   │
   ├── 工具可用 → 执行 → 返回结果
   │
   └── 工具不可用 → Ability Gap Detector
                     → Toolsmith-Lite（搜索→试用→封装）
                     → 注册到 Capability Fabric
                     → 重新执行
   ↓
7. Outcome Package Builder → Outcome Package
   ↓
8. Action Memory ← 完整任务记录
   Skill Library ← 新 Skill 候选
   Evolution Loop ← 改进信号
   ↓
9. 成果交付给用户 + 沉淀到 Omega Vault
```

---

## 四、技术选型建议

> ⚠️ **MFE 构建注意**：本节为早期设计探索的技术选型建议。实际 MFE 构建以
> `build-package/AGENTS.md` §1.1 强制技术选型为准。关键差异：
> - AGENTS.md 使用 **Click + Rich**（非 Typer）
> - AGENTS.md 使用 **自定义轻量 orchestrator**（非 LangGraph）
> - AGENTS.md **强制 PostgreSQL + Qdrant**（非 SQLite/可选）
> - 阶段 2+ 可重新评估本节建议。

| 层 | 推荐技术 | 备选 | 说明 |
|---|---------|------|------|
| **任务编排** | LangGraph | OpenAI Agents SDK, Prefect | LangGraph 支持 durable execution——失败/重启后从断点继续 |
| **主执行引擎** | Claude Code CLI | Codex CLI, 自建 Agent | Claude Code 当前最成熟，通过 CLI 调用 |
| **工具协议** | MCP (Model Context Protocol) | REST API, gRPC | MCP 是连接 AI 到外部工具的开放标准 |
| **浏览器自动化** | Playwright | Puppeteer, Selenium | Playwright 最成熟、跨浏览器 |
| **沙箱** | Docker | Firecracker, gVisor | Docker 最通用、生态最完善 |
| **向量搜索** | Qdrant | Chroma, Weaviate | Qdrant 性能好、Rust 实现、本地部署友好 |
| **关系数据库** | PostgreSQL | SQLite (MFE阶段) | SQLite 零配置适合 MFE，PostgreSQL 适合阶段 2+ |
| **消息队列** | Redis/NATS (阶段 3+) | PostgreSQL LISTEN/NOTIFY | 先不引入额外依赖 |
| **Web 框架** | FastAPI (Python) | Litestar, Flask | 轻量、异步、自动生成 OpenAPI 文档 |
| **CLI 框架** | Typer (Python) | Click, argparse | 基于类型注解，自动生成帮助 |
| **桌面应用** | Tauri v2 (阶段 3) | Electron | Rust 后端 + Web 前端，体积小 |

---

## 五、MFE 阶段的最小运行时

> ⚠️ **本节为早期设计草图**。实际 MFE 构建目录结构和文件清单以
> `Omega 构建指导书 — 给 Codex 的系统构造规范.md` §2 为准。

在 MFE 阶段（第一阶段），运行时以轻量形态存在：

```
omega-runtime/（MFE 最小版）
├── omega.yaml                   ← 系统配置
├── cli.py                       ← omega 命令入口
├── routers/
│   └── routing_table.yaml       ← 静态路由表
├── agents/
│   └── agent_definitions.yaml   ← Agent 静态定义
├── tools/
│   └── tool_registry.yaml       ← 工具注册表
├── schemas/
│   ├── task_contract.yaml       ← 任务契约 schema
│   └── outcome_package.yaml     ← 成果包 schema
├── scripts/
│   ├── run_task.py              ← 执行单任务的脚本
│   └── radar_scan.py            ← 工具雷达扫描
└── tests/
    └── benchmark_garden/        ← 基准任务
```

**MFE 阶段不需要**：
- PostgreSQL（用 SQLite 或 JSON 文件）
- Qdrant（用 Obsidian 全文搜索）
- Web UI（用 CLI + Obsidian 界面）
- Daemon（手动触发任务）
- 完整的 Agent SDK（Claude Code 已提供 Agent 能力）

---

## 六、与 Obsidian Vault 的交互

运行时通过以下方式与知识本体交互：

```python
# 读取 Vault
obsidian_adapter.read_page("omega生态系统项目/02-架构/Tool-Agent Router.md")
obsidian_adapter.search("SGLT2抑制剂")

# 写入 Vault
obsidian_adapter.create_page("wiki/来源/新文献.md", content, frontmatter)
obsidian_adapter.update_page("wiki/index.md", new_stats)

# 触发 ingest
obsidian_adapter.trigger_skill("ingest", file_path="raw/01-articles/新文件.pdf")
```

**约束**：
- 运行时只能写入 `wiki/` 和 `omega-workspace/`
- 运行时只能读取 `raw/`、`wiki/`、`omega生态系统项目/`
- 运行时不能修改 `CLAUDE.md` 或 `.obsidian/` 配置
- 运行时不能删除 `raw/` 中的文件（只能移动到 `09-archive/`）

---

## 七、相关页面

- [[Omega运行形态与本体文件说明]] — Omega 的三层形态和部署演进
- [[Dynamic Task Planner：动态任务规划器]] — 任务分解引擎
- [[Stage-Aware Tool-Agent Router]] — 阶段感知的工具/Agent 路由器
- [[omega.yaml]] — 系统本体配置总表
- [[Omega Manifest Schema]] — omega.yaml 的 schema 文档
- [[Omega生态系统项目-功能优先总方法论]] — 完整方法论
