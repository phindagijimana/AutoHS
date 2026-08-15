# AutoHS — Automated Hippocampal Sclerosis Workflow

This repository defines the **NeuroInsight** analysis pipeline as a structured, multi-step workflow. It documents how T1-weighted MRI scans flow from upload through FreeSurfer segmentation to asymmetry metrics and clinical review.

Each step maps to modules in the [NeuroInsight](https://github.com/phindagijimana/neuroinsight_local) application. Code references in step files point to that repo when run standalone here.

## Structure

```
workflow/
├── README.md                 # This file
├── __init__.py
├── load_pipeline.py          # Python loader + validator
├── validate.py               # CLI: python -m workflow.validate
├── requirements.txt          # PyYAML (for loader/CI)
├── pipeline.yaml             # Master pipeline (phases, steps, dependencies)
├── steps/                    # One file per top-level step (01–18)
│   ├── 01-upload-validate.yaml
│   ├── ...
│   ├── 08-freesurfer-segmentation.yaml
│   └── freesurfer/           # Nested sub-pipeline for step 08
│       ├── pipeline.yaml
│       └── substeps/         # 17 FreeSurfer recon-all micro-phases
├── tests/
│   └── test_workflow.py
└── diagrams/
    └── pipeline.mmd
```

## Pipeline at a glance

| Phase | Steps | Trigger |
|-------|-------|---------|
| **Intake** | Upload → Store → Register job | User uploads via UI |
| **Orchestration** | Queue → Dispatch Celery task | API after job creation |
| **Processing** | Validate → Prepare → FreeSurfer → Extract → Asymmetry → Visualize → Save | Celery worker |
| **Finalization** | Extract metrics → Complete job → Start next pending | Celery worker |
| **Delivery** | Dashboard → Viewer → PDF report | User views completed job |

## Job status lifecycle

```
PENDING → RUNNING → COMPLETED
                 ↘ FAILED
                 ↘ CANCELLED (user delete)
```

Queue limits: **1 running** + **5 pending** jobs maximum.

## Code mapping

| Layer | Primary paths |
|-------|----------------|
| Upload / API | `backend/api/upload_simple.py` |
| Job management | `backend/services/job_service.py` |
| Task queue | `workers/tasks/processing_web.py` |
| MRI pipeline | `pipeline/processors/mri_processor.py` |
| Metrics | `pipeline/utils/asymmetry.py`, `backend/services/metric_service.py` |
| Visualizations | `pipeline/utils/visualization.py`, `backend/api/visualizations.py` |
| Reports | `backend/api/reports.py` |
| Frontend | `frontend/src/pages/`, `frontend/src/components/` |

## Using these definitions

- **CLI:** Run `./AutoHS install`, `./AutoHS start`, `./AutoHS logs` from the repo root (see root README)
- **Onboarding:** Read `pipeline.yaml`, then drill into `steps/` for each step's inputs, outputs, and code references.
- **Debugging:** Match a stuck job's `current_step` / `progress` field to the step's `progress_range` in the step file.
- **Validation:** Run `python -m workflow.validate` from the repo root
- **Standalone repo:** Code-reference checks are skipped unless a `backend/` directory exists (full NeuroInsight checkout)
- **CI:** GitHub Actions job `workflow-validation` runs on every push/PR.
- **Future orchestration:** `pipeline.yaml` is structured so a workflow engine (Airflow, Temporal, custom runner) could load step metadata without rewriting business logic.

## Python loader

```python
from workflow import PipelineLoader

loader = PipelineLoader()
pipeline = loader.load()
errors = loader.validate()          # raises PipelineValidationError if invalid
order = loader.get_execution_order()  # ['upload-validate', 'store-file', ...]
step = loader.get_step("calculate-asymmetry")
```

## FreeSurfer sub-pipeline (step 08)

Step `freesurfer-segmentation` has a nested pipeline at `steps/freesurfer/pipeline.yaml`:

| Macro phase | Micro steps |
|-------------|-------------|
| **autorecon1** | motioncor → talairach → nu correction → intensity norm → skull stripping |
| **autorecon2-volonly** | em reg → ca reg (longest) → subcort seg → … → fill |
| **post-processing** | mri_segstats → aseg.stats |

Progress within 20–90% is driven by `#@#` markers in `recon-all-status.log` (see `mri_processor.py` phase_weights).

## Progress ranges (processing phase)

| Progress | Step |
|----------|------|
| 5% | Celery task init |
| 10% | Prepare input |
| 20–90% | FreeSurfer segmentation |
| 92% | Extract hippocampal volumes |
| 95% | Calculate asymmetry |
| 97% | Generate visualizations |
| 99% | Save results |
| 100% | Job complete |
