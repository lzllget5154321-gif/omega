---
type: concept
tags: [omega-ecosystem, external-ai, rolebook, agent-roles, platform-specialization]
created: 2026-05-15
updated: 2026-05-15
knowledge_stability: evolving
parent: [[AI工具生态雷达]]
related:
  - [[自我解惑与外援调用循环]]
  - [[Tool-Agent Router：最佳工具与最佳执行者选择器]]
  - [[SOTA Source Hierarchy：顶尖工具来源分级]]
---

# External AI Rolebook：外部 AI 角色手册

> **定位**：定义 Omega 可用调用的所有外部 AI、Agent 平台、工具平台的**生态位**——谁擅长什么、有什么限制、什么时候应该调用、什么时候不该调用。这是 Omega 作为一个"AI 工具协调者"的核心参考。

---

## 一、语言与推理引擎

### 1.1 Claude (Anthropic API)

```
生态位：Omega 的核心语言引擎——通用推理、写作、分析、代码审查

擅长：
  - 长文本理解和生成（200K 上下文）
  - 复杂推理和逻辑分析
  - 学术写作和结构化文档
  - 代码审查和架构建议
  - 多语言（中英双语优势）

限制：
  - 知识截止于训练日期
  - 无实时网络访问（除非通过工具）
  - 不能执行代码（需要 Claude Code 或沙箱）

在 Omega 中何时调用：
  - 任务理解、任务契约生成
  - 复杂推理和方法选型
  - 学术写作和内容生成
  - 代码审查和质量评估
  - Critic Agent 的执行引擎

何时不用：
  - 需要实时信息 → Perplexity / Web Search
  - 需要代码执行 → Claude Code / Docker 沙箱
  - 需要多文献 RAG → NotebookLM
  - 需要深度多轮搜索 → Deep Research
```

### 1.2 Claude Code (CLI)

```
生态位：Omega 的主要代码执行和工具编排引擎

擅长：
  - Python/Bash/JS 脚本编写和执行
  - 文件读取/写入/编辑（理解完整仓库上下文）
  - Git 操作
  - 工具链编排（串联多个 CLI 工具）
  - Docker 容器管理

限制：
  - 需要终端环境
  - 不适合需要持久化状态的长任务（需要 LangGraph 配合）
  - 操作有风险（需要 Safety Enforcer 保护）

在 Omega 中何时调用：
  - 所有本地代码编写和执行
  - 文件操作（读写编辑）
  - 工具适配器开发
  - 数据处理脚本
  - Git 版本控制

何时不用：
  - 需要持久化状态的任务 → LangGraph + State
  - 超过 10 步的复杂工作流 → Dynamic Task Planner 编排
  - 需要外部 AI 判断的任务 → Claude API + Router
```

### 1.3 ChatGPT / GPT-4 (OpenAI)

```
生态位：备选语言引擎——当 Claude 不可用或特定任务更适合时

擅长：
  - 与 Claude 类似的能力
  - 某些特定领域的知识可能更新
  - Codex CLI 的原生支持

限制：
  - 作为备选，优先级低于 Claude
  - API 风格和 token 计算不同

在 Omega 中何时调用：
  - Claude API 不可用时（故障切换）
  - 需要交叉验证 Claude 的判断时
  - 使用 Codex CLI 时的原生引擎

何时不用：
  - Claude 可用且表现良好 → 保持一致性优先
```

---

## 二、深度研究与文献综合引擎

### 2.1 Deep Research

```
生态位：深度多轮研究员——需要多次搜索、多源交叉验证的复杂问题

擅长：
  - 多轮搜索和交叉验证
  - 从数十个来源中综合信息
  - 结构化研究报告
  - 复杂主题的系统性分析

限制：
  - 耗时较长（分钟-小时）
  - 成本较高
  - 结果需要 Critic 审查（AI 生成的研究可能有偏差）

在 Omega 中何时调用：
  - 用户问："Omega，深入研究一下 X 领域的最新进展"
  - 复杂主题需要系统性文献调研（非 PubMed 能覆盖的）
  - 多学科交叉主题
  - 需要从大量非学术来源中提取信息

何时不用：
  - 简单事实查询 → Web Search / Perplexity
  - 纯学术文献 → PubMed / Semantic Scholar
  - 已经在知识库中的内容 → wiki/ 搜索
  - 快速回答 → Claude API
```

### 2.2 NotebookLM

```
生态位：多文档 RAG 综合引擎——在一个上下文中同时分析多篇文献

擅长：
  - 跨文献综合结论提取
  - PDF/网页/视频等多媒体源导入
  - 生成结构化研究报告
  - 发现跨文献的矛盾和共识
  - 自动生成 Briefing Report / FAQ / Timeline / Podcast

限制：
  - 导入源数量有限（单 notebook 约 50 个源）
  - 需要手动或 CLI 管理 notebook
  - 输出质量依赖源质量

在 Omega 中何时调用：
  - 5+ 篇同主题文献需要综合 → 创建 NotebookLM 任务
  - 用户说"帮我综合这几篇文献的结论"
  - 需要跨文献比较（方法、结论、质量）
  - 需要自动生成结构化报告

何时不用：
  - < 5 篇文献 → Researcher Agent 逐篇处理即可
  - 需要实时信息 → Perplexity
  - 需要代码分析 → Claude Code
```

---

## 三、实时信息与搜索引擎

### 3.1 Perplexity

```
生态位：实时网页信息初筛引擎

擅长：
  - 实时网页搜索
  - 快速事实核查
  - 最新新闻/动态查询
  - 带来源引用的简短回答

限制：
  - 深度不足（对比 Deep Research）
  - 不适合学术文献检索（PubMed 更专业）
  - 有时引用来源质量参差不齐

在 Omega 中何时调用：
  - "最新消息"类问题
  - 快速事实核查
  - 工具的最新版本/定价信息
  - 作为其他来源的补充交叉验证

何时不用：
  - 需要深度研究 → Deep Research
  - 需要学术文献 → PubMed/Semantic Scholar
  - Omega 知识库已有答案 → wiki/ 搜索
```

### 3.2 PubMed / Semantic Scholar

```
生态位：学术文献专用检索引擎

详见 [[Omega生态系统项目-功能优先总方法论]] 第五部分 Perception Mesh。
```

---

## 四、视觉与创意引擎

### 4.1 Nano Banana / Nano Banana Pro

```
生态位：高质量 AI 图像生成和编辑——文字准确、理解力强

擅长：
  - 文字准确性高的图像生成（信息图、海报、教学图）
  - 基于自然语言的复杂场景理解
  - 图像编辑和局部修改
  - 多语言文字渲染
  - 风格一致性和品牌视觉

限制：
  - 科学结构可能不精确（需 Scientific Critic 审查）
  - 可控性不如节点式工具（ComfyUI）
  - 依赖 Google Cloud API

在 Omega 中何时调用：
  - 医学信息图、教学海报
  - 快速概念可视化
  - 带文字的复杂图像
  - 需要理解复杂 prompt 的图像生成

何时不用：
  - 需要精确节点控制 → ComfyUI
  - 需要本地可复现 → ComfyUI + SD
  - 需要 3D 渲染 → Blender
  - 需要科学矢量图 → BioRender / Figma
```

### 4.2 ComfyUI

```
生态位：可控视觉 AI 工作流引擎——节点式、可复现、多模型

擅长：
  - 节点式工作流（可保存、可复现、可分享）
  - 多模型组合（SD + ControlNet + IP-Adapter + ...）
  - API 节点接入闭源模型（Nano Banana 等）
  - 图像/视频/3D/音频多模态
  - 批量生成

限制：
  - 学习曲线陡
  - 需要 GPU（本地）或云服务
  - 节点配置复杂

在 Omega 中何时调用：
  - 需要可复现的图像生成工作流
  - 需要精确控制的视觉输出
  - 批量图像生成
  - 多模型/多步骤视觉管线

何时不用：
  - 快速单张概念图 → Nano Banana
  - 不需要复现的一次性任务 → Nano Banana
  - 纯 3D 动画 → Blender
```

### 4.3 Blender

```
生态位：专业 3D 创作套件——Python 完全可控

详见 [[科学动画生产系统]]。
```

### 4.4 Manim

```
生态位：精确可解释的 2D 动画引擎——数学/科学可视化

详见 [[科学动画生产系统]]。
```

---

## 五、音视频与后期引擎

### 5.1 ffmpeg

```
生态位：通用音视频处理引擎——格式转换、合成、剪辑

擅长：
  - 视频/音频格式转换
  - 视频合成（画面+音频+字幕）
  - 批量处理
  - 命令行完全可控

限制：
  - 无 GUI
  - 复杂剪辑不如专业 NLE

在 Omega 中何时调用：
  - 视频最终渲染和合成
  - 格式转换
  - 字幕烧录
  - 所有自动化视频处理
```

### 5.2 TTS 引擎群

```
生态位：文本转语音——Edge TTS（免费+中文好）/ ElevenLabs（高质量）/ OpenAI TTS

选择规则：
  - 中文旁白 + 免费 → Edge TTS
  - 高质量 + 多语言 → ElevenLabs
  - 与 GPT 管道集成 → OpenAI TTS
```

---

## 六、开发与自动化引擎

### 6.1 Codex CLI / OpenAI Agents SDK

```
生态位：备选代码执行和 Agent 编排引擎

何时调用：
  - Claude Code 不可用时
  - 需要 OpenAI 原生工具（WebSearch, FileSearch, CodeInterpreter）
  - 需要使用 OpenAI Agents SDK 的特定能力
```

### 6.2 GitHub

```
生态位：代码仓库 + 工具发现 + 问题追踪 + 社区协作

在 Omega 中的角色：
  - S1 来源（代码验证）
  - 工具发现（Trending / Search）
  - 最佳实践参考（高星项目的使用方式）
  - 错误排查（Issues 中的已知问题和修复）
```

### 6.3 Docker

```
生态位：隔离执行环境——所有不可信代码的沙箱

详见 [[Safety-as-Enabler]]。
```

---

## 七、知识管理引擎

### 7.1 Obsidian

```
生态位：Omega 的长期记忆和知识本体存储

在 Omega 中的角色：
  - 语义记忆（wiki/ — 概念、事实、关系）
  - 项目蓝图（omega生态系统项目/）
  - 用户界面（命令面板 → 触发任务）
  - 日志（wiki/log.md）
```

### 7.2 Zotero

```
生态位：文献管理——存储、组织、引用学术文献

在 Omega 中的角色：
  - 文献记忆（SQLite 数据库 + PDF 存储）
  - 引用管理（CSL 格式化）
  - 批注和高亮管理
```

### 7.3 Qdrant

```
生态位：语义搜索——向量索引和相似度检索

在 Omega 中的角色（阶段 2+）：
  - wiki/ 页面语义搜索
  - 相似任务/概念/工具检索
  - Tool-Affordance Graph 的向量化查询
```

### 7.4 PostgreSQL

```
生态位：结构化数据存储——行动记忆、工具信誉、任务日志

在 Omega 中的角色（阶段 2+）：
  - Action Memory 数据库
  - Tool Reputation Ledger 数据库
  - 任务调度状态
  - 分析查询
```

---

## 八、角色调用优先级总表

| 任务场景 | 第一调用 | 第二调用 | 不调用 |
|---------|---------|---------|--------|
| 理解用户意图 | Claude API | GPT-4 | — |
| 代码编写执行 | Claude Code | Codex CLI | Claude API（不执行代码） |
| 深度研究 | Deep Research | NotebookLM | Perplexity（不够深） |
| 多文献综合 | NotebookLM | Researcher Agent | Claude API（上下文不够） |
| 实时信息 | Perplexity | Web Search | Deep Research（太慢） |
| 学术文献 | PubMed/Semantic Scholar | OpenAlex | Perplexity（不专业） |
| 医学信息图 | Nano Banana Pro | ComfyUI | DALL-E（文字不准） |
| 可控视觉 | ComfyUI | Blender | Nano Banana（可控性低） |
| 3D 动画 | Blender | Unreal Engine | Manim（2D 引擎） |
| 2D 教学动画 | Manim | After Effects | Blender（太重） |
| 视频合成 | ffmpeg | DaVinci Resolve | — |
| 中文旁白 | Edge TTS | ElevenLabs | OpenAI TTS（中文弱） |
| 知识存储 | Obsidian wiki/ | PostgreSQL | — |
| 文献管理 | Zotero | 手动 BibTeX | — |
| 沙箱执行 | Docker | Firecracker/gVisor | 主机裸执行 |

---

## 九、相关页面

- [[自我解惑与外援调用循环]] — 外部 AI 的求助路径
- [[Tool-Agent Router：最佳工具与最佳执行者选择器]] — 调用外部 AI 的路由决策
- [[Creative Tool Router]] — 创意工具的专用路由
- [[SOTA Source Hierarchy：顶尖工具来源分级]] — 评估外部 AI 能力的来源权重
- [[AI工具生态雷达]] — 监控外部 AI 平台的变化
