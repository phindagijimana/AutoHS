"""
Load and validate the NeuroInsight workflow pipeline definitions.

Usage:
    from workflow.load_pipeline import PipelineLoader

    loader = PipelineLoader()
    pipeline = loader.load()
    errors = loader.validate()
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import yaml


class PipelineValidationError(Exception):
    """Raised when pipeline validation fails."""

    def __init__(self, errors: list[str]):
        self.errors = errors
        super().__init__(f"Pipeline validation failed with {len(errors)} error(s)")


@dataclass
class StepDefinition:
    """A single workflow step loaded from YAML."""

    id: str
    path: Path
    data: dict[str, Any] = field(repr=False)
    substeps: list["StepDefinition"] = field(default_factory=list)

    @property
    def phase(self) -> str | None:
        return self.data.get("phase")

    @property
    def order(self) -> int | None:
        return self.data.get("order")

    @property
    def depends_on(self) -> list[str]:
        value = self.data.get("depends_on", [])
        return value if isinstance(value, list) else []

    @property
    def code_reference(self) -> dict[str, Any] | None:
        ref = self.data.get("code_reference")
        return ref if isinstance(ref, dict) else None


@dataclass
class PipelineDefinition:
    """Master pipeline with all steps and nested sub-pipelines."""

    root: Path
    data: dict[str, Any]
    steps: dict[str, StepDefinition]
    freesurfer_subpipeline: dict[str, Any] | None = None
    freesurfer_substeps: dict[str, StepDefinition] = field(default_factory=dict)


class PipelineLoader:
    """Load workflow YAML files and validate structure and code references."""

    STEP_GLOB = "[0-9][0-9]-*.yaml"

    def __init__(self, workflow_dir: Path | None = None, validate_code_refs: bool | None = None):
        self.workflow_dir = workflow_dir or Path(__file__).resolve().parent
        self.repo_root = self.workflow_dir.parent
        self._pipeline: PipelineDefinition | None = None
        # Auto-detect standalone repo: code refs point to external NeuroInsight app
        if validate_code_refs is None:
            self.validate_code_refs = (self.repo_root / "backend").exists()
        else:
            self.validate_code_refs = validate_code_refs

    def load(self) -> PipelineDefinition:
        """Load master pipeline, top-level steps, and FreeSurfer sub-pipeline."""
        pipeline_path = self.workflow_dir / "pipeline.yaml"
        if not pipeline_path.exists():
            raise FileNotFoundError(f"Missing pipeline definition: {pipeline_path}")

        with pipeline_path.open(encoding="utf-8") as handle:
            pipeline_data = yaml.safe_load(handle) or {}

        steps_dir = self.workflow_dir / "steps"
        steps = self._load_steps_from_dir(steps_dir)

        freesurfer_dir = steps_dir / "freesurfer"
        freesurfer_subpipeline = None
        freesurfer_substeps: dict[str, StepDefinition] = {}

        freesurfer_pipeline_path = freesurfer_dir / "pipeline.yaml"
        if freesurfer_pipeline_path.exists():
            with freesurfer_pipeline_path.open(encoding="utf-8") as handle:
                freesurfer_subpipeline = yaml.safe_load(handle) or {}
            substeps_dir = freesurfer_dir / "substeps"
            if substeps_dir.exists():
                freesurfer_substeps = self._load_steps_from_dir(substeps_dir, pattern="*.yaml")

        self._pipeline = PipelineDefinition(
            root=self.workflow_dir,
            data=pipeline_data,
            steps=steps,
            freesurfer_subpipeline=freesurfer_subpipeline,
            freesurfer_substeps=freesurfer_substeps,
        )
        return self._pipeline

    def _load_steps_from_dir(
        self, directory: Path, pattern: str | None = None
    ) -> dict[str, StepDefinition]:
        steps: dict[str, StepDefinition] = {}
        if not directory.exists():
            return steps

        glob_pattern = pattern or self.STEP_GLOB
        for path in sorted(directory.glob(glob_pattern)):
            if path.name == "pipeline.yaml":
                continue
            with path.open(encoding="utf-8") as handle:
                data = yaml.safe_load(handle) or {}

            step_id = data.get("id")
            if not step_id:
                raise ValueError(f"Step file missing 'id': {path}")

            steps[step_id] = StepDefinition(id=step_id, path=path, data=data)

        return steps

    def validate(self, raise_on_error: bool = True) -> list[str]:
        """Run all validation checks. Returns list of error messages."""
        if self._pipeline is None:
            self.load()

        assert self._pipeline is not None
        errors: list[str] = []
        errors.extend(self._validate_pipeline_metadata())
        errors.extend(self._validate_step_ids())
        errors.extend(self._validate_execution_order())
        errors.extend(self._validate_step_dependencies())
        errors.extend(self._validate_code_references())
        errors.extend(self._validate_freesurfer_subpipeline())

        if errors and raise_on_error:
            raise PipelineValidationError(errors)

        return errors

    def get_execution_order(self) -> list[str]:
        """Return ordered step IDs from pipeline.yaml execution_order."""
        if self._pipeline is None:
            self.load()

        assert self._pipeline is not None
        execution_order = self._pipeline.data.get("execution_order", [])
        return [entry["step"] for entry in execution_order if isinstance(entry, dict) and "step" in entry]

    def get_step(self, step_id: str) -> StepDefinition | None:
        if self._pipeline is None:
            self.load()

        assert self._pipeline is not None
        return self._pipeline.steps.get(step_id)

    def _validate_pipeline_metadata(self) -> list[str]:
        assert self._pipeline is not None
        errors: list[str] = []
        required_keys = ["name", "version", "phases", "execution_order"]
        for key in required_keys:
            if key not in self._pipeline.data:
                errors.append(f"pipeline.yaml missing required key: {key}")
        return errors

    def _validate_step_ids(self) -> list[str]:
        assert self._pipeline is not None
        errors: list[str] = []
        execution_ids = set(self.get_execution_order())
        defined_ids = set(self._pipeline.steps.keys())

        missing_files = execution_ids - defined_ids
        for step_id in sorted(missing_files):
            errors.append(f"execution_order references unknown step: {step_id}")

        orphan_steps = defined_ids - execution_ids
        for step_id in sorted(orphan_steps):
            errors.append(f"step file defined but not in execution_order: {step_id}")

        return errors

    def _validate_execution_order(self) -> list[str]:
        assert self._pipeline is not None
        errors: list[str] = []
        execution_order = self._pipeline.data.get("execution_order", [])
        seen: set[str] = set()

        for index, entry in enumerate(execution_order):
            if not isinstance(entry, dict):
                errors.append(f"execution_order[{index}] must be a mapping")
                continue

            step_id = entry.get("step")
            if not step_id:
                errors.append(f"execution_order[{index}] missing 'step'")
                continue

            if step_id in seen:
                errors.append(f"duplicate step in execution_order: {step_id}")
            seen.add(step_id)

        return errors

    def _validate_step_dependencies(self) -> list[str]:
        assert self._pipeline is not None
        errors: list[str] = []
        ordered_ids = self.get_execution_order()
        position = {step_id: idx for idx, step_id in enumerate(ordered_ids)}

        for step_id in ordered_ids:
            step = self._pipeline.steps.get(step_id)
            if not step:
                continue

            for dep in step.depends_on:
                if dep not in position:
                    errors.append(f"step '{step_id}' depends on unknown step '{dep}'")
                    continue

                if position[dep] >= position[step_id]:
                    errors.append(
                        f"step '{step_id}' depends on '{dep}' but '{dep}' is not earlier in execution_order"
                    )

        return errors

    def _validate_code_references(self) -> list[str]:
        if not self.validate_code_refs:
            return []

        assert self._pipeline is not None
        errors: list[str] = []

        all_steps = list(self._pipeline.steps.values()) + list(
            self._pipeline.freesurfer_substeps.values()
        )

        for step in all_steps:
            ref = step.code_reference
            if not ref:
                continue

            file_path = ref.get("file")
            if not file_path:
                errors.append(f"step '{step.id}' code_reference missing 'file'")
                continue

            resolved = self.repo_root / file_path
            if not resolved.exists():
                errors.append(f"step '{step.id}' code_reference file not found: {file_path}")
                continue

            function_name = ref.get("function")
            if function_name:
                # Support "Class.method" and comma-separated lists in metadata
                names = [name.strip() for name in str(function_name).split(",")]
                content = resolved.read_text(encoding="utf-8", errors="replace")
                for raw_name in names:
                    method = raw_name.split(".")[-1]
                    patterns = [
                        rf"def\s+{re.escape(method)}\s*\(",
                        rf"async def\s+{re.escape(method)}\s*\(",
                    ]
                    if not any(re.search(pattern, content) for pattern in patterns):
                        errors.append(
                            f"step '{step.id}' code_reference function not found: "
                            f"{raw_name} in {file_path}"
                        )

        return errors

    def _validate_freesurfer_subpipeline(self) -> list[str]:
        assert self._pipeline is not None
        errors: list[str] = []

        parent_step = self._pipeline.steps.get("freesurfer-processing")
        if not parent_step:
            parent_step = self._pipeline.steps.get("freesurfer-segmentation")
        if not parent_step:
            return errors

        subpipeline = self._pipeline.freesurfer_subpipeline
        if not subpipeline:
            errors.append("freesurfer-segmentation step exists but steps/freesurfer/pipeline.yaml is missing")
            return errors

        macro_order = subpipeline.get("macro_execution_order", [])
        macro_ids = {entry["step"] for entry in macro_order if isinstance(entry, dict) and "step" in entry}

        micro_order = subpipeline.get("micro_execution_order", [])
        micro_ids = {entry["step"] for entry in micro_order if isinstance(entry, dict) and "step" in entry}

        defined_substeps = set(self._pipeline.freesurfer_substeps.keys())
        missing_micro = micro_ids - defined_substeps
        for step_id in sorted(missing_micro):
            errors.append(f"freesurfer micro_execution_order references unknown substep: {step_id}")

        orphan_micro = defined_substeps - micro_ids
        for step_id in sorted(orphan_micro):
            errors.append(f"freesurfer substep defined but not in micro_execution_order: {step_id}")

        if macro_ids and not macro_ids.issubset(defined_substeps | {"autorecon1", "autorecon2-volonly", "mri-segstats"}):
            undefined_macros = macro_ids - defined_substeps - {"autorecon1", "autorecon2-volonly", "mri-segstats"}
            for step_id in sorted(undefined_macros):
                errors.append(f"freesurfer macro step not defined: {step_id}")

        return errors
