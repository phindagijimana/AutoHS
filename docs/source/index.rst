NeuroInsight-AutoHS documentation
===================================

**NeuroInsight-AutoHS** is the runnable application that implements the
`AutoHS pipeline <https://github.com/phindagijimana/AutoHS>`_. It is also distributed
as a `BIDS App <https://bids.neuroimaging.io/bids_apps.html>`_ named **AutoHS** for
hippocampal asymmetry analysis from T1-weighted MRI.

It performs segmentation (FreeSurfer or FastSurfer), extracts hippocampal volumes,
computes the asymmetry index (AI), and generates clinical reports for hippocampal
sclerosis (HS) screening.

NeuroInsight-AutoHS is designed for epilepsy surgical workup and research cohorts with
BIDS-organized T1w anatomical scans.

AutoHS pipeline reference
-------------------------

The canonical workflow definition (steps, dependencies, validation) lives in the
`AutoHS repository <https://github.com/phindagijimana/AutoHS>`_ under ``workflow/``.

.. toctree::
   :maxdepth: 2
   :caption: Contents

   installation
   quickstart
   usage
   outputs
   preprocessing
   citation
   roadmap
   maintainers

Indices and tables
==================

* :ref:`genindex`
* :ref:`search`
