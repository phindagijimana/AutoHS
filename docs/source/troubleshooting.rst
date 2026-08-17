Troubleshooting
===============

Common errors and fixes when running AutoHS as a BIDS App.

BIDS validation failures
------------------------

**Symptom:** ``bids-validator`` exits non-zero before processing starts.

**Fix:**

* Validate locally: ``bids-validator /path/to/bids``
* On air-gapped clusters: ``--skip-bids-validator`` (ensure layout is correct manually)
* Confirm T1w files use the ``*_T1w.nii`` or ``*_T1w.nii.gz`` suffix under ``anat/``

No T1w scans found
------------------

**Symptom:** ``FileNotFoundError: No T1w scans found under ...``

**Fix:**

* Check ``--participant-label`` matches folder names (``sub-001`` → label ``001``; ``sub-1`` → ``1``)
* If using ``--bids-filter-file``, confirm the JSON matches your dataset sessions/runs
* Run without filters first to confirm discovery works

FreeSurfer license errors
-------------------------

**Symptom:** ``FreeSurfer license not found``

**Fix:**

* Pass ``--fs-license-file /path/to/license.txt``
* Or place ``license.txt`` in the AutoHS repo root or ``~/.freesurfer/license.txt``
* Or use ``--fastsurfer`` (no FreeSurfer license required)

Container / runtime errors
--------------------------

**Symptom:** ``docker: command not found`` or Apptainer bind errors.

**Fix:**

* HPC: ``export AUTOHS_RUNTIME=apptainer`` and set ``FREESURFER_SIF`` / ``FASTSURFER_SIF``
* Explicit runtime: ``--runtime apptainer``
* Verify SIF paths exist and are readable on compute nodes

**Symptom:** Segmentation container exits immediately.

**Fix:**

* Check disk space in ``-w`` work directory (FreeSurfer needs several GB per subject)
* Inspect logs under ``<work_dir>/sub-*_ses-*/freesurfer/`` or FastSurfer ``scripts/deep-seg.log``
* Increase ``--nthreads`` only if CPUs are available; oversubscription can slow runs

``--reports-only`` failures
---------------------------

**Symptom:** ``reports-only`` cannot find prior segmentation.

**Fix:**

* Run a full pipeline first for the same subject/session with the same ``-w`` path
* Do not combine ``--reports-only`` with ``--fastsurfer`` (segmentation backend is inferred from work dir)

Partial batch failures
----------------------

**Symptom:** One subject fails in a multi-subject run.

**Fix:**

* Default behavior stops on the first failure
* Continue other subjects: ``--not-stop-on-first-crash`` (failed scans are logged; successful scans still publish)

Performance
-------------

**Symptom:** FreeSurfer takes many hours.

**Expected:** vol-only ``recon-all`` is CPU-heavy. Use ``--fastsurfer`` for faster turnaround when appropriate.

**Symptom:** CI or laptop runs hang.

**Fix:** Use mocked/integration fixtures for development; run real segmentation on HPC with Apptainer.

Getting help
------------

* Open an issue: https://github.com/phindagijimana/AutoHS/issues
* Include: AutoHS version (``python run.py --version``), command line, and the last 50 lines of logs
* Other inquiries: :doc:`contact`
