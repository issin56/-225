param(
    [string]$StartDate = "2023-01-01",
    [string]$EndDate = "",
    [string]$Output = "data/external_factors.usdjpy.csv"
)

$args = @(
    "-3.11",
    "-m",
    "kanekasegi.fred_factors",
    "--series-id", "DEXJPUS",
    "--factor-name", "usd_jpy_change",
    "--output", $Output,
    "--start-date", $StartDate
)

if ($EndDate -ne "") {
    $args += @("--end-date", $EndDate)
}

py @args
