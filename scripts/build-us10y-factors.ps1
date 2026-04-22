param(
    [string]$StartDate = "2023-01-01",
    [string]$EndDate = "",
    [string]$Output = "data/external_factors.macro.csv"
)

$args = @(
    "-3.11",
    "-m",
    "kanekasegi.fred_factors",
    "--series-id", "DGS10",
    "--factor-name", "us10y_change_bp",
    "--output", $Output,
    "--start-date", $StartDate,
    "--value-mode", "diff",
    "--value-scale", "100"
)

if ($EndDate -ne "") {
    $args += @("--end-date", $EndDate)
}

py @args
