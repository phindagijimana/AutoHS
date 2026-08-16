Usage
=====

The AutoHS preprocessing workflow takes as principal input the path of the dataset that
is to be processed. The input dataset is required to be in valid BIDS format with at
least one T1-weighted anatomical series. We highly recommend that you validate your
dataset with the free, online BIDS Validator.

The command follows the `BIDS Apps <https://bids.neuroimaging.io/bids_apps.html>`_ convention,
similar to `QSIPrep <https://qsiprep.readthedocs.io/en/stable/usage.html>`_ and fMRIPrep.

Example
-------

.. code-block:: bash

   autohs data/bids_root/ out/ participant \
     --participant-label 001 \
     --fs-license-file /path/to/license.txt \
     -w out/work/

Command-Line Arguments
----------------------

Positional Arguments
~~~~~~~~~~~~~~~~~~~~

``bids_dir``
   The root folder of a BIDS-valid dataset (``sub-*`` folders at the top level).

``output_dir``
   The output path for AutoHS derivatives and visual reports.

``analysis_level``
   Processing stage to run. AutoHS currently supports only ``participant``.

Options for filtering BIDS queries
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

``--participant-label``
   One or more participant labels **without** the ``sub-`` prefix (e.g. ``001`` ``002``).
   If omitted, all subjects with T1w data are processed.

``--session-label``
   Restrict processing to specific sessions (without the ``ses-`` prefix).

``--skip-bids-validator``
   Skip ``bids-validator`` (useful on air-gapped clusters).

``--bids-filter-file``
   JSON file with PyBIDS filters for the ``t1w`` query (QSIPrep-style). Example::

      { "t1w": { "session": "1", "run": "1" } }

Options to handle performance
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

``-w``, ``--work-dir``
   Working directory for intermediate segmentation files. Defaults to
   ``<output_dir>/work``.

``--nthreads``
   CPU threads for FreeSurfer / FastSurfer.

``--runtime {docker,apptainer,auto}``
   Container runtime. ``auto`` prefers Docker when the daemon is available, otherwise
   Apptainer/Singularity.

Workflow configuration
~~~~~~~~~~~~~~~~~~~~~~

``--fastsurfer``
   Use FastSurfer (``--seg_only``) instead of FreeSurfer ``recon-all`` for step 1.

``--fs-license-file``
   Path to FreeSurfer ``license.txt``. Not required with ``--fastsurfer``.

``--reports-only``
   Skip segmentation and re-run AI-compute plus derivative publishing from an
   existing ``-w`` work directory (requires prior full run for the same subject/session).

``--not-stop-on-first-crash``
   Continue processing remaining subjects when one scan fails (default: stop immediately).

Methods boilerplate
~~~~~~~~~~~~~~~~~~~

``--md-only-boilerplate``
   Print Markdown methods text for manuscripts and exit (NiPreps-style). Combine with
   ``--fastsurfer`` when FastSurfer was used. Does not require ``bids_dir`` arguments::

      python run.py --md-only-boilerplate > methods_autohs.md

Participant mode
----------------

AutoHS runs independently per subject (and per session when multiple T1w sessions exist).
Parallel runs can share the same ``output_dir`` as long as subject/session labels do not
overlap.

Group level
-----------

Group-level analysis is **not** implemented. AutoHS produces participant-level HS
classification and asymmetry metrics only.

Preparing data for AutoHS
-------------------------

AutoHS is a BIDS App: data must follow the BIDS specification for anatomical T1w scans.

Required inputs
~~~~~~~~~~~~~~~

* ``sub-<label>/anat/sub-<label>_T1w.nii.gz`` or
* ``sub-<label>/ses-<label>/anat/sub-<label>_ses-<label>_T1w.nii.gz``

Supported suffix
~~~~~~~~~~~~~~~~

Only ``*_T1w.nii`` and ``*_T1w.nii.gz`` files are used. Other contrasts (T2w, FLAIR)
are ignored.

FreeSurfer license
~~~~~~~~~~~~~~~~~~

When using the default FreeSurfer backend, provide a valid FreeSurfer license via
``--fs-license-file`` or by placing ``license.txt`` in the AutoHS repository root.
