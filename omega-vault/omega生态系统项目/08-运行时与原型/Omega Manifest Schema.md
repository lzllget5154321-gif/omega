---
type: concept
tags: [omega-ecosystem, manifest, schema, configuration, yaml]
created: 2026-05-15
updated: 2026-05-15
knowledge_stability: evolving
parent: [[omega.yaml]]
related:
  - [[Omega Runtime Architecture]]
  - [[Omega运行形态与本体文件说明]]
---

# Omega Manifest Schema

> **定位**：定义 `omega.yaml` 的完整字段 schema、默认值、约束和演进规则。运行时和工具均可参照此文档理解系统配置。

---

## 一、顶层结构

```yaml
omega:        # 系统身份
paths:        # 路径配置
runtime:      # 运行时配置
interfaces:   # 用户界面配置
memory:       # 记忆层配置
tools:        # 工具层配置
routing:      # 路由配置
planning:     # 规划器配置
safety:       # 安全策略
evolution:    # 进化配置
domains:      # 功能域配置
notifications:# 通知配置
logging:      # 日志配置
```

---

## 二、omega — 系统身份

| 字段 | 类型 | 必需 | 默认值 | 说明 |
|------|------|------|--------|------|
| `omega.name` | string | ✅ | — | 项目简称，如 "omega生态系统项目" |
| `omega.full_name` | string | ❌ | — | 完整英文名，如 "Omega Personal AI Action Ecology" |
| `omega.mode` | enum | ✅ | `function_first` | `function_first` / `safety_first` / `balanced` |
| `omega.owner` | string | ✅ | `user` | 系统所有者标识 |
| `omega.version` | string | ✅ | — | 当前版本号，如 "1.1" |
| `omega.description` | string | ❌ | — | 系统的一句话描述 |

---

## 三、paths — 路径配置

| 字段 | 类型 | 必需 | 默认值 | 说明 |
|------|------|------|--------|------|
| `paths.vault_path` | path | ✅ | `../omega-vault` | Obsidian Vault 的相对路径 |
| `paths.runtime_path` | path | ✅ | `.` | 运行时代码的根路径 |
| `paths.data_path` | path | ✅ | `../omega-data` | 数据库/日志/向量索引路径 |
| `paths.workspace_path` | path | ✅ | `../omega-workspace` | 任务工作区路径 |
| `paths.assets_path` | path | ✅ | `../omega-assets` | 媒体资产路径 |
| `paths.backups_path` | path | ❌ | `../backups` | 备份路径 |
| `paths.temp_path` | path | ✅ | `../omega-workspace/temp` | 临时文件（自动清理） |
| `paths.sandbox_path` | path | ✅ | `../omega-workspace/sandbox` | Docker 沙箱挂载目录 |
| `paths.outputs_path` | path | ✅ | `../omega-workspace/outputs` | 成果包输出目录 |

---

## 四、runtime — 运行时配置

| 字段 | 类型 | 必需 | 默认值 | 说明 |
|------|------|------|--------|------|
| `runtime.orchestrator` | enum | ✅ | `langgraph` | 任务编排框架：`langgraph` / `agents_sdk` / `custom` |
| `runtime.primary_executor` | enum | ✅ | `claude_code` | 主执行引擎：`claude_code` / `codex` / `local_agent` |
| `runtime.fallback_executor` | enum | ❌ | `codex` | 主执行器不可用时的备选 |
| `runtime.browser_automation` | enum | ✅ | `playwright` | 浏览器自动化：`playwright` / `puppeteer` / `selenium` |
| `runtime.sandbox` | enum | ✅ | `docker` | 沙箱引擎：`docker` / `firecracker` / `gvisor` |
| `runtime.sandbox_image` | string | ❌ | `omega-sandbox:latest` | Docker 镜像名 |
| `runtime.sandbox_memory_limit` | string | ❌ | `4GB` | 沙箱内存限制 |
| `runtime.sandbox_cpu_limit` | string | ❌ | `2` | 沙箱 CPU 核数限制 |
| `runtime.sandbox_timeout` | integer | ❌ | `600` | 沙箱超时（秒） |
| `runtime.max_concurrent_tasks` | integer | ❌ | `3` | 最大并发任务数 |
| `runtime.task_queue_backend` | enum | ❌ | `postgres` | 任务队列后端：`postgres` / `redis` / `memory` |

---

## 五、interfaces — 用户界面配置

| 字段 | 类型 | 必需 | 默认值 | 说明 |
|------|------|------|--------|------|
| `interfaces.cli.enabled` | boolean | ✅ | `true` | 启用 CLI 界面 |
| `interfaces.cli.entry_point` | string | ✅ | `omega` | CLI 入口命令名 |
| `interfaces.cli.commands` | list | ❌ | `[task, status, approve, radar, bench]` | 支持的命令列表 |
| `interfaces.web.enabled` | boolean | ❌ | `false` | 启用 Web 界面 |
| `interfaces.web.host` | string | ❌ | `127.0.0.1` | Web 服务绑定地址 |
| `interfaces.web.port` | integer | ❌ | `8420` | Web 服务端口 |
| `interfaces.web.auth` | enum | ❌ | `local_only` | 认证方式：`local_only` / `token` / `oauth` |
| `interfaces.daemon.enabled` | boolean | ❌ | `false` | 启用后台守护进程 |
| `interfaces.daemon.poll_interval` | integer | ❌ | `5` | 轮询间隔（秒） |
| `interfaces.daemon.auto_start` | boolean | ❌ | `false` | 开机自启 |

---

## 六、memory — 记忆层配置

| 字段 | 类型 | 必需 | 默认值 | 说明 |
|------|------|------|--------|------|
| `memory.obsidian.enabled` | boolean | ✅ | `true` | 启用 Obsidian 记忆 |
| `memory.zotero.enabled` | boolean | ✅ | `true` | 启用 Zotero 文献记忆 |
| `memory.qdrant.enabled` | boolean | ❌ | `false` | 启用 Qdrant 向量搜索（阶段 2） |
| `memory.postgres.enabled` | boolean | ❌ | `false` | 启用 PostgreSQL（阶段 2） |

---

## 七、tools — 工具层配置

| 字段 | 类型 | 必需 | 默认值 | 说明 |
|------|------|------|--------|------|
| `tools.registry` | path | ✅ | `./registries/tools.yaml` | 工具注册表路径 |
| `tools.mcp_config` | path | ❌ | `./mcp/mcp-config.json` | MCP 配置文件路径 |
| `tools.skills_path` | path | ✅ | `./skills` | Skill 实现目录 |
| `tools.workflows_path` | path | ✅ | `./workflows` | Workflow 定义目录 |
| `tools.core_adapters` | list | ✅ | — | MFE 阶段必需的工具适配器列表 |
| `tools.creative_adapters` | list | ❌ | — | 创意/可视化工具适配器（阶段 2+） |

---

## 八、routing — 路由配置

| 字段 | 类型 | 必需 | 默认值 | 说明 |
|------|------|------|--------|------|
| `routing.router` | string | ✅ | `tool_agent_router` | 路由器名称 |
| `routing.mode` | enum | ✅ | `static_then_scored` | 路由模式演进路径 |
| `routing.task_types` | path | ✅ | `./schemas/task-types.yaml` | 任务类型定义文件 |
| `routing.capabilities` | path | ✅ | `./schemas/capabilities.yaml` | 能力类型定义文件 |
| `routing.default_policy` | enum | ✅ | `function_first` | 默认选择策略 |
| `routing.scoring_dimensions` | list | ✅ | — | 评分维度及其权重 |

---

## 九、safety — 安全策略

| 字段 | 类型 | 必需 | 默认值 | 说明 |
|------|------|------|--------|------|
| `safety.principle` | string | ✅ | `risk_changes_path_not_goal` | 核心安全原则 |
| `safety.risk_levels.low.action` | enum | ✅ | `auto` | 低风险操作：自动执行 |
| `safety.risk_levels.medium.action` | enum | ✅ | `sandbox` | 中风险：沙箱执行 |
| `safety.risk_levels.high.action` | enum | ✅ | `confirm` | 高风险：等待确认 |
| `safety.risk_levels.critical.action` | enum | ✅ | `confirm_with_preview` | 极高风险：预览+确认 |
| `safety.forbidden` | list | ✅ | — | 绝对禁止的操作 |
| `safety.rollback.enabled` | boolean | ✅ | `true` | 启用回滚 |
| `safety.rollback.git_tracked_paths` | list | ✅ | — | Git 追踪的路径 |
| `safety.rollback.max_rollback_depth` | integer | ❌ | `10` | 最大回滚深度 |

---

## 十、evolution — 进化配置

| 字段 | 类型 | 必需 | 默认值 | 说明 |
|------|------|------|--------|------|
| `evolution.auto_evolve` | list | ✅ | — | 可自动执行的进化操作 |
| `evolution.confirm_evolve` | list | ✅ | — | 需用户确认的进化操作 |
| `evolution.forbidden_evolve` | list | ✅ | — | 禁止自动进化的操作 |

---

## 十一、domains — 功能域配置

每个功能域的配置格式：

| 字段 | 类型 | 必需 | 默认值 | 说明 |
|------|------|------|--------|------|
| `domains.<name>.enabled` | boolean | ✅ | — | 是否启用此功能域 |
| `domains.<name>.tools` | list | ✅ | — | 该域可用的工具列表 |
| `domains.<name>.agents` | list | ✅ | — | 该域可用的 Agent 列表 |

内置功能域：`academic_research`、`medical_research`、`data_analysis`、`scientific_visualization`、`creative_production`、`tool_learning`、`system_maintenance`

---

## 十二、notifications — 通知配置

| 字段 | 类型 | 必需 | 默认值 | 说明 |
|------|------|------|--------|------|
| `notifications.enabled` | boolean | ❌ | `false` | 全局通知开关 |
| `notifications.channels` | list | ❌ | — | 通知渠道列表 |

---

## 十三、logging — 日志配置

| 字段 | 类型 | 必需 | 默认值 | 说明 |
|------|------|------|--------|------|
| `logging.level` | enum | ❌ | `info` | 日志级别：`debug` / `info` / `warning` / `error` |
| `logging.format` | enum | ❌ | `structured` | 格式：`structured`（JSON）/ `human_readable` |
| `logging.rotation` | enum | ❌ | `daily` | 轮转策略：`daily` / `weekly` / `size` |
| `logging.retention_days` | integer | ❌ | `90` | 保留天数 |
| `logging.paths.agent_logs` | path | ❌ | — | Agent 日志路径 |
| `logging.paths.tool_logs` | path | ❌ | — | 工具日志路径 |
| `logging.paths.system_logs` | path | ❌ | — | 系统日志路径 |

---

## 十四、字段演进规则

1. **新增字段**：minor 版本升级（v1.1 → v1.2），向后兼容
2. **废弃字段**：先标记 `deprecated`，两个 minor 版本后移除
3. **修改字段语义**：major 版本升级（v1.x → v2.0）
4. **移除字段**：major 版本升级时清理

---

## 十五、相关页面

- [[omega.yaml]] — 实际配置文件
- [[Omega Runtime Architecture]] — 运行时架构设计
- [[Omega运行形态与本体文件说明]] — 系统形态定义
