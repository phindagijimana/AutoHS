# AutoHS

[![CI](https://github.com/phindagijimana/AutoHS/actions/workflows/ci.yml/badge.svg)](https://github.com/phindagijimana/AutoHS/actions/workflows/ci.yml)
[![Documentation](https://readthedocs.org/projects/autohs/badge/?version=latest)](https://autohs.readthedocs.io/en/latest/?badge=latest)

**Automated hippocampal sclerosis (HS) screening** from T1-weighted MRI — a [BIDS App](https://bids.neuroimaging.io/bids_apps.html) for epilepsy surgical workup and research.

📖 **Documentation:** [autohs.readthedocs.io](https://autohs.readthedocs.io)

AutoHS segments T1w scans (FreeSurfer or FastSurfer), extracts hippocampal volumes, computes the asymmetry index, applies published HS thresholds, and publishes BIDS derivatives with clinical reports. See the [theory page](https://autohs.readthedocs.io/en/latest/theory.html) for the scientific background.

## NeuroInsight platform

**NeuroInsight** is an umbrella platform for automated neuroimaging **workflows**. **AutoHS** is the first workflow (this repository). The deployable application that runs AutoHS is **[NeuroInsight-AutoHS](https://github.com/phindagijimana/neuroinsight_local)**.

```text
NeuroInsight (platform)
  └── AutoHS (this repo — workflow / BIDS App / method)
        └── NeuroInsight-AutoHS (web & desktop app)
```

Platform overview: [NeuroInsight landing page](https://phindagijimana.github.io/neuroinsight_landing_web/). App deployment: [docs/USER_GUIDE.md](docs/USER_GUIDE.md) and [neuroinsight_local](https://github.com/phindagijimana/neuroinsight_local).

## Research Software and Licensing

AutoHS is **publicly available, source-available research software** supporting automated hippocampal analysis from T1-weighted MRI and independent evaluation of the hippocampal asymmetry method described in:

Ndagijimana P, Brennan D, Shinohara RT, Gugger JJ.
*MRI derived hippocampal asymmetry identifies hippocampal sclerosis in epilepsy surgical specimens.*
Brain Communications. 2026;8(4):fcag320.
https://doi.org/10.1093/braincomms/fcag320

### Research and validation use

The source code is publicly available to support:

- scientific research
- reproducibility
- independent validation
- education and teaching
- evaluation on independent datasets
- development of research extensions, subject to the [LICENSE](LICENSE)

Independent validation by other research groups is encouraged.

See [VALIDATION.md](VALIDATION.md).

### Commercial use

The current release is distributed under a non-commercial, source-available license.

Commercial use requires a separate commercial license.

Organizations interested in commercial deployment, integration, redistribution, products, services, or other commercial applications should see [COMMERCIAL.md](COMMERCIAL.md).

### Clinical status

This software is research software and has not been cleared or approved by the U.S. Food and Drug Administration as a medical device.

Outputs should not be interpreted as a substitute for professional clinical judgment.

### Licensing history

The software implementation associated with the original publication was released under the MIT License and described in the publication as open-source software.

Beginning with the first commit **after** git tag **`publication-v1.0`**, subsequent releases are distributed under the license contained in the current [LICENSE](LICENSE) file.

The licensing transition does not alter the terms under which earlier versions were validly distributed.

| Release | License |
|---------|---------|
| Tag **`publication-v1.0`** (same commit as **`v1.0.27`**, `0aee2cc`) — publication-associated MIT implementation | MIT License |
| Commits after **`publication-v1.0`** on the default branch | PolyForm Noncommercial License 1.0.0 |

See [COMMERCIAL.md](COMMERCIAL.md) for commercial licensing inquiries.

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

| Layer | Name | Repository |
|-------|------|------------|
| Platform | **NeuroInsight** | [Landing page](https://phindagijimana.github.io/neuroinsight_landing_web/) |
| Workflow | **AutoHS** (this repo) | [AutoHS](https://github.com/phindagijimana/AutoHS) |
| Tool | **NeuroInsight-AutoHS** | [neuroinsight_local](https://github.com/phindagijimana/neuroinsight_local) |

App deployment guide: [docs/USER_GUIDE.md](docs/USER_GUIDE.md).

## Contact

- **Issues / bugs:** [GitHub issues](https://github.com/phindagijimana/AutoHS/issues)
- **Email:** phindagiji@gmail.com

## License

Current releases are distributed under the [PolyForm Noncommercial License 1.0.0](LICENSE) unless you obtained an earlier release under MIT (see **Licensing history** above).

FreeSurfer and FastSurfer have separate license terms when used as segmentation backends.

Copyright (c) 2025 University of Rochester. All rights reserved.
