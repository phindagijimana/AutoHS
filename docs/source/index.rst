AutoHS documentation
====================

.. image:: https://readthedocs.org/projects/autohs/badge/?version=latest
   :target: https://autohs.readthedocs.io/en/latest/?badge=latest
   :alt: Documentation Status

**AutoHS** is a `BIDS App <https://bids.neuroimaging.io/bids_apps.html>`_ for hippocampal
asymmetry analysis from T1-weighted MRI. It performs segmentation (FreeSurfer or
FastSurfer), extracts hippocampal volumes, computes the asymmetry index (AI), and
generates clinical reports for hippocampal sclerosis (HS) screening.

AutoHS is designed for epilepsy surgical workup and research cohorts with BIDS-organized
T1w anatomical scans.

Related software
----------------

`NeuroInsight-AutoHS <https://github.com/phindagijimana/neuroinsight_local>`_ is the full
web application that implements the AutoHS pipeline (dashboard, API, deployment).

.. toctree::
   :maxdepth: 2
   :caption: Contents

   installation
   quickstart
   sample_data
   usage
   outputs
   preprocessing
   methods
   faq
   troubleshooting
   citation
   changes
   roadmap
   bids_apps_hub
   maintainers
   privacy

Indices and tables
==================

* :ref:`genindex`
* :ref:`search`
