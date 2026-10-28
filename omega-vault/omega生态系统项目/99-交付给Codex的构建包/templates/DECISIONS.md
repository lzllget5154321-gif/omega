# Omega Build — Key Decisions Log

> **Supersession notice（2026-08-23）**：本文件在 2026-08-23 之前关于 Claude-first、固定 GPT 版本、DeepSeek-first 或自动本地回退的条目仅为不可变历史记录，不再是活动配置。当前唯一有效模型决策是文末“Codex-first 能力角色与原子模型迁移”及 `config/model_capabilities.yaml`。

> **由构建 Agent 自动维护。** 记录构建过程中的关键决策。
> 构建 Agent 重启后读取此文件，了解之前的设计意图。
> 此文件放在 `omega-runtime/DECISIONS.md`。

---

## 决策格式

每条决策记录以下信息：

```markdown
### YYYY-MM-DD HH:MM — <决策标题>

- **背景**：为什么需要做这个决定？
- **考虑的选项**：
  - A: <选项 A 描述>
  - B: <选项 B 描述>
  - C: <选项 C 描述>
- **决定**：选择了哪个选项，核心理由是什么
- **影响范围**：这个决定影响哪些模块/文件
- **可逆性**：可逆 / 不可逆（如果可逆，什么条件下可以改）
- **相关文件**：受影响的文件列表
```

---

## 构建前已知的关键决策

### 2026-05-15 — MFE 阶段只验证 4 个核心闭环

- **背景**：完整 Omega 定义了 12 个基准闭环，但 MFE 阶段资源有限
- **考虑的选项**：
  - A: 实现全部 12 个闭环（过于庞大，MFE 无法完成）
  - B: 实现 4 个核心闭环（文献摄取、数据分析、工具对比、工具学习）
  - C: 实现 6 个闭环（边界模糊，目标不明确）
- **决定**：选项 B — 4 个核心闭环覆盖了 Omega 的感知、分析、对比、学习四大核心能力
- **影响范围**：迭代 3 验收范围、BUILD_CHECKLIST.md、验收测试数据
- **可逆性**：可逆 — 阶段 2 追加其余 8 个闭环
- **相关文件**：AGENTS.md §5, CODEX_RUN_PROMPT.md, BUILD_CHECKLIST.md 迭代 3

### 2026-05-15 — 分层降级架构：Claude Tier 0 → DeepSeek Tier 1 → GPT-4 Tier 2

- **背景**：用户可能无法获取某些国外 AI 厂商 Key，但不应因此限制系统功能上限。需要一种既保留最佳引擎选项、又能在 Key 不可用时自动降级的架构。
- **考虑的选项**：
  - A: 绝对国内适配——所有路由指向 DeepSeek，国外引擎全部标记不可用（牺牲功能上限，用户明确反对）
  - B: 完全自由选择——所有引擎平级，用户自行配置（缺乏降级逻辑，一个 Key 缺失即阻塞）
  - C: 分层降级——Tier 0 Claude（最佳质量）→ Tier 1 DeepSeek（高性价比，国内平台）→ Tier 2 GPT-4（兜底），部署时按 api_tiers.yaml 协议询问用户，逐层降级
- **决定**：选项 C — 功能最大化优先。Claude 作为质量敏感任务首选（学术写作/证据评估/审查），DeepSeek 作为成本敏感任务首选（检索/提取/分析）。任何一层可用都能完整运行 Omega，差异仅在质量和成本。部署时 Codex 按 api_tiers.yaml 逐层询问用户，确认后生成 active_engines.yaml
- **影响范围**：全局——api_tiers.yaml（新增）、engine_resolution.yaml（重写）、routing_table.yaml（重写）、agents.yaml（重写）、tools.yaml（恢复）、.env.example（重写）、AGENTS.md、BUILD_CHECKLIST.md、CODEX_RUN_PROMPT.md、README.md、USER_ACTIONS.md
- **可逆性**：可逆 — 阶段 2 可在 engine_resolution.yaml 中追加更多引擎（通义千问/智谱/月之暗面/Gemini），层级可调整
- **相关文件**：config/api_tiers.yaml, config/engine_resolution.yaml, config/routing_table.yaml, config/agents.yaml, config/tools.yaml, config/.env.example

### 2026-05-15 — 功能最佳优先的交互式分层降级（非绝对国内-only）

- **背景**：用户可能无法获取某些国外 AI 厂商 Key，但"绝对国内适配"牺牲了功能上限。用户明确要求：先追求最佳引擎，部署时逐项确认 API，可用就启用，不可用才降级。
- **考虑的选项**：
  - A: 绝对国内-only — 所有路由指向 DeepSeek，国外引擎全部不可用（牺牲功能上限）
  - B: 功能最佳优先 — 先问 Claude/OpenAI/Perplexity/Brave，再确认 DeepSeek/国内平台。用户每项回答 Y（可用）/ L（deferred 稍后）/ N（unavailable_confirmed 降级）
- **决定**：选项 B — 部署时 Codex 按 api_tiers.yaml 协议逐层询问，生成 active_engines.yaml 记录三态（available/deferred/unavailable_confirmed）。匹配 4 种 deployment profiles（full_power/balanced/domestic_enhanced/minimal）
- **影响范围**：api_tiers.yaml（新增 deploy_options 三态选择）、deployment_profiles.yaml（新增）、active_engines.yaml（新增）、engine_resolution.yaml（扩展 6 级降级链）、.env.example（[BEST-OPTIONAL]/[RECOMMENDED]/[OPTIONAL-DOMESTIC]标记）
- **可逆性**：可逆 — 用户随时运行 `omega api-status --update` 更新 API 可用性，重新生成 active_engines.yaml
- **相关文件**：config/api_tiers.yaml, config/deployment_profiles.yaml, templates/active_engines.yaml, config/engine_resolution.yaml, config/.env.example

### 2026-05-15 — OMEGA_HOME 路径参数化（不再硬编码 D:\Omega-System）

- **背景**：v2.5 及之前所有路径硬编码为 D:\Omega-System，用户如部署到其他 D 盘目录需要全局查找替换
- **决定的选项**：所有硬编码路径改为 OMEGA_HOME 变量（默认 D:\Omega-System），setup.ps1 新增 -OmegaHome 参数，所有文档路径用 {OMEGA_HOME} 占位符。Codex 构建前先确认 OMEGA_HOME
- **影响范围**：setup.ps1、AGENTS.md、CODEX_RUN_PROMPT.md、README.md、USER_ACTIONS.md、mcp-config.json、tools.yaml（filesystem_mcp）
- **可逆性**：可逆——只是路径引用方式改变，不影响系统功能
- **相关文件**：scripts/setup.ps1, templates/mcp-config.json, config/tools.yaml, AGENTS.md, CODEX_RUN_PROMPT.md, README.md, USER_ACTIONS.md

### 2026-05-15 — 双沙箱策略：无网络执行 + 有限网络安装

- **背景**：安全性要求沙箱无网络，但工具学习需要网络安装依赖
- **考虑的选项**：
  - A: 单一沙箱，允许网络（不安全）
  - B: 单一沙箱，禁止网络（无法安装工具）
  - C: 双沙箱——omega-sandbox（无网络执行）+ omega-sandbox-net（有限网络安装）
- **决定**：选项 C — 双沙箱分工明确，安装后转移到无网络沙箱验证
- **影响范围**：docker-compose.yml, Dockerfile.sandbox, Dockerfile.sandbox-net, sandbox-net-filter.sh
- **可逆性**：可逆 — 阶段 2 可合并为单一强化沙箱
- **相关文件**：templates/docker-compose.yml, templates/Dockerfile.sandbox, templates/Dockerfile.sandbox-net, scripts/sandbox-net-filter.sh

---

## 构建过程中新增的决策

<!-- 构建 Agent 在此追加新决策 -->

### 2026-08-23 — Codex-first 能力角色与原子模型迁移

- **背景**：原配置把 Claude/DeepSeek/固定模型版本直接写进 Agent 与路由，产品升级时会引发全量配置重写；原生 Anthropic 账号不可用，NotebookLM 已排除。
- **决定**：`model_capabilities.yaml` 成为单一真相源。Codex 当前会话为构建主链，OpenAI 为运行时次主，OpenRouter/国产 Claude Messages 仅备用，国产 OpenAI-compatible 后续备用，本地模型仅显式灾备。禁止原生 Anthropic 与 `api.anthropic.com`。
- **迁移契约**：运行时以 2 秒边界发现模型；具体模型 ID 不写入 Agent/工作流；未知 provider/model ID、设置和历史原样保留。候选配置先验证，再原子替换，并保留上一文件供回滚。
- **兼容性**：`gpt4_api`、`claude_api`、`claude_code` 仅作为历史兼容别名；别名不得选择原生 Anthropic transport，也不重写旧收据。
- **相关文件**：config/model_capabilities.yaml, config/engine_resolution.yaml, config/api_tiers.yaml, config/agents.yaml, config/routing_table.yaml, templates/active_engines.yaml
