Citation
========

If you use AutoHS or the hippocampal asymmetry index in research, please cite the
publications below.

AutoHS / hippocampal asymmetry
------------------------------

   **Ndagijimana P**, **Brennan D**, **Shinohara R**, **Gugger J**. MRI derived
   hippocampal asymmetry identifies hippocampal sclerosis in epilepsy surgical
   specimens. *Brain Communications*. **Accepted (in press)**.

Sample dataset (IDEAS)
----------------------

The bundled IDEAS sample (``sample_data/ideas_bids/``) comes from the Imaging Database
for Epilepsy And Surgery (`IDEAS <https://sites.google.com/view/cnnp-lab/ideas-data>`_),
hosted on `OpenNeuro ds005602 <https://openneuro.org/datasets/ds005602>`_.

   **Taylor PN**, **Wang Y**, **Simpson C**, et al. The imaging database for epilepsy
   and surgery (IDEAS). *Epilepsia*. 2025;66(2):471-481.
   https://doi.org/10.1111/epi.18192

   OpenNeuro dataset **ds005602** (DOI: 10.18112/openneuro.ds005602.v1.0.0).

If you use IDEAS diffusion MRI or the IDEAS II release, also cite Taylor et al. (2026),
*Epilepsia* (in press): https://doi.org/10.1002/epi.70186

Third-party tools used by AutoHS
--------------------------------

**FreeSurfer** (default segmentation backend):

   **Fischl B**. FreeSurfer. *NeuroImage*. 2012;62(2):774-781.
   https://doi.org/10.1016/j.neuroimage.2012.01.021

**FastSurfer** (optional ``--fastsurfer`` backend):

   **Henschel L**, **Conrad M**, **Reuter M**. FastSurfer - A fast and accurate deep
   learning based neuroimaging pipeline. *NeuroImage*. 2020;219:117012.
   https://doi.org/10.1016/j.neuroimage.2020.117012

**BIDS** (data organization):

   **Gorgolewski KJ**, et al. The brain imaging data structure, a format for organizing
   and describing outputs of neuroimaging experiments. *Scientific Data*. 2016;3:160044.
   https://doi.org/10.1038/sdata.2016.44

**PyBIDS** (dataset indexing in the BIDS App):

   **Yarkoni T**, **Poline JB**, **Gorgolewski KJ**, et al. PyBIDS: Python tools for
   BIDS datasets. https://github.com/bids-standard/pybids

BibTeX
------

.. code-block:: bibtex

   @article{ndagijimana2026mri,
     title   = {MRI derived hippocampal asymmetry identifies hippocampal sclerosis in epilepsy surgical specimens},
     author  = {Ndagijimana, Philbert and Brennan, Daniel and Shinohara, Russell and Gugger, James},
     journal = {Brain Communications},
     year    = {2026},
     note    = {Accepted (in press)}
   }

   @article{taylor2025ideas,
     title   = {The imaging database for epilepsy and surgery (IDEAS)},
     author  = {Taylor, Peter N. and Wang, Yujiang and Simpson, Callum and others},
     journal = {Epilepsia},
     volume  = {66},
     number  = {2},
     pages   = {471--481},
     year    = {2025},
     doi     = {10.1111/epi.18192}
   }

   @article{fischl2012freesurfer,
     title   = {FreeSurfer},
     author  = {Fischl, Bruce},
     journal = {NeuroImage},
     volume  = {62},
     number  = {2},
     pages   = {774--781},
     year    = {2012},
     doi     = {10.1016/j.neuroimage.2012.01.021}
   }

   @article{henschel2020fastsurfer,
     title   = {FastSurfer - A fast and accurate deep learning based neuroimaging pipeline},
     author  = {Henschel, Leonie and Conrad, Martin and Reuter, Martin},
     journal = {NeuroImage},
     volume  = {219},
     pages   = {117012},
     year    = {2020},
     doi     = {10.1016/j.neuroimage.2020.117012}
   }

   @software{autohs2026,
     title  = {AutoHS: Automated Hippocampal Sclerosis Workflow},
     author = {Ndagijimana, Philbert and Brennan, Daniel and Shinohara, Russell and Gugger, James},
     year   = {2026},
     url    = {https://github.com/phindagijimana/AutoHS},
     version = {0.1.9}
   }

Related software
----------------

* `NeuroInsight-AutoHS <https://github.com/phindagijimana/neuroinsight_local>`_ — full web
  application that implements the AutoHS pipeline
* `QSIPrep <https://qsiprep.readthedocs.io/>`_ — BIDS App reference for documentation layout

Software citation file
------------------------

The repository includes ``CITATION.cff`` for automated citation metadata (GitHub and
reference managers). After Zenodo archives a GitHub release, add the concept DOI to
``CITATION.cff`` ``identifiers``. Maintainer steps: :doc:`maintainers` and
``./scripts/setup_ecosystem.sh``.
