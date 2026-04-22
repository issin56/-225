param(
    [string]$StartDate = "2023-01-01",
    [string]$EndDate = "",
    [string]$Output = "data/external_factors.macro.fred.csv"
)

$args = @(
    "-3.11",
    "-m",
    "kanekasegi.fred_factors",
    "--series-id", "SP500",
    "--factor-name", "sp500_change",
    "--output", $Output,
    "--start-date", $StartDate,
    "--value-mode", "pct_change"
)

if ($EndDate -ne "") {
    $args += @("--end-date", $EndDate)
}

py @args
