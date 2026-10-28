# Omega Build Package Assembly Script
# ====================================
# Run on current computer to verify all files needed for Codex delivery are present.
# This script does NOT modify any files -- read-only integrity check.
#
# Usage: .\assemble_package.ps1
# Encoding: MUST be saved as UTF-8 with BOM for PowerShell compatibility
#   If you see garbled output or parse errors, re-save this file as UTF-8 BOM

param(
    [switch]$CheckOnly = $true
)

$strictGate = Join-Path $PSScriptRoot "package_gate.py"
if (-not (Test-Path -LiteralPath $strictGate)) {
    Write-Error "Strict package gate is missing: $strictGate"
    exit 1
}
& python $strictGate --package (Resolve-Path "$PSScriptRoot\..")
if ($LASTEXITCODE -ne 0) {
    Write-Error "Strict MANIFEST/schema/reference/adversarial gate failed."
    exit $LASTEXITCODE
}

Write-Host "=== Omega Build Package Integrity Check ===" -ForegroundColor Cyan
Write-Host ""

$vaultRoot = Resolve-Path "$PSScriptRoot\..\..\..\"
$missing = @()
$found = @()

$manifestFiles = @(
    "omega生态系统项目\00-总览\Omega 构建指导书 — 给 Codex 的系统构造规范.md",
    "omega生态系统项目\00-总览\omega生态系统项目-总说明.md",
    "omega生态系统项目\00-总览\Omega运行形态与本体文件说明.md",
    "omega生态系统项目\00-总览\omega生态系统项目-版本演化图.md",
    "omega生态系统项目\01-方法论\Omega 最终完整方法论.md",
    "omega生态系统项目\02-架构\Tool-Agent Router：最佳工具与最佳执行者选择器.md",
    "omega生态系统项目\02-架构\Stage-Aware Tool-Agent Router.md",
    "omega生态系统项目\02-架构\Dynamic Task Planner：动态任务规划器.md",
    "omega生态系统项目\02-架构\Best-Practice Harvester：最佳实践采集器.md",
    "omega生态系统项目\02-架构\自我解惑与外援调用循环.md",
    "omega生态系统项目\03-能力矩阵\AI工具生态雷达.md",
    "omega生态系统项目\03-能力矩阵\SOTA Source Hierarchy：顶尖工具来源分级.md",
    "omega生态系统项目\03-能力矩阵\Model and Tool Lifecycle Manager.md",
    "omega生态系统项目\03-能力矩阵\Social Signal Validator.md",
    "omega生态系统项目\04-任务契约与成果包\Multimodal Outcome Package.md",
    "omega生态系统项目\08-运行时与原型\README.md",
    "omega生态系统项目\08-运行时与原型\Omega Runtime Architecture.md",
    "omega生态系统项目\08-运行时与原型\Omega Manifest Schema.md",
    "omega生态系统项目\08-运行时与原型\omega.yaml",
    "omega生态系统项目\08-运行时与原型\Auto-Upgrade Policy.md",
    "omega生态系统项目\09-功能基准任务花园\README.md",
    "omega生态系统项目\09-功能基准任务花园\Tool Benchmark Cards.md",
    "omega生态系统项目\10-外部AI与工具注册表\External AI Rolebook.md",
    "omega生态系统项目\10-外部AI与工具注册表\README.md",
    "omega生态系统项目\11-创意与科学可视化\科学动画生产系统.md",
    "omega生态系统项目\11-创意与科学可视化\Creative Tool Router.md"
)

$criticalBuildFiles = @(
    "AGENTS.md",
    "CODEX_RUN_PROMPT.md",
    "BUILD_CHECKLIST.md",
    "MANIFEST.yaml",
    "PRODUCTION_IDENTITY_LEDGER.yaml",
    "schemas\production_identity_ledger.schema.json",
    "config\model_capabilities.yaml",
    "config\engine_resolution.yaml",
    "config\api_tiers.yaml",
    "config\agents.yaml",
    "config\routing_table.yaml",
    "config\tools.yaml",
    "templates\active_engines.yaml"
)

Write-Host "Checking $($manifestFiles.Count) design files..." -ForegroundColor White
Write-Host ""

foreach ($file in $manifestFiles) {
    $fullPath = Join-Path $vaultRoot $file
    if (Test-Path $fullPath) {
        $size = (Get-Item $fullPath).Length
        $sizeKB = [math]::Round($size / 1KB, 1)
        Write-Host "  [OK] $file ($sizeKB KB)" -ForegroundColor Green
        $found += $file
    } else {
        Write-Host "  [MISSING] $file" -ForegroundColor Red
        $missing += $file
    }
}

Write-Host ""
Write-Host "Checking $($criticalBuildFiles.Count) critical build-package files..." -ForegroundColor White
foreach ($file in $criticalBuildFiles) {
    $fullPath = Join-Path (Resolve-Path "$PSScriptRoot\..") $file
    $displayPath = "build-package\$file"
    if (Test-Path -LiteralPath $fullPath) {
        Write-Host "  [OK] $displayPath" -ForegroundColor Green
        $found += $displayPath
    } else {
        Write-Host "  [MISSING] $displayPath" -ForegroundColor Red
        $missing += $displayPath
    }
}

Write-Host ""
Write-Host "=== Results ===" -ForegroundColor Cyan
Write-Host "  Found: $($found.Count) files" -ForegroundColor Green
Write-Host "  Missing: $($missing.Count) files" -ForegroundColor $(if ($missing.Count -eq 0) { "Green" } else { "Red" })

if ($missing.Count -gt 0) {
    Write-Host ""
    Write-Host "Missing files:" -ForegroundColor Red
    foreach ($m in $missing) {
        Write-Host "  - $m" -ForegroundColor Red
    }
    Write-Host ""
    Write-Host "Please add the above files before handing to Codex." -ForegroundColor Yellow
} else {
    Write-Host ""
    Write-Host "All design files present! Ready to hand to Codex." -ForegroundColor Green
    Write-Host ""
    Write-Host "Delivery checklist:" -ForegroundColor White
    Write-Host "  1. Entire omega生态系统项目\ directory (26 MANIFEST design files)" -ForegroundColor White
    Write-Host "  2. This folder (99-交付给Codex的构建包\) -- includes AGENTS.md + README.md + MANIFEST.yaml" -ForegroundColor White
    Write-Host "  3. Root AGENTS.md (Codex instructions); CLAUDE.md only if the compatible fallback is intentionally enabled" -ForegroundColor White
    Write-Host "  4. wiki\ directory (optional, if migrating knowledge base)" -ForegroundColor White
    Write-Host ""
    Write-Host "Copy to D:\Omega-System\omega-vault\ on the new computer." -ForegroundColor Cyan
}

if (-not $CheckOnly -and $missing.Count -eq 0) {
    Write-Host ""
    Write-Host "Generating delivery archive..." -ForegroundColor Yellow
    $outputZip = Join-Path $env:USERPROFILE "Desktop\Omega-Codex-Build-Package.zip"

    $items = @()
    $items += Join-Path $vaultRoot "omega生态系统项目"
    $items += Join-Path $vaultRoot "AGENTS.md"
    if (Test-Path (Join-Path $vaultRoot "CLAUDE.md")) { $items += Join-Path $vaultRoot "CLAUDE.md" }
    if (Test-Path (Join-Path $vaultRoot ".claude")) { $items += Join-Path $vaultRoot ".claude" }

    Compress-Archive -Path $items -DestinationPath $outputZip -Force
    Write-Host "Archive created: $outputZip" -ForegroundColor Green
}

if ($missing.Count -gt 0) {
    exit 1
}
