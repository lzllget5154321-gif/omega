# Omega 构建 — 用户手动操作指南

> **这个文件是给你的（人类用户）**，不是给 Codex 的。
> 它列出了整个 Omega MFE 构建过程中，**所有需要你手动操作的步骤**。
> 每个步骤都有明确的：做什么 → 怎么做 → 如何确认成功 → 出错了怎么办。
>
> Codex 会在需要你操作时**停下来明确提示**，并指引你查看本文件对应编号的步骤。Claude Code 兼容链仅为可选备用。

---

## 准备工作（构建开始前）

### 🅰 启动 Docker Desktop

| 项目 | 说明 |
|------|------|
| **做什么** | 启动 Docker Desktop，确认鲸鱼图标变绿 |
| **怎么做** | 开始菜单 → Docker Desktop → 等待托盘图标变绿（约 30 秒） |
| **确认成功** | PowerShell 中运行 `docker ps`，输出表头（不报错即可） |
| **常见问题** | 图标一直黄色/红色 → 重启 Docker Desktop；WSL2 未安装 → 运行 `wsl --install` |

```
┌──────────────────────────────────────────┐
│  🐳 Docker Desktop 状态检查               │
│                                          │
│  托盘图标颜色：                           │
│  🟢 绿色 = 运行中，可以继续               │
│  🟡 黄色 = 启动中，等 30 秒              │
│  🔴 红色 = 出错，点图标看错误信息         │
│  ⚫ 无图标 = 未启动，从开始菜单启动       │
└──────────────────────────────────────────┘
```

### 🅱 填写 .env 文件

| 项目 | 说明 |
|------|------|
| **做什么** | 复制 `.env.example` → `.env`，按 Codex 提示逐层确认并填入 API Key |
| **怎么做** | `copy {OMEGA_HOME}\build-package\config\.env.example {OMEGA_HOME}\.env` → 用记事本编辑 |
| **至少填什么** | `POSTGRES_PASSWORD`。Codex 当前会话足以构建；独立运行时 provider 可稍后配置 |
| **确认成功** | Codex 会在构建前逐项检查，生成 active_engines.yaml 确认可用引擎 |

```
┌──────────────────────────────────────────┐
│  🔑 API 分层确认卡（功能最佳优先）         │
│                                          │
│  Codex 会逐层询问，你对每项选择：         │
│  Y = 我已有，填入 .env                   │
│  L = 稍后尝试获取（标记 deferred）        │
│  N = 确认暂时无法获取（标记降级）         │
│                                          │
│  主链 — Codex 当前会话 + OpenAI：         │
│  □ OpenAI API [PRIMARY-OPTIONAL]         │
│    获取: https://platform.openai.com/    │
│    Omega 独立运行时主 provider            │
│  □ OpenRouter / 国产 Claude Messages     │
│    [FALLBACK-OPTIONAL] 禁止原生 Anthropic │
│  □ Perplexity API [BEST-OPTIONAL]        │
│    获取: https://www.perplexity.ai/      │
│    实时搜索增强（没有不影响核心功能）     │
│  □ Brave Search API [BEST-OPTIONAL]      │
│    获取: https://brave.com/search/api/   │
│    免费搜索备选                          │
│                                          │
│  后续备用 — 国内 OpenAI-compatible：      │
│  □ DeepSeek API [OPTIONAL]               │
│    获取: https://platform.deepseek.com/  │
│    推荐配置——国内平台，成本极低           │
│  □ 通义千问 / 智谱 / Kimi / 硅基流动    │
│    [OPTIONAL-DOMESTIC] 阶段 2 预留       │
│                                          │
│  ✅ POSTGRES_PASSWORD=你的强密码(≥16位)  │
│    [REQUIRED] 任意你记得住的强密码        │
│                                          │
│  Codex 确认后生成 active_engines.yaml    │
│  记录 available/deferred/unavailable     │
└──────────────────────────────────────────┘
```

---

## 迭代 0：骨架搭建

### 0-1 确认基础环境

Codex 会打印一份环境检查报告。你只需确认每一项都显示 `[OK]`：

```
[OK] Python 3.12.x
[OK] Node.js 22.x
[OK] Git 2.x
[OK] Docker 27.x
[OK] Codex 当前会话可用；独立运行时 provider 可 deferred
```

如果有 `[MISSING]`，按提示重新安装对应软件。

---

## 迭代 1：路由与规划

> 此迭代无用户操作——Codex 自主完成代码生成和配置。

---

## 迭代 2：执行与安全

### 2-1 确认 Docker 服务启动

Codex 会执行 `docker compose up -d`。**如果这是第一次启动**，Docker 可能需要拉取镜像（PostgreSQL + Qdrant，约 500 MB），需要 2-5 分钟。

```
Codex 会显示：
  [1/4] Starting PostgreSQL... ⏳
  [2/4] Starting Qdrant... ⏳
  [3/4] Building omega-sandbox... ⏳
  [4/4] Building omega-sandbox-net... ⏳

你只需等待，不需要操作。
```

### 2-2 高风险操作确认

当 Codex 要执行以下操作时，会**暂停并请求你确认**：

| 操作 | Codex 的提示 | 你的选择 |
|------|-------------|---------|
| 删除 Docker 卷 | "即将删除 omega_postgres_data 卷，所有数据将丢失。确认？" | 首次构建选 Y；已有数据选 N |
| 修改 .env | "即将在 .env 中新增 XXX 变量" | 通常选 Y |
| git push | "即将推送到远程仓库。确认？" | 首次构建通常选 N（先本地验证） |

```
┌──────────────────────────────────────────┐
│  ⚠️ 高风险操作确认                         │
│                                          │
│  Codex 说：即将删除卷 omega_postgres_data │
│                                          │
│  ⚡ 这意味着：数据库中的全部数据将永久丢失  │
│                                          │
│  你的选择：                               │
│  [Y] 确认删除（首次构建选这个）            │
│  [N] 取消操作（已有重要数据时选这个）      │
│  [S] 跳过此步骤，继续后面的               │
│                                          │
│  输入 Y / N / S 然后回车                  │
└──────────────────────────────────────────┘
```

---

## 迭代 3：闭环验证

### 3-1 检查输出物

每个闭环完成后，Codex 会展示成果摘要：

```
✅ 闭环 1 完成：文献摄取
   → 创建了 5 个 wiki/来源/ 页面
   → 示例: wiki/来源/Empagliflozin cardiovascular outcomes.md

✅ 闭环 3 完成：数据分析
   → 生成了 3 张图表（PNG）
   → 报告: omega-workspace/outputs/clinical_analysis_report.md
```

你可以在 Obsidian 中打开对应的 `wiki/来源/` 页面查看结果。

### 3-2 Zotero 条件同步

如果你需要 Zotero 文献自动同步：

| 项目 | 说明 |
|------|------|
| **什么时候需要** | 你希望 Omega 直接从 Zotero 读取文献库 |
| **需要提供什么** | Zotero API Key + User ID |
| **获取方式** | Zotero 桌面版 → Edit → Settings → Feeds/API → Create new private key |
| **不需要时的行为** | Omega 退化为导出 BibTeX/RIS 手动处理 |

---

## 构建完成后的验证

所有迭代完成后，运行以下命令确认系统正常：

```powershell
# 1. CLI 入口
omega --version     # 应输出 omega v0.1.0-mfe
omega --help        # 应显示 5 个子命令

# 2. 服务健康
omega status        # 全部显示 healthy

# 3. 快速测试
omega task "用一句话介绍 Omega 项目" --dry-run
```

---

## 遇到问题？

| 症状 | 可能原因 | 解决方法 |
|------|---------|---------|
| `docker ps` 报错 | Docker Desktop 未启动 | 启动 Docker Desktop，等鲸鱼变绿 |
| `.env` 中的 Key 不起作用 | Key 格式错误或过期 | 去对应平台重新生成 Key |
| `omega` 命令找不到 | 虚拟环境未激活 | 运行 `.venv\Scripts\activate` |
| PostgreSQL 起不来 | 端口 5432 被占用 | 修改 docker-compose.yml 中的端口映射 |
| 构建中途 Codex 上下文丢失 | 上下文窗口限制 | Codex 会读取 BUILD_STATE.md 自动恢复 |
