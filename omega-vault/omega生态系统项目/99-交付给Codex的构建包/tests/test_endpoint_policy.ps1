$ErrorActionPreference = "Stop"
$policy = Join-Path $PSScriptRoot "..\scripts\endpoint_policy.ps1"
. $policy

$invalid = @(
    "https://api.anthropic.com/v1/messages",
    "https://API.ANTHROPIC.COM.:443/v1/messages",
    ("https://api{0}anthropic{0}com/v1/messages" -f [char]0x3002),
    ("https://api{0}anthropic{0}com/v1/messages" -f [char]0xFF0E),
    ("https://api{0}anthropic{0}com/v1/messages" -f [char]0xFF61),
    "https://api%2eanthropic%2ecom/v1/messages",
    "https://api%252eanthropic%252ecom/v1/messages",
    "https://edge.api.anthropic.com/v1/messages",
    "https://user@api.anthropic.com/v1/messages",
    "ftp://openrouter.ai/api/v1",
    "https://openrouter.ai:invalid/api/v1"
)

$failures = @()
foreach ($value in $invalid) {
    if (Test-OmegaCompatibleEndpoint -Value $value) {
        $failures += "accepted forbidden/malformed URL: $value"
    }
}

$canonical = ConvertTo-OmegaCanonicalEndpoint -Value "HTTPS://OPENROUTER.AI.:443/api/v1"
if ($canonical -ne "https://openrouter.ai/api/v1") {
    $failures += "canonicalization mismatch: $canonical"
}
if (-not (Test-OmegaCompatibleEndpoint -Value "https://api.openai.com/v1")) {
    $failures += "rejected approved HTTPS endpoint"
}

$invalidEnvironments = @(
    "ANTHROPIC_API_KEY=do-not-read",
    "ANTHROPIC_BASE_URL=https://api.anthropic.com",
    "COMPAT_ENDPOINT=https://api%2eanthropic%2ecom/v1",
    ("COMPAT_MODELS_URL=https://api{0}anthropic{0}com/v1/models" -f [char]0x3002),
    "OLLAMA_HOST=https://api.anthropic.com.:443"
)
foreach ($content in $invalidEnvironments) {
    if (@(Get-OmegaEnvironmentPolicyViolations -Content $content).Count -eq 0) {
        $failures += "accepted forbidden environment variable class"
    }
}
$validEnvironment = "DOMESTIC_CLAUDE_BASE_URL=https://compatible.example/v1`nOLLAMA_HOST=http://localhost:11434"
if (@(Get-OmegaEnvironmentPolicyViolations -Content $validEnvironment).Count -ne 0) {
    $failures += "rejected approved compatibility environment"
}

if ($failures.Count -gt 0) {
    $failures | ForEach-Object { Write-Error $_ }
    exit 1
}
Write-Output "ENDPOINT_POLICY_TEST_PASS"
