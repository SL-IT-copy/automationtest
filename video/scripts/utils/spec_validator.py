# pyright: reportMissingModuleSource=false
from __future__ import annotations

from functools import lru_cache
from pathlib import Path

from jsonschema import Draft7Validator, FormatChecker


SCHEMA_PATH = Path(__file__).resolve().parents[2] / "schemas" / "video_spec.schema.json"


@lru_cache(maxsize=1)
def _validator() -> Draft7Validator:
    schema = SCHEMA_PATH.read_text(encoding="utf-8")
    import json

    return Draft7Validator(json.loads(schema), format_checker=FormatChecker())


def validate_spec(spec: dict) -> bool:
    validator = _validator()
    errors = sorted(
        validator.iter_errors(spec), key=lambda error: list(error.absolute_path)
    )
    if errors:
        details = []
        for error in errors:
            path = ".".join(str(part) for part in error.absolute_path) or "<root>"
            details.append(f"{path}: {error.message}")
        raise ValueError("Invalid video spec:\n" + "\n".join(details))
    return True
