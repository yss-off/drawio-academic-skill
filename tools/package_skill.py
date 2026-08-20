#!/usr/bin/env python3
"""Build a deterministic install-ready ZIP from the runtime skill source."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import tempfile
import tomllib
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FIXED_TIMESTAMP = (2026, 1, 1, 0, 0, 0)


def project_metadata() -> tuple[str, str, Path]:
    with (ROOT / "pyproject.toml").open("rb") as handle:
        document = tomllib.load(handle)
    project = document["project"]
    settings = document["tool"]["drawio_academic_skill"]
    skill_root = (ROOT / settings["skill_path"]).resolve()
    return project["version"], settings["skill_name"], skill_root


def package_files(skill_root: Path) -> list[Path]:
    files = []
    for path in skill_root.rglob("*"):
        if path.is_symlink():
            raise ValueError(f"refusing to package symlink: {path}")
        if not path.is_file():
            continue
        if path.name == ".gitignore" or "__pycache__" in path.parts or path.suffix == ".pyc":
            continue
        files.append(path)
    return sorted(files, key=lambda path: path.relative_to(skill_root).as_posix())


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Package the runtime skill deterministically.")
    parser.add_argument("--output-dir", type=Path, default=ROOT / "dist")
    parser.add_argument("--force", action="store_true")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    version, skill_name, skill_root = project_metadata()
    output_dir = args.output_dir.expanduser().resolve()
    output_dir.mkdir(parents=True, exist_ok=True)
    destination = output_dir / f"{skill_name}-{version}.zip"
    if destination.exists() and not args.force:
        raise SystemExit(f"refusing to overwrite existing package: {destination}")

    descriptor, temporary_name = tempfile.mkstemp(
        prefix=f".{destination.name}.", suffix=".tmp", dir=output_dir
    )
    os.close(descriptor)
    temporary = Path(temporary_name)
    files = package_files(skill_root)
    try:
        with zipfile.ZipFile(
            temporary, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9
        ) as archive:
            for source in files:
                relative = source.relative_to(skill_root)
                info = zipfile.ZipInfo(f"{skill_name}/{relative.as_posix()}", FIXED_TIMESTAMP)
                info.compress_type = zipfile.ZIP_DEFLATED
                info.external_attr = (source.stat().st_mode & 0o777) << 16
                archive.writestr(info, source.read_bytes())
        os.replace(temporary, destination)
    finally:
        try:
            temporary.unlink()
        except FileNotFoundError:
            pass

    print(
        json.dumps(
            {
                "status": "written",
                "path": str(destination),
                "version": version,
                "files": len(files),
                "sha256": sha256(destination),
            },
            indent=2,
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
