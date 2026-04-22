param(
    [string]$StartDate = "2023-01-01",
    [string]$EndDate = "",
    [string]$Output = "data/external_factors.macro.fred.csv"
)

$factorSpecs = @(
    @{
        SeriesId = "DEXJPUS"
        FactorName = "usd_jpy_change"
        ValueMode = "pct_change"
    },
    @{
        SeriesId = "SP500"
        FactorName = "sp500_change"
        ValueMode = "pct_change"
    },
    @{
        SeriesId = "VIXCLS"
        FactorName = "vix_change"
        ValueMode = "diff"
    },
    @{
        SeriesId = "DGS10"
        FactorName = "us10y_change_bp"
        ValueMode = "diff"
        ValueScale = "100"
    }
)

foreach ($spec in $factorSpecs) {
    $args = @(
        "-3.11",
        "-m",
        "kanekasegi.fred_factors",
        "--series-id", $spec.SeriesId,
        "--factor-name", $spec.FactorName,
        "--output", $Output,
        "--start-date", $StartDate,
        "--value-mode", $spec.ValueMode
    )

    if ($spec.ContainsKey("ValueScale")) {
        $args += @("--value-scale", $spec.ValueScale)
    }

    if ($EndDate -ne "") {
        $args += @("--end-date", $EndDate)
    }

    py @args
}
