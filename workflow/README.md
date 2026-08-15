# AutoHS pipeline — NeuroInsight-AutoHS

This directory defines the **[AutoHS pipeline](https://github.com/phindagijimana/AutoHS)** executed by **NeuroInsight-AutoHS** — a two-step hippocampal asymmetry workflow for T1-weighted MRI.

| Step | ID | Container |
|------|-----|-----------|
| 1 | `freesurfer-processing` | `freesurfer/freesurfer:7.4.1` |
| 2 | `ai-compute` | `autohs/ai-compute:latest` |

**Pipeline reference:** [github.com/phindagijimana/AutoHS](https://github.com/phindagijimana/AutoHS)

## Run locally

```bash
./AutoHS install
./AutoHS build
./AutoHS submit scan_T1w.nii.gz
./AutoHS run
```

## Step 2 — AI-compute container

Post-processing and reporting for the AutoHS pipeline:

- Parse `aseg.stats` hippocampal volumes
- Compute asymmetry index: `AI = (L − R) / (L + R)`
- Volume laterality: Left > Right if AI > 0.05; Right > Left if AI < −0.05; symmetric between
- HS classification: Right HS if AI > 0.046915816971433; Left HS if AI < −0.070839747728063
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
