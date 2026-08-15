# AutoHS

**Automated Hippocampal Sclerosis Workflow** — a structured, machine-readable pipeline for T1-weighted MRI analysis: hippocampal segmentation, volumetric extraction, asymmetry indexing, and clinical review.

AutoHS documents the end-to-end workflow used by [NeuroInsight](https://github.com/phindagijimana/neuroinsight_local). It is a standalone specification you can validate, extend, or plug into orchestration tools (Airflow, Temporal, etc.) without shipping the full application.

## What this repo contains

```
AutoHS/
├── AutoHS                  # Workflow CLI (install, start, logs, stop)
├── README.md
└── workflow/               # Pipeline definitions, loader, tests
    ├── README.md           # Detailed workflow documentation
    ├── pipeline.yaml       # Master pipeline (5 phases, 18 steps)
    ├── steps/              # Per-step YAML specs
    ├── load_pipeline.py    # Python loader + validator
    └── validate.py         # CLI validation tool
```

## CLI

AutoHS includes a command-line tool for installing dependencies, validating the pipeline, and viewing logs:

```bash
chmod +x ./AutoHS

./AutoHS install    # Create venv, install deps, validate pipeline
./AutoHS start      # Validate workflow and run tests
./AutoHS logs       # Show recent log output
./AutoHS stop       # Stop background process (if any)
./AutoHS status     # Show install and validation status
```

| Command | Description |
|---------|-------------|
| `install` | Create `venv/`, install `workflow/requirements.txt`, run initial validation |
| `start` | Validate pipeline + run unit tests; output appended to `logs/autohs.log` |
| `logs` | Tail last 80 lines of `logs/autohs.log` (use `logs -f` to follow) |
| `stop` | Stop background watch process if running |
| `status` | Print environment info and run validation |

Logs are written to `logs/autohs.log`.

## Pipeline overview

| Phase | Description |
|-------|-------------|
| **Intake** | Upload T1 NIfTI, store file, register job |
| **Orchestration** | Queue dispatch and task startup |
| **Processing** | FreeSurfer segmentation → volume extraction → asymmetry → visualizations |
| **Finalization** | Persist metrics, complete job, advance queue |
| **Delivery** | Dashboard, slice viewer, PDF report |

**18 top-level steps**, including a nested **17-step FreeSurfer sub-pipeline** (motion correction through `mri_segstats`).

## Hippocampal asymmetry index

AutoHS implements the MRI-derived hippocampal asymmetry index used to identify hippocampal sclerosis in epilepsy surgical specimens (see [Citation](#citation) below).

FreeSurfer subcortical segmentation yields left and right hippocampal volumes (**L**, **R**) in mm³. The asymmetry index (**AI**) is:

```
AI = (L − R) / (L + R)
```

| Symbol | Meaning |
|--------|---------|
| **L** | Left hippocampal volume (mm³) |
| **R** | Right hippocampal volume (mm³) |
| **AI** | Asymmetry index (dimensionless; typically −1 to +1) |

**Interpretation:**

- **AI > 0** — left hippocampus larger than right  
- **AI < 0** — right hippocampus larger than left  
- **AI ≈ 0** — symmetric volumes  

This metric is computed in workflow step `calculate-asymmetry` and is central to the AutoHS screening workflow described in the associated publication.

## Citation

If you use this workflow or the asymmetry index in research, please cite:

> **Ndagijimana P**, **Brennan D**, **Shinohara R**, **Gugger J**. MRI derived hippocampal asymmetry identifies hippocampal sclerosis in epilepsy surgical specimens. *Brain Communications*. **Accepted (in press)**.

**BibTeX:**

```bibtex
@article{ndagijimana2026mri,
  title   = {MRI derived hippocampal asymmetry identifies hippocampal sclerosis in epilepsy surgical specimens},
  author  = {Ndagijimana, Philbert and Brennan, Daniel and Shinohara, Russell and Gugger, James},
  journal = {Brain Communications},
  year    = {2026},
  note    = {Accepted (in press)}
}
```

## Quick start

```bash
git clone https://github.com/phindagijimana/AutoHS.git
cd AutoHS

chmod +x ./AutoHS
./AutoHS install
./AutoHS start
./AutoHS logs
```

Or manually:

```bash
pip install -r workflow/requirements.txt
python -m workflow.validate
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
