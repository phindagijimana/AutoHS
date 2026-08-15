#!/usr/bin/env python3
"""
Validate AutoHS workflow pipeline definitions.

Run from repository root:
    python -m workflow.validate
    python workflow/validate.py
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

# Allow running as script without installing the package
_REPO_ROOT = Path(__file__).resolve().parent.parent
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from workflow.load_pipeline import PipelineLoader, PipelineValidationError


def main() -> int:
    loader = PipelineLoader()

    try:
        pipeline = loader.load()
    except FileNotFoundError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1

    step_count = len(pipeline.steps)
    freesurfer_count = len(pipeline.freesurfer_substeps)
    execution_order = loader.get_execution_order()

    print("AutoHS workflow validation")
    print(f"  Pipeline: {pipeline.data.get('name')} v{pipeline.data.get('version')}")
    print(f"  Top-level steps: {step_count}")
    print(f"  FreeSurfer substeps: {freesurfer_count}")
    print(f"  Execution order: {' → '.join(execution_order[:4])} ... → {execution_order[-1]}")

    try:
        errors = loader.validate(raise_on_error=True)
    except PipelineValidationError as exc:
        print("\nValidation FAILED:", file=sys.stderr)
        for error in exc.errors:
            print(f"  - {error}", file=sys.stderr)
        return 1

    print(f"\nValidation PASSED ({len(errors)} checks, 0 errors)")

    summary = {
        "name": pipeline.data.get("name"),
        "version": pipeline.data.get("version"),
        "step_count": step_count,
        "freesurfer_substep_count": freesurfer_count,
        "execution_order": execution_order,
        "phases": [phase.get("id") for phase in pipeline.data.get("phases", [])],
    }
    print("\nSummary:")
    print(json.dumps(summary, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
