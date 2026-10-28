# Omega Terminal — 统一操作窗口设计规范

> **定位**：Omega 系统的唯一用户界面入口。所有用户交互——自然语言指令、文件上传、任务监控、系统反馈、审批确认——都在这个窗口中完成。
> **设计理念**：简洁、功能全面、类 VS Code/Obsidian 的现代操作体验。零学习成本——用户只需知道一个窗口。

---

## 一、设计目标

```
┌─────────────────────────────────────────────────────────────┐
│                    Omega Terminal 设计目标                    │
│                                                             │
│  🎯 唯一入口    │  所有 Omega 功能从一个窗口可达              │
│  💬 自然语言    │  输入中文/英文指令，Omega 自动解析执行       │
│  ⌨️  键盘优先   │  所有操作有快捷键，面向效率用户              │
│  📊 实时反馈    │  任务进度、日志、输出流式展示                │
│  🖱️  拖拽上传   │  文件直接拖入窗口上传处理                   │
│  🎨 现代设计    │  暗色/亮色主题，类 VS Code 布局             │
│  🔔 通知中心    │  所有 Omega 汇报/请求/警告汇聚一处          │
│  📁 文件管理    │  内置文件浏览器，管理 vault 和工作目录       │
└─────────────────────────────────────────────────────────────┘
```

---

## 二、技术架构

```
┌──────────────────────────────────────────────────────────┐
│                   Omega Terminal 架构                     │
│                                                          │
│  ┌─────────────────────┐   ┌─────────────────────────┐  │
│  │   Frontend (Web UI) │   │  Backend (FastAPI)       │  │
│  │                     │   │                         │  │
│  │  React + Tailwind   │◄──│  /api/terminal/ws       │  │
│  │  + CodeMirror       │   │  /api/upload            │  │
│  │  + ReactFlow (DAG)  │   │  /api/task/*            │  │
│  │                     │   │  /api/notify/stream     │  │
│  └─────────────────────┘   └──────────┬──────────────┘  │
│                                       │                  │
│                              ┌────────▼──────────────┐  │
│                              │  Omega Core            │  │
│                              │  (共享 CLI 后端逻辑)    │  │
│                              └───────────────────────┘  │
└──────────────────────────────────────────────────────────┘
```

**技术选型**：

| 层 | 技术 | 理由 |
|----|------|------|
| 前端框架 | React 18 + TypeScript | 组件化、生态丰富、与 VS Code 同技术栈 |
| 样式 | Tailwind CSS | 快速构建、暗色主题内置 |
| 编辑器 | CodeMirror 6 | 代码输入/文件预览/日志高亮 |
| 流程图 | ReactFlow | DAG 可视化（任务规划展示） |
| 图表 | Recharts | 统计图表渲染 |
| 实时通信 | WebSocket | 日志流、任务进度推送 |
| 打包 | Electron 28 | 独立桌面窗口（跨平台） |
| 后端 | FastAPI（已有） | 与 Phase 10 共享，无需新增后端框架 |

**备选轻量方案**（如果 Electron 太重）：
- PWA（Progressive Web App）——浏览器打开 `http://localhost:8420` 即可
- 使用 `pywebview` —— Python 原生窗口，前端仍用 React 打包产物

---

## 三、窗口布局

```
┌──────────────────────────────────────────────────────────────────┐
│  ≡  Omega Terminal                              ─  □  ×          │
├──────────┬────────────────────────────────┬──────────────────────┤
│          │                                │                      │
│  📁 文件  │  💬 对话区                      │  📋 上下文面板       │
│  浏览器   │                                │                      │
│          │  ┌──────────────────────────┐  │  📌 当前任务         │
│  📂 vault │  │                          │  │  · task_type        │
│  ├─ wiki/ │  │  用户: 搜5篇SGLT2抑制剂   │  │  · status           │
│  │ ├─ 来源 │  │  在心衰中的最新文献        │  │  · agent            │
│  │ ├─ 概念 │  │                          │  │  · elapsed          │
│  │ └─ 实体 │  │  Omega: 🔍 正在检索       │  │                      │
│  ├─ raw/  │  │  PubMed...               │  │  📊 任务进度         │
│  └─ assets│  │  [████████░░] 60%        │  │  ▓▓▓▓▓▓▓░░░ 80%     │
│          │  │                          │  │                      │
│  📂 输出  │  │  已完成: 3/5 篇文献        │  │  ⚙️ 活跃工具         │
│  ├─ 报告  │  │  当前: Nature Medicine    │  │  · pubmed_search    │
│  ├─ 图表  │  │  IF≈58 → L3 深度处理      │  │  · zotero_import    │
│  └─ 导出  │  │                          │  │  · pdf_extract      │
│          │  └──────────────────────────┘  │                      │
│          │                                │  📜 历史记录         │
├──────────┴────────────────────────────────┴──────────────────────┤
│  > 输入指令或按 Ctrl+Shift+P 打开命令面板...                       │
├──────────────────────────────────────────────────────────────────┤
│  ✅ 就绪  │  Omega v1.0.0  │ quality_reasoning │ 任务: 3 活跃     │
└──────────────────────────────────────────────────────────────────┘
```

### 面板说明

| 区域 | 宽度 | 功能 | 可折叠 |
|------|------|------|:------:|
| **左侧栏** — 文件浏览器 | 260px | 浏览 vault 目录、拖拽文件到对话区上传、右键菜单操作 | ✅ |
| **中央** — 对话区 | 弹性 | 自然语言输入、流式输出、任务进度条、内嵌图表/DAG 图 | ❌ |
| **右侧栏** — 上下文面板 | 300px | 当前任务详情、活跃工具、历史记录、快捷操作按钮 | ✅ |
| **底部栏** — 命令输入 | 全宽 | 命令输入框 + 发送按钮 + 附件上传按钮 | ❌ |
| **状态栏** | 全宽 | 系统状态、API 引擎、活跃任务数、时钟 | ❌ |

---

## 四、核心功能清单

### 4.1 自然语言命令输入（💬 对话区）

用户在底部输入框直接输入中文/英文指令，Omega 自动解析并执行。

```
输入示例：
  "搜5篇SGLT2抑制剂在心衰中的最新文献，L3深度处理"
  "分析 D:/data/clinical.csv，做描述性统计和PCA"
  "对比 Blender 和 Manim 在科学可视化方面的能力"
  "帮我把这篇 PDF 转成深度笔记"
  "检查系统健康状态"
  "生成本周工作总结PPT"
```

**智能补全**：输入时自动补全文件路径、catalog_id、历史命令。

### 4.2 命令面板（⌨️ Ctrl+Shift+P）

类似 VS Code 的命令面板，列出所有可用操作：

```
┌────────────────────────────────────────┐
│ > 搜索命令...                          │
├────────────────────────────────────────┤
│  📚 文献检索与知识摄取                   │
│  📊 CSV 数据分析与统计报告               │
│  ⚖️  工具对比分析                        │
│  🧪 工具自主学习与注册                   │
│  📄 PDF 文献深度处理                     │
│  ✍️  学术写作与审校                      │
│  🌐 浏览器自动化                         │
│  📈 科学可视化                           │
│  🎨 PPT 生成                             │
│  🔍 知识库健康检查                       │
│  ────────────────────────               │
│  ⚙️  系统状态 / 健康检查                  │
│  📋 查看活跃任务                         │
│  📜 查看历史记录                         │
│  🔔 通知中心                             │
│  📁 上传文件                             │
│  ⏸️  暂停/取消当前任务                   │
│  🔄 重新执行上次任务                     │
└────────────────────────────────────────┘
```

### 4.3 文件上传（📁 拖拽 + 按钮）

| 方式 | 操作 | 行为 |
|------|------|------|
| 拖拽上传 | 从文件管理器拖入对话区 | 自动识别文件类型 → 提示处理方式 |
| 按钮上传 | 点击底部 📎 按钮 | 打开文件选择器 |
| 粘贴上传 | Ctrl+V 粘贴剪贴板图片/文件 | 自动保存到临时目录 |
| 文件夹 | 拖入文件夹（含多文件） | 自动识别 → 提示批量处理 |

**智能识别**：根据文件扩展名自动推荐处理方式
- `.pdf` → "是否进行 PDF 深度处理 (L3/L2/L1)？"
- `.csv`/`.xlsx` → "是否进行数据分析？"
- `.md`/`.txt` → "是否摄入为知识库页面？"
- `.pptx`/`.docx` → "是否提取内容并分析？"
- 多文件 → "是否创建 Omega 批量研究与证据综合任务？"（NotebookLM 已排除）

### 4.4 实时任务监控（📊 上下文面板）

右侧面板实时展示当前任务状态：

```
┌─ 当前任务 ──────────────────────────┐
│ 📌 文献检索与知识摄取                 │
│ catalog_id: literature_ingestion     │
│                                      │
│ 状态: ⏳ 进行中                       │
│ Agent: Researcher (economical_general) │
│ 耗时: 2m 34s                         │
│                                      │
│ 📊 进度                              │
│ ▓▓▓▓▓▓▓▓▓░░░░░░░ 65%                │
│                                      │
│ 步骤:                                │
│ ✅ PubMed 检索 (5篇, 1.2s)           │
│ ✅ 摘要提取 (5篇, 3.1s)              │
│ ⏳ Zotero 导入 (3/5, 45.2s)         │
│ ⬜ wiki/来源/ 页面创建               │
│ ⬜ 概念链接 (≥2规则)                  │
│                                      │
│ 预计剩余: ~1min                      │
│                                      │
│ [⏸️ 暂停] [⏹️ 取消] [📋 复制日志]    │
└──────────────────────────────────────┘
```

### 4.5 通知中心（🔔）

所有 Omega 的系统反馈在此汇聚：

| 类型 | 示例 | 行为 |
|------|------|------|
| ℹ️ 信息 | "任务完成：文献检索 (5篇 L3)" | 自动消失(5s) |
| ✅ 成功 | "CSV 分析报告已生成" | 点击跳转文件 |
| ⚠️ 警告 | "Provider 调用超时，已切换到下一已验证兼容 provider" | 需手动关闭 |
| ❌ 错误 | "PubMed API 返回 429，等待 60s 重试" | 需手动关闭 |
| 🔔 请求 | "发现新工具 manim 2.0，是否测试并注册？" | **需用户确认** |
| 📋 审批 | "ECP #42：升级 pandas 2.0→2.1，风险 MEDIUM" | **需用户审批** |

**通知栏位置**：右上角铃铛图标 + 未读计数徽标。

### 4.6 文件浏览器（📁 左侧栏）

```
┌─ 文件浏览器 ─────────────────────────┐
│ 📂 Omega Vault                       │
│ ├─ 📂 wiki/                          │
│ │  ├─ 📂 来源/  (413)                │
│ │  ├─ 📂 概念/  (28)                 │
│ │  ├─ 📂 实体/  (15)                 │
│ │  ├─ 📂 对比/  (3)                  │
│ │  └─ 📂 洞察/  (7)                  │
│ ├─ 📂 raw/                           │
│ │  ├─ 📂 01-articles/ (12)           │
│ │  ├─ 📂 02-papers/   (8)            │
│ │  └─ 📂 09-archive/ (523)           │
│ ├─ 📂 assets/                        │
│ └─ 📂 omega-workspace/               │
│    ├─ 📂 outputs/ (报告/图表)         │
│    └─ 📂 exports/ (导出文件)          │
│                                      │
│ [🔍 筛选] [📋 右键菜单]               │
└──────────────────────────────────────┘
```

**右键菜单**：
- 预览文件（Markdown 渲染、图片、PDF 缩略图）
- 发送到对话区（作为任务输入）
- 复制路径
- 在系统文件管理器中打开

### 4.7 键盘快捷键

| 快捷键 | 功能 |
|--------|------|
| `Ctrl+Shift+P` | 命令面板 |
| `Ctrl+Enter` | 发送当前输入 |
| `Ctrl+L` | 清空对话区 |
| `Ctrl+B` | 切换左侧栏 |
| `Ctrl+J` | 切换右侧栏 |
| `Ctrl+K` | 上传文件 |
| `Ctrl+Shift+N` | 新任务 |
| `Ctrl+Shift+C` | 取消当前任务 |
| `Ctrl+Shift+R` | 重新执行上次任务 |
| `Ctrl+Shift+H` | 查看历史记录 |
| `Ctrl+Shift+F` | 全局搜索 vault |
| `Ctrl+1/2/3` | 切换标签页 |
| `Esc` | 关闭弹窗/面板 |

---

## 五、对话区功能详解

### 5.1 消息类型

对话区支持多种消息类型，Omega 的输出不仅仅是纯文本：

```
┌──────────────────────────────────────────────────┐
│                                                   │
│  📝 Markdown 渲染                                 │
│  · 标题、列表、粗体、代码块、表格                   │
│  · 数学公式 (KaTeX)                               │
│                                                   │
│  📊 内嵌图表                                       │
│  · matplotlib/plotly 图表 PNG 内嵌                 │
│  · 统计结果表格                                    │
│                                                   │
│  🗂️  DAG 可视化                                    │
│  · 任务规划 DAG 图（ReactFlow 渲染）               │
│  · 节点可点击查看详情                              │
│                                                   │
│  📄 文件卡片                                       │
│  · 生成的文件以卡片形式展示                         │
│  · 文件名 + 类型图标 + 大小 + 预览按钮              │
│                                                   │
│  ✅/❌ 确认框                                      │
│  · 需要用户确认的操作以交互式按钮呈现               │
│  · [✓ 确认] [✗ 取消] [↩ 调整参数]                  │
│                                                   │
│  ⚠️ 风险警告                                       │
│  · 高风险操作以红色边框突出显示                     │
│  · 显示风险等级 + 影响范围 + 回滚方案               │
│                                                   │
└──────────────────────────────────────────────────┘
```

### 5.2 交互式确认

Omega 需要用户确认时，不再只是纯文本——而是交互式组件：

```
┌─────────────────────────────────────────────┐
│ 🔔 Omega 需要你的确认                         │
│                                             │
│ 即将执行操作：工具自主学习与注册               │
│                                             │
│ 发现新工具: manim-community v0.18.0          │
│ 来源: PyPI                                   │
│ 沙箱测试: ✅ 通过（omega-sandbox-net）        │
│ 离线验证: ✅ 通过（omega-sandbox）            │
│ 风险等级: LOW                                │
│                                             │
│ 将添加到: config/tools.yaml                  │
│                                             │
│ [✓ 确认注册] [✗ 拒绝] [📋 查看详情]          │
└─────────────────────────────────────────────┘
```

### 5.3 结果展示

任务完成后，结果以结构化卡片展示：

```
┌─────────────────────────────────────────────┐
│ ✅ 任务完成：文献检索与知识摄取                │
│                                             │
│ 📊 摘要                                      │
│ · 搜索: SGLT2抑制剂 + 心衰 (PubMed)          │
│ · 找到: 127 篇 → 筛选: 5 篇（IF>10, 2024+）  │
│ · 处理: 5 篇 L3 深度处理                     │
│ · 耗时: 4m 12s                              │
│                                             │
│ 📄 产出文件                                   │
│ ┌──────────────────────────────────────┐    │
│ │ 📄 wiki/来源/Empagliflozin心衰.md    │    │
│ │ 📄 wiki/来源/Dapagliflozin_DELIVER  │    │
│ │ 📄 wiki/来源/SGLT2i_meta_2024.md    │    │
│ │ ... (共5个文件)                      │    │
│ └──────────────────────────────────────┘    │
│                                             │
│ 🔗 新建概念: SGLT2抑制剂·心衰应用             │
│                                             │
│ [📂 打开文件] [🔄 重新执行] [📋 复制摘要]      │
└─────────────────────────────────────────────┘
```

---

## 六、多标签支持

类似 VS Code 的标签页系统，支持同时进行多个任务：

```
┌─ 📚 文献检索  ─┬─ 📊 数据分析  ─┬─ ⚙️ 系统状态 ─┐
│                 │                │               │
│  标签页 1       │  标签页 2      │  标签页 3     │
│  (活跃)         │  (后台完成)    │  (空闲)       │
│                 │                │               │
└─────────────────┴────────────────┴───────────────┘
```

每个标签页 = 一个独立的对话线程，有自己的上下文和历史。

---

## 七、主题系统

### 内置主题

| 主题 | 描述 | 适用场景 |
|------|------|---------|
| **Omega Dark** | 默认暗色主题 | 日常使用 |
| **Omega Light** | 亮色主题 | 白天 / 演示 |
| **High Contrast** | 高对比度 | 可访问性需求 |

### 自定义

用户可通过 `~/.omega/terminal/theme.json` 自定义配色。

---

## 八、统一事件协议

> **Schema 定义**：`schemas/terminal_event.schema.json`（JSON Schema 2020-12）

Omega Core 与 Omega Terminal 之间的所有双向通信使用统一事件协议。共 12 种事件类型，确保"任何反馈都能进窗口"：

| 事件类型 | 方向 | 触发时机 | 终端组件 |
|---------|------|---------|---------|
| `task_progress` | Core→Terminal | 任务进度更新 | `TaskMonitor` |
| `log` | Core→Terminal | 日志输出（含流式） | `ChatArea` |
| `notification` | Core→Terminal | 系统通知/警告/错误 | `NotificationCenter` |
| `confirm_request` | Core→Terminal | 需要用户确认 | `ConfirmDialog` |
| `file_result` | Core→Terminal | 任务完成，产出文件 | `FileCard` |
| `risk_warning` | Core→Terminal | 高风险操作前 | `RiskWarning` |
| `approval_request` | Core→Terminal | ECP/工具注册/知识写入审批 | `ConfirmDialog` |
| `upload_result` | Core→Terminal | 文件上传完成 | `ChatArea` |
| `task_lifecycle` | Core→Terminal | 任务创建/开始/完成/失败 | `ContextPanel` |
| `system_health` | Core→Terminal | 服务健康状态变更 | `StatusBar` |
| `dag_visualization` | Core→Terminal | 任务规划 DAG 生成 | `DAGViewer` |
| `user_command` | Terminal→Core | 用户输入命令/上传文件 | Omega Core |

所有事件遵循统一信封格式：
```json
{
  "event_id": "uuid",
  "event_type": "task_progress",
  "timestamp": "2026-05-17T12:00:00Z",
  "task_id": "uuid-or-null",
  "session_id": "uuid",
  "payload": { /* 类型相关 */ }
}
```

详见 `schemas/terminal_event.schema.json`。

---

## 九、文件上传安全规则

> **原则**：所有用户上传文件进入隔离区（quarantine），通过多层安全检查后才能被 Omega 任务使用。**永不直接写入正式 wiki 或系统目录。**
> **安全等级**：此模块设计遵循 OWASP 文件上传防护最佳实践，覆盖大小/类型/路径/内容/压缩/溯源六个维度。

### 9.1 安全规则清单（9 层防护）

| # | 规则 | 说明 | 违反时行为 |
|---|------|------|-----------|
| 1 | **大小限制** | 单文件 ≤ 100MB，单次会话累计 ≤ 500MB，zip 解压后 ≤ 1GB | 拒绝上传，提示用户 |
| 2 | **路径隔离** | 上传文件存入 `omega-workspace/uploads/quarantine/{uuid}/`，不直接放入 vault。隔离目录权限 700（仅 Omega 进程可读） | 强制隔离 |
| 3 | **类型白名单（扩展名）** | 允许：`.pdf` `.csv` `.xlsx` `.xls` `.pptx` `.docx` `.md` `.txt` `.png` `.jpg` `.jpeg` `.gif` `.webp` `.zip` `.json` `.yaml` `.yml` `.py` `.r` `.ipynb` `.html` | 拒绝上传 |
| 4 | **禁止类型（可执行/脚本）** | 禁止：`.exe` `.bat` `.ps1` `.sh` `.dll` `.so` `.msi` `.scr` `.vbs` `.js` `.vbe` `.wsf` `.wsh` `.htm`（含 ActiveX） `.app` `.command` `.cpl` | 拒绝上传 + 安全警告 |
| 5 | **MIME 类型双重验证** | 用 `python-magic` 检测文件真实 MIME 类型，与扩展名交叉验证。不匹配 → 拒绝（防止扩展名伪造，如 `.pdf` 实为 `.exe`） | 拒绝上传 + 安全警告 |
| 6 | **Zip Bomb 防护** | 上传 `.zip` 时检测：① 压缩率 > 100:1（如 1MB→1GB）→ 拒绝；② 嵌套深度 > 3 层 → 拒绝；③ 内含禁止类型文件 → 拒绝；④ 总解压后 > 1GB → 拒绝 | 拒绝上传 + 安全警告 |
| 7 | **路径穿越防护** | 上传 `.zip` 时检测：① 文件名含 `../`、`..\`、绝对路径（`/etc/`、`C:\`）→ 拒绝；② 解压时使用 `os.path.realpath()` 校验最终路径仍在隔离区内 | 拒绝上传 + 安全警告 |
| 8 | **Hash 记录与去重** | 每文件计算 SHA-256，记录到 `uploads_manifest.json`。相同 hash 的文件 7 天内自动去重（返回已有 file_id） | 自动执行 |
| 9 | **来源取证** | 记录：上传时间（UTC）、终端会话 ID、用户是否拖拽/粘贴/按钮上传、原始文件名、文件大小、MIME 类型、SHA-256、隔离路径 | 自动执行 |

### 9.2 扩展安全机制

#### 9.2.1 病毒扫描（可选增强）

```bash
# Windows: 调用 Microsoft Defender 命令行扫描
"C:\Program Files\Windows Defender\MpCmdRun.exe" -Scan -ScanType 3 -File "<隔离区文件路径>"
```

- 扫描超时 30s（大文件可能更久）
- 发现威胁 → `status: quarantined` + `security.threat_detected: true` + 通知用户
- Defender 不可用 → 跳过扫描但记录警告日志（不阻断上传，依赖其他 8 层防护）

#### 9.2.2 内容安全检查

文件从隔离区释放到正式位置前，通过 `upload_api.py` 的 `ContentInspector` 执行：

| 检查项 | 方法 | 不通过行为 |
|--------|------|-----------|
| **PDF 恶意链接** | 提取 PDF 内嵌 URL，检查是否为已知恶意域名 | 标记 `security.warnings`，用户确认后放行 |
| **Office 宏检测** | 检测 `.xlsx`/`.pptx`/`.docx` 是否内嵌 VBA 宏 | 宏存在 → 拒绝（提取纯数据版本可放行） |
| **CSV 注入防护** | 检测 CSV 首字符是否为 `=` `+` `-` `@`（公式注入） | 自动转义为 `'=` 等安全形式 |
| **图片像素炸弹** | 检测 PNG/JPEG 分辨率是否 > 10000×10000（像素炸弹） | 拒绝上传 |
| **ZIP 内容扫描** | `.zip` 内每个文件的 MIME 类型逐一检测 | 任一禁止类型 → 拒绝整个 zip |

#### 9.2.3 文件类型白名单详解

```
┌──────────────────────────────────────────────────────────────┐
│ 允许类型（19 种扩展名 × MIME 验证）                            │
│                                                              │
│ ▸ 文档类（7）:  .pdf .md .txt .json .yaml .yml .html          │
│ ▸ 表格类（2）:  .csv .xlsx .xls                               │
│ ▸ 演示类（1）:  .pptx                                         │
│ ▸ 文字类（1）:  .docx                                         │
│ ▸ 图片类（5）:  .png .jpg .jpeg .gif .webp                   │
│ ▸ 代码类（3）:  .py .r .ipynb                                │
│ ▸ 压缩类（1）:  .zip（解压后内容逐文件检查）                    │
│                                                              │
│ 禁止类型（15 种可执行/脚本/二进制扩展名）:                      │
│ .exe .bat .ps1 .sh .dll .so .msi .scr .vbs .js .vbe          │
│ .wsf .wsh .app .command .cpl .htm(含ActiveX)                  │
└──────────────────────────────────────────────────────────────┘
```

### 9.3 文件生命周期（增强）

```
用户拖拽/粘贴/按钮上传文件
  │
  ▼
┌─ 第 1 层：大小检查 ──────────────────────┐
│ 单文件 ≤ 100MB / 累计 ≤ 500MB            │
│ 不通过 → ❌ 拒绝（终端通知）              │
└──────────────────────────────────────────┘
  │ ✅
  ▼
┌─ 第 2 层：扩展名白名单检查 ──────────────┐
│ 扩展名在白名单中？                        │
│ 在禁止名单中 → ❌ 拒绝 + 安全警告         │
│ 不在任何名单 → ❌ 拒绝（未知类型）        │
└──────────────────────────────────────────┘
  │ ✅
  ▼
┌─ 第 3 层：MIME 类型验证 ─────────────────┐
│ python-magic 检测真实类型 vs 扩展名       │
│ 不匹配 → ❌ 拒绝 + 安全警告（防伪造）     │
└──────────────────────────────────────────┘
  │ ✅
  ▼
┌─ 第 4 层：隔离区存储 ────────────────────┐
│ omega-workspace/uploads/quarantine/{uuid}/│
│ chmod 700（仅 Omega 进程可读）            │
│ SHA-256 hash + 来源记录                  │
└──────────────────────────────────────────┘
  │ ✅
  ├── 是 .zip → 第 4A 层：Zip 安全解包
  │   ├── 压缩率检查（<100:1）
  │   ├── 嵌套深度检查（≤3 层）
  │   ├── 路径穿越检查（无 ../ 或绝对路径）
  │   ├── 内容类型检查（逐文件 MIME 验证）
  │   └── 解压到隔离区子目录
  │
  ▼
┌─ 第 5 层：内容安全检查（ContentInspector）┐
│ PDF 恶意链接 / Office 宏 / CSV 注入       │
│ 图片像素炸弹 / ZIP 内容逐文件检查          │
│ 不通过 → ❌ 拒绝或标记警告                │
└──────────────────────────────────────────┘
  │ ✅
  ▼
┌─ 第 6 层：病毒扫描（可选） ──────────────┐
│ Windows Defender MpCmdRun.exe            │
│ 超时 30s / 不可用 → 跳过（不阻断）        │
│ 发现威胁 → ❌ 隔离 + 通知                │
└──────────────────────────────────────────┘
  │ ✅
  ▼
上传完成 → 返回 upload_result 事件
  │ · file_id + hash_sha256 + detected_type
  │ · suggestions（基于文件类型的智能处理建议）
  │ · security: { passed: true, checks: [...], warnings: [...] }
  │
  ▼
用户确认处理方式 → Omega 任务读取隔离区文件
  │
  ▼
任务完成 → 第 7 层：写入审核
  │ · 产出来源可溯源
  │ · 内容一致性检查
  │ · 用户确认
  ▼
产出写入正式目录（wiki/ 或 omega-workspace/outputs/）
  │
  ▼
隔离区文件保留 7 天 → 自动清理（cron 每日凌晨 3:00 执行）
```

### 9.4 知识写入保护

即使任务产生的输出要写入 `wiki/`，也必须经过知识防污染守卫（Phase 11.5）：
- AI 生成内容 → 候审区（`omega-workspace/staging/`）
- 6 项自动检查（来源溯源/内容一致性/引用准确性/格式完整性/无幻觉标记/冲突检测）
- 检查通过 → 提示用户确认 → 写入 wiki/

**上传文件本身永不直接进入 wiki/ 来源页**。必须先经过 Omega 任务处理（ingest/analyze/process），产出经审核后才入库。

---

## 十、任务回放功能

> **设计目标**：任何已完成/失败/取消的任务都能完整回放——输入、模型、工具、DAG、产物和溯源链。用于审计、调试、复现和学习。

### 10.1 回放数据记录

每次任务执行时，Omega Core 将以下快照数据写入 `omega-runtime/replays/{task_id}/`：

```
omega-runtime/replays/{task_id}/
├── replay_manifest.json     # 回放索引
├── input.json               # 用户原始输入（文本/文件引用/上下文）
├── dag_snapshot.json        # 任务 DAG（节点+边+每步耗时+工具/Agent选择）
├── tool_calls.jsonl         # 每次工具调用的完整请求/响应（一行一条）
├── model_calls.jsonl        # 每次 LLM API 调用的 prompt/completion/tokens
├── env_snapshot.yaml        # 环境快照（活跃引擎/工具版本/Python & npm 包列表）
├── artifacts/               # 产物副本（报告/图表/文件链接→原文件路径）
├── provenance.yaml          # 溯源链（每步输入→处理→输出 + 模型签名）
└── terminal_events.jsonl    # 此任务相关的全部 terminal_event（时间线重放用）
```

**记录策略**：
- **MFE-Alpha 阶段**：仅记录 `replay_manifest.json` + `dag_snapshot.json`（最小开销）
- **Full-Core 阶段**：全部 7 项记录（完整审计能力）
- 历史回放数据保留 90 天，之后自动归档到 `omega-runtime/replays/archive/`

### 10.2 回放触发方式

| 触发方式 | 操作 | 行为 |
|---------|------|------|
| **终端命令面板** | `Ctrl+Shift+R` → 选择历史任务 | 展示任务回放选择器 |
| **对话区指令** | "回放上次任务" / "回放 task_id=xxx" | 直接回放指定任务 |
| **文件结果卡片** | 结果卡片上的 🔄 按钮 | 回放该结果对应的任务 |
| **CLI 命令** | `omega replay <task_id>` | 终端中逐步回放 |
| **最近任务列表** | 右键上下文面板历史记录 → "回放此任务" | 视觉化回放 |

### 10.3 回放模式

```
┌──────────────────────────────────────────────────────────┐
│ 🔄 任务回放：literature_ingestion (task_id: abc-123)      │
│                                                          │
│ 回放模式：                                                │
│                                                          │
│ ▸ 📜 逐步回放 — 逐步展示每步的输入/输出/决策（可暂停）     │
│ ▸ ⏩ 快速回放 — 跳过细节，仅展示 DAG 节点通过/失败状态    │
│ ▸ 🔬 差异回放 — 用新引擎/新工具重新执行，对比产物差异     │
│ ▸ 📊 性能分析 — 展示每步耗时/Token 消耗/成本（无实际执行） │
│ ▸ 🎓 学习模式 — 解释每步为什么选择这个工具/Agent/路径     │
│                                                          │
│ 选择回放模式后，终端对话区展示回放时间线：                  │
│                                                          │
│ [14:30:01] 📥 用户输入: "搜5篇SGLT2抑制剂文献"             │
│ [14:30:02] 🧠 classify_task() → TaskType.LITERATURE       │
│ [14:30:03] 🔀 Router: pubmed_search (score: 0.94)         │
│ [14:30:04] 🤖 Agent: Researcher (economical_general)     │
│ [14:30:05] 🔗 PubMed: 查询 "SGLT2 inhibitor" → 23 结果    │
│ [14:30:06] 📊 筛选: IF≥6, 近2年 → 5 篇                    │
│ [14:30:12] 📥 Zotero 导入: 5/5 ✅                         │
│ [14:30:45] 📝 wiki/来源/ 页面创建: 5/5 ✅                  │
│ [14:31:02] 🔗 概念链接: ≥2规则触发 2 个新概念              │
│ [14:31:10] ✅ 任务完成 (耗时: 69s, 成本: $0.12)            │
│                                                          │
│ [⏸️ 暂停] [⏩ 快进] [📋 导出报告] [🔬 创建差异回放]       │
└──────────────────────────────────────────────────────────┘
```

### 10.4 回放事件类型（terminal_event）

新增 `task_replay` 事件——当用户触发回放时，终端向 Core 发送回放指令；Core 逐步推送回放帧。

详见 `schemas/terminal_event.schema.json` 中的 `TaskReplay` 定义。

---

## 十一、命令面板一等功能

> **设计原则**：Omega Terminal 的命令面板（`Ctrl+Shift+P`）不仅仅是系统内置命令的列表，而是 Omega 全部能力的统一入口。以下四个高级功能作为命令面板的**一等公民**——与文献检索、数据分析等核心闭环平级排列。

### 11.1 命令面板完整布局

```
┌──────────────────────────────────────────────┐
│ > 搜索命令或输入自然语言...                    │
├──────────────────────────────────────────────┤
│ ── 核心闭环 ──────────────────────────────── │
│  📚 文献检索与知识摄取    literature_ingestion  │
│  📄 PDF 文献深度处理       pdf_deep_processing  │
│  📊 CSV 数据分析           csv_analysis         │
│  ✍️  学术写作与审校        academic_writing     │
│  ⚖️  工具对比分析          tool_comparison      │
│  🧪 工具自主学习           tool_gap_learning    │
│  🌐 浏览器自动化           browser_prefill      │
│  📈 科学可视化             ...                  │
│  🎨 PPT 生成               ...                  │
│  🔍 知识库健康检查          knowledge_base_health│
│ ── 高级功能（一等公民）────────────────────── │
│  📱 微信公众号候审导入      wechat_draft_import  │
│  🐙 GitHub 仓库推荐        github_repo_radar    │
│  🎬 ComfyUI 图片/视频生成  comfyui_generate     │
│  📑 PDF/PPT 智能嵌入       document_embed       │
│ ── 系统操作 ──────────────────────────────── │
│  ⚙️  系统健康检查           system_health        │
│  📋 查看活跃任务           ...                  │
│  🔄 任务回放               task_replay          │
│  📁 上传文件               ...                  │
│  ...                                            │
└──────────────────────────────────────────────┘
```

### 11.2 微信公众号候审导入 (`wechat_draft_import`)

将微信公众号草稿箱中的文章预览链接导入 Omega 进行处理。

**触发方式**：
- 命令面板选择 `📱 微信公众号候审导入`
- 对话区输入 "导入微信公众号草稿"
- 拖拽公众号文章截图到对话区

**工作流**：
```
用户在微信公众号后台复制"预览链接"
  │
  ▼
粘贴到 Omega Terminal 或命令面板
  │
  ▼
Omega 通过 Playwright 访问预览链接
  │ 浏览器自动化：提取文章标题/正文/图片/排版
  │ 注意：不执行任何 Submit/发布操作
  ▼
内容提取 & 格式转换（WeChat HTML → Markdown）
  │
  ▼
┌─ 处理选项 ───────────────────────────────┐
│ A) 知识摄取 — 按 /ingest 流程入库        │
│ B) 学术审校 — 检查引文/数据/逻辑         │
│ C) 排版优化 — 建议标题/段落/配图改进     │
│ D) 多平台适配 — 转为知乎/博客园等格式    │
│ E) 仅预览 — 在终端 Markdown 渲染预览     │
└──────────────────────────────────────────┘
  │
  ▼
用户选择后 → 产出写入 omega-workspace/outputs/
```

**安全边界**（遵循 DEPLOYMENT_CONTRACT.md）：
- ✅ 可：提取内容、Markdown 转换、预览渲染、本地存储
- ❌ 不可：自动 Submit 发布、修改微信公众号后台任何设置
- ⚠️ 首次使用需用户确认浏览器已登录微信公众平台

### 11.3 GitHub 仓库推荐 (`github_repo_radar`)

基于用户当前任务/知识库内容，智能推荐相关 GitHub 仓库。

**触发方式**：
- 命令面板选择 `🐙 GitHub 仓库推荐`
- 对话区输入 "推荐一些XXX相关的开源工具"
- 当工具自主学习闭环检测到能力缺口时自动触发

**工作流**：
```
触发条件（任一）：
  · 用户主动请求
  · tool_gap_learning 检测到能力缺口
  · 科学可视化任务缺少特定渲染库
  │
  ▼
Omega 提取上下文关键词
  │ 从：当前任务描述 / wiki/概念/ 相关页面 / 最近5篇文献关键词
  │
  ▼
GitHub API 搜索（按 stars/updated/license 排序）
  │ · 搜索 repo: topic + language + sort
  │ · 排除：archived / fork / <10 stars（质量过滤）
  │
  ▼
┌─ 推荐结果卡片 ───────────────────────────┐
│ 🐙 manimcommunity/manim                  │
│    ⭐ 28k | Python | MIT License          │
│    数学动画引擎——与你的科学可视化任务匹配  │
│    匹配原因：你的任务涉及数学公式动画       │
│                                           │
│ 🐙 3b1b/manim                            │
│    ⭐ 65k | Python | MIT License          │
│    3Blue1Brown 的动画引擎（manim 原始仓库）│
│                                           │
│ 🐙 holoviz/holoviews                      │
│    ⭐ 2.8k | Python | BSD License          │
│    高级数据可视化——替代 matplotlib 复杂图表 │
│                                           │
│ [🔬 沙箱测试] [⭐ Star] [📋 加入工具注册表]│
│ [📎 复制 URL] [🔗 创建任务卡]              │
└──────────────────────────────────────────┘
```

**智能匹配维度**：
| 维度 | 权重 | 说明 |
|------|:----:|------|
| 关键词匹配 | 30% | 仓库 topic/tags vs 用户任务描述 |
| 知识库上下文 | 25% | wiki/概念/ 页面中讨论的工具/方法 |
| 生态兼容性 | 20% | 是否与现有 Omega 工具链兼容（Python/Node.js） |
| 活跃度 | 15% | 最近 commit 时间 + issue 响应速度 |
| 质量信号 | 10% | stars/forks/contributors/license/CII best practices |

### 11.4 ComfyUI 图片/视频生成 (`comfyui_generate`)

通过 ComfyUI API 生成科学插图、示意图、动画帧。

**前置条件**：
- ComfyUI 已安装并运行（`omega setup comfyui` 或在外部启动）
- 用户明确同意此功能（首次使用时确认）

**触发方式**：
- 命令面板选择 `🎬 ComfyUI 图片/视频生成`
- 对话区输入 "生成XXX的科学示意图"
- 科学可视化闭环的 `manim` 路线中作为备选帧生成器

**工作流**：
```
用户输入生成需求
  │ "生成 SGLT2 抑制剂作用机制示意图，白色背景，学术期刊风格"
  │
  ▼
Omega 分析需求 → 选择最佳路线
  │
  ├─ 简单图表/示意图 → ComfyUI（SDXL/SD3 workfow）
  ├─ 数学动画 → manim（科学可视化闭环）
  ├─ 3D 分子结构 → PyMOL/Blender（科学可视化闭环）
  └─ 数据图表 → matplotlib/plotly（csv_analysis 闭环）
  │
  ▼
[ComfyUI 路线]
  │
  ├── Omega 构建 ComfyUI workflow JSON
  │   · Positive prompt: 从文献摘要+用户需求自动生成
  │   · Negative prompt: 文字/水印/低质量/解剖错误
  │   · Model: 默认 SDXL（用户可配置）
  │   · Resolution: 1024×1024（期刊投稿 300dpi 标准）
  │
  ├── POST http://localhost:8188/prompt
  │   · 返回 prompt_id
  │
  ├── WebSocket 监听生成进度
  │   · task_progress 事件推送到终端（生成中/采样/VAE解码）
  │
  ▼
生成完成 → 图片保存到 omega-workspace/outputs/images/
  │
  ▼
┌─ 结果卡片 ───────────────────────────────┐
│ 🎬 SGLT2 抑制剂作用机制示意图              │
│                                            │
│ [图片预览]                                  │
│                                            │
│ 模型: SDXL | 分辨率: 1024×1024 | 耗时: 12s │
│                                            │
│ [📋 复制] [💾 下载] [📝 嵌入PPT]           │
│ [🔄 重新生成] [🎚️ 调整参数]                │
└──────────────────────────────────────────┘
```

**安全边界**：
- ComfyUI 仅本地运行（`localhost:8188`），不访问外部 API
- 用户首次使用时显示 ComfyUI 安装/启动指南
- 图片自动添加溯源水印（Phase 11.3）— `generated_by: Omega-ComfyUI | model: SDXL | date: ...`

### 11.5 PDF/PPT 智能嵌入 (`document_embed`)

将生成的图表、分析结果、科学插图自动嵌入到 PDF 报告或 PPT 演示文稿中。

**触发方式**：
- 命令面板选择 `📑 PDF/PPT 智能嵌入`
- 对话区输入 "把这次分析的图表嵌入之前的 PPT"
- 任务完成后自动提示"是否将结果嵌入现有文档？"

**支持的嵌入操作**：

| 嵌入类型 | 源格式 | 目标格式 | 实现方式 |
|---------|--------|---------|---------|
| 图表→PPT | PNG/SVG | .pptx | `python-pptx`：定位占位符→替换图片→调整尺寸 |
| 图表→PDF | PNG/SVG | .pdf | `reportlab`/`pikepdf`：在指定页面坐标插入图片 |
| 报告→笔记 | Markdown | .md (wiki) | 提取结构化内容→`![[chart.png]]` 嵌入 |
| 数据→表格 | CSV/JSON | .pptx/.pdf | 读取数据→创建表格→设置样式→插入 |
| 多图→画廊页 | PNG[] | .pptx/.pdf | 网格布局→等距排列→自动标注 |

**智能定位**：
```
用户在 PPT 中标记占位符：
  · 在幻灯片备注中写 {{omega:chart_1}} → Omega 自动替换为图表 1
  · 在幻灯片备注中写 {{omega:table_summary}} → Omega 自动替换为汇总表

用户在 PDF 中标记区域：
  · PDF 注释 "INSERT_CHART_HERE" → Omega 在该位置插入图表
```

---

## 十二、高风险动作强制 terminal_event 规则

> **原则**：任何被 DEPLOYMENT_CONTRACT.md 列为 `require_confirmation` 或 `never_auto` 的操作，Omega Core **必须**先发送 `risk_warning` 或 `approval_request` 事件到终端，**在用户明确确认之前绝对不能执行**。此规则不可被任何代码路径绕过。

### 12.1 强制事件映射

| 风险动作 | 事件类型 | 终端展示 | 用户操作 |
|---------|---------|---------|---------|
| ECP 审批（HIGH/CRITICAL） | `approval_request` | 🔴 审批对话框 + 红色边框 | 审批/拒绝/要求修改 |
| 新工具注册 | `approval_request` | 🟠 工具注册审批卡 | 批准/沙箱测试/拒绝 |
| AI 内容写入 wiki/ | `approval_request` | 🟡 知识写入审批卡（含 6 项检查结果） | 批准/修改/拒绝 |
| 系统配置变更 | `risk_warning` | 🔴 风险警告（含影响范围+回滚方案） | 确认/取消 |
| Docker 卷删除 | `risk_warning` | 🔴 数据不可恢复警告 | 确认/取消 |
| 外部发布/投稿 | `risk_warning` | 🔴 红线警告（媒介伦理） | 确认（用户手动操作） |
| API Key 缺失 | `confirm_request` | 🟡 提示获取 URL + 输入框 | 输入 Key / 跳过 |
| 大模型调用超时 | `notification` | 🟠 降级通知 | 自动降级 + 通知 |
| 沙箱异常退出 | `risk_warning` | 🟠 风险提示 + 日志 | 查看日志 / 重试 / 取消 |
| 预算超限 | `risk_warning` | 🟡 成本警告 + 本会话累计 | 继续 / 降级引擎 / 停止 |
| 文件上传安全拒绝 | `notification` | 🔴 安全警告（含原因） | 理解 / 选择其他文件 |
| Omega 自身升级 | `approval_request` | 🟠 升级审批（含变更/风险/回滚） | 审批/推迟 |

### 12.2 实现约束

```python
# 所有高风险操作的唯一入口——Omega Core 中的 safety_enforcer
# 伪代码（示意 Omega Terminal 集成后的执行逻辑）

class SafetyEnforcer:
    """
    每个高风险操作必须通过此守卫。
    在 terminal_event 发出并收到用户确认之前，操作被阻塞。
    """
    
    HIGH_RISK_ACTIONS = {
        "ecp_approve":       {"event": "approval_request", "blocking": True},
        "tool_register":     {"event": "approval_request", "blocking": True},
        "knowledge_write":   {"event": "approval_request", "blocking": True},
        "system_config":     {"event": "risk_warning",      "blocking": True},
        "docker_volume_rm":  {"event": "risk_warning",      "blocking": True},
        "external_publish":  {"event": "risk_warning",      "blocking": True},
        "budget_exceeded":   {"event": "risk_warning",      "blocking": True},
        "sandbox_crash":     {"event": "risk_warning",      "blocking": False},
        "api_degraded":      {"event": "notification",       "blocking": False},
    }
    
    def guard(self, action: str, context: dict) -> bool:
        """
        发送 terminal_event → 等待用户响应 → 返回是否允许执行。
        如果 Omega Terminal 未运行（headless 模式），回退到 CLI 确认。
        """
        if not self.terminal_available:
            return self._fallback_cli_confirm(action, context)
        
        event = self._build_event(action, context)
        self.ws.send(event)  # WebSocket → Terminal
        
        # 阻塞等待用户确认（超时 = 永不自动确认）
        response = self.ws.wait_for_response(
            request_id=event.payload.request_id,
            timeout=0  # 永不超时自动确认
        )
        return response.approved
```

### 12.3 用户永远不会错过确认

| 机制 | 说明 |
|------|------|
| **通知中心徽标** | 未处理的高风险确认请求 → 通知图标持续显示红色徽标 |
| **状态栏警告** | 状态栏显示 "⚠️ 1 个待确认操作" 并闪烁 |
| **对话区置顶** | `approval_request` 和 `risk_warning` 在对话区以置顶卡片展示，不被后续消息刷走 |
| **系统通知** | Electron 打包版本 → Windows 原生通知（Toast Notification） |
| **超时不自动** | 高风险确认**永不自动超时批准**（与低风险 info 通知的 5s 自动消失不同） |
| **会话恢复** | Omega Terminal 重启后自动拉取未处理的确认请求列表（从 `omega-runtime/pending_confirmations.json` 恢复） |

---

## 十三、实施计划（Phase 10 扩展）

> **注意**：Omega Terminal 分两层部署。**Phase 1.5（Terminal Lite）** 在 MFE 构建后立即提供基础窗口；**Phase 10（Terminal Full）** 在升级末期实现完整的 VS Code 风格工作台。

### 当前 Phase 10 范围（升级前）

| 文件 | 操作 | 说明 |
|------|------|------|
| `app/web/__init__.py` | 新建 | Web 后端包 |
| `app/web/app.py` | 新建 | FastAPI 基础 |
| `app/web/templates/dashboard.html` | 新建 | 简单 HTML |
| `app/service.py` | 新建 | 后台服务 |
| `app/notify.py` | 新建 | Obsidian 通知 |
| `app/main.py` | 修改 | + web 命令 |

### 扩展后 Phase 10 范围

```
Phase 10: Omega Terminal — 统一操作窗口

├── 10.1 后端扩展 (app/web/)
│   ├── app/web/app.py           — FastAPI + WebSocket + 文件上传
│   ├── app/web/ws.py            — WebSocket 管理器（实时推送）
│   └── app/web/api/
│       ├── task_api.py          — 任务提交/查询/取消
│       ├── upload_api.py        — 文件上传/识别
│       ├── notify_api.py        — 通知推送/已读
│       └── vault_api.py         — 文件浏览/搜索
│
├── 10.2 前端 (app/web/terminal/)
│   ├── index.html               — 入口 HTML
│   ├── main.tsx                 — React 入口
│   ├── App.tsx                  — 根组件（布局管理）
│   ├── components/
│   │   ├── CommandInput.tsx     — 底部命令输入栏
│   │   ├── ChatArea.tsx         — 对话区（消息列表）
│   │   ├── MessageBubble.tsx    — 单条消息渲染
│   │   ├── FileBrowser.tsx      — 左侧文件浏览器
│   │   ├── ContextPanel.tsx     — 右侧上下文面板
│   │   ├── TaskMonitor.tsx      — 任务进度监控
│   │   ├── CommandPalette.tsx   — Ctrl+Shift+P 命令面板
│   │   ├── NotificationCenter   — 通知中心
│   │   ├── StatusBar.tsx        — 底部状态栏
│   │   ├── ConfirmDialog.tsx    — 交互式确认框
│   │   ├── FileCard.tsx         — 文件结果卡片
│   │   ├── DAGViewer.tsx        — DAG 流程图渲染
│   │   └── ChartRenderer.tsx    — 图表内嵌渲染
│   ├── hooks/
│   │   ├── useWebSocket.ts      — WebSocket 连接
│   │   ├── useTasks.ts          — 任务状态管理
│   │   └── useNotifications.ts  — 通知管理
│   ├── styles/
│   │   └── tailwind.css         — Tailwind + 主题变量
│   └── package.json             — 前端依赖
│
├── 10.3 桌面打包 (可选)
│   ├── electron/
│   │   ├── main.js              — Electron 主进程
│   │   └── preload.js           — 预加载脚本
│   └── 或 pywebview 方案
│
├── 10.4 后台服务扩展
│   ├── app/service.py           — 扩展：任务队列 + 定时任务
│   └── app/notify.py            — 扩展：WebSocket 推送 + vault 写入
│
└── 10.5 验证
    ├── omega web --port 8420    — 启动完整终端
    ├── omega web --electron     — 启动独立桌面窗口
    ├── 功能验证清单（14 项）     — 见下方
    └── tests/test_terminal.py   — 自动化测试
```

**文件统计**：~28 个新文件，~3 个修改文件。

### 10.6 功能验证清单

- [ ] 浏览器打开 `http://localhost:8420` 显示完整终端界面
- [ ] 自然语言输入"搜3篇糖尿病文献"正常执行
- [ ] 命令面板 `Ctrl+Shift+P` 列出所有闭环命令
- [ ] 拖拽 PDF 文件到对话区 → 自动识别并提示处理
- [ ] 点击 📎 按钮上传 CSV → 自动识别并提示数据分析
- [ ] 实时任务进度条在右侧面板正确更新
- [ ] WebSocket 推送日志实时显示在对话区
- [ ] 任务完成后结构化卡片正常展示
- [ ] 通知中心收到 Omega 的确认请求并正确显示
- [ ] 文件浏览器正确展示 vault 目录结构
- [ ] 右键菜单"发送到对话区"正常工作
- [ ] `Ctrl+Enter` 发送命令、`Ctrl+L` 清空对话区
- [ ] 暗色/亮色主题切换正常
- [ ] 多标签页切换不丢失对话上下文

---

## 十四、与现有 Omega 组件的集成

```
Omega Terminal (用户界面)
    │
    ├── 自然语言输入
    │   └── Omega CLI (omega task "...")
    │       ├── classify_task()  → TaskType
    │       ├── DynamicScorer    → 最佳工具
    │       ├── AgentDispatcher  → 最佳 Agent
    │       └── DynamicTaskPlanner → DAG
    │
    ├── 文件上传
    │   └── app/web/api/upload_api.py
    │       ├── 类型识别 (PDF/CSV/PPTX/...)
    │       ├── 存入 omega-workspace/uploads/
    │       └── 触发生命周期 (ingest/analyze/...)
    │
    ├── 实时推送 (WebSocket)
    │   └── app/web/ws.py
    │       ├── 任务进度 → TaskMonitor
    │       ├── 日志流 → ChatArea
    │       └── 通知 → NotificationCenter
    │
    ├── 确认/审批
    │   └── ConfirmDialog
    │       ├── ECP 审批 → evolution_engine
    │       ├── 高风险操作 → safety_enforcer
    │       └── 知识写入 → knowledge_quarantine
    │
    └── 状态栏
        └── StatusBar
            ├── omega status     → 系统健康
            ├── active_engines   → API 状态
            └── task_count       → 活跃任务数
```

---

## 十五、实施优先级

| 阶段 | 内容 | 文件数 | 优先级 |
|------|------|--------|:------:|
| **10A** | 后端 WebSocket + 任务 API | 5 新 | 🔴 最高 |
| **10B** | React 基础布局 + 对话区 | 8 新 | 🔴 最高 |
| **10C** | 命令面板 + 文件浏览器 + 快捷键 | 5 新 | 🟠 高 |
| **10D** | 任务监控 + 通知中心 | 4 新 | 🟠 高 |
| **10E** | 文件上传 + 拖拽 + 智能识别 | 3 新 | 🟡 中 |
| **10F** | 图表渲染 + DAG 可视化 | 3 新 | 🟡 中 |
| **10G** | Electron 打包 + 主题系统 | 3 新 | 🟢 低 |
| **10H** | 自动化测试 | 1 新 | 🟡 中 |

**总计**：~28 个新文件，~3 个修改文件。

---

## 十六、备选方案：轻量 TUI

如果第一阶段想快速交付（不等完整前端开发），可以用 Python Textual 框架做一个 TUI 版本：

```bash
omega tui    # 启动终端 UI
```

**优点**：纯 Python、零前端依赖、启动快、与 CLI 完美共用代码。
**缺点**：终端渲染限制、不支持拖拽、不支持图表/DAG 内嵌。

TUI 版本适合 Phase 10 第一阶段快速验证，Web Terminal 是最终目标形态。

---

*文档版本: v2.0 — 2026-05-18*
*变更 v2.0：**Codex 第 10 轮反馈优化** — ①§9 文件上传安全规则扩展为 9 层防护（新增 MIME 双重验证、Zip Bomb 防护、路径穿越防护、内容安全检查、文件类型白名单详解）；②新增 §10 任务回放功能（5 种回放模式 + 7 项记录数据 + terminal_event 集成）；③新增 §11 命令面板一等功能（微信公众号候审导入、GitHub 仓库推荐雷达、ComfyUI 图片/视频生成、PDF/PPT 智能嵌入）；④新增 §12 高风险动作强制 terminal_event 规则（12 类操作事件映射 + SafetyEnforcer 实现约束 + 5 种用户不遗漏确认机制）；⑤terminal_event.schema.json 新增 task_replay 事件（14→15 种）；⑥全部后续章节重新编号（§10→§13，§11→§14，§12→§15，§13→§16）*
*关联文档: [[UPGRADE_GUIDE.md]] Phase 10, [[OMEGA_FINAL_FORM.md]], [[AGENTS.md]], [[DEPLOYMENT_CONTRACT.md]], [[schemas/terminal_event.schema.json]]*
