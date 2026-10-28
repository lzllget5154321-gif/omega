# 验收任务：工具学习与注册
# ============================
# Omega 功能基准闭环 11 的验收任务。
# Codex 构建完成后，执行以下命令验证闭环 11：
#   omega task --from "fixtures/tasks/tool_learning_task.md"
#
# 验收标准：
#   ✅ 在 omega-sandbox-net（有限网络）中自动安装一个预置工具
#   ✅ 在 omega-sandbox（无网络）中离线验证工具可运行
#   ✅ 生成符合 tool_card.schema.json 的工具注册卡
#   ✅ 评估报告含能力/cost/风险/限制 4 个维度
#   ✅ 工具注册卡写入 config/tools.yaml
#
# 双沙箱策略说明：
#   omega-sandbox-net: 有限网络（仅 GitHub/PyPI/npm/docs）用于下载安装
#   omega-sandbox:     无网络（network_mode: none）用于离线验证

task_type: tool_learning
complexity: linear
autonomy_level: L2
quality_profile: balanced
user_goal: "试用一个未知的 CLI 数据查询工具 csvkit（或等效工具），评估其能力并注册到 Omega 工具生态"
expected_outcome:
  primary_deliverables:
    - "在 omega-sandbox-net 中成功安装目标工具"
    - "在 omega-sandbox 中离线运行工具（验证无网络可行性）"
    - "生成符合 tool_card.schema.json 的工具注册卡"
    - "工具注册到 config/tools.yaml"
  secondary_deliverables:
    - "评估报告（含能力/cost/风险/限制 4 维度）"
    - "沙箱隔离验证报告（确认 omega-sandbox 内无网络访问）"
constraints:
  max_time_minutes: 12
  language: zh-CN
  sandbox_strategy: dual  # omega-sandbox-net 安装 → omega-sandbox 验证
  allowed_network: [pypi.org, files.pythonhosted.org, github.com, raw.githubusercontent.com]
