# IDEAS sample BIDS dataset (2 subjects)

This directory contains **two subjects** from the [Imaging Database for Epilepsy And
Surgery (IDEAS)](https://sites.google.com/view/cnnp-lab/ideas-data) release, fetched
from [OpenNeuro ds005602](https://openneuro.org/datasets/ds005602).

| Subject   | Modality | Source path |
|-----------|----------|-------------|
| `sub-1`   | T1w      | OpenNeuro `ds005602/sub-1/anat/` |
| `sub-2`   | T1w      | OpenNeuro `ds005602/sub-2/anat/` |

## Download

If the NIfTI files are not present (they are not tracked in git), run:

```bash
./scripts/download_ideas_sample.sh
```

## Run AutoHS

```bash
python run.py sample_data/ideas_bids bids_output participant \
  --participant-label 1 2 \
  --fastsurfer \
  --runtime apptainer \
  -w bids_output/work
```

## Required citations

When you use these scans, cite the IDEAS dataset publication:

> Taylor PN, Wang Y, Simpson C, et al. The imaging database for epilepsy and surgery (IDEAS). *Epilepsia*. 2025;66(2):471-481. https://doi.org/10.1111/epi.18192

Also cite the OpenNeuro deposit:

> OpenNeuro dataset ds005602 (DOI: 10.18112/openneuro.ds005602.v1.0.0)

Full IDEAS resources (FLAIR, diffusion MRI, resection masks, clinical metadata) are listed at
[https://sites.google.com/view/cnnp-lab/ideas-data](https://sites.google.com/view/cnnp-lab/ideas-data).

## License

IDEAS data are shared under **CC0** (see `dataset_description.json`).
