FAQ
===

General
-------

**Is AutoHS a BIDS App?**

Yes. AutoHS follows the `BIDS Apps <https://bids.neuroimaging.io/bids_apps.html>`_ command-line
convention: ``autohs bids_dir output_dir participant [options]``.

**Does AutoHS support group-level analysis?**

No. AutoHS runs at the **participant** level only. See :doc:`usage`.

**FreeSurfer or FastSurfer?**

* **FreeSurfer** (default): conventional subcortical segmentation; requires a license; ~2–4 h/subject on CPU.
* **FastSurfer** (``--fastsurfer``): deep-learning segmentation; no FreeSurfer license; ~30–60 min/subject.

Both backends use the same AI-compute step and HS thresholds. Details: :doc:`theory`.

Data requirements
-----------------

**What inputs does AutoHS need?**

At least one BIDS T1w anatomical scan per subject or session. Other modalities are ignored.

**Can I process only some subjects or sessions?**

Use ``--participant-label`` and ``--session-label``, or ``--bids-filter-file`` — see :doc:`usage`.

Outputs
-------

**Where are results written?**

Under ``<output_dir>/autohs/``. File layout and thresholds: :doc:`outputs` and :doc:`theory`.

**Can I regenerate reports without re-running segmentation?**

Yes, with ``--reports-only`` when the ``-w`` work directory contains prior segmentation.

Containers and HPC
------------------

**Docker image not found?**

Build locally (``docker/Dockerfile.bidsapp``), use a GitHub Release ``.sif``, or wait for
Docker Hub publish — see :doc:`installation`.

**How do I run on Slurm / Apptainer?**

Set ``FREESURFER_SIF`` / ``FASTSURFER_SIF`` and ``--runtime apptainer``. See :doc:`installation`.

**Something failed during a run?**

See :doc:`troubleshooting`.

Citations
---------

**What should I cite?**

AutoHS software, the Brain Communications asymmetry paper, and any datasets or tools you used.
See :doc:`citation`.

**Methods text for my manuscript?**

``python run.py --md-only-boilerplate`` — see :doc:`methods`.
