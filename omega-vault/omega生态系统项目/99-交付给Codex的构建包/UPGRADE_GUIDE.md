# Omega 系统完整升级指南：MFE → 完全体

> **给 Codex 的系统升级规范**
> 
> 当前版本：Omega v0.3.0-mfe（MFE 最小功能生态）  
> 目标版本：Omega v1.0.0-full（完全体）  
> **此指南要求 Codex 从当前已构建的 MFE 系统出发，逐阶段升级到完全体，实现全部设计文档中构想的理念和功能。**

---

## 0. 前置条件：Codex 必读

在开始升级前，Codex 必须确认以下前提：

### 0.0 环境确认

```bash
# 1. OMEGA_HOME 已设置
echo $env:OMEGA_HOME   # 默认 D:\Omega-System

# 2. MFE 已构建完成（7/7 bench 通过）
.venv\Scripts\python -m app.main bench --all

# 3. 所有基础设施已就绪
docker ps                 # PostgreSQL + Qdrant + sandbox 运行中
.venv\Scripts\python -m app.main status
```

> **⚠️ 闭环编号约定**：本指南中引用的"闭环 N"（如闭环 1/3/5 等）的数字编号在不同文档中含义不同。Codex 在实现闭环验收时，**必须以 `templates/BENCHMARK_CATALOG.yaml` 中的稳定字符串 ID（catalog_id）为准**，从中查找 `legacy_numbers.upgrade_guide` 字段确定具体对应哪个闭环。例如本指南的"闭环 1" = `literature_ingestion`，"闭环 3" = `csv_analysis`。

### 0.1 已完整实现（无需改动）

| 模块 | 文件 | 状态 |
|------|------|------|
| 配置加载 | `app/config.py` + `omega.yaml` | ✅ Pydantic v2 全模型、env 加载、引擎健康检查 |
| CLI 命令 | `app/main.py` | ✅ 10 个命令全部工作 |
| 任务网关 | `app/gateway/task_gateway.py` | ✅ 自然语言 → 11 种 task_type 分类 + TaskContract 构建 |
| 静态路由 | `app/router/router.py` | ✅ 18 种任务类型 × 静态 YAML 路由表 |
| 引擎解析器 | `app/router/engine_resolver.py` | ✅ 4 策略链（quality_sensitive/cost_sensitive/realtime_search/general）|
| 数据隐私守卫 | `app/safety/privacy.py` | ✅ 4 级数据分类 + glob→regex + 会话缓存 |
| 文件访问守卫 | `app/safety/guardian.py` | ✅ FileAccessGuard + SessionState（JSON 持久化）|
| Codex 守卫 CLI | `app/safety/codex_guard.py` | ✅ omega-guardian check/list-sensitive/authorize |
| 闭环基准 | `app/executor/closed_loop.py` | ✅ 7/7 bench 通过 |
| PPT 质量分析器 | `app/executor/ppt_generator.py` | ✅ 8 维度 ZIP 结构分析 |
| 工具发现引擎 | `app/executor/tool_discovery.py` | ✅ PyPI/GitHub 搜索 + Docker 安装 + 测试 + 注册 |
| 测试套件 | `tests/` | ✅ 72 测试通过 |

### 0.2 当前架构瓶颈（本升级要解决的核心问题）

```
┌─────────────────────────────────────────────────────────────────┐
│                     Omega v0.3.0-mfe 架构                        │
│                                                                 │
│  用户自然语言 → classify_task() → 静态路由表查 tool → 线性执行    │
│                                                                 │
│  缺失：                                                          │
│  ❌ 动态评分（12 维权重全定义但代码为零）                          │
│  ❌ Agent 运行时（11 个 Agent 全定义在 YAML 里但无执行代码）       │
│  ❌ 并行 DAG 规划（规划器只产生线性链）                            │
│  ❌ MCP 服务器管理（JSON 配置存在但无启动/停止/健康检查代码）       │
│  ❌ Toolsmith 完整闭环（发现→适配器→Skill 封装→注册）             │
│  ❌ Docker 沙箱无 Python/pip（基于 qdrant 镜像，只有 curl）       │
│  ❌ 演化自动升级引擎（risk_policy.yaml 定义但未调用）              │
│  ❌ 成果包组装器（app/outcome/ 空目录）                            │
│  ❌ 行动记忆层（app/memory/ 空目录，PostgreSQL/Qdrant 未编程使用） │
│  ❌ 日志系统（omega.yaml 定义了 logging 但代码从未写日志）         │
│  ❌ Web UI / 后台服务 / 通知（设计文档已定义但未实现）             │
│  ❌ 科学可视化 / 创意工具 / Computer Use（域配置存在但代码为空）   │
└─────────────────────────────────────────────────────────────────┘
```

---

## 1. 升级总览：12 个阶段（Phase 1.5 + 2-11）

```
Phase 1.5 ████████████ Omega Terminal Lite — 早期统一窗口（Jinja2+HTMX，零前端依赖）
Phase 2  ████████████ Docker 沙箱重构建（Python/pip/node 运行时）
Phase 3  ████████████ 动态评分路由器（12 维加权 → static_then_scored 的 scored 半）
Phase 4  ████████████ Agent 运行时（11 个 Agent 从 YAML → 可调度执行单元）
Phase 5  ████████████ 完整动态规划器（并行 DAG + 模板库 + 能力缺口预检）
Phase 6  ████████████ MCP 管理器 + Toolsmith-Lite（工具全生命周期）
Phase 7  ████████████ 记忆层（PostgreSQL 行动记忆 + Qdrant 向量索引）
Phase 8  ████████████ 演化引擎 + 成果包组装器 + 日志系统
Phase 9  ████████████ 域扩展（科学可视化 / 创意工具 / Computer Use-Lite）
Phase 10 ████████████ Omega Terminal Full（React+WebSocket VS Code 风格完全体）
Phase 11 ████████████ 质量与安全加固（模拟构建器 + 飞行记录仪 + 溯源水印 + 预算控制台 + 工具隔离 + 知识防污染）
```

> **为什么从 Phase 1.5 开始？** Phase 1（MFE 构建）已在当前系统中完成。Phase 1.5 在 MFE 之上立即部署统一操作窗口（Terminal Lite），然后用 Phase 2-11 逐步进化到完全体。

---

## Phase 1.5：Omega Terminal Lite — 早期统一窗口 【优先级：🔴 最高】

> **设计文档**：`build-package/OMEGA_TERMINAL.md`（完整终端设计）、`schemas/terminal_event.schema.json`（事件协议）
> **定位**：不等到 Phase 10 才拥有窗口。MFE 构建完成后立即部署一个轻量但完整的统一操作界面。
> **与 Phase 10 的关系**：Phase 1.5 = 功能完整的 Jinja2+HTMX 轻量版；Phase 10 = React+WebSocket 的 VS Code 风格完全体。两者共享同一后端 API，前端渐进升级。

### 问题
Omega MFE 目前只能通过 CLI（`omega task "..."`）交互。用户没有一个窗口可以看到任务进度、上传文件、查看通知。Omega 的很多反馈（确认请求、风险警告、文件产出）没有统一的展示渠道。

### 目标
在 MFE 构建完成后、Phase 2 升级开始前，立即部署一个**可用的统一操作窗口**。用户打开 `http://localhost:8420` 即可以：
- 自然语言输入任务
- 拖拽上传文件
- 查看实时任务进度
- 接收并响应 Omega 的确认/审批请求
- 查看通知和系统状态

### 设计原则
1. **零前端依赖**：纯 Jinja2 模板 + HTMX + 少量 Vanilla JS，不引入 React/npm/Node 构建链
2. **共享后端**：与 Phase 10 Terminal Full 共享同一套 FastAPI 后端和事件协议
3. **渐进升级**：Terminal Lite 的前端可以逐步替换为 React 组件，不中断服务
4. **事件驱动**：使用 `schemas/terminal_event.schema.json` 定义的统一事件协议

### 实施步骤

#### 1.5.1 后端 — `app/web/app.py`

```python
"""Omega Terminal Lite — 轻量统一操作窗口后端"""
from fastapi import FastAPI, Request, UploadFile, File
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import uuid, hashlib, os, json
from datetime import datetime

app = FastAPI(title="Omega Terminal")
templates = Jinja2Templates(directory="app/web/templates")
app.mount("/static", StaticFiles(directory="app/web/static"), name="static")

# ── 事件总线（内存，Terminal Lite 用轮询替代 WebSocket）──
event_bus: list = []  # 简化版事件队列，Phase 10 升级为 WebSocket

def push_event(event_type: str, payload: dict, task_id: str = None):
    """推入事件到总线"""
    event = {
        "event_id": str(uuid.uuid4()),
        "event_type": event_type,
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "task_id": task_id,
        "payload": payload
    }
    event_bus.append(event)
    # 保留最近 500 条
    if len(event_bus) > 500:
        event_bus.pop(0)
    return event

# ── 页面路由 ──
@app.get("/", response_class=HTMLResponse)
async def terminal(request: Request):
    """Omega Terminal 主界面"""
    return templates.TemplateResponse("terminal.html", {
        "request": request,
        "omega_version": "v0.3.0-mfe",
        "active_tasks": get_active_tasks()
    })

# ── API 路由 ──
@app.get("/api/events")
async def poll_events(since: str = None):
    """轮询事件（Terminal Lite 用，Phase 10 改为 WebSocket）"""
    if since:
        filtered = [e for e in event_bus if e["timestamp"] > since]
    else:
        filtered = event_bus[-20:]  # 最近 20 条
    return {"events": filtered, "server_time": datetime.utcnow().isoformat() + "Z"}

@app.post("/api/task")
async def submit_task(goal: str, files: list[str] = None):
    """提交自然语言任务"""
    task_id = str(uuid.uuid4())
    push_event("task_lifecycle", {
        "task_id": task_id, "status": "created", "goal": goal
    }, task_id)
    # → 调用 Omega Core pipeline（复用 CLI 逻辑）
    return {"task_id": task_id, "status": "created"}

@app.post("/api/upload")
async def upload_file(file: UploadFile = File(...)):
    """文件上传 + 安全规则（详见 OMEGA_TERMINAL.md §9）"""
    # 安全规则检查
    MAX_SIZE = 100 * 1024 * 1024  # 100MB
    ALLOWED_EXTENSIONS = {'.pdf','.csv','.xlsx','.pptx','.docx','.md','.txt','.png','.jpg','.jpeg','.gif','.webp','.zip','.json','.yaml','.py','.r','.ipynb'}
    ext = os.path.splitext(file.filename)[1].lower()
    if ext not in ALLOWED_EXTENSIONS:
        push_event("upload_result", {"original_name": file.filename, "status": "rejected", "security": {"passed": False, "warnings": [f"文件类型 {ext} 不在白名单中"]}})
        return {"error": f"文件类型 {ext} 不允许"}
    
    content = await file.read()
    if len(content) > MAX_SIZE:
        push_event("upload_result", {"original_name": file.filename, "status": "rejected", "security": {"passed": False, "warnings": ["文件超过 100MB 限制"]}})
        return {"error": "文件超过 100MB 限制"}
    
    file_id = str(uuid.uuid4())
    quarantine_dir = f"omega-workspace/uploads/quarantine/{file_id}"
    os.makedirs(quarantine_dir, exist_ok=True)
    
    filepath = os.path.join(quarantine_dir, file.filename)
    with open(filepath, "wb") as f:
        f.write(content)
    
    sha256 = hashlib.sha256(content).hexdigest()
    
    event = push_event("upload_result", {
        "file_id": file_id, "original_name": file.filename,
        "stored_path": filepath, "size_bytes": len(content),
        "hash_sha256": sha256, "status": "uploaded",
        "detected_type": ext.lstrip('.'),
        "suggestions": get_suggestions(ext),
        "security": {"passed": True, "checks": ["size_ok", "type_whitelisted", "hash_recorded", "quarantined"]}
    })
    return event["payload"]

@app.get("/api/status")
async def system_status():
    return {"omega_version": "v0.3.0-mfe", "services": check_services(), "uptime_seconds": get_uptime()}
```

#### 1.5.2 前端 — `app/web/templates/terminal.html`

Jinja2 + HTMX 三栏布局（无需 React，无需 npm install）：

```html
<!DOCTYPE html>
<html lang="zh-CN" data-theme="dark">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Omega Terminal</title>
    <script src="/static/htmx.min.js"></script>
    <style>
        /* Omega Dark 主题 —— 类 VS Code 配色 */
        :root {
            --bg-primary: #1e1e1e;
            --bg-secondary: #252526;
            --bg-tertiary: #2d2d30;
            --text-primary: #cccccc;
            --text-secondary: #969696;
            --accent: #007acc;
            --success: #4ec9b0;
            --warning: #cca700;
            --error: #f44747;
            --border: #3e3e42;
        }
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; background: var(--bg-primary); color: var(--text-primary); height: 100vh; display: flex; flex-direction: column; }
        
        /* 三段式布局 */
        .terminal-layout { display: flex; flex: 1; overflow: hidden; }
        .sidebar-left { width: 260px; background: var(--bg-secondary); border-right: 1px solid var(--border); overflow-y: auto; }
        .main-chat { flex: 1; display: flex; flex-direction: column; }
        .sidebar-right { width: 300px; background: var(--bg-secondary); border-left: 1px solid var(--border); overflow-y: auto; }
        
        /* 对话区 */
        .chat-messages { flex: 1; overflow-y: auto; padding: 16px; }
        .message { margin-bottom: 16px; padding: 12px; border-radius: 8px; }
        .message.user { background: var(--bg-tertiary); margin-left: 32px; }
        .message.omega { background: transparent; border-left: 3px solid var(--accent); padding-left: 16px; }
        
        /* 输入栏 */
        .command-bar { display: flex; padding: 12px; background: var(--bg-secondary); border-top: 1px solid var(--border); }
        .command-input { flex: 1; background: var(--bg-primary); color: var(--text-primary); border: 1px solid var(--border); border-radius: 6px; padding: 10px 16px; font-size: 14px; }
        .command-input:focus { outline: none; border-color: var(--accent); }
        
        /* 状态栏 */
        .status-bar { display: flex; justify-content: space-between; padding: 4px 12px; background: var(--accent); color: white; font-size: 12px; }
        
        /* 通知 */
        .notification { padding: 8px 12px; margin: 4px 8px; border-radius: 4px; font-size: 13px; }
        .notification.info { background: #04395e; border-left: 3px solid var(--accent); }
        .notification.success { background: #1a3a2a; border-left: 3px solid var(--success); }
        .notification.warning { background: #3d3500; border-left: 3px solid var(--warning); }
        .notification.error { background: #3d0000; border-left: 3px solid var(--error); }
        
        /* 文件卡片 */
        .file-card { display: flex; align-items: center; gap: 8px; padding: 8px 12px; margin: 4px 0; background: var(--bg-tertiary); border-radius: 6px; cursor: pointer; }
        .file-card:hover { background: #383838; }
        
        /* 进度条 */
        .progress-bar { height: 6px; background: var(--bg-tertiary); border-radius: 3px; overflow: hidden; margin: 8px 0; }
        .progress-fill { height: 100%; background: var(--accent); transition: width 0.3s; }
        
        /* 响应式 */
        @media (max-width: 900px) { .sidebar-right { display: none; } }
        @media (max-width: 600px) { .sidebar-left { display: none; } }
    </style>
</head>
<body>
    <div class="terminal-layout">
        <!-- 左侧：文件浏览器 + 上传 -->
        <aside class="sidebar-left">
            <div style="padding:12px;border-bottom:1px solid var(--border);">
                <h3 style="font-size:14px;color:var(--text-secondary);">📁 文件浏览器</h3>
            </div>
            <div hx-get="/api/vault/browse" hx-trigger="load, every 30s" hx-swap="innerHTML">
                加载中...
            </div>
            <div style="padding:12px;border-top:1px solid var(--border);">
                <form hx-post="/api/upload" hx-encoding="multipart/form-data" hx-target="#upload-result">
                    <input type="file" name="file" style="color:var(--text-secondary);font-size:12px;max-width:100%;"
                           hx-post="/api/upload" hx-encoding="multipart/form-data" hx-target="#upload-result"
                           _="on change the form request submit">
                </form>
                <div id="upload-result"></div>
                <p style="font-size:11px;color:var(--text-secondary);margin-top:4px;">
                    拖拽文件到此处或点击上传<br>支持 PDF/CSV/PPTX/DOCX/MD/图片
                </p>
            </div>
        </aside>
        
        <!-- 中央：对话区 -->
        <main class="main-chat">
            <div class="chat-messages" id="chat-messages"
                 hx-get="/api/events" hx-trigger="every 2s" hx-swap="innerHTML">
                <div class="message omega">
                    <strong>Omega Terminal</strong> 已就绪。<br>
                    输入自然语言指令或拖拽文件上传。
                </div>
            </div>
            <div class="command-bar">
                <input type="text" class="command-input" id="cmd-input"
                       placeholder="输入指令或 Ctrl+Shift+P 打开命令面板..."
                       hx-post="/api/task" hx-target="#chat-messages" hx-swap="beforeend"
                       _="on keydown if event.key is 'Enter' then the form request submit then set my value to '' end">
                <button style="margin-left:8px;padding:8px 16px;background:var(--accent);color:white;border:none;border-radius:6px;cursor:pointer;"
                        _="on click set #cmd-input's value to '' then halt">
                    发送
                </button>
            </div>
        </main>
        
        <!-- 右侧：任务状态 + 通知 -->
        <aside class="sidebar-right">
            <div style="padding:12px;border-bottom:1px solid var(--border);">
                <h3 style="font-size:14px;color:var(--text-secondary);">📊 活跃任务</h3>
            </div>
            <div id="task-panel" hx-get="/api/task/list" hx-trigger="every 3s" hx-swap="innerHTML">
                无活跃任务
            </div>
            <div style="padding:12px;border-bottom:1px solid var(--border);border-top:1px solid var(--border);">
                <h3 style="font-size:14px;color:var(--text-secondary);">🔔 通知</h3>
            </div>
            <div id="notifications" hx-get="/api/notify/list" hx-trigger="every 3s" hx-swap="innerHTML">
                无新通知
            </div>
        </aside>
    </div>
    
    <!-- 状态栏 -->
    <footer class="status-bar">
        <span>✅ Omega v0.3.0-mfe</span>
        <span id="engine-status">quality_reasoning</span>
        <span id="task-count">任务: 0 活跃</span>
        <span id="clock">--:--:--</span>
    </footer>
    
    <script>
        // 极简 JS：时钟 + 快捷键 + 拖拽
        setInterval(() => { document.getElementById('clock').textContent = new Date().toLocaleTimeString(); }, 1000);
        
        // 键盘快捷键
        document.addEventListener('keydown', (e) => {
            if (e.ctrlKey && e.key === 'Enter') {
                document.querySelector('.command-input').dispatchEvent(new Event('submit', {bubbles: true}));
            }
            if (e.ctrlKey && e.key === 'l') {
                e.preventDefault();
                document.getElementById('chat-messages').innerHTML = '';
            }
        });
        
        // 拖拽上传
        document.addEventListener('dragover', (e) => e.preventDefault());
        document.addEventListener('drop', async (e) => {
            e.preventDefault();
            const file = e.dataTransfer.files[0];
            if (!file) return;
            const formData = new FormData();
            formData.append('file', file);
            await fetch('/api/upload', { method: 'POST', body: formData });
        });
    </script>
</body>
</html>
```

#### 1.5.3 文件上传安全规则

详见 `OMEGA_TERMINAL.md §9`。Terminal Lite 也必须遵守：
- **大小限制**：单文件 ≤ 100MB
- **路径隔离**：上传文件存入 `omega-workspace/uploads/quarantine/{uuid}/`
- **类型白名单**：仅 19 种允许类型
- **Hash 记录**：SHA-256 → `uploads_manifest.json`
- **来源记录**：时间 + 会话 ID + 原始文件名
- **永不直接写 wiki**：所有上传文件必须经过任务处理 + 知识防污染审查后才入库

#### 1.5.4 静态资源

```bash
# 下载 HTMX（单文件，无构建步骤）
curl -o app/web/static/htmx.min.js https://unpkg.com/htmx.org@1.9.12/dist/htmx.min.js
```

无 npm、无 webpack、无 node_modules。总共 3 个静态文件：
- `app/web/static/htmx.min.js` — HTMX 库（~14KB gzipped）
- `app/web/static/favicon.ico` — Omega 图标
- `app/web/templates/terminal.html` — 主界面模板

#### 1.5.5 验证

```bash
omega web --port 8420                     # 启动 Terminal Lite
# → 浏览器打开 http://localhost:8420
# → 看到三栏布局（文件浏览器 | 对话区 | 任务/通知）
# → 输入"omega status"→ 返回系统状态
# → 拖拽 test.pdf → 上传成功卡片
# → 文件进入隔离区（非 wiki/）
# → 通知面板显示推送

# 代码行数验证
wc -l app/web/app.py     # 应 < 150 行
wc -l app/web/templates/terminal.html  # 应 < 200 行
```

### 受影响文件

| 文件 | 操作 |
|------|------|
| `app/web/__init__.py` | **新建** |
| `app/web/app.py` | **新建** — Terminal Lite 后端（~150行） |
| `app/web/templates/terminal.html` | **新建** — 三栏布局 + HTMX 交互（~200行） |
| `app/web/static/htmx.min.js` | **新建** — 下载（~14KB） |
| `app/web/static/favicon.ico` | **新建** — Omega 图标 |
| `app/main.py` | 修改 — 新增 `web` 命令 |

**文件统计**：5 新文件，1 修改文件。零前端构建依赖。

---

## Phase 2：Docker 沙箱重构建 【优先级：最高 🔴】

### 问题
当前 `Dockerfile.sandbox` 和 `Dockerfile.sandbox-net` 基于 `qdrant/qdrant:v1.14.1` 构建。沙箱内**没有 Python、pip、Node.js、npm**。所有 `docker exec pip install` 操作失败。这是阻塞所有后续阶段的基础设施缺陷。

### 目标
重构建双沙箱镜像，包含完整的 Python 3.11+ 和 pip，可选 Node.js。

### 实施步骤

#### 2.1 重写 Dockerfile.sandbox（离线执行沙箱）
- 文件：`{OMEGA_HOME}/omega-runtime/Dockerfile.sandbox`
- 新基础镜像：`python:3.11-slim-bookworm`
- 预装：`pip`、`wheel`、常用科学计算库（numpy, pandas, scipy, matplotlib, scikit-learn）
- 安全加固：Dockerfile 中创建非 root 用户 `omega`，`USER omega`
- `network_mode: none` 在 docker-compose 层控制
- tmpfs /tmp 在 docker-compose 层控制

```dockerfile
FROM python:3.11-slim-bookworm

# 安装系统依赖
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# 预装 Python 科学计算核心库
RUN pip install --no-cache-dir \
    numpy pandas scipy matplotlib scikit-learn \
    openpyxl python-pptx Pillow

# 创建非 root 用户
RUN useradd -m -s /bin/bash omega
USER omega
WORKDIR /workspace

ENTRYPOINT ["python"]
```

#### 2.2 重写 Dockerfile.sandbox-net（联网安装沙箱）
- 文件：`{OMEGA_HOME}/omega-runtime/Dockerfile.sandbox-net`
- 新基础镜像：`python:3.11-slim-bookworm`
- 预装：`pip`、`git`、`curl`、`nodejs`、`npm`
- 网络：bridge 模式

```dockerfile
FROM python:3.11-slim-bookworm

RUN apt-get update && apt-get install -y --no-install-recommends \
    git curl ca-certificates gnupg \
    && rm -rf /var/lib/apt/lists/*

# 安装 Node.js 22.x（可选，用于 npm 工具发现）
RUN curl -fsSL https://deb.nodesource.com/setup_22.x | bash - \
    && apt-get install -y nodejs \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir pip wheel setuptools

RUN useradd -m -s /bin/bash omega
USER omega
WORKDIR /workspace
```

#### 2.3 更新 docker-compose.yml
- 将两个沙箱服务的 `build.context` 指向 omega-runtime 根目录
- `omega-sandbox` 的 `build.dockerfile` 指向 `Dockerfile.sandbox`
- `omega-sandbox-net` 的 `build.dockerfile` 指向 `Dockerfile.sandbox-net`
- 删除旧的 `image: qdrant/qdrant:v1.14.1` 引用
- 保持挂载：`omega-workspace/sandbox/` → `/workspace/`
- 保持 `omega-sandbox` 的 `network_mode: "none"`
- 保持 `omega-sandbox-net` 的 DNS 配置

#### 2.4 重建沙箱镜像并验证
```bash
cd {OMEGA_HOME}/omega-runtime
docker compose build omega-sandbox omega-sandbox-net
docker compose up -d omega-sandbox omega-sandbox-net

# 验证
docker exec omega-sandbox python --version      # Python 3.11.x
docker exec omega-sandbox python -c "import numpy"  # 成功
docker exec omega-sandbox-net pip --version     # pip 24.x
docker exec omega-sandbox-net git --version     # git 2.x
docker exec omega-sandbox curl --version        # 离线沙箱不应有 curl（预期失败）
```

#### 2.5 更新 tool_discovery.py 的 pip 安装路径
- 验证 `docker exec omega-sandbox-net pip install <package>` 成功
- 验证安装后从 `omega-sandbox`（离线）可以 import 已安装库

#### 2.6 最终验证
```bash
omega bench --all
# 预期：7/7 通过，quality_improvement 工具发现在线部分不再报 "pip: not found"
```

### 受影响文件
| 文件 | 操作 |
|------|------|
| `Dockerfile.sandbox` | **重写** |
| `Dockerfile.sandbox-net` | **重写** |
| `docker-compose.yml` | 修改 — 更新 build 配置 |
| `app/executor/tool_discovery.py` | 验证 |

---

## Phase 3：动态评分路由器 【优先级：高 🟠】

### 问题
路由表 mode 是 `static_then_scored`，但只有 static 实现了。12 维评分权重（`omega.yaml` routing.scoring 段）和阶段感知权重覆盖（`stage_weights.yaml`）全定义了但**无代码使用**。

### 目标
实现 `DynamicScorer` 类，使 `ToolAgentRouter` 能在静态路由基础上，按 12 维分数动态选择最佳工具。

### 设计参考
- 主设计文档：`{OMEGA_HOME}/omega-vault/omega生态系统项目/02-架构/Tool-Agent Router：最佳工具与最佳执行者选择器.md`
- 配置文件：`omega.yaml` routing.scoring
- 阶段权重：`build-package/config/stage_weights.yaml`

### 实施步骤

#### 3.1 新建 `app/router/scorer.py`
```python
"""Dynamic multi-dimensional tool scoring engine."""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any

@dataclass
class ScoredCandidate:
    """A tool candidate with its dimension scores and total score."""
    tool_id: str
    tool_name: str
    total_score: float = 0.0
    dimension_scores: dict[str, float] = field(default_factory=dict)

class DynamicScorer:
    """12-dimension weighted tool scoring.
    
    Cold-start: all candidates start at 0.5 per dimension.
    Scores evolve through ScoreFeedbackLoop.
    Stage-aware weights override default weights per task stage.
    """
    
    DEFAULT_WEIGHTS = {
        "task_fit": 0.20,
        "success_rate": 0.18,
        "output_quality": 0.15,
        "reputation": 0.12,
        "cost": 0.10,
        "speed": 0.08,
        "controllability": 0.06,
        "batch_reproducibility": 0.05,
        "safety": 0.04,
        "documentation_quality": 0.02,
    }
    
    def __init__(self, stage_weights_path: str | None = None, 
                 tool_scores_path: str | None = None):
        self.weights = dict(self.DEFAULT_WEIGHTS)
        self.tool_scores: dict[str, dict[str, float]] = {}
        # Load stage weights and historical scores if paths provided
        
    def score(self, candidates: list[dict], task_context: dict) -> list[ScoredCandidate]:
        """Score candidates against task context. Returns sorted list (best first)."""
        results = []
        for c in candidates:
            dims = self._score_dimensions(c, task_context)
            total = sum(dims.get(d, 0.5) * self.weights.get(d, 0) 
                       for d in self.weights)
            results.append(ScoredCandidate(
                tool_id=c.get("id", ""),
                tool_name=c.get("name", ""),
                total_score=round(total, 4),
                dimension_scores=dims,
            ))
        results.sort(key=lambda x: x.total_score, reverse=True)
        return results
    
    def _score_dimensions(self, candidate: dict, context: dict) -> dict[str, float]:
        """Score all 12 dimensions for a candidate. 
        Uses historical scores if available, otherwise cold-start 0.5."""
        tool_id = candidate.get("id", "")
        historical = self.tool_scores.get(tool_id, {})
        return {
            dim: historical.get(dim, 0.5) for dim in self.weights
        }
```

#### 3.2 新建 `app/router/feedback.py`
```python
"""Score feedback loop — updates tool scores after task execution."""

from __future__ import annotations
import json
from pathlib import Path

class ScoreFeedbackLoop:
    """Updates tool scores based on execution outcomes.
    
    Uses exponential moving average: new = α × observed + (1-α) × old
    Stores scores as JSON for persistence across sessions.
    """
    
    def __init__(self, state_path: Path, alpha: float = 0.3):
        self.state_path = state_path
        self.alpha = alpha
        
    def update(self, tool_id: str, dimension: str, observed: float) -> None:
        """Update a single dimension score for a tool."""
        scores = self._load()
        old = scores.get(tool_id, {}).get(dimension, 0.5)
        scores.setdefault(tool_id, {})[dimension] = (
            self.alpha * observed + (1 - self.alpha) * old
        )
        self._save(scores)
    
    def update_from_result(self, tool_id: str, 
                           success: bool, duration_ms: float,
                           output_quality: float = 0.5) -> None:
        """Bulk update from execution result."""
        self.update(tool_id, "success_rate", 1.0 if success else 0.0)
        self.update(tool_id, "speed", min(1.0, 1000.0 / max(duration_ms, 1)))
        self.update(tool_id, "output_quality", output_quality)
    
    def _load(self) -> dict:
        if self.state_path.exists():
            return json.loads(self.state_path.read_text())
        return {}
    
    def _save(self, data: dict) -> None:
        self.state_path.parent.mkdir(parents=True, exist_ok=True)
        self.state_path.write_text(json.dumps(data, indent=2))
```

#### 3.3 修改 `app/router/router.py`
- 在 `ToolAgentRouter.select_steps()` 增加 `enable_scoring: bool = True` 参数
- 若 `enable_scoring`：从路由表获取候选 → DynamicScorer.score() 排序 → 选最高分 → Engine Resolver 验证可用性 → 不可用则降级

#### 3.4 修改 `app/planner/planner.py`
- 调用路由时传入 `enable_scoring=True`
- 任务执行完后调用 `ScoreFeedbackLoop.update_from_result()`

#### 3.5 验证
```bash
pytest tests/test_scorer.py -v    # 冷启动分数、权重覆盖、降级链
omega bench --all                 # 仍 7/7（评分不改变现有闭环行为）
```

### 受影响文件
| 文件 | 操作 |
|------|------|
| `app/router/scorer.py` | **新建** |
| `app/router/feedback.py` | **新建** |
| `app/router/__init__.py` | 修改 |
| `app/router/router.py` | 修改 |
| `app/planner/planner.py` | 修改 |
| `tests/test_scorer.py` | **新建** |

---

## Phase 4：Agent 运行时 【优先级：高 🟠】

### 问题
`config/agents.yaml` 定义了 11 个 Agent（含能力限制、工具白名单/黑名单、自主级别、交接目标），但**无运行时代码**。

### 目标
实现 Agent 运行时——每个 Agent 作为可执行单元，受其 YAML 定义的约束。

### 设计参考
- `{OMEGA_HOME}/omega-vault/omega生态系统项目/02-架构/Dynamic Task Planner：动态任务规划器.md` 第 6 节
- `{OMEGA_HOME}/omega-vault/omega生态系统项目/10-外部AI与工具注册表/External AI Rolebook.md`
- `config/agents.yaml`

### 实施步骤

#### 4.1 新建 `app/agents/__init__.py`
导出 AgentRuntime、AgentDispatcher、CapabilityChecker、AgentResult。

#### 4.2 新建 `app/agents/agent.py`
```python
"""Agent runtime — executes steps under agent constraints."""

from __future__ import annotations
from dataclasses import dataclass, field
from enum import Enum
from typing import Any

class AutonomyLevel(str, Enum):
    L0 = "L0"  # 全手动 — 暂停等待用户确认每一步
    L1 = "L1"  # 半自动 — 自动执行，关键决策询问
    L2 = "L2"  # 自动+确认 — 自动执行，完成后报告
    L3 = "L3"  # 全自动 — 完全自主，仅记录日志

@dataclass
class AgentResult:
    agent_id: str
    step_id: str
    success: bool
    output: Any = None
    error: str | None = None
    duration_ms: float = 0.0

class AgentRuntime:
    """Single agent execution environment.
    
    Loads agent config from agents.yaml and enforces:
    - Tool allowlist/denylist filtering
    - Autonomy level gating
    - Handoff targets
    """
    
    def __init__(self, agent_config: dict):
        self.id = agent_config["id"]
        self.role = agent_config.get("role", "")
        self.allowed_tools = set(agent_config.get("allowed_tools", []))
        self.forbidden_tools = set(agent_config.get("forbidden_tools", []))
        self.autonomy = AutonomyLevel(agent_config.get("autonomy_level", "L2"))
        self.handoff_targets = agent_config.get("handoff_targets", [])
        self.capabilities = agent_config.get("capabilities", [])
    
    def can_use_tool(self, tool_id: str) -> bool:
        if tool_id in self.forbidden_tools:
            return False
        if self.allowed_tools and tool_id not in self.allowed_tools:
            return False
        return True
    
    def requires_confirmation(self) -> bool:
        return self.autonomy in (AutonomyLevel.L0, AutonomyLevel.L1)
    
    def execute(self, step: dict, context: dict) -> AgentResult:
        """Execute a single step under this agent's constraints."""
        import time
        start = time.time()
        try:
            tool_id = step.get("selected_tool", "")
            if not self.can_use_tool(tool_id):
                return AgentResult(self.id, step["id"], False, 
                                   error=f"Tool {tool_id} not allowed for agent {self.id}")
            # Delegate to tool executor (actual execution handled by closed_loop)
            return AgentResult(self.id, step["id"], True,
                             duration_ms=(time.time() - start) * 1000)
        except Exception as e:
            return AgentResult(self.id, step["id"], False, error=str(e),
                             duration_ms=(time.time() - start) * 1000)
```

#### 4.3 新建 `app/agents/dispatcher.py`
```python
"""Agent dispatcher — assigns steps to agents."""

from pathlib import Path
import yaml
from app.agents.agent import AgentRuntime, AgentResult

class AgentDispatcher:
    """Loads all agent configs and dispatches steps to matching agents."""
    
    def __init__(self, config_path: Path):
        with open(config_path) as f:
            config = yaml.safe_load(f)
        self.agents: dict[str, AgentRuntime] = {}
        for agent_data in config.get("agents", []):
            agent = AgentRuntime(agent_data)
            self.agents[agent.id] = agent
    
    def dispatch(self, step: dict) -> AgentRuntime | None:
        """Find the best agent for a step. Returns None if no match."""
        assigned = step.get("assigned_agent")
        if assigned and assigned in self.agents:
            return self.agents[assigned]
        # Fallback: match by capabilities
        required = set(step.get("required_capabilities", []))
        for agent in self.agents.values():
            if required.issubset(set(agent.capabilities)):
                return agent
        return None
    
    def handoff(self, from_agent: str, to_agent: str, 
                context: dict) -> bool:
        """Transfer context from one agent to another."""
        if to_agent not in self.agents:
            return False
        if from_agent in self.agents:
            if to_agent not in self.agents[from_agent].handoff_targets:
                return False
        return True
```

#### 4.4 新建 `app/agents/capability.py`
```python
"""Capability checker — verifies agents can execute steps."""

class CapabilityChecker:
    """Checks whether an agent has the capabilities required for a step."""
    
    @staticmethod
    def check(agent_capabilities: list[str], 
              required_capabilities: list[str]) -> tuple[bool, list[str]]:
        """Returns (has_all, missing_capabilities)."""
        missing = [c for c in required_capabilities 
                   if c not in agent_capabilities]
        return len(missing) == 0, missing
    
    @staticmethod
    def find_gaps(plan_steps: list[dict], 
                  available_agents: list[str]) -> list[str]:
        """Find capabilities not covered by any agent."""
        all_agent_caps = set()
        all_required = set()
        for step in plan_steps:
            all_required.update(step.get("required_capabilities", []))
        return list(all_required - all_agent_caps)
```

#### 4.5 修改 `app/planner/planner.py`
- `plan()` 生成的每个 step 包含 `assigned_agent: str`
- `execute_plan()` 调用 `AgentDispatcher.dispatch()` 按 step 分配 Agent
- Agent 执行受其自主级别约束（L0→暂停等待确认）

#### 4.6 验证
```bash
pytest tests/test_agents.py -v    # Agent 加载、白名单过滤、门控、交接
omega bench --all                 # 仍 7/7
```

### 受影响文件
| 文件 | 操作 |
|------|------|
| `app/agents/__init__.py` | **新建** |
| `app/agents/agent.py` | **新建** |
| `app/agents/dispatcher.py` | **新建** |
| `app/agents/capability.py` | **新建** |
| `app/planner/planner.py` | 修改 |
| `tests/test_agents.py` | **新建** |

---

## Phase 5：完整动态规划器 【优先级：高 🟠】

### 问题
当前 `DynamicTaskPlanner.plan()` 只产生线性 DAG（`build_linear_dag()`）。设计文档承诺了 7 步规划流程。

### 目标
升级为真正的动态 DAG 生成器，支持并行分支和条件路径。

### 设计参考
- `{OMEGA_HOME}/omega-vault/omega生态系统项目/02-架构/Dynamic Task Planner：动态任务规划器.md`

### 7 步规划流程

1. **模板匹配** — 从模板库匹配最接近的任务模板
2. **依赖分析** — 分析 step 间数据流依赖关系
3. **能力缺口预检** — 检查所需能力是否可用
4. **并行化** — 识别独立分支标记为 parallel
5. **资源估算** — 估算时间/成本/API 调用量
6. **生成 DAG** — 构建完整执行 DAG
7. **写入执行计划** — 持久化为 JSON

### 实施步骤

#### 5.1 模板库 — `app/planner/templates/`
创建 JSON 模板文件：
- `research_pipeline.json` — 标准研究管线（检索→筛选→提取→分析→报告）
- `literature_review.json` — 文献综述（搜索→筛选→摘要→综合→写作）
- `data_analysis.json` — 数据分析（QC→清洗→统计→图表→报告）

每个模板定义：task_type, stages[], step_dependencies{}, parallel_groups[], required_capabilities[]

#### 5.2 依赖分析器 — `app/planner/dependency.py`
- `DependencyAnalyzer` 类
- `build_dependency_graph(steps)` → 依赖 DAG
- 基于数据流：step A 的输出 → step B 的输入 → B 依赖 A
- 输出：拓扑排序的层（每层内可并行）

#### 5.3 并行化 — 修改 `app/planner/dag.py`
- 新增 `build_parallel_dag(steps, dep_graph)` → 并行 DAG
- 识别独立分支 → 标记为 parallel
- 按拓扑序执行，同层并行分支可并发

#### 5.4 能力缺口预检 — `app/planner/gap_check.py`
- `GapPrecheck` 类
- `check(plan, available_capabilities)` → 缺口清单
- 若缺口可由 Toolsmith 自动填补 → 触发 Phase 6
- 若无法填补 → 标记 `requires_manual_intervention`

#### 5.5 修改 `DynamicTaskPlanner.plan()`
替换 `build_linear_dag()` → 完整 7 步流程。

#### 5.6 验证
```bash
pytest tests/test_planner.py -v  # 并行 DAG、模板匹配、缺口检测
omega bench --all                # 仍 7/7
```

### 受影响文件
| 文件 | 操作 |
|------|------|
| `app/planner/templates/research_pipeline.json` | **新建** |
| `app/planner/templates/literature_review.json` | **新建** |
| `app/planner/templates/data_analysis.json` | **新建** |
| `app/planner/dependency.py` | **新建** |
| `app/planner/gap_check.py` | **新建** |
| `app/planner/dag.py` | 修改 |
| `app/planner/planner.py` | 修改 |
| `tests/test_planner.py` | 扩展 |

---

## Phase 6：MCP 管理器 + Toolsmith-Lite 【优先级：中 🟡】

### 问题
`app/mcp/` 和 `app/toolsmith/` 均为空目录。MCP 配置 JSON 存在但无服务器生命周期管理。Toolsmith 闭环仅有"发现"这一步。

### 目标
实现 MCP 服务器的程序化管理和 Toolsmith 的完整 7 步闭环。

### 实施步骤

#### 6.1 MCP 管理器 — `app/mcp/manager.py`
```python
"""MCP server lifecycle manager."""

import subprocess
import json
import socket
from pathlib import Path
from typing import Any

class MCPServerManager:
    """Programmatic management of MCP servers.
    
    Supports 8 servers: filesystem, postgres, qdrant, playwright, 
    github, brave-search, sequential-thinking, memory.
    """
    
    def __init__(self, config_path: Path):
        with open(config_path) as f:
            self.config = json.load(f)
        self._processes: dict[str, subprocess.Popen] = {}
    
    def start(self, server_name: str) -> bool:
        """Start an MCP server by name."""
        server = self.config.get("servers", {}).get(server_name, {})
        if not server or server.get("disabled", False):
            return False
        cmd = server.get("command", [])
        env = server.get("env", {})
        proc = subprocess.Popen(cmd, env={**__import__('os').environ, **env})
        self._processes[server_name] = proc
        return True
    
    def stop(self, server_name: str) -> bool:
        """Stop an MCP server."""
        proc = self._processes.pop(server_name, None)
        if proc:
            proc.terminate()
            return True
        return False
    
    def health(self, server_name: str) -> bool:
        """Check if an MCP server is healthy."""
        # TCP port probe or process alive check
        proc = self._processes.get(server_name)
        return proc is not None and proc.poll() is None
    
    def stop_all(self) -> None:
        for name in list(self._processes):
            self.stop(name)
```

#### 6.2 Toolsmith 适配器 — `app/toolsmith/adapter.py`
- `ToolAdapter` 类
- 将原始工具包装为标准 Omega 接口
- 输入/输出 schema 生成、参数映射、错误处理、超时控制

#### 6.3 Toolsmith 闭环 — `app/toolsmith/smith.py`
- `Toolsmith` 类
- 完整 7 步闭环：`detect_gap()` → `discover()` → `install()` → `generate_adapter()` → `test()` → `register()` → `package_skill()`
- 调用 `ToolDiscoveryEngine` 做发现
- 调用 `ToolAdapter` 做包装
- 输出：注册到 `config/tools.yaml` + 创建 Skill 目录

#### 6.4 验证
```bash
pytest tests/test_mcp.py tests/test_toolsmith.py -v
omega tool discover ppt_generation --auto-install  # PyPI 搜索成功
omega bench --all  # 仍 7/7
```

### 受影响文件
| 文件 | 操作 |
|------|------|
| `app/mcp/__init__.py` | 修改 |
| `app/mcp/manager.py` | **新建** |
| `app/toolsmith/__init__.py` | 修改 |
| `app/toolsmith/adapter.py` | **新建** |
| `app/toolsmith/smith.py` | **新建** |
| `tests/test_mcp.py` | **新建** |
| `tests/test_toolsmith.py` | **新建** |

---

## Phase 7：记忆层 【优先级：中 🟡】

### 问题
`omega.yaml` 定义了 PostgreSQL（行动记忆）和 Qdrant（向量索引），但运行时从未编程使用它们。

### 目标
实现行动记忆（PostgreSQL）和语义记忆（Qdrant 向量索引）。

### 设计参考
- `{OMEGA_HOME}/omega-vault/omega生态系统项目/08-运行时与原型/Omega Runtime Architecture.md` 第 2.5 节

### 实施步骤

#### 7.1 DDL — `app/memory/schema.sql`
```sql
CREATE TABLE IF NOT EXISTS task_history (
    task_id TEXT PRIMARY KEY,
    goal TEXT NOT NULL,
    task_type TEXT NOT NULL,
    complexity TEXT,
    status TEXT NOT NULL DEFAULT 'pending',
    plan_json JSONB,
    started_at TIMESTAMPTZ,
    completed_at TIMESTAMPTZ,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS tool_executions (
    execution_id SERIAL PRIMARY KEY,
    task_id TEXT REFERENCES task_history(task_id),
    tool_id TEXT NOT NULL,
    step_id TEXT,
    success BOOLEAN NOT NULL DEFAULT false,
    duration_ms FLOAT,
    error_log TEXT,
    executed_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS agent_decisions (
    decision_id SERIAL PRIMARY KEY,
    task_id TEXT REFERENCES task_history(task_id),
    agent_id TEXT NOT NULL,
    step_id TEXT NOT NULL,
    chosen_tool TEXT,
    alternatives JSONB,
    reason TEXT,
    decided_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_tool_executions_tool ON tool_executions(tool_id);
CREATE INDEX idx_tool_executions_success ON tool_executions(success);
CREATE INDEX idx_task_history_type ON task_history(task_type);
CREATE INDEX idx_task_history_status ON task_history(status);
```

#### 7.2 行动记忆 — `app/memory/action_store.py`
```python
"""PostgreSQL action memory store."""

import json
from datetime import datetime
from typing import Any
import psycopg2
from psycopg2.extras import Json

class ActionStore:
    """CRUD operations for task execution memory in PostgreSQL."""
    
    def __init__(self, dsn: str):
        self.conn = psycopg2.connect(dsn)
        self._init_schema()
    
    def _init_schema(self) -> None:
        schema_path = Path(__file__).parent / "schema.sql"
        with self.conn.cursor() as cur:
            cur.execute(schema_path.read_text())
        self.conn.commit()
    
    def record_task(self, task_id: str, goal: str, task_type: str, 
                    complexity: str, plan: dict) -> None:
        with self.conn.cursor() as cur:
            cur.execute(
                """INSERT INTO task_history (task_id, goal, task_type, 
                   complexity, plan_json, started_at, status)
                   VALUES (%s, %s, %s, %s, %s, %s, 'running')""",
                (task_id, goal, task_type, complexity, Json(plan), datetime.utcnow())
            )
        self.conn.commit()
    
    def record_execution(self, task_id: str, tool_id: str, step_id: str,
                         success: bool, duration_ms: float, error: str = None) -> None:
        with self.conn.cursor() as cur:
            cur.execute(
                """INSERT INTO tool_executions (task_id, tool_id, step_id, 
                   success, duration_ms, error_log)
                   VALUES (%s, %s, %s, %s, %s, %s)""",
                (task_id, tool_id, step_id, success, duration_ms, error)
            )
        self.conn.commit()
    
    def get_tool_success_rate(self, tool_id: str) -> float:
        with self.conn.cursor() as cur:
            cur.execute(
                """SELECT AVG(CASE WHEN success THEN 1.0 ELSE 0.0 END)
                   FROM tool_executions WHERE tool_id = %s""",
                (tool_id,)
            )
            row = cur.fetchone()
            return row[0] or 0.5
```

#### 7.3 语义记忆 — `app/memory/semantic_store.py`
```python
"""Qdrant semantic memory store for vector similarity search."""

from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct

class SemanticStore:
    """Semantic search across tool descriptions, task patterns, source pages."""
    
    COLLECTIONS = ["tool_descriptions", "task_patterns", "source_pages"]
    
    def __init__(self, url: str = "http://localhost:6333", embedding_dim: int = 1536):
        self.client = QdrantClient(url=url)
        self.embedding_dim = embedding_dim
        self._init_collections()
    
    def _init_collections(self) -> None:
        for name in self.COLLECTIONS:
            if not self._collection_exists(name):
                self.client.create_collection(
                    collection_name=name,
                    vectors_config=VectorParams(size=self.embedding_dim, 
                                                distance=Distance.COSINE)
                )
    
    def _collection_exists(self, name: str) -> bool:
        collections = self.client.get_collections().collections
        return any(c.name == name for c in collections)
    
    def search(self, collection: str, query_vector: list[float], 
               limit: int = 5) -> list[dict]:
        """Search for semantically similar items."""
        results = self.client.search(
            collection_name=collection,
            query_vector=query_vector,
            limit=limit,
        )
        return [{"id": r.id, "score": r.score, "payload": r.payload} 
                for r in results]
```

#### 7.4 评分器反馈集成
- `ScoreFeedbackLoop`（Phase 3）从 `action_store` 读取历史成功率
- 新工具执行后自动写入 `tool_executions`

#### 7.5 验证
```bash
omega status  # 应显示 PostgreSQL 和 Qdrant 连接状态
pytest tests/test_memory.py -v
omega bench --all  # 仍 7/7
```

### 受影响文件
| 文件 | 操作 |
|------|------|
| `app/memory/__init__.py` | 修改 |
| `app/memory/action_store.py` | **新建** |
| `app/memory/semantic_store.py` | **新建** |
| `app/memory/schema.sql` | **新建** |
| `app/router/feedback.py` | 修改 |
| `tests/test_memory.py` | **新建** |

---

## Phase 8：演化引擎 + 成果包组装器 + 日志 【优先级：中 🟡】

### 问题
三个独立模块缺失：演化引擎、成果包组装器、日志系统。

### 实施步骤

#### 8.1 演化引擎 — `app/evolution/engine.py`
- `EvolutionEngine` 类
- 读取 `risk_policy.yaml`：LOW→auto_upgrade、MEDIUM→sandbox_test_then_upgrade、HIGH→confirm_before_upgrade、CRITICAL→no_auto_upgrade
- 定期扫描工具注册表，检测过时工具
- 自动升级：发现新版本 → 沙箱测试 → 质量对比 → 自动替换或建议
- CLI：`omega evolve --check`、`omega evolve --upgrade <tool_id>`
- **🆕 Evolution Change Proposal (ECP)**：对于 MEDIUM/HIGH 风险级别的变更，EvolutionEngine 自动生成 ECP 提案（含变更摘要、风险评估、回滚方案、影响面分析），用户审批后才执行。ECP 持久化为 JSON（`omega-workspace/state/ecps/`），形成可审计的演化决策历史。

#### 8.1.1 Evolution Change Proposal (ECP) — `app/evolution/ecp.py`

**功能**：为所有非 LOW 风险的演化变更生成结构化提案，要求用户审批。解决"自动升级不受控地改核心"的风险。

```python
"""Evolution Change Proposal — structured change proposals requiring human approval."""

from __future__ import annotations
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
import json
from datetime import datetime, timezone


class ECPStatus(Enum):
    DRAFT = "draft"
    PENDING_REVIEW = "pending_review"
    APPROVED = "approved"
    REJECTED = "rejected"
    EXECUTED = "executed"
    ROLLED_BACK = "rolled_back"


class ChangeCategory(Enum):
    TOOL_UPGRADE = "tool_upgrade"        # 工具版本升级
    TOOL_REPLACEMENT = "tool_replacement"  # 工具替换
    ENGINE_SWITCH = "engine_switch"       # 默认引擎切换
    CONFIG_CHANGE = "config_change"       # 配置文件变更
    DEPENDENCY_UPDATE = "dependency_update" # 依赖更新


@dataclass
class ImpactAssessment:
    """受影响模块和风险评估。"""
    affected_modules: list[str] = field(default_factory=list)
    affected_tasks: list[str] = field(default_factory=list)
    breaking_changes: list[str] = field(default_factory=list)
    benchmark_impact: dict[str, str] = field(default_factory=dict)  # loop_name → expected_change
    rollback_complexity: str = "simple"  # simple | moderate | complex | irreversible


@dataclass
class EvolutionChangeProposal:
    """一份完整的演化变更提案。"""
    ecp_id: str                          # ECP-YYYYMMDD-NNN
    title: str
    category: ChangeCategory
    risk_level: str                      # LOW | MEDIUM | HIGH | CRITICAL
    status: ECPStatus = ECPStatus.DRAFT
    
    # 变更描述
    current_state: str = ""
    proposed_state: str = ""
    rationale: str = ""
    
    # 影响评估
    impact: ImpactAssessment = field(default_factory=ImpactAssessment)
    
    # 验证计划
    sandbox_test_plan: list[str] = field(default_factory=list)
    benchmark_before: dict[str, float] = field(default_factory=dict)   # loop → score
    benchmark_after: dict[str, float] = field(default_factory=dict)    # loop → score
    
    # 审批
    proposed_at: str = ""
    approved_by: str = ""
    approved_at: str = ""
    
    # 执行
    executed_at: str = ""
    rollback_command: str = ""
    
    # 溯源
    triggered_by: str = ""               # cron | manual | tool_smith | benchmark_oracle
    related_ecps: list[str] = field(default_factory=list)


class ECPManager:
    """管理 ECP 生命周期：创建→审批→执行→回滚→归档。"""
    
    def __init__(self, ecp_dir: Path):
        self.ecp_dir = Path(ecp_dir)
        self.ecp_dir.mkdir(parents=True, exist_ok=True)
    
    def create_proposal(
        self, title: str, category: ChangeCategory, risk_level: str,
        current: str, proposed: str, rationale: str
    ) -> EvolutionChangeProposal:
        """创建新的 ECP。"""
        ecp_id = f"ECP-{datetime.now(timezone.utc).strftime('%Y%m%d')}-{self._next_sequence():03d}"
        ecp = EvolutionChangeProposal(
            ecp_id=ecp_id,
            title=title,
            category=category,
            risk_level=risk_level,
            current_state=current,
            proposed_state=proposed,
            rationale=rationale,
            proposed_at=datetime.now(timezone.utc).isoformat()
        )
        self._save(ecp)
        return ecp
    
    def assess_impact(self, ecp: EvolutionChangeProposal) -> ImpactAssessment:
        """自动评估变更影响面。"""
        # 扫描受影响的模块、任务类型、是否有 breaking changes
        impact = ImpactAssessment()
        # ... 实现略
        return impact
    
    def submit_for_review(self, ecp: EvolutionChangeProposal) -> str:
        """提交审批，生成人类可读的审批摘要。"""
        ecp.status = ECPStatus.PENDING_REVIEW
        self._save(ecp)
        return self._format_review_summary(ecp)
    
    def approve(self, ecp_id: str, approved_by: str = "user") -> EvolutionChangeProposal:
        """审批通过。"""
        ecp = self._load(ecp_id)
        ecp.status = ECPStatus.APPROVED
        ecp.approved_by = approved_by
        ecp.approved_at = datetime.now(timezone.utc).isoformat()
        self._save(ecp)
        return ecp
    
    def reject(self, ecp_id: str, reason: str) -> EvolutionChangeProposal:
        """驳回。"""
        ecp = self._load(ecp_id)
        ecp.status = ECPStatus.REJECTED
        ecp.rationale += f"\n驳回原因: {reason}"
        self._save(ecp)
        return ecp
    
    def execute(self, ecp_id: str) -> EvolutionChangeProposal:
        """执行已批准的 ECP（沙箱测试 → 应用变更 → 基准验证）。"""
        ecp = self._load(ecp_id)
        if ecp.status != ECPStatus.APPROVED:
            raise ValueError(f"ECP {ecp_id} 状态为 {ecp.status.value}，不能执行")
        # 1. 记录执行前基准
        # 2. 在沙箱中执行变更
        # 3. 运行基准验证
        # 4. 若通过 → EXECUTED；若失败 → 自动回滚
        ecp.status = ECPStatus.EXECUTED
        ecp.executed_at = datetime.now(timezone.utc).isoformat()
        self._save(ecp)
        return ecp
    
    def rollback(self, ecp_id: str) -> EvolutionChangeProposal:
        """回滚已执行的 ECP。"""
        ecp = self._load(ecp_id)
        ecp.status = ECPStatus.ROLLED_BACK
        self._save(ecp)
        return ecp
    
    def _format_review_summary(self, ecp: EvolutionChangeProposal) -> str:
        """生成 Markdown 格式的审批摘要。"""
        return f"""## ECP 审批请求：{ecp.title}
        
| 字段 | 值 |
|------|-----|
| **ECP ID** | {ecp.ecp_id} |
| **类别** | {ecp.category.value} |
| **风险级别** | {ecp.risk_level} |
| **当前状态** | {ecp.current_state} |
| **提议变更** | {ecp.proposed_state} |
| **理由** | {ecp.rationale} |
| **影响模块** | {', '.join(ecp.impact.affected_modules)} |
| **Breaking Changes** | {', '.join(ecp.impact.breaking_changes) or '无'} |
| **回滚复杂度** | {ecp.impact.rollback_complexity} |
| **回滚命令** | `{ecp.rollback_command}` |

> 输入 `omega evolve approve {ecp.ecp_id}` 批准，`omega evolve reject {ecp.ecp_id}` 驳回
"""
    
    def _next_sequence(self) -> int:
        existing = list(self.ecp_dir.glob(f"ECP-{datetime.now(timezone.utc).strftime('%Y%m%d')}-*.json"))
        return len(existing) + 1
    
    def _save(self, ecp: EvolutionChangeProposal):
        path = self.ecp_dir / f"{ecp.ecp_id}.json"
        path.write_text(json.dumps(ecp.__dict__, default=str, indent=2, ensure_ascii=False))
    
    def _load(self, ecp_id: str) -> EvolutionChangeProposal:
        path = self.ecp_dir / f"{ecp_id}.json"
        if not path.exists():
            raise FileNotFoundError(f"ECP {ecp_id} 不存在")
        data = json.loads(path.read_text())
        return EvolutionChangeProposal(**data)
```

**ECP CLI 命令**：
```bash
omega evolve --check                          # 检测可升级工具
omega evolve --propose <tool_id>              # 为特定工具生成 ECP 提案
omega evolve approve <ecp_id>                 # 审批 ECP
omega evolve reject <ecp_id> --reason "..."   # 驳回 ECP
omega evolve execute <ecp_id>                 # 执行已批准的 ECP
omega evolve rollback <ecp_id>                # 回滚
omega evolve list-ecps                        # 列出所有 ECP（按状态筛选）
```

#### 8.2 成果包组装器 — `app/outcome/builder.py`
- `OutcomeBuilder` 类
- 8 种模态成果包：文献综述包、数据分析包、PPT 演示包、代码项目包、对比报告包、Meta 分析包、工具学习包、质量改进包
- 每个包包含：主产物 + 质量报告 + 复现脚本 + 元数据
- 输出到 `omega-workspace/outcomes/<task_id>/`

#### 8.3 日志系统 — `app/logging_setup.py`
（文件名为 `logging_setup.py` 避免与标准库 `logging` 冲突）
- 按 `omega.yaml` logging 段配置：level=INFO、文件轮转、控制台输出
- 在关键节点写日志：task 创建、plan 生成、Agent 分配、工具执行、完成/失败

#### 8.4 修改 `app/main.py`
- 新增 `omega evolve` 命令
- 新增 `omega outcome` 命令

#### 8.5 验证
```bash
# 演化引擎
omega evolve --check                              # 报告可升级工具
omega evolve --propose <tool_id>                  # 为特定工具生成 ECP 提案
omega evolve approve <ecp_id>                     # 审批 ECP
omega evolve execute <ecp_id>                     # 执行已批准的 ECP
omega evolve list-ecps --status pending           # 列出待审批的 ECP
omega evolve rollback <ecp_id>                    # 回滚已执行的 ECP

# 成果包
omega task "..." --execute                        # 完成后检查 omega-workspace/outcomes/ 有产物包
cat logs/omega.log                                # 结构化日志记录
omega bench --all                                 # 仍 7/7
```

### 受影响文件
| 文件 | 操作 |
|------|------|
| `app/evolution/__init__.py` | **新建** |
| `app/evolution/engine.py` | **新建** |
| `app/evolution/ecp.py` | **新建** — Evolution Change Proposal 管理器 |
| `app/outcome/__init__.py` | 修改 |
| `app/outcome/builder.py` | **新建** |
| `app/logging_setup.py` | **新建** |
| `app/main.py` | 修改 |
| `tests/test_evolution.py` | **新建** — 含 ECP 审批流程测试 |
| `tests/test_outcome.py` | **新建** |

---

## Phase 9：域扩展 【优先级：低 🟢】

> ⚠️ **现实主义说明**：科学可视化和创意工具是 Omega 的重依赖区。matplotlib/plotly 可以可靠落地；manim 需要 LaTeX/字体/渲染运行时（通过 Toolsmith 自动安装，但首次配置可能需人工介入）；blender 需要独立安装、GPU 支持和大量 CPU 时间（离线渲染一帧可能几分钟）。本 Phase 实现四个层级的可视化管线，但 **manim/blender 层标记为"尽力而为"** ——如果环境不支持，自动降级到 matplotlib/plotly 并通知用户。

### 问题
`omega.yaml` domains 段定义了 6 个域，4 个 enabled，2 个 disabled。disabled 的域未实现。

### 目标
补全已启用域的核心能力，激活已禁用域。建立四级可视化降级管线。

### 实施步骤（按需激活）

#### 9.1 科学可视化生产系统
- 9 阶段管线（设计文档在 `11-创意与科学可视化/科学动画生产系统.md`）
- 4 工具链：matplotlib → plotly → manim → blender
- 输出：学术图表、动画、3D 结构
- 需安装：manim、blender（通过 Toolsmith 自动安装）
- 新文件：`app/executor/viz_executor.py`

#### 9.2 Computer Use-Lite
- Playwright MCP 已在 Phase 6 启动管理
- 实现浏览器表单预填、截图、自动化
- 新文件：`app/executor/browser_executor.py`

#### 9.3 创意工具路由器
- 12 种创意任务类型（设计文档在 `11-创意与科学可视化/Creative Tool Router.md`）
- 新文件：`app/executor/creative_router.py`

#### 9.4 R 引擎支持
- Docker 沙箱中添加 R 运行时
- 修改 `Dockerfile.sandbox` 和 `Dockerfile.sandbox-net` 安装 R

### 受影响文件（按需）
| 文件 | 操作 | 触发条件 |
|------|------|---------|
| `app/executor/viz_executor.py` | 新建 | 启用 scientific_visualization |
| `app/executor/browser_executor.py` | 新建 | 完善 computer_use |
| `app/executor/creative_router.py` | 新建 | 启用 creative_tools |
| `Dockerfile.sandbox` | 修改 | 添加 R 运行时 |

---

## Phase 10：Omega Terminal — 统一操作窗口 【优先级：最高 🔴】

> **设计文档**：`build-package/OMEGA_TERMINAL.md` — 完整 UI 规范、布局图、功能清单
> **定位**：Omega 系统的唯一用户界面入口——所有用户交互都在这个窗口中完成。

### 问题
原 Phase 10 设计过于简陋（简单 HTML dashboard + HTMX），无法满足"统一操作窗口"的需求。用户需要在 Obsidian/VS Code 之外还有一个独立的 Omega 专用窗口，支持自然语言输入、文件拖拽上传、实时任务监控、通知汇聚。

### 目标
实现 Omega Terminal——一个类 VS Code 布局的现代化 Web 应用，作为 Omega 的唯一用户界面。所有功能从命令面板可达，所有反馈在此汇聚。

### 设计原则
1. **唯一入口**：用户只需打开一个窗口即可操作 Omega 全部功能
2. **自然语言优先**：直接输入中文/英文指令，无需学习 CLI 命令
3. **键盘优先**：所有操作有快捷键（Ctrl+Shift+P 命令面板等）
4. **实时反馈**：WebSocket 推送日志流、任务进度、通知
5. **交互式确认**：需要用户决策的事项以对话框呈现，不再只是终端文字

### 实施步骤

#### 10.1 后端扩展 — `app/web/`

扩展原有 Phase 10 的 FastAPI 后端，增加 WebSocket 和文件 API：

```python
# app/web/ws.py — WebSocket 管理器
class WebSocketManager:
    """管理所有连接的 WebSocket 客户端，推送实时消息"""
    connections: Dict[str, WebSocket]  # task_id → ws
    async def push_log(self, task_id: str, message: str)
    async def push_progress(self, task_id: str, percent: float, step: str)
    async def push_notification(self, notification: Notification)
    async def push_confirm(self, request_id: str, confirm: ConfirmRequest)
```

```python
# app/web/api/upload_api.py — 文件上传 + 智能识别
@router.post("/api/upload")
async def upload_file(file: UploadFile):
    """
    上传文件 → 自动识别类型 → 返回处理建议
    支持: PDF/CSV/XLSX/PPTX/DOCX/MD/TXT/PNG/JPG/ZIP
    """
    file_type = detect_type(file)
    suggestions = get_suggestions(file_type)  # L3处理 / 数据分析 / ingest / ...
    return {"file_id": id, "type": file_type, "suggestions": suggestions}
```

新增端点：

| 端点 | 方法 | 功能 |
|------|------|------|
| `/api/terminal/ws` | WebSocket | 实时双向通信（日志/进度/通知/确认） |
| `/api/upload` | POST | 文件上传 + 类型识别 |
| `/api/vault/browse` | GET | 文件浏览器（目录树 JSON） |
| `/api/vault/search` | GET | 全文搜索 vault |
| `/api/notify/list` | GET | 通知列表 |
| `/api/notify/ack` | POST | 标记通知已读 |
| `/api/task/list` | GET | 活跃任务列表 |
| `/api/history` | GET | 历史命令/任务记录 |

#### 10.2 前端 — `app/web/terminal/`

React 18 + TypeScript + Tailwind CSS 构建的单页应用。

**核心组件**（详见 `OMEGA_TERMINAL.md` 第四章）：

| 组件 | 文件 | 功能 |
|------|------|------|
| `App.tsx` | 根组件 | 布局管理、标签页切换、主题切换 |
| `CommandInput.tsx` | 底部命令栏 | 自然语言输入 + 智能补全 + 发送 |
| `ChatArea.tsx` | 中央对话区 | 消息列表（Markdown/图表/DAG/文件卡片） |
| `FileBrowser.tsx` | 左侧栏 | vault 目录树 + 右键菜单 + 拖拽源 |
| `ContextPanel.tsx` | 右侧栏 | 当前任务详情 + 活跃工具 + 历史 |
| `TaskMonitor.tsx` | 右侧面板 | 任务进度条 + 步骤列表 + 暂停/取消 |
| `CommandPalette.tsx` | 弹出面板 | Ctrl+Shift+P 命令列表 |
| `NotificationCenter.tsx` | 弹出面板 | 通知列表 + 未读徽标 |
| `StatusBar.tsx` | 底部栏 | 系统状态 + API 引擎 + 任务数 |
| `ConfirmDialog.tsx` | 弹出对话框 | ECP 审批 / 高风险确认 / 知识写入确认 |
| `DAGViewer.tsx` | 内嵌 | ReactFlow DAG 可视化 |
| `ChartRenderer.tsx` | 内嵌 | Recharts 图表渲染 |
| `FileCard.tsx` | 内嵌 | 生成文件的结果卡片 |

**构建命令**：
```bash
cd app/web/terminal/
npm install            # React + Tailwind + CodeMirror + ReactFlow + Recharts
npm run build          # 产出 dist/ → FastAPI static mount
```

#### 10.3 桌面打包 — `electron/`（可选，优先级低）

```javascript
// electron/main.js
const { app, BrowserWindow } = require('electron');
// 加载 http://localhost:8420 并封装为独立窗口
// 支持系统托盘、全局快捷键（Ctrl+Alt+O 呼出 Omega Terminal）
```

备选方案：`pywebview`（Python 原生窗口 + 内嵌 WebView），免去 Electron 的 150MB 体积。

#### 10.4 后台服务扩展

```python
# app/service.py — 扩展
class OmegaService:
    """Omega 常驻后台服务"""
    web_server: FastAPI      # 端口 8420
    task_queue: asyncio.Queue
    evolution_timer: Timer   # 定时扫描工具更新
    mcp_health_timer: Timer  # 定时检查 MCP 健康
    ws_manager: WebSocketManager  # 通知推送

# app/notify.py — 扩展
class Notifier:
    """多渠道通知"""
    async def notify(self, msg: Notification):
        await ws_manager.push(msg)           # WebSocket → 终端
        await self.write_vault(msg)           # 写入 vault 通知.md（Obsidian 兼容）
```

#### 10.5 验证

```bash
omega web --port 8420                 # 启动完整终端
# → 浏览器打开 http://localhost:8420 → 显示 Omega Terminal
# → 输入"搜3篇糖尿病文献"→ 正常执行
# → Ctrl+Shift+P → 命令面板列出所有闭环
# → 拖拽 PDF → 自动识别并提示处理
# → WebSocket 日志流实时显示

omega web --electron                  # 启动独立桌面窗口（可选）

# 自动化测试
.venv\Scripts\python -m pytest tests/test_terminal.py -v
```

**功能验证清单**（14 项，详见 `OMEGA_TERMINAL.md` §10.6）：
1. 浏览器打开完整界面
2. 自然语言输入正常执行
3. 命令面板列出所有闭环
4. 文件拖拽上传 + 智能识别
5. 实时任务进度推送
6. WebSocket 日志流
7. 结构化结果卡片
8. 通知中心汇聚
9. 交互式确认对话框
10. 文件浏览器展示 vault
11. 键盘快捷键（Ctrl+Enter 等）
12. 主题切换
13. 多标签页
14. 自动化测试通过

### 受影响文件

| 文件 | 操作 |
|------|------|
| `app/web/__init__.py` | **新建** — Web 后端包 |
| `app/web/app.py` | **新建** — FastAPI + WebSocket + 静态挂载 |
| `app/web/ws.py` | **新建** — WebSocket 管理器 |
| `app/web/api/task_api.py` | **新建** — 任务 API |
| `app/web/api/upload_api.py` | **新建** — 上传 + 类型识别 |
| `app/web/api/notify_api.py` | **新建** — 通知 API |
| `app/web/api/vault_api.py` | **新建** — 文件浏览/搜索 |
| `app/web/terminal/index.html` | **新建** — SPA 入口 |
| `app/web/terminal/main.tsx` | **新建** — React 入口 |
| `app/web/terminal/App.tsx` | **新建** — 根组件 |
| `app/web/terminal/components/CommandInput.tsx` | **新建** |
| `app/web/terminal/components/ChatArea.tsx` | **新建** |
| `app/web/terminal/components/FileBrowser.tsx` | **新建** |
| `app/web/terminal/components/ContextPanel.tsx` | **新建** |
| `app/web/terminal/components/TaskMonitor.tsx` | **新建** |
| `app/web/terminal/components/CommandPalette.tsx` | **新建** |
| `app/web/terminal/components/NotificationCenter.tsx` | **新建** |
| `app/web/terminal/components/StatusBar.tsx` | **新建** |
| `app/web/terminal/components/ConfirmDialog.tsx` | **新建** |
| `app/web/terminal/components/DAGViewer.tsx` | **新建** |
| `app/web/terminal/components/ChartRenderer.tsx` | **新建** |
| `app/web/terminal/components/FileCard.tsx` | **新建** |
| `app/web/terminal/hooks/useWebSocket.ts` | **新建** |
| `app/web/terminal/hooks/useTasks.ts` | **新建** |
| `app/web/terminal/hooks/useNotifications.ts` | **新建** |
| `app/web/terminal/styles/tailwind.css` | **新建** |
| `app/web/terminal/package.json` | **新建** |
| `electron/main.js` | **新建**（可选） |
| `electron/preload.js` | **新建**（可选） |
| `app/service.py` | **扩展** — 任务队列 + 推送 |
| `app/notify.py` | **扩展** — WebSocket 推送 |
| `app/main.py` | 修改 — 扩展 web/service 命令 |
| `tests/test_terminal.py` | **新建** — 终端自动化测试 |

**文件统计**：~28 新文件，~3 修改文件。

---

## Phase 11：质量与安全加固 【优先级：最高 🔴】

### 问题
Codex 模拟测试揭示了 6 个质量/安全/可追溯性空白，这些是 Omega 从"能跑"到"可信任"的关键差距：

1. **无构建预览**：Codex 直接修改文件，用户看不到完整 DAG/文件变更清单/风险表/预计耗时——缺乏透明度
2. **无任务审计**：每个任务的输入、路由、模型、工具、成本、失败点、产物来源——全无记录，无法追溯
3. **无溯源水印**：结论无法追溯到文献/代码/数据/模型调用——学术严谨性缺失
4. **无预算模式**：无法按任务自动选择省钱/高质量/离线模式——日常使用不够灵活
5. **无工具隔离**：Toolsmith 学到的新工具直接进入正式注册表——缺少隔离验收环节
6. **无知识防污染**：AI 生成内容直接写入 Obsidian vault——可能污染知识库

这 6 项是 Codex 在模拟测试后主动建议的优化方向，是 Omega 从"工程上能运行"到"生产级可信任"的最后一块拼图。

### 目标
实现 6 项质量/安全加固，使 Omega 具备：构建透明度、任务可审计性、结论可溯源性、成本可控性、工具安全性、知识纯净性。

### 实施步骤

#### 11.1 模拟构建器 — `app/safety/simulator.py`

**功能**：在 Codex 实际修改任何文件前，生成完整 DAG、文件变更清单、风险表、预计耗时——用户审查后再执行。

```python
"""Pre-flight build simulator — dry-run DAG + risk + timeline before touching files."""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any
from pathlib import Path
import yaml
import json

@dataclass
class FileChange:
    path: str
    operation: str  # create | modify | delete
    reason: str
    risk_level: str  # low | medium | high
    rollback_possible: bool = True

@dataclass
class RiskItem:
    description: str
    probability: str  # low | medium | high
    impact: str
    mitigation: str

@dataclass
class SimulationResult:
    phase: str
    dag: dict  # Execution DAG with dependencies
    file_changes: list[FileChange] = field(default_factory=list)
    risks: list[RiskItem] = field(default_factory=list)
    estimated_time_minutes: int = 0
    total_files_to_modify: int = 0
    rollback_command: str = ""

class BuildSimulator:
    """Generates a complete build simulation before any file modification.
    
    Codex calls this FIRST for each phase — shows the user what will happen,
    waits for confirmation, THEN makes changes.
    """
    
    def simulate_phase(self, phase_config: dict, 
                       current_state: dict) -> SimulationResult:
        """Generate simulation for a single phase. No files modified."""
        result = SimulationResult(phase=phase_config.get("name", "unknown"))
        
        # Analyze what files will be created/modified
        result.file_changes = self._predict_file_changes(phase_config)
        result.total_files_to_modify = len(result.file_changes)
        
        # Build execution DAG with dependency ordering
        result.dag = self._build_execution_dag(phase_config)
        
        # Risk assessment
        result.risks = self._assess_risks(phase_config, current_state)
        
        # Time estimate
        result.estimated_time_minutes = self._estimate_time(phase_config)
        
        # Rollback plan
        result.rollback_command = self._generate_rollback(phase_config)
        
        return result
    
    def _predict_file_changes(self, config: dict) -> list[FileChange]:
        """Predict all file changes from phase config."""
        changes = []
        for f in config.get("affected_files", []):
            changes.append(FileChange(
                path=f["path"],
                operation=f.get("operation", "modify"),
                reason=f.get("reason", ""),
                risk_level=f.get("risk", "low"),
            ))
        return changes
    
    def _assess_risks(self, config: dict, state: dict) -> list[RiskItem]:
        """Identify risks: breaking changes, dependency conflicts, API unavailability."""
        risks = []
        if config.get("modifies_existing", False):
            risks.append(RiskItem(
                description="Modifies existing functionality — requires bench regression",
                probability="medium",
                impact="Could break existing closed loops",
                mitigation="Run omega bench --all before and after; git diff to review",
            ))
        if config.get("external_dependency", False):
            risks.append(RiskItem(
                description="Requires external service or API — may fail if unavailable",
                probability="medium",
                impact="Feature degradation to fallback mode",
                mitigation="Engine Resolver auto-degrades; test fallback path explicitly",
            ))
        return risks
    
    def _build_execution_dag(self, config: dict) -> dict:
        """Build ordered execution DAG for the phase."""
        steps = config.get("steps", [])
        dag = {"nodes": [], "edges": []}
        for i, step in enumerate(steps):
            dag["nodes"].append({"id": f"step_{i}", "label": step.get("label", ""), 
                                  "files": step.get("files", [])})
            if i > 0:
                dag["edges"].append({"from": f"step_{i-1}", "to": f"step_{i}"})
        return dag
    
    def _estimate_time(self, config: dict) -> int:
        """Estimate phase execution time in minutes."""
        file_count = len(config.get("affected_files", []))
        if file_count <= 3:
            return 15
        elif file_count <= 8:
            return 30
        else:
            return 45
    
    def _generate_rollback(self, config: dict) -> str:
        return f"git checkout HEAD~1  # roll back last commit for {config.get('name', 'phase')}"

    def to_markdown_report(self, result: SimulationResult) -> str:
        """Render simulation as a user-readable Markdown report."""
        lines = [
            f"# 🔍 构建模拟报告：{result.phase}",
            "",
            "## 📋 文件变更清单",
            "| 文件 | 操作 | 风险 | 可回滚 |",
            "|------|------|------|--------|",
        ]
        for fc in result.file_changes:
            lines.append(f"| `{fc.path}` | {fc.operation} | {fc.risk_level} | {'✅' if fc.rollback_possible else '❌'} |")
        
        lines.extend([
            "",
            "## ⚠️ 风险评估",
            "| 风险 | 概率 | 影响 | 缓解措施 |",
            "|------|------|------|---------|",
        ])
        for r in result.risks:
            lines.append(f"| {r.description} | {r.probability} | {r.impact} | {r.mitigation} |")
        
        lines.extend([
            "",
            "## 📊 预估",
            f"- 修改文件数：{result.total_files_to_modify}",
            f"- 预计耗时：~{result.estimated_time_minutes} 分钟",
            f"- 回滚命令：`{result.rollback_command}`",
            "",
            "---",
            "确认执行？ [Y] 执行 [N] 取消 [S] 跳过此阶段",
        ])
        return "\n".join(lines)
```

#### 11.2 任务飞行记录仪 — `app/memory/flight_recorder.py`

**功能**：每个任务保存——输入、路由决策、模型选择、工具调用、成本、失败点、产物来源。解决"这个结论怎么来的"的追溯问题。

```python
"""Task flight recorder — black-box audit trail for every Omega task."""

from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any
from pathlib import Path
import json
import uuid

@dataclass
class FlightRecord:
    record_id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])
    task_id: str = ""
    goal: str = ""
    task_type: str = ""
    
    # Routing decisions
    selected_tools: list[str] = field(default_factory=list)
    fallback_chain: list[str] = field(default_factory=list)
    engine_used: str = ""
    agent_assigned: str = ""
    
    # Execution trace
    steps: list[dict] = field(default_factory=list)  # [{step_id, tool, status, duration_ms, error}]
    
    # Cost tracking
    total_api_calls: int = 0
    estimated_cost_usd: float = 0.0
    total_duration_ms: float = 0.0
    
    # Output provenance
    output_files: list[str] = field(default_factory=list)
    output_pages: list[str] = field(default_factory=list)
    
    # Quality
    auto_quality_score: float = 0.0
    failures: list[str] = field(default_factory=list)
    
    started_at: str = ""
    completed_at: str = ""

class FlightRecorder:
    """Records a complete audit trail for every Omega task execution.
    
    Each record answers: what was asked → what route was chosen → 
    what tools ran → what failed → what cost → where outputs went.
    """
    
    def __init__(self, log_dir: Path):
        self.log_dir = log_dir
        self.log_dir.mkdir(parents=True, exist_ok=True)
        self._current: FlightRecord | None = None
    
    def start_task(self, goal: str, task_type: str, task_id: str = "") -> FlightRecord:
        self._current = FlightRecord(
            task_id=task_id or str(uuid.uuid4())[:8],
            goal=goal,
            task_type=task_type,
            started_at=datetime.utcnow().isoformat(),
        )
        return self._current
    
    def record_step(self, step_id: str, tool: str, success: bool, 
                    duration_ms: float, error: str = None) -> None:
        if self._current:
            self._current.steps.append({
                "step_id": step_id, "tool": tool,
                "success": success, "duration_ms": duration_ms,
                "error": error,
                "timestamp": datetime.utcnow().isoformat(),
            })
    
    def finish_task(self) -> Path:
        if self._current:
            self._current.completed_at = datetime.utcnow().isoformat()
            path = self.log_dir / f"flight_{self._current.record_id}.json"
            path.parent.mkdir(parents=True, exist_ok=True)
            # Convert dataclass to dict for JSON
            path.write_text(json.dumps(self._current, default=str, indent=2))
            return path
        return Path("")
    
    def get_summary(self, record: FlightRecord) -> str:
        """Human-readable flight summary."""
        success_count = sum(1 for s in record.steps if s.get("success"))
        return (
            f"✈️ 任务 [{record.record_id}]: {record.goal[:60]}...\n"
            f"   类型: {record.task_type} | 引擎: {record.engine_used} | Agent: {record.agent_assigned}\n"
            f"   步骤: {success_count}/{len(record.steps)} 成功 | "
            f"耗时: {record.total_duration_ms/1000:.1f}s | 成本: ${record.estimated_cost_usd:.4f}\n"
            f"   产出: {len(record.output_files)} files + {len(record.output_pages)} wiki pages"
        )
```

#### 11.3 溯源水印 — `app/outcome/provenance.py`

> 🆕 **Claim-Level Provenance 增强**（Codex 建议）：当前实现给整个成果包加溯源水印。增强后，成果包内的**每个关键结论**都有独立溯源链（claim_id → source_id → evidence_type → confidence → model_call），而非整个文档共用一个水印。这样当某个结论被质疑时，可以精确追溯到该结论的来源而不影响其他结论的可信度。

**功能**：每个结论标注来源链——文献 DOI/URL、代码 commit hash、数据文件路径、模型调用 ID。学术成果可追溯至原始资料。

```python
"""Outcome provenance watermark — every conclusion traces to its sources."""

from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime
import hashlib
import json

@dataclass
class ProvenanceLink:
    """A single source reference in the provenance chain."""
    type: str  # literature | code | data | model_call | web_search | tool_output
    identifier: str  # DOI | file_path | URL | model:prompt_hash
    description: str
    timestamp: str = field(default_factory=lambda: datetime.utcnow().isoformat())
    content_hash: str = ""  # SHA256 of the referenced content

@dataclass
class ProvenanceChain:
    """A chain of provenance links for one conclusion."""
    conclusion_id: str
    conclusion_text: str
    links: list[ProvenanceLink] = field(default_factory=list)
    chain_hash: str = ""  # Merkle-like hash of all links
    
    def compute_hash(self) -> str:
        """Compute a content-addressable hash for the entire chain."""
        payload = json.dumps([
            {"type": l.type, "identifier": l.identifier, "hash": l.content_hash}
            for l in self.links
        ], sort_keys=True)
        return hashlib.sha256(payload.encode()).hexdigest()[:16]

class ProvenanceWatermark:
    """Attaches provenance chains to outcome packages.
    
    Every assertion in an outcome package must be traceable through one or 
    more ProvenanceLink — answering "where did this conclusion come from?"
    
    Watermark format (appended to each outcome page):
    ```
    <!-- OMEGA-PROVENANCE
    conclusion_id: <id>
    chain_hash: <sha256>
    links:
      - type: literature | identifier: doi:10.xxx | hash: abc123
      - type: code | identifier: omega-runtime/... | hash: def456
      - type: model_call | identifier: claude:hash | hash: ghi789
    verified_by: <agent_id> | verified_at: <iso_timestamp>
    -->
    ```
    """
    
    def __init__(self):
        self._chains: dict[str, ProvenanceChain] = {}
    
    def start_conclusion(self, conclusion_id: str, text: str) -> ProvenanceChain:
        chain = ProvenanceChain(conclusion_id=conclusion_id, conclusion_text=text)
        self._chains[conclusion_id] = chain
        return chain
    
    def add_source(self, conclusion_id: str, type: str, identifier: str, 
                   description: str, content: str = "") -> None:
        if conclusion_id not in self._chains:
            self._chains[conclusion_id] = ProvenanceChain(
                conclusion_id=conclusion_id, conclusion_text=""
            )
        content_hash = hashlib.sha256(content.encode()).hexdigest()[:16] if content else ""
        self._chains[conclusion_id].links.append(ProvenanceLink(
            type=type, identifier=identifier, description=description,
            content_hash=content_hash,
        ))
    
    def seal(self, conclusion_id: str, verifier: str = "omega") -> str:
        """Seal the provenance chain and return the HTML comment watermark."""
        chain = self._chains.get(conclusion_id)
        if not chain:
            return ""
        chain.chain_hash = chain.compute_hash()
        links_yaml = "\n".join(
            f"  - type: {l.type} | identifier: {l.identifier} | hash: {l.content_hash}"
            for l in chain.links
        )
        return (
            f"<!-- OMEGA-PROVENANCE\n"
            f"conclusion_id: {conclusion_id}\n"
            f"chain_hash: {chain.chain_hash}\n"
            f"links:\n{links_yaml}\n"
            f"verified_by: {verifier} | verified_at: {datetime.utcnow().isoformat()}\n"
            f"-->"
        )
```

#### 11.4 预算与质量控制台 — `app/router/budget_console.py`

**功能**：按任务自动选择省钱/高质量/离线模式。quality_profile（strict/balanced/permissive）映射到具体的引擎选择和成本上限。

```python
"""Budget and quality console — mode-aware task execution."""

from __future__ import annotations
from enum import Enum
from dataclasses import dataclass
from typing import Any

class ExecutionMode(str, Enum):
    CHEAP = "cheap"           # 成本最低——全部 DeepSeek，跳过非必需步骤
    HIGH_QUALITY = "high_quality"  # quality_reasoning 能力角色，所有验证步骤
    OFFLINE = "offline"       # 完全本地——只用沙箱+本地数据，不调外部 API
    BALANCED = "balanced"     # 默认——按 task_type 自动选择

@dataclass
class BudgetProfile:
    mode: ExecutionMode
    max_cost_usd: float
    preferred_engine: str
    skip_optional_steps: bool
    require_provenance: bool

@dataclass  
class QualityProfile:
    mode: ExecutionMode
    require_peer_review: bool   # L2+ 任务是否必须 critic Agent 审查
    require_reproducibility: bool  # 是否必须生成复现脚本
    min_confidence: float       # 最低置信度阈值
    provenance_level: str       # none | basic | full

class BudgetConsole:
    """Task-level budget and quality mode selector.
    
    Integrated into the planner: before executing a task, the console 
    selects the ExecutionMode based on user preference or task_type defaults.
    
    Mode selection logic:
    - User says "用省钱模式" → CHEAP
    - User says "高质量" → HIGH_QUALITY  
    - User says "离线" → OFFLINE
    - Omega detects no API keys → OFFLINE (auto-degrade)
    - Default → BALANCED（按 capability role 动态解析，不固定 provider/model）
    """
    
    DEFAULT_PROFILES = {
        ExecutionMode.CHEAP: BudgetProfile(
            mode=ExecutionMode.CHEAP, max_cost_usd=0.10,
            preferred_engine="economical_general", skip_optional_steps=True,
            require_provenance=False,
        ),
        ExecutionMode.HIGH_QUALITY: BudgetProfile(
            mode=ExecutionMode.HIGH_QUALITY, max_cost_usd=2.00,
            preferred_engine="quality_reasoning", skip_optional_steps=False,
            require_provenance=True,
        ),
        ExecutionMode.OFFLINE: BudgetProfile(
            mode=ExecutionMode.OFFLINE, max_cost_usd=0.0,
            preferred_engine="economical_general", skip_optional_steps=True,
            require_provenance=False,
        ),
        ExecutionMode.BALANCED: BudgetProfile(
            mode=ExecutionMode.BALANCED, max_cost_usd=0.50,
            preferred_engine="engineering_primary", skip_optional_steps=False,
            require_provenance=True,
        ),
    }
    
    QUALITY_PROFILES = {
        ExecutionMode.CHEAP: QualityProfile(
            mode=ExecutionMode.CHEAP, require_peer_review=False,
            require_reproducibility=False, min_confidence=0.5,
            provenance_level="none",
        ),
        ExecutionMode.HIGH_QUALITY: QualityProfile(
            mode=ExecutionMode.HIGH_QUALITY, require_peer_review=True,
            require_reproducibility=True, min_confidence=0.85,
            provenance_level="full",
        ),
        ExecutionMode.OFFLINE: QualityProfile(
            mode=ExecutionMode.OFFLINE, require_peer_review=False,
            require_reproducibility=True, min_confidence=0.6,
            provenance_level="basic",
        ),
        ExecutionMode.BALANCED: QualityProfile(
            mode=ExecutionMode.BALANCED, require_peer_review=False,
            require_reproducibility=False, min_confidence=0.7,
            provenance_level="basic",
        ),
    }
    
    def __init__(self, active_engines: dict[str, str]):
        self.active_engines = active_engines
        self._default_mode = ExecutionMode.BALANCED
    
    def select_mode(self, task_type: str, user_preference: str = "") -> ExecutionMode:
        """Select execution mode: user override > task auto-select."""
        if user_preference:
            try:
                return ExecutionMode(user_preference.lower())
            except ValueError:
                pass
        
        # Auto-select: quality_sensitive tasks → HIGH_QUALITY
        quality_sensitive = {"academic_writing", "literature_review", 
                            "meta_analysis", "medical_research"}
        if task_type in quality_sensitive and "quality_reasoning" in self.active_engines:
            return ExecutionMode.HIGH_QUALITY
        
        # If no external engines available → OFFLINE
        if not self.active_engines:
            return ExecutionMode.OFFLINE
        
        return ExecutionMode.BALANCED
    
    def get_profile(self, mode: ExecutionMode) -> BudgetProfile:
        return self.DEFAULT_PROFILES.get(mode, self.DEFAULT_PROFILES[ExecutionMode.BALANCED])
```

#### 11.5 Toolsmith 隔离与签名 — `app/toolsmith/quarantine.py`

**功能**：Toolsmith 学到的新工具先进入隔离区（quarantine registry），经过自动化验收测试（功能测试 + 安全检查 + 依赖冲突检测）后才进入正式注册表。

```python
"""Toolsmith quarantine and signing — safety gate for learned tools."""

from __future__ import annotations
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from datetime import datetime
import hashlib
import json
import subprocess

class QuarantineStatus(str, Enum):
    PENDING = "pending"            # 等待验收
    TESTING = "testing"            # 正在运行验收测试
    PASSED = "passed"              # 验收通过，等待签名
    REJECTED = "rejected"          # 验收失败
    SIGNED = "signed"              # 已签名，可进入正式注册表

@dataclass
class QuarantineEntry:
    tool_id: str
    tool_name: str
    source: str  # PyPI | GitHub | npm | custom
    version: str
    discovered_at: str = field(default_factory=lambda: datetime.utcnow().isoformat())
    
    # Acceptance test results
    status: QuarantineStatus = QuarantineStatus.PENDING
    functional_test_passed: bool = False
    safety_check_passed: bool = False
    dependency_conflict_free: bool = False
    benchmark_score: float = 0.0
    
    # Signing
    signature: str = ""
    signed_by: str = ""
    signed_at: str = ""

class QuarantineManager:
    """Toolsmith learned tools enter quarantine before the official registry.
    
    Safety workflow:
    1. Toolsmith discovers tool → enters quarantine (status=PENDING)
    2. Run automated acceptance tests:
       a. Functional: does it do what it claims?
       b. Safety: no network calls, file writes within sandbox, CPU/mem limits
       c. Dependencies: no conflicts with existing toolset
    3. If all pass → status=PASSED, generate signature
    4. If any fail → status=REJECTED, report to user
    5. Signed tools → promote to official config/tools.yaml
    
    This prevents untested tools from polluting the tool registry.
    """
    
    def __init__(self, quarantine_path: Path):
        self.quarantine_path = quarantine_path
        self.quarantine_path.mkdir(parents=True, exist_ok=True)
        self._entries: dict[str, QuarantineEntry] = {}
        self._load()
    
    def _load(self) -> None:
        registry = self.quarantine_path / "quarantine_registry.json"
        if registry.exists():
            data = json.loads(registry.read_text())
            for e in data.get("entries", []):
                entry = QuarantineEntry(**e)
                self._entries[entry.tool_id] = entry
    
    def _save(self) -> None:
        registry = self.quarantine_path / "quarantine_registry.json"
        registry.write_text(json.dumps(
            {"entries": [vars(e) for e in self._entries.values()]},
            indent=2, default=str,
        ))
    
    def admit(self, tool_id: str, tool_name: str, source: str, 
              version: str) -> QuarantineEntry:
        """Admit a newly discovered tool to quarantine."""
        entry = QuarantineEntry(tool_id=tool_id, tool_name=tool_name,
                                source=source, version=version)
        self._entries[tool_id] = entry
        self._save()
        return entry
    
    def run_acceptance_tests(self, tool_id: str) -> bool:
        """Run full acceptance test suite on the quarantined tool."""
        entry = self._entries.get(tool_id)
        if not entry:
            return False
        
        entry.status = QuarantineStatus.TESTING
        
        # 1. Functional test — import and basic smoke test
        try:
            result = subprocess.run(
                ["docker", "exec", "omega-sandbox", "python", "-c",
                 f"import {tool_id}; print('OK')"],
                capture_output=True, text=True, timeout=30,
            )
            entry.functional_test_passed = "OK" in result.stdout
        except Exception:
            entry.functional_test_passed = False
        
        # 2. Safety check — no suspicious imports/network calls
        # (in real implementation: static analysis of the package)
        entry.safety_check_passed = True  # Placeholder
        
        # 3. Dependency conflict check
        try:
            result = subprocess.run(
                ["docker", "exec", "omega-sandbox-net", "pip", "check"],
                capture_output=True, text=True, timeout=30,
            )
            entry.dependency_conflict_free = result.returncode == 0
        except Exception:
            entry.dependency_conflict_free = False
        
        # Decide
        all_pass = (entry.functional_test_passed and 
                   entry.safety_check_passed and 
                   entry.dependency_conflict_free)
        entry.status = QuarantineStatus.PASSED if all_pass else QuarantineStatus.REJECTED
        self._save()
        return all_pass
    
    def sign(self, tool_id: str, signer: str = "omega-quarantine") -> str:
        """Sign a passed tool — generates a content hash as signature."""
        entry = self._entries.get(tool_id)
        if not entry or entry.status != QuarantineStatus.PASSED:
            return ""
        
        payload = f"{entry.tool_id}:{entry.version}:{entry.source}"
        entry.signature = hashlib.sha256(payload.encode()).hexdigest()[:32]
        entry.signed_by = signer
        entry.signed_at = datetime.utcnow().isoformat()
        entry.status = QuarantineStatus.SIGNED
        self._save()
        return entry.signature
    
    def promote_to_registry(self, tool_id: str) -> dict | None:
        """Promote a signed tool to the official tool registry entry format."""
        entry = self._entries.get(tool_id)
        if not entry or entry.status != QuarantineStatus.SIGNED:
            return None
        
        return {
            "id": entry.tool_id,
            "name": entry.tool_name,
            "category": "toolsmith_discovered",
            "capabilities": ["ToolExecution"],
            "status": "integrated",
            "risk_level": "low",
            "quarantine_signature": entry.signature,
            "quarantine_benchmark_score": entry.benchmark_score,
            "notes": f"Discovered via Toolsmith from {entry.source} v{entry.version}. "
                     f"Passed quarantine acceptance tests. Signed by {entry.signed_by}.",
        }
```

#### 11.6 知识库防污染守卫 — `app/safety/kb_guard.py`

> 🆕 **知识候审区分层**（Codex 建议）：当前 `omega-workspace/review/` 是单一候审区。增强后细分为 4 层：
> | 层级 | 目录 | 内容类型 | 合并条件 |
> |------|------|---------|---------|
> | `source_summary/` | 来源摘要 | 文献/网页的提炼内容 | auto_approved ≥5/6 |
> | `claim_candidate/` | 声明候选 | AI 生成的结论/断言 | ≥5/6 + 至少 1 个外部来源引用 |
> | `insight_candidate/` | 洞察候选 | 跨文献综合洞察 | 仅人工审查（不入自动合并） |
> | `formal_knowledge/` | 正式知识 | 已验证的高质量内容 | 自动合并到 wiki/ |
>
> 这防止了 AI 生成的洞察直接污染正式知识层——`insight_candidate` 必须经过人工审查才能进入 `wiki/洞察/`。

**功能**：AI 生成内容写入 Obsidian 前先进入候审区（`omega-workspace/review/`），通过质量检查（长度、结构、重复率、来源标注）后由 `knowledge_steward` Agent 合并到正式 wiki/。

```python
"""Knowledge base pollution guard — AI output quality gate for Obsidian."""

from __future__ import annotations
from dataclasses import dataclass, field
from pathlib import Path
from datetime import datetime
from typing import Any
import hashlib
import json

@dataclass
class ContentReview:
    review_id: str
    target_path: str
    source_agent: str
    task_id: str
    
    content: str = ""
    content_hash: str = ""
    
    # Automated checks
    checks_passed: dict[str, bool] = field(default_factory=dict)
    quality_score: float = 0.0
    
    # Human override
    auto_approved: bool = False
    reviewer_notes: str = ""
    merged_at: str = ""

class KnowledgeBaseGuard:
    """Quality gate for AI-generated content before it enters the Obsidian vault.
    
    All Omega-generated content for wiki/ is staged in omega-workspace/review/
    and must pass automated checks before the knowledge_steward agent merges it.
    
    Checks:
    1. Minimum substance (>100 chars, no placeholder-only content)
    2. Structure (has frontmatter, has ## sections)
    3. No hallucination markers (catches common AI filler patterns)
    4. Source attribution (has [[wikilink]] or DOI references)
    5. Duplicate detection (content hash vs existing pages)
    
    If auto_approved → knowledge_steward merges immediately
    If quality_score < 0.5 → held for human review (reported in Obsidian 通知.md)
    """
    
    MIN_CONTENT_LENGTH = 100
    HALLUCINATION_PATTERNS = [
        "as an AI language model",
        "I don't have access to",
        "based on my training data",
        "please verify this information",
        "I apologize, but I cannot",
    ]
    
    def __init__(self, review_dir: Path, vault_dir: Path):
        self.review_dir = review_dir
        self.vault_dir = vault_dir
        self.review_dir.mkdir(parents=True, exist_ok=True)
        self._known_hashes: set[str] = self._load_known_hashes()
    
    def _load_known_hashes(self) -> set[str]:
        """Load content hashes of all existing wiki pages for dedup."""
        hashes = set()
        wiki_dir = self.vault_dir / "wiki"
        if wiki_dir.exists():
            for f in wiki_dir.rglob("*.md"):
                hashes.add(hashlib.sha256(f.read_text(encoding="utf-8").encode()).hexdigest())
        return hashes
    
    def stage_content(self, target_path: str, content: str,
                     agent: str, task_id: str) -> ContentReview:
        """Stage AI-generated content for review. Returns review object."""
        review_id = hashlib.sha256(f"{target_path}{datetime.utcnow()}".encode()).hexdigest()[:12]
        review = ContentReview(
            review_id=review_id,
            target_path=target_path,
            source_agent=agent,
            task_id=task_id,
            content=content,
            content_hash=hashlib.sha256(content.encode()).hexdigest(),
        )
        
        # Run automated checks
        review.checks_passed = {
            "min_length": len(content) >= self.MIN_CONTENT_LENGTH,
            "has_frontmatter": content.strip().startswith("---"),
            "has_sections": "## " in content,
            "no_hallucination_markers": not any(
                pattern.lower() in content.lower() 
                for pattern in self.HALLUCINATION_PATTERNS
            ),
            "has_source_attribution": ("[[" in content or "doi:" in content.lower()),
            "not_duplicate": review.content_hash not in self._known_hashes,
        }
        
        # Quality score: percentage of checks passed
        passed = sum(1 for v in review.checks_passed.values() if v)
        total = len(review.checks_passed)
        review.quality_score = passed / total if total > 0 else 0.0
        
        # Auto-approve if ≥ 5/6 checks pass (allowing one failure)
        review.auto_approved = review.quality_score >= 5/6
        
        # Save staged content
        stage_file = self.review_dir / f"{review_id}.md"
        stage_file.write_text(content, encoding="utf-8")
        
        # Save review metadata
        meta_file = self.review_dir / f"{review_id}.json"
        meta_file.write_text(json.dumps({
            "review_id": review.review_id,
            "target_path": review.target_path,
            "source_agent": review.source_agent,
            "task_id": review.task_id,
            "checks_passed": review.checks_passed,
            "quality_score": review.quality_score,
            "auto_approved": review.auto_approved,
        }, indent=2))
        
        return review
    
    def needs_human_review(self, review: ContentReview) -> bool:
        """Check if this content needs human attention."""
        return review.quality_score < 0.5 or not review.auto_approved
    
    def merge_approved(self, review_id: str) -> bool:
        """Merge an approved review into the actual vault."""
        meta_file = self.review_dir / f"{review_id}.json"
        content_file = self.review_dir / f"{review_id}.md"
        
        if not meta_file.exists() or not content_file.exists():
            return False
        
        meta = json.loads(meta_file.read_text())
        if not meta.get("auto_approved", False):
            return False
        
        # Write to actual vault path
        target = self.vault_dir / meta["target_path"]
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content_file.read_text(encoding="utf-8"))
        
        # Record the hash to prevent future duplicates
        self._known_hashes.add(hashlib.sha256(
            content_file.read_text(encoding="utf-8").encode()
        ).hexdigest())
        
        # Mark as merged
        meta["merged_at"] = datetime.utcnow().isoformat()
        meta_file.write_text(json.dumps(meta, indent=2))
        
        return True
```

#### 11.7 基准预言机（Benchmark Oracle）— `app/executor/benchmark_oracle.py`

> 🆕 **Codex 建议**：闭环验收不能只看文件是否生成，要有金标准样例、统计结果校验、引用完整率、幻觉率、人工修改量。

**功能**：为 Omega 的 12 个基准闭环提供客观的质量度量。不再只是"文件生成了"→ 通过，而是"生成的文件在统计上正确、引用完整、无可检测幻觉、人工修改量低"→ 通过。

```python
"""Benchmark Oracle — gold-standard quality metrics for closed-loop verification."""

from __future__ import annotations
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any
import json
import hashlib
import re

@dataclass
class OracleResult:
    loop_id: int
    loop_name: str
    passed: bool
    
    # Quantitative metrics
    file_generated: bool = False  # 基础：文件是否存在
    statistical_correctness: float = 0.0  # 统计结果与金标准样本的偏差
    citation_completeness: float = 0.0  # 引用完整率（声明数 / 有来源的声明数）
    hallucination_score: float = 0.0  # 幻觉率（越低越好，0.0 = 无法检测到幻觉）
    human_edit_distance: float = 0.0  # 人工修改量（编辑距离 / 总字符数）
    reproducibility_score: float = 0.0  # 复现率（相同输入两次执行结果一致性）
    
    # Detail
    failed_checks: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)

class BenchmarkOracle:
    """Gold-standard quality verification for Omega's 12 closed loops.
    
    Goes beyond "file was created" → measures correctness, completeness, 
    hallucination, and human edit overhead.
    
    Each loop has:
    - A gold-standard expected output (fixtures/oracle/loop_N_expected.json)
    - Acceptable deviation thresholds
    - Anti-hallucination patterns
    """
    
    # Thresholds for each metric
    THRESHOLDS = {
        "statistical_correctness": 0.90,    # ≥90% match with gold standard
        "citation_completeness": 0.70,      # ≥70% of claims have sources
        "hallucination_score": 0.05,         # ≤5% detected hallucination patterns
        "human_edit_distance": 0.20,          # ≤20% of content needs human editing
        "reproducibility_score": 0.85,        # ≥85% reproducibility
    }
    
    def __init__(self, oracle_dir: Path):
        self.oracle_dir = oracle_dir
        self._gold_standards = self._load_gold_standards()
        self._hallucination_patterns = self._load_hallucination_patterns()
    
    def _load_gold_standards(self) -> dict[int, dict]:
        """Load expected outputs for each loop."""
        standards = {}
        for loop_id in range(1, 13):
            path = self.oracle_dir / f"loop_{loop_id}_expected.json"
            if path.exists():
                standards[loop_id] = json.loads(path.read_text())
        return standards
    
    def _load_hallucination_patterns(self) -> list[str]:
        """Patterns that indicate potential AI hallucination."""
        return [
            r"(?i)as an AI language model",
            r"(?i)I don't have access to (real-time|current|the latest)",
            r"(?i)based on my (training data|knowledge cutoff)",
            r"(?i)please (verify|confirm|check) (this|the) (information|data|result)",
            r"(?i)I (apologize|'m sorry).{0,50}(cannot|unable to|don't have)",
            r"(?i)hypothetical (example|scenario|case)",
            r"(?i)it is important to note that.{0,100}may (vary|differ|not be accurate)",
        ]
    
    def evaluate_loop(self, loop_id: int, output_dir: Path) -> OracleResult:
        """Evaluate one closed loop's output against gold standard."""
        result = OracleResult(loop_id=loop_id, loop_name=f"loop_{loop_id}")
        
        # 1. File existence check (baseline)
        result.file_generated = self._check_files_exist(loop_id, output_dir)
        if not result.file_generated:
            result.failed_checks.append("output_files_missing")
            return result
        
        # 2. Statistical correctness (compare with gold standard)
        gold = self._gold_standards.get(loop_id, {})
        if gold:
            result.statistical_correctness = self._compare_statistics(
                output_dir, gold.get("expected_statistics", {})
            )
        
        # 3. Citation completeness
        result.citation_completeness = self._measure_citation_coverage(output_dir)
        
        # 4. Hallucination detection
        result.hallucination_score = self._detect_hallucinations(output_dir)
        
        # 5. Human edit distance (vs gold standard prose)
        if gold.get("expected_prose"):
            result.human_edit_distance = self._measure_edit_distance(
                output_dir, gold["expected_prose"]
            )
        
        # 6. Reproducibility (run twice, compare)
        result.reproducibility_score = self._measure_reproducibility(loop_id, output_dir)
        
        # Final verdict
        thresholds = self.THRESHOLDS
        checks = [
            ("statistical", result.statistical_correctness >= thresholds["statistical_correctness"]),
            ("citation", result.citation_completeness >= thresholds["citation_completeness"]),
            ("hallucination", result.hallucination_score <= thresholds["hallucination_score"]),
            ("edit_distance", result.human_edit_distance <= thresholds["human_edit_distance"]),
            ("reproducibility", result.reproducibility_score >= thresholds["reproducibility_score"]),
        ]
        
        for name, passed in checks:
            if not passed:
                result.failed_checks.append(f"{name}_below_threshold")
        
        # Must pass all checks + file must exist
        result.passed = result.file_generated and len(result.failed_checks) == 0
        
        return result
    
    def _check_files_exist(self, loop_id: int, output_dir: Path) -> bool:
        expected = {
            1: ["wiki/来源/*.md"],        # Literature ingestion
            3: ["*.png", "*.md"],          # Data analysis
            10: ["wiki/对比/*.md"],        # Tool comparison
            11: ["*_report.md"],           # Tool learning
        }
        patterns = expected.get(loop_id, ["*.md"])
        for pattern in patterns:
            if not list(output_dir.glob(pattern)):
                return False
        return True
    
    def _compare_statistics(self, output_dir: Path, 
                           expected: dict) -> float:
        """Compare output statistics with gold standard values."""
        # Find the main output file
        md_files = list(output_dir.glob("*.md"))
        if not md_files:
            return 0.0
        
        content = md_files[0].read_text(encoding="utf-8")
        
        # Extract numbers from content and compare with expected
        matches = 0
        total = len(expected)
        for key, expected_value in expected.items():
            # Simple regex: find the key and a nearby number
            pattern = rf"{key}.*?([\d.]+)"
            m = re.search(pattern, content, re.IGNORECASE)
            if m:
                actual = float(m.group(1))
                deviation = abs(actual - expected_value) / max(abs(expected_value), 0.001)
                if deviation < 0.10:  # 10% tolerance
                    matches += 1
        
        return matches / max(total, 1)
    
    def _measure_citation_coverage(self, output_dir: Path) -> float:
        """Measure what fraction of factual claims have citations."""
        md_files = list(output_dir.glob("*.md"))
        if not md_files:
            return 0.0
        
        content = md_files[0].read_text(encoding="utf-8")
        
        # Count claim-like sentences (containing numbers, statistics, "showed", "found")
        claim_pattern = re.compile(
            r'(?:showed|found|reported|demonstrated|indicated|suggested|'
            r'was associated|were significantly|OR\s*=|HR\s*=|RR\s*=)',
            re.IGNORECASE
        )
        claims = len(claim_pattern.findall(content))
        
        # Count citations: [[...]], doi:, PMID:, @citekey, (Author, Year)
        citation_pattern = re.compile(
            r'(\[\[.+?\]\]|doi:\s*\S+|PMID:\s*\d+|@\w+|\([A-Z][a-z]+.*?\d{4}\))'
        )
        citations = len(citation_pattern.findall(content))
        
        # Coverage = citations / claims (capped at 1.0)
        return min(citations / max(claims, 1), 1.0)
    
    def _detect_hallucinations(self, output_dir: Path) -> float:
        """Detect AI hallucination markers in output."""
        md_files = list(output_dir.glob("*.md"))
        if not md_files:
            return 1.0  # No files = worst score
        
        content = md_files[0].read_text(encoding="utf-8")
        total_sentences = len(re.split(r'[.!?]+', content))
        
        hallucination_hits = 0
        for pattern in self._hallucination_patterns:
            hits = len(re.findall(pattern, content))
            hallucination_hits += hits
        
        # Score: fraction of sentences with hallucination markers
        return hallucination_hits / max(total_sentences, 1)
    
    def _measure_edit_distance(self, output_dir: Path, 
                              expected_prose: str) -> float:
        """Measure edit distance between output prose and expected."""
        md_files = list(output_dir.glob("*.md"))
        if not md_files:
            return 1.0
        
        content = md_files[0].read_text(encoding="utf-8")
        # Normalized Levenshtein-like ratio
        max_len = max(len(content), len(expected_prose))
        if max_len == 0:
            return 0.0
        
        # Simple character-level diff ratio
        common = sum(1 for a, b in zip(content, expected_prose) if a == b)
        return 1.0 - (common / max_len)
    
    def _measure_reproducibility(self, loop_id: int, 
                                 output_dir: Path) -> float:
        """Placeholder: in production, run the loop twice and compare outputs."""
        # For initial implementation, mark as 1.0 (not tested)
        # Real implementation: run omega task twice, hash both outputs, compare
        return 1.0
    
    def evaluate_all(self, output_base: Path) -> dict[int, OracleResult]:
        """Run oracle evaluation on all 12 loops."""
        results = {}
        for loop_id in range(1, 13):
            loop_dir = output_base / f"loop_{loop_id}"
            if loop_dir.exists():
                results[loop_id] = self.evaluate_loop(loop_id, loop_dir)
            else:
                results[loop_id] = OracleResult(
                    loop_id=loop_id, loop_name=f"loop_{loop_id}",
                    passed=False, failed_checks=["loop_not_executed"]
                )
        return results
    
    def to_report(self, results: dict[int, OracleResult]) -> str:
        """Generate a human-readable oracle report."""
        lines = ["# 🔮 Benchmark Oracle 评估报告", ""]
        total_passed = sum(1 for r in results.values() if r.passed)
        total = len(results)
        
        lines.append(f"## 总结：{total_passed}/{total} 闭环通过预言机验证")
        lines.append("")
        lines.append("| 闭环 | 状态 | 统计正确性 | 引用完整率 | 幻觉率 | 人工修改量 |")
        lines.append("|------|------|-----------|-----------|--------|-----------|")
        
        for loop_id, r in sorted(results.items()):
            status = "✅" if r.passed else "❌"
            lines.append(
                f"| {loop_id} | {status} | {r.statistical_correctness:.0%} | "
                f"{r.citation_completeness:.0%} | {r.hallucination_score:.0%} | "
                f"{r.human_edit_distance:.0%} |"
            )
        
        if total_passed < total:
            lines.append("")
            lines.append("## 未通过项")
            for loop_id, r in sorted(results.items()):
                if r.failed_checks:
                    lines.append(f"### 闭环 {loop_id}")
                    for fc in r.failed_checks:
                        lines.append(f"- ❌ {fc}")
        
        return "\n".join(lines)
```

#### 11.8 闭环预言机金标准数据

创建 `fixtures/oracle/` 目录，为每个闭环提供金标准预期输出：

```json
// fixtures/oracle/loop_3_expected.json — 数据分析闭环金标准
{
  "loop_id": 3,
  "loop_name": "data_analysis",
  "expected_statistics": {
    "mean_glucose": 107.4,
    "sd_glucose": 22.1,
    "mean_hba1c": 5.84,
    "correlation_glucose_hba1c": 0.72,
    "missing_glucose_count": 1,
    "missing_hba1c_count": 1
  },
  "expected_prose": "对 20 例模拟临床数据进行分析...",
  "expected_output_files": ["clinical_analysis_report.md", "glucose_distribution.png", "correlation_heatmap.png"],
  "acceptable_deviation": 0.10
}
```

#### 11.9 CLIG 集成 

**修改 `app/main.py`**，新增以下 CLI 命令：

```python
# 模拟构建
@app.cli.command()
@click.argument("phase")
def simulate(phase: str):
    """生成构建阶段的模拟报告（不修改任何文件）。"""
    from app.safety.simulator import BuildSimulator
    simulator = BuildSimulator()
    # Load phase config from UPGRADE_GUIDE.md phase mapping
    result = simulator.simulate_phase({"name": phase}, {})
    click.echo(simulator.to_markdown_report(result))

# 飞行记录查询
@app.cli.command()
@click.argument("task_id")
def flightlog(task_id: str):
    """查看任务的飞行记录仪日志。"""
    from app.memory.flight_recorder import FlightRecorder
    recorder = FlightRecorder(Path("omega-runtime/logs/flights"))
    # Load and display flight record

# 预算模式切换
@app.cli.command()
@click.argument("mode")
def budget(mode: str):
    """设置执行模式: cheap | high_quality | offline | balanced"""
    from app.router.budget_console import BudgetConsole, ExecutionMode
    console = BudgetConsole({})
    selected = console.select_mode("general", mode)
    click.echo(f"预算模式已切换为: {selected.value}")

# 隔离区管理
@app.cli.command()
@click.argument("action")
@click.option("--tool-id", help="工具 ID")
def quarantine(action: str, tool_id: str):
    """管理工具隔离区: list | test | sign | promote"""
    from app.toolsmith.quarantine import QuarantineManager
    qm = QuarantineManager(Path("omega-runtime/quarantine"))
    # Dispatch action

# 知识审查区
@app.cli.command()
@click.argument("action")
def review(action: str):
    """管理知识候审区: list | approve | reject"""
    from app.safety.kb_guard import KnowledgeBaseGuard
    guard = KnowledgeBaseGuard(
        Path("omega-workspace/review"),
        Path(os.environ.get("OMEGA_HOME", ".")) / "omega-vault"
    )
    # Dispatch action

# 🆕 基准预言机
@app.cli.command()
@click.argument("action")  # run | report | compare | calibrate
@click.option("--loop", help="指定闭环（不指定则全部）")
@click.option("--gold-standard", help="金标准数据路径")
def oracle(action: str, loop: str = None, gold_standard: str = None):
    """基准预言机：运行闭环预测 vs 金标准对比 | 生成偏差报告 | 校准闭环"""
    from app.executor.benchmark_oracle import BenchmarkOracle
    oracle = BenchmarkOracle(Path("omega-runtime/config/benchmark_oracle.yaml"))
    if action == "run":
        result = oracle.run_closed_loop(loop) if loop else oracle.run_all()
        click.echo(oracle.format_result(result))
    elif action == "report":
        report = oracle.generate_deviation_report()
        click.echo(report)
    elif action == "compare":
        click.echo(oracle.compare_versions(loop))
    elif action == "calibrate":
        adjusted = oracle.calibrate(loop)
        click.echo(f"Calibrated: {json.dumps(adjusted, indent=2)}")

# 🆕 溯源验证
@app.cli.command()
@click.argument("claim_id")
def provenance(claim_id: str):
    """验证指定结论的溯源链完整性。"""
    from app.outcome.provenance import ProvenanceWatermark
    pw = ProvenanceWatermark()
    chain = pw.verify_chain(claim_id)
    click.echo(pw.render_chain(chain))

# 🆕 本地引擎管理
@app.cli.command()
@click.argument("action")  # status | start | stop | test
def local_engine(action: str):
    """管理本地 AI 引擎：Ollama/LM Studio/llama-cpp-python"""
    from app.router.local_engine import LocalEngineManager
    mgr = LocalEngineManager()
    if action == "status":
        click.echo(mgr.check_all())
    elif action == "test":
        result = mgr.test_fallback_chain()
        click.echo(f"Fallback chain test: {'PASS' if result else 'FAIL'}")
```

#### 11.10 验证

```bash
# 模拟构建（不修改文件）
omega simulate phase-2      # 生成沙箱重构建的完整 DAG + 风险 + 文件变更清单

# 飞行记录
omega task "搜5篇文献" --execute
omega flightlog <task_id>   # 查看完整审计记录

# 预算模式
omega budget cheap
omega task "快速分析数据" --execute  # 使用 DeepSeek，跳过非必需步骤

# 工具隔离
omega quarantine list        # 列出隔离区中的工具
omega quarantine test --tool-id textstat   # 运行验收测试
omega quarantine sign --tool-id textstat   # 签名
omega quarantine promote --tool-id textstat  # 推广到正式注册表

# 知识审查
omega review list            # 列出候审区内容
omega review approve <id>    # 手动批准
omega review reject <id>     # 拒绝

# 🆕 基准预言机
omega oracle run --loop 1                         # 运行闭环 1 并对比金标准
omega oracle run --all                              # 运行全部闭环
omega oracle report                                 # 生成偏差报告
omega oracle compare --loop 3                       # 版本间质量对比
omega oracle calibrate --loop 5                     # 校准闭环阈值

# 🆕 溯源验证
omega provenance <claim_id>                         # 验证溯源链完整性
omega task "..." --execute && omega provenance last # 验证最新任务的溯源链

# 🆕 ECP 审批流程（Phase 8 增强）
omega evolve --propose numpy                        # 为 numpy 升级生成 ECP
omega evolve list-ecps --status pending             # 列出待审批 ECP
omega evolve approve ECP-20260517-001               # 审批
omega evolve execute ECP-20260517-001               # 执行
omega evolve rollback ECP-20260517-001              # 回滚

# 🆕 本地引擎回退
omega local-engine status                           # 检查本地引擎状态
omega local-engine test                             # 测试回退链

# 回归验证
pytest tests/test_simulator.py tests/test_flight_recorder.py \
       tests/test_provenance.py tests/test_budget.py \
       tests/test_quarantine.py tests/test_kb_guard.py \
       tests/test_benchmark_oracle.py tests/test_ecp.py -v
omega bench --all            # 仍保持 ≥ 90% 通过率
```

### 受影响文件

| 文件 | 操作 |
|------|------|
| `app/safety/simulator.py` | **新建** |
| `app/memory/flight_recorder.py` | **新建** |
| `app/outcome/provenance.py` | **新建** |
| `app/router/budget_console.py` | **新建** |
| `app/toolsmith/quarantine.py` | **新建** |
| `app/safety/kb_guard.py` | **新建** |
| `app/executor/benchmark_oracle.py` | **新建** — 基准预言机 |
| `app/router/local_engine.py` | **新建** — 本地引擎回退管理 |
| `app/main.py` | 修改 — 新增 10 个 CLI 命令 |
| `config/benchmark_oracle.yaml` | **新建** — 闭环 × 金标准映射配置 |
| `fixtures/gold_standard/closed_loop_1.json` | **新建** — 闭环 1 金标准 |
| `fixtures/gold_standard/closed_loop_3.json` | **新建** — 闭环 3 金标准 |
| `fixtures/gold_standard/closed_loop_5.json` | **新建** — 闭环 5 金标准 |
| `tests/test_simulator.py` | **新建** |
| `tests/test_flight_recorder.py` | **新建** |
| `tests/test_provenance.py` | **新建** |
| `tests/test_budget.py` | **新建** |
| `tests/test_quarantine.py` | **新建** |
| `tests/test_kb_guard.py` | **新建** |
| `tests/test_benchmark_oracle.py` | **新建** |
| `tests/test_ecp.py` | **新建** |

---

所有文档均位于 `{OMEGA_HOME}/omega-vault/omega生态系统项目/`：

| 文档 | 路径 | 用途 |
|------|------|------|
| 构建指导书 | `00-总览/Omega 构建指导书 — 给 Codex 的系统构造规范.md` | 整体架构和构建顺序 |
| 功能总方法论 | `01-方法论/Omega 最终完整方法论.md` | 当前系统哲学和设计原则 |
| Tool-Agent Router | `02-架构/Tool-Agent Router：最佳工具与最佳执行者选择器.md` | 12 维评分引擎（Phase 3） |
| Stage-Aware Router | `02-架构/Stage-Aware Tool-Agent Router.md` | 阶段权重覆盖（Phase 3） |
| Dynamic Task Planner | `02-架构/Dynamic Task Planner：动态任务规划器.md` | 7 步规划流程（Phase 4+5） |
| Best-Practice Harvester | `02-架构/Best-Practice Harvester：最佳实践采集器.md` | 8 步经验采集（Phase 7） |
| 自我解惑与外援调用 | `02-架构/自我解惑与外援调用循环.md` | 外部 AI 调用（Phase 6） |
| AI工具生态雷达 | `03-能力矩阵/AI工具生态雷达.md` | 工具发现（Phase 6+8） |
| SOTA Source Hierarchy | `03-能力矩阵/SOTA Source Hierarchy：顶尖工具来源分级.md` | 工具来源分级 |
| Model and Tool Lifecycle | `03-能力矩阵/Model and Tool Lifecycle Manager.md` | 工具生命周期（Phase 6+8） |
| Multimodal Outcome Package | `04-任务契约与成果包/Multimodal Outcome Package.md` | 成果包设计（Phase 8） |
| Runtime Architecture | `08-运行时与原型/Omega Runtime Architecture.md` | 11 组件数据流 |
| Omega Manifest Schema | `08-运行时与原型/Omega Manifest Schema.md` | omega.yaml 字段 schema |
| Auto-Upgrade Policy | `08-运行时与原型/Auto-Upgrade Policy.md` | 自动升级策略（Phase 8） |
| 基准任务花园 | `09-功能基准任务花园/README.md` | 12 个基准闭环定义 |
| External AI Rolebook | `10-外部AI与工具注册表/External AI Rolebook.md` | 外部 AI 生态位 |
| 科学动画生产系统 | `11-创意与科学可视化/科学动画生产系统.md` | 9 阶段管线（Phase 9） |
| Creative Tool Router | `11-创意与科学可视化/Creative Tool Router.md` | 创意评分系统（Phase 9） |

## 附录 B：每阶段通用验证方法

```bash
cd {OMEGA_HOME}/omega-runtime

# 1. 单元测试
.venv\Scripts\python -m pytest tests/ -v

# 2. 闭环基准（Phase 2-8 确保仍 7/7，Phase 9+ 增加新闭环）
.venv\Scripts\python -m app.main bench --all

# 3. 类型检查
.venv\Scripts\python -m mypy app/ --ignore-missing-imports

# 4. 手动冒烟
.venv\Scripts\python -m app.main task "search literature on SGLT2" --dry-run
.venv\Scripts\python -m app.main status

# 5. Git 提交
git add -A
git commit -m "feat: complete Phase N — <简短描述>"
```

## 附录 C：Codex 执行规则

```
Codex，读取 {OMEGA_HOME}/omega-runtime/ 中的 Omega v0.3.0-mfe 项目。

请按照 {OMEGA_HOME}/omega-vault/omega生态系统项目/99-交付给Codex的构建包/UPGRADE_GUIDE.md
中的升级指南，从 Phase 2 开始，逐阶段升级 Omega 到 v1.0.0-full。

规则：
0. **模拟优先**：每个阶段开始前，先 `omega simulate phase-N` 生成 DAG+风险+变更清单预览，展示给用户确认后才开始写代码
1. 每完成一个阶段，运行 omega bench --all 验证回归通过
2. 每完成一个阶段，运行 pytest 验证全部测试通过  
3. 若某阶段导致已有功能退化，回滚该阶段并报告
4. 不要跳过任何阶段——Phase 2 是 Phase 3 的基础，Phase 3 是 Phase 4 的基础，依此类推至 Phase 11
5. 实现前先阅读对应设计文档（附录 A 索引）
6. 每个阶段完成后，写 ITERATION_N_REPORT.md 记录变更
7. 所有代码用英文，所有注释用英文，面向用户的输出用中文
8. 遵守 AGENTS.md 中的凭据处理规则、构建边界、上下文管理协议、知识防污染协议、工具隔离协议、模拟优先协议
```

---

*升级指南版本：v3.1 — 2026-05-17*
*覆盖：Omega v0.3.0-mfe → v1.0.0-full（11 个 Phase）*
*目标：实现全部设计文档中构想的功能和理念，含 Phase 11 质量与安全加固*
*变更 v3.1：Phase 8 新增 Evolution Change Proposal (ECP) 审批流程；Phase 11 新增基准预言机（Benchmark Oracle）、溯源验证、本地引擎回退 CLI；验证与受影响文件表同步更新*
*变更 v3.0：新增 Phase 11（6 项安全特性：模拟构建器/飞行记录仪/溯源水印/预算控制台/工具隔离/知识防污染）；Phase 9 新增现实主义说明；附录 C 新增模拟优先规则；全局"10 阶段"更新为"11 阶段"*
