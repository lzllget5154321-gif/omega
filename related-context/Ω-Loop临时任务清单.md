---
type: insight
tags: [Ω-Loop, 任务清单, 临时文件, 多窗口验证]
created: 2026-06-16
updated: 2026-06-16
knowledge_stability: timely
note: 临时任务清单——执行完成后可删除。主方案见 [[Ω-Loop最终执行方案]]。
---

# Ω-Loop 临时任务清单 v1.0

> 此文件为纯任务清单版本——每项可独立勾选。用于多窗口分步执行、相互验证。
> **主方案（含诊断/架构/UEP/风险/验收）**: [[Ω-Loop最终执行方案]]
> **Skill 导航（人类查阅）**: [[Skill导航]]
>
> 总任务: **35 项** | 总预估 Token: **~286K**

---

## Phase 0: 规则冲突统一（5 项 · ~14K）

- [x] **P0-1** (3K) C1: agent-automation.md F.4 删除双重 dispatch 定义 → 改为引用 agent-dispatch.md G.4.5
  → 验证: `grep -n "F\.4\|dispatch.*实效性" .claude/rules/agent-automation.md` 确认无独立定义段落
- [x] **P0-2** (3K) C2: external-project-workflow.md F.1/F.2 声明为外部安全门控唯一来源。compliance #17 改为引用
  → 验证: `grep -n "#17.*外部" .claude/rules/compliance-monitoring.md` 含"→ 统一门控见 external-project-workflow.md"
- [x] **P0-3** (3K) C3: verification-gate.md v2.0 统一验证协议——Grep compliance #21/#29 + evolve 4.5 → 确认均引用
  → 验证: 三个引用点均指向 verification-gate.md（不含过期的 self-reference）
- [x] **P0-4** (3K) C4: tool-fallback-matrix.md Part 0 v3.0 unified_search.py 单入口——Grep compliance #36 + evolution-sources S3.1 + skill-orchestration G.1
  → 验证: 三个引用点均指向 unified_search.py 或 tool-fallback-matrix Part 0
- [x] **P0-5** (2K) C5: self-evolution.md Part D 冷却章节追加「以 compliance-monitoring.md #30 的 format_gate.py evolve-cooling 返回码为强制执行标准」
  → 验证: `grep "evolve-cooling.*返回码\|compliance-monitoring.*#30.*冷却" .claude/rules/self-evolution.md`

---

## Phase Ω-1: 钩子层部署（7 项 · ~68K）

> 🔴 核心交付物。执行顺序：先建脚本 → 再配 settings.json → 再更新 CLAUDE.md → 最后验证。

- [x] **Ω-1.1** (20K) 创建 `.claude/scripts/skill_router.py` + `.claude/hooks/skill_router.sh` — UserPromptSubmit 钩子
  → 功能: 每次用户说话→语义匹配 skill-registry.json→注入 Top 5 Skill 推荐
  → 验证: `echo '{"prompt":"帮我写一篇论文初稿"}' | python .claude/scripts/skill_router.py` 输出含 academic-writing, compose, halluref-citation-check
  → 约束: 永不阻止（exit 0 always），超时 25s

- [x] **Ω-1.2** (8K) 创建 `wiki/洞察/Skill导航.md` — 人类查阅入口
  → 功能: 7 大类（写作·图表·数据分析·知识管理·系统·发布·医学科研）
  → 验证: 文件 ≥3KB + 含 ≥30 个 Skill 条目 + 每个条目含 Skill 名/一句话/触发方式

- [x] **Ω-1.3a** (5K) 创建 `.claude/scripts/hooks/compliance_pre_write.py` — PreToolUse Write/Edit 合规 ✅ 已修复
  → 功能: `format_gate.py pre-write --path "$FILE_PATH"` → exit≠0 阻止
  → 验证: 尝试直接 Write 文件（不运行 pre-write）→ 应被阻止

- [x] **Ω-1.3b** (5K) 创建 `.claude/scripts/hooks/compliance_bash_guard.py` — PreToolUse Bash 路由 ✅ 已部署
  → 功能: 拦截 curl/wget/Invoke-WebRequest → 检查 SEARCH_ROUTER_OK 标记文件（2min 有效期）
  → 验证: 尝试 `curl` 外部 URL → 应被阻止

- [x] **Ω-1.3c** (3K) 创建 `.claude/scripts/hooks/pre_read_guard.py` — PreToolUse Read 预检 ✅ 已部署
  → 功能: `.csv/.json/.py/.R` → `format_gate.py pre-read` → exit 3 (≥30MB) 硬阻断
  → 验证: 尝试 Read ≥30MB 文件 → 应被阻止

- [x] **Ω-1.4** (5K) 创建 `.claude/scripts/hooks/agent_quota_stop.py` — Stop 钩子 ✅ 已部署
  → 功能: 会话结束前检查 Agent 配额 + pending-dispatch.json + pending-critic-check.json → 未达标则 block
  → 约束: `stop_hook_active=true` 自动放行。超时 10s
  → 验证: 创建 pending-dispatch.json → 尝试结束会话 → 应被阻止

- [x] **Ω-1.5** (8K) 配置 `.claude/settings.json` — 注册全部 5 个钩子 ✅
  → 功能: UserPromptSubmit ×1 + PreToolUse ×3 + Stop ×1
  → 关键: 若已有 hooks 块→逐个追加非替换。备份原文件到 `.bak`
  → 验证: `/hooks` 菜单显示 5 个钩子已注册

- [x] **Ω-1.6** (3K) 创建 `.claude/hooks/audit_post_tool.sh` — PostToolUse 审计
  → 功能: 每次 Write/Edit 成功后追加 `tool.use` 事件到 event-store.jsonl
  → 约束: 永不阻止（exit 0 always），超时 5s

- [x] **Ω-1.7** (3K) 创建 `.claude/hooks/session_start.sh` — SessionStart 健康检查
  → 功能: 检查 5 个钩子脚本存在+可执行 → 检查信号文件残留 → 注入 Ω-Loop 健康摘要
  → 验证: 删除一个钩子脚本 → 启动新会话 → 应看到 "⚠️ 钩子层不完整"

---

## Phase Ω-2: 总线层建设（5 项 · ~35K）

> 依赖 Phase Ω-1 的 PostToolUse 钩子。

- [x] **Ω-2.1** (12K) 创建 `.claude/scripts/event_store.py` — Event Store 核心 API
  → 功能: `record_event(source, event, payload)` → 追加 JSONL
  → Schema: `{"timestamp":"ISO","source":"component","event":"type","payload":{},"session":"id"}`
  → 事件类型: tool.use, hook.block, agent.spawn, agent.complete, evolve.apply, compliance.violation, resource.discover, resource.deprecate, session.start, session.complete

- [x] **Ω-2.2** (3K) PostToolUse → Event Store 集成（修改 Ω-1.6 的 audit_post_tool.sh）
  → 功能: Write/Edit 成功 → `python .claude/scripts/event_store.py record --source hook --event tool.use`

- [x] **Ω-2.3** (5K) Agent spawn → Event Store 集成（修改 agent-dispatch.md Part G + log.md 写入逻辑）
  → 功能: 每次 Agent spawn 完成后追加 `agent.spawn` 事件

- [x] **Ω-2.4** (10K) compliance_watchdog → Event Store 读取（修改 gate_enforcer.py）
  → 功能: 从 event-store.jsonl 而非 log.md 解析操作密度

- [x] **Ω-2.5** (5K) /lint 新增 Event Store 健康检查（修改 lint SKILL.md）
  → 功能: Event Store 事件量 / 丢失事件（log.md 有但 Event Store 无） / 延迟事件

---

## Phase Ω-3: 编排层升级（6 项 · ~70K）

> 依赖 Phase Ω-2 的 Event Store。

- [x] **Ω-3.1** (25K) 创建 `.claude/scripts/meta_orchestrator.py` — 元编排器核心引擎
  → 功能: 意图分解→RSPL 匹配→DAG 工作流生成
  → 验证: 可为 ≥3 种不同意图生成 DAG

- [x] **Ω-3.2** (15K) 创建 `.claude/scripts/llm_judge.py` — LLM Judge 执行评分
  → 功能: 每步 Agent 产出自动评分（1-10）—完整性/准确性/格式合规/wikilink密度/可追溯性
  → 验证: LLM Judge 评分与 Critic 评分偏差 ≤2 分

- [x] **Ω-3.3** (8K) skill-orchestration 模板升级 ✅ Part H 已存在（2026-06-16）
  → 功能: 新增 Part H「元编排器路由」：静态模板匹配 → 未命中 → 元编排器动态合成

- [x] **Ω-3.4** (12K) 创建 `.claude/scripts/rspl_discover.py` — RSPL 资源发现 API
  → 功能: `discover(task_description)` → 查询所有注册表 → 返回匹配资源
  → 验证: 返回 ≥5 个匹配资源

- [x] **Ω-3.5** (5K) Agent pipeline 可视化（扩展 meta_orchestrator.py）
  → 功能: 每次编排生成 Mermaid DAG 图

- [x] **Ω-3.6** (5K) 编排效果追踪（扩展 event_store.py + meta_orchestrator.py）
  → 功能: 每次编排完成→Event Store→二阶进化追踪

---

## Phase Ω-4: 自进化层闭环（7 项 · ~65K）

> 依赖 Phase Ω-3 的 RSPL + Event Store。

- [x] **Ω-4.1** (12K) SEPL 五算子形式化（修改 self-evolution.md）
  → 功能: /evolve 管道步骤映射到论文五算子（arXiv:2604.15034 §E.3）:
    **Reflect**=步骤 1-2, **Select**=步骤 3, **Improve**=步骤 4.0-4.4, **Evaluate**=步骤 4.5, **Commit**(含rollback)=evolution_canary revert
  → 验证: self-evolution.md §Part A 含五算子映射表

- [x] **Ω-4.2** (15K) RSPL 资源版本化（修改全部注册表 JSON 文件）
  → 功能: skill/mcp/新增 rule/script registry → 每个加 version + changelog 字段
  → 新增事件: resource.discover / resource.deprecate

- [x] **Ω-4.3** (10K) 自动回滚协议（修改 evolution_canary.py）
  → 功能: post-deploy RSI 下降 ≥0.05 → 自动建议回滚 → 用户确认 → git revert + 恢复 .bak
  → 验证: 至少 1 次退化检测触发

- [x] **Ω-4.4** (12K) CAR 能力激活率仪表盘（修改 car_tracker.py）
  → 功能: 四类能力（Skill/MCP/Script/Agent）激活率实时追踪。综合 CAR <15%→🔴
  → 数据源: event-store.jsonl

- [x] **Ω-4.5** (6K) RSI 进化效果基准扩展（修改 evolve_convergence.py）
  → 功能: 新增子指标——钩子覆盖率/Skill 激活率/Event Store 健康度/Agent spawn 比

- [x] **Ω-4.6** (5K) SessionStart Ω-Loop 上下文注入 ✅ CAR+RSI+Omega-Loop one-liner 已追加 (5K) SessionStart Ω-Loop 上下文注入（修改 session_start.sh）
  → 功能: 注入 Ω-Loop 健康摘要——钩子状态/Event Store 事件量/CAR 趋势/待处理信号文件

- [x] **Ω-4.7** (5K) 端到端 SEPL 闭环验证 ✅ 5/5 operators ×2 events, 14 evolve events total (5K) 端到端 SEPL 闭环验证
  → 功能: 修改一个规则→追踪 Reflect→Select→Improve→Evaluate→Commit 全链路→验证每一步都有 Event Store 记录

---

## Phase Ω-5: 文档与验证（5 项 · ~34K）

> 依赖全部前置 Phase。

- [x] **Ω-5.1** (5K) Ω-Loop 架构文档完善（更新 Ω-Loop生态系统架构.md）
  → 功能: 更新移植率、补充 SEPL 映射细节、新增 Event Store schema

- [x] **Ω-5.2** (6K) Skill 导航文件完善（完善 Skill导航.md——Ω-1.2 创建的基础版）
  → 功能: 补充全部 7 大类表格 + 新增「医学科研全流程」专区

- [x] **Ω-5.3** (5K) CLAUDE.md 更新
  → 功能: 新增步骤 0.7（钩子健康检查）+ 步骤 0.8（Ω-Loop 状态摘要）+ 更新 Skill 索引

- [x] **Ω-5.4** (15K) 端到端集成测试 ✅ 5/5 验证点通过（36 events, 5 sources, agent.spawn×3） (15K) 端到端集成测试 — SBB 课题 v4.0 重跑
  → 验证点: Skill 推荐被注入 / Write 被 hook 拦截 / Agent 被派遣 / Event Store 有记录 / Stop hook 检查配额

- [x] **Ω-5.5** (3K) Omega v2 ↔ Ω-Loop 对照表完善（更新 Ω-Loop生态系统架构.md 第五节）
  → 功能: 标注 15 项 Omega 理念的移植完成状态

---

## 多窗口分步执行建议

| 窗口 | Phase | 依赖 | 预估 Token |
|:--:|------|------|:--:|
| **窗口 1** | P0-1→P0-5（规则冲突统一） | 无 | ~14K |
| **窗口 2** | Ω-1.1 + Ω-1.2（Skill 路由+导航） | P0 完成 | ~28K |
| **窗口 3** | Ω-1.3a/b/c + Ω-1.4 + Ω-1.6 + Ω-1.7（钩子脚本） | P0 完成 | ~24K |
| **窗口 4** | Ω-1.5（settings.json 配置） | 窗口 2+3 的脚本已创建 | ~8K |
| **窗口 5** | Ω-5.4（SBB 重跑验证） | Ω-1 全部完成 | ~15K |
| — | 后续 Phase 按依赖串行 — | | |

**交叉验证方式**: 两个独立窗口执行同一 Phase 的不同任务 → 完成后对比 Event Store 记录的一致性。

---

*此文件为临时任务清单——执行完成后可删除。*
