[CmdletBinding(SupportsShouldProcess = $true)]
param(
    [Parameter(Mandatory = $true)]
    [string]$Mt5DataFolder
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$eaDir = Split-Path -Parent $PSScriptRoot
$sourceEa = Join-Path $eaDir "USDJPY_SR_Breakout_RiskGuard_EA.mq5"
$sourcePresetDir = Join-Path $eaDir "presets"

$resolvedDataFolder = Resolve-Path -LiteralPath $Mt5DataFolder
$mql5Folder = Join-Path $resolvedDataFolder "MQL5"

if (-not (Test-Path -LiteralPath $mql5Folder)) {
    Write-Error "MQL5 folder was not found under MT5 data folder: $mql5Folder"
}

$expertDest = Join-Path $mql5Folder "Experts\USDJPY_SR_Breakout_RiskGuard"
$testerPresetDest = Join-Path $mql5Folder "Profiles\Tester"

if ($PSCmdlet.ShouldProcess($expertDest, "Create EA destination folder")) {
    New-Item -ItemType Directory -Force -Path $expertDest | Out-Null
}

if ($PSCmdlet.ShouldProcess($testerPresetDest, "Create tester preset destination folder")) {
    New-Item -ItemType Directory -Force -Path $testerPresetDest | Out-Null
}

if ($PSCmdlet.ShouldProcess($expertDest, "Copy EA source")) {
    Copy-Item -LiteralPath $sourceEa -Destination $expertDest -Force
}

if (Test-Path -LiteralPath $sourcePresetDir) {
    foreach ($preset in Get-ChildItem -LiteralPath $sourcePresetDir -Filter "*.set" -File) {
        if ($PSCmdlet.ShouldProcess($testerPresetDest, "Copy preset $($preset.Name)")) {
            Copy-Item -LiteralPath $preset.FullName -Destination $testerPresetDest -Force
        }
    }
}

Write-Host "Install helper finished."
Write-Host "EA destination: $expertDest"
Write-Host "Preset destination: $testerPresetDest"
Write-Host "Next: open MetaEditor, compile USDJPY_SR_Breakout_RiskGuard_EA.mq5, then restart MT5 or refresh Navigator."
