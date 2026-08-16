"""Methods-section boilerplate for publications using AutoHS."""

from __future__ import annotations

METHODS_MARKDOWN = """\
## Structural MRI preprocessing and hippocampal asymmetry

T1-weighted structural MRI scans organized in the Brain Imaging Data Structure \
(BIDS; Gorgolewski et al., 2016) were processed with AutoHS \
(https://github.com/phindagijimana/AutoHS), a BIDS App for hippocampal sclerosis \
screening. Skull-stripped segmentation was performed with {segmentation_backend} \
({segmentation_citation}). Hippocampal volumes were extracted from the segmentation \
statistics, and the asymmetry index (AI) was computed as (left − right) / \
(left + right). Hippocampal sclerosis classification followed the thresholds \
described by Ndagijimana et al. (2026, Brain Communications, in press). \
AutoHS version {version} was executed in participant mode with the BIDS App \
command-line interface.

### Software references

- AutoHS: https://github.com/phindagijimana/AutoHS
- BIDS: Gorgolewski KJ, et al. Scientific Data. 2016;3:160044. doi:10.1038/sdata.2016.44
- {segmentation_reference}
- Ndagijimana P, et al. Brain Communications. 2026 (in press).
"""

BACKEND_INFO = {
    "freesurfer": {
        "segmentation_backend": "FreeSurfer 7.4.1 recon-all (volume-only stages)",
        "segmentation_citation": "Fischl, 2012",
        "segmentation_reference": (
            "FreeSurfer: Fischl B. NeuroImage. 2012;62(2):774-781. "
            "doi:10.1016/j.neuroimage.2012.01.021"
        ),
    },
    "fastsurfer": {
        "segmentation_backend": "FastSurfer (segmentation-only mode, CPU)",
        "segmentation_citation": "Henschel et al., 2020",
        "segmentation_reference": (
            "FastSurfer: Henschel L, Conrad M, Reuter M. NeuroImage. 2020;219:117012. "
            "doi:10.1016/j.neuroimage.2020.117012"
        ),
    },
}


def methods_boilerplate(*, version: str, fastsurfer: bool = False) -> str:
    backend = BACKEND_INFO["fastsurfer" if fastsurfer else "freesurfer"]
    return METHODS_MARKDOWN.format(version=version, **backend)
