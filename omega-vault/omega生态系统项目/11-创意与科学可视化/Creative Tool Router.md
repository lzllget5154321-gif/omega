---
type: concept
tags: [omega-ecosystem, creative-tools, visualization-routing, image-generation, animation, design]
created: 2026-05-15
updated: 2026-05-15
knowledge_stability: evolving
parent: [[科学动画生产系统]]
related:
  - [[Stage-Aware Tool-Agent Router]]
  - [[Best-Practice Harvester：最佳实践采集器]]
  - [[SOTA Source Hierarchy：顶尖工具来源分级]]
---

# Creative Tool Router：创意工具路由器

> **定位**：专门处理作图、动画、视频、3D、音频、字幕、演示等创意任务的工具选择。它继承 Stage-Aware Router 的框架，但增加了**创意任务特有的选择维度**——视觉风格、可控性、科学准确性、美学质量、可复现性。

---

## 一、创意任务的工具选择逻辑

```
"帮我做一张细胞吞噬过程的医学教学图"
        ↓
第一步：任务细分
  ├── 是快速概念图还是最终出版级图像？
  ├── 是静态图还是动画？
  ├── 是信息图（带文字标注）还是纯视觉图？
  ├── 是 2D 图解还是 3D 渲染？
  ├── 需要多大程度的可控性？
  ├── 是否要求科学准确性？
  └── 是否需要本地可复现的工作流？

        ↓
第二步：工具空间枚举
  ├── 图像生成：Nano Banana Pro / ComfyUI / DALL-E / Midjourney / SD
  ├── 2D 矢量图：Figma / Illustrator / Manim / BioRender
  ├── 3D 渲染：Blender / Cinema 4D / Unreal Engine
  ├── 动画：Blender / Manim / After Effects
  ├── 视频：ffmpeg / DaVinci Resolve / CapCut
  ├── 演示：PowerPoint / Keynote / Canva / Reveal.js
  └── 后期：ffmpeg / DaVinci Resolve / TTS 服务

        ↓
第三步：创意维度评分（在标准 12 维基础上新增 5 维）
  ├── visual_style_match（视觉风格匹配度）
  ├── scientific_accuracy（科学准确性）
  ├── controllability（可控性——能否精确调整）
  ├── batch_reproducibility（批量和可复现性）
  └── aesthetic_quality（美学质量——非科学任务时）

        ↓
第四步：选择并返回推荐 + 备选 + 混合方案
```

---

## 二、创意任务分类与推荐工具矩阵

| 任务类型 | 典型需求 | 首选工具 | 备选工具 | 混合方案 |
|---------|---------|---------|---------|---------|
| **医学信息图**（带文字标注） | 文字准确 + 科学正确 + 结构清晰 | Nano Banana Pro | ComfyUI + SD | Nano Banana Pro 主体 + Manim 标注层 |
| **科研插图**（细胞/分子/机制） | 科学准确 + 矢量可编辑 | BioRender / Figma | Nano Banana Pro | AI 生成概念 → Figma 精修 |
| **3D 细胞/器官动画** | 立体感 + 可旋转 + 流程演示 | Blender (bpy) | Unreal Engine | ComfyUI 纹理 → Blender 建模 |
| **2D 过程图解动画** | 可控 + 可解释 + 数学精确 | Manim | After Effects | Manim 主体 + ffmpeg 后期 |
| **快速概念草稿** | 速度 + 迭代探索 | Nano Banana / Gemini Image | DALL-E | — |
| **高质量海报/封面** | 美学 + 冲击力 + 品牌一致 | Nano Banana Pro | ComfyUI + SDXL | — |
| **短视频/科普片段** | 节奏 + 旁白 + 字幕 | Manim + ffmpeg + TTS | CapCut | AI 生成素材 + 手动剪辑 |
| **PPT/Keynote 演示** | 结构清晰 + 图表 + 动画 | PowerPoint + python-pptx | Canva / Keynote | Claude 生成内容 → PPT 排版 |
| **实验流程图** | 逻辑清晰 + 标准符号 | Figma / draw.io | Manim | — |
| **数据可视化** | 精确 + 可复现 | Python matplotlib/seaborn | R ggplot2 / Observable | Python 生成 → AI 美化 |
| **交互式 3D 演示** | Web 可访问 | Three.js / WebGL | Blender → Web 导出 | — |
| **音频（旁白/背景音乐）** | 自然 + 同步 | Edge TTS / ElevenLabs | OpenAI TTS | — |

---

## 三、创意维度评分

在标准 Tool-Agent Router 的 12 维基础上，创意任务新增 5 个维度：

| # | 维度 | 权重（创意任务） | 说明 | 数据来源 |
|---|------|:--:|------|---------|
| 13 | **视觉风格匹配** (visual_style_match) | 0.12 | 该工具的输出风格是否符合需求（医学插图/3D写实/极简图解/卡通教学） | Tool Registry + 基准测试 |
| 14 | **科学准确性** (scientific_accuracy) | 0.15 | 工具是否擅长科学/医学内容的准确呈现（对文字、结构、比例的保真度） | Scientific Accuracy Critic |
| 15 | **可控性** (controllability) | 0.10 | 能否精确控制每个元素的属性（位置、颜色、大小、标注） | 工具特征 + 沙箱测试 |
| 16 | **批量可复现** (batch_reproducibility) | 0.08 | 能否用脚本批量生成、能否在 Docker 中复现 | 代码验证 |
| 17 | **美学质量** (aesthetic_quality) | 0.10 | 输出在美学上是否专业（非科学任务时权重提升至 0.18） | Aesthetic Critic |

**创意任务总权重 = 标准 12 维 × 0.65 + 创意 5 维 × 0.35**

（当任务无科学准确性要求时，scientific_accuracy 权重转移到 aesthetic_quality）

---

## 四、工具对比示例

### 医学信息图任务：「细胞吞噬过程教学信息图，带中英文标注」

| 维度 | Nano Banana Pro | ComfyUI + SDXL | DALL-E 3 | BioRender | Figma (手动) |
|------|:--:|:--:|:--:|:--:|:--:|
| task_fit | 0.90 | 0.70 | 0.65 | 0.85 | 0.60 |
| success_rate | 0.88 | 0.80 | 0.75 | 0.92 | 0.95 |
| output_quality | 0.90 | 0.78 | 0.72 | 0.88 | 0.90 |
| visual_style_match | 0.92 | 0.75 | 0.70 | 0.88 | 0.85 |
| scientific_accuracy | 0.78 | 0.60 | 0.55 | 0.94 | 0.96 |
| controllability | 0.65 | 0.85 | 0.50 | 0.80 | 0.98 |
| batch_reproducibility | 0.70 | 0.90 | 0.60 | 0.70 | 0.95 |
| cost | 0.85 | 0.90 | 0.80 | 0.60 | 0.50 |
| speed | 0.92 | 0.70 | 0.85 | 0.50 | 0.30 |
| **加权总分** | **0.843** | **0.772** | **0.686** | **0.800** | **0.729** |

→ **首选 Nano Banana Pro**（快速高质量 + 文字能力强）
→ **备选 BioRender**（科学准确性最高，但速度慢、需手动）
→ **混合方案**：Nano Banana Pro 生成主体 → Manim 加标注层 → Scientific Critic 审查

---

## 五、混合工具流水线

创意任务常需要**多工具混合**——单一工具难以满足所有需求：

### 流水线模板 1：AI 生成 + 程序化标注

```
Nano Banana Pro / ComfyUI
  → 生成视觉主体（细胞、细菌、溶酶体）
  ↓
Manim / Python PIL
  → 叠加标注文字、箭头、步骤编号
  ↓
Scientific Accuracy Critic
  → 审查科学准确性
  ↓
ffmpeg / PIL
  → 最终合成输出
```

### 流水线模板 2：3D + 2D 混合

```
Blender (bpy)
  → 3D 细胞膜变形、伪足伸展、吞噬体闭合
  ↓
Blender → 渲染为 PNG 序列
  ↓
Manim
  → 叠加 2D 标注层（文字、箭头、时间轴）
  ↓
ffmpeg
  → 合成视频 + 旁白音频 + 字幕
```

### 流水线模板 3：快速概念 → 精修

```
Nano Banana (快速)
  → 生成 5 个概念草稿（不同风格/角度）
  ↓
用户选择 1 个方向
  ↓
Nano Banana Pro (高质量)
  → 基于选中方向生成精修版
  ↓
Aesthetic Critic 审查
  ↓
如需微调 → ComfyUI 节点精确调整
```

---

## 六、与 Best-Practice Harvester 的联动

当 Router 选定创意工具后，自动触发 Best-Practice Harvester：

```
Router 选择：Nano Banana Pro 用于医学信息图
  ↓
Best-Practice Harvester 搜索：
  - "Nano Banana Pro medical infographic best practices"
  - "Nano Banana Pro scientific diagram prompt engineering"
  - "Nano Banana Pro text accuracy settings"
  ↓
提取最佳实践：
  - prompt 模板：[科学描述] + [医学插图风格] + [中英文标注] + [医学生受众]
  - 参数：temperature=0.4, text_accuracy=high
  - 常见陷阱：复杂分子式可能出错 → 人工审查
  ↓
注入到 Agent 执行上下文
```

---

## 七、创意质量模式

| 模式 | 说明 | 工具选择偏好 |
|------|------|------------|
| **speed_first** | 快速出图，用于内部讨论/概念探索 | Nano Banana / DALL-E（单次生成） |
| **balanced** | 质量与速度平衡 | Nano Banana Pro / ComfyUI 简单工作流 |
| **highest_quality** | 最高质量，用于出版/教学/外部展示 | 混合流水线（AI + 手动 + Critic 审查） |
| **scientific_only** | 科学准确性为唯一标准 | BioRender / 手动 Figma（AI 仅作为辅助） |

---

## 八、相关页面

- [[科学动画生产系统]] — 完整的创意生产管线
- [[Stage-Aware Tool-Agent Router]] — Router 的基础框架
- [[Best-Practice Harvester：最佳实践采集器]] — 工具最佳实践采集
- [[SOTA Source Hierarchy：顶尖工具来源分级]] — 创意工具的信誉来源
- [[Model and Tool Lifecycle Manager]] — 创意工具的生命周期管理
- [[Multimodal Outcome Package]] — 创意成果的多模态交付
