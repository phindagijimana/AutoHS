AutoHS documentation
====================

.. image:: https://readthedocs.org/projects/autohs/badge/?version=latest
   :target: https://autohs.readthedocs.io/en/latest/?badge=latest
   :alt: Documentation Status

**AutoHS** is a `BIDS App <https://bids.neuroimaging.io/bids_apps.html>`_ for automated
**hippocampal sclerosis (HS) screening** from T1-weighted MRI. It is designed for epilepsy
surgical workup and research cohorts with BIDS-organized anatomical scans.

What problem does AutoHS solve?
-------------------------------

Temporal lobe epilepsy is often associated with **hippocampal sclerosis** — atrophy and
structural change in one hippocampus. Clinicians look for **left–right hippocampal volume
asymmetry** on MRI. AutoHS turns that question into a reproducible, quantitative pipeline:

#. **Segment** the T1w scan (FreeSurfer or FastSurfer) to label subcortical structures
#. **Measure** left and right hippocampal volumes (mm³)
#. **Compute** the asymmetry index (AI): :math:`(L - R) / (L + R)`
#. **Classify** volume laterality and apply published **HS screening thresholds**
#. **Publish** JSON metrics, a clinical summary, and a PDF report as BIDS derivatives

AutoHS is **decision-support software**, not a standalone diagnosis. Results should be
interpreted with clinical context, EEG, and pathology when available.

Start here
----------

New users:

* :doc:`theory` — **science and theory** (clinical background, AI formula, thresholds)
* :doc:`quickstart` — run on sample or your own BIDS dataset in minutes
* :doc:`installation` — Docker, Apptainer, or source install

Researchers writing a paper:

* :doc:`methods` — generate methods-section boilerplate (``python run.py --md-only-boilerplate``)
* :doc:`citation` — required references for AutoHS, IDEAS sample data, and third-party tools

Related software
----------------

`NeuroInsight-AutoHS <https://github.com/phindagijimana/neuroinsight_local>`_ is the full
web application that implements the AutoHS pipeline (dashboard, API, deployment).

.. toctree::
   :maxdepth: 2
   :caption: Contents

   theory
   installation
   quickstart
   sample_data
   usage
   outputs
   preprocessing
   methods
   faq
   troubleshooting
   contributing
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
