---
type: concept
tags: [omega-ecosystem, merge-plan, agent-company, architecture, v3.2]
created: 2026-05-21
updated: 2026-05-21
knowledge_stability: evolving
parent: [[omega生态系统项目-总说明]]
related:
  - "[[Omega 最终完整方法论]]"
  - "[[Omega 构建指导书 — 给 Codex 的系统构造规范]]"
  - "[[洞察/AI Agent 公司架构方案]]"
---

# Omega ↔ AI Agent 公司 合并方案 v3.2

> **核心结论**：Omega 是 Agent OS Layer（基础设施），AI Agent 公司是在其上运行的 Agent Society 默认配置。
> 两者不矛盾——应该统一为 Omega 的「Agent Society v2 配置」+「三平面治理」+「五层记忆」。

---

## 一、关系定位

```
Omega (Agent OS Layer)                       AI Agent 公司 v2.0
══════════════════════                      ══════════════════
基础设施层                                  一种团队配置
├── Ω行动中枢 (命令→任务契约)               ├── Manager-Worker 模型
├── Dynamic Task Planner                    ├── 五层记忆体系
├── Tool-Agent Router                       ├── 三平面架构
├── 11 个运行时 Agent                       ├── 评测驱动开发
├── 6 份冻结共享合同                        ├── 医学生专项
├── 四级接口栈                              └── 中国法规合规
├── SessionGrant/SecretLease
├── 双沙箱隔离
└── 本地优先降级协议

关  系：Omega 是操作系统，Agent 公司是操作系统上运行的一个"桌面环境"
合  并：Agent 公司中 Omega 没有的部分 → 注入 Omega；重复的部分 → Omega 保留
```

## 二、逐项差异分析

### 2.1 Omega 已有的（Agent 公司无需重复）

| Agent 公司概念 | Omega 等价物 | Omega 更优之处 |
|:---|:---|:---|
| Manager Worker | `orchestrator` 运行时 Agent | Omega 已有完整 TaskContract + 状态机 |
| 任务分解 | `Dynamic Task Planner`（7 步规划 + DAG） | Agent 公司只有概念描述 |
| 工具路由 | `Stage-Aware Tool-Agent Router`（12 维评分） | Agent 公司只有四模式描述 |
| 权限审批 | `SessionGrant` + `SecretLease` + `risk_policy.yaml` | 6 种 Lease 失败码 + 8 种 Grant 状态转移 |
| 任务恢复 | `ContinuationPackage` + 5 种 ResumePrecondition | Agent 公司无此设计 |
| 结果验证 | `VerifierPlugin` 接口 + `FileExists/Assertion/DiffCheck` | Agent 公司只有概念 |
| 工具隔离 | Toolsmith 三步验收 + 双 Docker 沙箱 | Agent 公司无此设计 |
| 知识防污染 | KB Anti-Pollution Protocol（6 项自动检查） | Agent 公司只有"人工确认" |
| 安全沙箱 | Codex Seatbelt + Docker 双沙箱 | Agent 公司只有概念描述 |
| 溯源与审计 | `FlightRecorder` + `ProvenanceWatermark`（6 类链接） | Agent 公司只有四类日志概念 |
| 本地降级 | Local-First Fallback Protocol（4 级降级链） | Agent 公司无此设计 |

### 2.2 Agent 公司有、Omega 缺少的（需要注入）

| Agent 公司概念 | Omega 现状 | 注入方式 | 优先级 |
|:---|:---|:---|:---:|
| **三平面架构**（控制/数据/治理分离） | 混合在一起——Runtime Architecture 没有明确分层 | 作为组织原则，重组 Omega Runtime Architecture 的 11 组件为三平面 | 🔴 高 |
| **五层记忆体系**（L0-L4） | 有 Action Memory + Postgres + Qdrant，但没有明确分层和生命周期策略 | 新增 `05-知识库与记忆/五层记忆体系.md`，定义每层的存储后端、生命周期、写入策略 | 🔴 高 |
| **Manager-Worker 默认拓扑** | 11 个 Agent 扁平排列，`agent_role_mapping.yaml` 已有概念映射但缺少层级 | 更新 `config/agents.yaml`，新增 `topology: manager_worker` 配置段 | 🟡 中 |
| **评测流水线**（四层基线实验） | 有 `Tool Benchmark Cards` 和 `BENCHMARK_CATALOG.yaml`，但缺少系统化评测流水线 | 新增 `09-功能基准任务花园/评测流水线与四层基线.md` | 🟡 中 |
| **中国法规合规**（2026 实施意见） | 方法论有安全红线但未对齐具体法规 | 在方法论第九部分新增 §9.x 中国法规合规对齐 | 🟡 中 |
| **医学生专项配置** | 有 `06-医学强化域/` 目录（目前为空）+ `medical_evidence_agent` | 填充 `06-医学强化域/`：医学生 Agent Society 预设、PubMed/证据等级/PRISMA 工具链 | 🟡 中 |
| **记忆写入决策树** | 有 KB Anti-Pollution Protocol 但针对 wiki/ 写入，不针对记忆层 | 在五层记忆体系中加入写入决策树 | 🟢 低 |
| **医学知识特殊约束**（来源追溯、证据等级、时效性、冲突检测、PII 零写入） | Omega 有 provenance 水印但没有医学专项约束 | 在医学生专项配置中加入约束定义 | 🟡 中 |

---

## 三、具体注入内容

### 注入 1：三平面架构（重组 Runtime Architecture）

**位置**：更新 `08-运行时与原型/Omega Runtime Architecture.md`

**当前问题**：Omega Runtime Architecture 的 11 组件图是扁平的——Task Gateway → Planner → Router → Safety Enforcer → Capability Fabric → Agent Society → Toolsmith → Outcome Package → Action Memory → Skill Library → Evolution Loop。控制、数据、治理混在一起。

**注入后结构**：

```
┌──────────────────────────────────────────────────────────────┐
│                  CONTROL PLANE（控制平面）                     │
│  谁可以做什么、派谁做、做到哪了、失败了怎么恢复                  │
│                                                              │
│  Task Gateway → Dynamic Task Planner → Stage-Aware Router    │
│  → Safety Enforcer → ContinuationPackage (恢复)              │
│  → SessionGrant/SecretLease (授权)                            │
│  → ResourceLock (资源锁)                                      │
└──────────────────────────────────────────────────────────────┘
                           │
                           ▼
┌──────────────────────────────────────────────────────────────┐
│                  DATA PLANE（数据平面）                        │
│  实际干活的人、工具、记忆、知识                                 │
│                                                              │
│  Capability Fabric → Agent Society (Manager-Worker 拓扑)      │
│  → Toolsmith Lite → Outcome Package                          │
│  → Action Memory (L1 情节)                                    │
│  → 五层记忆后端 (Postgres + Qdrant + Neo4j)                   │
│  → External AI Tool Gateway (Claude Code / Codex / Hermes)   │
└──────────────────────────────────────────────────────────────┘
                           │
                           ▼
┌──────────────────────────────────────────────────────────────┐
│                GOVERNANCE PLANE（治理平面）                    │
│  做过什么、对不对、怎么改进                                     │
│                                                              │
│  FlightRecorder (全链路追踪) + ProvenanceWatermark (溯源)     │
│  → VerifierPlugin (结果验证)                                   │
│  → 评测流水线 (四层基线)                                       │
│  → Skill Library → Evolution Loop                             │
│  → L4 合规日志 (Postgres 审计分区，只追加不可删改)              │
│  → Red Team 安全回归                                          │
└──────────────────────────────────────────────────────────────┘
```

### 注入 2：五层记忆体系

**位置**：新建 `05-知识库与记忆/五层记忆体系.md`

Omega 目前有：Action Memory（Postgres）、向量索引（Qdrant）、知识库（Obsidian wiki/）、溯源水印。但缺少明确的分层和每层的生命周期策略。

**注入内容**：

| 层级 | 名称 | Omega 对应组件 | 存储后端 | 生命周期 | 写入策略 |
|:----:|------|:------------|---------|---------|---------|
| **L0** | 会话记忆 | Task Contract 的当前执行状态 | LangGraph State / 内存 | 单会话 | 自动 |
| **L1** | 情节记忆 | Action Memory 的历史任务记录 | Postgres + 时间戳 + TTL 衰减 | 永久（自动衰减） | 自动摘要（结构化模板，禁止自由反思文本） |
| **L2** | 语义记忆 | wiki/实体/ + wiki/概念/ + PubMed 提取的事实 | Qdrant 向量 + Neo4j 知识图谱 | 永久（带版本号+来源追溯） | **人工确认后写入**（默认不自动写） |
| **L3** | 程序记忆 | Skill Library + `.claude/skills/` | 文件系统 + Git 版本控制 | 永久（有回滚按钮） | **人工审核后合并**（默认不自动生成） |
| **L4** | 合规日志 | FlightRecorder + 审批日志 + 评测日志 | Postgres 审计分区 | 永久（冷热分层） | 系统自动（不可篡改） |

**关键新增**：
- L1 的 TTL 衰减机制：旧记录自动降权
- L2 的医学知识约束：每条事实必须带 `source_doi`/`source_pmid` + 证据等级
- L2/L3 的写入审批：必须人工确认，防止错误知识固化
- L4 的不可篡改性：只追加、不修改、不删除

### 注入 3：Manager-Worker 作为默认 Agent Society 拓扑

**位置**：更新 `config/agents.yaml` + `config/agent_role_mapping.yaml`

**当前状态**：agents.yaml 有 11 个运行时 Agent，但它们是扁平并列的。

**注入内容**：在 agents.yaml 中新增 `topology` 配置段：

```yaml
# config/agents.yaml — 新增 topology 段
topology:
  mode: manager_worker  # 默认拓扑模式
  manager:
    agent_id: orchestrator
    capabilities: [task_decomposition, worker_assignment, approval_decision, result_aggregation]
  workers:
    - agent_id: researcher
      domain: [literature_search, knowledge_ingestion, evidence_evaluation]
      engine: hermes  # 长期运行、记忆管理
    - agent_id: code_builder
      domain: [code_generation, data_analysis, bioinfo_pipeline]
      engine: codex  # 代码执行、沙箱安全
    - agent_id: writer
      domain: [academic_writing, content_creation, translation]
      engine: claude  # 语言质量优先
    - agent_id: critic
      domain: [fact_check, citation_validation, quality_review]
      engine: claude  # 推理严谨性
    - agent_id: knowledge_steward
      domain: [knowledge_curation, index_maintenance, lint_check]
      engine: hermes  # 持久记忆管理
    - agent_id: tool_smith
      domain: [tool_discovery, tool_registration, skill_creation]
      engine: hermes  # 工具学习闭环

  # Worker 间通信规则
  communication:
    cross_worker_direct: false  # Worker 间不直接通信
    all_via_manager: true       # 所有跨 Worker 信息通过 Manager 传递
    context_isolation: true     # Worker 上下文隔离（防提示注入传播）

  # 审批策略（按 Worker 权限等级）
  approval:
    risk_class_low: { default: none }
    risk_class_medium: { default: once_per_task }
    risk_class_high: { default: always }
    risk_class_critical: { default: always, require_human: true }
```

### 注入 4：评测流水线

**位置**：新建 `09-功能基准任务花园/评测流水线与四层基线.md`

Omega 已有 `BENCHMARK_CATALOG.yaml`（13+ 闭环）和 `Tool Benchmark Cards`，但缺少：

1. **四层基线实验设计**（单 Agent 基线 → +RAG → +多 Worker → +评测循环）
2. **自动化评测评分器**（LLM-as-judge rubric）
3. **评测指标 Dashboard**（成功率/成本/幻觉率/审批率）
4. **红队测试集**（提示注入/越权/引用幻觉/PHI 泄露）

### 注入 5：中国法规合规

**位置**：更新 `01-方法论/Omega 最终完整方法论.md` 第九部分 §9.x

Omega 方法论已有安全红线，但需要显式对齐 2026 年《智能体规范应用与创新发展实施意见》的 10 项要求：

| 实施意见要求 | Omega 现有能力 | 需补充 |
|:---|:---|:---|
| 决策权限边界 | SessionGrant + 4 级自主等级 ✅ | — |
| 用户知情权与最终决策权 | 审批点 + 人类接管 ✅ | — |
| 执行不超出授权范围 | risk_policy.yaml + Safety Enforcer ✅ | — |
| 数字身份 | Agent ID + 角色注册表 ✅ | — |
| 能力声明 | agent_card.schema.json ✅ | — |
| 分类分级治理 | risk_class 四级 ✅ | — |
| 供应链安全 | Toolsmith 三步验收 + Quarantine ✅ | 需增加 MCP Server 签名验证 |
| 异常行为检测 | 断路器（3 次失败 → Blocked）✅ | — |
| 行为可追溯 | FlightRecorder + ProvenanceWatermark ✅ | 需确保 L4 日志不可篡改 |
| 安全评估 | ❌ 缺失 | 需增加 Red Team 安全回归集 |

### 注入 6：医学生专项配置

**位置**：填充 `06-医学强化域/` 目录

```
06-医学强化域/
├── README.md                          ← 医学生场景导航
├── 医学生Agent Society预设.md          ← Manager-Worker 的医学配置
├── PubMed工具链.md                    ← PubMed API + E-utilities + 检索策略
├── 证据等级自动判定.md                 ← GRADE/RoB 2/NOS 规则引擎
├── PRISMA流程图生成.md                ← 文献筛选 PRISMA 2009/2020
├── 医学知识约束协议.md                 ← 来源追溯/时效性/冲突检测/PII零写入
├── 医学生评测数据集设计.md             ← 4 类测试场景（检索/提取/引用/冲突）
└── 临床学习辅助.md                     ← 病例分析/鉴别诊断辅助（仅供学习参考）
```

---

## 四、文件变更清单

### 需新建的文件

| 文件 | 内容 | 优先级 |
|------|------|:------:|
| `05-知识库与记忆/五层记忆体系.md` | L0-L4 定义、后端、策略、写入决策树 | 🔴 |
| `09-功能基准任务花园/评测流水线与四层基线.md` | 四层实验设计、自动评分、指标看板 | 🟡 |
| `06-医学强化域/README.md` | 医学生场景导航 | 🟡 |
| `06-医学强化域/医学生Agent Society预设.md` | 医学 Manager-Worker 配置 | 🟡 |
| `06-医学强化域/PubMed工具链.md` | PubMed API 封装规范 | 🟢 |
| `06-医学强化域/医学知识约束协议.md` | 来源追溯/证据等级/时效/冲突/PII | 🟡 |

### 需更新的文件

| 文件 | 变更内容 | 优先级 |
|------|---------|:------:|
| `08-运行时与原型/Omega Runtime Architecture.md` | 重组 11 组件为三平面架构 | 🔴 |
| `01-方法论/Omega 最终完整方法论.md` | 第九部分新增 §9.x 中国法规合规对齐 | 🟡 |
| `99-交付给Codex的构建包/config/agents.yaml` | 新增 `topology` 配置段（Manager-Worker） | 🟡 |
| `99-交付给Codex的构建包/config/agent_role_mapping.yaml` | 新增 Manager-Worker 拓扑映射 | 🟡 |
| `99-交付给Codex的构建包/AGENTS.md` | 新增三平面架构引用、五层记忆协议 | 🟡 |

### 需更新的 wiki 页面

| 文件 | 变更内容 |
|------|---------|
| [[洞察/AI Agent 公司架构方案]] | 顶部新增醒目说明：本方案已合并入 Omega v3.2；此处保留为设计历史参考 |

---

## 五、合并后 Omega 的完整图景

```
┌──────────────────────────────────────────────────────────────┐
│                    Omega v3.2 — 完整架构                       │
│                                                              │
│  用户："Omega，帮我综述 TyG 指数与 CVD 的因果证据"             │
│                                                              │
│  ═══════════════ CONTROL PLANE ═══════════════════════════   │
│  Ω行动中枢 → TaskContract → Dynamic Task Planner             │
│  → Stage-Aware Tool-Agent Router → Safety Enforcer            │
│  → SessionGrant (授权) + ResourceLock (资源锁)                │
│  → ContinuationPackage (失败恢复)                              │
│                                                              │
│  ═══════════════ DATA PLANE ══════════════════════════════   │
│  Manager Worker (orchestrator) — Claude Code 驱动             │
│    ├── Research Worker (researcher + medical_evidence)        │
│    │   → Hermes Agent → PubMed API → PDF 解析                 │
│    ├── Code Worker (code_builder)                             │
│    │   → Codex CLI 沙箱 → Python/R 分析 → 森林图              │
│    └── Review Worker (critic)                                 │
│        → Claude Code → 事实核查 → 引用验证 → GRADE 评级       │
│                                                              │
│  ═══════════════ GOVERNANCE PLANE ════════════════════════   │
│  FlightRecorder (全链路追踪)                                   │
│  → VerifierPlugin (证据三件套验证)                              │
│  → 评测流水线 (单Agent基线 → +RAG → +Workers → +评测循环)     │
│  → L4 合规日志 (不可篡改审计分区)                               │
│  → Evolution Loop (Skill 沉淀 → 回滚 → 灰度发布)              │
│                                                              │
│  ═══════════════ MEMORY (五层) ═══════════════════════════   │
│  L0 会话 → L1 情节(Postgres) → L2 语义(Qdrant+Neo4j)         │
│  → L3 程序(Skills+Git) → L4 合规(审计分区)                    │
└──────────────────────────────────────────────────────────────┘
```

---

## 六、执行优先级

| 优先级 | 任务 | 工作量 | 对 Codex 构建的影响 |
|:---:|------|:---:|:---|
| **1** | 创建 `五层记忆体系.md` | 1h | 影响 Memory 模块的数据库 schema 设计 |
| **2** | 重组 Runtime Architecture 为三平面 | 30min | 影响模块划分——控制/数据/治理三层目录结构 |
| **3** | 更新 `AGENTS.md` 新增三平面和五层记忆引用 | 15min | 新增构建前必读文件 |
| **4** | 创建医学强化域 4 个核心文件 | 2h | 新增 `src/medical/` 模块 |
| **5** | 更新 `agents.yaml` 新增 topology 段 | 30min | 影响 AgentSociety 的初始化代码 |
| **6** | 创建评测流水线文档 | 1h | 新增 `src/governance/evaluator.py` |
| **7** | 更新方法论合规章节 | 30min | 影响 Safety Enforcer 的策略规则 |
| **8** | 更新 Agent 公司 wiki 页（标注已被 Omega 吸收） | 5min | 无代码影响 |

**总计约 6 小时文档工作 + Codex 按新规范调整代码。**

---

*合并方案版本 v1.0 — 2026-05-21*
*基于 Omega v3.1 完整方法论 + AI Agent 公司 v2.0 架构方案对比分析*
