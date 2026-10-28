# 验收任务：数据分析
# ==================
# 此文件是 Omega 功能基准闭环 3 的验收任务。
# Codex 构建完成后，执行以下命令验证闭环 3：
#   omega task --from "fixtures/tasks/data_analysis_task.md"
#
# 验收标准：
#   ✅ 成功读取 CSV
#   ✅ 描述性统计量计算正确
#   ✅ 生成 ≥2 张图表（PNG 格式，含标题和轴标签）
#   ✅ 输出 Markdown 格式分析报告
#   ✅ 缺失值检测和报告

task_type: data_analysis
complexity: branching
autonomy_level: L1
quality_profile: balanced
user_goal: "分析 fixtures/data/sample_clinical.csv 文件，生成完整的描述性统计报告和图表"
expected_outcome:
  primary_deliverables:
    - "Markdown 分析报告（含统计量 + 图表嵌入）"
    - "≥2 张 PNG 图表"
  secondary_deliverables:
    - "缺失值报告"
    - "数据质量评估"
constraints:
  max_time_minutes: 10
  language: zh-CN
