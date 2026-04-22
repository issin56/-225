from __future__ import annotations

import argparse
import json
import re
from datetime import datetime
from pathlib import Path
from typing import Any


LEADER_PATTERNS = (
    re.compile(r"Current strongest portfolio remains `([^`]+)`"),
    re.compile(r"Current strongest portfolio is `([^`]+)`"),
    re.compile(r"Current leader remains `([^`]+)`"),
)
DATE_PATTERN = re.compile(r"(\d{4}-\d{2}-\d{2})")


def _latest_matching_file(directory: Path, pattern: str) -> Path | None:
    candidates = list(directory.glob(pattern))
    if not candidates:
        return None
    return max(candidates, key=lambda path: path.stat().st_mtime)


def _load_json(path: Path | None) -> Any:
    if path is None or not path.exists():
        return None
    return json.loads(path.read_text(encoding="utf-8"))


def _extract_leader_name(snapshot_text: str) -> str | None:
    for pattern in LEADER_PATTERNS:
        match = pattern.search(snapshot_text)
        if match:
            return match.group(1)
    return None


def _matching_leader_files(results_dir: Path, leader_name: str, prefix: str) -> list[Path]:
    def _leader_tokens(name: str) -> list[str]:
        tokens = {name}
        if name.startswith("lot3_base10_june_t8_"):
            tokens.add(name.removeprefix("lot3_base10_june_t8_"))
        normalized = {token.replace("_", "-") for token in tokens}
        tokens.update(normalized)
        return sorted(tokens, key=len, reverse=True)

    leader_tokens = _leader_tokens(leader_name)
    candidates = [
        path
        for path in results_dir.glob(f"{prefix}*.json")
        if any(token in path.stem for token in leader_tokens)
    ]
    if not candidates:
        return []

    exact_suffix = f"-{leader_name}"
    exact_suffixes = {f"-{token}" for token in leader_tokens}
    exact = [path for path in candidates if any(path.stem.endswith(suffix) for suffix in exact_suffixes)]
    if exact:
        return sorted(exact, key=lambda path: path.stat().st_mtime, reverse=True)

    if prefix.startswith("validation-"):
        gated_markers = {f"-{token}-" for token in leader_tokens}
        gated = [path for path in candidates if any(marker in path.stem for marker in gated_markers)]
        if gated:
            return sorted(gated, key=lambda path: path.stat().st_mtime, reverse=True)

    return sorted(candidates, key=lambda path: path.stat().st_mtime, reverse=True)


def _extract_date_token(path: Path | None) -> str | None:
    if path is None:
        return None
    match = DATE_PATTERN.search(path.stem)
    return match.group(1) if match else None


def _latest_with_date(paths: list[Path], date_token: str) -> Path | None:
    dated = [path for path in paths if _extract_date_token(path) == date_token]
    if not dated:
        return None
    return max(dated, key=lambda path: path.stat().st_mtime)


def _select_leader_bundle(results_dir: Path, leader_name: str) -> tuple[Path | None, Path | None, Path | None, str | None, bool]:
    result_files = _matching_leader_files(results_dir, leader_name, "portfolio-research-")
    validation_files = _matching_leader_files(results_dir, leader_name, "validation-")
    diagnostics_files = _matching_leader_files(results_dir, leader_name, "portfolio-diagnostics-")

    common_dates = (
        {_extract_date_token(path) for path in result_files}
        & {_extract_date_token(path) for path in validation_files}
        & {_extract_date_token(path) for path in diagnostics_files}
    )
    common_dates.discard(None)

    if common_dates:
        bundle_date = sorted(common_dates)[-1]
        return (
            _latest_with_date(result_files, bundle_date),
            _latest_with_date(validation_files, bundle_date),
            _latest_with_date(diagnostics_files, bundle_date),
            bundle_date,
            True,
        )

    return (
        result_files[0] if result_files else None,
        validation_files[0] if validation_files else None,
        diagnostics_files[0] if diagnostics_files else None,
        None,
        False,
    )


def _recent_summary_files(results_dir: Path, limit: int = 6) -> list[Path]:
    candidates = [path for path in results_dir.glob("*.json") if "summary" in path.stem]
    return sorted(candidates, key=lambda path: path.stat().st_mtime, reverse=True)[:limit]


def _recent_result_files(results_dir: Path, limit: int = 12) -> list[Path]:
    candidates = list(results_dir.glob("*.json"))
    return sorted(candidates, key=lambda path: path.stat().st_mtime, reverse=True)[:limit]


def _relative_link(base_file: Path, target: Path) -> str:
    try:
        relative = target.relative_to(base_file.parent.parent)
        return relative.as_posix()
    except ValueError:
        try:
            return target.relative_to(base_file.parent).as_posix()
        except ValueError:
            return target.as_posix()


def _format_months(items: list[dict[str, Any]] | None) -> list[str]:
    if not items:
        return ["- none"]
    lines = []
    for item in items[:5]:
        month = item.get("month", "?")
        pnl = item.get("pnl", "?")
        lines.append(f"- `{month}`: `{pnl}`")
    return lines


def _format_candidate_names(names: list[str] | None) -> list[str]:
    if not names:
        return ["- none"]
    return [f"- `{name}`" for name in names]


def _format_summary_entry(base_file: Path, path: Path) -> list[str]:
    data = _load_json(path)
    link = _relative_link(base_file, path)
    lines = [f"- [{path.name}]({link})"]
    if isinstance(data, list):
        lines.append(f"  entries: `{len(data)}`")
        if data and isinstance(data[0], dict):
            preview = data[0]
            if preview.get("name"):
                lines.append(f"  first_entry: `{preview.get('name')}`")
        return lines
    if not isinstance(data, dict):
        return lines
    decision = data.get("decision")
    if isinstance(decision, str) and decision:
        lines.append(f"  decision: `{decision}`")
    best_new = data.get("best_new_candidate")
    if isinstance(best_new, dict) and best_new.get("name"):
        lines.append(
            "  best_new_candidate: "
            f"`{best_new.get('name')}` / profit `{best_new.get('profit')}` / "
            f"DD `{best_new.get('max_drawdown')}` / win_rate `{best_new.get('win_rate')}`"
        )
    baseline = data.get("baseline")
    if isinstance(baseline, dict) and baseline.get("name"):
        lines.append(f"  baseline: `{baseline.get('name')}`")
    return lines


def build_dashboard_markdown(docs_dir: Path, results_dir: Path, output_path: Path) -> str:
    latest_snapshot = _latest_matching_file(docs_dir, "RESEARCH_SNAPSHOT_*.md")
    snapshot_text = latest_snapshot.read_text(encoding="utf-8") if latest_snapshot else ""
    leader_name = _extract_leader_name(snapshot_text)

    if leader_name:
        leader_result_path, leader_validation_path, leader_diagnostics_path, bundle_date, exact_bundle = _select_leader_bundle(
            results_dir, leader_name
        )
    else:
        leader_result_path = None
        leader_validation_path = None
        leader_diagnostics_path = None
        bundle_date = None
        exact_bundle = False

    leader_result = _load_json(leader_result_path) or {}
    leader_validation = _load_json(leader_validation_path) or {}
    leader_diagnostics = _load_json(leader_diagnostics_path) or {}

    recent_summaries = _recent_summary_files(results_dir)
    recent_results = _recent_result_files(results_dir)

    generated_at = datetime.now().astimezone().isoformat(timespec="seconds")
    lines: list[str] = [
        "# Current Research Status",
        "",
        f"Generated: `{generated_at}`",
        "",
        "## Current Leader",
    ]

    if leader_name:
        lines.append(f"- name: `{leader_name}`")
    else:
        lines.append("- name: `unknown`")
    if bundle_date:
        lines.append(f"- bundle_date: `{bundle_date}`")
        lines.append("- bundle_mode: `matched result/validation/diagnostics set`")
    elif leader_name and not exact_bundle:
        lines.append("- bundle_mode: `mixed latest files (no exact matched set found)`")

    if leader_result_path:
        lines.append(f"- result: [{leader_result_path.name}]({_relative_link(output_path, leader_result_path)})")
    if leader_validation_path:
        lines.append(f"- validation: [{leader_validation_path.name}]({_relative_link(output_path, leader_validation_path)})")
    if leader_diagnostics_path:
        lines.append(f"- diagnostics: [{leader_diagnostics_path.name}]({_relative_link(output_path, leader_diagnostics_path)})")

    if leader_result:
        lines.extend(
            [
                f"- profit: `{leader_result.get('profit')}`",
                f"- max_drawdown: `{leader_result.get('max_drawdown')}`",
                f"- win_rate: `{leader_result.get('win_rate')}`",
                f"- trades: `{leader_result.get('trades')}`",
                f"- profitable_months: `{leader_result.get('profitable_months')}`",
                f"- losing_months: `{leader_result.get('losing_months')}`",
                f"- average_monthly_pnl: `{leader_result.get('average_monthly_pnl')}`",
            ]
        )

    lines.extend(
        [
            "",
            "## Leader Candidate Set",
            *_format_candidate_names(leader_result.get("candidate_names")),
            "",
            "## Weak Months",
            *_format_months(leader_diagnostics.get("worst_months")),
        ]
    )

    validation_summary = leader_validation.get("summary", {}) if isinstance(leader_validation, dict) else {}
    lines.extend(
        [
            "",
            "## Validation",
            f"- tested_windows: `{validation_summary.get('tested_windows', 'n/a')}`",
            f"- accepted_both_windows: `{validation_summary.get('accepted_both_windows', 'n/a')}`",
            f"- total_test_profit: `{validation_summary.get('total_test_profit', 'n/a')}`",
            f"- average_test_win_rate: `{validation_summary.get('average_test_win_rate', 'n/a')}`",
            f"- worst_test_drawdown: `{validation_summary.get('worst_test_drawdown', 'n/a')}`",
        ]
    )

    lines.extend(["", "## Latest Snapshot"])
    if latest_snapshot:
        lines.append(f"- snapshot: [{latest_snapshot.name}]({_relative_link(output_path, latest_snapshot)})")
        lines.append("")
        lines.append("```md")
        lines.extend(snapshot_text.strip().splitlines()[:24])
        lines.append("```")
    else:
        lines.append("- snapshot: `not found`")

    lines.extend(["", "## Recent Batch Summaries"])
    if recent_summaries:
        for path in recent_summaries:
            lines.extend(_format_summary_entry(output_path, path))
    else:
        lines.append("- none")

    lines.extend(["", "## Recent Result Files"])
    for path in recent_results:
        timestamp = datetime.fromtimestamp(path.stat().st_mtime).strftime("%Y-%m-%d %H:%M:%S")
        lines.append(f"- `{timestamp}` [{path.name}]({_relative_link(output_path, path)})")

    lines.append("")
    return "\n".join(lines)


def write_dashboard(docs_dir: Path, results_dir: Path, output_path: Path) -> str:
    rendered = build_dashboard_markdown(docs_dir, results_dir, output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(rendered, encoding="utf-8")
    return rendered


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--docs-dir", default="docs")
    parser.add_argument("--results-dir", default="results")
    parser.add_argument("--output", default="docs/CURRENT_RESEARCH_STATUS.md")
    args = parser.parse_args()

    docs_dir = Path(args.docs_dir)
    results_dir = Path(args.results_dir)
    output_path = Path(args.output)
    print(write_dashboard(docs_dir, results_dir, output_path))


if __name__ == "__main__":
    main()
