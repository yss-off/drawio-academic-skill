#!/usr/bin/env python3
"""Inspect local font resolution and glyph coverage without changing fonts."""

from __future__ import annotations

import argparse
import sys
from collections import defaultdict
from pathlib import Path
from typing import Any

from _common import CliError, emit_json, positive_int

SCHEMA_VERSION = "1.0"
DEFAULT_TEXT = "ASCII 0123456789 − ± × μ Δ 中文"
DEFAULT_FAMILIES = [
    "Arial",
    "Helvetica",
    "Liberation Sans",
    "DejaVu Sans",
    "Noto Sans CJK SC",
    "Source Han Sans SC",
]


def _display(character: str) -> str:
    if character == " ":
        return "SPACE"
    return character


def preflight_fonts(
    text: str,
    *,
    families: list[str] | None = None,
    max_chars: int = 256,
) -> dict[str, Any]:
    """Return actual local font files used to cover the requested characters."""
    if len(text) > max_chars:
        raise CliError(f"text contains {len(text)} characters; limit is {max_chars}")
    try:
        from matplotlib import ft2font, font_manager
    except ImportError as exc:
        raise CliError(
            "Matplotlib is required for font preflight; run with --with 'matplotlib==3.11.1'"
        ) from exc

    requested_families = families or list(DEFAULT_FAMILIES)
    entries = sorted(
        font_manager.fontManager.ttflist,
        key=lambda entry: (entry.name.casefold(), str(Path(entry.fname).resolve())),
    )
    preferred: list[Any] = []
    others: list[Any] = []
    seen_paths: set[str] = set()
    requested_casefold = [family.casefold() for family in requested_families]

    for family in requested_casefold:
        for entry in entries:
            path = str(Path(entry.fname).resolve())
            if entry.name.casefold() == family and path not in seen_paths:
                preferred.append(entry)
                seen_paths.add(path)
    for entry in entries:
        path = str(Path(entry.fname).resolve())
        if path not in seen_paths:
            others.append(entry)
            seen_paths.add(path)

    charmap_cache: dict[str, set[int]] = {}

    def charmap(entry: Any) -> set[int]:
        path = str(Path(entry.fname).resolve())
        if path not in charmap_cache:
            try:
                charmap_cache[path] = set(ft2font.FT2Font(path).get_charmap())
            except (OSError, RuntimeError):
                charmap_cache[path] = set()
        return charmap_cache[path]

    assignments: dict[str, list[str]] = defaultdict(list)
    font_records: dict[str, dict[str, Any]] = {}
    missing: list[dict[str, Any]] = []
    unique_characters = list(dict.fromkeys(text))

    for character in unique_characters:
        if character.isspace():
            continue
        codepoint = ord(character)
        selected = next(
            (entry for entry in [*preferred, *others] if codepoint in charmap(entry)),
            None,
        )
        if selected is None:
            missing.append(
                {
                    "character": _display(character),
                    "codepoint": f"U+{codepoint:04X}",
                }
            )
            continue
        path = str(Path(selected.fname).resolve())
        assignments[path].append(character)
        font_records[path] = {
            "family": selected.name,
            "path": path,
            "requested_family": selected.name.casefold() in requested_casefold,
        }

    stack = []
    for path, characters in assignments.items():
        record = dict(font_records[path])
        record["characters"] = "".join(characters)
        record["codepoints"] = [f"U+{ord(character):04X}" for character in characters]
        stack.append(record)

    return {
        "schema_version": SCHEMA_VERSION,
        "requested_families": requested_families,
        "requested_text": text,
        "font_stack": stack,
        "missing_glyphs": missing,
        "status": "pass" if not missing else "review",
        "notice": (
            "This checks local font-file coverage only. It does not prove that a backend embeds "
            "the font or that the final rendered figure is legible."
        ),
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Report local font fallback and glyph coverage for figure text."
    )
    parser.add_argument("--text", default=DEFAULT_TEXT)
    parser.add_argument("--family", action="append", default=[], help="preferred family; repeat in priority order")
    parser.add_argument("--max-chars", type=positive_int, default=256)
    parser.add_argument("--output")
    parser.add_argument("--force", action="store_true")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    try:
        args = parser.parse_args(argv)
        report = preflight_fonts(
            args.text,
            families=args.family or None,
            max_chars=args.max_chars,
        )
        emit_json(report, output=args.output, force=args.force)
        return 0
    except CliError as exc:
        parser.exit(2, f"error: {exc}\n")


if __name__ == "__main__":
    sys.exit(main())
