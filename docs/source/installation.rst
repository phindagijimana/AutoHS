Installation
============

AutoHS can be installed as a BIDS App using Docker, Apptainer/Singularity, or directly
from source on HPC systems.

Docker Container
----------------

Pull the published BIDS App image (after maintainers configure Docker Hub):

.. code-block:: bash

   docker pull autohs/autohs:latest

Or build locally:

.. code-block:: bash

   docker build -f docker/Dockerfile.bidsapp -t autohs/autohs:latest .

Run:

.. code-block:: bash

   docker run --rm \
     -v /path/to/bids:/data:ro \
     -v /path/to/output:/out \
     -v /path/to/license.txt:/license.txt:ro \
     autohs/autohs:latest \
     /data /out participant \
     --participant-label 001 \
     --fs-license-file /license.txt

Documentation is hosted on Read the Docs:

`<https://autohs.readthedocs.io/en/latest/>`_

Apptainer / Singularity Container
---------------------------------

On shared HPC clusters without Docker, build a ``.sif`` from the Docker image:

.. code-block:: bash

   apptainer build autohs.sif docker://autohs/autohs:latest

Set segmentation SIF paths when running outside the bundled Docker stack:

.. code-block:: bash

   export FREESURFER_SIF=/path/to/freesurfer_7.4.1.sif
   export FASTSURFER_SIF=/path/to/fastsurfer_latest.sif
   export AUTOHS_RUNTIME=apptainer

These variables are **required** for Apptainer runs (no site-specific defaults are shipped
in the repository).

Python / Source Install
-----------------------

For development or Apptainer-only HPC nodes:

.. code-block:: bash

   git clone https://github.com/phindagijimana/AutoHS.git
   cd AutoHS
   ./AutoHS install
   pip install -r requirements-bids.txt

External Dependencies
---------------------

+------------------+------------------------------------------+------------------------------------------+
| Dependency       | Required for                             | Notes                                    |
+==================+==========================================+==========================================+
| T1w BIDS dataset | Always                                   | At least one ``*_T1w.nii*``              |
+------------------+------------------------------------------+------------------------------------------+
| FreeSurfer       | Default segmentation                     | ``license.txt`` required                 |
+------------------+------------------------------------------+------------------------------------------+
| FastSurfer       | ``--fastsurfer``                         | No FreeSurfer license needed             |
+------------------+------------------------------------------+------------------------------------------+
| Docker           | Default runtime when available           | Or Apptainer on HPC                      |
+------------------+------------------------------------------+------------------------------------------+
| bids-validator   | Optional                                 | Use ``--skip-bids-validator`` to skip    |
+------------------+------------------------------------------+------------------------------------------+

FreeSurfer license
~~~~~~~~~~~~~~~~~~

Place ``license.txt`` in the repo root or pass ``--fs-license-file``. FreeSurfer is
**not** required when using ``--fastsurfer``.
