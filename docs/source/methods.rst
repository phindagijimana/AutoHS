Methods boilerplate
===================

AutoHS provides copy-paste methods text for manuscripts, similar to NiPreps BIDS Apps
(fMRIPrep, QSIPrep).

Generate boilerplate
--------------------

FreeSurfer backend (default):

.. code-block:: bash

   python run.py --md-only-boilerplate

FastSurfer backend:

.. code-block:: bash

   python run.py --md-only-boilerplate --fastsurfer

Write to a file:

.. code-block:: bash

   python run.py --md-only-boilerplate > methods_autohs.md

Example output
--------------

.. code-block:: markdown

   ## Structural MRI preprocessing and hippocampal asymmetry

   T1-weighted structural MRI scans organized in the Brain Imaging Data Structure
   (BIDS; Gorgolewski et al., 2016) were processed with AutoHS ...

Customize the ``{segmentation_backend}`` paragraph by passing ``--fastsurfer`` when your
study used FastSurfer.

Additional citations
--------------------

Always cite:

* AutoHS software (``CITATION.cff`` / GitHub repository)
* Ndagijimana et al., Brain Communications (in press) — asymmetry index and HS thresholds
* Your segmentation backend (FreeSurfer or FastSurfer)
* BIDS (Gorgolewski et al., 2016)
* Any **datasets** used (e.g. IDEAS — see :doc:`sample_data` and :doc:`citation`)
