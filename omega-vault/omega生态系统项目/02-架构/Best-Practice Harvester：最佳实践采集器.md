---
type: concept
tags: [omega-ecosystem, best-practice, tool-learning, quality-assurance, knowledge-harvesting]
created: 2026-05-15
updated: 2026-05-15
knowledge_stability: evolving
parent: [[Toolsmith-Lite与Skillsmith]]
related:
  - [[SOTA Source Hierarchy：顶尖工具来源分级]]
  - [[Stage-Aware Tool-Agent Router]]
  - [[自我解惑与外援调用循环]]
  - [[Tool Reputation Ledger]]
---

# Best-Practice Harvester：最佳实践采集器

> **定位**：当 Omega 选定一个工具来执行任务时，Best-Practice Harvester 负责回答一个问题：**"这个工具当前的最佳用法是什么？"** 它自动搜索官方文档、GitHub 示例、社区工作流、教程和开发者分享，提取最佳实践，验证后提供给 Agent 使用，最终沉淀为 Skill。

---

## 一、为什么需要这个机制

Toolsmith-Lite 解决"找到工具并学会基本使用"。自我解惑循环解决"不会时求助"。但还缺一个关键层：

**"工具我会用，但我用的是最好的方式吗？"**

同样是 ComfyUI：
- 初学者用法：手动拖节点、默认参数
- 最佳实践：使用 API 节点接入 Nano Banana Pro 作为 backbone + 社区验证的医学插图工作流 + 批量参数优化脚本

同样是 Blender：
- 初学者用法：手动建模、手动渲染
- 最佳实践：Python bpy 脚本自动化建模 + 程序化材质 + Eevee 实时渲染 + 命令行批量渲染

Best-Practice Harvester 让 Omega 不只是"能用工具"，而是"用好工具"。

---

## 二、采集流程

```
Router 选定工具 X 用于任务 Y
  │
  ↓
Best-Practice Harvester 启动
  │
  ├── 步骤 1：确定采集目标
  │     ├── 工具名称 + 版本
  │     ├── 任务类型（如"医学教学动画"）
  │     ├── 质量要求（highest_quality / standard / draft）
  │     └── 约束条件（本地/云端、免费/付费、速度要求）
  │
  ├── 步骤 2：多源搜索最佳实践
  │     ├── S0 官方：文档的 Best Practices / Tutorials / Examples
  │     ├── S0 官方：GitHub 仓库的 examples/ 目录
  │     ├── S1 代码：GitHub 上使用该工具的高星项目
  │     ├── S1 代码：HuggingFace 上的使用示例
  │     ├── S2 社区：YouTube 高播放量教程
  │     ├── S2 社区：Reddit/Discord 的"best way to X"讨论
  │     ├── S2 社区：X 上核心开发者的推荐
  │     └── S2 社区：微信公众号/技术博客的深度教程
  │
  ├── 步骤 3：提取最佳实践要素
  │     ├── 推荐的工作流/节点配置/参数设置
  │     ├── 推荐的模型/checkpoint/LoRA 组合
  │     ├── 推荐的提示词范式（如适用）
  │     ├── 常见陷阱和避免方法
  │     ├── 性能优化技巧（GPU 内存/渲染速度/批处理）
  │     ├── 质量提升技巧（后处理/精修/合成）
  │     └── 版本依赖和兼容性注意事项
  │
  ├── 步骤 4：交叉验证
  │     ├── 官方文档的最佳实践 vs 社区的最佳实践 → 是否一致？
  │     ├── 多个社区来源的最佳实践 → 是否共同推荐？
  │     ├── 核心开发者的推荐 → 是否有代码/数据支撑？
  │     └── 如有矛盾 → 标记 + 沙箱实测决定
  │
  ├── 步骤 5：沙箱验证
  │     ├── 在 Docker 沙箱中复现最佳实践的最小示例
  │     ├── 验证输出质量是否确实更好
  │     ├── 记录性能数据
  │     └── 验证失败 → 标记为"未验证的最佳实践"
  │
  ├── 步骤 6：生成最佳实践指南
  │     ├── 格式：Markdown + YAML（机器可读）
  │     ├── 包含：推荐配置、步骤、参数、示例代码、预期效果
  │     ├── 标注来源和置信度
  │     └── 标注验证状态：✅ 已验证 / ⚠️ 社区推荐但未实测 / 🔴 有争议
  │
  ├── 步骤 7：注入到 Agent 执行
  │     ├── 将最佳实践指南作为 Agent 执行时的额外上下文
  │     ├── Router 选择工具时考虑"是否有最佳实践覆盖"
  │     └── 在 Outcome Package 中注明"基于最佳实践执行"
  │
  └── 步骤 8：沉淀为 Skill 或 Workflow
        ├── 如果最佳实践可复用 → 封装为 Skill
        ├── 如果涉及多工具链 → 封装为 Workflow 模板
        └── 写入 Skill Library + 更新 Tool-Affordance Graph
```

---

## 三、最佳实践采集的示例

### 示例：用 Nano Banana Pro 制作医学信息图

```
任务："用 Nano Banana Pro 做一张细胞吞噬过程医学信息图，最高质量"

1. 采集目标：
   - 工具：Nano Banana Pro（Gemini 3 Pro Image）
   - 任务：医学信息图 / 教学图解
   - 质量：highest_quality

2. S0 搜索：Nano Banana Pro 官方文档
   → 发现官方推荐的信息图 prompt 模板
   → 发现文字准确性增强参数
   → 发现多语言文本支持的设置

3. S1 搜索：GitHub / Google AI 示例
   → 找到官方示例代码中的医学插图生成示例
   → 找到推荐的分辨率、风格参数

4. S2 搜索：YouTube / X / Reddit
   → 找到医学插画师的 Nano Banana 使用分享
   → 发现"先用 Nano Banana Pro 生成主体 → 再用 Manim 加标注"
     的混合工作流

5. 提取最佳实践：
   - prompt 结构：[科学事实] + [视觉风格] + [标注要求] + [受众]
   - 参数推荐：temperature=0.4（医学需要准确性）
   - 文字检查：开启 text_accuracy=high
   - 迭代策略：先生成布局草稿 → 确认 → 生成最终图

6. 沙箱验证：
   → 用 3 个不同的医学信息图 prompt 测试
   → 2/3 生成结果文字准确、结构清晰
   → 1/3 有一个术语错误（需人工审查）

7. 生成最佳实践指南：
   nano-banana-medical-infographic-best-practice.md
   - 标注：✅ 经验证的 prompt 模板
   - ⚠️ 医学术语仍需人工审查
   - 置信度：高（S0 + S1 + 沙箱验证）

8. 沉淀：Skill 候选
   skill: medical-infographic-nano-banana-v1
```

### 示例：用 ComfyUI + Blender 做细胞吞噬 3D 动画

```
任务："用最高质量方式做细胞吞噬 3D 教学动画"

1. 采集目标：ComfyUI + Blender 组合工作流

2. S0/S1/S2 搜索：
   → ComfyUI 官方：3D 生成节点（Hunyuan3D, Stable Zero123）
   → Blender 官方：Python bpy 脚本、程序化细胞建模
   → GitHub：comfyui-blender-integration 项目
   → YouTube：医学 3D 动画教程
   → X：Blender 医学可视化社区推荐

3. 提取最佳实践：
   - 推荐工作流：
     ComfyUI API node 生成细胞纹理 → Blender bpy 脚本建模 →
     Eevee 实时预览 → Cycles 最终渲染 → ffmpeg 合成
   - 参数：
     Blender：细胞模型用 metaball + subdivision surface
     渲染：先 Eevee 720p 快速预览 → Cycles 1080p 最终
     批渲染：命令行 `blender -b -P script.py`

4. 沙箱验证：成功渲染 30 秒测试动画

5. 生成最佳实践指南 + Skill 候选

6. 在 Outcome Package 中注明：
   "动画基于 ComfyUI + Blender 最佳实践工作流（S0+S1 验证）"
```

---

## 四、最佳实践指南格式

```yaml
best_practice_guide:
  tool: "Nano Banana Pro"
  version: "latest (2026-05)"
  task_type: "medical_infographic"
  quality_level: "highest_quality"
  harvested_at: "2026-05-15"
  
  sources:
    s0_official:
      - "Google AI for Developers — Image Generation docs"
      - "Nano Banana Pro blog announcement (blog.google)"
    s1_code:
      - "google-gemini/cookbook — medical illustration examples"
    s2_community:
      - "YouTube: Medical Illustrator's Nano Banana workflow"
      - "Reddit: r/MedicalIllustration — best practices thread"
      
  cross_validation:
    consistency: "high"  # S0 + S1 + S2 一致
    contradictions: []
    unverified_claims: 0
    
  sandbox_verification:
    status: "passed"
    test_cases: 3
    success_rate: 2/3
    notes: "1 case had terminology error — needs human review for medical terms"
    
  best_practices:
    prompt_structure:
      template: |
        [Subject: scientific description]
        [Style: clean medical illustration]
        [Annotations: labels in Chinese, arrows pointing to key structures]
        [Audience: medical students]
        [Constraints: scientifically accurate, no artistic liberty on structures]
    parameters:
      temperature: 0.4
      text_accuracy: "high"
      resolution: "4K"
    workflow:
      - "Step 1: Generate layout draft (low resolution, check structure)"
      - "Step 2: User confirms layout"
      - "Step 3: Generate final high-resolution infographic"
      - "Step 4: Scientific Accuracy Critic review"
    pitfalls:
      - "Medical terminology may be hallucinated → always review with Critic"
      - "Complex multi-step pathways may need multiple images"
    
  confidence: "high"
  verified_tags: ["✅ verified by S0", "✅ verified by sandbox", "⚠️ human review for medical terms"]
```

---

## 五、与"最高质量模式"的联动

当用户指定 `quality_profile: highest_quality` 时，Best-Practice Harvester 的行为：

| 维度 | 标准模式 | 最高质量模式 |
|------|---------|------------|
| **来源搜索深度** | S0 + S1 | S0 + S1 + S2 × 3 |
| **沙箱验证** | 1 个测试用例 | 3 个测试用例 |
| **多工具对比** | 不对比 | 对比至少 2 个替代工具 |
| **Critic 参与** | 1 轮审查 | 2 轮审查（科学 + 美学） |
| **人工审查** | 可选 | 强制（最终输出前必须用户确认） |
| **成果包** | 简化版 | 完整版（含最佳实践来源 + 对比报告） |
| **Skill 沉淀** | 仅记录 | 自动封装 + 标记复用潜力 |

---

## 六、相关页面

- [[SOTA Source Hierarchy：顶尖工具来源分级]] — Best-Practice Harvester 的来源选择依据
- [[Toolsmith-Lite与Skillsmith]] — 沙箱验证和 Skill 封装
- [[Stage-Aware Tool-Agent Router]] — 不同阶段的工具选择
- [[自我解惑与外援调用循环]] — 搜集不到最佳实践时求助
- [[Multimodal Outcome Package]] — 最佳实践指南作为成果包的一部分
- [[Creative Tool Router]] — 创意任务的最佳实践采集
