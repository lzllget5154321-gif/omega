---
type: concept
tags: [omega-ecosystem, lifecycle-manager, model-upgrade, tool-replacement, auto-upgrade]
created: 2026-05-15
updated: 2026-05-15
knowledge_stability: evolving
parent: [[AI工具生态雷达]]
related:
  - [[Auto-Upgrade Policy]]
  - [[Tool Reputation Ledger]]
  - [[Tool-Affordance Graph]]
  - [[Tool-Agent Router：最佳工具与最佳执行者选择器]]
  - [[Evolution Loop]]
---

# Model and Tool Lifecycle Manager

> **定位**：管理 Omega 中所有工具、模型、Adapter 和 Skill 的完整生命周期——从发现到退役。回答用户的核心问题：**"如果某个 Agent 或 AI 发布了新模型，Omega 会不会自动识别并提醒我更替？或者自动更替？"**

---

## 一、生命周期状态

每个工具/模型在 Omega 中经历 9 个状态：

```
discovered → investigating → sandbox_tested → benchmarked
                                                      ↓
                                              candidate → integrated
                                                              ↓
                                                         preferred
                                                              ↓
                                                    deprecated → retired
```

| 状态 | 含义 | 进入条件 | 离开条件 |
|------|------|---------|---------|
| `discovered` | 雷达发现，仅记录 | AI 工具生态雷达扫描到新工具 | 被标记为 investigate |
| `investigating` | 正在深度评估 | 雷达标记为 investigate / 用户指令 | 完成文档评估 + 手动标记 |
| `sandbox_tested` | 已在沙箱中成功运行 | Toolsmith-Lite 试用通过 | 完成基准测试 |
| `benchmarked` | 已通过基准任务测试 | 在 Functional Benchmark Garden 中通过 ≥60% 任务 | 被标记为 candidate |
| `candidate` | 可作为候选工具 | 通过基准测试 + Tool Reputation Ledger 准入 | 首次在生产任务中成功使用 |
| `integrated` | 已进入 Capability Fabric | 首次生产任务成功 + Adapter 注册 | 成为 preferred 或降级 |
| `preferred` | 当前该类任务的优先工具 | 连续成功 + 评分超过前任 preferred | 被新工具超越或退役 |
| `deprecated` | 不再推荐使用 | 被更好工具超越 / 维护停滞 / 安全漏洞 | 所有依赖迁移完成 |
| `retired` | 已从系统中移除 | 无活跃依赖 + 替代工具就绪 | — |

---

## 二、生命周期事件与自动行为

### 2.1 新模型/新工具发布

```
事件：AI 工具生态雷达检测到新模型发布
  （如 Anthropic 发布 Claude 4.x，Google 发布新图像模型，社区发布新 MCP Server）

自动行为（无需用户干预）：
  1. 生成工具摘要卡（YAML 格式）
  2. 写入 AI 工具注册表（10-外部AI与工具注册表/）
  3. 标记为 discovered
  4. 评估与 Omega 功能域的匹配度
  5. 如果匹配度 high → 自动标记为 investigating
  6. 加入预学习队列（按优先级排序）

通知用户（周报中）：
  "本周发现 N 个新工具，其中 X 个与你的工作域高度相关：
   1. [工具名] — 可能提升 Y 类任务的效率 Z%"
```

### 2.2 自动试用与测试

```
事件：工具进入 investigating → sandbox_tested

自动行为：
  1. Toolsmith-Lite 在 Docker 沙箱中安装和试跑
  2. 运行工具的基本功能测试
  3. 生成初始信誉评分
  4. 如果试用通过 → 自动进入 benchmarked
  5. 如果试用失败 → 标记为 discovered + 记录失败原因

通知用户：
  "新工具 [X] 已通过沙箱试用：成功执行 Y，失败 Z。
   建议在功能基准任务花园中测试。"
```

### 2.3 基准测试通过后

```
事件：工具通过基准测试 → candidate

自动行为：
  1. 更新 Tool Reputation Ledger（信誉评分 + 基准测试结果）
  2. 更新 Tool-Affordance Graph（能力节点 + 边）
  3. 更新 Tool-Agent Router 的候选工具列表
  4. 在低风险任务中开始推荐（标注为"candidate, 需验证"）

通知用户：
  "工具 [X] 已通过基准测试（12/15 任务通过）。
   现已在低风险草稿任务中作为可选工具。是否升级为 integrated？"
```

### 2.4 替换旧工具（生态演替）

```
事件：candidate 工具的评分在同类任务中持续超过 preferred 工具

条件：
  1. 新工具在 ≥10 次同类任务中成功率 > 旧工具
  2. 新工具的加权评分 > 旧工具 × 1.15（15% 显著提升阈值）
  3. 新工具的 Tool Reputation Ledger 信誉 ≥ 0.70

自动行为：
  1. 低风险工具（如图像草稿生成）：
     → 自动将新工具标记为 preferred
     → 旧工具降级为 deprecated
     → 在周报中报告
  2. 中风险工具（如代码生成、数据分析）：
     → 自动推荐替换 + 等待用户确认
     → 展示对比数据（成功率/速度/质量/成本）
  3. 高风险工具（如医学结论、外部发布、核心系统工具）：
     → 仅提醒，不自动替换
     → 需要用户明确确认 + canary 测试

通知用户：
  "工具 [新] 在 [任务类型] 上持续优于 [旧]：
   - 成功率：94% vs 82%
   - 平均质量评分：0.88 vs 0.75
   - 成本：$0.03/次 vs $0.05/次
   建议替换。是否确认？"
```

### 2.5 工具退役

```
事件：工具触发退役条件

退役条件（满足任一）：
  1. 连续 20 次使用中成功率 < 60%
  2. 官方宣布停止维护（EOL）
  3. 发现严重安全漏洞（CVE High/Critical）
  4. API 服务下线
  5. 许可证变更导致不可用
  6. 被 ≥2 个替代工具在全部维度上超越

自动行为：
  1. 标记为 deprecated
  2. 停止在新任务中推荐
  3. 自动为已有依赖寻找替代工具
  4. 生成迁移计划
  5. 当所有依赖迁移完成后 → 标记为 retired

通知用户：
  "工具 [X] 将被退役：
   原因：[EOL / 成功率低 / 安全漏洞]
   替代方案：[Y] 或 [Z]
   影响的任务：[列出仍依赖此工具的 Skill/Workflow]
   迁移计划：[自动迁移 / 需要你手动确认]"
```

---

## 三、自动更替 vs 人工确认的边界

| 场景 | 自动行为 | 需要人工 |
|------|---------|---------|
| **低风险草稿图像生成** | ✅ 自动替换为评分更高的工具 | ❌ |
| **一般文档/代码生成** | ✅ 自动推荐 + 展示对比 | 确认替换 |
| **数据分析** | ✅ 自动测试 + 展示对比 | 确认替换 |
| **医学结论/诊断相关** | ❌ 仅提醒 | ✅ 必须确认 |
| **论文投稿/外部发布** | ❌ 仅提醒 | ✅ 必须确认 |
| **需要付费 API** | ❌ 仅提醒 | ✅ 必须确认 |
| **涉及隐私/敏感数据** | ❌ 仅提醒 | ✅ 必须确认 |
| **核心系统工具（Docker/Git/Obsidian）** | ❌ 仅提醒 | ✅ 必须确认 + canary |
| **原工具已完全失效（API下线）** | ✅ 自动切换到备选 | 通知（非确认） |
| **安全漏洞紧急替换** | ✅ 自动暂停使用 | 确认替换方案 |

---

## 四、质量模式与生命周期

当用户指定 `quality_profile: highest_quality` 时，生命周期管理的行为变化：

| 维度 | 标准模式 | 最高质量模式 |
|------|---------|------------|
| **新工具准入门槛** | 基准测试通过率 ≥ 60% | 基准测试通过率 ≥ 85% |
| **替换阈值** | 新工具评分 > 旧工具 × 1.15 | 新工具评分 > 旧工具 × 1.25 |
| **替换前观察期** | 5 次同类任务 | 15 次同类任务 |
| **人工审查** | 低风险工具自动 | 全部工具（包括低风险）需 confirm |
| **回滚准备** | 备选工具就绪 | 备选工具 + 回滚脚本就绪 |

---

## 五、生命周期仪表盘

在 Ω 操作界面中（阶段 3），生命周期状态以仪表盘形式展示：

```text
┌─────────────────────────────────────────────────────────────┐
│  🛠 工具生命周期仪表盘                                        │
│                                                               │
│  总工具数：47 | Preferred: 12 | Integrated: 18 | Candidate: 3│
│  Investigating: 5 | Deprecated: 7 | Retired: 2               │
│                                                               │
│  ⚠️ 需要关注：                                                │
│  · [Tool-A] 退役提醒 — 维护已停止 3 个月，建议替换              │
│  · [Tool-B] 升级可用 — v2.3 → v3.0（性能提升 40%）             │
│  · [Model-C] 新版本发布 — 需要在基准花园中测试                  │
│                                                               │
│  📊 本周变更：                                                │
│  · Nano Banana Pro → preferred（医学信息图）                   │
│  · ComfyUI v4.2 → integrated（新增 3D 生成节点）               │
│  · Tool-D → deprecated（成功率降至 58%）                       │
└─────────────────────────────────────────────────────────────┘
```

---

## 六、相关页面

- [[AI工具生态雷达]] — 工具的发现和初始评估
- [[Auto-Upgrade Policy]] — 自动升级的详细策略
- [[Tool Reputation Ledger]] — 工具信誉数据
- [[Tool-Affordance Graph]] — 工具能力图谱
- [[Tool-Agent Router：最佳工具与最佳执行者选择器]] — 使用生命周期状态影响路由
- [[Evolution Loop]] — 生态演替的驱动引擎
- [[SOTA Source Hierarchy：顶尖工具来源分级]] — 新工具来源的信誉权重
