---
type: concept
tags: [omega-ecosystem, tool-agent-router, task-routing, tool-selection, agent-selection, capability-matching]
created: 2026-05-15
updated: 2026-05-15
knowledge_stability: evolving
parent: [[Omega生态系统项目-功能优先总方法论]]
related:
  - [[Ω行动中枢]]
  - [[Action Brain]]
  - [[Capability Fabric]]
  - [[Toolsmith-Lite与Skillsmith]]
  - [[Productive Agent Society]]
  - [[Tool-Affordance Graph]]
  - [[Tool Reputation Ledger]]
---

# Tool-Agent Router：最佳工具与最佳执行者选择器

> **定位**：Tool-Agent Router 是 Omega 系统的"任务→工具/Agent 匹配中枢"。当 Ω 行动中枢将用户自然语言命令转化为任务契约后，Action Brain 调用 Tool-Agent Router 来回答一个核心问题：**"这个任务，用谁、用什么工具来做，效果最好？"**

---

## 一、为什么需要 Tool-Agent Router

现有方法论已经定义了完整的架构（Ω → Action Brain → Capability Fabric → Productive Agent Society），但缺一层关键的**选择逻辑**：当系统面对一个具体任务时，它**如何判断**应该用 Claude Code 还是 NotebookLM？用 Python 还是 R？让 Researcher 先上还是直接把任务发给 Data Analyst？

Tool-Agent Router 填补这个空白——它是**任务类型→能力需求→候选工具/Agent→多维度评分→最优选择**的完整决策链。

---

## 二、核心问题域

Tool-Agent Router 要回答 8 个问题：

| # | 问题 | 对应阶段 |
|---|------|---------|
| 1 | 这个任务属于什么类型？ | 任务分类 |
| 2 | 这种任务类型需要哪些能力？ | 能力映射 |
| 3 | 有哪些候选工具可以满足这些能力？ | 候选枚举 |
| 4 | 有哪些候选 Agent 可以执行这个任务？ | 候选枚举 |
| 5 | 如何比较多个候选工具/Agent？ | 多维评分 |
| 6 | 如果工具 A 快但不准，工具 B 慢但可靠，怎么取舍？ | 权衡策略 |
| 7 | 如果有多个 AI/Agent 平台都能参与，谁先上？ | 优先级路由 |
| 8 | 如果系统自己不知道该用什么，先问谁、查哪里？ | 升级路径 |

---

## 三、任务类型分类体系

### 3.1 一级分类（任务大类）

每条用户命令在 Ω 生成任务契约时，首先被分类到以下任务大类型：

| 任务类型 | 典型用户命令 | 核心能力需求 |
|---------|------------|------------|
| **knowledge_ingestion** | "把这 5 篇 PDF 处理了" | 文档解析 + 文本提取 + 知识提炼 + 网络化 |
| **literature_search** | "搜一下 SGLT2 抑制剂肾保护的文献" | 学术检索 + 元数据获取 + PDF 获取 + 筛选 |
| **data_analysis** | "分析这个 CSV 的统计特征" | 数据读取 + 清洗 + 探索性分析 + 可视化 |
| **meta_analysis** | "对这 8 篇研究做 Meta 分析" | 效应量提取 + 异质性检验 + 森林图 + GRADE |
| **academic_writing** | "基于这几篇文献写综述初稿" | 文献综合 + 结构化写作 + 引用管理 + IMRaD |
| **code_generation** | "写一个批量重命名的 Python 脚本" | 代码编写 + 沙箱测试 + 错误处理 |
| **file_processing** | "把 PDF 转成 Markdown" | 格式转换 + 批处理 + 质量检查 |
| **browser_automation** | "去投稿系统预填表单" | 浏览器导航 + 表单识别 + 截图 + 预填 |
| **tool_learning** | "那个新出的 X 工具怎么用" | 文档读取 + API 理解 + 沙箱试用 + Skill 封装 |
| **knowledge_query** | "我的笔记里关于 X 怎么说" | 语义搜索 + 跨页综合 + Wikilink 引用 |
| **medical_research** | "选题→检索→证据表→写作→投稿" | PICO + 检索 + GRADE + 写作 + 期刊匹配 |
| **system_maintenance** | "检查知识库死链" | 死链扫描 + 索引一致性 + 自动修复 |

### 3.2 二级分类（任务子维度）

每个大类型下按复杂度进一步细分：

| 复杂度 | 特征 | 示例 | 自主等级 |
|--------|------|------|---------|
| **简单（linear）** | 单步、单一工具、无分支 | "把这篇 PDF 转为 Markdown" | L0（自动） |
| **中等（branching）** | 多步、2-3 工具、含条件分支 | "搜 5 篇文献→提取摘要→对比结论" | L1（自动+通知） |
| **复杂（workflow）** | 多 Agent 协作、4+ 工具、含并行/合并 | "选题→检索→证据表→Meta 分析→写作→投稿预填" | L2（关键步骤需确认） |

---

## 四、能力需求映射表

每种任务类型自动映射到一组**必要能力（required_capabilities）**和**可选能力（optional_capabilities）**：

| 任务类型 | 必要能力 | 可选能力 | 典型工具通道 |
|---------|---------|---------|------------|
| knowledge_ingestion | ReadFile, ExtractText, WriteDraft, TaintCheck | OCR, TranslateDocument, ConceptLinking | pdftotext/Marker → Zotero → Obsidian wiki |
| literature_search | NetworkFetch, SearchAPI, CreateZotero, GetPDF | LiteratureFilter, CitationNetwork | PubMed/Semantic Scholar → Zotero |
| data_analysis | ReadData, ExecutePythonSandbox, GenerateChart | ExecuteRSandbox, StatisticalModel, MLModel | Python (pandas/scipy) / R |
| meta_analysis | ReadData, ExecutePythonSandbox/ExecuteRSandbox, GenerateChart, GRADE | PublicationBias, NetworkMetaAnalysis | R (metafor) / Python |
| academic_writing | ReadLocalFormal, WriteDraft, CiteManagement, FormatCSL | TranslateWriting, JournalMatch, AutoFigure | pandoc/Quarto/LaTeX |
| code_generation | ExecutePythonSandbox/ExecuteShellSandbox, ReadFile, WriteFile | PackageInstall, APITest | Python SDK / Docker |
| file_processing | ReadFile, WriteFile, ExecutePythonSandbox | OCR, BatchOperation, Compression | PyMuPDF/Marker/Pandoc |
| browser_automation | BrowserControl, Screenshot, DOMRead, FormFill | OCR, CaptchaAssist | Playwright / agent-browser |
| tool_learning | ReadDocumentation, ExecuteSandbox, AnalyzeAPI | CompareTools, GenerateAdapter | Toolsmith-Lite 闭环 |
| knowledge_query | SemanticSearch, ReadWiki, CrossPageSynthesize | QdrantVector, GraphTraversal | Obsidian + Qdrant |
| medical_research | PICO, LiteratureSearch, GRADE, QualityAssessment, AcademicWriting | LivingEvidence, JournalMatch | MEA + Researcher + Writer |
| system_maintenance | ReadWiki, DeadLinkScan, IndexCheck | AutoRepair, ConflictDetect | Knowledge Steward |

---

## 五、候选工具与 Agent 评分体系

### 5.1 评分维度定义

每个候选工具/Agent 在以下 12 个维度上评分（0.0-1.0），加权汇总：

| # | 维度 | 权重 | 说明 | 数据来源 |
|---|------|------|------|---------|
| 1 | **任务匹配度** (task_fit) | 0.20 | 该工具/Agent 是否专门设计用于这类任务 | Tool-Affordance Graph |
| 2 | **历史成功率** (success_rate) | 0.18 | 该工具/Agent 在此类任务上的历史成功率 | Action Memory 统计 |
| 3 | **工具信誉** (reputation) | 0.12 | 来源可信度、社区认可度、维护活跃度 | Tool Reputation Ledger |
| 4 | **执行成本** (cost) | 0.10 | Token 消耗、API 费用、时间成本 | 工具注册表 |
| 5 | **执行速度** (speed) | 0.08 | 平均完成时间（同类任务对比） | Action Memory 统计 |
| 6 | **上下文容量** (context_window) | 0.06 | 能处理的数据/文本量上限 | 工具规格 |
| 7 | **自动化程度** (automation) | 0.08 | 是否需要人类介入：全自动=1.0，需多次确认=0.3 | 自主等级设定 |
| 8 | **输出质量** (output_quality) | 0.10 | 历史输出的人类满意度/审阅通过率 | Critic 评估 + 用户反馈 |
| 9 | **风险等级** (risk_level) | 0.06 | 该工具/Agent 的操作风险（反向评分：低风险=高分） | Safety-as-Enabler |
| 10 | **可回滚性** (rollback) | 0.04 | 操作是否可撤销：Git 可回滚=1.0，API 发送不可撤回=0.0 | 工具特征 |
| 11 | **已有 Skill 覆盖** (skill_coverage) | 0.06 | 是否已有成熟 Skill 封装该操作 | Skill Library |
| 12 | **领域适配** (domain_fit) | 0.08 | 是否适合特定领域（医学/学术/工程） | 领域标签 |

**总分 = Σ(维度评分 × 权重)**

> 权重不是固定的——Evolution Loop 可以根据历史任务结果动态调整权重（如某类任务中"速度"比"成本"更重要 → 自动提升 speed 权重）。

### 5.2 评分示例：文献检索任务

用户命令：「搜 20 篇 SGLT2 抑制剂肾保护的最新文献」

| 维度 | PubMed E-utilities | Semantic Scholar | OpenAlex | Google Scholar (Browser) |
|------|:--:|:--:|:--:|:--:|
| task_fit (0.20) | 0.95 | 0.90 | 0.75 | 0.60 |
| success_rate (0.18) | 0.96 | 0.92 | 0.88 | 0.70 |
| reputation (0.12) | 0.98 | 0.90 | 0.78 | 0.65 |
| cost (0.10) | 0.95 | 0.90 | 0.98 | 0.20 |
| speed (0.08) | 0.85 | 0.90 | 0.80 | 0.40 |
| context_window (0.06) | 0.60 | 0.70 | 0.70 | 0.50 |
| automation (0.08) | 0.95 | 0.95 | 0.95 | 0.20 |
| output_quality (0.10) | 0.95 | 0.88 | 0.80 | 0.65 |
| risk_level (0.06) | 0.95 | 0.95 | 0.95 | 0.70 |
| rollback (0.04) | 0.90 | 0.90 | 0.90 | 0.80 |
| skill_coverage (0.06) | 0.95 | 0.80 | 0.40 | 0.20 |
| domain_fit (0.08) | 0.98 | 0.92 | 0.80 | 0.55 |
| **加权总分** | **0.930** | **0.894** | **0.816** | **0.530** |

→ **选择 PubMed E-utilities 作为主工具**，Semantic Scholar 作为备选（当 PubMed API 超时时自动切换）。

### 5.3 评分示例：Agent 选择

同一个文献检索任务——谁来做？

| 维度 | Researcher | Data Analyst | Coder |
|------|:--:|:--:|:--:|
| task_fit (0.20) | 0.98 | 0.40 | 0.25 |
| success_rate (0.18) | 0.94 | 0.70 | 0.60 |
| reputation (0.12) | 0.95 | 0.85 | 0.80 |
| cost (0.10) | 0.85 | 0.80 | 0.90 |
| speed (0.08) | 0.90 | 0.85 | 0.85 |
| context_window (0.06) | 0.85 | 0.90 | 0.95 |
| automation (0.08) | 0.90 | 0.85 | 0.80 |
| output_quality (0.10) | 0.92 | 0.75 | 0.65 |
| risk_level (0.06) | 0.95 | 0.85 | 0.75 |
| rollback (0.04) | 0.90 | 0.90 | 0.90 |
| skill_coverage (0.06) | 0.95 | 0.30 | 0.20 |
| domain_fit (0.08) | 0.95 | 0.40 | 0.25 |
| **加权总分** | **0.926** | **0.682** | **0.628** |

→ **选择 Researcher** 作为主执行者。

---

## 六、决策路由算法

### 6.1 主路由流程

```
Ω 生成任务契约（Task Contract）
  │
  ├── 步骤 1：任务类型分类
  │     └── 匹配一级分类 + 二级复杂度
  │
  ├── 步骤 2：能力需求映射
  │     └── 从能力映射表获取 required_capabilities + optional_capabilities
  │
  ├── 步骤 3：候选工具枚举
  │     ├── 查询 Capability Fabric → 哪些工具提供这些能力？
  │     ├── 查询 Tool-Affordance Graph → 哪些工具组合适合这类任务？
  │     └── 查询 Tool Reputation Ledger → 过滤信誉不合格的工具
  │
  ├── 步骤 4：候选 Agent 枚举
  │     ├── 查询 Productive Agent Society → 哪些 Agent 的生态位匹配？
  │     ├── 过滤 Agent 的当前可用性（是否被占用/维护中）
  │     └── 过滤自主等级不匹配的 Agent（L0 任务不让 L3 Agent 做）
  │
  ├── 步骤 5：12 维评分
  │     ├── 对每个候选工具 × 候选 Agent 组合评分
  │     └── 生成排序列表（top-3 组合）
  │
  ├── 步骤 6：选择策略
  │     ├── 默认：加权总分最高的组合
  │     ├── 用户偏好覆盖：如果用户说"用 NotebookLM 做"→ 强制使用
  │     ├── 约束过滤：如果首选工具不可用 → 自动切换到第二高分
  │     └── 自主等级适配：L0 任务可自动选择 → L2 任务展示候选列表给用户
  │
  └── 步骤 7：执行后记录
        └── 将本次选择的结果写回 Tool Reputation Ledger + Action Memory
```

### 6.2 多工具组合的路由

复杂任务通常不能用单一工具完成——需要**工具组合**：

```
任务：「搜 SGLT2 抑制剂文献→GRADE 评级→写综述」

工具组合路由：
  搜索阶段       → PubMed E-utilities (主) + Semantic Scholar (备)
  文献管理        → Zotero Adapter
  PDF 提取       → Marker (主) + pdftotext (备)
  GRADE 评级     → MEA (Medical Evidence Agent)
  写作           → Academic Writer
  格式化         → pandoc + CSL
  审查           → Critic
```

**组合优化原则**：
- 相邻步骤的工具应兼容（输出格式 = 下一步的输入格式）
- 避免工具过度切换（同类型步骤尽量用同一工具链）
- 并行步骤的工具应独立（不共享状态/不竞争资源）

### 6.3 多平台 AI 参与的优先级路由

当多个 AI/Agent 平台都能参与同一类任务时：

| 场景 | 优先级顺序 | 路由规则 |
|------|-----------|---------|
| **代码生成/执行** | Claude Code → Codex CLI → Coder Agent | Claude Code 首选（集成度最高），Codex 为备选 |
| **文献综合/长篇研究** | NotebookLM → Researcher → Deep Research | 有 5+ 篇同主题文献时优先 NotebookLM |
| **简短事实查询** | Claude → Perplexity → Researcher | 优先内部知识+知识库，外部搜索为补充 |
| **网页浏览/操作** | Playwright (agent-browser) → Computer Use-Lite | 优先 agent-browser（速度+稳定性） |
| **数据分析** | Data Analyst Agent → Python 脚本 → R 脚本 | 优先 Agent（含上下文理解），裸脚本为备选 |
| **医学证据评估** | MEA Agent → Claude 内置知识 → Researcher | MEA 首选（专业 GRADE 工具链） |
| **格式转换/文件处理** | File Editor Agent → Python 脚本 → Pandoc CLI | 优先 Agent（含错误处理+质量检查） |

### 6.4 跨平台 AI 咨询路由（外部 AI 作为顾问）

当 Omega 自己不确定答案时，它可以**咨询外部 AI** 作为参考判断：

| 问题类型 | 咨询对象 | 咨询方式 | 结果处理 |
|---------|---------|---------|---------|
| "这个统计方法选对了吗？" | Claude API / ChatGPT | 发送问题描述 + 候选方法 → 获取判断 | 标注来源 + 置信度，由 Critic 综合 |
| "这篇文献的方法学质量如何？" | NotebookLM (RAG) | 导入 PDF → 提问方法学质量 | 标注"AI 辅助评估"，MEA 做最终判断 |
| "这两个工具哪个更适合这个场景？" | Perplexity / Claude | 发送对比查询 → 获取推荐 | 写入 Tool Reputation Ledger 作为参考 |
| "这个投稿策略合理吗？" | Claude + Journal Matcher Agent | Agent 路径 + Claude 判断交叉验证 | 标注"AI 建议，非人类编辑判断" |

**重要约束**：外部 AI 的咨询结果是**参考输入**，不是**最终决策**。最终决策由 Omega 的 Critic/MEA 或用户做出。

---

## 七、当系统不知道用什么时的升级路径

### 7.1 升级触发条件

| 触发条件 | 含义 | 升级路径 |
|---------|------|---------|
| 无候选工具匹配 | Capability Fabric 中没有工具覆盖所需能力 | → **Toolsmith-Lite** 搜索新工具 |
| 所有候选评分 < 阈值 | 最匹配的工具评分也低于 0.60 | → **Toolsmith-Lite** 搜索更好的工具 |
| 排名第一和第二差距 < 0.03 | 无法明确区分最优选择 | → **咨询外部 AI** + 展示候选给用户 |
| Capability Fabric 返回空集 | 所需能力类型尚未注册 | → **Ability Gap Detector** 诊断 → **Toolsmith-Lite** |
| 历史数据显示所有候选均不稳定 | Action Memory 显示此类任务成功率 < 0.70 | → **Planner** 重新规划任务结构 |
| 任务类型不在分类表中 | 系统从未见过此类任务 | → **向用户提出最小必要澄清问题** |

### 7.2 最小必要澄清协议

当系统真的不知道时——向用户提问，但遵循**最小必要**原则：

```
❌ 坏的提问："这个任务你想用什么工具？"  （把决策负担抛回用户）
✅ 好的提问："这个任务我找到 3 种方案：
               A) PubMed + R metafor（标准 Meta 分析路径，约 25 分钟）
               B) NotebookLM 综合（适合初步探索，约 10 分钟）
               C) 你指定其他方式
               建议选 A（因为涉及 GRADE 评级，需要可重复分析）。你确认吗？"
```

**最小必要提问规则**：
1. 必须附带 ≥2 个具体方案（不能只问"你想怎么办"）
2. 必须附带推荐方案 + 理由
3. 必须附带预估时间
4. 必须允许用户说"就按你的推荐来"（一键确认）
5. 一次只问一个问题（不连环追问）

---

## 八、与现有架构组件的接口

| 上游输入 | 来自 | 输入内容 |
|---------|------|---------|
| Ω 行动中枢 | [[Ω行动中枢]] | 已结构化的任务契约（task_type / user_goal / required_tools / agents） |
| Action Brain | [[Action Brain]] | 任务 DAG 分解后的每个子步骤 + 所需能力列表 |

| 下游输出 | 去向 | 输出内容 |
|---------|------|---------|
| Capability Fabric | [[Capability Fabric]] | 选定的工具列表 + 调用参数 |
| Productive Agent Society | [[Productive Agent Society]] | 选定的 Agent 列表 + 分工安排 |
| Action Memory | [[Action Memory]] | 本次选择的完整记录（用于未来评分优化） |
| Tool Reputation Ledger | [[Tool Reputation Ledger]] | 本次选择的成功/失败反馈 |

| 查询依赖 | 来源 | 查询内容 |
|---------|------|---------|
| Tool-Affordance Graph | [[Tool-Affordance Graph]] | 什么工具能做什么任务 |
| Tool Reputation Ledger | [[Tool Reputation Ledger]] | 工具的信誉和历史表现 |
| Skill Library | [[Skill Library]] | 已有 Skill 覆盖的情况 |
| Action Memory | [[Action Memory]] | 历史同类任务的工具/Agent 选择与结果 |

---

## 九、评分数据来源与更新机制

```
评分维度          数据来源              更新频率         更新方式
─────────────────────────────────────────────────────────────
task_fit         Tool-Affordance Graph   实时            手动/半自动（Toolsmith 发现新工具时）
success_rate     Action Memory 统计      每次任务后      自动（成功/失败记录 → 移动平均）
reputation       Tool Reputation Ledger  工具事件触发    半自动（Toolsmith + Critic 评估）
cost             AI工具生态雷达          每周            半自动（API 价格监控）
speed            Action Memory 统计      每次任务后      自动（记录执行时间 → 移动平均）
context_window   工具规格注册表          工具接入时      手动（读取工具文档）
automation       自主等级设定            Skill/Agent 定义 手动（任务契约中指定）
output_quality   Critic 评估 + 用户反馈  每次任务后      半自动（Critic 评分 + 用户确认/拒绝）
risk_level       Safety-as-Enabler       工具接入时      自动（能力类型系统静态分析）
rollback         工具特征分类            工具接入时      手动（注册时标注）
skill_coverage   Skill Library           每次 Skill 更新  自动（Skill 关联工具查询）
domain_fit       领域标签                工具接入时      手动（注册时标注领域）
```

---

## 十、实施路线图

| 阶段 | 内容 | 依赖 |
|------|------|------|
| **MFE v1** | 静态路由表——手动维护 task_type → tool/agent 映射表（YAML），不做动态评分 | 任务分类表 + 能力映射表 |
| **MFE v2** | 简单评分——在静态路由基础上加入 3 个核心维度（task_fit + success_rate + reputation），加权求和 | Action Memory 开始积累数据 |
| **MFE v3** | 完整 12 维评分——全部 12 个维度启用，权重可手动调整 | Tool Reputation Ledger 就绪 |
| **阶段 2** | 动态权重——Evolution Loop 根据任务结果动态调整各维度权重 | Evolution Loop 就绪 |
| **阶段 3** | 咨询路由——自动判断何时咨询外部 AI，何时向用户提问 | 自我解惑与外援调用循环就绪 |

---

## 十一、当前 MFE 阶段的简化实现（静态路由表）

在 MFE 阶段，Tool-Agent Router 以**静态 YAML 路由表**的形态存在：

```yaml
# 文件位置：omega生态系统项目/03-能力矩阵/tool-agent-routing-table.yaml
# 用途：MFE 阶段的静态工具/Agent 路由表
# 演进：MFE v2 起由 Action Memory 统计驱动，本表作为冷启动默认值

routing_table:
  knowledge_ingestion:
    primary_tools: [pdftotext, marker, zotero_adapter]
    fallback_tools: [pymupdf, easyocr]
    primary_agent: researcher
    secondary_agents: [knowledge_steward]
    autonomy: auto  # L0

  literature_search:
    primary_tools: [pubmed_api, zotero_adapter]
    fallback_tools: [semantic_scholar_api, openalex_api]
    primary_agent: researcher
    secondary_agents: []
    autonomy: auto  # L0

  data_analysis:
    primary_tools: [python_pandas, python_matplotlib]
    fallback_tools: [r_ggplot2, r_dplyr]
    primary_agent: data_analyst
    secondary_agents: [coder]
    autonomy: notify  # L1

  meta_analysis:
    primary_tools: [r_metafor, python_statsmodels, robvis]
    fallback_tools: [python_pymc, r_meta]
    primary_agent: data_analyst
    secondary_agents: [medical_evidence_agent, researcher]
    autonomy: confirm  # L2

  academic_writing:
    primary_tools: [pandoc, csl_styles, python_docx]
    fallback_tools: [quarto, latex]
    primary_agent: academic_writer
    secondary_agents: [critic, medical_evidence_agent]
    autonomy: confirm  # L2

  code_generation:
    primary_tools: [python_sdk, docker]
    fallback_tools: [nodejs, bash]
    primary_agent: coder
    secondary_agents: [critic]
    autonomy: auto  # L0 (if sandboxed)

  file_processing:
    primary_tools: [pymupdf, marker, pandoc]
    fallback_tools: [python_docx, tesseract]
    primary_agent: file_editor
    secondary_agents: []
    autonomy: auto  # L0

  browser_automation:
    primary_tools: [playwright, agent_browser]
    fallback_tools: [puppeteer]
    primary_agent: submission_navigator
    secondary_agents: []
    autonomy: confirm  # L2 (始终需要用户确认提交)

  tool_learning:
    primary_tools: [toolsmith_lite]
    fallback_tools: []
    primary_agent: coder
    secondary_agents: [researcher]
    autonomy: confirm  # L2

  knowledge_query:
    primary_tools: [obsidian_search, qdrant]
    fallback_tools: [grep, ripgrep]
    primary_agent: knowledge_steward
    secondary_agents: []
    autonomy: auto  # L0

  medical_research:
    primary_tools: [pubmed_api, zotero_adapter, r_metafor, robvis]
    fallback_tools: [semantic_scholar_api, openalex_api]
    primary_agent: medical_evidence_agent
    secondary_agents: [researcher, academic_writer, journal_matcher, data_analyst]
    autonomy: confirm  # L2

  system_maintenance:
    primary_tools: [obsidian_cli, git]
    fallback_tools: [bash_find, python_pathlib]
    primary_agent: knowledge_steward
    secondary_agents: []
    autonomy: notify  # L1
```

---

## 十二、相关页面

- [[Ω行动中枢]] — 任务入口，生成任务契约后调用 Router
- [[Action Brain]] — 任务分解 + 调度，Router 是它的选择引擎
- [[Capability Fabric]] — 提供候选工具的能力清单
- [[Tool-Affordance Graph]] — "工具能做什么"的知识图谱
- [[Tool Reputation Ledger]] — 工具信誉和准入状态
- [[Productive Agent Society]] — 候选 Agent 的社会分工
- [[Toolsmith-Lite与Skillsmith]] — Router 无候选时的升级路径
- [[自我解惑与外援调用循环]] — Router 不确定时的外部咨询路径
- [[Skill Library]] — 已有 Skill 覆盖情况
- [[Action Memory]] — 历史选择记录的存储
