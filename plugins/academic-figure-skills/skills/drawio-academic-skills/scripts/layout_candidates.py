#!/usr/bin/env python3
"""Generate deterministic layout-plan candidates without rendering or rewriting content."""

from __future__ import annotations

import argparse
import sys
from typing import Any

from _common import CliError, emit_json

SCHEMA_VERSION = "1.0"
NODE_BUDGETS = {
    "architecture": {"target": "30-35", "maximum": 60},
    "workflow": {"target": "25-30", "maximum": 50},
    "roadmap": {"target": "15-20", "maximum": 40},
}

LAYOUT_LIBRARY: dict[str, list[dict[str, Any]]] = {
    "architecture": [
        {
            "id": "architecture-layered",
            "layout_family": "layered-left-to-right",
            "main_axis": "left-to-right data or responsibility flow",
            "placement": "Place each major section in one layer; reserve top/bottom corridors for control or feedback.",
            "strengths": ["clear stage order", "stable module boundaries", "good double-column fit"],
            "risks": ["can falsely imply chronology when relations are static"],
            "use_when": "The argument has an input-to-output path through distinct modules.",
        },
        {
            "id": "architecture-modular-grid",
            "layout_family": "modular-grid",
            "main_axis": "hierarchy by rows and peer comparison by columns",
            "placement": "Group peer subsystems into aligned modules; keep shared services in a separate band.",
            "strengths": ["supports subsystem comparison", "balanced whitespace", "compact legends"],
            "risks": ["cross-module edges can become dense"],
            "use_when": "The argument emphasizes subsystem roles more than one execution sequence.",
        },
        {
            "id": "architecture-hero-support",
            "layout_family": "hero-plus-support",
            "main_axis": "central mechanism with supporting evidence around it",
            "placement": "Give the core mechanism the largest region and place inputs, constraints, and outputs in smaller aligned bands.",
            "strengths": ["strong visual hierarchy", "fits one dominant contribution"],
            "risks": ["central placement may overstate causal importance"],
            "use_when": "One mechanism is the paper's primary contribution and other sections support it.",
        },
    ],
    "workflow": [
        {
            "id": "workflow-linear",
            "layout_family": "linear-left-to-right",
            "main_axis": "ordered execution",
            "placement": "Place confirmed steps on one row; put annotations and outputs in separate bands.",
            "strengths": ["fast reading", "few bends", "compact single-loop figures"],
            "risks": ["branches or repeated loops can overload the row"],
            "use_when": "The method is predominantly sequential with few decisions.",
        },
        {
            "id": "workflow-swimlane",
            "layout_family": "swimlane",
            "main_axis": "execution across actors or phases",
            "placement": "Assign one lane per confirmed actor, data state, or phase; keep handoffs orthogonal.",
            "strengths": ["clear responsibility", "separates parallel work", "supports handoff evidence"],
            "risks": ["too many lanes shrink labels and increase crossings"],
            "use_when": "The scientific meaning depends on who or what performs each step.",
        },
        {
            "id": "workflow-branch-converge",
            "layout_family": "branch-and-converge",
            "main_axis": "shared setup, parallel variants, shared evaluation",
            "placement": "Keep setup and evaluation on the centerline; align branches symmetrically between them.",
            "strengths": ["good for ablations", "makes shared evaluation explicit"],
            "risks": ["symmetry can imply equal evidential weight when variants differ"],
            "use_when": "Confirmed alternatives or experimental variants converge on comparable evaluation.",
        },
    ],
    "roadmap": [
        {
            "id": "roadmap-horizontal",
            "layout_family": "horizontal-milestones",
            "main_axis": "left-to-right progression",
            "placement": "Place stages on one timeline and align stage outputs in a supporting band.",
            "strengths": ["familiar reading order", "clear milestone outputs"],
            "risks": ["wide plans may fail single-column print scale"],
            "use_when": "Progression is the only primary axis.",
        },
        {
            "id": "roadmap-vertical",
            "layout_family": "vertical-stages",
            "main_axis": "top-to-bottom progression",
            "placement": "Stack stages vertically and place evidence or deliverables beside each stage.",
            "strengths": ["fits narrow columns", "supports longer stage labels"],
            "risks": ["can resemble an execution workflow instead of a roadmap"],
            "use_when": "The target is narrow or the stage descriptions need horizontal space.",
        },
        {
            "id": "roadmap-dual-axis",
            "layout_family": "progression-with-context-axis",
            "main_axis": "primary progression plus non-causal contextual bands",
            "placement": "Keep milestones on the primary axis; show maturity, capability, or evidence as labeled bands without causal arrows.",
            "strengths": ["separates progression from context", "supports capability ladders"],
            "risks": ["adjacency may be misread as causality"],
            "use_when": "The source explicitly contains a second contextual progression dimension.",
        },
    ],
}


def build_candidates(
    figure_type: str,
    sections: list[str],
    *,
    has_feedback: bool = False,
    secondary_axis: bool = False,
    count: int = 3,
) -> dict[str, Any]:
    if figure_type not in LAYOUT_LIBRARY:
        raise CliError(f"unsupported figure type: {figure_type}")
    normalized_sections = [section.strip() for section in sections]
    if len(normalized_sections) < 2 or len(normalized_sections) > 12:
        raise CliError("provide between 2 and 12 major sections")
    if any(not section for section in normalized_sections):
        raise CliError("major-section values must not be empty")
    if len(set(normalized_sections)) != len(normalized_sections):
        raise CliError("major-section values must be unique")
    if count < 2 or count > 3:
        raise CliError("candidate count must be 2 or 3")

    candidates = []
    for template in LAYOUT_LIBRARY[figure_type]:
        if template["id"] == "roadmap-dual-axis" and not secondary_axis:
            continue
        candidate = dict(template)
        candidate["section_order"] = normalized_sections
        candidate["node_budget"] = NODE_BUDGETS[figure_type]
        candidate["edge_strategy"] = (
            "Reserve one outer corridor for confirmed feedback; keep the primary path separate."
            if has_feedback
            else "Do not add feedback or cross-axis arrows unless the semantic inventory confirms them."
        )
        candidate["scientific_content_status"] = "unchanged"
        candidates.append(candidate)

    if secondary_axis and figure_type != "roadmap":
        candidates[-1] = {
            **candidates[-1],
            "id": f"{figure_type}-orthogonal-context",
            "layout_family": "primary-axis-with-context-bands",
            "main_axis": "primary scientific path plus non-causal contextual bands",
            "placement": (
                "Keep the confirmed primary path intact; show the secondary dimension as "
                "bands, brackets, or a ladder without cross-axis arrows unless confirmed."
            ),
            "strengths": ["separates process and progression semantics", "supports two-axis arguments"],
            "risks": ["proximity may still be misread as an unsupported mapping"],
            "use_when": "The source explicitly distinguishes a primary path from a contextual axis.",
        }

    selected = candidates[:count]
    if len(selected) < 2:
        raise CliError("the requested constraints produced fewer than two candidates")
    return {
        "schema_version": SCHEMA_VERSION,
        "figure_type": figure_type,
        "input_contract": {
            "major_sections": normalized_sections,
            "has_feedback": has_feedback,
            "secondary_axis": secondary_axis,
        },
        "candidates": selected,
        "selection_status": "pending",
        "selected_id": None,
        "selection_reason": None,
        "notice": (
            "These are planning alternatives, not rendered figures or scientific decisions. "
            "Confirm semantic relations before selecting and authoring YAML."
        ),
    }


def candidate_count(value: str) -> int:
    try:
        parsed = int(value)
    except ValueError as exc:
        raise argparse.ArgumentTypeError("expected 2 or 3") from exc
    if parsed not in {2, 3}:
        raise argparse.ArgumentTypeError("expected 2 or 3")
    return parsed


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Generate 2-3 distinct academic layout plans without rendering."
    )
    parser.add_argument("--figure-type", required=True, choices=tuple(LAYOUT_LIBRARY))
    parser.add_argument("--major-section", action="append", required=True)
    parser.add_argument("--has-feedback", action="store_true")
    parser.add_argument("--secondary-axis", action="store_true")
    parser.add_argument("--count", type=candidate_count, default=3)
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    try:
        args = parser.parse_args(argv)
        emit_json(
            build_candidates(
                args.figure_type,
                args.major_section,
                has_feedback=args.has_feedback,
                secondary_axis=args.secondary_axis,
                count=args.count,
            )
        )
        return 0
    except CliError as exc:
        parser.exit(2, f"error: {exc}\n")


if __name__ == "__main__":
    sys.exit(main())
