BIDS Apps hub registration
==========================

AutoHS follows the `BIDS Apps specification <https://bids.neuroimaging.io/bids_apps.html>`_.
To list the app on the community hub and BIDS website, maintainers complete the steps
below (one-time, plus updates on major releases).

Docker Hub image
----------------

Published image: ``autohs/autohs`` (tags ``0.1.0``, ``latest``, …).

Users run:

.. code-block:: bash

   docker run --rm -v /data:/data:ro -v /out:/out autohs/autohs:latest \
     /data/bids /out participant --participant-label 001

Apptainer / Singularity
-----------------------

On each semver tag, GitHub Actions builds a ``.sif`` from the BIDS App Docker image and
attaches it to the GitHub release (``autohs_<version>.sif``).

Download from `GitHub Releases <https://github.com/phindagijimana/AutoHS/releases>`_ or
build locally:

.. code-block:: bash

   apptainer build autohs.sif docker://autohs/autohs:0.1.0

List on the BIDS website
------------------------

1. Fork `bids-standard/bids-website <https://github.com/bids-standard/bids-website>`_.
2. Add an entry to ``data/tools/apps.yml`` using the template in
   ``registry/bids-website-apps.yml`` in this repository.
3. Open a pull request describing AutoHS, Docker Hub namespace, and CI workflow name
   (``CI`` on branch ``main``).

Optional: BIDS Apps GitHub organization
---------------------------------------

To host under `github.com/bids-apps <https://github.com/bids-apps>`_, email
``bids.maintenance+apps@gmail.com`` with the repository URL and Docker Hub namespace.

Citation metadata
-----------------

Software and publication citations are in ``CITATION.cff`` at the repository root.
See :doc:`citation` for the preferred publication reference.
