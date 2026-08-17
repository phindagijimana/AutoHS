Quick Start
===========

This page shows **example commands** to run AutoHS. Install options (Docker, Apptainer,
source) are on :doc:`installation`.

Validate your dataset
---------------------

AutoHS expects a BIDS-valid dataset with at least one T1-weighted anatomical scan per
subject. We recommend validating with the `BIDS Validator <https://bids-standard.github.io/bids-validator/>`_.

.. code-block:: bash

   bids-validator /path/to/bids_dataset

IDEAS sample (recommended first run)
------------------------------------

Download two public IDEAS subjects (OpenNeuro ``ds005602``), then run AutoHS:

.. code-block:: bash

   ./scripts/download_ideas_sample.sh

   python run.py sample_data/ideas_bids bids_output participant \
     --participant-label 1 2 \
     --fastsurfer \
     --runtime apptainer \
     -w bids_output/work

See :doc:`sample_data` and :doc:`citation` for required citations. Outputs:
``bids_output/autohs/sub-*/``.

Docker example (one subject)
----------------------------

Requires FreeSurfer ``license.txt`` when not using ``--fastsurfer``.

.. code-block:: bash

   docker run --rm \
     -v /path/to/bids_dataset:/data:ro \
     -v /path/to/output:/out \
     -v /path/to/license.txt:/license.txt:ro \
     autohs/autohs:latest \
     /data /out participant \
     --participant-label 001 \
     --fs-license-file /license.txt

Apptainer example (HPC)
-----------------------

Set ``FREESURFER_SIF`` / ``FASTSURFER_SIF`` before running (see :doc:`installation`).

.. code-block:: bash

   export AUTOHS_RUNTIME=apptainer
   export FREESURFER_SIF=/path/to/freesurfer_7.4.1.sif

   apptainer exec --bind /path/to/bids_dataset:/data:ro \
     --bind /path/to/output:/out \
     --bind /path/to/license.txt:/license.txt:ro \
     autohs.sif \
     /data /out participant \
     --participant-label 001 \
     --fs-license-file /license.txt

FastSurfer (no FreeSurfer license)
----------------------------------

.. code-block:: bash

   python run.py /path/to/bids_dataset /path/to/output participant \
     --participant-label 001 \
     --fastsurfer \
     --runtime apptainer

FastSurfer is typically **5–10× faster** than FreeSurfer on CPU. CLI reference: :doc:`usage`.
