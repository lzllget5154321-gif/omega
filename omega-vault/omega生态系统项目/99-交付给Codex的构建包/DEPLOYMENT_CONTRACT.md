# Omega 部署契约 — Codex 全权部署边界定义
# ===============================================================
# 目的：定义"全权部署"的具体边界——Codex 能自动做什么、必须用户确认什么、
# 永远不自动做什么。防止 Codex 做了不该做的事，也防止 Codex 因过度保守而
# 每步都问用户。
#
# 版本：v1.0 — 2026-05-17

version: "1.1"
last_updated: "2026-05-18"
applies_to: "Omega v0.3.0-mfe → v1.0.0-full 全权部署"

# ═══════════════════════════════════════════
# 第一类：Codex 可自动执行（无需询问）
# ═══════════════════════════════════════════
auto_actions:

  - category: 文件创建与编辑
    scope: "{OMEGA_HOME}/omega-runtime/ 内的所有 .py/.yaml/.json/.md 文件"
    allowed:
      - "创建新文件（app/、tests/、config/ 等）"
      - "修改已有源文件（按 UPGRADE_GUIDE.md 规范）"
      - "运行 pytest、mypy、omega bench 等验证命令"
    not_allowed:
      - "修改 {OMEGA_HOME}/omega-vault/wiki/ 中的知识页（除非通过 knowledge_steward Agent 的候审流程）"
      - "修改 {OMEGA_HOME}/omega-vault/CLAUDE.md（除非用户明确指令）"
      - "修改 .env 文件（API Key 敏感信息）"

  - category: Docker 操作
    allowed:
      - "docker compose build 构建镜像"
      - "docker compose up -d 启动容器"
      - "docker compose down 停止容器"
      - "docker exec 在沙箱内执行命令"
      - "docker ps / docker logs 查看状态"
    not_allowed:
      - "docker system prune 删除未使用的镜像/卷（可能误删用户其他项目数据）"
      - "docker volume rm 删除命名卷（数据不可恢复）"
      - "修改 docker-compose.yml 中的端口映射（可能冲突用户已有服务）"

  - category: Python 环境
    allowed:
      - "pip install 在 {OMEGA_HOME}/omega-runtime/.venv 中安装依赖"
      - "pip install --upgrade 升级 Omega 的依赖"
      - "python -m venv 创建虚拟环境（仅限 OMEGA_HOME 内）"
    not_allowed:
      - "pip install 到系统全局 Python"
      - "修改系统 PATH 或环境变量（除 OMEGA_HOME 相关）"

  - category: Git 操作
    allowed:
      - "git add + git commit 在 {OMEGA_HOME}/omega-runtime/ 中提交"
      - "git log / git status / git diff 查看状态"
      - "git branch 创建新分支"
    not_allowed:
      - "git push 到远程仓库（除非用户明确授权）"
      - "git reset --hard / git clean -f 等破坏性操作"
      - "修改 .gitignore 排除敏感文件以外的条目"

  - category: 模拟构建
    allowed:
      - "omega simulate phase-N 生成模拟报告（不修改任何文件）"
      - "展示 DAG/风险/变更清单给用户审查"
    requirement: "每个升级阶段必须先 simulate，展示结果后再等待用户确认"

# ═══════════════════════════════════════════
# 第二类：必须用户确认（Codex 暂停等待）
# ═══════════════════════════════════════════
require_confirmation:

  - action: "API Key 配置"
    trigger: "任何需要新 API Key 的操作"
    behavior: "暂停，说明需要哪个 API 和获取 URL，等待用户填入 .env"
    rationale: "API Key 是用户的付费凭据，Codex 不能代替用户注册/付费"

  - action: "外部账号登录"
    trigger: "需要 GitHub/Zotero/PubMed/浏览器登录"
    behavior: "暂停，说明需要登录哪个服务和为什么，等待用户确认已完成"
    rationale: "外部账号是用户的身份凭据"

  - action: "系统级变更"
    trigger: "修改环境变量、注册表、防火墙规则、Windows 服务"
    behavior: "暂停，展示变更内容和原因，等待用户确认"
    rationale: "可能影响用户电脑上其他软件"

  - action: "Docker 卷删除或重建"
    trigger: "docker volume rm 或需要清空 PostgreSQL/Qdrant 数据"
    behavior: "暂停，警告数据不可恢复，等待用户确认"
    rationale: "可能丢失用户已积累的行动记忆和知识索引"

  - action: "External API 调用（非语言引擎）"
    trigger: "调用 PubMed/Semantic Scholar/GitHub/Brave Search 等外部 API"
    behavior: "首次使用时暂停，说明用途和频率，等待用户确认。后续同类调用自动放行"
    rationale: "可能产生 API 费用或触发频率限制"

  - action: "Omega evolve --upgrade 的 HIGH/CRITICAL 级别"
    trigger: "ECP 风险级别为 HIGH 或 CRITICAL"
    behavior: "暂停，展示 ECP 审批摘要（变更内容/风险评估/回滚方案），等待用户 approve/reject"
    rationale: "可能破坏现有功能或引入不兼容变更"

  - action: "Omega 升级到下一 Phase 前"
    trigger: "完成当前 Phase 全部验证，准备开始下一 Phase"
    behavior: "暂停，展示当前 Phase 的 ITERATION_N_REPORT.md 摘要，等待用户确认继续"
    rationale: "用户可能想检查当前阶段产物后再继续"

  - action: "Omega review approve（知识库写入）"
    trigger: "AI 生成内容准备写入 wiki/"
    behavior: "暂停，展示候审内容摘要，等待用户 approve/reject"
    rationale: "知识库是用户的长期资产，AI 不应自动写入"

# ═══════════════════════════════════════════
# 第三类：永远不自动做（红线）
# ═══════════════════════════════════════════
never_auto:

  - action: "上传/投稿/发表到外部平台"
    rationale: "法律和伦理边界——投稿系统、预印本服务器、社交媒体等的 Submit 操作必须人类执行"
    safety: "方法论安全红线 MED-03：封闭平台适配可截图/预填，不可自动 Submit"

  - action: "删除用户个人文件"
    rationale: "Omega 工作空间外的任何文件都是用户资产"
    exception: "Omega 在 omega-workspace/ 内创建的临时文件可以自动清理"

  - action: "修改系统级配置文件"
    rationale: "包括 Windows 注册表、hosts 文件、系统服务配置"
    scope: "C:\\Windows、/etc、系统环境变量等"

  - action: "安装系统级软件"
    rationale: "winget/apt/brew 等系统包管理器的安装操作"
    exception: "pip install 在 OMEGA_HOME 的 .venv 中允许（见第一类）"

  - action: "发送电子邮件/短信/通知到外部"
    rationale: "可能被误用为垃圾信息或钓鱼"
    exception: "写入本地 Obsidian vault 的 通知.md 允许（本地文件，非外部发送）"

  - action: "访问或修改其他 Obsidian vault"
    rationale: "Omega 仅操作 {OMEGA_HOME}/omega-vault/，不触碰用户的其他 vault"

  - action: "自动接受外部工具的 ToS/隐私协议"
    rationale: "法律协议必须由人类阅读并接受"

  - action: "修改 Omega 自身的安全策略文件"
    rationale: "risk_policy.yaml、guardian.py、隐私分级等安全文件只能由用户手动修改"
    exception: "按 UPGRADE_GUIDE.md 明确要求的新增安全模块代码（如 Phase 11 的 kb_guard.py）允许"

# ═══════════════════════════════════════════
# Codex 自检清单（每 Phase 开始前执行）
# ═══════════════════════════════════════════
self_check: |
  开始 Phase N 前，Codex 自问：
  1. 本 Phase 是否有 need_confirmation 类操作？ → 有则先取得用户确认
  2. 本 Phase 是否涉及 never_auto 红线？ → 是则跳过该操作，标记为"需用户手动执行"
  3. 是否先执行了 omega simulate phase-N？ → 未执行则先 simulate
  4. 本 Phase 是否需要新 API Key？ → 需要则先提示用户
  5. 本 Phase 是否会修改 omega-vault/wiki/？ → 会则通过 review 候审流程
  6. 本 Phase 是否涉及高风险操作？ → 每个高风险动作是否强制生成 terminal_event (risk_warning / approval_request)？
     → 详见 OMEGA_TERMINAL.md §十二"高风险动作强制 terminal_event 规则"
