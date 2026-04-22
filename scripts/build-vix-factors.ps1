param(
    [string]$StartDate = "2023-01-01",
    [string]$EndDate = "",
    [string]$Output = "data/external_factors.macro.csv"
)

$args = @(
    "-3.11",
    "-m",
    "kanekasegi.fred_factors",
    "--series-id", "VIXCLS",
    "--factor-name", "vix_change",
    "--output", $Output,
    "--start-date", $StartDate,
    "--value-mode", "diff"
)

if ($EndDate -ne "") {
    $args += @("--end-date", $EndDate)
}

py @args
