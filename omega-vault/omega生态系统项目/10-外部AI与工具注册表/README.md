# 10-外部AI与工具注册表

> 本目录是 Omega 系统的**外部世界能力目录**——记录每个外部 AI 平台、工具、API、MCP Server 的详细档案，让系统在任务路由和工具选择时有据可查。

## 为什么需要这个目录

用户的初心是：
> "AI 工具太多，我需要 Omega 替我学习和管理它们。"

这个目录就是这个需求的直接实现——它不是方法论描述，而是**可查询的结构化数据库**，记录每个工具的：
- 能力、限制、适用场景
- API 方式、成本、上下文窗口
- 在 Omega 中的接入状态和路由位置
- 与其他工具的替代/互补关系

## 注册表格式

每个工具一个 Markdown 文件，遵循标准模板（见 [[AI工具生态雷达]] 第四节）：

```markdown
---
type: entity
tags: [external-ai, tool-registry, <category>]
radar_status: integrated | investigating | watching | deprecated
category: model | agent_platform | mcp_server | cli_tool | api | platform
---

# <工具名称>

## 基本信息
## 核心能力
## 技术规格
## 在 Omega 中的适用场景
## 接入方式
## 限制与注意事项
## 替代工具
## 相关 Omega 组件
```

## 必须首批注册的核心工具

### AI 模型

| 工具 | 文件 | 优先级 |
|------|------|--------|
| Claude (Anthropic API) | `Claude.md` | P0 |
| ChatGPT / GPT-4 (OpenAI) | `ChatGPT-GPT4.md` | P0 |
| Gemini (Google) | `Gemini.md` | P1 |

### Agent / CLI 工具

| 工具 | 文件 | 优先级 |
|------|------|--------|
| Claude Code | `Claude-Code.md` | P0 |
| Codex CLI | `Codex-CLI.md` | P0 |
| Aider | `Aider.md` | P2 |

### 外部研究平台

| 工具 | 文件 | 优先级 |
|------|------|--------|
| NotebookLM | `NotebookLM.md` | P0 |
| Deep Research | `Deep-Research.md` | P0 |
| Perplexity | `Perplexity.md` | P1 |

### 自动化工具

| 工具 | 文件 | 优先级 |
|------|------|--------|
| Playwright | `Playwright.md` | P0 |
| agent-browser | `agent-browser.md` | P1 |

### 知识/数据平台

| 工具 | 文件 | 优先级 |
|------|------|--------|
| Obsidian | `Obsidian.md` | P0 |
| Zotero | `Zotero.md` | P0 |
| Qdrant | `Qdrant.md` | P1 |
| PubMed | `PubMed.md` | P0 |
| Semantic Scholar | `Semantic-Scholar.md` | P1 |
| Docker | `Docker.md` | P1 |

## 注册表维护

- **新增**：AI 工具生态雷达发现 → 评估通过 → 创建注册页
- **更新**：工具重大版本更新 → 更新注册页
- **退役**：工具被弃用 → 标记 `radar_status: deprecated`

## 与其他目录的关系

- `03-能力矩阵/AI工具生态雷达.md` — 定义监控和评估机制
- `02-架构/Tool-Agent Router` — 查询注册表做路由决策
- `02-架构/Capability Fabric` — 注册表是 Adapter 创建的前置评估层
