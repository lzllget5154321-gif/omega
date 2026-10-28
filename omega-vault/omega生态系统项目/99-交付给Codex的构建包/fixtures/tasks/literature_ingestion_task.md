# 验收任务：文献检索与知识摄取
# ==============================
# 此文件是 Omega 功能基准闭环 1 的验收任务。
# Codex 构建完成后，执行以下命令验证闭环 1：
#   omega task --from "fixtures/tasks/literature_ingestion_task.md"
#
# 验收标准：
#   ✅ 成功调用 PubMed / Semantic Scholar API
#   ✅ 返回 ≥10 篇相关文献
#   ✅ 每篇文献创建 wiki/来源/ 页面
#   ✅ 来源页含 quality/noise_ratio/credibility/knowledge_stability 字段
#   ✅ ≥2 规则触发时自动创建概念页
#   ✅ 更新 wiki/index.md 和 wiki/log.md

task_type: literature_search
complexity: branching
autonomy_level: L1
quality_profile: balanced
user_goal: "检索 2022-2025 年关于 SGLT2 抑制剂肾脏保护作用的系统综述和 Meta 分析"
expected_outcome:
  primary_deliverables:
    - "≥10 个 wiki/来源/ 页面创建（含 quality/noise_ratio/credibility/knowledge_stability）"
    - "wiki/log.md 追加操作记录"
  secondary_deliverables:
    - "触发 ≥2 规则的概念页"
    - "SGLT2 抑制剂相关实体页更新"
    - "若 ZOTERO_API_KEY 已配置 → ≥10 篇文献同步至 Zotero"
    - "若 ZOTERO_API_KEY 未配置 → 生成 BibTeX/RIS 文件供后续手动导入"
  zotero_behavior: "conditional"  # Zotero Key 存在则同步，不存在则导出 BibTeX/RIS
constraints:
  max_time_minutes: 15
  language: zh-CN
