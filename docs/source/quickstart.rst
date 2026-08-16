Quick Start
===========

Validate your dataset
---------------------

AutoHS expects a BIDS-valid dataset with at least one T1-weighted anatomical scan per
subject. We recommend validating with the `BIDS Validator <https://bids-standard.github.io/bids-validator/>`_.

.. code-block:: bash

   bids-validator /path/to/bids_dataset

Docker example (one subject)
----------------------------

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

FastSurfer quick start
----------------------

FastSurfer is typically **5–10× faster** than FreeSurfer on CPU and does not require a
FreeSurfer license:

.. code-block:: bash

   python run.py /path/to/bids_dataset /path/to/output participant \
     --participant-label 001 \
     --fastsurfer \
     --runtime apptainer

IDEAS sample dataset (recommended)
----------------------------------

Download two public IDEAS subjects (OpenNeuro ``ds005602``), then run AutoHS:

.. code-block:: bash

   ./scripts/download_ideas_sample.sh

   python run.py sample_data/ideas_bids bids_output participant \
     --participant-label 1 2 \
     --fastsurfer \
     --runtime apptainer \
     -w bids_output/work

See :doc:`sample_data` and :doc:`citation` for required IDEAS, FreeSurfer, and FastSurfer
citations.

Outputs appear under ``bids_output/autohs/sub-*/``.
