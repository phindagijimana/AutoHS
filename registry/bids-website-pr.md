# Pull request text for bids-standard/bids-website

## Title
Add AutoHS to BIDS Apps listing

## Body

Adds AutoHS (`phindagijimana/AutoHS`) to the BIDS Apps tool listing.

AutoHS is a BIDS App for hippocampal sclerosis screening from T1w MRI. It performs
FreeSurfer or FastSurfer segmentation, hippocampal volume extraction, asymmetry
index computation, and clinical reporting with BIDS Derivatives outputs.

- GitHub: https://github.com/phindagijimana/AutoHS
- Docker Hub: `autohs/autohs`
- Documentation: https://autohs.readthedocs.io
- CI: GitHub Actions workflow `CI` on branch `main`

## apps.yml entry

```yaml
- gh: phindagijimana/AutoHS
  dh: autohs/autohs
  description: >-
    Automated hippocampal sclerosis workflow from T1w MRI: segmentation,
    hippocampal volumes, asymmetry index, and clinical reports.
  status: active
  ds_type:
    - raw
  datatype:
    - anat
  ci: gh
  branch: main
  workflow: CI
```
