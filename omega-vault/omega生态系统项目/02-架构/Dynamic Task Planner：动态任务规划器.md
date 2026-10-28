---
type: concept
tags: [omega-ecosystem, task-planning, dynamic-planner, task-decomposition, dag]
created: 2026-05-15
updated: 2026-05-15
knowledge_stability: evolving
parent: [[Omega生态系统项目-功能优先总方法论]]
related:
  - [[Tool-Agent Router：最佳工具与最佳执行者选择器]]
  - [[Stage-Aware Tool-Agent Router]]
  - [[Ω行动中枢]]
  - [[Action Brain]]
---

# Dynamic Task Planner：动态任务规划器

> **定位**：Tool-Agent Router 解决"用谁做"，Dynamic Task Planner 解决"怎么拆任务"。它接收 Ω 生成的任务契约，将用户的一句话目标分解为可执行的步骤 DAG（有向无环图），包含阶段标注、依赖关系、并行机会和能力需求。

---

## 一、为什么需要 Dynamic Task Planner

标准 Action Brain 的任务分解是隐式的——它依赖模型的理解来分解任务，但没有显式的规划算法。Dynamic Task Planner 将其**显式化、结构化、可验证**：

| 维度 | 隐式分解（当前） | Dynamic Task Planner |
|------|----------------|---------------------|
| 分解方式 | LLM 自由发挥 | 基于任务模板 + 能力映射 + 优化算法 |
| 并行识别 | 随机 | 依赖分析 → 无依赖步骤自动并行 |
| 阶段标注 | 无 | 每个步骤标注所属阶段（perception/extraction/...） |
| 可复现性 | 低（同一个任务可能不同分解） | 高（同类型任务使用同一模板+参数） |
| 优化空间 | 无 | 从 Action Memory 中学习最优分解模式 |

---

## 二、规划流程

```
输入：Task Contract（用户目标 + 类型 + 复杂度 + 约束）
  │
  ├── 步骤 1：目标解析
  │     ├── 识别交付物（最终要产出什么）
  │     ├── 识别输入（已有材料、数据、约束）
  │     └── 识别目标受众和质量要求
  │
  ├── 步骤 2：任务模板匹配
  │     ├── 在 Workflow Library 中搜索匹配的模板
  │     ├── 如果命中 → 加载模板，用参数实例化
  │     └── 如果未命中 → 从零构建
  │
  ├── 步骤 3：子任务分解
  │     ├── 按阶段顺序拆解：检索→提取→分析→综合→审查→格式化→交付
  │     ├── 每个阶段生成 1-N 个子步骤
  │     └── 每个子步骤标注：
  │         - stage（所属阶段）
  │         - required_capabilities（需要的能力）
  │         - inputs（输入数据/文件）
  │         - expected_outputs（期望输出）
  │         - autonomy_level（自主等级）
  │         - safety_constraints（安全约束）
  │
  ├── 步骤 4：依赖分析
  │     ├── 识别步骤间的数据依赖（A 的输出是 B 的输入）
  │     ├── 识别资源依赖（共享同一工具/Agent）
  │     └── 识别条件依赖（if-then 分支）
  │
  ├── 步骤 5：并行化优化
  │     ├── 无依赖步骤标记为可并行
  │     ├── 共享资源但无数据依赖 → 标注资源竞争，由调度器处理
  │     └── 生成 DAG（有向无环图）
  │
  ├── 步骤 6：能力需求汇总
  │     ├── 汇总所有步骤的 required_capabilities
  │     ├── 检查 Capability Fabric 是否覆盖全部能力
  │     └── 如有缺口 → 提前触发 Toolsmith-Lite（不等执行时失败）
  │
  ├── 步骤 7：估计与优化
  │     ├── 估计每步的执行时间
  │     ├── 识别关键路径
  │     ├── 检查是否可进一步并行化缩短总时间
  │     └── 检查是否超过任务截止时间（如有）
  │
  └── 输出：Task DAG
        ├── steps（有序步骤列表，含 stage 标注）
        ├── dependencies（步骤间依赖关系）
        ├── parallel_groups（可并行执行的步骤组）
        ├── capability_summary（能力需求汇总）
        ├── gap_analysis（能力缺口 + 预触发的 Toolsmith）
        └── estimated_duration（总预估时间）
```

---

## 三、任务模板系统

### 3.1 模板结构

```yaml
task_template:
  name: "literature_review_from_pdfs"
  task_type: "academic_writing"
  complexity: "workflow"
  description: "从 PDF 集合到综述初稿"
  applies_when:
    input_has: ["pdf_files", "writing_request"]
    domain: ["medical", "academic"]
  
  steps:
    - step_id: 1
      stage: extraction
      description: "提取 PDF 文本和元数据"
      parallelizable: true               # 每篇 PDF 可并行处理
      per_item: "pdf_file"               # 对每个 PDF 重复此步骤
      required_capabilities: [pdf_extract, metadata_parse]
      expected_output: "markdown_text_per_pdf"
      
    - step_id: 2
      stage: extraction
      description: "创建 Zotero 条目"
      depends_on: [1]
      required_capabilities: [zotero_create]
      expected_output: "zotero_items"
      
    - step_id: 3
      stage: perception
      description: "补充文献检索"
      depends_on: [1]
      parallelizable: true               # 可与步骤 2 并行
      required_capabilities: [literature_search]
      expected_output: "additional_papers"
      
    - step_id: 4
      stage: extraction
      description: "处理补充文献"
      depends_on: [3]
      parallelizable: true
      per_item: "additional_paper"
      required_capabilities: [pdf_extract, metadata_parse, zotero_create]
      expected_output: "additional_markdown"
      
    - step_id: 5
      stage: analysis
      description: "提取关键发现和共同主题"
      depends_on: [1, 4]
      required_capabilities: [cross_document_analysis, theme_extraction]
      expected_output: "theme_matrix"
      
    - step_id: 6
      stage: review
      description: "GRADE 评级（医学文献）"
      depends_on: [5]
      condition: "domain == 'medical'"
      required_capabilities: [grade_assessment]
      expected_output: "evidence_table"
      
    - step_id: 7
      stage: synthesis
      description: "撰写综述初稿"
      depends_on: [5, 6]
      required_capabilities: [academic_writing, cite_management]
      expected_output: "review_draft"
      
    - step_id: 8
      stage: review
      description: "Critic 审查"
      depends_on: [7]
      required_capabilities: [content_critique, format_check]
      expected_output: "review_feedback"
      
    - step_id: 9
      stage: synthesis
      description: "根据反馈修改"
      depends_on: [8]
      required_capabilities: [academic_writing]
      expected_output: "review_final"
      max_iterations: 3                 # 审查→修改循环最多 3 轮
      
    - step_id: 10
      stage: delivery
      description: "组装成果包"
      depends_on: [9]
      required_capabilities: [outcome_packaging]
      expected_output: "outcome_package"

  estimated_duration: "20-35min"
  success_rate_historical: 0.88
```

### 3.2 模板库

规划器从以下来源匹配模板：

| 来源 | 模板类型 | 示例 |
|------|---------|------|
| **Workflow Library** | 已验证的复杂工作流 | `literature_review_from_pdfs`, `meta_analysis_pipeline` |
| **Skill Library** | 已有 Skill 的步骤链 | `ingest-pubmed-L3`, `csv-analysis-report` |
| **Action Memory** | 历史成功任务的分解 | "上次处理 5 篇 PDF 写综述时的 10 步分解" |
| **从零构建** | 无模板时的动态生成 | 基于任务类型和能力映射表从零规划 |

---

## 四、动态规划（无模板时）

当没有匹配模板时，规划器从零构建：

### 4.1 基于任务类型映射的阶段序列

```
任务类型 → 阶段序列

knowledge_ingestion:
  perception → extraction → review → delivery

literature_search:
  perception → extraction → review → delivery

data_analysis:
  perception → extraction → analysis → review → delivery

meta_analysis:
  perception → extraction → analysis → review → synthesis → delivery

academic_writing:
  perception → extraction → analysis → synthesis → review → transformation → delivery

medical_research:
  perception → extraction → analysis → review → synthesis → review → transformation → delivery

scientific_visualization:
  perception → extraction → synthesis → execution → review → transformation → delivery

creative_production:
  perception → extraction → synthesis → execution → review → transformation → delivery
```

### 4.2 从用户目标中提取结构化信息

```
用户目标：「帮我制作一个 2 分钟的细胞吞噬过程 AI 演示动画，
          面向医学生，要求科学准确、视觉清晰、包含旁白字幕和关键步骤标注，
          最后输出 MP4、分镜稿、旁白稿和源文件。」

提取：
  task_type: scientific_visualization
  topic: "细胞吞噬 / phagocytosis"
  target_audience: "医学生"
  quality_requirements: ["科学准确", "视觉清晰"]
  duration: "2分钟"
  deliverables:
    primary: ["MP4 视频"]
    secondary: ["分镜稿", "旁白稿", "源文件", "关键步骤标注"]
  features: ["旁白", "字幕"]

映射到阶段序列（scientific_visualization）:
  1. perception     → 检索吞噬过程的科学文献和参考动画
  2. extraction     → 提取关键科学事实、步骤、视觉参考
  3. synthesis      → 编写视觉脚本（科学→镜头）、旁白稿
  4. execution      → 生成动画（Blender/Manim）、生成旁白音频（TTS）
  5. review         → 科学准确性审查、视觉质量审查
  6. transformation → 添加字幕、最终渲染、格式转换
  7. delivery       → 组装成果包（MP4 + 分镜稿 + 旁白稿 + 源文件）
```

---

## 五、并行化优化

### 5.1 并行化规则

| 条件 | 行为 | 示例 |
|------|------|------|
| 无数据依赖 + 无资源冲突 | 自动并行 | 同时搜索 PubMed 和 Semantic Scholar |
| 无数据依赖 + 共享资源 | 标记为"可并行，需调度" | 多个 PDF 都用 Marker 提取（共享 CPU/内存） |
| 有数据依赖 | 串行 | 先提取 PDF 再分析内容 |
| 同一 per_item 循环 | 自动并行 | 5 篇 PDF各自独立提取 |
| across per_item 循环 | 批次并行 | 提取 PDF1-3 → 同时提取 PDF4-5 |

### 5.2 并行度控制

```python
MAX_PARALLEL_STEPS = 5          # 最多 5 个步骤同时执行
MAX_PARALLEL_ITEMS = 10          # per_item 循环最多 10 个并行副本
MAX_PARALLEL_SANDBOXES = 3       # 沙箱资源有限，最多 3 个并发沙箱
```

---

## 六、能力缺口预检测

在规划阶段（而非执行阶段）就检测能力缺口：

```python
class CapabilityGapPreDetector:
    def detect_gaps(self, task_dag: TaskDAG) -> list[CapabilityGap]:
        """在执行前扫描所有步骤的能力需求"""
        all_required = set()
        for step in task_dag.steps:
            all_required.update(step.required_capabilities)
        
        gaps = []
        for capability in all_required:
            if not CapabilityFabric.has_adapter(capability):
                gaps.append(CapabilityGap(
                    capability=capability,
                    affected_steps=[s for s in task_dag.steps 
                                   if capability in s.required_capabilities],
                    severity="blocking" if self.is_blocking(capability) else "warning"
                ))
        
        return gaps
    
    def pre_trigger_toolsmith(self, gaps: list[CapabilityGap]):
        """不等执行失败，提前启动 Toolsmith 搜索工具"""
        for gap in gaps:
            if gap.severity == "blocking":
                ToolsmithLite.search_and_learn(gap.capability)
```

---

## 七、从历史中学习——规划优化

每次任务完成后，规划器从 Action Memory 中提取改进信号：

```yaml
planner_learning:
  task_id: "omega-task-2026-0515-050"
  planned_steps: 9
  actual_steps: 11               # 多了 2 步（遇到了意外依赖）
  what_happened:
    - "planned: PDF提取→分析     actual: PDF提取→表格提取→格式转换→分析"
    - "原因: PDF 表格需要 Camelot 单独提取，Marker 提取不完整"
  optimization:
    - "下次类似任务时，自动在 PDF 提取和分析之间插入表格提取步骤"
    - "更新模板: 当 PDF 包含表格时，加入 camelot_table_extract 步骤"
  parallelization_accuracy:
    planned_parallel_groups: 3
    actual_parallel_groups: 2    # 一组被资源竞争阻止
    reason: "3 个 PDF 同时用 Marker 提取导致内存超限"
    fix: "将 PDF 并行提取的最大并发数从 5 降为 2"
```

---

## 八、与上下游组件的接口

```
上游输入：
  Ω Action Hub → Task Contract
  自我解惑循环 → 重新规划请求

下游输出：
  Stage-Aware Router → 带 stage 标注的 Task DAG
  Capability Fabric → 能力缺口预检测结果
  Toolsmith-Lite → 提前触发的工具搜索

反馈循环：
  Action Memory → 历史任务分解记录
  Evolution Loop → 规划模板的优化
```

---

## 九、相关页面

- [[Tool-Agent Router：最佳工具与最佳执行者选择器]] — 为每个 step 选择工具和 Agent
- [[Stage-Aware Tool-Agent Router]] — 使用 step 的 stage 标注优化选择
- [[Ω行动中枢]] — 生成 Task Contract 作为 Planner 的输入
- [[Action Brain]] — Planner 是其核心组件
- [[自我解惑与外援调用循环]] — Planner 的能力缺口触发 Toolsmith
- [[Action Memory]] — 规划结果的存储和学习来源
