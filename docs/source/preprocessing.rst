Preprocessing
=============

AutoHS is a two-step participant-level workflow.

Pipeline overview
-----------------

.. code-block:: text

   BIDS T1w  →  Step 1: Segmentation  →  Step 2: AI-compute  →  Reports

Step 1 — Segmentation
---------------------

Default: FreeSurfer
~~~~~~~~~~~~~~~~~~~

* Container: ``freesurfer/freesurfer:7.4.1`` (Docker) or ``freesurfer_7.4.1.sif`` (Apptainer)
* Command: ``recon-all -autorecon1 -autorecon2-volonly``
* Post-step: ``mri_segstats`` → ``stats/aseg.stats``
* Typical runtime: **2–4 hours** per subject on CPU

Optional: FastSurfer (``--fastsurfer``)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

* Container: ``deepmi/fastsurfer:latest`` or ``fastsurfer_latest.sif``
* Command: ``run_fastsurfer.sh --seg_only --device cpu``
* Stats: ``stats/aseg+DKT.stats``
* Typical runtime: **30–60 minutes** per subject on CPU

Step 2 — AI-compute
-------------------

Runs in the AutoHS Python environment (native on Apptainer/HPC, Docker image otherwise).

1. Parse hippocampal volumes from segmentation stats
2. Compute asymmetry index: ``AI = (L − R) / (L + R)``
3. Apply HS classification thresholds
4. Generate ``report.json``, ``summary.txt``, ``report.pdf``, and optional overlays

Processing a subject/session pair
---------------------------------

For each T1w file matched by BIDS queries:

1. Copy input to an isolated work directory
2. Run segmentation with subject id ``job_<label>``
3. Run AI-compute referencing segmentation output
4. Publish reports to ``output_dir/autohs/sub-*/ses-*/``

Enabling and disabling steps
----------------------------

+------------------+-------------------------------+
| Flag             | Effect                        |
+==================+===============================+
| ``--fastsurfer`` | Use FastSurfer instead of FS  |
+------------------+-------------------------------+
| (default)        | FreeSurfer vol-only recon-all |
+------------------+-------------------------------+

What is happening?
------------------

During FreeSurfer you may see long pauses at Talairach registration, subcortical
segmentation, and white-matter segmentation — this is expected.

During FastSurfer, monitor ``scripts/deep-seg.log`` under the work directory for CNN
segmentation progress.

References
----------

See :doc:`citation` for the publication describing the hippocampal asymmetry index and
HS classification thresholds.
