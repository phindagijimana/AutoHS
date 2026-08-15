# AutoHS

**Automated Hippocampal Sclerosis Workflow** — a structured, machine-readable pipeline for T1-weighted MRI analysis: hippocampal segmentation, volumetric extraction, asymmetry indexing, and clinical review.

AutoHS is a **runnable two-step workflow** for hippocampal asymmetry analysis from T1-weighted MRI. It queues jobs and runs them when Docker and system resources are available.

## What this repo contains

```
AutoHS/
├── AutoHS                  # CLI: install, build, submit, run, queue, logs
├── ai_compute/             # Step 2 container code (post-processing + reporting)
├── docker/
│   └── Dockerfile.ai-compute
├── docker-compose.yml
├── workflow/
│   ├── pipeline.yaml       # 2-step runnable pipeline
│   ├── runner.py           # Orchestrates FreeSurfer → AI-compute
│   ├── queue.py            # SQLite job queue
│   └── steps/
│       ├── 01-freesurfer-processing.yaml
│       └── 02-ai-compute.yaml
└── data/jobs/              # Job workspaces (created at runtime)
```

## Runnable workflow (2 steps)

| Step | Name | Container | What it does |
|------|------|-----------|--------------|
| **1** | FreeSurfer processing | `freesurfer/freesurfer:7.4.1` | `recon-all` + `mri_segstats` → `aseg.stats` |
| **2** | AI-compute | `autohs/ai-compute:latest` | Extract volumes, asymmetry index, overlays, PDF report |

Jobs stay **pending** until `./AutoHS run` and resources are ready (Docker, disk, RAM, images, queue slot).

## CLI

```bash
chmod +x ./AutoHS

./AutoHS install              # Python deps + validate pipeline
./AutoHS build                # Build ai-compute container
./AutoHS submit scan_T1w.nii.gz
./AutoHS run                  # Run pending job if resources available
./AutoHS queue                # List jobs + resource status
./AutoHS logs
./AutoHS status
```

| Command | Description |
|---------|-------------|
| `install` | Create `venv/`, install dependencies, validate pipeline |
| `build` | Build `autohs/ai-compute:latest` from `docker/Dockerfile.ai-compute` |
| `submit` | Queue a T1 NIfTI scan for processing |
| `run` | Execute step 1 then step 2 for oldest pending job when resources allow |
| `queue` | Show job queue and resource readiness |
| `start` | Validate pipeline + run unit tests |
| `logs` | Tail `logs/autohs.log` |

### Prerequisites

- Docker (with `freesurfer/freesurfer:7.4.1` pulled)
- FreeSurfer `license.txt` in repo root (see `license.txt.example`)
- T1 NIfTI input (`.nii` or `.nii.gz`)

```bash
cp license.txt.example license.txt   # then paste your FreeSurfer license
./AutoHS install && ./AutoHS build
./AutoHS submit path/to/T1w.nii.gz
./AutoHS run
```

Outputs per job: `data/jobs/{job_id}/output/report.json`, `report.pdf`, `summary.txt`

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

This metric is computed in **AI-compute (step 2)** and is central to the AutoHS screening workflow described in the associated publication.

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
- Docker
- FreeSurfer license (`license.txt`)
- PyYAML, psutil (`workflow/requirements.txt`)

No Redis or PostgreSQL required — jobs are tracked in SQLite at `data/autohs.db`.

Implementation reference: [NeuroInsight](https://github.com/phindagijimana/neuroinsight_local) (full web application).

## License

Workflow definitions: MIT (see NeuroInsight project for application licensing and FreeSurfer terms).

© 2025 University of Rochester. All rights reserved.
