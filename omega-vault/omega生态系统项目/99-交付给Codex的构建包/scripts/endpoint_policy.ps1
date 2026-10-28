# Shared fail-closed endpoint normalizer used by setup.ps1.
# Returns a canonical URL, or $null when parsing/policy validation fails.
function ConvertTo-OmegaCanonicalEndpoint {
    param([Parameter(Mandatory = $true)][string]$Value)

    $decoded = $Value.Trim()
    $converged = $false
    for ($i = 0; $i -lt 6; $i++) {
        try { $next = [Uri]::UnescapeDataString($decoded) } catch { return $null }
        if ($next -eq $decoded) {
            $converged = $true
            break
        }
        $decoded = $next
    }
    if (-not $converged) { return $null }
    $decoded = $decoded.Replace([char]0x3002, '.').Replace([char]0xFF0E, '.').Replace([char]0xFF61, '.')
    $uri = $null
    if (-not [Uri]::TryCreate($decoded, [UriKind]::Absolute, [ref]$uri)) { return $null }
    if ($uri.Scheme.ToLowerInvariant() -notin @('http', 'https')) { return $null }
    if (-not [string]::IsNullOrEmpty($uri.UserInfo)) { return $null }
    try {
        $idn = [Globalization.IdnMapping]::new()
        $normalizedHost = $idn.GetAscii($uri.DnsSafeHost.Replace([char]0x3002, '.').Replace([char]0xFF0E, '.').Replace([char]0xFF61, '.').TrimEnd('.')).ToLowerInvariant()
        if ([string]::IsNullOrWhiteSpace($normalizedHost)) { return $null }
        $port = $uri.Port
    } catch {
        return $null
    }
    if ($normalizedHost -eq 'anthropic.com' -or $normalizedHost.EndsWith('.anthropic.com', [StringComparison]::Ordinal)) { return $null }
    try {
        $builder = [UriBuilder]::new($uri)
        $builder.Scheme = $uri.Scheme.ToLowerInvariant()
        $builder.Host = $normalizedHost
        $builder.Port = if ($uri.IsDefaultPort) { -1 } else { $port }
        return $builder.Uri.AbsoluteUri
    } catch {
        return $null
    }
}

function Test-OmegaCompatibleEndpoint {
    param([Parameter(Mandatory = $true)][string]$Value)
    return $null -ne (ConvertTo-OmegaCanonicalEndpoint -Value $Value)
}

# Returns only variable names/reasons; it never returns credential or URL values.
function Get-OmegaEnvironmentPolicyViolations {
    param([Parameter(Mandatory = $true)][string]$Content)

    $violations = @()
    if ($Content -match "(?im)^\s*ANTHROPIC_API_KEY\s*=") {
        $violations += "ANTHROPIC_API_KEY is forbidden"
    }
    $endpointPattern = "(?im)^\s*([A-Z0-9_]*(?:BASE_URL|ENDPOINT|MODELS_URL|HOST))\s*=\s*([^#\r\n]*)"
    foreach ($match in [regex]::Matches($Content, $endpointPattern)) {
        $name = $match.Groups[1].Value
        $value = $match.Groups[2].Value.Trim()
        if ($value -and -not (Test-OmegaCompatibleEndpoint -Value $value)) {
            $violations += "$name failed endpoint policy"
        }
    }
    return $violations
}
