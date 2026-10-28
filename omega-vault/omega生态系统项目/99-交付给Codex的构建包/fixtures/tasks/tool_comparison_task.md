# 验收任务：工具对比报告
# ======================
# Omega 功能基准闭环 10 的验收任务。
# 验收命令：omega task --from "fixtures/tasks/tool_comparison_task.md"
#
# 验收标准：
#   ✅ 对比维度 ≥8
#   ✅ 每个维度有具体数据支撑
#   ✅ 生成 wiki/对比/ 页面
#   ✅ 页面含 Wikilink 连接相关工具

task_type: tool_comparison
complexity: branching
autonomy_level: L1
quality_profile: balanced
user_goal: "对比 Blender 和 Manim 在医学动画制作中的优劣，生成结构化对比报告"
expected_outcome:
  primary_deliverables:
    - "wiki/对比/Blender vs Manim 医学动画.md"
  secondary_deliverables:
    - "最佳实践指南 YAML"
constraints:
  max_time_minutes: 20
  language: zh-CN
