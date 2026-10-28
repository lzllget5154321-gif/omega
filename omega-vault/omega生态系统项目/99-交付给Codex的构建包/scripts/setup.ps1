# Omega 新电脑环境安装脚本
# ==========================
# 在新 Windows 电脑上以管理员身份运行此脚本。
# 用法: 右键 PowerShell → 以管理员身份运行 → .\setup.ps1
#
# 此脚本仅配置环境（安装软件、创建目录、配置 Docker）。
# 实际的 Omega 系统构建由 Codex 完成。

param(
    [string]$OmegaHome = "D:\Omega-System",
    [switch]$SkipWinget = $false,
    [switch]$SkipDocker = $false,
    [switch]$DryRun = $false
)

$ErrorActionPreference = "Stop"
[Console]::OutputEncoding = [Text.Encoding]::UTF8

$endpointPolicy = Join-Path $PSScriptRoot "endpoint_policy.ps1"
if (-not (Test-Path -LiteralPath $endpointPolicy -PathType Leaf)) {
    throw "Fail-closed: endpoint policy module is missing: $endpointPolicy"
}
. $endpointPolicy

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Omega 系统环境安装" -ForegroundColor Cyan
Write-Host "  目标: Omega-Lite MFE (阶段 1 先锋物种)" -ForegroundColor Cyan
Write-Host "  部署路径: $OmegaHome" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# ── 步骤 0: 检查管理员权限 ──
Write-Host "[0/6] 检查管理员权限..." -ForegroundColor Yellow
$isAdmin = ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole] "Administrator")
if (-not $isAdmin) {
    Write-Host "[ERROR] 此脚本需要管理员权限。请右键 PowerShell → 以管理员身份运行。" -ForegroundColor Red
    exit 1
}
Write-Host "  [OK] 管理员权限" -ForegroundColor Green

# ── 步骤 1: 创建目录结构 ──
Write-Host "[1/6] 创建 Omega 目录结构..." -ForegroundColor Yellow
$omegaDirs = @(
    "$OmegaHome",
    "$OmegaHome\omega-vault",
    "$OmegaHome\omega-runtime",
    "$OmegaHome\omega-data\postgres",
    "$OmegaHome\omega-data\qdrant",
    "$OmegaHome\omega-data\logs",
    "$OmegaHome\omega-workspace\temp",
    "$OmegaHome\omega-workspace\sandbox",
    "$OmegaHome\omega-workspace\outputs",
    "$OmegaHome\omega-workspace\outputs\screenshots",
    "$OmegaHome\omega-assets\zotero",
    "$OmegaHome\omega-assets\templates",
    "$OmegaHome\omega-assets\fonts"
)

foreach ($dir in $omegaDirs) {
    if (-not (Test-Path $dir)) {
        if (-not $DryRun) {
            New-Item -ItemType Directory -Path $dir -Force | Out-Null
        } else {
            Write-Host "  [DRY-RUN] Would create: $dir" -ForegroundColor Gray
        }
    }
}
Write-Host "  [OK] 目录结构就绪 ($OmegaHome\)" -ForegroundColor Green

# ── 步骤 2: 安装基础软件 ──
if (-not $SkipWinget) {
    Write-Host "[2/6] 安装基础软件 (winget)..." -ForegroundColor Yellow

    $packages = @(
        @{name="Python 3.12"; id="Python.Python.3.12"},
        @{name="Node.js 22 LTS"; id="OpenJS.NodeJS.LTS.22"},
        @{name="Git"; id="Git.Git"},
        @{name="Visual Studio Code"; id="Microsoft.VisualStudioCode"}
    )

    foreach ($pkg in $packages) {
        try {
            $installed = winget list --id $pkg.id 2>$null | Select-String $pkg.id
            if ($installed) {
                Write-Host "  [SKIP] $($pkg.name) 已安装" -ForegroundColor Gray
            } else {
                Write-Host "  [INSTALL] $($pkg.name) ..." -ForegroundColor Gray
                if (-not $DryRun) {
                    winget install --id $pkg.id --silent --accept-package-agreements --accept-source-agreements
                }
                Write-Host "  [OK] $($pkg.name) 安装完成" -ForegroundColor Green
            }
        } catch {
            Write-Host "  [WARN] $($pkg.name) 安装失败: $_" -ForegroundColor Yellow
        }
    }

    # Docker Desktop 单独安装（需要手动操作）
    try {
        $dockerInstalled = Get-Command docker -ErrorAction SilentlyContinue
        if ($dockerInstalled) {
            Write-Host "  [SKIP] Docker Desktop 已安装" -ForegroundColor Gray
        } else {
            Write-Host "  [INSTALL] Docker Desktop ..." -ForegroundColor Gray
            if (-not $DryRun) {
                winget install --id Docker.DockerDesktop --silent --accept-package-agreements
            }
            Write-Host "  ⚠️  Docker Desktop 安装完成后，请手动启动它并等待鲸鱼图标变绿！" -ForegroundColor Yellow
            Write-Host "  启动后按任意键继续..." -ForegroundColor Yellow
            if (-not $DryRun) {
                $null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
            }
        }
    } catch {
        Write-Host "  [WARN] Docker Desktop 安装失败: $_" -ForegroundColor Yellow
    }
} else {
    Write-Host "[2/6] 跳过软件安装 (--SkipWinget)" -ForegroundColor Gray
}

# ── 步骤 3: 验证基础软件 ──
Write-Host "[3/6] 验证基础软件..." -ForegroundColor Yellow
$checks = @(
    @{cmd="python --version"; name="Python"},
    @{cmd="node --version"; name="Node.js"},
    @{cmd="git --version"; name="Git"},
    @{cmd="docker --version"; name="Docker"},
    @{cmd="codex --version"; name="Codex CLI"}
)

foreach ($check in $checks) {
    try {
        $result = Invoke-Expression $check.cmd 2>&1
        Write-Host "  [OK] $($check.name): $result" -ForegroundColor Green
    } catch {
        Write-Host "  [MISSING] $($check.name) — 请手动安装后重新运行此脚本" -ForegroundColor Red
    }
}

# ── 步骤 4: 配置 Python 虚拟环境 ──
Write-Host "[4/6] 配置 Python 虚拟环境..." -ForegroundColor Yellow
$venvPath = "$OmegaHome\.venv"
if (-not (Test-Path $venvPath)) {
    if (-not $DryRun) {
        python -m venv $venvPath
    }
    Write-Host "  [OK] 虚拟环境创建: $venvPath" -ForegroundColor Green
} else {
    Write-Host "  [SKIP] 虚拟环境已存在" -ForegroundColor Gray
}

# ── 步骤 5: 配置 .env 文件 ──
Write-Host "[5/6] 配置环境变量..." -ForegroundColor Yellow
$envTemplate = "$OmegaHome\build-package\config\.env.example"
$envTarget = "$OmegaHome\.env"

if (Test-Path $envTemplate) {
    if (-not (Test-Path $envTarget)) {
        if (-not $DryRun) {
            Copy-Item $envTemplate $envTarget
            Write-Host "  [OK] .env 文件已从模板创建" -ForegroundColor Green
        } else {
            Write-Host "  [DRY-RUN] Would copy .env.example → .env" -ForegroundColor Gray
        }
        Write-Host ""
        Write-Host "  ⚠️  重要：请编辑 $OmegaHome\.env，至少设置数据库密码：" -ForegroundColor Yellow
        Write-Host "     1. POSTGRES_PASSWORD (必需) — 任意强密码" -ForegroundColor White
        Write-Host "     2. OPENAI_API_KEY (Omega 独立运行时主 provider，可选)" -ForegroundColor White
        Write-Host "     3. OPENROUTER_API_KEY / DOMESTIC_CLAUDE_API_KEY (兼容备用，可选)" -ForegroundColor White
        Write-Host "     4. 国内 OpenAI-compatible Key 为后续备用；不得配置原生 Anthropic" -ForegroundColor White
        Write-Host ""
        Write-Host "  编辑完成后按任意键继续..." -ForegroundColor Yellow
        if (-not $DryRun) {
            $null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
        }
    } else {
        Write-Host "  [SKIP] .env 已存在" -ForegroundColor Gray
    }
} else {
    Write-Host "  [WARN] .env.example 模板不存在，稍后 Codex 会提示你创建" -ForegroundColor Yellow
}

# ── 步骤 6: 就绪检查 ──
Write-Host "[6/6] 最终检查..." -ForegroundColor Yellow

$allOk = $true
$policyOk = $true

# 检查目录
if (-not (Test-Path "$OmegaHome\omega-vault")) {
    Write-Host "  [TODO] omega-vault/ 目录为空，请复制 Omega 设计文档到此处" -ForegroundColor Yellow
    $allOk = $false
} else {
    Write-Host "  [OK] omega-vault/ 就绪" -ForegroundColor Green
}

# 检查 .env
if (-not (Test-Path "$OmegaHome\.env")) {
    Write-Host "  [TODO] .env 文件不存在，稍后 Codex 会提示创建" -ForegroundColor Yellow
} else {
    $envContent = Get-Content "$OmegaHome\.env" -Raw
    $policyViolations = @(Get-OmegaEnvironmentPolicyViolations -Content $envContent)
    foreach ($violation in $policyViolations) {
        Write-Host "  [ERROR] $violation" -ForegroundColor Red
        $allOk = $false
        $policyOk = $false
    }
    $hasOpenRouter = ($envContent -match "OPENROUTER_API_KEY=\S" -and $envContent -notmatch "OPENROUTER_API_KEY=$")
    $hasDomesticClaude = ($envContent -match "DOMESTIC_CLAUDE_API_KEY=\S" -and $envContent -notmatch "DOMESTIC_CLAUDE_API_KEY=$")
    $hasDeepSeek = ($envContent -match "DEEPSEEK_API_KEY=\S" -and $envContent -notmatch "DEEPSEEK_API_KEY=$")
    $hasOpenAI = ($envContent -match "OPENAI_API_KEY=\S" -and $envContent -notmatch "OPENAI_API_KEY=$")
    $hasPassword = ($envContent -match "POSTGRES_PASSWORD=\S" -and $envContent -notmatch "POSTGRES_PASSWORD=$")
    if ($hasOpenAI -or $hasOpenRouter -or $hasDomesticClaude -or $hasDeepSeek) {
        if ($hasOpenRouter) { Write-Host "  [OK] OpenRouter fallback 已配置" -ForegroundColor Green }
        if ($hasDomesticClaude) { Write-Host "  [OK] Domestic Claude Messages fallback 已配置" -ForegroundColor Green }
        if ($hasDeepSeek) { Write-Host "  [OK] DEEPSEEK_API_KEY 已设置" -ForegroundColor Green }
        if ($hasOpenAI) { Write-Host "  [OK] OPENAI_API_KEY 已设置" -ForegroundColor Green }
    } else {
        Write-Host "  [INFO] 独立运行时 provider 均未配置；Codex 会话仍可完成构建，运行时集成标记 deferred" -ForegroundColor Yellow
    }
    if (-not $hasPassword) {
        Write-Host "  [TODO] POSTGRES_PASSWORD 未设置" -ForegroundColor Yellow
        $allOk = $false
    } else {
        Write-Host "  [OK] POSTGRES_PASSWORD 已设置" -ForegroundColor Green
    }
}

Write-Host ""

if (-not $policyOk) {
    exit 1
}
Write-Host "========================================" -ForegroundColor Cyan
if ($allOk) {
    Write-Host "  环境安装完成！可以交给 Codex 开始构建了。" -ForegroundColor Green
} else {
    Write-Host "  环境基本就绪（有 TODO 项）。可以交给 Codex，" -ForegroundColor Yellow
    Write-Host "  Codex 会在构建过程中提示你完成剩余配置。" -ForegroundColor Yellow
}
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "下一步：" -ForegroundColor White
Write-Host "  1. 确保 omega生态系统项目/ 设计文档已复制到 omega-vault/" -ForegroundColor White
Write-Host "  2. 确保 build-package/ 已复制到 $OmegaHome\" -ForegroundColor White
Write-Host "  3. 启动 Codex，按照 CODEX_RUN_PROMPT.md 中的提示词开始构建" -ForegroundColor White
Write-Host ""
