#!/usr/bin/env python3
"""Query the overlay's small, license-tracked local reference index."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Any

from _common import CliError, emit_json, load_json

SKILL_ROOT = Path(__file__).resolve().parents[1]
INDEX_PATH = SKILL_ROOT / "references" / "reference-index.json"


def load_index() -> dict[str, Any]:
    document = load_json(INDEX_PATH)
    if document.get("schema_version") != "1.0":
        raise CliError("unsupported reference-index schema_version")
    entries = document.get("entries")
    if not isinstance(entries, list):
        raise CliError("reference index entries must be a list")
    ids: set[str] = set()
    for entry in entries:
        if not isinstance(entry, dict):
            raise CliError("every reference entry must be an object")
        required = {
            "id",
            "path",
            "kind",
            "figure_types",
            "features",
            "use_when",
            "avoid_when",
            "license",
            "source",
        }
        missing = required.difference(entry)
        if missing:
            raise CliError(f"reference entry is missing fields: {sorted(missing)}")
        if entry["id"] in ids:
            raise CliError(f"duplicate reference id: {entry['id']}")
        ids.add(entry["id"])
        relative = Path(entry["path"])
        if relative.is_absolute() or ".." in relative.parts:
            raise CliError(f"reference path must stay inside the overlay: {relative}")
        resolved = (SKILL_ROOT / relative).resolve()
        try:
            resolved.relative_to(SKILL_ROOT)
        except ValueError as exc:
            raise CliError(f"reference escapes overlay root: {relative}") from exc
        if not resolved.is_file() or resolved.is_symlink():
            raise CliError(f"reference target is missing or unsafe: {relative}")
    return document


def query_index(
    *,
    figure_type: str | None = None,
    features: list[str] | None = None,
    kind: str | None = None,
    limit: int = 5,
) -> dict[str, Any]:
    document = load_index()
    requested_features = {value.casefold() for value in (features or [])}
    matches = []
    for entry in document["entries"]:
        if figure_type and figure_type not in entry["figure_types"]:
            continue
        if kind and entry["kind"] != kind:
            continue
        available = {value.casefold() for value in entry["features"]}
        if requested_features and not requested_features.issubset(available):
            continue
        matches.append(entry)
    matches.sort(key=lambda entry: entry["id"])
    return {
        "schema_version": document["schema_version"],
        "query": {
            "figure_type": figure_type,
            "features": sorted(requested_features),
            "kind": kind,
            "limit": limit,
        },
        "matches": matches[:limit],
        "match_count": len(matches),
        "license_scope": document["license_scope"],
        "notice": (
            "Use matches as layout priors only. Preserve scientific content and "
            "do not copy labels, data, trademarks, or protected external compositions."
        ),
    }


def positive_int(value: str) -> int:
    try:
        parsed = int(value)
    except ValueError as exc:
        raise argparse.ArgumentTypeError("expected an integer") from exc
    if parsed <= 0 or parsed > 20:
        raise argparse.ArgumentTypeError("value must be between 1 and 20")
    return parsed


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Query bundled academic layout references.")
    parser.add_argument("--figure-type", choices=("architecture", "workflow", "roadmap"))
    parser.add_argument("--feature", action="append", default=[])
    parser.add_argument("--kind", choices=("example", "template"))
    parser.add_argument("--limit", type=positive_int, default=5)
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    try:
        args = parser.parse_args(argv)
        emit_json(
            query_index(
                figure_type=args.figure_type,
                features=args.feature,
                kind=args.kind,
                limit=args.limit,
            )
        )
        return 0
    except CliError as exc:
        parser.exit(2, f"error: {exc}\n")


if __name__ == "__main__":
    sys.exit(main())
