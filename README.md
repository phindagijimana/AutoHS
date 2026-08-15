# AutoHS

**Automated Hippocampal Sclerosis Workflow** — a structured, machine-readable pipeline for T1-weighted MRI analysis: hippocampal segmentation, volumetric extraction, asymmetry indexing, and clinical review.

AutoHS documents the end-to-end workflow used by [NeuroInsight](https://github.com/phindagijimana/neuroinsight_local). It is a standalone specification you can validate, extend, or plug into orchestration tools (Airflow, Temporal, etc.) without shipping the full application.

## What this repo contains

```
AutoHS/
└── workflow/               # Pipeline definitions, loader, tests
    ├── README.md           # Detailed workflow documentation
    ├── pipeline.yaml       # Master pipeline (5 phases, 18 steps)
    ├── steps/              # Per-step YAML specs
    ├── load_pipeline.py    # Python loader + validator
    └── validate.py         # CLI validation tool
```

## Pipeline overview

| Phase | Description |
|-------|-------------|
| **Intake** | Upload T1 NIfTI, store file, register job |
| **Orchestration** | Queue dispatch and task startup |
| **Processing** | FreeSurfer segmentation → volume extraction → asymmetry → visualizations |
| **Finalization** | Persist metrics, complete job, advance queue |
| **Delivery** | Dashboard, slice viewer, PDF report |

**18 top-level steps**, including a nested **17-step FreeSurfer sub-pipeline** (motion correction through `mri_segstats`).

### Asymmetry index

Hippocampal asymmetry is computed as:

```
AI = (L − R) / (L + R)
```

where L and R are left and right hippocampal volumes (mm³).

## Quick start

```bash
git clone https://github.com/phindagijimana/AutoHS.git
cd AutoHS

pip install -r workflow/requirements.txt

# Validate pipeline structure
python -m workflow.validate

# Run tests
python -m unittest workflow.tests.test_workflow -v
```

## Documentation

- **[workflow/README.md](workflow/README.md)** — full pipeline reference, progress ranges, FreeSurfer sub-steps, Python loader API
- **[workflow/pipeline.yaml](workflow/pipeline.yaml)** — master definition with execution order and job state machine
- **[workflow/diagrams/](workflow/diagrams/)** — Mermaid flowcharts

## Relationship to NeuroInsight

| Repo | Role |
|------|------|
| **AutoHS** (this repo) | Workflow specification — steps, dependencies, progress, code references |
| **[neuroinsight_local](https://github.com/phindagijimana/neuroinsight_local)** | Runnable application — API, UI, FreeSurfer processing, deployment |

Step files include `code_reference` fields pointing to NeuroInsight source modules. When AutoHS is cloned alone, file-existence checks are skipped; clone both repos side-by-side for strict validation.

## Requirements

- Python 3.9+
- PyYAML (`workflow/requirements.txt`)

No Redis, PostgreSQL, or Docker required to **validate** the workflow definitions. Running actual MRI processing requires the NeuroInsight application stack.

## License

Workflow definitions: MIT (see NeuroInsight project for application licensing and FreeSurfer terms).

© 2025 University of Rochester. All rights reserved.
