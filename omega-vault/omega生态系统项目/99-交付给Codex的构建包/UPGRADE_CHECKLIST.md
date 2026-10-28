# Omega 升级验收清单
# ===================
# Codex 每完成一个升级阶段，必须逐项检查。全部通过才能进入下一阶段。
# 如某项未通过，必须在进入下一阶段前修复。

---

## Phase 1.5：Omega Terminal Lite — 早期统一窗口

> 设计文档：`build-package/OMEGA_TERMINAL.md`、`schemas/terminal_event.schema.json`

- [ ] `app/web/app.py` 存在（Terminal Lite 后端，< 150 行）
- [ ] `app/web/templates/terminal.html` 存在（三栏布局 + HTMX，< 200 行）
- [ ] `app/web/static/htmx.min.js` 已下载
- [ ] `omega web --port 8420` 启动成功
- [ ] 浏览器打开 `http://localhost:8420` → 三栏布局渲染正确
- [ ] 左侧栏：文件浏览器正常展示 vault 目录
- [ ] 中央栏：对话区消息正常渲染
- [ ] 右侧栏：任务面板 + 通知面板正常
- [ ] 底部栏：命令输入框 + 发送按钮工作
- [ ] 状态栏：显示 Omega 版本 + API 引擎 + 任务数 + 时钟
- [ ] 自然语言输入"omega status"→ 返回系统状态（对话区显示）
- [ ] 文件拖拽上传 → 隔离区存储 → 返回 upload_result 卡片
- [ ] 文件上传安全规则生效（类型白名单/大小限制/隔离区路径/SHA-256）
- [ ] 通知推送正常显示在通知面板
- [ ] `curl http://localhost:8420/api/events` 轮询正常
- [ ] `curl http://localhost:8420/api/status` 返回 JSON
- [ ] `omega bench --all` 通过率 ≥ 80%

---

## 升级前基线（Phase 1 = MFE）

- [ ] `OMEGA_HOME` 已确认（默认 `D:\Omega-System`）
- [ ] `omega --version` 返回 `omega v0.3.0-mfe`
- [ ] `omega bench --all` 返回 7/7 通过
- [ ] `omega status` 显示所有服务健康
- [ ] Docker 容器全部运行（postgres, qdrant, omega-sandbox, omega-sandbox-net）
- [ ] `pytest tests/` 全部通过（72 tests）
- [ ] `.venv` 虚拟环境存在且激活

---

## Phase 2：Docker 沙箱重构建

> **Python 版本说明**：主机 Omega 运行时使用 Python 3.12；Docker 沙箱镜像使用 python:3.11-slim-bookworm（Debian bookworm 稳定版兼容性优先——沙箱内 Python 版本独立于主机，不影响主机 3.12 代码执行）。

- [ ] `Dockerfile.sandbox` 基于 `python:3.11-slim-bookworm`（沙箱内 3.11；主机仍 3.12）
- [ ] `Dockerfile.sandbox-net` 基于 `python:3.11-slim-bookworm` + git + curl + node
- [ ] `docker compose build omega-sandbox omega-sandbox-net` 成功
- [ ] `docker exec omega-sandbox python --version` 输出 Python 3.11.x
- [ ] `docker exec omega-sandbox python -c "import numpy"` 成功
- [ ] `docker exec omega-sandbox python -c "import pandas"` 成功
- [ ] `docker exec omega-sandbox-net pip --version` 输出 pip 24.x
- [ ] `docker exec omega-sandbox-net pip install matplotlib` 成功
- [ ] `docker exec omega-sandbox curl --version` 失败（离线沙箱无 curl）
- [ ] `omega-sandbox` 容器 `network_mode: "none"` 仍生效
- [ ] `omega bench --all` 仍 7/7 通过
- [ ] `pytest tests/` 全部通过

---

## Phase 3：动态评分路由器

- [ ] `app/router/scorer.py` 存在 — `DynamicScorer` 类
- [ ] `app/router/feedback.py` 存在 — `ScoreFeedbackLoop` 类
- [ ] `DynamicScorer.score()` 返回 `list[ScoredCandidate]` 按总分降序
- [ ] 12 维评分权重正确（task_fit=0.20, success_rate=0.18, output_quality=0.15...）
- [ ] 冷启动所有候选 0.5 分
- [ ] 阶段权重从 `stage_weights.yaml` 加载
- [ ] `ToolAgentRouter.select_steps()` 接受 `enable_scoring=True`
- [ ] Engine Resolver 在评分后硬过滤不可用引擎
- [ ] `ScoreFeedbackLoop.update()` 使用 EMA（α=0.3）
- [ ] 工具分数持久化到 `omega-workspace/state/tool_scores.json`
- [ ] `tests/test_scorer.py` 全部通过
- [ ] `omega bench --all` 仍 7/7 通过

---

## Phase 4：Agent 运行时

- [ ] `app/agents/` 包存在（`__init__.py`, `agent.py`, `dispatcher.py`, `capability.py`）
- [ ] `AgentRuntime` 从 `agents.yaml` 加载配置
- [ ] 工具白名单/黑名单过滤生效
- [ ] 自主级别门控 `AutonomyLevel` 枚举（L0/L1/L2/L3）
- [ ] `AgentDispatcher.dispatch()` 按 agent 字段或能力匹配
- [ ] `AgentDispatcher.handoff()` 验证交接目标
- [ ] `CapabilityChecker.check()` 返回 (has_all, missing)
- [ ] `CapabilityChecker.find_gaps()` 发现能力缺口
- [ ] Planner 的 `plan()` 每个 step 包含 `assigned_agent`
- [ ] Planner 的 `execute_plan()` 调用 AgentDispatcher
- [ ] `tests/test_agents.py` 全部通过
- [ ] `omega bench --all` 仍 7/7 通过

---

## Phase 5：完整动态规划器

- [ ] `app/planner/templates/` 含 3+ JSON 模板
- [ ] 模板定义 task_type/stages/dependencies/parallel_groups/capabilities
- [ ] `app/planner/dependency.py` — `DependencyAnalyzer` 类
- [ ] `DependencyAnalyzer.build_dependency_graph()` 返回正确拓扑序
- [ ] `app/planner/dag.py` — `build_parallel_dag()` 存在
- [ ] 并行 DAG 正确标记 parallel 分支
- [ ] `app/planner/gap_check.py` — `GapPrecheck` 类
- [ ] `GapPrecheck.check()` 报告能力缺口
- [ ] 无法填补的缺口标记 `requires_manual_intervention`
- [ ] `DynamicTaskPlanner.plan()` 执行完整 7 步流程
- [ ] `tests/test_planner.py` 扩展测试全部通过
- [ ] `omega bench --all` 仍 7/7 通过

---

## Phase 6：MCP 管理器 + Toolsmith-Lite

- [ ] `app/mcp/manager.py` — `MCPServerManager` 类
- [ ] `start()` / `stop()` / `health()` 方法实现
- [ ] 支持 8 个 MCP 服务器（filesystem/postgres/qdrant/playwright/github/brave-search/sequential-thinking/memory）
- [ ] `app/toolsmith/adapter.py` — `ToolAdapter` 类
- [ ] 输入/输出 schema 生成、参数映射、错误处理、超时控制
- [ ] `app/toolsmith/smith.py` — `Toolsmith` 类
- [ ] 完整 7 步闭环：detect_gap → discover → install → generate_adapter → test → register → package_skill
- [ ] `omega tool discover ppt_generation --auto-install` 成功
- [ ] `tests/test_mcp.py` 全部通过
- [ ] `tests/test_toolsmith.py` 全部通过
- [ ] `omega bench --all` 仍 7/7 通过

---

## Phase 7：记忆层

- [ ] `app/memory/schema.sql` — 3 张表 DDL
- [ ] `app/memory/action_store.py` — `ActionStore` 类
- [ ] `record_task()` / `record_execution()` / `get_tool_success_rate()` 工作
- [ ] `app/memory/semantic_store.py` — `SemanticStore` 类
- [ ] Qdrant 三表创建（tool_descriptions/task_patterns/source_pages）
- [ ] `search()` 返回语义相似条目
- [ ] `ScoreFeedbackLoop` 从 action_store 读取历史成功率
- [ ] `omega status` 显示 PostgreSQL 和 Qdrant 连接状态
- [ ] 手动触发任务后 `task_history` 表有记录
- [ ] `tests/test_memory.py` 全部通过
- [ ] `omega bench --all` 仍 7/7 通过

---

## Phase 8：演化引擎 + 成果包 + 日志

- [ ] `app/evolution/engine.py` — `EvolutionEngine` 类
- [ ] 读取 `risk_policy.yaml`：LOW→auto/MEDIUM→sandbox_test/HIGH→confirm/CRITICAL→no_auto
- [ ] `omega evolve --check` 报告可升级工具
- [ ] `omega evolve --upgrade <tool_id>` 手动升级
- [ ] `app/evolution/ecp.py` — `ECPManager` 类（🆕 Evolution Change Proposal）
- [ ] `omega evolve --propose <tool_id>` 生成 ECP 提案
- [ ] ECP 包含：变更摘要/风险评估/影响面分析/回滚方案/沙箱测试计划
- [ ] `omega evolve approve <ecp_id>` 审批 ECP
- [ ] `omega evolve execute <ecp_id>` 执行已批准 ECP
- [ ] `omega evolve rollback <ecp_id>` 回滚 ECP
- [ ] `omega evolve list-ecps --status pending` 列出待审批 ECP
- [ ] ECP 持久化为 JSON（`omega-workspace/state/ecps/`）
- [ ] `app/outcome/builder.py` — `OutcomeBuilder` 类
- [ ] 8 种模态成果包实现
- [ ] `omega task "..." --execute` 完成后 `omega-workspace/outcomes/` 有产物包
- [ ] `app/logging_setup.py` — Python logging 配置
- [ ] `omega-runtime/logs/omega.log` 有结构化记录
- [ ] 日志含 task 创建/plan 生成/Agent 分配/工具执行/完成/失败
- [ ] `tests/test_evolution.py` 全部通过（含 ECP 审批流程测试）
- [ ] `tests/test_outcome.py` 全部通过
- [ ] `omega bench --all` 仍 7/7 通过

---

## Phase 9：域扩展

- [ ] `app/executor/viz_executor.py` 存在且可生成 matplotlib 图表
- [ ] [可选] manim 安装成功（通过 Toolsmith）
- [ ] [可选] blender 命令行可用
- [ ] `app/executor/browser_executor.py` — 浏览器表单预填/截图
- [ ] Playwright MCP 服务器健康检查通过
- [ ] `app/executor/creative_router.py` — 12 种创意任务类型
- [ ] [可选] `Dockerfile.sandbox-net` 添加 R 运行时
- [ ] `tests/test_viz.py` 全部通过
- [ ] `tests/test_browser.py` 全部通过
- [ ] `omega bench --all` 通过率 ≥ 80%（新增闭环）
- [ ] 新增闭环（科学可视化、浏览器自动化）至少 1/2 通过

---

## Phase 10：Omega Terminal — 统一操作窗口

> 设计文档：`build-package/OMEGA_TERMINAL.md`

### 10.1 后端扩展
- [ ] `app/web/ws.py` — WebSocket 管理器（连接/日志/进度/通知推送）
- [ ] `app/web/api/task_api.py` — 任务 CRUD API
- [ ] `app/web/api/upload_api.py` — 文件上传 + 智能类型识别（PDF/CSV/PPTX 等）
- [ ] `app/web/api/notify_api.py` — 通知列表/已读 API
- [ ] `app/web/api/vault_api.py` — 文件浏览/搜索 API
- [ ] WebSocket 端点 `/api/terminal/ws` 正常连接
- [ ] `omega web --port 8420` 启动完整后端 + 静态挂载

### 10.2 前端（React SPA）
- [ ] `app/web/terminal/package.json` 存在，`npm install && npm run build` 成功
- [ ] 布局渲染：左栏(文件浏览器) | 中栏(对话区) | 右栏(上下文面板) | 底栏(输入) | 状态栏
- [ ] `CommandInput.tsx` — 自然语言输入 + 发送按钮工作
- [ ] `ChatArea.tsx` — 消息列表正确渲染（Markdown/代码块/文件卡片）
- [ ] `FileBrowser.tsx` — vault 目录树展示，右键菜单工作
- [ ] `ContextPanel.tsx` — 当前任务详情 + 历史记录展示
- [ ] `CommandPalette.tsx` — Ctrl+Shift+P 列出所有闭环命令
- [ ] `TaskMonitor.tsx` — 实时进度条 + 步骤列表更新
- [ ] `NotificationCenter.tsx` — 通知汇聚 + 未读徽标
- [ ] `ConfirmDialog.tsx` — 交互式确认框（ECP 审批/高风险确认）
- [ ] `StatusBar.tsx` — 系统状态/API 引擎/任务数显示
- [ ] 键盘快捷键全部工作（Ctrl+Enter/Ctrl+L/Ctrl+Shift+P 等 12 个）

### 10.3 文件上传
- [ ] 拖拽 PDF → 对话区 → 自动识别 + 提示处理方式
- [ ] 点击 📎 → 文件选择器 → 上传 + 识别
- [ ] 拖拽文件夹（多文件）→ 提示批量处理建议

### 10.4 实时通信
- [ ] WebSocket 日志流实时显示在对话区
- [ ] 任务进度推送实时更新 TaskMonitor
- [ ] 通知推送实时更新 NotificationCenter

### 10.5 后台服务
- [ ] `app/service.py` — 常驻进程 + 任务队列 + 演化定时器
- [ ] `app/notify.py` — WebSocket 推送 + vault 通知.md 双写
- [ ] `omega service start` 启动后台服务

### 10.6 桌面打包（可选）
- [ ] `omega web --electron` 启动独立桌面窗口
- [ ] 或 `pywebview` 方案可用

### 10.7 自动化测试
- [ ] `tests/test_terminal.py` 全部通过（14 项功能验证）
- [ ] `omega bench --all` 通过率 ≥ 90%

---

## Phase 11：质量与安全加固

### 11.1 模拟构建器
- [ ] `app/safety/simulator.py` — `BuildSimulator` 类
- [ ] `omega simulate phase-2` 生成完整 DAG + 文件变更清单 + 风险表 + 预计耗时
- [ ] 模拟报告包含：文件变更/风险评估/时间预估/回滚命令
- [ ] 模拟不修改任何文件（干运行验证）
- [ ] `tests/test_simulator.py` 全部通过

### 11.2 任务飞行记录仪
- [ ] `app/memory/flight_recorder.py` — `FlightRecorder` 类
- [ ] 每个任务记录：goal/task_type/selected_tools/engine_used/agent_assigned
- [ ] 每个步骤记录：step_id/tool/success/duration_ms/error
- [ ] 成本追踪：total_api_calls/estimated_cost_usd
- [ ] 产出溯源：output_files/output_pages
- [ ] `omega flightlog <task_id>` 显示完整审计记录
- [ ] 飞行记录持久化为 JSON（`omega-runtime/logs/flights/`）
- [ ] `tests/test_flight_recorder.py` 全部通过

### 11.3 溯源水印
- [ ] `app/outcome/provenance.py` — `ProvenanceWatermark` 类
- [ ] `ProvenanceLink` 支持 7 种来源类型（literature/code/data/model_call/web_search/tool_output）
- [ ] 每个结论可追溯至原始来源（DOI/file_path/URL/prompt_hash）
- [ ] 溯源链计算 Merkle 式哈希
- [ ] 水印以 HTML 注释嵌入成果页（`<!-- OMEGA-PROVENANCE ... -->`）
- [ ] `tests/test_provenance.py` 全部通过

### 11.4 预算与质量控制台
- [ ] `app/router/budget_console.py` — `BudgetConsole` 类
- [ ] 4 种执行模式：CHEAP / HIGH_QUALITY / OFFLINE / BALANCED
- [ ] 每种模式映射具体引擎选择和成本上限
- [ ] `omega budget cheap` 切换为低成本模式
- [ ] `omega budget high_quality` 切换为高质量模式
- [ ] 质量敏感任务（academic_writing/literature_review）自动选 HIGH_QUALITY
- [ ] 无外部引擎时自动降级为 OFFLINE
- [ ] `tests/test_budget.py` 全部通过

### 11.5 Toolsmith 隔离与签名
- [ ] `app/toolsmith/quarantine.py` — `QuarantineManager` 类
- [ ] 新工具先进入隔离区（quarantine registry），不直接写正式注册表
- [ ] 验收测试：功能测试 + 安全检查 + 依赖冲突检测
- [ ] 三项全通过 → PASSED → 可签名
- [ ] 任一项失败 → REJECTED
- [ ] 签名工具 → `omega quarantine promote` 推广到正式 `config/tools.yaml`
- [ ] `omega quarantine list` 列出隔离区工具
- [ ] `omega quarantine test --tool-id <id>` 运行验收测试
- [ ] `tests/test_quarantine.py` 全部通过

### 11.6 知识库防污染守卫
- [ ] `app/safety/kb_guard.py` — `KnowledgeBaseGuard` 类
- [ ] AI 生成内容先写入 `omega-workspace/review/`（候审区）
- [ ] 6 项自动检查：min_length / has_frontmatter / has_sections / no_hallucination_markers / has_source_attribution / not_duplicate
- [ ] quality_score ≥ 5/6 → auto_approved（自动合并）
- [ ] quality_score < 0.5 → 标记需要人工审查
- [ ] `omega review list` 列出候审区
- [ ] `omega review approve <id>` 手动批准
- [ ] `omega review reject <id>` 拒绝
- [ ] 自动批准的内容由 knowledge_steward 合并到正式 wiki/
- [ ] `tests/test_kb_guard.py` 全部通过

### 11.7 基准预言机（Benchmark Oracle）
- [ ] `app/executor/benchmark_oracle.py` — `BenchmarkOracle` 类
- [ ] 加载 `config/benchmark_oracle.yaml` 配置（闭环 × 金标准映射）
- [ ] `run_closed_loop(loop_id)` 运行指定闭环并采集 6 维质量指标
- [ ] 6 维指标：statistical_correctness / citation_completeness / hallucination_score / human_edit_distance / reproducibility / file_existence
- [ ] `run_all()` 运行全部闭环
- [ ] `generate_deviation_report()` 生成偏差报告（预期 vs 实际）
- [ ] `compare_versions(loop_id)` 跨版本质量趋势对比
- [ ] `calibrate(loop_id)` 自动校准闭环阈值
- [ ] `omega oracle run --loop 1` 运行并对比金标准
- [ ] `omega oracle report` 生成偏差报告
- [ ] `omega oracle compare --loop 3` 版本对比
- [ ] `tests/test_benchmark_oracle.py` 全部通过

### 11.8 闭环预言机金标准数据
- [ ] `fixtures/gold_standard/closed_loop_1.json` 存在（文献检索金标准）
- [ ] `fixtures/gold_standard/closed_loop_3.json` 存在（数据分析金标准）
- [ ] `fixtures/gold_standard/closed_loop_5.json` 存在（PPT 生成金标准）
- [ ] 金标准文件含：expected_prose / expected_data / expected_output_files / acceptable_deviation
- [ ] 金标准数据覆盖核心闭环（≥3 个闭环）

### 11.9 综合验证
- [ ] `pytest tests/test_simulator.py tests/test_flight_recorder.py tests/test_provenance.py tests/test_budget.py tests/test_quarantine.py tests/test_kb_guard.py tests/test_benchmark_oracle.py tests/test_ecp.py` 全部通过
- [ ] `omega bench --all` 通过率 ≥ 90%
- [ ] `omega simulate phase-2` 不修改任何文件
- [ ] `omega flightlog <task_id>` 显示之前任务的完整审计
- [ ] `omega oracle run --all` 全部闭环通过金标准对比（偏差 ≤ acceptable_deviation）
- [ ] `omega oracle report` 无 CRITICAL 偏差

---

## 升级完成总验收（v1.0.0-full）

- [ ] `omega --version` 返回 `omega v1.0.0-full`
- [ ] `omega status` 显示所有服务健康（含 MCP + Web + 后台）
- [ ] `omega bench --all` 通过率 ≥ 90%
- [ ] `pytest tests/` 全部通过（预计 140+ tests）
- [ ] `mypy app/` 无新增类型错误
- [ ] `omega simulate phase-N` 对所有阶段均可生成模拟报告
- [ ] `omega quarantine list` 显示隔离区（应为空或仅有合法条目）
- [ ] `omega review list` 显示候审区（应为空或仅有待审内容）
- [ ] `omega oracle run --all` 全部闭环通过金标准对比
- [ ] `omega evolve list-ecps` 列出演化变更历史
- [ ] `omega local-engine status` 显示本地引擎状态
- [ ] 所有 API Key 在 `.env` 中，不在代码中
- [ ] `git log --oneline` 显示完整升级历史（Phase 2-11）
- [ ] 升级报告 `ITERATION_2_REPORT.md` ~ `ITERATION_11_REPORT.md` 全部存在

---

*清单版本：v2.1 — 2026-05-17*
*变更 v2.1：Phase 8 新增 ECP 审批流程验证项；Phase 11 新增基准预言机（11.7）和金标准数据（11.8）验证项；综合验证新增 oracle/ecp/local-engine 检查项；升级完成总验收新增 oracle/ecp/local-engine 检查项*
*变更 v2.0：新增 Phase 11（质量与安全加固——6 项安全特性），升级完成总验收增加模拟/隔离/审查检查项*
