#!/usr/bin/env python3
"""Small, network-free safety helpers for overlay-local CLIs."""

from __future__ import annotations

import hashlib
import json
import os
import stat
import tempfile
from pathlib import Path
from typing import Any

MAX_INPUT_BYTES = 16 * 1024 * 1024
MAX_OUTPUT_BYTES = 8 * 1024 * 1024


class CliError(ValueError):
    """Expected user-facing validation error."""


def checked_input_file(value: str | os.PathLike[str]) -> Path:
    path = Path(value).expanduser()
    if path.is_symlink():
        raise CliError(f"input must not be a symlink: {path}")
    try:
        info = path.stat()
    except OSError as exc:
        raise CliError(f"cannot access input {path}: {exc}") from exc
    if not stat.S_ISREG(info.st_mode):
        raise CliError(f"input is not a regular file: {path}")
    if info.st_size > MAX_INPUT_BYTES:
        raise CliError(f"input exceeds {MAX_INPUT_BYTES} bytes: {path}")
    return path.resolve()


def checked_output_file(
    value: str | os.PathLike[str], *, force: bool = False, mkdir: bool = False
) -> Path:
    path = Path(value).expanduser()
    if not path.name:
        raise CliError("output must name a file")
    if path.is_symlink():
        raise CliError(f"output must not be a symlink: {path}")
    parent = path.parent
    if mkdir:
        parent.mkdir(parents=True, exist_ok=True)
    if not parent.exists() or not parent.is_dir() or parent.is_symlink():
        raise CliError(f"output parent is not a safe directory: {parent}")
    if path.exists() and not force:
        raise CliError(f"refusing to overwrite existing output: {path}")
    if path.exists() and not path.is_file():
        raise CliError(f"output exists and is not a regular file: {path}")
    return parent.resolve() / path.name


def load_json(value: str | os.PathLike[str]) -> dict[str, Any]:
    path = checked_input_file(value)
    try:
        document = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise CliError(f"cannot read JSON {path}: {exc}") from exc
    if not isinstance(document, dict):
        raise CliError(f"JSON root must be an object: {path}")
    return document


def atomic_write_json(
    path: str | os.PathLike[str], document: dict[str, Any], *, force: bool = False
) -> Path:
    destination = checked_output_file(path, force=force)
    payload = (
        json.dumps(document, indent=2, sort_keys=True, ensure_ascii=False) + "\n"
    ).encode("utf-8")
    if len(payload) > MAX_OUTPUT_BYTES:
        raise CliError(f"output exceeds {MAX_OUTPUT_BYTES} bytes")
    descriptor, temporary_name = tempfile.mkstemp(
        prefix=f".{destination.name}.", suffix=".tmp", dir=destination.parent
    )
    temporary = Path(temporary_name)
    try:
        with os.fdopen(descriptor, "wb") as handle:
            handle.write(payload)
            handle.flush()
            os.fsync(handle.fileno())
        os.chmod(temporary, 0o600)
        if destination.exists() and not force:
            raise CliError(f"refusing to overwrite existing output: {destination}")
        os.replace(temporary, destination)
    finally:
        try:
            temporary.unlink()
        except FileNotFoundError:
            pass
    return destination


def emit_json(document: dict[str, Any]) -> None:
    print(json.dumps(document, indent=2, sort_keys=True, ensure_ascii=False))


def sha256_file(path: str | os.PathLike[str]) -> str:
    source = checked_input_file(path)
    digest = hashlib.sha256()
    with source.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()
