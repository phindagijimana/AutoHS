# AutoHS — Runnable Workflow

Two-step hippocampal asymmetry pipeline:

| Step | ID | Container |
|------|-----|-----------|
| 1 | `freesurfer-processing` | `freesurfer/freesurfer:7.4.1` |
| 2 | `ai-compute` | `autohs/ai-compute:latest` |

## Run locally

```bash
./AutoHS install
./AutoHS build
./AutoHS submit scan_T1w.nii.gz
./AutoHS run
```

## Step 2 — AI-compute container

Post-processing and reporting:

- Parse `aseg.stats` hippocampal volumes
- Compute asymmetry index: `AI = (L − R) / (L + R)`
- HS classification (Ndagijimana et al., Brain Communications, in press)
- Optional coronal overlays
- `report.json`, `report.pdf`, `summary.txt`

Build only the container:

```bash
docker compose build ai-compute
docker run --rm autohs/ai-compute:latest --help
```

## Publication

> Ndagijimana P, Brennan D, Shinohara R, Gugger J. **MRI derived hippocampal asymmetry identifies hippocampal sclerosis in epilepsy surgical specimens.** *Brain Communications*. Accepted (in press).

Legacy 18-step specification files are archived under `steps/archive/`. FreeSurfer micro-phases remain documented under `steps/freesurfer/`.
