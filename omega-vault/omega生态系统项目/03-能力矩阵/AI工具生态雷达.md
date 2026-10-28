---
type: concept
tags: [omega-ecosystem, ai-tool-radar, tool-monitoring, capability-tracking, external-platforms, tool-registry]
created: 2026-05-15
updated: 2026-05-15
knowledge_stability: evolving
parent: [[Omega生态系统项目-功能优先总方法论]]
related:
  - [[Capability Fabric]]
  - [[Toolsmith-Lite与Skillsmith]]
  - [[Tool Reputation Ledger]]
  - [[Tool-Affordance Graph]]
  - [[Tool-Agent Router：最佳工具与最佳执行者选择器]]
  - [[自我解惑与外援调用循环]]
---

# AI 工具生态雷达

> **定位**：AI 工具生态雷达（AI Tool Radar）是 Omega 系统的**外部工具世界持续监控层**。它的职责不是使用工具——那是 Capability Fabric 和 Toolsmith-Lite 的事。它的职责是**持续发现、追踪、评估外部 AI 世界中出现的新模型、新 Agent 平台、新 Skill、新 MCP Server、新自动化工具**，让 Omega 永远不会"不知道外面有什么新东西可用"。

---

## 一、为什么需要 AI 工具生态雷达

### 1.1 原始动机

用户最初设计 Omega 的核心动机之一就是：

> "AI 大模型、Agent、Skill、新平台、新方法太多，我跟不上。Omega 要替我持续学习它们，并在任务中自动选择最适合的。"

现有方法论中，Toolsmith-Lite 负责"系统遇到能力缺口时去找工具"——这是**被动响应**。AI 工具生态雷达负责"系统持续扫描外部世界，提前发现可能有用的工具"——这是**主动监控**。

两者互补：雷达提供"你可能需要关注的新工具"列表，Toolsmith-Lite 在任务中验证和封装它们。

### 1.2 设计哲学

```
被动模式（当前 Toolsmith-Lite）：
  任务失败 → 发现缺工具 → 搜索 → 找到 → 学习

主动模式（AI 工具生态雷达）：
  持续扫描 → 发现新工具 → 评估 → 注册 → 预学习
                                         ↓
                              任务需要时 → 直接可用（或只需轻量验证）
```

---

## 二、监控范围

### 2.1 七大类监控对象

| # | 类别 | 监控内容 | 为什么重要 |
|---|------|---------|-----------|
| 1 | **新 AI 模型** | 新发布的大语言模型、嵌入模型、多模态模型 | 模型升级可能替代多个工具或 Agent |
| 2 | **新 Agent 平台** | 新 Agent 框架、自主 Agent 平台、多 Agent 编排工具 | 可能成为更好的"执行者"或"协调者" |
| 3 | **新 MCP Server** | Model Context Protocol 服务器——数据库、API、文件系统连接器 | 直接扩展 Capability Fabric 的工具池 |
| 4 | **新 CLI/自动化工具** | Claude Code、Codex CLI、Aider、Open Interpreter 等 | 可能直接接入成为系统执行引擎 |
| 5 | **新 Skill/Workflow 模式** | 社区分享的 Agent Skill 模式、Prompt 工程模式 | 可复用的"怎么做"知识 |
| 6 | **新 API 和平台** | LLM API 新功能、RAG 平台新能力、浏览器自动化新工具 | 扩展系统可操作的外部世界边界 |
| 7 | **工具退役/弃用** | 旧工具停止维护、API 下线、安全漏洞公开 | 防止系统依赖已失效的工具 |

### 2.2 具体监控源

| 监控源 | 扫描内容 | 频率 | 工具 |
|--------|---------|------|------|
| **GitHub Trending** | 每日/每周热门 AI/Agent 仓库 | 每日 | GitHub API / RSS |
| **PyPI 新包** | 关键词 "agent"/"llm"/"mcp"/"rag"/"skill" 的新包 | 每周 | PyPI JSON API |
| **npm 新包** | 关键词 "agent"/"llm"/"mcp" 的新包 | 每周 | npm Registry API |
| **MCP Hub** | 新注册的 MCP Server | 每周 | MCP Hub 网站 / 社区列表 |
| **Hacker News** | AI/Agent 相关的热门讨论 | 每日 | HN API (algolia) |
| **Reddit r/LocalLLaMA, r/ClaudeAI, r/MachineLearning** | 新工具/新模型讨论 | 每周 | Reddit API |
| **arXiv cs.AI / cs.CL** | Agent 系统、工具使用、LLM 相关论文 | 每日 | arXiv API |
| **Twitter/X 关键账号** | 关注 Anthropic、OpenAI、LangChain、CrewAI 等官方账号 | 每日 | RSS/API（如有） |
| **YouTube 技术频道** | AI Agent 工具评测、教程 | 每周 | YouTube API |
| **Anthropic/OpenAI/Google 官方博客** | 产品更新、API 变更、新模型发布 | 每日 | RSS / Web Scraping |
| **Tool Reputation Ledger** | 已注册工具的维护状态变更 | 每周 | 内部数据库 |
| **PyPI/npm 包弃用公告** | 关键依赖的 deprecation 警告 | 每周 | 依赖扫描 |

---

## 三、雷达工作流程

### 3.1 主循环

```
┌─────────────────────────────────────────────────────────┐
│                  AI 工具生态雷达 — 主循环                   │
│                                                           │
│  ① 监控（Monitor）                                        │
│     ├── 定时任务：每日（GitHub/HN/arXiv/官方博客)         │
│     └── 定时任务：每周（PyPI/npm/MCP Hub/Reddit/YouTube） │
│                                                           │
│  ② 筛选（Filter）                                         │
│     ├── 关键词匹配：agent / mcp / skill / tool-use       │
│     ├── 社区热度：Star/Upvote/讨论量 阈值过滤             │
│     ├── 相关性评估：是否与 Omega 的工具需求匹配？          │
│     └── 去重：已在 Capability Fabric 或 Tool Registry    │
│                                                           │
│  ③ 摘要（Summarize）                                      │
│     ├── 自动生成工具摘要卡（名称/用途/能力/限制/链接）    │
│     ├── 标注发现来源和发现时间                            │
│     └── 初评：看起来有用 / 可能有潜力 / 暂不关注          │
│                                                           │
│  ④ 注册（Register）                                       │
│     ├── 写入外部AI与工具注册表（结构化 YAML/Markdown）    │
│     ├── 标记为 "radar: detected"                         │
│     └── 如果看起来特别有用 → 标记为 "radar: investigate" │
│                                                           │
│  ⑤ 深度评估（Deep Evaluate）——对 "investigate" 标记的工具 │
│     ├── 读文档 / README / 论文                            │
│     ├── 沙箱安装和试跑（Toolsmith-Lite 调用）             │
│     ├── 评估与现有工具的互补性/替代性                      │
│     └── 写入 Tool Reputation Ledger（初始信誉）           │
│                                                           │
│  ⑥ 入库（Integrate）——对评估通过的工具                     │
│     ├── 创建 Tool Adapter → 注册到 Capability Fabric      │
│     ├── 更新 Tool-Affordance Graph                       │
│     ├── 如有高频使用场景 → 封装为 Skill 候选              │
│     └── 标记为 "radar: integrated"                       │
│                                                           │
│  ⑦ 定期报告（Weekly Radar Report）                        │
│     ├── 本周值得关注的新工具 top-5                        │
│     ├── 本周深度评估结果                                  │
│     ├── 本周入库的新工具                                  │
│     └── 退役/弃用提醒                                    │
│                                                           │
│  ⑧ 退役追踪（Sunset Tracker）                             │
│     ├── 已注册工具的维护状态监控                          │
│     ├── 弃用警告 → 建议替代方案                           │
│     └── 标记 "radar: deprecated" + 通知用户              │
│                                                           │
└─────────────────────────────────────────────────────────┘
```

### 3.2 工具摘要卡格式

每个被雷达发现的工具生成标准摘要卡：

```yaml
tool_radar_entry:
  name: "Open Interpreter"
  category: agent_platform  # model / agent_platform / mcp_server / cli_tool / skill_pattern / api / platform
  radar_status: detected  # detected → investigating → integrated → deprecated
  discovered_at: 2026-05-15
  discovered_from: "GitHub Trending (weekly)"
  
  summary:
    what_it_is: "开源桌面 Agent，可以执行 Python/JS/Shell 代码并控制电脑"
    key_capabilities:
      - "本地代码执行（Python/JS/Shell）"
      - "文件系统操作"
      - "浏览器控制（Playwright）"
      - "多模型后端（Claude/GPT/本地模型）"
    limitations:
      - "仅限本地执行，无远程 Agent 协调"
      - "安全模型较宽松，默认允许较多操作"
    relevance_to_omega: high  # high / medium / low / none
    potential_use:
      - "可替代 Coder Agent 的代码执行后端"
      - "增强 Computer Use-Lite 的本地操作能力"

  technical_specs:
    install_method: "pip install open-interpreter"
    api_type: "CLI + Python SDK"
    supported_models: [claude, gpt-4, gpt-4o, llama3]
    cost: free  # free / freemium / paid / api_pricing
    license: AGPL-3.0
    active_maintenance: true
    last_release: 2026-04-28

  initial_assessment:
    maturity: beta  # alpha / beta / stable / mature
    community_size: 52k GitHub stars
    ecosystem_fit: "可能补充 Capability Fabric 的本地代码执行层"
    conflict_with_existing: ["Coder Agent 的代码执行部分"]
    recommended_action: investigate  # skip / watch / investigate / integrate
    investigation_priority: medium  # low / medium / high / critical
```

---

## 四、外部 AI 与工具注册表

### 4.1 注册表结构

`10-外部AI与工具注册表/` 目录中的每个文件代表**一个外部 AI 平台或关键工具**，格式如下：

```markdown
---
type: entity
tags: [external-ai, tool-registry, <category>]
radar_status: integrated
first_discovered: YYYY-MM-DD
last_updated: YYYY-MM-DD
category: model | agent_platform | mcp_server | cli_tool | skill_pattern | api | platform
---

# <工具/平台名称>

## 基本信息
- **类型**：大语言模型 / Agent 框架 / MCP Server / ...
- **开发者**：Anthropic / OpenAI / 社区 / ...
- **官网**：https://...
- **文档**：https://...
- **定价**：免费 / API 按量 / 订阅 / ...

## 核心能力
- 能力 1：...
- 能力 2：...

## 技术规格
- **API 方式**：REST / SDK / CLI / MCP / ...
- **支持模型**：Claude / GPT / ...
- **上下文窗口**：200K tokens
- **输入格式**：文本 / 图片 / 文件 / ...
- **输出格式**：文本 / 代码 / JSON / ...

## 在 Omega 中的适用场景
- 场景 1：何时使用这个工具
- 场景 2：...

## 接入方式
- **当前接入状态**：已接入 / 待接入 / 评估中
- **接入层**：Capability Fabric / Computer Use-Lite / Perception Mesh / ...
- **调用方式**：CLI / SDK / API / MCP

## 限制与注意事项
- 限制 1：...
- 注意事项：...

## 替代工具
- [[替代工具A]] — 在 X 场景下可替代
- [[替代工具B]] — 在某些约束下更好

## 相关 Omega 组件
- [[Tool-Agent Router]] 中的路由位置
- [[Tool Reputation Ledger]] 中的信誉记录
- [[Capability Fabric]] 中的 Adapter
```

### 4.2 必须首批注册的核心外部 AI/工具

| 工具/平台 | 类别 | 注册优先级 | 原因 |
|----------|------|-----------|------|
| **Claude (Anthropic API)** | model | P0 | Omega 的核心语言引擎 |
| **Claude Code** | cli_tool | P0 | Python/Bash 执行 + 工具编排 |
| **OpenAI ChatGPT / GPT-4** | model | P0 | 备选语言引擎 |
| **OpenAI Codex CLI** | cli_tool | P0 | 备选代码执行引擎 |
| **Google NotebookLM** | platform | P0 | 多文献 RAG 综合 |
| **Deep Research** | platform | P0 | 深度多轮搜索 |
| **Perplexity** | platform | P0 | 实时信息查询 |
| **Playwright** | cli_tool | P1 | 浏览器自动化 |
| **Obsidian** | platform | P1 | 知识库存储 + 前端 |
| **Zotero** | platform | P1 | 文献管理 |
| **Qdrant** | platform | P1 | 语义搜索 |
| **Docker** | platform | P1 | 代码沙箱 |
| **GitHub (API + Platform)** | api | P1 | 代码搜索 + 工具发现 |
| **PubMed E-utilities** | api | P1 | 学术文献检索 |
| **Semantic Scholar** | api | P1 | 学术文献检索 |
| **PyPI** | platform | P2 | Python 包管理 |
| **MCP 服务器生态** | mcp_server | P2 | 工具协议扩展 |

---

## 五、雷达报告格式

### 5.1 周度雷达报告

每周自动生成（或用户说"本周有什么新工具"时按需生成）：

```markdown
# AI 工具生态雷达周报 — 2026-W21

> 扫描时间：2026-05-15 至 2026-05-21
> 扫描来源：GitHub / PyPI / npm / Hacker News / arXiv / MCP Hub / Reddit / 官方博客
> 本周共发现 X 个新项目，其中 top-5 值得关注

---

## 🔥 本周 Top-5

### 1. [工具名称] — ⭐ XXXX GitHub Stars
- **是什么**：一句话描述
- **为什么关注**：对 Omega 的潜在价值
- **主要能力**：...
- **行动建议**：investigate / watch / skip
- → 详细信息：[[10-外部AI与工具注册表/工具名称]]

### 2. ...

---

## 📊 本周统计

| 类别 | 发现 | 标记 investigate | 入库 | 弃用 |
|------|------|:--:|:--:|:--:|
| 新 AI 模型 | 3 | 1 | 0 | 0 |
| Agent 平台 | 2 | 1 | 0 | 0 |
| MCP Server | 5 | 2 | 1 | 0 |
| CLI 工具 | 4 | 0 | 0 | 1 |
| Skill 模式 | 1 | 0 | 0 | 0 |
| API/平台 | 2 | 0 | 0 | 0 |

---

## 🟢 本周入库的新工具

| 工具 | 接入层 | 用途 |
|------|--------|------|
| X | Capability Fabric | ... |

---

## 🟡 本周标记 investigate 的工具

| 工具 | 优先级 | 评估方向 |
|------|--------|---------|
| Y | high | 可能替代 Z 工具 |

---

## 🔴 弃用提醒

| 工具 | 原因 | 建议替代 |
|------|------|---------|
| A | 停止维护 | [[B]] |

---

## 📖 值得阅读的行业动态

- Anthropic 发布 Claude 4.x 新功能：...
- OpenAI 宣布 XXX：...
- MCP 协议更新到 vX：...
```

---

## 六、工具退役追踪

### 6.1 退役信号

| 信号 | 严重级别 | 响应 |
|------|---------|------|
| GitHub 仓库 archived / 超过 6 个月无 commit | 🟡 预警 | 标记为 watch，开始寻找替代 |
| 官方公告停止维护（EOL） | 🟠 警告 | 立即搜索替代工具，通知用户 |
| 发现严重安全漏洞（CVE High/Critical） | 🔴 危险 | 立即暂停使用，评估风险，紧急替换 |
| API 服务下线 | 🔴 紧急 | 自动切换到 fallback 工具，通知用户 |
| 许可证变更（从开源变为商业） | 🟡 预警 | 评估影响，通知用户 |
| 被更好的工具明显超越 | 🟢 提示 | 在周报中建议评估升级 |

### 6.2 退役处理协议

```
检测到退役信号
  │
  ├── 步骤 1：确认退役事实
  │     └── 交叉验证（官方公告 + GitHub 状态 + 社区讨论）
  │
  ├── 步骤 2：影响评估
  │     ├── Capability Fabric 中有哪些 Adapter 依赖此工具？
  │     ├── Skill Library 中有哪些 Skill 依赖此工具？
  │     ├── Workflow 中有哪些流程使用此工具？
  │     └── Action Memory 中此工具的使用频率？
  │
  ├── 步骤 3：寻找替代
  │     ├── Tool-Affordance Graph 中查找同能力类型的其他工具
  │     ├── AI工具生态雷达中查找是否已有候选
  │     └── 如果没有 → 触发 Toolsmith-Lite 搜索
  │
  ├── 步骤 4：过渡计划
  │     ├── 低影响（仅预警级别）→ 在周报中提示用户
  │     ├── 中影响（警告级别）→ 自动准备替代方案 + 通知用户确认
  │     └── 高影响（危险/紧急级别）→ 立即暂停 + 自动切换到 fallback + 紧急通知
  │
  └── 步骤 5：执行退役
        ├── 更新 Capability Fabric（标记 Adapter 为 deprecated）
        ├── 更新 Skill Library（标记依赖 Skill）
        ├── 更新 Tool Reputation Ledger
        └── 写入 Action Memory（记录替换过程）
```

---

## 七、与其他组件的接口

### 7.1 数据流

```
AI工具生态雷达（持续监控）
  │
  ├── 发现新工具 → AI工具注册表（10-外部AI与工具注册表/）
  │
  ├── 标记 investigate → Toolsmith-Lite（沙箱试用）
  │                           │
  │                           └── 评估通过 → Capability Fabric（注册 Adapter）
  │                                        → Tool Reputation Ledger（初始信誉）
  │                                        → Tool-Affordance Graph（能力节点）
  │
  ├── 发现优质工具模式 → Skill Library（Skill 候选）
  │
  ├── 周度报告 → Ω 行动中枢（用户可见）
  │
  └── 退役信号 → Safety-as-Enabler（紧急暂停）
                → Tool-Agent Router（更新路由表）
```

### 7.2 上游依赖

| 组件 | 提供的功能 |
|------|-----------|
| [[Perception Mesh]] | Web 搜索、API 调用、RSS 监控 |
| [[Toolsmith-Lite与Skillsmith]] | 工具的沙箱试用和评估 |
| [[Tool Reputation Ledger]] | 已有工具的维护状态查询 |

### 7.3 下游输出

| 组件 | 接收的输出 |
|------|-----------|
| [[Capability Fabric]] | 新工具 Adapter 的注册 |
| [[Tool-Affordance Graph]] | 新工具的能力节点和边 |
| [[Tool-Agent Router：最佳工具与最佳执行者选择器]] | 路由表的更新（新工具的评分数据） |
| [[自我解惑与外援调用循环]] | 缺工具时的候选工具搜索范围 |
| [[Ω行动中枢]] | 周度雷达报告 + 弃用提醒 |
| [[Evolution Loop]] | 工具替换建议（旧工具退役 → 新工具替代） |

---

## 八、主动预学习队列（Pre-Learning Queue）

> 雷达不仅要发现工具，还要让 Omega **不等任务失败就提前学好**可能有用的工具。

### 8.1 预学习队列逻辑

```
雷达发现新工具
  │
  ├── 1. 快速匹配
  │     ├── 该工具的能力是否与 Omega 当前功能域相关？
  │     ├── 该工具是否填补了已知的能力缺口？
  │     └── 该工具是否可能替代当前使用的低信誉工具？
  │
  ├── 2. 优先级排序
  │     ├── Critical: 填补已知的能力缺口 → 立即进入队列
  │     ├── High: 与高频任务类型匹配 → 本周内进入队列
  │     ├── Medium: 与低频但重要的任务类型匹配 → 本月内
  │     └── Low: 有趣但不紧急 → 记录，等待手动触发
  │
  ├── 3. 进入预学习队列
  │     ├── 队列最大容量: 10 个工具（超出后按优先级淘汰）
  │     ├── 并行学习上限: 3 个（沙箱资源限制）
  │     └── 每个工具最大学习时间: 30 分钟
  │
  ├── 4. 自动预学习
  │     ├── 读取工具文档/README/论文
  │     ├── 在 Docker 沙箱中安装和试跑
  │     ├── 生成工具摘要卡（标准 YAML 格式）
  │     ├── 评估与现有工具的互补性/替代性
  │     ├── 如果值得接入 → 标记为 "radar: investigate"
  │     └── 如果不值得 → 标记为 "radar: watched" + 记录原因
  │
  └── 5. 学习成果入库
        ├── 工具摘要卡 → 10-外部AI与工具注册表/
        ├── 初始信誉 → Tool Reputation Ledger
        ├── 如果通过试用 → 触发 Toolsmith-Lite 深度评估
        └── 如果特别有价值 → 周报中高亮推荐
```

### 8.2 预学习队列优先级算法

```python
def calculate_prelearning_priority(tool: ToolRadarEntry) -> float:
    """计算工具的预学习优先级"""
    score = 0.0
    
    # 填补已知能力缺口 (+0.40)
    if tool.capabilities ∩ known_gaps:
        score += 0.40
    
    # 与高频任务类型匹配 (+0.25)
    if tool.task_types ∩ frequent_task_types:
        score += 0.25
    
    # 可能替代低信誉工具 (+0.15)
    if tool.replaces and ToolReputationLedger.get(tool.replaces).reputation < 0.5:
        score += 0.15
    
    # 社区热度高 (+0.10)
    if tool.community_size > 5000:  # GitHub Stars
        score += 0.10
    
    # 维护活跃 (+0.05)
    if tool.active_maintenance and tool.last_release > 30_days_ago:
        score += 0.05
    
    # 开源 (+0.05)
    if tool.license in ['MIT', 'Apache-2.0', 'GPL', 'AGPL']:
        score += 0.05
    
    return score
```

### 8.3 预学习队列状态

| 状态 | 含义 |
|------|------|
| `queued` | 已加入队列，等待学习资源 |
| `learning` | 正在沙箱中学习和试用 |
| `learned_promising` | 学习完成，值得深度评估 |
| `learned_watch` | 学习完成，暂不接入但继续关注 |
| `learned_skip` | 学习完成，不适合 Omega |
| `failed` | 学习失败（安装失败/不兼容/文档缺失） |

---

## 九、实施路线图（更新）

| 阶段 | 内容 | 实现方式 |
|------|------|---------|
| **MFE v0** | 手动注册表——人工维护 `10-外部AI与工具注册表/` 中的核心工具页 | 用户 + Claude 手动填写 |
| **MFE v1** | 手动雷达——用户说"有什么新工具"时，Claude 搜索并报告 | Claude 手动搜索 + 生成周报 |
| **MFE v2** | 半自动雷达——定时脚本扫描 GitHub Trending/PyPI + 生成摘要，Claude 审核 | Python 脚本 + Claude 审核 |
| **阶段 2** | 自动雷达——定时全量扫描所有监控源，自动生成工具摘要卡 + 周报 | 定时任务 + Perception Mesh |
| **阶段 3** | 智能雷达——AI 自动评估工具与 Omega 的匹配度、自动标记 investigate/integrate | LLM 评估 + Toolsmith 自动化试用 |
| **阶段 4** | 自适应雷达——根据历史任务失败模式，自动调整监控关键词和来源权重 | Evolution Loop 驱动 |

---

## 十、核心原则总结

1. **雷达是眼睛，不是手**——它的职责是发现和评估，不是使用
2. **主动监控 > 被动搜索**——不等任务失败才找，提前发现可能的工具
3. **工具摘要卡标准化**——统一格式，让 Toolsmith 和 Router 能直接消费
4. **退役追踪和发现同样重要**——不知道旧工具失效比不知道新工具更危险
5. **周报是人类接口**——用户不需要关注每个工具，每周看一眼报告就够了
6. **雷达本身也进化**——监控源、关键词、评估标准都随生态变化而调整

---

## 十一、相关页面

- [[Toolsmith-Lite与Skillsmith]] — 雷达发现工具后的深度评估和封装
- [[Capability Fabric]] — 评估通过后的工具注册目标
- [[Tool-Affordance Graph]] — 新工具的能力节点注册
- [[Tool Reputation Ledger]] — 工具信誉和准入状态追踪
- [[Tool-Agent Router：最佳工具与最佳执行者选择器]] — 使用雷达数据更新路由决策
- [[自我解惑与外援调用循环]] — 缺工具时的外部求助，雷达提供候选范围
- [[Perception Mesh]] — 雷达的感知基础设施
