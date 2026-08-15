# AutoHS

[![CI](https://github.com/phindagijimana/AutoHS/actions/workflows/ci.yml/badge.svg)](https://github.com/phindagijimana/AutoHS/actions/workflows/ci.yml)
[![Documentation](https://readthedocs.org/projects/autohs/badge/?version=latest)](https://autohs.readthedocs.io/en/latest/?badge=latest)

**Automated Hippocampal Sclerosis Workflow** — a BIDS App and runnable pipeline for T1-weighted MRI: hippocampal segmentation, volumetric extraction, asymmetry indexing, and clinical review.

📖 **Documentation:** [autohs.readthedocs.io](https://autohs.readthedocs.io)

🐳 **Docker:** `docker pull autohs/autohs:latest` (after release; see [Maintainers](docs/source/maintainers.rst))

AutoHS is a **runnable two-step workflow** for hippocampal asymmetry analysis. It queues jobs and runs them when Docker and system resources are available.

## Runnable workflow (2 steps)

| Step | Name | Container | What it does |
|------|------|-----------|--------------|
| **1** | FreeSurfer processing | `freesurfer/freesurfer:7.4.1` | `recon-all` + `mri_segstats` → `aseg.stats` |
| **2** | AI-compute | `autohs/ai-compute:latest` | Extract volumes, asymmetry index, overlays, PDF report |

## BIDS App

AutoHS follows the [BIDS Apps](https://bids.neuroimaging.io/bids_apps.html) specification.

```bash
# Install BIDS dependencies
pip install -r requirements-bids.txt

# Run on a BIDS dataset (Apptainer/HPC example)
python run.py /path/to/bids /path/to/output participant \
  --participant-label 001 \
  --fastsurfer \
  --runtime apptainer

# Docker
docker build -f docker/Dockerfile.bidsapp -t autohs/autohs:latest .
docker run --rm -v /data/bids:/data:ro -v /data/out:/out autohs/autohs:latest \
  /data /out participant --participant-label 001 --fastsurfer
```

Outputs: `output/autohs/sub-*/` with `report.json`, `report.pdf`, `summary.txt`.

Full documentation: [docs/source/index.rst](docs/source/index.rst) (Sphinx / Read the Docs layout, QSIPrep-style).

See also the `./AutoHS` CLI for single-file job queue workflows.

## What this repo contains

```
AutoHS/
├── AutoHS                  # CLI: install, build, submit, run, queue, logs
├── ai_compute/             # Step 2 container code (post-processing + reporting)
├── docker/
│   └── Dockerfile.ai-compute
├── docker-compose.yml
├── workflow/
│   ├── pipeline.yaml       # 2-step pipeline definition
│   ├── runner.py           # Orchestrates FreeSurfer → AI-compute
│   ├── queue.py            # SQLite job queue
│   └── steps/
│       ├── 01-freesurfer-processing.yaml
│       └── 02-ai-compute.yaml
└── data/jobs/              # Job workspaces (created at runtime)
```

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

**Volume laterality** (threshold ±0.05):

| Condition | Interpretation |
|-----------|----------------|
| **AI > 0.05** | Left hippocampus larger than right |
| **AI < −0.05** | Right hippocampus larger than left |
| **−0.05 ≤ AI ≤ 0.05** | Symmetric volumes |

**Hippocampal sclerosis (HS) classification** (publication thresholds):

| Condition | Interpretation |
|-----------|----------------|
| **AI > 0.046915816971433** | Left-dominant (Right HS suspected) |
| **AI < −0.070839747728063** | Right-dominant (Left HS suspected) |
| Otherwise | Balanced (No HS) |

These rules are applied in **AI-compute (step 2)** and written to `report.json`, `summary.txt`, and `report.pdf`.

## Citation

If you use AutoHS or the asymmetry index in research, please cite:

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

**AutoHS software reference:**

```bibtex
@software{autohs2026,
  title  = {AutoHS: Automated Hippocampal Sclerosis Workflow},
  author = {Ndagijimana, Philbert},
  year   = {2026},
  url    = {https://github.com/phindagijimana/AutoHS}
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

- **[autohs.readthedocs.io](https://autohs.readthedocs.io)** — AutoHS BIDS App documentation
- **[workflow/README.md](workflow/README.md)** — pipeline reference, progress ranges, FreeSurfer sub-steps
- **[workflow/pipeline.yaml](workflow/pipeline.yaml)** — master definition with execution order and job state machine
- **[workflow/diagrams/](workflow/diagrams/)** — Mermaid flowcharts

## Related software

| Project | Repository | Role |
|---------|------------|------|
| **AutoHS** (this repo) | [AutoHS](https://github.com/phindagijimana/AutoHS) | Pipeline spec, CLI, BIDS App, Docker runner |
| **NeuroInsight-AutoHS** | [neuroinsight_local](https://github.com/phindagijimana/neuroinsight_local) | Full web application that implements the AutoHS pipeline |

## Requirements

- Python 3.9+
- Docker
- FreeSurfer license (`license.txt`)
- PyYAML, psutil (`workflow/requirements.txt`)

No Redis or PostgreSQL required — jobs are tracked in SQLite at `data/autohs.db`.

## License

Workflow definitions: MIT. See project licensing and FreeSurfer terms for processing components.

© 2025 University of Rochester. All rights reserved.
