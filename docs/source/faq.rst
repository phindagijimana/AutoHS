FAQ
===

General
-------

**Is AutoHS a BIDS App?**

Yes. AutoHS follows the `BIDS Apps <https://bids.neuroimaging.io/bids_apps.html>`_ command-line
convention: ``autohs bids_dir output_dir participant [options]``.

**Does AutoHS support group-level analysis?**

No. AutoHS runs at the **participant** level only and produces per-subject HS screening
reports. Aggregate statistics should be computed downstream from the published JSON metrics.

**FreeSurfer or FastSurfer?**

* **FreeSurfer** (default): gold-standard segmentation; requires a license; ~2–4 h/subject on CPU.
* **FastSurfer** (``--fastsurfer``): deep-learning segmentation; no FreeSurfer license; ~30–60 min/subject.

Both backends feed the same AI-compute step and HS classification thresholds.

Data requirements
-----------------

**What inputs does AutoHS need?**

At least one BIDS T1w anatomical scan per subject or session. FLAIR and diffusion data are
ignored.

**Can I process only some subjects?**

Yes: ``--participant-label 001 002`` (labels without the ``sub-`` prefix).

**Can I filter sessions or runs?**

Use ``--session-label`` or a PyBIDS ``--bids-filter-file`` JSON (see :doc:`usage`).

Outputs
-------

**Where are results written?**

Under ``<output_dir>/autohs/`` with BIDS Derivatives-style filenames (``desc-autohs``).

**What is the asymmetry index (AI)?**

``AI = (L − R) / (L + R)`` using hippocampal volumes from segmentation statistics. See
:doc:`outputs` for HS classification thresholds.

**Can I regenerate reports without re-running segmentation?**

Yes, with ``--reports-only`` after a full run populated the ``-w`` work directory.

Containers and HPC
------------------

**Docker image not found?**

Pull ``autohs/autohs:latest`` after maintainers publish to Docker Hub, build locally from
``docker/Dockerfile.bidsapp``, or download ``autohs_<version>.sif`` from
`GitHub Releases <https://github.com/phindagijimana/AutoHS/releases>`_.

**How do I run on Slurm without Docker?**

Use Apptainer with ``--runtime apptainer`` and set ``FREESURFER_SIF`` / ``FASTSURFER_SIF``.
See :doc:`installation`.

Citations
---------

**What should I cite?**

AutoHS software, the Brain Communications asymmetry paper, and any datasets or third-party
tools you used (IDEAS, FreeSurfer, FastSurfer). See :doc:`citation`.

**Methods text for my manuscript?**

Run ``python run.py --md-only-boilerplate`` or see :doc:`methods`.
