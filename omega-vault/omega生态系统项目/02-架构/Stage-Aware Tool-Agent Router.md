---
type: concept
tags: [omega-ecosystem, stage-aware-router, task-routing, tool-selection, task-stages]
created: 2026-05-15
updated: 2026-05-15
knowledge_stability: evolving
parent: [[Tool-Agent Router：最佳工具与最佳执行者选择器]]
related:
  - [[Dynamic Task Planner：动态任务规划器]]
  - [[Tool-Affordance Graph]]
  - [[Tool Reputation Ledger]]
  - [[Productive Agent Society]]
---

# Stage-Aware Tool-Agent Router

> **定位**：Standard Tool-Agent Router 解决了"这个任务用谁做"，但同一个任务的不同阶段对工具的要求截然不同。Stage-Aware Router 在标准 Router 的基础上增加了**阶段感知**——每个阶段使用不同的评分权重和选择策略。

---

## 一、为什么需要阶段感知

标准 Router 把整个任务当成一个整体来评分。但现实是：

```
任务：「搜文献→数据分析→写论文→投稿预填」

检索阶段：需要高召回率，宁可多搜不能漏
分析阶段：需要可重复性，代码必须能在沙箱中复现
写作阶段：需要结构清晰、引用准确、语言流畅
投稿阶段：需要安全、可预览、回滚
```

如果用一个统一的评分标准（如"成功率优先"）来处理所有阶段，会出现：
- 检索阶段选了"最稳定的工具"但召回率不够
- 投稿阶段选了"最快的工具"但不可回滚

**阶段感知 = 根据任务阶段动态调整评分权重和选择策略。**

---

## 二、任务阶段分类

### 2.1 通用阶段定义

| 阶段 | 英文 | 典型操作 | 优先级偏好 |
|------|------|---------|-----------|
| **感知/检索** | Perception | 搜索、爬取、文献检索、数据获取 | 召回率 > 速度 > 成本 |
| **提取/理解** | Extraction | PDF 解析、OCR、文本提取、实体识别 | 准确性 > 上下文容量 > 速度 |
| **分析/计算** | Analysis | 统计分析、建模、数据清洗、可视化 | 可重复性 > 速度 > 可解释性 |
| **综合/创作** | Synthesis | 写作、综述、报告生成、内容创作 | 质量 > 结构 > 速度 |
| **审查/验证** | Review | 事实检查、GRADE 评级、格式验证 | 准确性 > 完整性 > 速度 |
| **转换/格式化** | Transformation | 格式转换、文件处理、批量操作 | 保真度 > 批量能力 > 速度 |
| **操作/执行** | Execution | 代码运行、工具调用、浏览器操作 | 安全性 > 可回滚 > 速度 |
| **发布/交付** | Delivery | 投稿预填、文件保存、成果输出 | 安全性 > 预览能力 > 速度 |

### 2.2 阶段特定的评分权重覆盖

每个阶段覆盖默认的 12 维权重。未覆盖的维度使用默认值。

```yaml
stage_weights:
  perception:           # 感知/检索阶段
    task_fit: 0.25      # ↑ 检索专用工具优先
    success_rate: 0.15
    reputation: 0.10
    cost: 0.08
    speed: 0.12         # ↑ 搜索需要快
    context_window: 0.05
    automation: 0.10    # ↑ 自动搜索
    output_quality: 0.08
    risk_level: 0.03    # ↓ 搜索风险低，不重要
    rollback: 0.02
    skill_coverage: 0.05
    domain_fit: 0.12    # ↑ 学术/医学检索需要领域匹配

  extraction:           # 提取/理解阶段
    task_fit: 0.15
    success_rate: 0.15
    reputation: 0.10
    cost: 0.08
    speed: 0.05
    context_window: 0.15  # ↑ PDF 全文提取需要大上下文
    automation: 0.05
    output_quality: 0.20  # ↑ 提取质量直接决定后续步骤
    risk_level: 0.03
    rollback: 0.02
    skill_coverage: 0.05
    domain_fit: 0.12

  analysis:             # 分析/计算阶段
    task_fit: 0.15
    success_rate: 0.18
    reputation: 0.10
    cost: 0.08
    speed: 0.05
    context_window: 0.05
    automation: 0.10
    output_quality: 0.15
    risk_level: 0.10    # ↑ 分析代码需要在沙箱中安全运行
    rollback: 0.08      # ↑ 计算结果需可复现
    skill_coverage: 0.08
    domain_fit: 0.08

  synthesis:            # 综合/创作阶段
    task_fit: 0.15
    success_rate: 0.15
    reputation: 0.10
    cost: 0.05
    speed: 0.05
    context_window: 0.12  # ↑ 写作需要大上下文来引用多个来源
    automation: 0.05
    output_quality: 0.25  # ↑↑ 写作质量是核心
    risk_level: 0.05
    rollback: 0.03
    skill_coverage: 0.08
    domain_fit: 0.12     # ↑ 医学/学术写作需要领域匹配

  review:               # 审查/验证阶段
    task_fit: 0.10
    success_rate: 0.18
    reputation: 0.15    # ↑ 审查工具的声誉很重要
    cost: 0.05
    speed: 0.05
    context_window: 0.05
    automation: 0.05
    output_quality: 0.15
    risk_level: 0.15    # ↑ 审查的保守性
    rollback: 0.05
    skill_coverage: 0.08
    domain_fit: 0.14    # ↑ 医学审查需要 MEA

  transformation:       # 转换/格式化阶段
    task_fit: 0.20      # ↑ 格式转换专用工具
    success_rate: 0.15
    reputation: 0.08
    cost: 0.05
    speed: 0.10
    context_window: 0.05
    automation: 0.15    # ↑ 批量转换自动化
    output_quality: 0.12 # 保真度
    risk_level: 0.05
    rollback: 0.05
    skill_coverage: 0.08
    domain_fit: 0.07

  execution:            # 操作/执行阶段
    task_fit: 0.12
    success_rate: 0.15
    reputation: 0.10
    cost: 0.05
    speed: 0.08
    context_window: 0.05
    automation: 0.08
    output_quality: 0.10
    risk_level: 0.15    # ↑ 执行安全
    rollback: 0.15      # ↑↑ 必须可回滚
    skill_coverage: 0.05
    domain_fit: 0.07

  delivery:             # 发布/交付阶段
    task_fit: 0.10
    success_rate: 0.10
    reputation: 0.10
    cost: 0.05
    speed: 0.03
    context_window: 0.05
    automation: 0.05
    output_quality: 0.10
    risk_level: 0.20    # ↑↑ 交付安全最高优先级
    rollback: 0.20      # ↑↑ 必须可预览和回滚
    skill_coverage: 0.05
    domain_fit: 0.07
```

---

## 三、阶段感知的路由算法

```
输入：Task DAG（由 Dynamic Task Planner 生成）

对 Task DAG 中的每个 Step：
  │
  ├── 1. 识别 step 的阶段类型
  │      └── 从 step.stage 字段获取，或从 step 的 capability 推断
  │
  ├── 2. 加载该阶段的权重覆盖
  │      └── 从 stage_weights 表获取，未覆盖的用默认权重
  │
  ├── 3. 枚举该 step 的候选工具和 Agent
  │      └── 与标准 Router 相同
  │
  ├── 4. 用阶段特定权重评分
  │      └── Σ(维度评分 × 阶段权重)
  │
  ├── 5. 选择最优 + 备选
  │      └── top-2 组合（主 + 备）
  │
  └── 6. 跨阶段一致性检查
         ├── 前后阶段的工具是否兼容？（输出格式 = 下一阶段的输入格式）
         ├── 避免工具过度切换（相邻同类型步骤尽量用同一工具链）
         └── 如果兼容性冲突 → 调整次优选择
```

---

## 四、跨阶段一致性检查

### 4.1 工具链兼容矩阵

```
上一阶段输出         下一阶段期望输入        兼容？
─────────────────────────────────────────────────
PubMed XML           Zotero 条目             ✅ (Zotero 可直接导入)
PubMed XML           Python DataFrame        ⚠️ (需要 XML 解析适配)
Markdown 文本         pandoc 输入            ✅
CSV 文件             Python pandas           ✅
PDF 文件             pdftotext               ✅
Blender .blend       ffmpeg                  ❌ (需要先渲染为视频帧)
Manim .mp4           ffmpeg                  ✅ (直接处理)
JSON 分析结果         LaTeX/pandoc           ⚠️ (需要模板转换)
```

### 4.2 工具链兼容性自动解决

```
检测到不兼容:
  上一步输出: Blender .blend
  下一步期望: ffmpeg 视频输入

自动解决:
  1. 在两步之间插入一个 "渲染" 步骤:
     Blender → 渲染为 PNG 序列/MP4 → ffmpeg
  2. 检查是否有可替代的工具链:
     Manim → 直接输出 MP4 → ffmpeg（更流畅）
  3. 如果当前工具链无法自动解决 → 报告给用户 + 建议替代方案
```

---

## 五、阶段感知的 Agent 切换

同样一个任务的不同阶段可能需要不同的 Agent：

```
任务：「细胞吞噬动画制作」

阶段 1：科学内容核查 → Researcher (检索+验证生物学事实)
阶段 2：视觉脚本编写 → Storyboard Agent (科学→镜头)
阶段 3：资产生成       → Asset Generation Agent (图像/模型)
阶段 4：动画制作       → Animation Agent (Blender/Manim)
阶段 5：旁白字幕       → Narration Agent + Subtitle Agent
阶段 6：科学审查       → Scientific Accuracy Critic
阶段 7：美学审查       → Aesthetic Critic
阶段 8：渲染输出       → Video Editing Agent + ffmpeg
阶段 9：成果交付       → Ω Action Hub (用户确认)
```

Router 为每个阶段独立选择 Agent——而不是选一个 Agent 做完所有事。

---

## 六、与 Dynamic Task Planner 的接口

```
Dynamic Task Planner 输出 Task DAG，每个 Step 带有 stage 标记：

task_dag:
  task_id: "omega-task-2026-0515-050"
  steps:
    - step_id: 1
      stage: perception           ← Router 使用 perception 权重
      description: "检索吞噬过程的最新文献"
      required_capabilities: [literature_search]
      
    - step_id: 2
      stage: synthesis            ← Router 使用 synthesis 权重
      description: "整理科学事实，编写视觉脚本"
      required_capabilities: [scientific_writing, storyboard]
      
    - step_id: 3
      stage: execution            ← Router 使用 execution 权重
      description: "用 Blender 生成动画"
      required_capabilities: [3d_animation, python_scripting]
      
    - step_id: 4
      stage: review               ← Router 使用 review 权重
      description: "科学准确性审查"
      required_capabilities: [scientific_critique]
```

---

## 七、实施路线图

| 阶段 | 内容 | 依赖 |
|------|------|------|
| **MFE v1** | 标准 Router（无阶段感知）——整个任务用统一权重 | 标准 Router 就绪 |
| **MFE v2** | 阶段感知权重覆盖——每个 step 使用其 stage 的特定权重 | Dynamic Task Planner 为 step 标注 stage |
| **MFE v3** | 跨阶段兼容性检查——自动检测和修复工具链不兼容 | 工具输出/输入格式 schema 就绪 |
| **阶段 2** | 动态权重调整——Evolution Loop 根据历史结果自动优化各阶段权重 | Evolution Loop 就绪 |

---

## 八、相关页面

- [[Tool-Agent Router：最佳工具与最佳执行者选择器]] — 基础 Router（12 维评分 + 静态路由表）
- [[Dynamic Task Planner：动态任务规划器]] — 为 Router 提供带 stage 标记的 Task DAG
- [[Tool-Affordance Graph]] — 工具能力图谱
- [[Tool Reputation Ledger]] — 工具信誉和准入状态
- [[Productive Agent Society]] — Agent 社会分工
