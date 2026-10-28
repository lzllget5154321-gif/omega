---
type: concept
tags: [omega-ecosystem, version-history]
created: 2026-05-15
updated: 2026-05-15
knowledge_stability: stable
parent: [[omega生态系统项目-总说明]]
---

# Omega 生态系统项目 — 版本演化图

> 本文档记录 Omega 从 V2 论文到当前版本的完整演进路径。

## 演化时间线

```
V2 论文（AI Agent 生态系统终极研究）
  │  生态隐喻、工具使用、Agent 社会
  ▼
V3 论文
  │  主动性 + 社会性保留为核
  ▼
V4 论文
  │  行动枢纽保留为架构主体
  ▼
V5 论文
  │  Skill 降级为后台
  ▼
V6 论文
  │  安全/治理降级为后台使能器
  ▼
Omega v1.0（2026-05-15）
  │  功能优先总方法论发布（2007 行）
  │  九层架构定义 + 10 条核心原则 + 19 个专题全覆盖
  │  MFE 定义：6 个基准闭环
  ▼
Omega v1.1（2026-05-15）
  │  三大核心机制：Tool-Agent Router / 自我解惑与外援调用循环 / AI 工具生态雷达
  ▼
Omega v2.0（2026-05-15）
  │  Agent OS Layer 化：omega.yaml 本体配置 / 运行形态定义 / 阶段感知路由
  │  创意与科学可视化域 / 多模态成果包 / Dynamic Task Planner
  ▼
Omega v3.0（2026-05-15）
  │  信息质量与生态演化：SOTA 四级来源 / Best-Practice Harvester / 工具生命周期
  │  Social Signal Validator / Tool Benchmark Cards / Creative Tool Router
  │  External AI Rolebook / Auto-Upgrade Policy
  │  共 8 个关键机制页面全闭环
  ▼
Omega v3.1（2026-05-15）← 当前版本
  │  Codex 构建包全面升级：29 个 build-package 文件
  │  含 schema/config/fixtures/templates/scripts
  │  双沙箱策略 / Zotero 条件同步 / Windows 原生 + WSL2 双路径
  ▼
Omega MFE（目标：Codex 从零构建）
     CLI + 文献检索 + 数据分析 + 双沙箱 + 闭环验证
```

## 版本之间的关系

每个版本在前一版本基础上累加，而非替代：
- v1.0 的九层架构和 10 条核心原则 → 全程不变的基础
- v1.1 的 Router / 求助循环 / 雷达 → v2.0 的 Agent OS Layer 依赖
- v2.0 的 omega.yaml 和运行形态 → v3.0 的升级策略和工具生命周期依赖
- v3.0-v3.1 的构建包 → MFE 可构建性的前提

## 相关文档

- 总说明：[[omega生态系统项目-总说明]]
- 功能优先总方法论：[[omega生态系统项目-功能优先总方法论]]
- 运行形态：[[Omega运行形态与本体文件说明]]
- 构建指导书：[[Omega 构建指导书 — 给 Codex 的系统构造规范]]
