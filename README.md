# AutoHS

[![CI](https://github.com/phindagijimana/AutoHS/actions/workflows/ci.yml/badge.svg)](https://github.com/phindagijimana/AutoHS/actions/workflows/ci.yml)
[![Documentation](https://readthedocs.org/projects/autohs/badge/?version=latest)](https://autohs.readthedocs.io/en/latest/?badge=latest)

**Automated hippocampal sclerosis (HS) screening** from T1-weighted MRI — a [BIDS App](https://bids.neuroimaging.io/bids_apps.html) for epilepsy surgical workup and research.

📖 **Documentation:** [autohs.readthedocs.io](https://autohs.readthedocs.io)

AutoHS segments T1w scans (FreeSurfer or FastSurfer), extracts hippocampal volumes, computes the asymmetry index, applies published HS thresholds, and publishes BIDS derivatives with clinical reports. See the [theory page](https://autohs.readthedocs.io/en/latest/theory.html) for the scientific background.

## Quick start (BIDS App)

```bash
git clone https://github.com/phindagijimana/AutoHS.git
cd AutoHS
pip install -r requirements-bids.txt

# IDEAS sample (two public subjects)
./scripts/download_ideas_sample.sh
python run.py sample_data/ideas_bids bids_output participant \
  --participant-label 1 2 --fastsurfer --runtime apptainer -w bids_output/work
```

Results appear under `bids_output/autohs/sub-*/`. Full install options (Docker, Apptainer, HPC): [installation](https://autohs.readthedocs.io/en/latest/installation.html).

## Run on your data

```bash
python run.py /path/to/bids /path/to/output participant \
  --participant-label 001 \
  --fastsurfer \
  --runtime apptainer
```

On Apptainer/HPC, set `FREESURFER_SIF` and/or `FASTSURFER_SIF` before running. See [usage](https://autohs.readthedocs.io/en/latest/usage.html) for all CLI options.

## Containers

| Artifact | Where |
|----------|-------|
| Docker | `autohs/autohs:latest` (after maintainers publish; build locally with `docker/Dockerfile.bidsapp`) |
| Apptainer | `autohs_<version>.sif` on [GitHub Releases](https://github.com/phindagijimana/AutoHS/releases) |

The BIDS App image **orchestrates** segmentation (FreeSurfer/FastSurfer) and AI-compute; it does not bundle those tools in a single monolithic image. See [installation](https://autohs.readthedocs.io/en/latest/installation.html#architecture).

## Citation

If you use AutoHS, cite the Brain Communications asymmetry paper and this software. BibTeX and dataset references: [`CITATION.cff`](CITATION.cff) and [citation docs](https://autohs.readthedocs.io/en/latest/citation.html).

## Legacy job-queue CLI

The `./AutoHS` bash CLI (submit/run/queue for single NIfTI files) is documented in [workflow/README.md](workflow/README.md). The **recommended** entry point for BIDS datasets is `run.py`.

## Related software

| Project | Role |
|---------|------|
| **AutoHS** (this repo) | BIDS App, pipeline, containers |
| **[NeuroInsight-AutoHS](https://github.com/phindagijimana/neuroinsight_local)** | Web dashboard and deployment |

## License

MIT — see [`LICENSE`](LICENSE). FreeSurfer and FastSurfer have separate license terms when used as segmentation backends.
