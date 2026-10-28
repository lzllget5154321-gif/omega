# Omega 构建验收清单
# ================
# 每完成一个迭代，Codex 必须逐项检查。全部通过才能进入下一迭代。
# 如某项未通过，必须在进入下一迭代前修复。

## 迭代 0：骨架搭建

- [ ] `OMEGA_HOME` 已确定（默认 `D:\Omega-System`，可由用户自定义）
- [ ] `omega --version` 返回 `omega v0.1.0-mfe`
- [ ] `omega --help` 显示所有命令（task, status, approve, bench, radar）
- [ ] 从自定义 `OMEGA_HOME` 路径下 `omega status` 能正常解析 `omega.yaml`
- [ ] `.env` 文件存在且 `POSTGRES_PASSWORD` 非空；Codex 会话满足构建要求，运行时 provider 可 deferred
- [ ] `active_engines.yaml` 已生成（omega-runtime/config/），记录 available/deferred/unavailable_confirmed
- [ ] 已确认可用的 API 健康检查通过（按 active_engines.yaml 验证）
- [ ] 未提供的运行时 provider 已标记为 `deferred` 或 `unavailable_confirmed`（不阻塞构建）
- [ ] Codex 构建 Agent 不要求 `OPENAI_API_KEY`（当前运行时使用 user_session 凭据，不固定模型版本）
- [ ] `model_capabilities.yaml` 为唯一模型策略源，Agent/路由只绑定稳定 capability role
- [ ] 原生 Anthropic 账号/API 与 `api.anthropic.com` 被拒绝；NotebookLM 未进入任何活动路由
- [ ] 模型发现有 2 秒边界，未知 provider/model ID 与设置可无损往返
- [ ] 配置迁移先验证再原子替换，并保留上一版本；本地模型默认关闭
- [ ] `python build-package/scripts/package_gate.py --package build-package` 返回 `PACKAGE_GATE_PASS`（不得跳过对抗测试）
- [ ] `model_policy_runtime.py migrate/restore` 对未知 provider/model/嵌套字段/route history 无损往返；候选验证失败不产生替换或临时残留
- [ ] PowerShell 端点对抗门禁拒绝 `ANTHROPIC_API_KEY`、原生 Anthropic host 的端口/尾点/Unicode 点/百分号编码及所有兼容 endpoint 变量
- [ ] `omega.yaml` 存在且可被 `omega status` 正确解析
- [ ] `pyproject.toml` 中所有依赖版本号精确（不含 `>=` 范围）
- [ ] Python 虚拟环境已激活，`pip install -e .` 成功
- [ ] `git init` 已完成，`.gitignore` 存在且包含 `.env`
- [ ] 目录结构符合 `Omega 构建指导书 §2` 的完整定义
- [ ] 无任何密钥/Token/密码出现在代码文件中（grep 验证）

---

## 迭代 1：路由与规划

- [ ] `omega task "搜5篇SGLT2抑制剂的文献" --dry-run` 输出合法 JSON
- [ ] JSON 包含 `task_type`, `complexity`, `steps` 字段
- [ ] steps 数组中每个步骤包含 `stage`, `required_capabilities`, `selected_tool`, `fallback_tool`
- [ ] DAG 包含至少 3 个阶段，且依赖关系正确（无循环）
- [ ] `omega.yaml` 中 `routing.mode` 为 `static_then_scored`
- [ ] 冷启动路由表 `routing_table.yaml` 存在且含 12+ 任务类型（实际 16 种，与 task_contract.schema.json 一致）
- [ ] `config/tools.yaml` 中所有工具符合 `schemas/tool_card.schema.json`
- [ ] `config/agents.yaml` 中所有 Agent 符合 `schemas/agent_card.schema.json`
- [ ] `pytest tests/test_router.py tests/test_planner.py` 全部通过

---

## 迭代 2：执行与安全

- [ ] `docker compose up -d` 启动所有服务（postgres + qdrant + sandbox）
- [ ] `docker exec omega-postgres pg_isready -U omega` 返回 accepting connections
- [ ] `curl -s http://localhost:6333/collections` 返回合法 JSON
- [ ] Safety Enforcer 正确拒绝 `risk_level: critical` 任务的自动执行
- [ ] Safety Enforcer 正确拒绝裸 `os.system("del /F /S *")` 调用
- [ ] `omega-sandbox`（execution sandbox）容器内 `curl http://example.com` 失败（network_mode: none）
- [ ] `omega-sandbox-net`（toolsmith sandbox）容器内可访问 PyPI/npm/GitHub（有限网络）
- [ ] `omega task "分析 fixtures/data/sample_clinical.csv" --execute` 成功
- [ ] 语言引擎健康检查通过（按 active_engines.yaml 检查所有活跃引擎，至少一个引擎可用）
- [ ] 所有 API 调用使用环境变量中的 Key，未硬编码
- [ ] `pytest tests/` 全部通过

---

## 迭代 3：闭环验证（MFE-Alpha：4 核心闭环）

> **MFE 分层验收定义**（四层，以 `templates/BENCHMARK_CATALOG.yaml` 为唯一权威源）：
> | 层级 | 闭环数 | Catalog IDs | 对应阶段 |
> |------|--------|------------|---------|
> | **MFE-Alpha** | 4 | `literature_ingestion` `csv_analysis` `tool_comparison` `tool_gap_learning` | 迭代 0-3（Codex 初始构建） |
> | **MFE-Methodology** | 6 | `literature_ingestion` `pdf_deep_processing` `csv_analysis` `academic_writing` `tool_gap_learning` `browser_prefill` | MFE 构建完成后、升级前 |
> | **MFE-Plus** | 9 | Methodology 6 + `code_generation` `tool_comparison` `quality_improvement` | Phase 2-9 升级后 |
> | **Full-Core** | 12 | 全部 12 个 Full-Core 闭环 | Phase 2-11 升级完成后 |
> | **Full-Extended** | 13+ | Full-Core 12 + `knowledge_base_health` 等扩展闭环 | 持续演化 |
>
> 方法论以 `01-方法论/Omega 最终完整方法论.md` 为当前总纲；闭环口径由 `BENCHMARK_CATALOG.yaml` 唯一裁决。
> 构建包初始构建的 4 个闭环对应 **MFE-Alpha**（工程冷启动验证）。两者是分步递进关系。
> **所有闭环引用一律使用 catalog_id（字符串），禁止使用数字编号。**

- [ ] `literature_ingestion`（文献检索与知识摄取）：PDF → `wiki/来源/` 页面，含 quality + noise_ratio + credibility + knowledge_stability
- [ ] `csv_analysis`（CSV 数据分析与统计报告）：CSV → 统计分析 + 图表 PNG + Markdown 报告，统计量正确
- [ ] `tool_comparison`（工具对比分析）：生成 ≥8 维度对比的页面，每个维度有具体数据
- [ ] `tool_gap_learning`（工具自主学习）：在 omega-sandbox-net 中安装 + 在 omega-sandbox 中离线测试一个未知 CLI 工具 + 生成评估报告（双沙箱策略：有限网络安装 → 无网络验证）
- [ ] `omega bench --all` 通过率 ≥ 80%
- [ ] `omega status` 显示所有服务健康状态
- [ ] `omega radar` 输出有效 YAML（扫描外部工具生态）
- [ ] `wiki/log.md` 记录了所有操作（追加模式）
- [ ] `wiki/index.md` 正确更新（Stats 与实际文件数一致）
- [ ] 🆕 记录 MFE-Alpha 验收状态到 `BUILD_STATE.md`（标注"MFE-Alpha 4/4 通过，待升级至 MFE-Methodology 6/6"）
