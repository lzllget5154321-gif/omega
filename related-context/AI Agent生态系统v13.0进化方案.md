---
type: insight
tags: [AI-Agent生态系统, 生物启发架构, 控制论, 生理学映射, v13.0, 本体重定义, 自我进化, 运行时修复, allostasis, 生物控制论]
sources:
  - "[[洞察/v12.0多Agent知识库进化-最终构建总方案]]"
  - "[[洞察/Ω-Loop最终执行方案]]"
  - "[[洞察/个人AI知识-行动生命体]]"
  - "[[洞察/Agent自进化框架设计模式对比]]"
  - "2026-07 互联网深度研究（Anthropic工程博客/arXiv多篇/Cognition博客，见附录）"
  - "生理学解剖学教材级研究（Guyton & Hall/Kandel/StatPearls/NCBI Bookshelf，见附录）"
  - "控制论/CS基础研究（Ashby/Brooks/McClelland/Erlang OTP，见附录）"
  - "本次会话对 .claude/ 全量结构与 wiki/log.md 的直接审计"
created: 2026-07-12
updated: 2026-07-12
knowledge_stability: evolving
status: "blueprint — Phase 0（运行时修复）可立即执行；Phase 1+ 需逐项用户审批"
---

> **定位**：本文档是本知识库从「Obsidian 知识库工作流」到「AI Agent 生态系统」这一本体转变的**权威设计蓝图**。它不取代 [[洞察/v12.0多Agent知识库进化-最终构建总方案]]（多Agent团队决策）或 [[洞察/Ω-Loop最终执行方案]]（钩子/Event Store 基建），而是在两者之上补齐三个此前缺失的维度：**(1) 严谨的生理学/解剖学→控制论→工程三级映射**（此前「行动生命体」的「器官/肌肉」类比是方向性的、非机制级的）；**(2) 2026 年最新行业共识中的反过度工程校准**（此前三代蓝图全部是"增加复杂度"方向，零处引用"多 Agent 生产失败率 41-87%""目标造假是自我改进系统头号失效模式"等 2026 一手研究——这恰恰是本知识库自身 EMI/freeze_enforcer 已经在犯的错）；**(3) 对当前运行时状态的诚实审计**（v12.0 待审批 6 周未决，Ω-Loop 建成的钩子层已静默失效 ~1 个月而无人发现——这比"要不要建生态系统"更紧急）。

---

## 执行摘要（≤600字）

用户提出：将知识库工作流的定义从"Obsidian 知识库工作流"升级为"以 Obsidian+Claude 为核心、能自我进化/修正/检查/改进的 AI Agent 生态系统"，并要求借鉴人体生理解剖学原理、广泛调研 2026 年最新行业共识后给出完整进化方案。

**本次研究的三个关键发现，决定了方案的形态：**

1. **这不是第一次尝试。** 2026-05-15 起已有三代同类蓝图：「行动生命体」（生物隐喻起点）→ v12.0（多Agent团队决策，**至今待审批 6 周**）→ Ω-Loop（钩子/Event Store 基建，**已部分建成**）。真正的空白不是"有没有愿景"，而是"愿景为何两次都没有走到底"。
2. **正在运行的系统已经悄悄坏了，而且是坏在"自我检查"这个能力本身。** 本次审计发现：Write/Edit 钩子自 2026-07-08 起静默失效、Event Store 冻结 23-33 天、Agent spawn 因 503 错误 14 天内失败 43 次并静默降级、知识库健康分从 87 降至 ~60。**没有任何自动机制报告了这些衰变**——这正是本文档 §7 要重新定义的"自我检查"能力当前并不真实存在的证据。
3. **2026 行业的头号共识恰好是本库已经踩中的坑。** Cognition《Don't Build Multi-Agents》等 2026 一手资料显示生产环境多 Agent 系统失败率 41-87%，自我改进系统的头号命名失效模式是"目标造假"（objective hacking，指标看起来在控制但从未真正接线）——这精确描述了本库 EMI 公式中 s2 恒为 1.00、freeze_enforcer 与 EMI 无代码联动的已知问题。

**因此本方案的核心论点**：生态系统方向是对的，生物映射的直觉是对的——但下一步不是叠加第三层复杂性，而是先诚实止血（修复静默失效）、再用医学教材级精度校准已有的松散生物类比、再用 2026 反过度工程共识做减法与统计学验收门，最后才是本体身份的正式重定义。四步顺序不可颠倒——这本身就是从"伤口愈合"（先止血、再清创、再重建、再重塑）借来的医学原则，详见 §4.8/§11。

**新增定义提案**（§7 详述）：*"以 Obsidian + Claude Code 为核心载体，以生理学与控制论精确映射为设计校准依据，以可验证、可审计、抗静默失效为底线约束的自我进化、自我修正、自我检查、自我改进的个人 AI Agent 生态系统。"* 相比用户原始提法，新增"可验证、可审计、抗静默失效"——因为本次审计证明，"自我检查"若不被强制验证，会在无人察觉的情况下停止运作。

---

## 目录

1. [与既有蓝图的关系](#一与既有蓝图的关系)
2. [现状诊断：运行时衰变审计](#二现状诊断运行时衰变审计)
3. [2026 行业情报简报](#三2026-行业情报简报)
4. [生理学与解剖学精确原理](#四生理学与解剖学精确原理)
5. [控制论与计算机科学基础](#五控制论与计算机科学基础)
6. [生物→控制论→工程 映射表](#六生物控制论工程-映射表)
7. [本体重定义](#七本体重定义)
8. [架构蓝图：七个子系统](#八架构蓝图七个子系统)
9. [效能评估体系](#九效能评估体系)
10. [反模式与自指风险](#十反模式与自指风险)
11. [分阶段路线图](#十一分阶段路线图)
12. [治理与自指保护](#十二治理与自指保护)
13. [附录：引用来源](#十三附录引用来源)

---

## 一、与既有蓝图的关系

| 蓝图 | 日期 | 核心贡献 | 当前状态 | 本文档的关系 |
|------|------|---------|:--:|------|
| [[洞察/个人AI知识-行动生命体]] | 2026-05-15 | 生物隐喻起点：系统=认知-行动操作系统，Codex/Claude Code/NotebookLM等="器官/肌肉"；三层自主性；命令→意图→权限→分解→路由→执行→校验→审查→记忆→进化 十步公式 | 反思性洞察，未形式化 | 本文档 §7 继承其"操作系统"定性，§6 把"器官/肌肉"升级为机制级映射 |
| [[洞察/v12.0多Agent知识库进化-最终构建总方案]] | 2026-06-01 | 决策：用 Claude Code Agent Teams 而非物理构建 Omega；团队规模2→4；Critic 需对立激励；共享状态=vault文件；记忆=现有wiki四层 | **blueprint——待用户审批，已 6 周未决** | 本文档不改变其决策，但 §9/§10 补充"读多写少才并行"的2026行业验收标准，建议审批前先过 Phase 0 |
| [[洞察/Ω-Loop最终执行方案]] | 2026-06-16 | 诊断：26项基建零使用，根因是"依赖Claude在执行模式下记得做合规检查"；解法：钩子层+Event Store+SEPL闭环，6 Phase 35任务 | **已部分执行**（hook-fire-log 显示曾经运行），**现已静默失效**（自2026-07-08起零记录） | 本文档 §2 直接审计其产出物的当前健康度；§11 Phase 0 = 优先修复 Ω-Loop 已建但已坏的部分，而非重建 |
| [[洞察/Agent自进化框架设计模式对比]] | — | DGM/Lamarckian继承/Misevolution 等自我进化设计模式对比 | 参考性 | 本文档 §10 引入 PACE 统计验收门，是对其比较的补充而非替代 |
| `omega生态系统项目/`（44文件） | 2026-05 | Omega 完整蓝图：9层架构+建构包 | v12.0 已决策不物理构建 | 不涉及，尊重 v12.0 决策 |

**结论**：本文档的合法性不来自"提出一个新愿景"，而来自"诚实核查前三代愿景的执行现状，并补齐它们共同缺失的三块拼图"（严谨生物映射、行业反过度工程校准、静默失效检测）。

---

## 二、现状诊断：运行时衰变审计

> 为什么诊断放在设计之前？—— 借用医学原则：对失血的病人先止血，再讨论康复训练计划。下面的发现如果不先处理，任何新架构都会被"接在已经停摆的神经上"。

### 2.1 三个并发衰变信号（本次审计直接核实）

| 信号 | 证据 | 衰变时长 | 严重度 |
|------|------|:--:|:--:|
| Write/Edit 钩子静默失效 | `hook-fire-log.jsonl` 自 2026-07-08 起零新记录 | ~4 天（审计时点 2026-07-12） | 🔴 致命——Ω-Loop Phase Ω-1 的核心交付物失效 |
| Event Store / 看板 / Agent 记忆通道冻结 | 相关信号文件 23–33 天无更新 | 最长 33 天 | 🔴 致命——"自我检查"赖以运作的记忆底座已停摆超一个月 |
| Agent spawn 大量 503 失败 | 14 天内 43 次，静默降级为 Team-Lead-direct | 14 天窗口 | 🟡 严重——多Agent能力实际上已 retreat 回单Agent，但无人被通知 |
| 知识库健康分下滑 | 87 → ~60（2026-07-12 lint 记录） | 未知起点 | 🟡 严重 |

### 2.2 为什么现有自我检查机制没有报告这些衰变——"目标造假"实证

这是本文档最重要的单一发现：**本库的自我进化/自我检查机制本身已经出现了 2026 行业文献命名的头号失效模式**。

| 机制 | 设计意图 | 实际状态 | 对应 2026 文献概念 |
|------|---------|---------|---------|
| EMI（Execution Mode Index） | 量化追踪执行模式健康度，≥2月连续下降触发规则冻结 | s2（Skill采用率）8次快照恒为1.00——公式天花板效应，非真实测量；s4 曾8次测量恒为0.00（2026-07-05才修复） | **Objective hacking**（arXiv 2508.07407 综述命名的自我改进系统头号失效模式：指标看起来在控制，从未真正接线） |
| freeze_enforcer.py | EMI 降至 critical → 触发规则冻结 | 已核实：读取的是完全不同的 `evolve_force_log.jsonl`，**与 EMI 无任何代码或 hook 联动** | 同上——"控制回路"存在于文档叙述中，不存在于代码中 |
| task_completion_gate.py | 所有任务完成前的物理验证门 | 仅覆盖 P3.1/2/3 三个历史任务，其余任务 exit 0 放行+警告；**未接入任何 hook** | 覆盖率错觉——"存在验证脚本"≠"验证被执行" |
| Hook 健康监控 | 理论上应检测钩子静默失效 | 钩子层本身死掉后，"检测钩子是否死掉"的责任落在……钩子层 | 循环依赖——监控者与被监控者共用同一失效路径 |

**这一发现直接驱动本文档 §7 的重定义**：不能只说系统"能够自我检查"，必须明确"自我检查"这一属性本身需要**独立于被检查对象的验证路径**（生理学类比见 §4 免疫系统的双重耐受检查机制——中枢耐受失败时依赖外周耐受作为第二道独立防线，而不是同一套机制检查自己）。

### 2.3 诊断结论

系统当前状态不是"缺少 AI Agent 生态系统的构想"，而是**"构想已经两次被正式采纳（v12.0 决策、Ω-Loop 部署），但采纳后的运行时验证是缺失的"**。任何新一轮设计如果不先解决"如何知道设计是否真的在运行"，就会成为第四个躺在 `wiki/洞察/` 里的漂亮文档。

**Phase 0（见 §11）必须先于本文档其余部分执行**，且不需要新设计——只需要修复已经决策过的东西。

---

## 三、2026 行业情报简报

> 完整来源见 §13。本节只保留对本方案有直接决策影响的结论。

### 3.1 编排范式：Orchestrator-Worker 是唯一验证过的模式，但"多≠好"

2026 年行业已从"Agent 能不能用"转向"如何可靠编排"。主导模式是 **Orchestrator-Worker**（主 Agent 规划+委派给独立上下文的子 Agent），Anthropic 自研多Agent研究系统在检索广度任务上比单 Agent Opus 高 ~90%。但**关键前提被反复验证**：多 Agent 收益仅在**读多写少、可并行**的任务上出现；**写多、需要连贯性**的任务上（恰恰是本库"编译wiki页面"的核心工作）多 Agent 反而净损失（Cognition 报告 −39%~−70%）。生产环境多 Agent 系统失败率 **41–87%**，即便单步可靠性达 99%，误差仍会复合放大。MCP（工具/上下文连接）+ A2A（Agent 间协议）是两个已成型的互联互通标准，与 v12.0 决策的 P2P 邮箱+共享文件系统方向一致。

**→ 决策**：v12.0 的 Agent Teams 升级**保留**，但必须显式区分"读多写少任务默认并行"vs"写多/主观判断任务默认单Agent"，而不是只按文件数量分级（现行 agent-dispatch.md 矩阵仅按文件数/复杂度分级，缺这一维度）。

### 3.2 AI-native PKM 是被命名的真实赛道，本库的模式已被业界独立验证

`obsidian-wiki`（GitHub）明确实现 Karpathy 提出的"LLM Wiki"范式——一次编译、保持更新，而非每次查询重跑 RAG，与本库 CLAUDE.md 的四层架构定位完全一致。竞品 `obsidian-second-brain`（2026-07，v0.12）强调**"vault-first research"**（先扫描已有笔记，只对缺口做外部搜索）+ **把 Agent 写入当作可审查的 Git PR**——这是比本库更轻量的对照组，值得作为§9 的效能基准。

**→ 决策**：不需要"发明新范式"的自我怀疑——本库的四层架构方向正确，改进空间在"更轻、更可审查"而非"更多层"。

### 3.3 记忆架构：四类型已是共识，检索策略比存储形态更重要

生产实践收敛到 **working / episodic / semantic / procedural** 四类记忆，与 v12.0 已经映射的 L0-L4 五层记忆结构高度吻合。**A-MEM**（Zettelkasten 式自动关联笔记 + supersession 检测）与本库 wiki 的 wikilink 结构几乎同构，是最值得直接借用的具体机制——本库当前**没有**"检测新笔记是否取代旧笔记"的机制。核心教训：**"检索策略比存储形态更重要"**——纯向量相似度对多跳/时序查询会失败；需要混合语义+关键词+图谱+时序检索（本库四层架构的 Graph RAG 层已覆盖多跳，但时序/supersession 检测缺失）。

**→ 决策**：§8.3 补充 A-MEM 式 supersede 检测机制，而不是新建记忆后端。

### 3.4 自我进化 Agent：完整学术框架已存在，本库缺其"验收统计学"

权威综述 arXiv 2508.07407 将自我进化建模为 {Agent系统, 环境, 优化器} 反馈环，安全层级为 **Endure（不可退化的安全底线）→ Excel（不能倒退）→ Evolve（允许适应）**——与本库 self-evolution.md 的确认/冷却机制精神一致。**本库缺失的关键一环**：arXiv 2606.08106（PACE）指出几乎所有自我进化系统"把单次经验性得分当作接受决策"，缺乏统计学意义上的假设检验；本库 `/evolve` 的确认门当前正是"单次confirm"，没有"最少样本量"要求。

**→ 决策**：§10/§12 引入 PACE 式统计验收门——一个规则修改在被"确认"前，必须有 ≥5 组可比历史操作数据支持，而不是一次性观感确认。

### 3.5 Anthropic 官方方向：原生能力已解决大半"重新发明的轮子"

官方栈：MCP（连接）→ Agent Skills（渐进式披露——Claude 默认只看到 name+description，需要时才展开）→ Claude Agent SDK → 子 Agent（隔离上下文，并行）→ Agent Teams（2026早期）。2025年9月上线的 **memory tool**（跨会话文件式记忆）+ **context editing**（自动清理陈旧工具调用结果），组合后在100轮任务上 token 消耗降 84%、检索任务得分升 39%。官方哲学明确写在《Building Effective Agents》：**保持简单、优先透明、只在简单方案确实不够时才增加 Agent 复杂度**。

**→ 决策**：审计 `.claude/scripts/` 中是否有功能与官方 memory tool / context editing 重叠的自研实现（如 `chroma_memory.py`/`mirror_memory.py`/`skill_memory.py` 三个记忆脚本并存本身就值得怀疑），优先切换到官方原生能力，退役自研重复件。

### 3.6 头号风险信号：本库最应该警惕的，恰恰是本库最擅长的

Cognition《Don't Build Multi-Agents》：并行子 Agent 各自独立决策，产生冲突、脆弱的输出；可靠性来自**上下文工程**（共享完整轨迹）而非更多 Agent。arXiv 2601.17311：固定预算下增加 Agent 数量存在**相变饱和点**，超过后性能不升反降。arXiv 2601.04170（Agent Drift）：Agent 系统的行为会在长交互中**退化**，需要独立量化指标追踪——这正是本库 EMI 想做但没做到的事。

**→ 决策**：§10 把"过度工程"列为与"衰变/失效"并列的一级风险，而非视"更复杂=更先进"。

---

## 四、生理学与解剖学精确原理

> 本节只陈述机制本身（教材级精度，来源见§13），工程映射在 §6。这是用户明确要求的前置步骤：「开始设计前，深度研读生理学、解剖学的医学教材或专业书籍论文」。

**4.1 神经系统分级控制与反射弧**：反射弧五要素——感受器→传入神经元（背根神经节）→整合中枢（脊髓/脑干）→传出神经元→效应器。单突触反射（膝跳反射）延迟最短；多突触反射（屈曲/交叉伸肌反射）经中间神经元、速度较慢但可整合多肌群。运动分级：皮层负责技巧性自主动作，基底神经节做动作选择闸门，脑干控制姿势/启动步态；**关键点**：节律性步态由脊髓局部**中枢模式发生器（CPG）**自主生成——半中心屈肌/伸肌互相抑制振荡，切断上下行连接仍可产生节律，高级中枢只是"调制"而非逐帧下令。

**4.2 自主神经系统：动态平衡而非开关**：交感/副交感**持续同时激活**，多数器官双重神经支配，净输出是"张力平衡点"。静息心率受副交感张力持续制动（固有~100bpm被压到~70bpm），血压受交感张力主导，平衡点可测量（心率变异性）。

**4.3 内分泌反馈：长回路负反馈，正反馈罕见且必须有终止条件**：HPA轴（CRH→ACTH→皮质醇）、HPT轴（TRH→TSH→T3/T4）都是长回路负反馈、双位点抑制上游、设定点本身可被动态调整。正反馈极罕见（分娩Ferguson反射），其安全性完全依赖**存在明确终止事件**——**没有终止条件的正反馈=失控**（发热螺旋、休克）。

**4.4 内稳态（Cannon）vs 应变稳态（allostasis）——设计中最关键的一对概念**：内稳态围绕固定设定点、偏差后负反馈纠正——"通过恒定实现稳定"。应变稳态（Sterling & Eyer 1988；McEwen）**"通过变化实现稳定"**——预测性、前馈式调节，大脑在需求到来*之前*主动调整设定点。McEwen提出"应变负荷"——反复/慢性调节的累积代价，"应变超载"直接致病（本态模型无法解释设定点没坏但反复调节代价过大的疾病）。**这一区分直接决定 §8 的监控哲学**：不能只做"偏离阈值才反应"的被动纠错，要做"预判负荷趋势、主动前移干预"的应变式设计。

**4.5 免疫系统：双重耐受检查+免疫记忆**：固有免疫快速非特异、无记忆；适应性免疫（B体液/T细胞）慢但高特异、产生记忆。自我/非我判别靠MHC（MHC-I配CD8，MHC-II配CD4）。**耐受是两级检查**：中枢耐受（胸腺/骨髓阶段删除自身反应细胞）+外周耐受（对逃逸细胞的第二道**独立**防线：无能化/调节T细胞/删除）——自身免疫病=两级耐受**同时**失效。**关键设计点**：耐受检查必须是两条独立通路，不能自己检查自己（对应§2.2循环依赖问题）。

**4.6 记忆巩固：双时间尺度+海马-皮层对话**：巩固分两尺度——突触巩固（分钟-小时，依赖蛋白质合成的晚期LTP，局部）；系统巩固（数周-数年，记忆逐渐从依赖海马转移到分布式新皮层）。慢波睡眠期间，海马尖波涟漪嵌套在皮层慢振荡与丘脑皮质纺锤波中，构成"海马-新皮层对话"，主动把近期痴迹回放进皮层。

**4.7 器官冗余与功能储备——储备掩盖早期损伤**：肾储备——全肾功能要到约50%肾单位丢失才开始下降，基础指标正常时损伤可能已很严重；肺储备——约50%肺循环被阻塞前肺动脉压才升高。共同原理：**冗余带来优雅降级，但代价是"基础指标正常"这一信号本身会掩盖早期损伤**——冗余系统必须监控"储备消耗趋势"而非仅监控"当前是否故障"。

**4.8 伤口愈合四阶段——系统自愈的时序模板**：止血（即刻-2天）→炎症（数天-1周，清创）→增殖（3天-2周，重建）→重塑（3周-12个月，抗张强度恢复至原有**约80%，永不到100%**）。**设计教训**：故障恢复必须按此顺序（先止损、再诊断、再重建、再强化），且要接受"修复后的系统通常达不到从零设计的理论强度"——这是正常的健康修复，不是失败。

**4.9 昼夜节律与睡眠——周期性"离线"是主动维护，不是浪费**：SCN由CLOCK/BMAL1—Per/Cry反馈环驱动，固有周期~24.2小时，经光每日校准。睡眠期间淋巴系统主动清除代谢废物；突触稳态假说（Tononi & Cirelli）认为清醒净增强突触、睡眠下调至可持续基线——"这是为可塑性付出的代价"。许多过程在睡眠中是**上调**而非停止。

**4.10 演化包袱——不该被模仿的清单**：喉返神经因胚胎期主动脉弓牵连绕远路（长颈鹿约4.6米，超出直连所需约7倍）——纯路径依赖，非最优设计。视网膜倒装——光感受器背光排列，视神经必须穿透视网膜形成盲点。**核心教训**：软件不受"渐进修改、不能重新设计"的演化约束——**不要因为"以前是这么接的"就保留一个绕远路的调用链、一个结构性盲区的接口朝向、或一个新旧组件速度不匹配的耦合**。这是人体被困住、而工程可以自由修正的地方。

---

## 五、控制论与计算机科学基础

> 让 §4 的生物类比获得工程严谨性，而非停留在比喻层面。标注 🟢直接可用 / 🟡概念性但非组件 / 🔴部分过时，来源见§13。

**5.1 经典控制论——Ashby必要变异度定律 🟡**：调节器能控制系统的前提是**调节器自身的响应变异度 ≥ 干扰的变异度**（"唯变异度能吸收变异度"）。是本库监控层的**设计约束**，不是可直接实现的组件：如果监控/纠错机制的应对花样比它要处理的失效模式少，系统必然失控。

**5.2 Subsumption架构与快慢双系统 🟢**：Brooks用分层反应式行为取代中心化规划，对应§4.1反射弧"快通路"。现代对应是**Talker-Reasoner双系统架构**（2024 NeurIPS）——直觉/缓存路径 vs 推理/工具调用路径的显式路由，是本库"何时用便宜模型/缓存Skill、何时用完整Agent派遣"决策的直接工程模板。

**5.3 互补学习系统理论（CLS） 🟢**：海马（快速记录具体情节，不覆盖旧知识）+新皮层（缓慢提炼统计规律）分工，为避免灾难性干扰——是本库"分层记忆"设计的理论依据，2025年多篇论文已直接以CLS理论指导LLM Agent记忆架构。

**5.4 记忆增强Agent框架 🟢**：CoALA给出工作/情节/语义/程序四类记忆标准分类；MemGPT/Letta走"Agent自主管理分级内存"路线；Generative Agents的"反思"机制是情节→语义巩固的具体实现；Voyager的可执行代码技能库对应程序记忆；A-MEM的Zettelkasten式自链接笔记直接对应本库wikilink结构。**共同短板：自动巩固目前都靠脆弱的LLM摘要式heuristic实现**，不要过度承诺"睡眠回放"式巩固的可靠性。

**5.5 人工免疫系统（AIS） 🟡→🔴**：自体/非自体判别、危险理论等immune-inspired异常检测**已部分被深度学习方法超越**——高维场景假阳性高，2025综述称现状为hybrid化用于IoT/零日攻击niche场景。**建议**：借用§4.5概念框架指导设计，具体实现用主流ML/规则引擎，而非重新发明NSA/DCA算法。

**5.6 生物冗余式容错分布式系统 🟢**：Erlang/OTP"let it crash"——进程隔离失败、监督者按策略重启（one-for-one/one-for-all）；断路器/舱壁隔离是同一思想现代形态。文献明确将生物冗余与拜占庭容错并列。**直接可用**，Netflix/Amazon生产验证多年。

**5.7 层级化多Agent控制 🟢**：黑板架构——专家Agent向共享黑板自助发布/订阅；HTN——管理者自顶向下分解、工作者执行。2025文献指出：**层级化协同的开销随Agent数量超线性增长**，分层收益仅在任务可并行时成立（约80%增益上限）——与§3.1"读多写少才并行"结论一致。

---

## 六、生物→控制论→工程 映射表

> 核心交付物。每一行必须能同时回答"§4 哪个精确机制"+"§5 哪个控制论形式化"+"落到 `.claude/` 哪个现有文件"——三者缺一即不采纳（防止重演「行动生命体」式松散隐喻）。

| # | 生理机制 (§4) | 控制论形式化 (§5) | 现有 `.claude/` 对应件 | 现状诊断 | 本方案动作 |
|:--:|------|------|------|------|------|
| 1 | 反射弧/CPG分级 (4.1) | Subsumption/Talker-Reasoner (5.2) | `agent-dispatch.md` 派遣矩阵 | 仅按文件数/复杂度分级，未区分读/写性质（3.1） | 新增"连贯性风险位"：写多/主观判断任务强制单Agent，不论文件数 |
| 2 | 自主神经张力平衡 (4.2) | 双回路持续平衡控制 (5.1) | `model-strategy.md` 4档模型路由 | 离散级联fallback（opus→sonnet→haiku 断崖切换） | 改为连续张力式路由：按任务复杂度实时混合，而非阈值跳变 |
| 3 | 长回路负反馈+正反馈终止条件 (4.3) | 经典负反馈+终止约束 | `self-evolution.md` 双环冷却倍增器（同文件×3.0/同维度×2.0） | 倍增器是正反馈式升级，需检查是否有复位条件 | 审计冷却倍增链是否有"应变超载后复位"机制，无则补 |
| 4 | 内稳态 vs 应变稳态 (4.4) | 预测性前馈+累积负荷追踪 (4.4) | EMI/知识库健康分 | **反应式、静态阈值，且已证实是objective hacking（§2.2）** | 改为应变式：追踪"连续N天钩子沉默""健康分下降速率"等趋势型累积负荷，预警发生在阈值*之前* |
| 5 | 双重独立耐受+免疫记忆 (4.5) | Self/non-self+两条独立验证通路 (5.5) | `compliance-monitoring.md` 操作前/后双重监察 | 概念正确，但监控者与被监控者共享同一钩子失效路径——本质是单通路（§2.2） | 钩子健康检查移出钩子系统本身，用独立调度（cron/ScheduleWakeup）执行 |
| 6 | 海马-皮层对话/系统巩固 (4.6) | CLS/CoALA四类记忆 (5.3/5.4) | Event Store（拟海马）→wiki L2（拟新皮层） | Event Store冻结23-33天="顺行性遗忘" | Phase 0恢复写入路径；补A-MEM式supersede检测；建立真实夜间巩固任务 |
| 7 | 器官储备掩盖早期损伤 (4.7) | 储备消耗趋势监控 | token预算分级/`agent-team-protocol.md`阈值 | 仅监控当前值是否越过悬崖阈值（<200K/<80K/<50K） | 增加"储备消耗速率"二级指标，趋势下降先于触底预警 |
| 8 | 伤口愈合四阶段 (4.8) | 分阶段故障恢复协议 (5.6) | 目前无形式化事件响应流程 | 本次发现的钩子死亡无固定处理流程 | 新增"系统自愈协议"：止血(隔离坏钩子)→清创(诊断)→重建(修复验证)→重塑(复盘+加固) |
| 9 | 昼夜节律/强制性维护 (4.9) | 周期性离线维护窗口 | 无现存机制；`ScheduleWakeup`/`CronCreate` 可用但未用于此 | 衰变23-33天无人发现，根因是无主动周期检查 | 建立每日强制巡检（Event Store写入验证/钩子存活探针/健康分复算），非可选项 |
| 10 | 生物冗余/监督树+断路器 (5.6) | let-it-crash+主管重启+断路器 | Agent spawn 失败处理 | 503失败43次/14天后**静默**降级，无告警无断路器 | 连续N次503开断路器→暂停派遣并**显式告警**；半开探测恢复；one-for-one重启 |
| 11 | Ashby必要变异度 (5.1) | 响应花样必须≥失效花样 | 62个合规触发点+17维进化检测 | 数量庞大，但关键失效（钩子死亡）未被任一触发点覆盖——数量多≠变异度够 | 补齐"元层失效"这一类（监控系统自身失效），而非继续新增同类型触发点 |
| 12 | 演化包袱审计 (4.10) | 工程可自由重构，无需负重前行 | `.claude/scripts/`（~80个）+982 Skills（仅179已验证） | 大量脚本/维度/Skill无法确认是否仍被调用或有下游消费者 | 建立"废用审计"：N天零调用+无下游消费者+文档存在但未接线 → 标记退役候选，纳入`/lint`常规扫描 |

---

## 七、本体重定义

### 7.1 为什么这是本体转变，而非功能升级

用户提出的转变——从"Obsidian 知识库工作流"到"AI Agent 生态系统"——本质是把系统从"被 AI 辅助的工具"重新定性为"接受人类治理的自主系统"。[[洞察/个人AI知识-行动生命体]] 在 2026-05-15 已经提出这一定性（"认知-行动操作系统"），但停留在反思层面。§2 的审计证明：**仅仅"定性"不会自动带来"自我检查"这一属性的真实存在**——过去两个月的执行证明，没有被独立验证的"自我检查"会在无人察觉时停止运作。因此本体重定义必须把"可验证性"写入定义本身，而不是作为附带假设。

### 7.2 定义候选对比

| | 内容 | 说明 |
|---|------|------|
| **用户原始提法** | "以obsidian+claude等为核心，功能全面、能力强大，能够自我进化、自我修正、自我检查、自我改进的AI agent生态系统或AI agent辅助扩展系统" | 方向正确，但"功能全面/能力强大"是结果性描述而非约束，"自我检查"缺少可验证性要求 |
| **本文档提案** | **"以 Obsidian + Claude Code 为核心载体，以生理学与控制论精确映射为设计校准依据，以可验证、可审计、抗静默失效为底线约束的自我进化、自我修正、自我检查、自我改进的个人 AI Agent 生态系统。"** | 见下方逐点差异说明 |

**逐点差异与理由**：

1. **去掉"功能全面、能力强大"作为定义性描述**——这是结果不是约束，且 §3.6 显示"更全面更强大"恰恰是 2026 行业头号风险信号（过度工程）。复杂度的正确态度是"必要才增加"，不是把"全面强大"当作追求目标。
2. **新增"以生理学与控制论精确映射为设计校准依据"**——把"借鉴人体设计"从灵感来源提升为方法论约束：任何新机制要被以"仿生"之名采纳，必须能回答"§4 哪个精确机制 + §5 哪个控制论形式化 + §6 映射表哪一行"，否则不采纳。防止「行动生命体」式的松散隐喻反复出现而不落地。
3. **新增"可验证、可审计、抗静默失效"**——这是 §2.2 发现驱动的最重要新增。"自我检查"如果不能被独立验证，就不是能力，是声明。三个词分别对应：**可验证**=有独立于被检查对象的验证路径（4.5 双重耐受）；**可审计**=有留痕、可事后复盘（4.6 记忆巩固+Event Store）；**抗静默失效**=衰变必须被主动发现，不能靠"没人抱怨=没问题"（4.9 强制周期维护）。
4. **保留"AI agent生态系统"定名**（不采用"或"后半句"AI agent辅助扩展系统"）——本次审计显示系统已具备生态系统特征（982个Skill、17维进化、多Agent团队待激活、独立的Event Store与合规层），"辅助扩展"低估了现状；但也不用"或"制造定义模糊，避免后续设计目标漂移。

### 7.3 隐喻收紧：从"器官/肌肉"到"神经-内分泌-免疫-记忆"四轴模型

「行动生命体」用"器官/肌肉"类比外部工具（Codex=手，本系统=大脑）。这类一对一器官映射**无法被证伪**——"哪个工具算哪个器官"可以无限争论却不产生工程决策，与 §2.2 "目标造假"是同一类风险（叙事精巧但不可验证）。

本文档改用**四条控制轴**分类系统的任一组件，而不问它属于哪个工具：

| 轴 | 对应 §4/§5 | 回答的问题 |
|------|------|------|
| **神经轴**（分级路由） | 反射弧/CPG (4.1) + Subsumption (5.2) | 这个操作该走"脊髓级"缓存/自动化，还是"皮层级"Agent deliberation？ |
| **内分泌轴**（调节反馈） | HPA轴/内稳态-应变稳态 (4.3/4.4) | 这个信号该用负反馈+终止条件治理，还是需要应变式预测？ |
| **免疫轴**（安全容忍） | 自我/非我+双重耐受 (4.5) | 这个校验需要独立双重验证吗？过去的违规是否被记成"免疫记忆"供下次更快识别？ |
| **记忆轴**（巩固） | CLS/系统巩固 (4.6) | 这是该留在情节记忆（Event Store/log.md）的原始记录，还是该被巩固为语义记忆（wiki概念/实体页）？巩固节奏是什么？ |

一个工具（如 Claude Code）可以同时承担四轴的不同角色；四轴模型问的是"这个具体机制在做什么调节"，而不是"这个工具像哪个器官"——前者可检验，后者是叙事。

### 7.4 明确的非目标（防止范围蔓延）

- **不**物理构建 Omega——v12.0 已决策，本文档尊重该决策。
- **不**模拟情绪/意识等主观属性——用户自身调研已指出此边界，予以采纳（§一致）。
- **不**用人工免疫算法（NSA/DCA）重新发明异常检测——§5.5 结论，用主流ML/规则引擎实现，只借用概念框架。
- **不**把"增加 Agent 数量"或"增加规则触发点数量"本身当作进化的度量——§3.6/§10，度量是效能提升，不是复杂度。

---

## 八、架构蓝图：七个子系统

> 每个子系统标注：目的 / 依附现有文件（不新建平行系统）/ 具体设计 / 验收标准。全部子系统的确认与落地遵循 §12 治理流程，不因写入本文档而自动生效。

### 8.1 神经路由层——分级快慢双径

**目的**：让"便宜且频繁"的操作走缓存/自动化路径，"复杂且稀有"的操作才升级到完整 Agent 推理，且升级判断包含"连贯性风险"维度。
**依附**：`agent-dispatch.md` 派遣矩阵、`skill_router.py`/`skill_activation_router.py`。
**具体设计**：现行矩阵按文件数分级(≤4直接/5-14 Writer+Critic/≥15 Researcher链)保留，**新增读写性质位**：写多+主观判断(如wiki页面文风/取舍)→无论文件数强制单Agent；读多+可并行(如批量摘要/多源检索)→维持现行并行分级。新增"缓存命中直答"：重复模式的请求由路由层直接返回缓存结果，不经过完整Agent决策链——这是CPG式"无需皮层介入的节律执行"。
**验收标准**：抽样30次近期操作，"写多任务被错误并行化"实例数=0；缓存命中率有真实数据（非声明）。

### 8.2 内分泌调节层——应变式监控取代静态阈值

**目的**：把EMI/健康分从"反应式打分"改造成"预测式负荷追踪"，修复§2.2发现的objective hacking。
**依附**：`execution_mode_tracker.py`、`freeze_enforcer.py`、`model-strategy.md`。
**具体设计**：**必须先做**——把`freeze_enforcer.py`接到真实EMI输出（当前读的是不相关的`evolve_force_log.jsonl`）——这不是新设计，是修复已声明但未接线的功能。新增"应变负荷"字段：连续N天关键信号（钩子/Event Store）沉默→负荷累加，累加值触发的预警比单点阈值更早。模型路由从离散级联（opus→sonnet→haiku跳变）改为按任务复杂度连续加权选择，参考§6第2行。
**验收标准**：`freeze_enforcer.py`与EMI的联动可用一次真实的模拟衰变触发验证（而非文档声明）；应变负荷字段在本文档写入30天后有真实累积数据可查。

### 8.3 免疫安全层——独立双重验证+违规记忆

**目的**：让"自我检查"具备§4.5的两条独立通路，而非监控者与被监控者共享同一失效面。
**依附**：`compliance-monitoring.md`、`hook_health_monitor.py`。
**具体设计**：钩子健康检查**必须**由独立于PreToolUse/PostToolUse钩子体系之外的机制执行——用`ScheduleWakeup`/`CronCreate`定期主动探测（"外周耐受"角色），不能只靠钩子体系自证健康（"中枢耐受"单独失效即全灭）。违规记录应反哺进"威胁模式库"：同类违规二次出现时检测应更快更严（免疫记忆），当前只是记录不反哺。
**验收标准**：制造一次可控的钩子故障（测试环境），确认独立探测机制能在钩子体系完全瘫痪的情况下仍然报警。

### 8.4 记忆巩固层——恢复海马、正式化巩固

**目的**：修复Event Store冻结（"顺行性遗忘"），并把"情节→语义"巩固从偶发变为例行。
**依附**：Event Store相关信号文件、`chroma_memory.py`/`mirror_memory.py`/`skill_memory.py`、`wiki/log.md`。
**具体设计**：**Phase 0优先项**——诊断并恢复Event Store写入路径（很可能是某个钩子/脚本静默异常，需要日志排查，不是重新设计）。三个记忆脚本（chroma/mirror/skill_memory）功能疑似重叠——按§3.5建议先审计是否可以退役为Anthropic原生memory tool或合并为一。新增A-MEM式supersede检测：新wiki页面创建时检查是否与既有页面语义重复/取代关系，自动提示合并而非留存重复。巩固节奏形式化为§8.7的夜间任务，而非"有空的时候"。
**验收标准**：Event Store连续14天零中断写入；三个记忆脚本审计结论落地（合并/退役/保留理由三选一并执行）。

### 8.5 冗余容错层——监督树+断路器

**目的**：修复Agent spawn的503静默降级，让故障"响亮地崩溃、快速地恢复"而非"安静地劣化"。
**依附**：Agent派遣重试逻辑（当前分散在各调用点，无统一层）。
**具体设计**：引入**断路器**——滑动窗口内连续N次503（如5次/10分钟）→断路器开启，暂停该能力的新派遣尝试，**显式记录+对用户可见的告警**（而非静默retreat）。半开探测：断路器开启后按退避策略（如30s/2min/10min）尝试单次探测请求，成功则关闭断路器恢复正常派遣。one-for-one重启策略：单个Agent失败只重启该Agent，不影响同批次其他Agent（现有L1 spawn-and-die已部分具备此特性，需显式文档化+验证）。
**验收标准**：过去14天的43次503事件复盘，用断路器规则重放，确认"用户会被告知能力已降级"这一结果在规则下成立。

### 8.6 自愈协议层——伤口愈合四阶段事件响应

**目的**：给"系统检测到自身故障后该做什么"一个形式化、可重复的流程，而不是每次靠临时排查。
**依附**：新增运行手册（可落地为`.claude/rules-t2/self-healing-protocol.md`，具体文件由§12治理流程决定是否/何时创建）。
**具体设计（四阶段，严格顺序）**：①**止血**——检测到关键失效（如钩子零记录超过阈值）→立即隔离受影响功能，避免依赖它的下游做出"看似成功"的假判断（`med_completion_gate.py`的fail-open设计已部分具备此思想，需推广）；②**清创**——收集失效窗口内的日志/信号文件时间线，定位根因（不猜测，要有证据链）；③**重建**——修复+在受控条件下验证（非直接判定"看起来好了"，需§8.3独立验证通路确认）；④**重塑**——写入`wiki/log.md`复盘，评估该失效类型是否需要成为新的合规触发点（§6第11行"元层失效"覆盖）；接受修复后系统的可靠性通常低于"从未坏过"的理论值，这是正常状态，不是遗留失败。
**验收标准**：本次审计发现的钩子死亡问题走完四阶段并留痕，作为该协议的第一个真实案例。

### 8.7 昼夜维护层——强制性周期巡检

**目的**：把"发现衰变"从被动（等健康分骤降或用户抱怨）变为主动（每日结构性检查）。
**依附**：`ScheduleWakeup`/`CronCreate`（已可用工具）、`kb_registry.py --summary`、健康分复算脚本。
**具体设计**：每日一次巡检任务，验证Event Store最近写入时间戳在阈值内、验证关键钩子在过去24h内有触发记录、复算健康分、扫描废用候选（§6第12行）。巡检**本身不做修复**，只负责发现+记录+按严重度决定是否需要用户介入——修复走§8.6自愈协议。巡检结果写入固定位置（如`wiki/log.md`的"每日巡检"小节），可被追溯审计。
**验收标准**：巡检任务连续运行7天，产出7条可追溯记录；本次审计发现的三个衰变信号（钩子/EventStore/503）如果巡检早于本次对话运行，应能被提前发现——用这一反事实检验巡检设计是否足够。

---

## 九、效能评估体系

> 基于用户自己的调研草稿（三层：基础运行/任务能力/长期鲁棒 + 对照组方法论）精炼而成，**指标全部锚定到本库已有的可获取信号**，不新建平行指标体系（新指标体系本身就是§10的一个反模式风险）。

### 9.1 第一层：基础运行效能（"生命体征"）

| 指标 | 数据来源（已存在） | 现状 | 目标 |
|------|------|------|------|
| Token/任务成本 | Agent调用日志 | 未系统追踪 | 建立基线后设定预算红线 |
| Agent spawn成功率 | 503错误日志 | 14天43次失败，成功率分母缺失 | 断路器上线后连续追踪 |
| 钩子存活率 | `hook-fire-log.jsonl` | 2026-07-08起=0（已死） | Phase 0后100%，之后≥99%/日 |
| 知识库健康分 | lint 健康巡检 | 87→~60 | 恢复至≥85并追踪**趋势**而非单点 |

### 9.2 第二层：任务能力效能（"器官功能"）——对应用户草稿五个仿生子模块

| 仿生子模块 | 本库对应指标 | 数据来源/依附章节 |
|------|------|------|
| 记忆模块 | Event Store连续性、A-MEM supersede命中率、跨会话知识召回准确率抽样 | §8.4 |
| 规划决策 | agent-dispatch实效性评分（`score_card.py`已存在） | §8.1 |
| 感知-执行闭环 | 工具调用失败后的重试/修正成功率 | §8.5 |
| 稳态调控 | 应变负荷指标（§8.2新增）、EMI（修复后） | §8.2 |
| 多模块协同 | Agent Team任务完成率 vs 单Agent基线（v12.0 Phase 0已设计此对照实验，直接复用） | v12.0 §Phase 0 |

### 9.3 第三层：长期鲁棒效能（"免疫力/自愈力"）

| 指标 | 说明 |
|------|------|
| 故障容错成功率 | §8.5断路器规则重放43次历史503事件的"用户被正确告知"比例 |
| 异常抵抗能力 | 模糊/异常输入下的崩溃率（现有anti-hallucination V1-V9可作基线） |
| 废用清理率 | §6第12行"废用审计"清单的季度清理执行率 |
| **静默失效发现时延**（新指标） | 从衰变开始到被巡检/告警发现的天数——本次审计的钩子问题是数天、Event Store是23-33天。目标是持续压缩这个数字，而不是幻想"零衰变"（不现实，§4.7器官储备原理已说明储备必然掩盖早期损伤，能做的是缩短"掩盖期"） |

### 9.4 对照组方法论（采纳用户草稿，锚定到本库真实场景）

| 组 | 定义 |
|------|------|
| 空白对照 | 单Agent直接模式（v12.0 Phase 0已设计的基线测量，直接复用不重做） |
| 行业对照 | `obsidian-second-brain`式"轻量vault-first"方案（§3.2）——用同一批10篇`raw/`文件分别跑本库管道与轻量对照，比较耗时/token/遗漏率 |
| 实验组 | 本方案落地后的`.claude/`管道 |

**红线**（采纳用户草稿）：算力开销比基线提升>30%且任务完成率提升<10% → 判定该次改动低效，回退；连续长任务运行后性能下降>40%且无自动纠正 → 判定稳态调控失败。

### 9.5 综合得分公式

```
综合得分 = 任务完成率×40% + 单位任务算力节省率×25% + 长期运行性能衰减降幅×20% + 故障容错成功率×15%
```

季度复算一次，**趋势比单次得分更重要**（§4.4应变稳态原则——反应式单点打分正是EMI已经失败的模式）。

---

## 十、反模式与自指风险

> 本方案自己也可能变成第四个"漂亮但没落地"的蓝图，或变成"目标造假"的下一个受害者。本节明确红线。

### 10.1 反模式清单

| 反模式 | 描述 | 本库已发生的具体实例 | 防范 |
|------|------|------|------|
| 目标造假 (objective hacking) | 指标看起来在控制，从未真正接线 | EMI s2/freeze_enforcer（§2.2） | 任何新指标上线前必须有一次"故意制造失效并验证指标能捕获"的演练（§8.2/8.3验收标准已含此要求） |
| 叙事精巧但不可验证的隐喻 | "器官/肌肉"式一对一类比无法证伪 | 「行动生命体」的松散比喻（§7.3已收紧） | §6映射表的三要素强制要求（精确机制+形式化+现有文件） |
| 过度工程/多Agent崇拜 | 把"更多Agent/更多层"当作进化本身 | v12.0/Ω-Loop/Omega三代蓝图零处引用反过度工程文献 | §3.6/§7.4非目标条款 |
| 静默降级 | 故障发生但系统"优雅"地不告诉任何人 | Agent spawn 503静默retreat（§8.5） | 断路器必须显式告警，"安静的健壮"在本方案中不算健壮 |
| 覆盖率错觉 | "验证脚本存在"被误当作"验证被执行" | `task_completion_gate.py`仅覆盖3个历史任务且未接入hook | §12治理要求新机制上线时明确标注"接入路径"，不接入hook的验证脚本不能被称为"门" |
| 规则堆叠而不做减法 | 62个触发点/17维/982 Skill持续增长，废用件从不退役 | 本次审计未发现任何主动退役记录 | §6第12行废用审计，纳入`/lint`常规项 |

### 10.2 本方案的自指保护

- 本文档提出的每一项新机制，落地前必须先满足§8各小节写下的"验收标准"——不满足则不算完成（沿用`anti-execution-mode.md`的物理门控精神，而非文本自觉）。
- 本文档 **12 个月后必须接受一次外部（非本文档作者视角）复核**：逐项核对§8七个子系统的验收标准是否达成，未达成的诚实标注"未完成"而非悄悄移除该条目。
- 若§9.4的对照实验显示"仿生改造"综合得分不如轻量对照组，本方案的结论应是**承认并简化**，不是加更多仿生机制去补救——这是对§10.1"过度工程"反模式的自我约束。

---

## 十一、分阶段路线图

| Phase | 内容 | 前提 | 预计工作量 | 用户审批要求 |
|:--:|------|------|:--:|:--:|
| **Phase 0：止血** | 恢复Event Store写入、诊断钩子死亡原因并修复、`freeze_enforcer.py`接线真实EMI、Agent spawn断路器上线 | 无（修复已决策功能，非新设计） | 数天 | 可**立即执行**——这是修复不是新设计，符合"wiki/由Claude全权维护"的既有授权精神；涉及`.claude/`脚本部分仍走既有确认流程但审批门槛更低 |
| **Phase 1：核对** | 正式核查v12.0待审批状态——是否批准/修改/搁置；Ω-Loop已建部分与本文档§2的差异清单确认 | Phase 0完成 | 1次决策会话 | **需要用户明确批复**（v12.0本身已等待6周，不能再无限期悬置） |
| **Phase 2：校准** | 按§6映射表逐行落地（每行独立，可分批）；优先级：先做§8.2(应变监控)+§8.3(独立验证)+§8.7(强制巡检)——这三项直接防止"再来一次静默衰变" | Phase 1核对结果 | 数周，逐项确认 | 每项改动遵循`self-evolution.md`既有确认/冷却协议，**不绕开** |
| **Phase 3：做减法** | §6第12行废用审计；§3.5原生能力替代自研重复件（记忆脚本审计） | Phase 2部分完成 | 持续性，纳入`/lint`常规项 | 退役建议逐项经用户确认，不自动删除 |
| **Phase 4：重定义落地** | §7本体重定义正式写入`CLAUDE.md`（版本号+定义更新）；本文档转为`stable`状态 | Phase 0-2稳定运行≥30天且§9指标有真实趋势数据 | 半天 | 需要用户最终批准——这是身份声明，理应最谨慎 |

> 🔴 **Phase 0 实际执行记录（2026-07-13，部分完成——详见 [[log|wiki/log.md]] 同日 audit 条目）**：
> - **钩子静默失效诊断**：✅ 完成，且比本文档 §2.1 原描述更彻底——本会话（Claude Agent SDK child session，`CLAUDE_CODE_CHILD_SESSION=1`，大概率由 Claudian Obsidian 插件启动）现场对 Read/Write|Edit/Bash 三个 matcher 各做一次真实工具调用+前后 diff 比对，`hook-fire-log.jsonl`/`event-store.jsonl` 均零新记录——证实钩子在**本会话类型下**完全不触发，非零星失效，也不是"没有注册钩子"（settings.json 中确有真实 hooks 配置块）。是否为所有会话类型的普遍限制，还是 child session 特有，本会话内无法验证；用户裁定"等我测完顶层 CLI 会话再定"——`med_mode_hook.py` 是否补注册 `Write|Edit` matcher 因此暂缓，未改代码。
> - **Event Store 写入路径**：⚠️ 未"恢复"，因为诊断后发现它不是可独立修复的故障——`event_store.py` 脚本本身功能正常（探针写入成功），冻结是钩子层不触发的下游症状；真正的组织事件（`hook.pass`）最后一条为 2026-07-08 19:04，此后的两条记录（07-10/07-12）是手动/探针调用，非钩子自动产生。
> - **`freeze_enforcer.py` 接线真实 EMI**：⏭️ 按用户明确许可跳过（本条目本身标注为非阻塞项+本次时间优先给真实科研任务）。
> - **Agent spawn 断路器**：⏭️ 完整断路器设计未做——✅ 已应用一条轻量文本澄清（"写入 log.md 不等于已告知用户"，Agent 降级须在可见回复正文单独声明，已标注为非物理门）。诊断证实 503 降级已是 2026-06 至今持续 6+ 周的**常态**而非偶发。
> - **`med-capability-card.md` 逐条核对**：✅ 完成——表中 5 行"执行机制"全部依赖 PreToolUse hook，鉴于上述钩子不触发实测结果，全部"🟢 硬阻断"标注在本会话类型下均不成立；✅ 修正已应用（新增"运行时校验"列）。

**关键排序原则**（§4.8伤口愈合的直接应用）：**止血必须在重塑之前**——不能跳过Phase 0直接讨论Phase 4的身份重定义，即使身份重定义是用户最初提出这个任务的直接动机。

---

## 十二、治理与自指保护

- 本文档是**提案/指导文档**，不是执行授权。`wiki/` 层归 Claude 全权维护（可创建本文档本身），但 `.claude/` 层是"共同演进"——本文档中涉及 `.claude/` 脚本、规则、钩子的任何具体改动，仍必须逐项走 `self-evolution.md` 已有的"展示→等待→确认→执行"确认流程与双环冷却，**本文档不构成绕过该流程的授权**。
- Phase 0（止血类修复）性质上是"修复已经被v12.0/Ω-Loop决策+部署过的功能"，而非新设计——按现有惩罚/冷却机制的精神，修复性变更的审批门槛应低于新增性变更，但仍需在执行后的日志中明确留痕（§8.6自愈协议第4阶段"重塑"）。
- 本文档中提出的§3.4 PACE式统计验收门（≥5组可比历史数据方可确认规则改动"有效"），一旦被采纳，**适用于本文档自己未来的修订**——即本文档本身也不能仅凭"感觉更好了"被判定为成功。
- 若12个月复核（§10.2）发现本文档提出的机制大量停留在"写了但未接线"状态，该发现本身应被诚实记录，不应归因于"用户没批准"而回避——参照§2的诊断标准同样适用于对本文档的自我评估。

---

## 十三、附录：引用来源

### 13.1 行业与Agent架构（§三）

- How and when to build multi-agent systems — LangChain, https://www.langchain.com/blog/how-and-when-to-build-multi-agent-systems
- How Anthropic built its multi-agent research system, https://theaiengineer.substack.com/p/how-anthropic-built-multi-agent-deep
- AI Agent Orchestration in 2026 — enterprise guide, https://viston.tech/ai-agent-orchestration-in-2026-moving-from-pilots-to-enterprise-wide-execution/
- obsidian-wiki（Karpathy LLM-Wiki范式实现）, https://github.com/ar9av/obsidian-wiki
- obsidian-second-brain, https://github.com/eugeniughelbur/obsidian-second-brain
- claude-obsidian AI second brain, https://agricidaniel.com/blog/claude-obsidian-ai-second-brain
- MemGPT: LLMs as Operating Systems — arXiv 2310.08560, https://arxiv.org/abs/2310.08560
- AI Agent Memory Systems 2026 Guide, https://jobsbyculture.com/blog/ai-agent-memory-systems-guide-2026
- Choosing How to Remember: Adaptive Memory Structures — arXiv 2602.14038, https://arxiv.org/pdf/2602.14038
- A Comprehensive Survey of Self-Evolving AI Agents — arXiv 2508.07407, https://arxiv.org/abs/2508.07407
- Awesome-Self-Evolving-Agents, https://github.com/EvoAgentX/Awesome-Self-Evolving-Agents
- PACE: Anytime-Valid Acceptance Tests for Self-Evolving Agents — arXiv 2606.08106, https://arxiv.org/pdf/2606.08106
- Building agents with the Claude Agent SDK — Anthropic, https://www.anthropic.com/engineering/building-agents-with-the-claude-agent-sdk
- Managing context: memory tool + context editing — Anthropic, https://www.anthropic.com/news/context-management
- Agent Skills overview — Claude Platform Docs, https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview
- Don't Build Multi-Agents — Cognition, https://cognition.com/blog/dont-build-multi-agents
- The Multi-Agent Trap — Towards Data Science, https://towardsdatascience.com/the-multi-agent-trap/
- Phase Transition for Budgeted Multi-Agent Synergy — arXiv 2601.17311, https://arxiv.org/pdf/2601.17311
- Agent Drift: behavioral degradation over extended interactions — arXiv 2601.04170, https://arxiv.org/pdf/2601.04170

### 13.2 控制论与CS基础（§五）

- Ashby, *An Introduction to Cybernetics* (1956), http://pcp.vub.ac.be/books/IntroCyb.pdf；*Design for a Brain* (1952)
- Slogar, "AI is Turning Us All into Managers: A Cybernetics Perspective" (2025), https://medium.com/cyberneticum/ai-is-making-managers-of-us-all-a-cybernetics-perspective-on-the-future-of-management-25558fb30ffd
- "Develop AI Agents for System Engineering in Factorio" — arXiv 2502.01492, https://arxiv.org/pdf/2502.01492
- Brooks, "A Robust Layered Control System for a Mobile Robot" (1986), DOI 10.1109/JRA.1986.1087032
- "Agents Thinking Fast and Slow: A Talker-Reasoner Architecture" — arXiv 2410.08328, https://arxiv.org/pdf/2410.08328
- "Agentic Large Language Models, a survey" — arXiv 2503.23037, https://arxiv.org/pdf/2503.23037
- McClelland, McNaughton & O'Reilly, *Psychological Review* 102(3):419-457 (1995), DOI 10.1037/0033-295X.102.3.419
- "Position: Episodic Memory is the Missing Piece for Long-Term LLM Agents" — arXiv 2502.06975, https://arxiv.org/pdf/2502.06975
- ICLR 2026 "MemAgents" workshop proposal, https://openreview.net/pdf?id=U51WxL382H
- Sumers et al., "CoALA" — arXiv 2309.02427, https://arxiv.org/abs/2309.02427
- Park et al., "Generative Agents" — arXiv 2304.03442, https://arxiv.org/abs/2304.03442
- Wang et al., "Voyager" — arXiv 2305.16291, https://arxiv.org/abs/2305.16291
- Chhikara et al., "Mem0" — arXiv 2504.19413, https://arxiv.org/abs/2504.19413
- Xu et al., "A-MEM" — arXiv 2502.12110, https://arxiv.org/abs/2502.12110
- Aickelin & Cayzer, "The Danger Theory and Its Application to AIS" — arXiv 0801.3549, https://arxiv.org/abs/0801.3549
- Hosseini et al., "AIS for Industrial Intrusion Detection: A Systematic Review" (2025), https://onlinelibrary.wiley.com/doi/full/10.1155/je/8408209
- "Generating detectors from anomaly samples via negative selection" (2025), *Scientific Reports*, https://www.nature.com/articles/s41598-025-20516-6
- Armstrong, "Making Reliable Distributed Systems in the Presence of Software Errors" (2003 PhD thesis)
- Nygard, *Release It!* (2007/2018)
- "Advancing System Performance with Redundancy: From Biological to Artificial Designs" — arXiv 1802.05324, https://arxiv.org/abs/1802.05324
- "Bioinspired Algorithms to Enhance Self-Healing and Fault Tolerance in Critical Software Systems" (2025), https://link.springer.com/chapter/10.1007/978-3-031-95127-5_21
- Hayes-Roth, "A Blackboard Architecture for Control," *Artificial Intelligence* 26(3) (1985)
- "PC-Agent: A Hierarchical Multi-Agent Collaboration Framework" — arXiv 2502.14282, https://arxiv.org/pdf/2502.14282
- "LLM-based Multi-Agent Blackboard System for Information Discovery" — arXiv 2510.01285, https://arxiv.org/abs/2510.01285
- "Online Learning of HTN Methods for Integrated LLM-HTN Planning" — arXiv 2511.12901, https://arxiv.org/pdf/2511.12901

### 13.3 生理学与解剖学（§四）

- StatPearls, *Monosynaptic Reflex*, https://www.ncbi.nlm.nih.gov/books/NBK541028/；*Withdrawal Response*, https://www.ncbi.nlm.nih.gov/books/NBK544292/
- PMC, CPG for Locomotion, https://pmc.ncbi.nlm.nih.gov/articles/PMC3567435/
- StatPearls, *Parasympathetic Nervous System*, https://www.ncbi.nlm.nih.gov/books/NBK553141/；Basic Human Physiology, ANS章节, https://iu.pressbooks.pub/humanphys/chapter/autonomic-nervous-system/
- Cleveland Clinic, HPA axis, https://my.clevelandclinic.org/health/body/hypothalamic-pituitary-adrenal-hpa-axis；HPT axis overview, https://www.sciencedirect.com/topics/neuroscience/hypothalamic-pituitary-thyroid-axis
- Oxytocin in Childbirth (Ferguson reflex), https://pmc.ncbi.nlm.nih.gov/articles/PMC8578887/
- "Clarifying the Roles of Homeostasis and Allostasis," PMC4166604, https://pmc.ncbi.nlm.nih.gov/articles/PMC4166604/
- Sterling, *Principles of Allostasis: Optimal Design, Predictive Regulation* (2004), https://scispace.com/papers/principles-of-allostasis-optimal-design-predictive-2ju1gxtc5i
- StatPearls, *Biochemistry, Autoimmunity*, https://www.ncbi.nlm.nih.gov/books/NBK576418/
- Immunopaedia, Central & Peripheral Tolerance, https://www.immunopaedia.org.za/immunology/advanced/2-central-peripheral-tolerance/
- Simply Psychology, Multi-Store Model, https://www.simplypsychology.org/multi-store.html
- Nature Neuroscience, "Systems Consolidation During Sleep," https://www.nature.com/articles/s41593-019-0467-3
- Renal Functional Reserve review, *AJP*, https://journals.physiology.org/doi/full/10.1152/ajpregu.00237.2020
- Liver regeneration review, PMC12308566, https://pmc.ncbi.nlm.nih.gov/articles/PMC12308566/
- StatPearls, *Pulmonary Vascular Resistance*, https://www.ncbi.nlm.nih.gov/books/NBK554380/
- Kitano, "Biological Robustness," PMC2013924, https://pmc.ncbi.nlm.nih.gov/articles/PMC2013924/
- StatPearls, *Wound Healing Phases*, https://www.ncbi.nlm.nih.gov/books/NBK470443/
- Frontiers, "SCN Circadian Mechanism," https://www.frontiersin.org/journals/neural-circuits/articles/10.3389/fncir.2024.1385908/full
- Tononi & Cirelli, "Sleep Function and Synaptic Homeostasis," https://www.sciencedirect.com/science/article/abs/pii/S1087079205000420
- StatPearls, *Physiology of Sleep*, https://www.ncbi.nlm.nih.gov/books/NBK482512/
- Acta Palaeontologica Polonica, "A Monument of Inefficiency" (喉返神经), https://bioone.org/journals/acta-palaeontologica-polonica/volume-57/issue-2/app.2011.0019/
- bioRxiv, "Origin of the Inverted Retina," https://www.biorxiv.org/content/10.1101/2022.10.04.510789v1.full

### 13.4 内部审计来源（§二、§一）

本次会话对以下文件的直接读取/审计：`.claude/rules-t2/self-evolution.md`、`.claude/rules-med/self-evolution-detail.md`、`.claude/rules-t2/agent-dispatch.md`、`.claude/rules-t2/agent-team-protocol.md`、`.claude/rules-t2/model-strategy.md`、`.claude/rules/anti-execution-mode.md`、`.claude/rules-t1/architecture-coordination.md`、`.claude/agents/*.md`、`.claude/cache/skill-registry.json`、`wiki/log.md`（尾部~150行）、[[洞察/v12.0多Agent知识库进化-最终构建总方案]]、[[洞察/Ω-Loop最终执行方案]]、[[洞察/个人AI知识-行动生命体]]、[[洞察/Agent自进化框架设计模式对比]]。

---

*创建于 2026-07-12 — 用户提出知识库工作流的本体转变（"Obsidian知识库工作流"→"AI Agent生态系统"），要求生物启发架构设计+2026行业最新研究+生理解剖学教材级依据。四路并行深度研究（行业趋势/CS控制论基础/医学生理解剖/知识库内部审计）后完成本方案。核心发现：该转变已是第三代尝试（行动生命体→v12.0→Ω-Loop），且当前运行时已发生静默衰变（钩子死亡/Event Store冻结/Agent spawn 503），本方案因此以"止血优先于重定义"为核心排序原则。*

