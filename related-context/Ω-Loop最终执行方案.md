---
type: insight
tags: [Ω-Loop, 架构设计, 执行方案, 最高优先级, 最终版]
created: 2026-06-16
updated: 2026-06-16
knowledge_stability: evolving
cqs: 5.0
cqs_dimensions:
  density: 5
  reuse: 5
  attribution: 5
  uniqueness: 5
  structure: 5
sources:
  - wiki/洞察/知识库发展历程.md
  - wiki/洞察/Ω-Loop生态系统架构.md
  - D:\Omega-System\PROJECT.md
  - D:\Omega-System\AGENTS.md
  - arXiv 2604.15034v4 (Autogenesis Protocol, Zhang et al. NTU/Stanford/Princeton, 2026-05-19 — SEPL 五算子: Reflect·Select·Improve·Evaluate·Commit, §E.3.2-§E.3.3)
  - arXiv 2603.28986 (Mimosa Framework)
  - docs.anthropic.com Clode Code Hooks
---

# Ω-Loop 最终执行方案 v1.0

> **「你不记得的，我来记住。你记不住的，我来执行。」**
>
> 取 Omega v2 之骨架（事件驱动·合约制·闭环进化），
> 取 Autogenesis 之协议（RSPL 资源注册·SEPL Reflect→Select→Improve→Evaluate→Commit 五算子闭环[arXiv:2604.15034]），
> 取 Mimosa 之编排（MCP 动态发现·元编排器·LLM Judge 评分），
> 取 Claude Code 之钩子（PreToolUse·UserPromptSubmit·Stop·SessionStart·PostToolUse），
> 长在知识库的土壤上（33 规则·764 Skills·54 触发点·14 维进化·三层 AI·多 Agent）。

---

## 执行摘要（≤500 字 — CEO 可读）

2026-06-16 的 SBB 感官脑体三元衰老课题 v4.0 暴露了知识库工作流系统的根本性缺陷：**26 项基建升级在真实会话中零使用**。所有强制门、Agent 管道、格式验证、搜索路由——全部被绕过。根因不是某个脚本坏了，是**架构范式错误**：系统依赖 Claude 在"执行模式"下"记得"做合规检查——而执行模式的定义就是认知负荷最高、最不可能记得的时候。

**解决方案**：将合规检查从"需要 Claude 记忆的文本自检"升级为"操作系统层运行的钩子脚本"。同时将 Omega v2 的 12 项架构模式（事件存储、合约验证、回滚恢复、能力发现等）移植到知识库已有基础设施上。

**分 6 个 Phase 执行，共 35 项任务，预估 ~350K tokens**：
- Phase 0：规则冲突统一（5 项，清理地基）
- Phase Ω-1：钩子层部署（7 项，H-1~H-7，核心交付物）
- Phase Ω-2：总线层建设（5 项，Event Store + 信号文件 + MessageBus）
- Phase Ω-3：编排层升级（6 项，元编排器 + LLM Judge + RSPL）
- Phase Ω-4：自进化层闭环（7 项，SEPL 五算子 + CAR 仪表盘 + 自动回滚）
- Phase Ω-5：文档与验证（5 项，Skill导航 + CLAUDE.md + 端到端测试）

**预期效果**：Skill 激活率 0%→≥30%，Agent spawn 率 8%→≥50%，合规拦截率 不存在→≥95%，Event Store 完整性 不存在→100%。

---

## 一、现状诊断

### 1.1 SBB 课题 v4.0 失效模式全景

2026-06-16 的 SBB 感官脑体三元衰老课题 v4.0 会话（~120K tokens）中，以下全部基建**零使用**：

```
零 Agent spawn          →  Agent 配额从未触发（SBB 从未调 /ingest）
零 format_gate 调用      →  Write/Edit 操作未经 pre-write 验证
零 kb_health 触发         →  健康检查从未运行
零 kb-engine 使用         →  Go 引擎从未被调用
零 MessageBus 使用        →  组件间通信全部走 Claude 文本
零 Skill 工具调用          →  749 Skills 在全程手动执行中完全静默
零 unified_search.py 路由  →  外部搜索直接 curl/Bing（违反触发点 #36）
```

### 1.2 根因分析（EISR 分类）

| 失效模式 | 根因 | EISR | 影响 |
|---------|------|:--:|------|
| 所有强制门仅嵌入 SKILL.md 管道 | `/ingest`/`/evolve`/`/lint` 之外的路径零门控 | `MISSING` | 🔴 致命 |
| Agent 配额由管道步骤 8.8 触发 | 非 /ingest 会话从不触发 Agent 派遣判定 | `WRONG` | 🔴 致命 |
| "文件存在"验证标准无法检测调用 | `format_gate.py` 存在 ≠ 被调用了 | `WRONG` | 🔴 致命 |
| 长任务认知负荷挤出合规自检 | Claude 在"执行模式"下系统性遗忘 | `MISSING` | 🔴 致命 |
| 外部搜索无强制执行路由 | 直接 curl 不经过 search_router.py | `MISSING` | 🔴 致命 |
| Skill 注册但从不推荐 | 无每次对话注入的发现机制 | `MISSING` | 🔴 致命 |

### 1.3 已有规则冲突清单（Phase 0 修复）

| # | 冲突 | 文件 A | 文件 B | 解决 |
|:--:|------|------|------|------|
| **C1** | dispatch 实效性双重定义 | agent-dispatch G.4.5 | agent-automation F.4 | G.4.5 为唯一定义 |
| **C2** | 外部安全门控不一致 | compliance #17 | external-project-workflow F.1/F.2 | 统一到 external-project-workflow |
| **C3** | 验证格式重复 | compliance #21 | verification-gate v2.0 | 已解决，确认无残留 |
| **C4** | 搜索入口冲突 | compliance #36 | tool-fallback-matrix Part 0 v3.0 | 已解决，确认无旧引用 |
| **C5** | 冷却双重定义 | self-evolution D.2 | compliance #30 | compliance #30 为强制执行标准 |

### 1.4 基础设施缺口

| 缺口 | 当前状态 | Omega v2 对应 | 修复 Phase |
|------|:--:|------|:--:|
| Event Store | 不存在（仅 log.md 文本） | JsonlEventStore | Ω-2 |
| 元编排器 | skill-orchestration 11 静态模板 | TeamOrchestrator | Ω-3 |
| 资源版本化 (RSPL) | 注册表无 version/changelog | contracts/ 类型定义 | Ω-4 |
| SEPL 闭环 | /evolve 步骤未形式化 | propose→assess→commit 映射 | Ω-4 |
| 钩子层 | 未部署 | MutatingWriteGuard | Ω-1 |
| CAR 仪表盘 | 仅概念（D17 维度） | KPI aggregation | Ω-4 |

---

## 二、架构总览

### 2.1 五层生态系统

```
┌──────────────────────────────────────────────────────────────────┐
│               Layer 4: 自进化层 (Immune + Endocrine)               │
│  SEPL 五算子(arXiv:2604.15034): Reflect→Select→Improve→Evaluate→Commit │
│  + Rollback(Commit 内置安全阀) + 映射到 /evolve 管道                     │
│  RSPL 资源版本化 + CAR 能力激活率仪表盘 + 自动回滚 + 回归快照       │
├──────────────────────────────────────────────────────────────────┤
│               Layer 3: 编排层 (Brain)                              │
│  元编排器: 意图分解→RSPL匹配→DAG生成→LLM Judge评分→精炼            │
│  Agent 调度: Writer/Critic/Researcher + 事件驱动 spawn             │
├──────────────────────────────────────────────────────────────────┤
│               Layer 2: 总线层 (Circulatory)                        │
│  Event Store (JSONL) + Signal Files + MessageBus                  │
│  统一事件: tool.use | hook.block | agent.spawn | evolve.apply     │
├──────────────────────────────────────────────────────────────────┤
│               Layer 1: 钩子层 (Nervous)  ← Phase Ω-1               │
│  UserPromptSubmit → Skill 路由（每次对话注入推荐）                   │
│  PreToolUse ×3  → Write 合规 / Bash 路由 / Read 预检                │
│  Stop           → Agent 配额 + 完成前验证                           │
│  PostToolUse    → Event Store 审计                                  │
│  SessionStart   → 健康检查 + Ω-Loop 状态摘要                        │
├──────────────────────────────────────────────────────────────────┤
│               Layer 0: 资源层 (Skeleton)                           │
│  Rules (33) · Skills (764) · Scripts · MCPs (4) · Agents (3)      │
│  Wiki · NotebookLM · Zotero · GraphRAG · ChromaDB                 │
│  所有资源通过 RSPL 注册为版本化、可发现接口                         │
└──────────────────────────────────────────────────────────────────┘
```

### 2.2 Omega v2 模式移植对照

| Omega v2 理念                    | Omega v2 实现                       | Ω-Loop 实现                            |    状态    |
| ------------------------------ | --------------------------------- | ------------------------------------ | :------: |
| Events as audit root           | JsonlEventStore                   | `.claude/cache/event-store.jsonl`    | 🔜 Ω-2.1 |
| Mutating write guard           | SessionGrant + MutatingWriteGuard | PreToolUse 钩子 + format_gate.py       |  🔜 Ω-1  |
| Verification before completion | P0 verifier plugins               | Stop 钩子 + format_gate.py enforce     |  🔜 Ω-1  |
| Contracts as canonical source  | packages/contracts/*.ts           | `.claude/rules/*.md` (33 文件)         |   ✅ 已有   |
| Skill promotion with replay    | packages/compiler + shadow replay | evolution_canary post-deploy         |   ✅ 已有   |
| Bounded autonomy               | packages/governance budget        | compliance density tracking          |  ⚠️ 部分   |
| Capability discovery           | packages/services router          | skill-registry + UserPromptSubmit 钩子 |  🔜 Ω-1  |
| Scheduler for evolution        | packages/scheduler ticks          | Cron watchdog                        |  ⚠️ 部分   |
| Dynamic team orchestration     | packages/orchestration            | skill-orchestration + Agent dispatch |  ⚠️ 部分   |
| Interface degradation chain    | ToolAgentRouter.selectPath()      | tool-fallback-matrix 四层降级            |   ✅ 已有   |
| Secret isolation               | packages/secrets lease resolvers  | `.env` + CLAUDE_ENV_FILE             |   ✅ 已有   |
| Rollback with compensation     | RollbackExecutor.compensateAll()  | evolution_canary revert + .bak       |   ✅ 已有   |
| P0 small enough to verify      | fixtures + P0 scenarios           | format_gate.py 系列                    |   ✅ 已有   |
| Shadow replay farm             | ShadowReplayFarm.run()            | 未来（Ω-5+）                             |  ❌ 未移植   |
| Continuation package           | RecoveryService.evaluateResume()  | 未来（Ω-5+）                             |  ❌ 未移植   |

**移植率: 11/15 (73%)**。

---

## 三、普适执行协议 (Universal Execution Protocol)

UEP 是所有用户操作的单一执行路径——无论走 `/ingest`、`/evolve`、直接对话、还是"自主执行"。

```
用户说任何话
      │
      ▼
┌──────────────────────────────────────────────┐
│ UEP Step 0: 意图解析 (SessionStart + 每次对话) │
│                                              │
│  SessionStart 钩子:                            │
│    → kb_registry.py --summary (能力注册表)       │
│    → kb_activate.py --mode session-start        │
│    → 检查钩子健康 (5 个钩子脚本是否存在+可执行)    │
│    → 检查信号文件残留 (pending-*.json)           │
│    → 注入 Ω-Loop 状态摘要到会话上下文             │
│                                              │
│  UserPromptSubmit 钩子 (每次用户说话):           │
│    → skill_router.py 语义匹配                    │
│    → 注入 Top 5 Skill 推荐                      │
│    → 注入编排模板建议 (若匹配场景)                │
└──────────────────────────────────────────────┘
      │
      ▼
┌──────────────────────────────────────────────┐
│ UEP Step 1: 行动决议                           │
│                                              │
│  Claude 决定: 直接执行 / Skill / Agent / Workflow│
│    → 若复杂度 > 阈值 → 自动建议 Agent            │
│    → 若匹配编排模板 → 自动建议管道                │
│    → 若外部搜索需求 → 强制路由 unified_search.py  │
└──────────────────────────────────────────────┘
      │
      ▼
┌──────────────────────────────────────────────┐
│ UEP Step 2: 执行 + 门控 (PreToolUse 钩子)       │
│                                              │
│  每次 Write/Edit → compliance_pre_write.sh    │
│    → format_gate.py pre-write → ✅/🔴          │
│  每次 Bash(curl/wget) → compliance_bash_guard  │
│    → search_router 标记检查 → ✅/🔴             │
│  每次 Read(.csv/.json/.py) → compliance_pre_read│
│    → format_gate.py pre-read → ✅/🔴            │
│  每 ≥8 次工具调用 → 中继检查 (anti-self-loop)    │
│  (全部操作系统层运行, Claude 零记忆负担)         │
└──────────────────────────────────────────────┘
      │
      ▼
┌──────────────────────────────────────────────┐
│ UEP Step 3: 完成验证 (Stop 钩子)               │
│                                              │
│  Stop 钩子触发:                                │
│    → Agent 配额检查 (≥50K tokens + 零 spawn?)   │
│    → format_gate.py enforce --gate all        │
│    → 信号文件残留检查 (pending-*.json)          │
│    → 未通过 → "ok": false → Claude 继续工作     │
│    → 通过 → 放行                               │
└──────────────────────────────────────────────┘
      │
      ▼
┌──────────────────────────────────────────────┐
│ UEP Step 4: 事件归档 (PostToolUse 钩子)        │
│                                              │
│  PostToolUse 钩子 (每次 Write/Edit 成功后):     │
│    → event-store.jsonl 追加 tool.use 事件      │
│    → 更新 compliance 密度追踪                   │
│  会话结束:                                     │
│    → event-store.jsonl 追加 session.complete   │
│    → Watchdog 异步扫描 → 密度审计                │
│    → CAR 追踪器更新 (car_tracker.py)            │
└──────────────────────────────────────────────┘
```

**UEP 的关键承诺**：
1. **零认知负荷**：五个钩子在操作系统层静默运行，Claude 不需要"记得"做检查
2. **全路径覆盖**：无论用户说 `/ingest`、`/evolve`、`帮我做X`、还是 `自主执行全部`——都走同一条 UEP
3. **失败安全**：钩子脚本失败（非零退出）→ 操作被阻止。不依赖 Claude "决定是否遵守"
4. **可审计**：每次 Write/Edit 的 pre-write 结果、每次 Bash 的路由检查——都在 event-store.jsonl 中有结构化记录

---

## 四、任务清单

### 总览

| Phase | 名称 | 任务数 | 预估 Token | 依赖 | 核心交付物 |
|:--:|------|:--:|:--:|------|------|
| **0** | 规则冲突统一 | 5 | ~14K | 无 | 消除 5 项已有冲突 |
| **Ω-1** | 钩子层部署 | 7 | ~68K | Phase 0 | 5 个钩子脚本 + settings.json + CLAUDE.md |
| **Ω-2** | 总线层建设 | 5 | ~35K | Phase Ω-1 | Event Store + PostToolUse + Watchdog |
| **Ω-3** | 编排层升级 | 6 | ~70K | Phase Ω-2 | 元编排器 + LLM Judge + RSPL API |
| **Ω-4** | 自进化层闭环 | 7 | ~65K | Phase Ω-3 | SEPL 形式化 + CAR 仪表盘 + 自动回滚 |
| **Ω-5** | 文档与验证 | 5 | ~34K | Phase Ω-4 | Skill导航 + 端到端测试 + Omega 对照表 |
| **合计** | **6 Phases** | **35** | **~286K** | | |

---

### Phase 0: 规则冲突统一（5 项 · 地基清理）

> 必须先清理地基——在已有冲突上建新系统会让冲突指数级扩散。

| # | 任务 | 窗口 | Token | 前置 | 验证 |
|:--:|------|:--:|:--:|------|------|
| **P0-1** | C1: agent-automation.md F.4 删除双重 dispatch 定义 → 改为引用 agent-dispatch.md G.4.5 | 1 | ~3K | — | Grep agent-automation.md 确认无独立 dispatch 实效性定义段落 |
| **P0-2** | C2: external-project-workflow.md F.1/F.2 声明为外部安全门控唯一来源。compliance #17 改为引用 | 1 | ~3K | — | Grep compliance #17 含"→ 统一门控见 external-project-workflow.md" |
| **P0-3** | C3: 确认 verification-gate.md v2.0 统一验证协议在所有引用点生效 | 1 | ~3K | — | 三个引用点均指向 verification-gate.md |
| **P0-4** | C4: 确认 tool-fallback-matrix.md Part 0 v3.0 unified_search.py 单入口规则在所有引用点生效 | 1 | ~3K | — | 三个引用点均指向 unified_search.py |
| **P0-5** | C5: self-evolution.md Part D 冷却章节追加「以 compliance-monitoring.md #30 的 format_gate.py evolve-cooling 返回码为强制执行标准」 | 1 | ~2K | — | self-evolution.md Part D 含此声明句 |

**Phase 0 DoD**: 5 项规则冲突均有明确引用链。`format_gate.py multi-file` 通过。

---

### Phase Ω-1: 钩子层部署（7 项 · 核心交付物）

> 整个 Ω-Loop 的神经系统。执行顺序：**先建脚本 → 再配 settings.json → 再更新 CLAUDE.md → 最后验证**。

#### Ω-1.1: UserPromptSubmit 钩子 — Skill 路由

| 维度 | 内容 |
|------|------|
| **文件** | `.claude/scripts/skill_router.py` + `.claude/hooks/skill_router.sh` |
| **功能** | 每次用户提交提示词时自动运行——语义匹配 skill-registry.json → 注入 Top 5 Skill 推荐 |
| **窗口** | 3 |
| **Token** | ~20K |
| **验证** | `echo '{"prompt":"帮我写一篇论文初稿"}' \| python .claude/scripts/skill_router.py` → 输出含 `academic-writing, compose, halluref-citation-check` |
| **约束** | 永不阻止（exit 0 always）。超时 25s（UserPromptSubmit 限制） |

#### Ω-1.2: Skill 导航文件（人类查阅）

| 维度 | 内容 |
|------|------|
| **文件** | `wiki/洞察/Skill导航.md` |
| **功能** | 按任务意图组织——7 大类：写作·图表与演示·数据分析与研究·知识管理·系统与工具·发布与分发·医学科研 |
| **窗口** | 1 |
| **Token** | ~8K |
| **验证** | 文件 ≥3KB + 含 ≥30 个 Skill 条目 + 每个条目含 Skill 名/一句话/触发方式 |

#### Ω-1.3: PreToolUse ×3 合规钩子

| # | 文件 | 拦截对象 | 门控脚本 | 阻止条件 | Token |
|:--:|------|------|------|------|:--:|
| **Ω-1.3a** | `.claude/hooks/compliance_pre_write.sh` | Write + Edit | `format_gate.py pre-write` | exit≠0 | ~5K |
| **Ω-1.3b** | `.claude/hooks/compliance_bash_guard.sh` | Bash(curl/wget/Invoke-WebRequest) | 检查 SEARCH_ROUTER_OK 标记文件 | 无标记或 >2min 过期 | ~5K |
| **Ω-1.3c** | `.claude/hooks/compliance_pre_read.sh` | Read(.csv/.json/.py/.R) | `format_gate.py pre-read` | exit 3 (≥30MB 硬阻断) | ~3K |

#### Ω-1.4: Stop 钩子 — Agent 配额 + 完成前验证

| 维度 | 内容 |
|------|------|
| **文件** | `.claude/hooks/agent_quota_stop.sh` |
| **功能** | 会话结束前检查：Agent 配额是否满足？信号文件是否残留？format_gate enforce 是否通过？ |
| **窗口** | 2 |
| **Token** | ~5K |
| **约束** | `stop_hook_active=true` 时自动放行（防止无限循环）。超时 10s |

#### Ω-1.5: 配置 settings.json 全部钩子

| 维度 | 内容 |
|------|------|
| **文件** | `.claude/settings.json` |
| **功能** | 注册全部 5 个钩子：UserPromptSubmit ×1, PreToolUse ×3, Stop ×1 |
| **窗口** | 1 |
| **Token** | ~8K |
| **验证** | 运行 `/hooks` 菜单 → 确认全部 5 个钩子已注册 |

#### Ω-1.6: PostToolUse 钩子 — 审计日志

| 维度 | 内容 |
|------|------|
| **文件** | `.claude/hooks/audit_post_tool.sh` |
| **功能** | 每次 Write/Edit 成功后追加 event-store.jsonl（`tool.use` 事件） |
| **窗口** | 1 |
| **Token** | ~3K |
| **约束** | 永不阻止（exit 0 always）。超时 5s |

#### Ω-1.7: SessionStart 钩子 — 健康检查 + 上下文注入

| 维度 | 内容 |
|------|------|
| **文件** | `.claude/hooks/session_start.sh` |
| **功能** | 每次会话启动时：检查 5 个钩子脚本是否存在+可执行 → 检查信号文件残留 → 注入 Ω-Loop 健康摘要 |
| **窗口** | 1 |
| **Token** | ~3K |

**Phase Ω-1 DoD**:
- [ ] `/hooks` 菜单显示 5 个钩子已注册
- [ ] 尝试直接 Write 文件 → 被 PreToolUse 钩子阻止
- [ ] 尝试 `curl` 外部 URL → 被 Bash guard 钩子阻止
- [ ] 创建 pending-dispatch.json → 尝试结束会话 → 被 Stop 钩子阻止
- [ ] 输入 "帮我写论文" → Claude 上下文被注入 Skill 推荐

---

### Phase Ω-2: 总线层建设（5 项 · 循环系统）

#### Ω-2.1: Event Store 核心 API

| 维度 | 内容 |
|------|------|
| **文件** | `.claude/scripts/event_store.py` |
| **功能** | `record_event(source, event, payload)` → 追加 JSONL 到 `.claude/cache/event-store.jsonl` |
| **Schema** | `{"timestamp":"ISO","source":"component","event":"type","payload":{},"session":"id"}` |
| **事件类型** | `tool.use`, `hook.block`, `agent.spawn`, `agent.complete`, `evolve.apply`, `compliance.violation`, `resource.discover`, `resource.deprecate`, `session.start`, `session.complete` |
| **窗口** | 2 | **Token** | ~12K |

#### Ω-2.2: PostToolUse → Event Store 集成

| 维度 | 内容 |
|------|------|
| **文件** | 修改 `.claude/hooks/audit_post_tool.sh`（Ω-1.6） |
| **窗口** | 1 | **Token** | ~3K |

#### Ω-2.3: Agent spawn → Event Store 集成

| 维度 | 内容 |
|------|------|
| **文件** | 修改 `agent-dispatch.md` Part G + log.md 写入逻辑 |
| **窗口** | 1 | **Token** | ~5K |

#### Ω-2.4: compliance_watchdog → Event Store 读取

| 维度 | 内容 |
|------|------|
| **文件** | 修改 `.claude/scripts/gate_enforcer.py` |
| **功能** | 从 event-store.jsonl 而非 log.md 解析操作密度 |
| **窗口** | 2 | **Token** | ~10K |

#### Ω-2.5: /lint 新增 Event Store 健康检查

| 维度 | 内容 |
|------|------|
| **文件** | 修改 `D:\skills\lint\SKILL.md` |
| **功能** | Event Store 事件量 / 丢失事件 / 延迟事件检测 |
| **窗口** | 1 | **Token** | ~5K |

**Phase Ω-2 DoD**: Event Store 有 ≥10 条事件。PostToolUse 自动追加。compliance_watchdog 从 Event Store 读取。Event Store 健康度纳入 /lint 报告。

---

### Phase Ω-3: 编排层升级（6 项 · 大脑）

#### Ω-3.1: 元编排器核心引擎

| 维度 | 内容 |
|------|------|
| **文件** | `.claude/scripts/meta_orchestrator.py` |
| **功能** | 意图分解（LLM-assisted）→ RSPL 资源匹配 → DAG 工作流生成 |
| **窗口** | 3 | **Token** | ~25K |

#### Ω-3.2: LLM Judge — 执行评分

| 维度 | 内容 |
|------|------|
| **文件** | `.claude/scripts/llm_judge.py` |
| **功能** | 对编排管道中每步 Agent 产出自动评分（1-10），反馈驱动精炼 |
| **评分维度** | 完整性 / 准确性 / 格式合规 / wikilink 密度 / 可追溯性 |
| **窗口** | 2 | **Token** | ~15K |

#### Ω-3.3: skill-orchestration 模板升级

| 维度 | 内容 |
|------|------|
| **文件** | 修改 `.claude/rules/skill-orchestration.md` |
| **功能** | 新增 Part H「元编排器路由」：静态模板匹配 → 未命中 → 元编排器动态合成 |
| **窗口** | 1 | **Token** | ~8K |

#### Ω-3.4: RSPL 资源发现统一 API

| 维度 | 内容 |
|------|------|
| **文件** | `.claude/scripts/rspl_discover.py` |
| **功能** | `discover(task_description)` → 查询所有注册表 → 返回匹配资源 |
| **窗口** | 2 | **Token** | ~12K |

#### Ω-3.5: Agent pipeline 可视化

| 维度 | 内容 |
|------|------|
| **文件** | 新增功能到 `meta_orchestrator.py` |
| **功能** | 每次编排生成 Mermaid DAG 图 |
| **窗口** | 1 | **Token** | ~5K |

#### Ω-3.6: 编排效果追踪

| 维度 | 内容 |
|------|------|
| **文件** | 修改 `event_store.py` + `meta_orchestrator.py` |
| **功能** | 每次编排完成 → Event Store → 二阶进化追踪 |
| **窗口** | 1 | **Token** | ~5K |

**Phase Ω-3 DoD**: 元编排器可为 ≥3 种不同意图生成 DAG。LLM Judge 评分与 Critic 评分偏差 ≤2 分。RSPL discover 返回 ≥5 个匹配资源。

---

### Phase Ω-4: 自进化层闭环（7 项 · 免疫+内分泌）

#### Ω-4.1: SEPL 五算子形式化

| 维度 | 内容 |
|------|------|
| **文件** | 修改 `.claude/rules/self-evolution.md` |
| **功能** | `/evolve` 管道步骤映射到论文 SEPL 五算子（arXiv:2604.15034 §E.3） |
| **五算子映射**（论文→Ω-Loop）: |
| | **Reflect** (映射执行轨迹→因果失败假设) = /evolve 步骤 1-2（14维扫描+检测） |
| | **Select** (识别可进化实体→生成修改提案) = /evolve 步骤 3（生成提案+Watchlist） |
| | **Improve** (通过 RSPL 接口应用提案→候选状态) = /evolve 步骤 4.0-4.4（预验证→展示→用户确认→安全写入） |
| | **Evaluate** (对照目标+安全不变量评分) = /evolve 步骤 4.5（验证+金丝雀测试+回归快照） |
| | **Commit** (有条件接受或回滚) = evolution_canary revert（退化检测→建议回滚→用户确认） |
| **关键发现**: 论文中的五算子并非 Propose/Assess/Commit/Reflect/Rollback——而是 Reflect/Select/Improve/Evaluate/Commit。Rollback 是 Commit 的内置安全阀，非独立算子。此映射基于论文 §E.3.3 和 v4 (2026-05-19) 全文 |
| **窗口** | 2 | **Token** | ~12K |

#### Ω-4.2: RSPL 资源版本化

| 维度 | 内容 |
|------|------|
| **文件** | 修改所有注册表 JSON 文件（skill/mcp/新增 rule/script registry） |
| **功能** | 每个注册表新增 `version` + `changelog` 字段。`resource.discover`/`resource.deprecate` 事件自动追加 |
| **窗口** | 2 | **Token** | ~15K |

#### Ω-4.3: 自动回滚协议

| 维度 | 内容 |
|------|------|
| **文件** | 修改 `.claude/scripts/evolution_canary.py` |
| **功能** | post-deploy 检测到 RSI 下降 ≥0.05 → 自动建议回滚 → 用户确认 → `git revert` + 恢复 .bak |
| **窗口** | 2 | **Token** | ~10K |

#### Ω-4.4: CAR 能力激活率仪表盘

| 维度 | 内容 |
|------|------|
| **文件** | 修改 `.claude/scripts/car_tracker.py` |
| **功能** | 四类能力（Skill/MCP/Script/Agent）激活率实时追踪。综合 CAR <15% → 🔴 强制报告 |
| **数据源** | event-store.jsonl（`resource.discover` + `tool.use` + `agent.spawn` 事件） |
| **窗口** | 2 | **Token** | ~12K |

#### Ω-4.5: RSI 进化效果基准扩展

| 维度 | 内容 |
|------|------|
| **文件** | 修改 `.claude/scripts/evolve_convergence.py` |
| **功能** | RSI 新增子指标：钩子覆盖率 / Skill 激活率 / Event Store 健康度 / Agent spawn 比 |
| **窗口** | 1 | **Token** | ~6K |

#### Ω-4.6: SessionStart Ω-Loop 上下文注入

| 维度 | 内容 |
|------|------|
| **文件** | 修改 `.claude/hooks/session_start.sh`（Ω-1.7） |
| **功能** | 每次会话启动注入 Ω-Loop 健康摘要：钩子状态 / Event Store 事件量 / CAR 趋势 / 待处理信号文件 |
| **窗口** | 1 | **Token** | ~5K |

#### Ω-4.7: 端到端 SEPL 闭环验证

| 维度 | 内容 |
|------|------|
| **功能** | 修改一个规则 → 追踪 Reflect→Select→Improve→Evaluate→Commit 全链路 → 验证每一步都有 Event Store 记录 |
| **窗口** | 1 | **Token** | ~5K |

**Phase Ω-4 DoD**: SEPL 五算子（Reflect→Select→Improve→Evaluate→Commit）在 Event Store 中有完整闭环记录。CAR 仪表盘显示四类能力激活率。自动回滚建议被正确触发（至少 1 次退化检测）。

---

### Phase Ω-5: 文档与验证（5 项 · 交付验收）

#### Ω-5.1: Ω-Loop 架构文档完善

| 维度 | 内容 |
|------|------|
| **文件** | 更新 `wiki/洞察/Ω-Loop生态系统架构.md` |
| **功能** | 更新移植率、补充 SEPL 映射细节、新增 Event Store schema |
| **窗口** | 1 | **Token** | ~5K |

#### Ω-5.2: Skill 导航文件完善

| 维度 | 内容 |
|------|------|
| **文件** | `wiki/洞察/Skill导航.md`（Ω-1.2 创建，本阶段完善） |
| **功能** | 补充全部 7 大类表格 + 新增「医学科研全流程」专区 |
| **窗口** | 1 | **Token** | ~6K |

#### Ω-5.3: CLAUDE.md 更新

| 维度 | 内容 |
|------|------|
| **文件** | 修改 `CLAUDE.md` |
| **功能** | 新增步骤 0.7（钩子健康检查）+ 步骤 0.8（Ω-Loop 状态摘要）+ 更新 Skill 索引 |
| **窗口** | 1 | **Token** | ~5K |

#### Ω-5.4: 端到端集成测试 — SBB 课题 v4.0 重跑

| 维度 | 内容 |
|------|------|
| **功能** | 在新的 Ω-Loop 系统下重跑 SBB 课题——验证基线指标改善 |
| **验证点** | Skill 推荐被注入 / Write 操作被 hook 拦截 / Agent 被派遣 / Event Store 有记录 / Stop hook 检查配额 |
| **窗口** | 2 | **Token** | ~15K |

#### Ω-5.5: Omega v2 ↔ Ω-Loop 对照表完善

| 维度 | 内容 |
|------|------|
| **文件** | 更新 `wiki/洞察/Ω-Loop生态系统架构.md` 第五节 |
| **功能** | 标注 15 项 Omega 理念的移植完成状态 |
| **窗口** | 1 | **Token** | ~3K |

**Phase Ω-5 DoD**: SBB 课题重跑：Skill 推荐被注入、Write 被 hook 拦截、Agent 被派遣。Omega 对照表 15/15 项标注完成。

---

## 五、风险矩阵

### 5.1 技术风险

| 风险 | 影响 | 概率 | 缓解策略 |
|------|:--:|:--:|------|
| **钩子脚本执行权限问题** | 🔴 整个钩子层不可用 | 中 | SessionStart 钩子自动检测；`chmod +x` 验证 |
| **PreToolUse 钩子阻止合法操作** | 🟡 用户操作被误拦 | 低 | 钩子脚本保守设计——仅拦截明确违规，放行不确定项 |
| **Stop 钩子无限循环** | 🟡 会话无法正常结束 | 低 | `stop_hook_active=true` 自动放行；Claude Code 内置限 8 次 |
| **Event Store 性能退化** | 🟡 JSONL 文件过大 | 低 | 月度轮转（>10K 行→归档）；/lint 自动检测 |
| **settings.json 合并冲突** | 🟡 已有 hooks 块被覆盖 | 低 | 合并前备份；逐 matcher 追加 |
| **skill_router.py 匹配质量差** | 🟡 推荐不相关 Skill | 中 | 50+ 模式起步；使用反馈逐步精炼 |

### 5.2 组织风险

| 风险 | 影响 | 概率 | 缓解策略 |
|------|:--:|:--:|------|
| **用户拒绝钩子层** | 🔴 基础被否决 | 低 | 每个 Phase 完成后的验收演示 |
| **逐项确认疲劳** | 🟡 35 项逐一确认 | 中 | Phase 内任务批量展示；提供"Phase N 全部确认" |
| **方案过大导致中断** | 🔴 中途搁置 | 低 | Phase 独立交付——每 Phase 完成后系统已可运行 |

### 5.3 降级策略

| 场景 | 降级方案 |
|------|---------|
| 钩子脚本执行失败 | 回退到当前合规自检模式（文本规则）——SessionStart 中检测并报告 |
| Event Store 写入失败 | 降级到 log.md 文本模式——/lint 中检测并报告 |
| 元编排器合成失败 | 降级到 skill-orchestration 静态模板匹配 |
| CAR 追踪器数据不足 | 降级到 log.md grep 估算 |
| 自动回滚误触发 | 回滚前必须用户确认——不自动执行 |

---

## 六、验收标准

### 6.1 全局验收标准

| 指标 | 当前（vFinal 前） | 目标（Ω-5 后） | 测量方式 |
|------|:--:|:--:|------|
| Skill 激活率 | 0% | ≥30% | car_tracker.py — Skill 类 |
| Agent spawn 覆盖率 | 8% (1/12 dispatch) | ≥50% | car_tracker.py — Agent 类 |
| PreToolUse 合规拦截率 | 不存在 | ≥95% | Event Store `hook.block` 事件/总 Write 操作 |
| Event Store 完整性 | 不存在 | 100% | /lint Event Store vs log.md 对比 |
| RSI（规则稳定性） | ~0.80 | ≥0.85 | evolve_convergence.py |
| 钩子可用性 | 不存在 | 5/5 钩子注册且可执行 | SessionStart 钩子自检 |
| SBB 重跑 Skill 激活 | 0/749 | ≥3 个 Skill 通过 Skill() 工具调用 | 会话 log 分析 |

### 6.2 上线后监控

每次会话启动注入：
```
📊 Ω-Loop 状态
钩子层: ✅ 5/5 | Event Store: N 条事件 | Agent: N spawn/7d
CAR: X% | RSI: 0.XX | 信号文件: N 个待处理
```

每次 /lint 自动审计：Event Store 完整性 / 钩子拦截率 / Skill 推荐精准度 / Agent 配额达标率 / RSI 趋势。

---

## 附录 A: 与 vFinal v2 修复方案的对照

| vFinal v2 任务 | Ω-Loop Phase | 变更 |
|------|:--:|------|
| H-1 Skill 路由系统 | Ω-1.1 | 基本一致，增强：从 skill-registry.json 动态生成映射 |
| H-2 Skill 导航文件 | Ω-1.2 → Ω-5.2 | 分两阶段 |
| H-3 PreToolUse Write | Ω-1.3a | 一致 |
| H-4 PreToolUse Bash | Ω-1.3b | 一致 |
| H-5 PreToolUse Read | Ω-1.3c | 一致 |
| H-6 Stop Agent 配额 | Ω-1.4 | 增强：新增 enforce --gate all 检查 |
| H-7 settings.json | Ω-1.5 | 增强：新增 PostToolUse + SessionStart 钩子 |
| H-8 规则冲突统一 | Phase 0 | 扩展：3→5 项，独立 Phase |
| H-9 CLAUDE.md 更新 | Ω-5.3 | 扩展：新增步骤 0.8 |
| H-10 端到端验证 | Ω-5.4 | 扩展：SBB 课题重跑 |
| — | Ω-2.1~Ω-2.5 | 🆕 总线层 |
| — | Ω-3.1~Ω-3.6 | 🆕 编排层 |
| — | Ω-4.1~Ω-4.7 | 🆕 自进化层 |
| — | Ω-5.5 | 🆕 Omega 对照表 |

## 附录 B: 执行顺序与依赖图

```
Phase 0 (规则冲突统一) ─────────────────────────────┐
      │                                              │
      ▼                                              │
Phase Ω-1 (钩子层) ──── 核心交付物 ──────────────────┤
      │                                              │
      ├── Ω-1.1 skill_router.py                      │
      ├── Ω-1.2 Skill导航.md (基础)                   │
      ├── Ω-1.3a/b/c PreToolUse ×3                   │
      ├── Ω-1.4 Stop 钩子                            │
      ├── Ω-1.5 settings.json                        │
      ├── Ω-1.6 PostToolUse ──→ Ω-2.2                 │
      └── Ω-1.7 SessionStart ──→ Ω-4.6               │
      │                                              │
      ▼                                              │
Phase Ω-2 (总线层) ──── 依赖 PostToolUse 钩子 ───────┤
      │                                              │
      ▼                                              │
Phase Ω-3 (编排层) ──── 依赖 Event Store + RSPL ─────┤
      │                                              │
      ▼                                              │
Phase Ω-4 (自进化层) ── 依赖 Event Store + SEPL ─────┤
      │                                              │
      ▼                                              │
Phase Ω-5 (文档与验证) ─ 依赖全部前置 Phase ─────────┘
```

---

*创建于 2026-06-16 — Ω-Loop 最终执行方案 v1.0*
*基于：Omega v2 + Autogenesis Protocol (arXiv:2604.15034) + Mimosa Framework (arXiv:2603.28986) + SBB 课题 v4.0 复盘 + 知识库工作流修复方案 vFinal v2*
