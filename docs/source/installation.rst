Installation
============

AutoHS can be installed as a BIDS App using Docker, Apptainer/Singularity, or directly
from source on HPC systems. For a first run after install, see :doc:`quickstart`.

Architecture
------------

The published BIDS App image (``autohs/autohs``) is an **orchestrator**: it discovers BIDS
T1w scans, invokes **segmentation** (FreeSurfer or FastSurfer in a separate container or
SIF), then runs **AI-compute** (hippocampal volumes, asymmetry index, reports). Segmentation
backends are **not** embedded in the orchestrator image — you provide Docker images or
Apptainer SIF paths at runtime (see below).

Docker Container
----------------

Pull the published image (after maintainers configure Docker Hub):

.. code-block:: bash

   docker pull autohs/autohs:latest

Or build locally:

.. code-block:: bash

   docker build -f docker/Dockerfile.bidsapp -t autohs/autohs:latest .

Run examples: :doc:`quickstart`.

Apptainer / Singularity Container
---------------------------------

Download a release artifact or build from Docker:

.. code-block:: bash

   apptainer build autohs.sif docker://autohs/autohs:latest

Or download ``autohs_<version>.sif`` from
`GitHub Releases <https://github.com/phindagijimana/AutoHS/releases>`_.

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

Documentation is hosted at `<https://autohs.readthedocs.io/en/latest/>`_.
