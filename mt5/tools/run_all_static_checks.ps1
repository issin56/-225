Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$mt5Dir = Split-Path -Parent $PSScriptRoot
$checkScripts = Get-ChildItem -Path $mt5Dir -Recurse -Filter "static_check.ps1" -File |
    Where-Object { $_.FullName -notlike "*\mt5\tools\*" } |
    Sort-Object FullName

if ($checkScripts.Count -eq 0) {
    Write-Error "No EA static_check.ps1 scripts were found under $mt5Dir"
}

$failed = @()

foreach ($script in $checkScripts) {
    $eaDir = Split-Path -Parent (Split-Path -Parent $script.FullName)
    Write-Host ""
    Write-Host "==> Running static check: $eaDir" -ForegroundColor Cyan

    & powershell -ExecutionPolicy Bypass -File $script.FullName
    if ($LASTEXITCODE -ne 0) {
        $failed += $script.FullName
    }
}

Write-Host ""
if ($failed.Count -gt 0) {
    Write-Host "One or more static checks failed:" -ForegroundColor Red
    $failed | ForEach-Object { Write-Host " - $_" -ForegroundColor Red }
    exit 1
}

Write-Host "All MT5 static checks passed. MetaEditor compile is still required." -ForegroundColor Green
