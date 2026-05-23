Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$eaDir = Split-Path -Parent $PSScriptRoot
$eaPath = Join-Path $eaDir "USDJPY_SR_Breakout_RiskGuard_EA.mq5"

if (-not (Test-Path -LiteralPath $eaPath)) {
    Write-Error "EA file not found: $eaPath"
}

$text = Get-Content -Raw -Encoding UTF8 -LiteralPath $eaPath
$checks = @()

function Add-Check {
    param(
        [string]$Name,
        [bool]$Passed,
        [string]$Detail
    )

    $script:checks += [pscustomobject]@{
        Name = $Name
        Passed = $Passed
        Detail = $Detail
    }
}

$requiredInputs = @(
    "EnableTrading",
    "NewsStopMode",
    "JSTOffsetHours",
    "RequireJPYAccount",
    "MagicNumber",
    "LotSize",
    "MaxSpreadPips",
    "SpreadCooldownMinutes",
    "MaxTradesPerDay",
    "MaxConsecutiveLossesPerDay",
    "DailyLossLimitJPY",
    "WeeklyLossLimitJPY",
    "MonthlyLossLimitJPY",
    "EmergencyFloatingLossLimitJPY",
    "MaxHoldingMinutes",
    "TradeStartHourJST",
    "TradeEndHourJST",
    "FridayNoEntryAfterHourJST",
    "ClosePositionsOnFriday",
    "FridayCloseHourJST",
    "D1LineLookbackBars",
    "H4LineLookbackBars",
    "MinLineTouches",
    "LineTolerancePips",
    "BreakoutBufferPips",
    "MinBreakoutBodyPips",
    "BigCandleAtrMultiplier",
    "MinATRPips",
    "StopBufferPips",
    "MinStopLossPips",
    "MaxStopLossPips",
    "RewardRiskRatio",
    "SlippagePoints",
    "ManagementTimerSeconds",
    "OrderComment"
)

foreach ($inputName in $requiredInputs) {
    Add-Check "input: $inputName" ($text -match "input\s+\w+\s+$inputName\b") "Required external parameter exists."
}

$presetDir = Join-Path $eaDir "presets"
if (Test-Path -LiteralPath $presetDir) {
    $presetFiles = Get-ChildItem -LiteralPath $presetDir -Filter "*.set" -File
    foreach ($preset in $presetFiles) {
        $presetText = Get-Content -Encoding UTF8 -LiteralPath $preset.FullName
        $presetNames = @(
            $presetText |
                Where-Object { $_ -match "\S" -and $_ -notmatch "^\s*[;#]" } |
                ForEach-Object { ($_ -split "=", 2)[0].Trim() }
        )

        $missingInPreset = @($requiredInputs | Where-Object { $_ -notin $presetNames })
        $unknownInPreset = @($presetNames | Where-Object { $_ -notin $requiredInputs })

        Add-Check "preset complete: $($preset.Name)" ($missingInPreset.Count -eq 0) ("missing=" + (($missingInPreset -join ",") -replace "^$", "none"))
        Add-Check "preset names: $($preset.Name)" ($unknownInPreset.Count -eq 0) ("unknown=" + (($unknownInPreset -join ",") -replace "^$", "none"))
    }
}
else {
    Add-Check "preset directory" $false "Missing presets directory."
}

$openBraces = ([regex]::Matches($text, "\{")).Count
$closeBraces = ([regex]::Matches($text, "\}")).Count
Add-Check "brace balance" ($openBraces -eq $closeBraces) "open=$openBraces close=$closeBraces"

Add-Check "USDJPY lock" ($text -match 'const\s+string\s+TARGET_SYMBOL\s*=\s*"USDJPY"') "TARGET_SYMBOL is fixed to USDJPY."
Add-Check "non-target OnTick guard" ($text -match 'void\s+OnTick\s*\(\)\s*\{\s*if\(!g_symbol_allowed\)') "OnTick exits before management or entries on non-target symbols."
Add-Check "pip digit handling" ($text -match 'if\(_Digits\s*==\s*3\s*\|\|\s*_Digits\s*==\s*5\)') "3/5 digit symbols use _Point * 10."
Add-Check "JST conversion" ($text -match 'server_time\s*\+\s*JSTOffsetHours\s*\*\s*3600') "Server time is offset to JST by input."
Add-Check "JPY account guard" ($text -match 'RequireJPYAccount' -and $text -match 'ACCOUNT_CURRENCY' -and $text -match 'Account currency must be JPY') "Non-JPY accounts can be blocked from new entries."
Add-Check "spread cooldown" ($text -match 'g_last_spread_block_time' -and $text -match 'SpreadCooldownMinutes') "Wide-spread events trigger a temporary entry cooldown."
Add-Check "D1/H4 line detection" ($text -match 'PERIOD_D1' -and $text -match 'PERIOD_H4' -and $text -match 'MinLineTouches') "Higher-timeframe SR line detection exists."
Add-Check "M15 confirmed break" ($text -match 'm15_bar_1' -and $text -match 'm15_bar_2' -and $text -match 'BreakoutBufferPips') "M15 closed-bar breakout logic exists."
Add-Check "body-based line" ($text -match 'body_high' -and $text -match 'body_low') "Line detection uses candle bodies."
Add-Check "RR dynamic TP" ($text -match 'RewardRiskRatio' -and $text -match 'take_profit = NormalizeDouble') "TP is derived from stop distance."
Add-Check "single position gate" ($text -match 'CountSymbolPositions\(\)\s*>\s*0') "Any USDJPY position blocks new entries."
Add-Check "MagicNumber management" ($text -match 'POSITION_MAGIC' -and $text -match 'DEAL_MAGIC') "Open positions and history are filtered by magic number."
Add-Check "history risk rebuild" ($text -match 'HistorySelect\(0,\s*now_server\)') "Risk state is rebuilt from account history."
Add-Check "fee-inclusive PnL" ($text -match 'DEAL_COMMISSION' -and $text -match 'DEAL_SWAP') "Risk PnL includes commission and swap."
Add-Check "emergency floating loss close" ($text -match 'EmergencyFloatingLossLimitJPY' -and $text -match 'POSITION_PROFIT' -and $text -match 'Emergency floating loss limit reached') "Managed positions have an emergency floating-loss brake."
Add-Check "Friday close protection" ($text -match 'ShouldForceFridayClose' -and $text -match 'CloseAllManagedPositions\("Friday close protection\."\)') "Friday close path exists."
Add-Check "max holding close" ($text -match 'MaxHoldingMinutes' -and $text -match 'CloseManagedPosition\("MaxHoldingMinutes exceeded\."\)') "Max holding close path exists."
Add-Check "timer management" ($text -match 'EventSetTimer\(ManagementTimerSeconds\)' -and $text -match 'void\s+OnTimer') "Position management also runs on timer."
Add-Check "fixed lot only" ($text -match 'double\s+volume\s*=\s*LotSize;' -and $text -notmatch 'LotSize\s*[\*\+]' -and $text -notmatch 'volume\s*[\*\+]=') "No visible lot escalation pattern."
Add-Check "order error log" ($text -match '\[ORDER_FAIL\]' -and $text -match 'ResultRetcodeDescription') "Order failures log retcode and description."
Add-Check "block reason log" ($text -match 'void\s+LogBlock' -and $text -match '\[BLOCK\]') "Entry block reasons are logged."

$checks | Format-Table -AutoSize

$failed = @($checks | Where-Object { -not $_.Passed })
if ($failed.Count -gt 0) {
    Write-Host ""
    Write-Host "Static check failed: $($failed.Count) issue(s)." -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "Static check passed. MetaEditor compile is still required for final MQL5 validation." -ForegroundColor Green
