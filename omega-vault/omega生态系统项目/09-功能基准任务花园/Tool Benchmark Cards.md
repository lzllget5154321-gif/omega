---
type: concept
tags: [omega-ecosystem, benchmark-cards, tool-evaluation, capability-testing, tool-reputation]
created: 2026-05-15
updated: 2026-05-15
knowledge_stability: evolving
parent: [[Tool-Agent Router：最佳工具与最佳执行者选择器]]
related:
  - [[Model and Tool Lifecycle Manager]]
  - [[Tool Reputation Ledger]]
  - [[Auto-Upgrade Policy]]
  - [[Creative Tool Router]]
  - [[External AI Rolebook]]
---

# Tool Benchmark Cards：工具基准任务卡

> **定位**：定义 Omega 如何客观评测每个工具的**真实能力**。每个工具类别有一组小型基准任务——新工具进入 `investigating` 状态后，必须在这些任务上跑分，分数直接影响 Tool Reputation Ledger 的初始信誉和 Tool-Agent Router 的评分权重。

---

## 一、基准任务设计原则

```
1. 小型化  — 每个任务 ≤ 5 分钟，快速跑完
2. 可量化  — 每个任务有明确 score（0-1）+ 维度分
3. 可复现  — 同一任务同一 prompt，多次跑取平均
4. 分层级  — 基础任务（都必须过）+ 高级任务（专业工具可见）
5. 真场景  — 任务来自实际使用场景，不用人造玩具题
6. 多维度  — 不仅看"是否完成"，还要看速度/成本/质量/可控性/可复现性
```

---

## 二、基准任务卡：图像生成工具

> 适用工具：Nano Banana / Nano Banana Pro / ComfyUI+SD/SDXL / DALL-E / Midjourney / Gemini Image / Flux / Ideogram
> 基准集名称：`image_generation_bench`

### 2.1 基础任务（所有图像工具必测）

#### 任务 I1：医学教学信息图生成

```
任务 I1：医学教学信息图生成
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
prompt: "制作一张细胞吞噬（phagocytosis）过程的医学教学信息图，
  标注：伪足、吞噬体、溶酶体融合、吞噬溶酶体、残余体，
  中英文标注，面向医学生，教学风格，清晰结构"

验收标准：
  ✅ 所有 5 个结构（伪足/吞噬体/溶酶体融合/吞噬溶酶体/残余体）都被正确描绘
  ✅ 标注文字清晰可读、无拼写错误
  ✅ 结构比例大体正确（吞噬体 > 溶酶体）
  ✅ 标注箭头指向正确位置
  ⚠️ 伪足形态合理（允许风格化但不出现本质错误）

评分维度（每个 0-1）：
  structural_accuracy: 0.30    — 生物结构正确性
  text_accuracy: 0.25          — 文字拼写、术语正确性
  visual_clarity: 0.20         — 视觉层次和清晰度
  annotation_quality: 0.15     — 标注位置和箭头准确性
  medical_style_appropriateness: 0.10 — 医学教学风格匹配度

综合分 = weighted sum
```

#### 任务 I2：信息图文字准确性压力测试

```
任务 I2：信息图文字准确性压力测试
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
prompt: "制作一张信息图，标题为'线粒体电子传递链（ETC）复合物 I-IV'，
  包含以下文字标注（必须精确）：
  - NADH dehydrogenase (Complex I)
  - Succinate dehydrogenase (Complex II)
  - Cytochrome bc1 (Complex III)
  - Cytochrome c oxidase (Complex IV)
  - ATP synthase (Complex V)
  - 每个复合物的质子泵数量标注"

验收标准：
  ✅ 所有 5 个复合物名称完全正确（包括罗马数字和英文拼写）
  ✅ 质子泵数量标注数值正确（I:4, II:0, III:4, IV:2）
  ✅ 无拼写错误（连字符、大小写、空格）
  🔴 任何一处术语拼写错误 → 此项 0 分（文字准确性是信息图的底线）

评分维度（每个 0-1）：
  text_precision: 0.50         — 术语 100% 正确
  layout_readability: 0.25     — 文字布局可读性
  scientific_correctness: 0.25 — 流程/关系正确性
```

#### 任务 I3：风格一致性测试

```
任务 I3：风格一致性测试
━━━━━━━━━━━━━━━━━━━━━
测试方式：用同一风格 prompt 生成 3 张不同主题的图，比较风格一致性

prompt_1: "科普风格：DNA 复制过程的示意图，扁平化设计，蓝白配色"
prompt_2: "科普风格：蛋白质翻译过程的示意图，扁平化设计，蓝白配色"
prompt_3: "科普风格：细胞分裂过程的示意图，扁平化设计，蓝白配色"

验收标准：
  ✅ 3 张图色调一致（蓝白主题保持一致）
  ✅ 设计语言一致（同样的扁平化程度、线条粗细、图标风格）
  ✅ 构图逻辑一致（类似的布局结构）
  ⚠️ 允许轻微色调差异

评分维度（每个 0-1）：
  color_consistency: 0.25
  design_language_consistency: 0.25
  layout_consistency: 0.25
  prompt_adherence: 0.25       — 每张是否都遵循了风格指令
```

#### 任务 I4：局部编辑/修改能力

```
任务 I4：局部编辑/修改能力
━━━━━━━━━━━━━━━━━━━━━━━━
测试方式：先生成一张图 → 要求局部修改 → 检查修改精确度

步骤 1：生成 "一只卡通风格的猫坐在桌子上"
步骤 2：修改 "把猫的颜色从橘色改成黑色，其他不变"
步骤 3：修改 "在桌子上加一杯咖啡，其他不变"

验收标准（仅适用于支持编辑的工具）：
  ✅ 步骤 2：猫的颜色改变了，背景和桌子不变
  ✅ 步骤 3：咖啡出现，猫（黑色）和其他元素保持
  🔴 不支持编辑的工具 → 此项标记 N/A，不影响总体评分

评分维度（每个 0-1）：
  edit_precision: 0.40        — 修改指定之外的元素流失率
  unchanged_preservation: 0.40 — 未指定修改的元素是否完好
  multi_round_stability: 0.20  — 多轮修改后的累积退化程度
```

#### 任务 I5：出图速度和成本

```
任务 I5：出图速度和成本
━━━━━━━━━━━━━━━━━━━━━━
测试方式：跑 I1 任务 5 次，记录时间和成本

记录指标：
  avg_time_seconds:    平均出图时间（秒）
  p95_time_seconds:    P95 出图时间
  cost_per_image:      单张成本（美元或 API credit）
  batch_efficiency:    批量生成时是否支持并行

评分维度（每个 0-1）：
  speed_score: 0.50          — 基于 avg_time 的归一化分（越快越高）
  cost_score: 0.50            — 基于 cost_per_image 的归一化分（越便宜越高）

注：speed_score = min(1.0, 30 / avg_time_seconds)  # 30 秒为基准
    cost_score = min(1.0, 0.05 / cost_per_image)    # $0.05 为基准
```

### 2.2 高级任务（专业图像工具选测）

#### 任务 I6：科学结构精确性深度测试

```
任务 I6：科学结构精确性深度测试
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
仅适用于：支持精确可控的工具（ComfyUI/BioRender/Blender）

prompt: "生成人类心脏四腔室的解剖结构图，必须精确描绘：
  - 左心房、左心室、右心房、右心室
  - 二尖瓣（mitral valve）、三尖瓣（tricuspid valve）
  - 主动脉（aorta）、肺动脉（pulmonary artery）
  - 室间隔（interventricular septum）
  标注所有结构"

验收标准：
  ✅ 心腔相对大小正确（左心室壁最厚）
  ✅ 瓣膜数量和位置正确
  ✅ 大血管连接位置正确
  ✅ 室间隔位置正确
  🔴 任何结构性错误 → 此项 ≤ 0.3

评分维度（每个 0-1）：
  anatomical_accuracy: 0.60   — 解剖结构精度
  proportional_accuracy: 0.20 — 比例精度
  annotation_accuracy: 0.20   — 标注精度
```

---

## 三、基准任务卡：3D 动画工具

> 适用工具：Blender / Unreal Engine / Cinema 4D / Houdini
> 基准集名称：`3d_animation_bench`

### 任务 3D1：基础场景搭建

```
任务 3D1：基础场景搭建
━━━━━━━━━━━━━━━━━━━━
prompt: "在 Blender 中创建一个医学教学场景：
  - 一个细胞（球形，半透明外壁）
  - 内部可见细胞核（球形，位于中央偏左）
  - 3 个溶酶体（小球，分布在不同位置）
  - 基础三点光照（key + fill + rim）
  - 相机位置：正前方，轻微俯角"

验收标准：
  ✅ 所有元素存在且位置合理
  ✅ 材质透明度和颜色合理
  ✅ 光照可区分细胞结构
  ✅ 相机视角正确

评分维度（每个 0-1）：
  scene_completeness: 0.25
  material_quality: 0.20
  lighting_quality: 0.20
  camera_setup: 0.15
  script_quality: 0.20       — 是否用 Python bpy 脚本（可复现性）
```

### 任务 3D2：动画关键帧

```
任务 3D2：动画关键帧
━━━━━━━━━━━━━━━━━━
prompt: "在上述场景中，创建 5 秒动画：
  - 0-1s：细胞膜局部凹陷（伪足形成）
  - 1-3s：凹陷加深包裹颗粒（吞噬体形成）
  - 3-5s：吞噬体向细胞内部移动
  每秒 24 帧，共 120 帧"

验收标准：
  ✅ 动画流畅（帧之间无跳跃）
  ✅ 三个阶段的过渡自然
  ✅ 细胞膜变形符合物理直觉
  ✅ 关键帧设置合理（非 AI 自动插值混乱）

评分维度（每个 0-1）：
  animation_smoothness: 0.35
  morphing_realism: 0.30     — 形变是否合理
  keyframe_quality: 0.20
  timing: 0.15                — 时间节奏
```

### 任务 3D3：渲染输出

```
任务 3D3：渲染输出
━━━━━━━━━━━━━━━━━━
测试方式：渲染 3D2 的动画为 MP4

验收标准：
  ✅ 输出 1920×1080 MP4
  ✅ 无渲染错误（黑帧、闪烁）
  ✅ 渲染时间合理（≤ 任务目标时间的 10 倍）
  ✅ 文件大小合理（≤ 50 MB for 120 frames）

评分维度（每个 0-1）：
  render_quality: 0.30
  render_speed: 0.25
  file_size_efficiency: 0.20
  no_render_errors: 0.25
```

---

## 四、基准任务卡：2D 动画工具

> 适用工具：Manim / After Effects / Motion Canvas / Rive
> 基准集名称：`2d_animation_bench`

### 任务 2D1：科学图解动画

```
任务 2D1：科学图解动画
━━━━━━━━━━━━━━━━━━━━
prompt: "用 Manim 创建一段简短的数学教学动画：
  - 主题：梯度下降（Gradient Descent）
  - 展示一个 2D 曲面 + 小球从高处沿最陡方向滚到最低点
  - 标注：初始点、梯度方向、局部最小值
  - 时长 15-30 秒"

验收标准：
  ✅ 曲面正确渲染
  ✅ 小球运动方向符合梯度方向
  ✅ 标注清晰可见
  ✅ 动画节奏适合教学

评分维度（每个 0-1）：
  mathematical_accuracy: 0.35
  visual_quality: 0.25
  annotation_clarity: 0.20
  pacing: 0.20
```

### 任务 2D2：代码可复现性

```
任务 2D2：代码可复现性
━━━━━━━━━━━━━━━━━━━━
测试方式：将 2D1 的 Manim 代码保存 → 在新环境中运行 → 检查输出一致性

验收标准：
  ✅ 代码可在干净 Python 环境中运行（pip install manim 后）
  ✅ 输出动画与原始一致（视觉对比 ≥ 95% 相似）
  ✅ 不依赖未声明的外部文件
  ✅ 代码有注释，可读

评分维度（每个 0-1）：
  reproducibility: 0.40
  dependency_clarity: 0.20
  code_quality: 0.25
  output_consistency: 0.15
```

---

## 五、基准任务卡：视频处理工具

> 适用工具：ffmpeg / DaVinci Resolve / CapCut / Premiere
> 基准集名称：`video_processing_bench`

### 任务 V1：格式转换与合成

```
任务 V1：格式转换与合成
━━━━━━━━━━━━━━━━━━━━
测试素材：使用项目提供的 sample_video.mp4 + sample_audio.mp3 + sample_subtitle.srt

任务步骤：
  1. 将视频从 H.264 转码为 H.265（保持质量）
  2. 合成视频 + 音频 + 字幕（烧录）
  3. 裁剪为前 60 秒
  4. 输出 1080p MP4

验收标准：
  ✅ 输出视频可播放
  ✅ 音频同步（偏差 < 0.3s）
  ✅ 字幕正确烧录且同步
  ✅ 文件大小 < 原视频的 80%（H.265 压缩率）

评分维度（每个 0-1）：
  format_correctness: 0.25
  a_v_sync: 0.25
  subtitle_accuracy: 0.25
  compression_efficiency: 0.25
```

### 任务 V2：批量处理

```
任务 V2：批量处理
━━━━━━━━━━━━━━━━━━
测试方式：对 10 个视频文件批量执行 V1 任务

验收标准：
  ✅ 10/10 视频成功处理
  ✅ 无内存泄漏或崩溃
  ✅ 处理总时间 < 单文件 × 10 × 1.2（批处理开销 ≤ 20%）
  ✅ 每个文件输出符合 V1 标准

评分维度（每个 0-1）：
  batch_completion_rate: 0.40
  resource_efficiency: 0.25
  error_rate: 0.20
  parallel_support: 0.15
```

---

## 六、基准任务卡：TTS 引擎

> 适用工具：Edge TTS / ElevenLabs / OpenAI TTS / Coqui
> 基准集名称：`tts_bench`

### 任务 TTS1：中文旁白质量

```
任务 TTS1：中文旁白质量
━━━━━━━━━━━━━━━━━━━━
测试文本（含专业术语）：
  "细胞吞噬是一个复杂的过程。首先，细胞膜通过受体识别病原体，
  然后通过肌动蛋白聚合推动伪足伸展，包裹病原体形成吞噬体。
  随后，吞噬体与溶酶体融合，形成吞噬溶酶体，
  其中的酸性水解酶和活性氧将病原体降解。"

验收标准：
  ✅ 所有医学术语发音正确（细胞膜/吞噬体/溶酶体/伪足/水解酶）
  ✅ 语调自然，有适当的停顿
  ✅ 中文流畅，无英文口音
  ✅ 语速适合教学（约 150-180 字/分钟）

评分维度（每个 0-1）：
  pronunciation_accuracy: 0.35  — 尤其专业术语
  naturalness: 0.25             — 语调自然度
  pacing: 0.20
  clarity: 0.20                 — 清晰度
```

### 任务 TTS2：多语言混合

```
任务 TTS2：多语言混合
━━━━━━━━━━━━━━━━━━━━
测试文本（中英混合）：
  "研究表明，使用 CRISPR-Cas9 系统进行基因编辑时，
  sgRNA 的设计对 on-target efficiency 至关重要。
  PAM 序列（NGG）是 Cas9 识别和切割 DNA 的必要条件。
  在 Nature Communications 2024 年的一项研究中..."

验收标准：
  ✅ 中文和英文切换自然
  ✅ 英文术语发音正确
  ✅ 缩略语发音正确（如 Cas9 读作 "C-A-S-9" 而非 "cas-nine"）
  ✅ 数字和符号处理正确

评分维度（每个 0-1）：
  mixed_language_fluency: 0.40
  abbreviation_handling: 0.30
  english_pronunciation: 0.30
```

---

## 七、基准任务卡：代码生成与执行引擎

> 适用工具：Claude Code / Codex CLI / GPT-4 + CodeInterpreter
> 基准集名称：`code_generation_bench`

### 任务 C1：数据分析脚本

```
任务 C1：数据分析脚本
━━━━━━━━━━━━━━━━━━
测试方式：给定一个 CSV 文件（sample_data.csv），要求生成 Python 分析脚本

要求：
  1. 读取 CSV
  2. 描述性统计（均值、标准差、分位数）
  3. 缺失值检测和报告
  4. 生成 2 张图表（分布直方图 + 相关性热力图）
  5. 输出 Markdown 分析报告

验收标准：
  ✅ 脚本可一次运行成功（无 import 错误、语法错误）
  ✅ 统计量计算正确
  ✅ 图表生成正确且有标题/轴标签
  ✅ Markdown 报告格式正确

评分维度（每个 0-1）：
  first_run_success: 0.30     — 不需修改即可运行
  correctness: 0.30            — 数据计算正确
  code_quality: 0.20           — 可读性/注释/错误处理
  output_quality: 0.20         — 图表和报告质量
```

### 任务 C2：错误处理与修复

```
任务 C2：错误处理与修复
━━━━━━━━━━━━━━━━━━━━
测试方式：故意给一个缺少 import 和包含语法错误的 Python 脚本，
  要求工具发现并修复所有错误

验收标准：
  ✅ 发现所有错误（≥3 个）
  ✅ 修复后脚本可运行
  ✅ 修复不引入新错误
  ✅ 修复说明清晰

评分维度（每个 0-1）：
  error_detection: 0.35
  fix_correctness: 0.35
  fix_quality: 0.30
```

### 任务 C3：跨文件操作

```
任务 C3：跨文件操作
━━━━━━━━━━━━━━━━━━
测试方式：给定一个包含 5 个 Python 文件的小项目，
  要求找到所有文件中的 TODO 注释并汇总到一个 report.md

验收标准：
  ✅ 正确扫描所有 5 个文件
  ✅ 提取所有 TODO 注释（无遗漏）
  ✅ 汇总报告格式清晰
  ✅ 包含文件路径 + 行号 + TODO 内容

评分维度（每个 0-1）：
  completeness: 0.40
  accuracy: 0.30
  report_quality: 0.30
```

---

## 八、基准任务卡：学术文献检索工具

> 适用工具：PubMed API / Semantic Scholar / OpenAlex / Web of Science
> 基准集名称：`literature_search_bench`

### 任务 L1：精准检索

```
任务 L1：精准检索
━━━━━━━━━━━━━━━━
查询："2020-2025 年发表的，关于 CRISPR-Cas9 在 β-地中海贫血
  基因治疗中的临床试验和临床前研究"

验收标准：
  ✅ 返回 ≥ 10 篇相关文献
  ✅ 前 5 篇的 relevance ≥ 80%（人工判断）
  ✅ 包含至少 2 篇临床试验（clinical trial）
  ✅ 排除纯基础研究（basic research）的比例 ≥ 70%

评分维度（每个 0-1）：
  precision: 0.40             — 前 20 篇相关比例
  recall: 0.30                 — 是否遗漏重要文献
  query_parser: 0.20           — 是否正确理解复杂查询
  date_filter: 0.10            — 日期过滤准确性
```

### 任务 L2：引用信息完整性

```
任务 L2：引用信息完整性
━━━━━━━━━━━━━━━━━━━━
测试方式：检索后，检查返回的文献元数据完整性

验收标准：
  ✅ 每篇包含：标题、作者、期刊、年份、DOI
  ✅ ≥ 80% 包含摘要
  ✅ ≥ 60% 包含引用计数
  ✅ 无错误元数据（如错误期刊名/年份）

评分维度（每个 0-1）：
  metadata_completeness: 0.40
  abstract_availability: 0.25
  citation_count_accuracy: 0.15
  zero_error_rate: 0.20
```

---

## 九、基准任务卡：演示文稿生成

> 适用工具：python-pptx / Reveal.js / Canva API / Google Slides API
> 基准集名称：`presentation_bench`

### 任务 P1：数据报告 PPT

```
任务 P1：数据报告 PPT
━━━━━━━━━━━━━━━━━━
prompt: "基于以下数据生成 5 页 PPT：
  - 页面 1：标题页（项目名 + 日期 + 作者）
  - 页面 2：背景与目标（bullets）
  - 页面 3：关键数据（含图表）
  - 页面 4：分析结论（bullets + 高亮数字）
  - 页面 5：下一步行动（numbered list）
  主题色：深蓝 + 白色，整洁商务风格"

验收标准：
  ✅ PPT 可用 PowerPoint 打开
  ✅ 5 页全部生成
  ✅ 图表嵌入在页面 3
  ✅ 风格统一（字体/颜色/布局）
  ✅ 无文字溢出/重叠

评分维度（每个 0-1）：
  slide_completeness: 0.25
  visual_design: 0.25
  data_accuracy: 0.25
  text_quality: 0.25
```

---

## 十、基准任务卡：网页操作/Computer Use

> 适用工具：Playwright Agent / Puppeteer Agent / Claude Computer Use
> 基准集名称：`computer_use_bench`

### 任务 CU1：表单预填

```
任务 CU1：表单预填
━━━━━━━━━━━━━━━━
测试方式：打开一个测试网页表单（含 text/select/radio/checkbox），
  自动识别字段并填入预设数据

验收标准：
  ✅ 字段识别率 ≥ 90%
  ✅ 预填准确率 ≥ 90%（每个字段填对了）
  ✅ 选择框/单选框正确选择
  ✅ 未触发前端校验错误

评分维度（每个 0-1）：
  field_recognition: 0.35
  fill_accuracy: 0.35
  interaction_correctness: 0.20  — 如何处理 select/radio/checkbox
  error_avoidance: 0.10
```

### 任务 CU2：截图识别

```
任务 CU2：截图识别
━━━━━━━━━━━━━━━━
测试方式：给定 3 张软件界面截图，识别界面元素，
  生成操作步骤说明书

验收标准：
  ✅ 识别所有可交互元素（按钮/输入框/下拉菜单）
  ✅ 操作步骤逻辑正确
  ✅ 说明书可被新用户跟随操作
  ✅ 中英文界面都能识别

评分维度（每个 0-1）：
  element_detection: 0.30
  step_accuracy: 0.35
  instruction_clarity: 0.20
  language_support: 0.15
```

---

## 十一、跨工具基准任务：对比评估

> 用于同时评测多个工具在同一任务上的相对表现。
> 每个对比任务生成一份 [[Tool-Agent Router：最佳工具与最佳执行者选择器]] 可消费的评分数据。

### 任务 X1：图像生成工具大对比

```
任务 X1：图像生成工具大对比
━━━━━━━━━━━━━━━━━━━━━━━━
参与工具：Nano Banana Pro / ComfyUI+SDXL / DALL-E 3 / Midjourney / Flux

任务：同时执行 I1（医学信息图）+ I2（文字准确性）+ I3（风格一致性）

输出：
  ┌──────────────┬────────┬────────┬────────┬────────┬────────┐
  │   维度        │Nano Pro│ComfyUI │DALL-E 3│   MJ   │  Flux  │
  ├──────────────┼────────┼────────┼────────┼────────┼────────┤
  │ 结构准确性    │  0.85  │  0.70  │  0.60  │  0.55  │  0.78  │
  │ 文字准确性    │  0.92  │  0.65  │  0.55  │  0.40  │  0.82  │
  │ 风格一致性    │  0.88  │  0.90  │  0.75  │  0.85  │  0.80  │
  │ 速度          │  0.92  │  0.60  │  0.85  │  0.70  │  0.75  │
  │ 成本          │  0.75  │  0.90  │  0.80  │  0.50  │  0.85  │
  │ 可复现性      │  0.70  │  0.95  │  0.60  │  0.55  │  0.80  │
  │ 局部编辑      │  0.80  │  0.90  │  0.70  │  0.50  │  0.75  │
  ├──────────────┼────────┼────────┼────────┼────────┼────────┤
  │ 加权总分     │ 0.843 │ 0.772 │ 0.686 │ 0.582 │ 0.791 │
  └──────────────┴────────┴────────┴────────┴────────┴────────┘

此数据直接影响 Tool-Agent Router 的 task_fit + success_rate + output_quality 评分。
```

### 任务 X2：动画工具大对比

```
任务 X2：动画工具大对比
━━━━━━━━━━━━━━━━━━━━
参与工具：Blender / Manim / After Effects / AI Video Generator

任务：制作同一主题（细胞吞噬）的 30 秒动画

对比维度：
  scientific_accuracy  — Blender:0.95 | Manim:0.90 | AE:0.85 | AI:0.60
  visual_quality       — Blender:0.90 | Manim:0.70 | AE:0.95 | AI:0.75
  controllability      — Blender:0.98 | Manim:0.98 | AE:0.95 | AI:0.45
  script_reproducibility—Blender:0.95| Manim:0.98 | AE:0.60 | AI:0.20
  production_speed     — Blender:0.40 | Manim:0.70 | AE:0.50 | AI:0.85
  cost                 — Blender:0.90 | Manim:0.90 | AE:0.30 | AI:0.50
```

---

## 十二、基准结果如何影响系统

```
新工具进入 Omega
      ↓
工具类别匹配 → 加载对应的 Benchmark Cards
      ↓
在 Docker 沙箱中按序执行基准任务
      ↓
每项任务生成 score_card（YAML，含每维度分 + 综合分）
      ↓
score_card 写入 Tool Reputation Ledger
      ↓
Tool-Agent Router 自动加载新评分
      ↓
工具生命周期状态更新：benchmarked → candidate（如通过 ≥60% 任务）
      ↓
与 preferred 工具对比 → 触发替换评估（Auto-Upgrade Policy）
```

### Score Card 输出格式

```yaml
benchmark_result:
  tool: "Nano Banana Pro"
  tool_category: "image_generation"
  benchmark_version: "v1.0"
  tested_date: "2026-05-15"
  
  tasks:
    I1_medical_infographic:
      passed: true
      scores:
        structural_accuracy: 0.85
        text_accuracy: 0.92
        visual_clarity: 0.88
        annotation_quality: 0.82
        medical_style_appropriateness: 0.90
      composite: 0.874
      notes: "伪足动态感稍弱，但不影响教学使用"
    
    I2_text_accuracy_stress:
      passed: true
      scores:
        text_precision: 0.95
        layout_readability: 0.85
        scientific_correctness: 0.90
      composite: 0.913
      notes: "复合物 IV 的罗马数字 IV 与英文间距稍大"
    
    # ... 其他任务 ...
  
  overall:
    pass_rate: 5/6           # 通过的任务数/总任务数（含选测）
    mandatory_pass_rate: 5/5 # 所有必测任务必须通过
    weighted_total: 0.882    # 加权总分
    benchmark_passed: true   # ≥ 60% 即为通过
    recommended_phase: "candidate"
```

---

## 十三、基准任务与风险域的关系

| 工具风险域 | 最少通过任务数 | 最少观察次数 | 进入 candidate 条件 |
|-----------|:-----------:|:----------:|-------------------|
| 低风险（格式转换/草稿生成） | 3/5 必测 | 5 次 | 加权总分 ≥ 0.65 |
| 中风险（代码生成/数据分析） | 4/5 必测 | 10 次 | 加权总分 ≥ 0.75 |
| 高风险（医学结论/核心系统） | 5/5 必测 + 全部选测 | 20 次 | 加权总分 ≥ 0.85 |

---

## 十四、相关页面

- [[Tool-Agent Router：最佳工具与最佳执行者选择器]] — 消费基准评分数据
- [[Model and Tool Lifecycle Manager]] — 基准通过后的生命周期流转
- [[Tool Reputation Ledger]] — 基准结果的持久化存储
- [[Auto-Upgrade Policy]] — 基准评分触发替换的阈值
- [[Creative Tool Router]] — 图像/动画/视频工具的具体选择逻辑
- [[External AI Rolebook]] — 各工具生态位的完整描述
- [[SOTA Source Hierarchy：顶尖工具来源分级]] — 基准验证的可信度来源
