#!/usr/bin/env python3
"""Offline project verifier for the independently maintained overlay source."""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import tempfile
import tomllib
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
PYPROJECT = ROOT / "pyproject.toml"


class VerificationError(RuntimeError):
    """Raised when a project invariant or subprocess check fails."""


def run_checked(command: list[str], *, env: dict[str, str] | None = None) -> str:
    result = subprocess.run(
        command,
        cwd=ROOT,
        env=env,
        text=True,
        capture_output=True,
        check=False,
    )
    output = "\n".join(part for part in (result.stdout, result.stderr) if part).strip()
    if result.returncode != 0:
        raise VerificationError(
            f"command failed ({result.returncode}): {' '.join(command)}\n{output}"
        )
    return output


def load_project() -> tuple[dict[str, Any], Path]:
    with PYPROJECT.open("rb") as handle:
        document = tomllib.load(handle)
    project = document.get("project")
    settings = document.get("tool", {}).get("drawio_academic_skill")
    if not isinstance(project, dict) or not isinstance(settings, dict):
        raise VerificationError("pyproject.toml is missing project/tool metadata")
    version = project.get("version")
    if not isinstance(version, str) or not version:
        raise VerificationError("project.version must be a non-empty string")
    skill_path = settings.get("skill_path")
    if not isinstance(skill_path, str):
        raise VerificationError("tool.drawio_academic_skill.skill_path is required")
    skill_root = (ROOT / skill_path).resolve()
    try:
        skill_root.relative_to(ROOT)
    except ValueError as exc:
        raise VerificationError("skill_path must stay inside the project") from exc
    return project, skill_root


def validate_structure(project: dict[str, Any], skill_root: Path) -> dict[str, int]:
    required = (
        ROOT / "README.md",
        ROOT / "CHANGELOG.md",
        ROOT / "LICENSE",
        ROOT / "AGENTS.md",
        ROOT / "Makefile",
        skill_root / "SKILL.md",
        skill_root / "agents" / "openai.yaml",
        skill_root / "assets" / "schemas" / "figure-manifest.schema.json",
        skill_root / "evals" / "evals.json",
        skill_root / "evals" / "smoke_test.py",
        skill_root / "scripts" / "figure_manifest.py",
    )
    missing = [str(path.relative_to(ROOT)) for path in required if not path.is_file()]
    if missing:
        raise VerificationError(f"required project files are missing: {missing}")

    forbidden_runtime_docs = (
        "README.md",
        "README_CN.md",
        "CHANGELOG.md",
        "evals/baseline-prompts.json",
        "evals/test-prompts.json",
        "evals/darwin-results.tsv",
    )
    present = [name for name in forbidden_runtime_docs if (skill_root / name).exists()]
    if present:
        raise VerificationError(
            f"project-only documents must not live in the runtime skill: {present}"
        )

    symlinks = [str(path.relative_to(ROOT)) for path in skill_root.rglob("*") if path.is_symlink()]
    if symlinks:
        raise VerificationError(f"runtime skill must not contain symlinks: {symlinks}")

    skill_lines = len((skill_root / "SKILL.md").read_text(encoding="utf-8").splitlines())
    if skill_lines > 500:
        raise VerificationError(f"SKILL.md exceeds the 500-line limit: {skill_lines}")

    evals = json.loads((skill_root / "evals" / "evals.json").read_text(encoding="utf-8"))
    if evals.get("version") != project["version"]:
        raise VerificationError(
            "evals/evals.json version must match pyproject.toml project.version"
        )

    json_files = sorted(skill_root.rglob("*.json"))
    for path in json_files:
        try:
            json.loads(path.read_text(encoding="utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise VerificationError(f"invalid JSON: {path.relative_to(ROOT)}: {exc}") from exc

    return {
        "runtime_files": sum(path.is_file() for path in skill_root.rglob("*")),
        "json_files": len(json_files),
        "skill_lines": skill_lines,
    }


def find_quick_validator(explicit: Path | None) -> Path | None:
    candidates = [
        explicit,
        Path.home() / ".codex" / "skills" / ".system" / "skill-creator" / "scripts" / "quick_validate.py",
    ]
    return next((path for path in candidates if path and path.is_file()), None)


def find_base(explicit: Path | None) -> Path:
    candidates = [
        explicit,
        ROOT / "skill" / "drawio",
        Path.home() / ".codex" / "skills" / "drawio",
        Path.home() / ".agents" / "skills" / "drawio",
    ]
    for candidate in candidates:
        if candidate and (candidate / "scripts" / "cli.js").is_file():
            return candidate.resolve()
    raise VerificationError("sibling base not found; pass --base /path/to/drawio")


def validate_base(skill_root: Path, base_root: Path) -> dict[str, Any]:
    sources = sorted((skill_root / "references" / "examples").glob("*.yaml"))
    sources += sorted((skill_root / "references" / "templates").glob("*.yaml"))
    notices: set[str] = set()
    with tempfile.TemporaryDirectory(prefix="drawio-academic-base-") as temporary:
        output_root = Path(temporary)
        for source in sources:
            output = output_root / f"{source.stem}.drawio"
            text = run_checked(
                [
                    "node",
                    str(base_root / "scripts" / "cli.js"),
                    str(source),
                    str(output),
                    "--validate",
                    "--strict-warnings",
                ]
            )
            for line in text.splitlines():
                if "recommends SVG export for paper-ready vector output" in line:
                    notices.add(line.strip())
    return {
        "base_root": str(base_root),
        "strict_examples": len(sources),
        "base_notices": sorted(notices),
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Verify the draw.io academic skill project.")
    parser.add_argument("--with-base", action="store_true")
    parser.add_argument("--base", type=Path)
    parser.add_argument("--quick-validator", type=Path)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        project, skill_root = load_project()
        summary: dict[str, Any] = {
            "status": "pass",
            "project": project["name"],
            "version": project["version"],
            "structure": validate_structure(project, skill_root),
        }
        with tempfile.TemporaryDirectory(prefix="drawio-academic-pycache-") as cache:
            environment = dict(os.environ)
            environment["PYTHONPYCACHEPREFIX"] = cache
            run_checked(
                [sys.executable, str(skill_root / "evals" / "smoke_test.py")],
                env=environment,
            )
        summary["smoke_tests"] = "pass"

        validator = find_quick_validator(args.quick_validator)
        if validator:
            run_checked([sys.executable, str(validator), str(skill_root)])
            summary["skill_validation"] = "pass"
        else:
            summary["skill_validation"] = "not_available"

        if args.with_base:
            summary["base_validation"] = validate_base(skill_root, find_base(args.base))
        else:
            summary["base_validation"] = "not_requested"

        print(json.dumps(summary, indent=2, ensure_ascii=False, sort_keys=True))
        return 0
    except (OSError, KeyError, ValueError, VerificationError) as exc:
        print(json.dumps({"status": "fail", "error": str(exc)}, ensure_ascii=False))
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
