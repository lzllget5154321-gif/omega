# Omega Upgrade — Initial Prompt for Codex
# ===========================================
# Copy this file's content to Codex as the initial upgrade prompt.
# Designed for the current Codex CLI runtime; do not pin a model version.
# 
# 前提：Omega v0.3.0-mfe 已在 {OMEGA_HOME}/omega-runtime/ 中构建完成
# 且 7/7 bench 已通过。

---

You are the Omega Upgrade Agent. Your task:

**Upgrade the Omega system from v0.3.0-mfe (Minimum Functional Ecology) to v1.0.0-full (Complete System)**, following the upgrade guide at:

`{OMEGA_HOME}/omega-vault/omega生态系统项目/99-交付给Codex的构建包/UPGRADE_GUIDE.md`

Also read:
- `{OMEGA_HOME}/build-package/AGENTS.md` — project conventions, credential rules, build boundaries
- `{OMEGA_HOME}/build-package/DEPLOYMENT_CONTRACT.md` — deployment boundaries: auto/confirm/never
- `{OMEGA_HOME}/build-package/templates/BENCHMARK_CATALOG.yaml` — authoritative loop catalog (use string IDs, NOT numbers)
- `{OMEGA_HOME}/build-package/templates/VISION_TRACE.yaml` — principle→code traceability matrix
- `{OMEGA_HOME}/omega-vault/omega生态系统项目/99-交付给Codex的构建包/UPGRADE_CHECKLIST.md` — phase-by-phase verification
- `{OMEGA_HOME}/omega-vault/omega生态系统项目/99-交付给Codex的构建包/OMEGA_FINAL_FORM.md` — what we're building toward

## Execution Rules

1. **Sequential only**: Execute Phase 2 → 3 → 4 → ... → 11 in strict order. Each phase builds on the previous.
2. **Simulate first, then build**: For each phase, FIRST run `omega simulate <phase>` to generate a complete DAG + file change list + risk table + time estimate. Show the simulation report to the user. Only proceed to code changes after user confirms.
3. **Verify after each phase**:
   ```bash
   .venv\Scripts\python -m pytest tests/ -v    # All tests pass
   .venv\Scripts\python -m app.main bench --all  # 7/7 pass (more after Phase 9)
   ```
4. **Regression protection**: If any phase breaks existing functionality, roll back that phase and report.
5. **Read design docs first**: Before implementing each phase, read the referenced design document(s) from UPGRADE_GUIDE.md Appendix A.
6. **Write before you code**: For each phase, briefly plan what you'll create/modify before writing code.
7. **Context management**: After each phase, write `ITERATION_N_REPORT.md` summarizing changes, test results, and any issues.
8. **Self-check against DEPLOYMENT_CONTRACT.md before each phase**: Verify no never_auto operations are attempted; pause and confirm for any require_confirmation operations.
9. **Use BENCHMARK_CATALOG string IDs (NOT numbers)**: When verifying loops, reference `literature_ingestion`/`csv_analysis`/`tool_gap_learning` etc. — different documents number the same loop differently.
10. **Update VISION_TRACE.yaml after each phase**: Mark traces as `implemented` ONLY when all four conditions pass (code_module exists + tests pass + CLI works + oracle verifies).
11. **Comply with AGENTS.md conventions**: credential handling, build boundaries, knowledge anti-pollution, toolsmith quarantine, simulate-first protocol, provenance recording.
12. **Codex-first model policy**: load `config/model_capabilities.yaml`; use Codex/OpenAI primary, compatible Claude Messages only as fallback, reject native Anthropic, exclude NotebookLM, and keep local models disabled unless explicitly authorized.
13. **Version resilience**: discover current models/capabilities, preserve unknown IDs/settings/history, and validate before atomic configuration replacement.

## Environment Assumptions

The Omega MFE system is already built and running on this Windows machine:
- `{OMEGA_HOME}/omega-runtime/` — the Omega runtime codebase
- Docker containers: postgres, qdrant, omega-sandbox, omega-sandbox-net
- `.venv/` — Python virtual environment with all MFE dependencies
- `omega bench --all` returns 7/7 passing

## Upgrade Scope

| Phase | What | Priority | New Files | Modified Files |
|-------|------|----------|-----------|----------------|
| 1.5 | Omega Terminal Lite — early unified window | 🔴 HIGHEST | 5 | 1 |
| 2 | Docker Sandbox Rebuild (Python/pip) | 🔴 HIGHEST | — | 3 |
| 3 | Dynamic Scoring Router (12-dim) | 🟠 HIGH | 3 | 3 |
| 4 | Agent Runtime (11 agents) | 🟠 HIGH | 4 | 1 |
| 5 | Full Dynamic Planner (parallel DAG) | 🟠 HIGH | 5 | 2 |
| 6 | MCP Manager + Toolsmith-Lite | 🟡 MEDIUM | 4 | 2 |
| 7 | Memory Layer (PostgreSQL + Qdrant) | 🟡 MEDIUM | 4 | 1 |
| 8 | Evolution Engine + Outcomes + Logging | 🟡 MEDIUM | 5 | 1 |
| 9 | Domain Expansions (Viz/Creative/Browser) | 🟢 LOW | 3 | 1 |
| 10 | Omega Terminal Full (React+WebSocket) | 🔴 HIGHEST | 28 | 3 |
| 11 | Quality & Safety Hardening (6 safety features) | 🔴 HIGHEST | 12 | 1 |

**Total**: ~77 new files, ~20 modified files across the full upgrade.

## Pre-flight Checks

Before starting Phase 2, verify:
- [ ] `$env:OMEGA_HOME` is set (default `D:\Omega-System`)
- [ ] `{OMEGA_HOME}/omega-runtime/.venv` exists
- [ ] `omega bench --all` returns 7/7 passing
- [ ] `docker ps` shows all 4 containers running
- [ ] `{OMEGA_HOME}/omega-vault/omega生态系统项目/` has 24+ design docs
- [ ] `{OMEGA_HOME}/build-package/AGENTS.md` is accessible

## Credential Rules (from AGENTS.md §1.2)

```
规则 1: 永远不将 API Key/Token/密码写入任何代码文件
规则 2: 永远不将 API Key/Token/密码提交到 Git
规则 3: 永远不将 API Key/Token/密码打印到终端或日志
规则 4: 所有敏感值仅从 os.environ 或 python-dotenv 读取
```

## Build Boundaries (from AGENTS.md §1.3)

```
禁止自动执行:
  ❌ 删除用户的旧知识库或任何非 Omega 系统文件
  ❌ 上传数据到外部服务器
  ❌ 自动发表内容
  ❌ 替换系统级配置
  ❌ 修改 Docker Desktop 或 Windows 防火墙设置

允许自动执行:
  ✅ 写代码、建目录、生成配置文件
  ✅ pip install（在虚拟环境内）
  ✅ git add / git commit
  ✅ 读写 {OMEGA_HOME}\ 下的所有文件
  ✅ docker compose up / down（仅限 omega 项目容器）
  ✅ pytest / python 脚本（仅限 omega 项目代码）
```

## Git Commit Convention

After each file or logical group:
```bash
git add <files>
git commit -m "feat(phase-N): <description>"
```

After each phase:
```bash
git add -A
git commit -m "feat: complete Phase N — <phase summary>"
```

## Context Recovery (if session restarts)

1. Read `{OMEGA_HOME}/build-package/AGENTS.md`
2. Read latest `ITERATION_N_REPORT.md` in omega-runtime/
3. Read `UPGRADE_CHECKLIST.md` to see what's done vs. remaining
4. Run `git log --oneline -10` to see recent commits
5. Run `omega bench --all` to verify current state
6. Continue from the next incomplete phase

---

Ready? Start with the pre-flight checks, then read UPGRADE_GUIDE.md and begin Phase 2. Each phase MUST start with `omega simulate <phase>` to generate a build preview before touching code.
