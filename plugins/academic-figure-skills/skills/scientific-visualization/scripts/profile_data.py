#!/usr/bin/env python3
"""Read-only, deterministic CSV/TSV profiler for figure planning.

The profiler reports observable structure and explicitly labelled heuristics. It
does not clean data, infer an independent replicate, select a statistical test,
or recommend a chart.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import math
import sys
from collections import Counter
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any, Iterable

from _common import (
    MAX_REPORT_BYTES,
    CliError,
    atomic_write_bytes,
    checked_input_file,
    emit_json,
    positive_float,
    positive_int,
)

SCHEMA_VERSION = "1.0"
TOOL_VERSION = "1.0"
SUPPORTED_SUFFIXES = {".csv": ",", ".tsv": "\t"}
DEFAULT_MAX_CATEGORIES = 100
DEFAULT_MAX_DUPLICATE_ROWS = 100_000
DEFAULT_MISSING_REVIEW_RATE = 0.20
DEFAULT_SKEW_REVIEW = 1.0
DEFAULT_SCALE_SPAN_REVIEW = 100.0


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _finite_float(value: str) -> float | None:
    try:
        parsed = float(value.strip())
    except ValueError:
        return None
    return parsed if math.isfinite(parsed) else None


def _is_nonfinite_number(value: str) -> bool:
    try:
        return not math.isfinite(float(value.strip()))
    except ValueError:
        return False


def _is_iso_datetime(value: str) -> bool:
    candidate = value.strip()
    if not candidate or not any(token in candidate for token in ("-", "/", ":", "T")):
        return False
    try:
        datetime.fromisoformat(candidate.replace("Z", "+00:00").replace("/", "-"))
    except ValueError:
        return False
    return True


@dataclass
class OnlineMoments:
    count: int = 0
    mean: float = 0.0
    m2: float = 0.0
    m3: float = 0.0
    minimum: float = math.inf
    maximum: float = -math.inf
    zero_count: int = 0
    negative_count: int = 0

    def add(self, value: float) -> None:
        previous_count = self.count
        self.count += 1
        delta = value - self.mean
        delta_n = delta / self.count
        term = delta * delta_n * previous_count
        self.m3 += (
            term * delta_n * (self.count - 2)
            - 3.0 * delta_n * self.m2
        )
        self.m2 += term
        self.mean += delta_n
        self.minimum = min(self.minimum, value)
        self.maximum = max(self.maximum, value)
        self.zero_count += value == 0
        self.negative_count += value < 0

    def summary(self) -> dict[str, Any]:
        if not self.count:
            return {}
        standard_deviation = (
            math.sqrt(self.m2 / (self.count - 1)) if self.count > 1 else 0.0
        )
        skewness = None
        if self.count >= 3 and self.m2 > 0:
            skewness = math.sqrt(self.count) * self.m3 / (self.m2 ** 1.5)
        return {
            "count_finite": self.count,
            "mean": self.mean,
            "standard_deviation_sample": standard_deviation,
            "minimum": self.minimum,
            "maximum": self.maximum,
            "skewness_moment": skewness,
            "zero_count": self.zero_count,
            "negative_count": self.negative_count,
        }


@dataclass
class ColumnAccumulator:
    name: str
    max_categories: int
    total: int = 0
    missing: int = 0
    numeric_count: int = 0
    nonfinite_numeric_count: int = 0
    datetime_count: int = 0
    boolean_count: int = 0
    min_text_length: int | None = None
    max_text_length: int = 0
    values: Counter[str] = field(default_factory=Counter)
    unique_overflow: bool = False
    moments: OnlineMoments = field(default_factory=OnlineMoments)

    def add(self, value: str, missing_values: set[str]) -> None:
        self.total += 1
        if value in missing_values:
            self.missing += 1
            return

        length = len(value)
        self.min_text_length = (
            length if self.min_text_length is None else min(self.min_text_length, length)
        )
        self.max_text_length = max(self.max_text_length, length)

        if not self.unique_overflow:
            self.values[value] += 1
            if len(self.values) > self.max_categories:
                self.unique_overflow = True
                self.values.clear()

        parsed = _finite_float(value)
        if parsed is not None:
            self.numeric_count += 1
            self.moments.add(parsed)
        elif _is_nonfinite_number(value):
            self.numeric_count += 1
            self.nonfinite_numeric_count += 1

        self.datetime_count += _is_iso_datetime(value)
        self.boolean_count += value.strip().lower() in {"true", "false"}

    @property
    def non_missing(self) -> int:
        return self.total - self.missing

    def inferred_type(self) -> tuple[str, str]:
        if self.non_missing == 0:
            return "unknown", "no non-missing values"
        if self.numeric_count == self.non_missing:
            return "numeric", "all non-missing values parse as numbers"
        if self.boolean_count == self.non_missing:
            return "boolean", "all non-missing values are true/false tokens"
        if self.datetime_count == self.non_missing:
            return "datetime", "all non-missing values parse as ISO-like datetimes"
        if not self.unique_overflow:
            return "categorical", "distinct values are within the configured reporting cap"
        return "text_or_identifier", "distinct values exceed the configured reporting cap"

    def report(self) -> dict[str, Any]:
        inferred, basis = self.inferred_type()
        result: dict[str, Any] = {
            "name": self.name,
            "inferred_type": inferred,
            "type_inference_basis": basis,
            "count_total": self.total,
            "count_non_missing": self.non_missing,
            "count_missing": self.missing,
            "missing_rate": self.missing / self.total if self.total else 0.0,
            "distinct": {
                "status": "above_cap" if self.unique_overflow else "exact",
                "count": None if self.unique_overflow else len(self.values),
                "cap": self.max_categories,
            },
            "text_length": {
                "minimum": self.min_text_length,
                "maximum": self.max_text_length if self.non_missing else None,
            },
        }
        if not self.unique_overflow:
            result["value_counts"] = [
                {"value": value, "count": count}
                for value, count in sorted(
                    self.values.items(), key=lambda item: (-item[1], item[0])
                )[:20]
            ]
        if inferred == "numeric":
            result["numeric"] = self.moments.summary()
            result["numeric"]["count_nonfinite"] = self.nonfinite_numeric_count
        return result


def _risk(
    code: str,
    message: str,
    *,
    column: str | None = None,
    evidence: dict[str, Any] | None = None,
    heuristic: dict[str, Any] | None = None,
) -> dict[str, Any]:
    item: dict[str, Any] = {
        "code": code,
        "level": "review",
        "message": message,
    }
    if column is not None:
        item["column"] = column
    if evidence:
        item["evidence"] = evidence
    if heuristic:
        item["heuristic"] = heuristic
    return item


def _column_risks(
    accumulator: ColumnAccumulator,
    column: dict[str, Any],
    *,
    missing_review_rate: float,
    skew_review: float,
    scale_span_review: float,
) -> list[dict[str, Any]]:
    risks: list[dict[str, Any]] = []
    name = accumulator.name
    if column["count_missing"]:
        risks.append(
            _risk(
                "missing_values_present",
                "Missing values are present; confirm their meaning and plotting treatment.",
                column=name,
                evidence={
                    "count": column["count_missing"],
                    "rate": column["missing_rate"],
                },
            )
        )
    if column["missing_rate"] >= missing_review_rate:
        risks.append(
            _risk(
                "missing_rate_heuristic",
                "Missingness meets the configured review threshold; this is not a deletion or imputation rule.",
                column=name,
                evidence={"rate": column["missing_rate"]},
                heuristic={"threshold": missing_review_rate, "comparison": ">="},
            )
        )
    if column["count_non_missing"] and column["distinct"]["status"] == "exact":
        if column["distinct"]["count"] == 1:
            risks.append(
                _risk(
                    "constant_column",
                    "All observed non-missing values are identical.",
                    column=name,
                    evidence={"distinct_count": 1},
                )
            )
    if column["inferred_type"] == "numeric":
        numeric = column["numeric"]
        if numeric.get("count_nonfinite"):
            risks.append(
                _risk(
                    "nonfinite_numeric_values",
                    "Numeric tokens include NaN or infinity; confirm how they should be represented.",
                    column=name,
                    evidence={"count": numeric["count_nonfinite"]},
                )
            )
        skewness = numeric.get("skewness_moment")
        if skewness is not None and abs(skewness) >= skew_review:
            risks.append(
                _risk(
                    "skewness_heuristic",
                    "The observed numeric distribution meets the configured skewness review threshold.",
                    column=name,
                    evidence={"skewness_moment": skewness},
                    heuristic={"absolute_threshold": skew_review, "comparison": ">="},
                )
            )
        minimum = numeric.get("minimum")
        maximum = numeric.get("maximum")
        if minimum is not None and minimum > 0 and maximum / minimum >= scale_span_review:
            risks.append(
                _risk(
                    "positive_scale_span_heuristic",
                    "Positive values span the configured ratio; review scale "
                    "choice without transforming automatically.",
                    column=name,
                    evidence={"minimum": minimum, "maximum": maximum, "ratio": maximum / minimum},
                    heuristic={"ratio_threshold": scale_span_review, "comparison": ">="},
                )
            )
        if column["distinct"]["status"] == "exact" and column["distinct"]["count"] <= 7:
            risks.append(
                _risk(
                    "low_cardinality_numeric",
                    "A numeric column has few distinct values; confirm whether it "
                    "is a measurement, code, or ordered category.",
                    column=name,
                    evidence={"distinct_count": column["distinct"]["count"]},
                    heuristic={"threshold": 7, "comparison": "<="},
                )
            )
    if 0 < accumulator.numeric_count < accumulator.non_missing:
        risks.append(
            _risk(
                "mixed_numeric_and_text",
                "Only some non-missing values parse as finite numbers; confirm the column semantics.",
                column=name,
                evidence={
                    "numeric_like_count": accumulator.numeric_count,
                    "non_missing_count": accumulator.non_missing,
                },
            )
        )
    return risks


def profile_file(
    source: str | Path,
    *,
    group_columns: Iterable[str] = (),
    missing_values: Iterable[str] = ("",),
    max_categories: int = DEFAULT_MAX_CATEGORIES,
    max_duplicate_rows: int = DEFAULT_MAX_DUPLICATE_ROWS,
    missing_review_rate: float = DEFAULT_MISSING_REVIEW_RATE,
    skew_review: float = DEFAULT_SKEW_REVIEW,
    scale_span_review: float = DEFAULT_SCALE_SPAN_REVIEW,
) -> dict[str, Any]:
    """Profile one CSV/TSV file without modifying it."""
    path = checked_input_file(source)
    suffix = path.suffix.lower()
    if suffix not in SUPPORTED_SUFFIXES:
        raise CliError("profiler supports only .csv and .tsv files in P0")
    delimiter = SUPPORTED_SUFFIXES[suffix]
    group_columns = list(group_columns)
    missing_set = set(missing_values)
    missing_set.add("")

    row_count = 0
    duplicate_count = 0
    duplicate_rows: set[tuple[str, ...]] | None = set()
    group_counts: Counter[tuple[str, ...]] = Counter()
    group_tracking = True

    try:
        handle = path.open("r", encoding="utf-8-sig", newline="")
        with handle:
            reader = csv.reader(handle, delimiter=delimiter, strict=True)
            try:
                header = next(reader)
            except StopIteration as exc:
                raise CliError(f"input table is empty: {path}") from exc
            if not header or any(name == "" for name in header):
                raise CliError("header must contain a non-empty name for every column")
            if len(set(header)) != len(header):
                duplicates = sorted(name for name, count in Counter(header).items() if count > 1)
                raise CliError(f"header contains duplicate column names: {duplicates}")
            if len(header) > 1000:
                raise CliError("input has more than 1000 columns")
            missing_groups = [name for name in group_columns if name not in header]
            if missing_groups:
                raise CliError(f"group columns not found: {missing_groups}")
            group_indexes = [header.index(name) for name in group_columns]
            accumulators = [ColumnAccumulator(name, max_categories) for name in header]

            for line_number, row in enumerate(reader, start=2):
                if len(row) != len(header):
                    raise CliError(
                        f"row {line_number} has {len(row)} fields; expected {len(header)}"
                    )
                row_count += 1
                for accumulator, value in zip(accumulators, row):
                    accumulator.add(value, missing_set)

                if duplicate_rows is not None:
                    key = tuple(row)
                    duplicate_count += key in duplicate_rows
                    duplicate_rows.add(key)
                    if len(duplicate_rows) > max_duplicate_rows:
                        duplicate_rows = None

                if group_indexes and group_tracking:
                    group_key = tuple(row[index] for index in group_indexes)
                    group_counts[group_key] += 1
                    if len(group_counts) > max_categories:
                        group_counts.clear()
                        group_tracking = False
    except UnicodeDecodeError as exc:
        raise CliError(
            "input is not valid UTF-8/UTF-8-SIG; convert explicitly and record the conversion"
        ) from exc
    except csv.Error as exc:
        raise CliError(f"cannot parse delimited table: {exc}") from exc

    columns = [accumulator.report() for accumulator in accumulators]
    risks: list[dict[str, Any]] = []
    for accumulator, column in zip(accumulators, columns):
        risks.extend(
            _column_risks(
                accumulator,
                column,
                missing_review_rate=missing_review_rate,
                skew_review=skew_review,
                scale_span_review=scale_span_review,
            )
        )
    for name in header:
        if name != name.strip():
            risks.append(
                _risk(
                    "header_whitespace",
                    "A column name contains leading or trailing whitespace; the profiler preserves it.",
                    column=name,
                )
            )

    if duplicate_rows is None:
        duplicate_report: dict[str, Any] = {
            "status": "not_computed_above_cap",
            "cap": max_duplicate_rows,
            "count": None,
        }
    else:
        duplicate_report = {
            "status": "exact",
            "cap": max_duplicate_rows,
            "count": duplicate_count,
        }
        if duplicate_count:
            risks.append(
                _risk(
                    "duplicate_rows_present",
                    "Exact duplicate rows are present; do not remove them without confirming their meaning.",
                    evidence={"count": duplicate_count},
                )
            )

    group_summary: dict[str, Any] | None = None
    if group_columns:
        if group_tracking:
            sizes = list(group_counts.values())
            group_summary = {
                "status": "exact",
                "columns": group_columns,
                "group_count": len(group_counts),
                "minimum_rows": min(sizes) if sizes else 0,
                "maximum_rows": max(sizes) if sizes else 0,
                "counts": [
                    {"key": list(key), "count": count}
                    for key, count in sorted(group_counts.items(), key=lambda item: item[0])
                ],
                "notice": (
                    "Row counts are not independent-replicate counts unless the "
                    "contract establishes that equivalence."
                ),
            }
        else:
            group_summary = {
                "status": "not_computed_above_cap",
                "columns": group_columns,
                "cap": max_categories,
                "notice": "Increase the explicit cap only after confirming that detailed group counts are needed.",
            }

    return {
        "source": {
            "path": str(path),
            "sha256": _sha256(path),
            "size_bytes": path.stat().st_size,
            "format": suffix.lstrip("."),
            "encoding": "utf-8-sig",
            "delimiter": "tab" if delimiter == "\t" else "comma",
        },
        "table": {
            "row_count": row_count,
            "column_count": len(header),
            "columns": columns,
            "duplicate_rows": duplicate_report,
            "group_summary": group_summary,
        },
        "risks": sorted(risks, key=lambda item: (item["code"], item.get("column", ""))),
    }


def profile_sources(sources: Iterable[str | Path], **kwargs: Any) -> dict[str, Any]:
    normalized_kwargs = dict(kwargs)
    for key in ("group_columns", "missing_values"):
        if key in normalized_kwargs:
            normalized_kwargs[key] = list(normalized_kwargs[key])
    profiles = [profile_file(source, **normalized_kwargs) for source in sources]
    if not profiles:
        raise CliError("at least one input file is required")
    return {
        "schema_version": SCHEMA_VERSION,
        "tool": {"name": "profile_data.py", "version": TOOL_VERSION},
        "settings": {
            "read_only": True,
            "files_profiled_separately": True,
            "missing_values": sorted(
                set(normalized_kwargs.get("missing_values", ("",))) | {""}
            ),
            "max_categories": normalized_kwargs.get(
                "max_categories", DEFAULT_MAX_CATEGORIES
            ),
            "max_duplicate_rows": normalized_kwargs.get(
                "max_duplicate_rows", DEFAULT_MAX_DUPLICATE_ROWS
            ),
            "heuristics": {
                "missing_review_rate": normalized_kwargs.get(
                    "missing_review_rate", DEFAULT_MISSING_REVIEW_RATE
                ),
                "absolute_skewness_review": normalized_kwargs.get(
                    "skew_review", DEFAULT_SKEW_REVIEW
                ),
                "positive_scale_span_review": normalized_kwargs.get(
                    "scale_span_review", DEFAULT_SCALE_SPAN_REVIEW
                ),
            },
        },
        "profiles": profiles,
        "limitations": [
            "Types are lexical inferences and must be checked against variable semantics.",
            "Row and group counts are not independent-replicate counts unless the figure contract says so.",
            "Risk records are review prompts, not cleaning instructions or scientific conclusions.",
            "No statistical test, imputation, transformation, join, or chart selection is performed.",
        ],
        "notice": "The profiler did not modify source data and does not certify scientific validity.",
    }


def _markdown_text(value: Any) -> str:
    return str(value).replace("|", "\\|").replace("\n", " ")


def render_markdown(document: dict[str, Any]) -> str:
    """Derive a human-readable report from the authoritative JSON document."""
    lines = ["# Data profile", ""]
    for profile in document["profiles"]:
        source = profile["source"]
        table = profile["table"]
        lines.extend(
            [
                f"## `{_markdown_text(source['path'])}`",
                "",
                f"- SHA-256: `{source['sha256']}`",
                f"- Shape: {table['row_count']} rows x {table['column_count']} columns",
                f"- Parse: {source['encoding']}, {source['delimiter']} delimiter",
                "",
                "| Column | Inferred type | Non-missing | Missing | Summary |",
                "|---|---:|---:|---:|---|",
            ]
        )
        for column in table["columns"]:
            summary = column["type_inference_basis"]
            if column["inferred_type"] == "numeric":
                numeric = column["numeric"]
                summary = (
                    f"range [{numeric.get('minimum')}, {numeric.get('maximum')}], "
                    f"mean {numeric.get('mean')}, sample SD {numeric.get('standard_deviation_sample')}"
                )
            lines.append(
                "| {name} | {kind} | {nonmissing} | {missing} ({rate:.1%}) | {summary} |".format(
                    name=_markdown_text(column["name"]),
                    kind=column["inferred_type"],
                    nonmissing=column["count_non_missing"],
                    missing=column["count_missing"],
                    rate=column["missing_rate"],
                    summary=_markdown_text(summary),
                )
            )
        lines.append("")
        if profile["risks"]:
            lines.extend(["### Review prompts", ""])
            for risk in profile["risks"]:
                location = f" `{_markdown_text(risk['column'])}`:" if risk.get("column") else ":"
                lines.append(f"- `{risk['code']}`{location} {risk['message']}")
            lines.append("")
        else:
            lines.extend(["No review prompts were emitted by the configured screens.", ""])
    lines.extend(
        [
            "## Limitations",
            "",
            *[f"- {item}" for item in document["limitations"]],
            "",
            f"> {document['notice']}",
            "",
        ]
    )
    return "\n".join(lines)


def _rate(value: str) -> float:
    parsed = positive_float(value)
    if parsed > 1:
        raise CliError("rate must be greater than 0 and at most 1")
    return parsed


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Profile UTF-8 CSV/TSV files without modifying, joining, or cleaning them."
    )
    parser.add_argument("sources", nargs="+", help="one or more .csv/.tsv files")
    parser.add_argument("--group", action="append", default=[], help="explicit grouping column; repeat as needed")
    parser.add_argument("--missing-value", action="append", default=[], help="additional exact missing-value token")
    parser.add_argument("--format", choices=("json", "markdown"), default="json")
    parser.add_argument("--output", help="output file; stdout when omitted")
    parser.add_argument("--force", action="store_true", help="allow explicit output overwrite")
    parser.add_argument("--max-categories", type=positive_int, default=DEFAULT_MAX_CATEGORIES)
    parser.add_argument("--max-duplicate-rows", type=positive_int, default=DEFAULT_MAX_DUPLICATE_ROWS)
    parser.add_argument("--missing-review-rate", type=_rate, default=DEFAULT_MISSING_REVIEW_RATE)
    parser.add_argument("--skew-review", type=positive_float, default=DEFAULT_SKEW_REVIEW)
    parser.add_argument("--scale-span-review", type=positive_float, default=DEFAULT_SCALE_SPAN_REVIEW)
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    try:
        args = parser.parse_args(argv)
        document = profile_sources(
            args.sources,
            group_columns=args.group,
            missing_values=["", *args.missing_value],
            max_categories=args.max_categories,
            max_duplicate_rows=args.max_duplicate_rows,
            missing_review_rate=args.missing_review_rate,
            skew_review=args.skew_review,
            scale_span_review=args.scale_span_review,
        )
        if args.format == "json":
            emit_json(document, output=args.output, force=args.force)
        else:
            payload = (render_markdown(document) + "\n").encode("utf-8")
            if len(payload) > MAX_REPORT_BYTES:
                raise CliError("Markdown report exceeds the report-size limit")
            if args.output:
                atomic_write_bytes(Path(args.output), payload, force=args.force)
            else:
                print(payload.decode("utf-8"), end="")
        return 0
    except CliError as exc:
        parser.exit(2, f"error: {exc}\n")


if __name__ == "__main__":
    sys.exit(main())
