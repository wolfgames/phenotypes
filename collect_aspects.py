#!/usr/bin/env python3
"""collect_aspects.py
Usage:
    python collect_aspects.py <path-to-file>

This utility scans the given file for JSON objects that describe an
`updateAspect` operation (as seen in the project examples). For every
`aspect` found it prints a corresponding `$createAspect` declaration in
one of three forms:

    ($createAspect: "some_flag", "boolean", "false")
    ($createAspect: "some_counter", "number", "0")
    ($createAspect: "some_text", "string", "")

Determination of the aspect type is based on the value associated with
`"value"` or, when the operation is "increment", it defaults to
`number`. Any non-numeric, non-boolean literal is treated as a
string.

It also gathers every `checkAspect` block and lists the referenced
aspects in the form:

    (checkAspect: "some_aspect", "eq", "true")
"""
from __future__ import annotations

import re
import sys
from pathlib import Path
from typing import Dict, Tuple

# ---------------------------------------------------------------------------
# Regex patterns (compiled once)
# ---------------------------------------------------------------------------
# Roughly match an `updateAspect` JSON object — not necessarily valid JSON by
# itself, but captures the portion between the opening and closing braces. We
# use a *reluctant* match to avoid spanning unrelated content.
UPDATE_ASPECT_OBJ_RE = re.compile(
    r'\{[^{}]*?"type"\s*:\s*"updateAspect"[^{}]*?\}',
    re.DOTALL,
)

# Extract field patterns inside a matched object
FIELD_RE = re.compile(r'"(?P<key>[^"]+)"\s*:\s*(?P<value>[^,}]+)')

# Pattern to locate the start of a `checkAspect` block
CHECK_ASPECT_TYPE_RE = re.compile(r'"type"\s*:\s*"checkAspect"', re.IGNORECASE)

# Simple patterns to extract fields inside a `check` sub-object
ASPECT_FIELD_RE = re.compile(r'"aspect"\s*:\s*"([^"\n]+)"')
CMP_FIELD_RE = re.compile(r'"type"\s*:\s*"([^"\n]+)"')  # comparison operator inside `check`
TARGET_FIELD_RE = re.compile(r'"target"\s*:\s*"([^"\n]+)"')

# Match a condition object containing both aspect and its target value, used for compound AND/OR checks
ASPECT_CONDITION_RE = re.compile(
    r'"aspect"\s*:\s*"([^"\n]+)"[^{}]*?"target"\s*:\s*"([^"\n]+)"',
    re.DOTALL,
)


# ---------------------------------------------------------------------------
# Helper functions
# ---------------------------------------------------------------------------

def parse_update_object(raw_obj: str) -> Dict[str, str]:
    """Extract key/value pairs out of a raw JSON-like `updateAspect` object.

    The input *raw_obj* is a substring beginning with "{" and ending with
    "}" that contains a `type` field set to "updateAspect". We parse its
    simple (flat) structure using a regex rather than `json.loads` because the
    file may include trailing commas or non-standard JSON.
    """
    data: Dict[str, str] = {}
    for match in FIELD_RE.finditer(raw_obj):
        key = match.group("key")
        value_raw = match.group("value").strip()
        # Remove surrounding quotes if any
        if value_raw.startswith("\"") and value_raw.endswith("\""):
            value_raw = value_raw[1:-1]
        data[key] = value_raw
    return data


def classify_aspect(value: str, operation: str | None) -> Tuple[str, str]:
    """Return (type, default_value) where type is "boolean" or "number"."""
    v_lower = value.lower()

    # If the operation is increment we treat it as numeric irrespective of
    # what `value` contains (commonly "1").
    if operation and operation.lower() == "increment":
        return "number", "0"

    # Boolean detection
    if v_lower in {"true", "false"}:
        return "boolean", "false"

    # Numeric detection (int or float)
    try:
        float(value)
    except ValueError:
        # Not numeric -> treat as string
        return "string", ""
    else:
        return "number", "0"


def _merge_aspect(aspect_name: str, aspect_type: str, default_val: str, aspects: Dict[str, Tuple[str, str]]):
    """Merge a detected aspect into the *aspects* dict, resolving type conflicts."""
    prior = aspects.get(aspect_name)
    if prior:
        prev_type, _ = prior
        if prev_type == aspect_type:
            return
        # Conflict resolution: string > number > boolean
        priority = {"boolean": 0, "number": 1, "string": 2}
        chosen_type = aspect_type if priority[aspect_type] >= priority[prev_type] else prev_type
        if chosen_type == prev_type:
            return  # keep existing default
        aspects[aspect_name] = (chosen_type, "" if chosen_type == "string" else ("0" if chosen_type == "number" else "false"))
    else:
        aspects[aspect_name] = (aspect_type, default_val)


def collect_all_aspects(text: str) -> Dict[str, Tuple[str, str]]:
    """Return dictionary of {aspect: (type, default)} from updateAspect and checkAspect blocks."""
    aspects: Dict[str, Tuple[str, str]] = {}

    # --- Scan updateAspect blocks ---
    for obj_match in UPDATE_ASPECT_OBJ_RE.finditer(text):
        raw_obj = obj_match.group(0)
        data = parse_update_object(raw_obj)

        if data.get("type", "") != "updateAspect":
            continue

        name = data.get("aspect")
        if not name:
            continue

        operation = data.get("operation")
        value = data.get("value", "")

        atype, default = classify_aspect(value, operation)
        _merge_aspect(name, atype, default, aspects)

    # --- Scan checkAspect blocks ---
    window = 2500  # larger to cover nested structures
    for m in CHECK_ASPECT_TYPE_RE.finditer(text):
        snippet = text[m.end(): m.end() + window]

        # First, handle explicit condition objects with both aspect and target
        found_any = False
        for cond in ASPECT_CONDITION_RE.finditer(snippet):
            found_any = True
            name, target_val = cond.group(1), cond.group(2)
            atype, default = classify_aspect(target_val, None)
            _merge_aspect(name, atype, default, aspects)

        if found_any:
            continue  # already processed compound conditions

        # Fallback to simple pattern (non-compound)
        aspect_match = ASPECT_FIELD_RE.search(snippet)
        if not aspect_match:
            continue
        name = aspect_match.group(1)
        tgt_match = TARGET_FIELD_RE.search(snippet)
        target_val = tgt_match.group(1) if tgt_match else ""
        atype, default = classify_aspect(target_val, None)
        _merge_aspect(name, atype, default, aspects)

    return aspects


# ---------------------------------------------------------------------------
# CLI entrypoint
# ---------------------------------------------------------------------------

def main() -> None:
    if len(sys.argv) != 2:
        print("Usage: python collect_aspects.py <path-to-file>")
        sys.exit(1)

    file_path = Path(sys.argv[1])
    if not file_path.is_file():
        print(f"Error: {file_path} is not a valid file.")
        sys.exit(1)

    text = file_path.read_text(encoding="utf-8", errors="replace")

    aspects = collect_all_aspects(text)
    for line in sorted(
        (
            f'($createAspect: "{name}", "{atype}", "{default}")'
            for name, (atype, default) in aspects.items()
        ),
        key=str.lower,
    ):
        print(line)


if __name__ == "__main__":
    main() 