Maintaining AutoHS
==================

This page describes how maintainers publish releases to match the production bar used
by apps such as QSIPrep.

Release checklist
-----------------

1. Bump ``version`` in the repository root and ``CITATION.cff`` ``version`` / ``date-released``.
2. Update ``CHANGELOG.md`` and ``docs/source/changes.rst``.
3. Merge to ``main``.
4. Tag and push: ``git tag v0.1.0 && git push origin v0.1.0``
5. Confirm GitHub Actions: **CI**, **Documentation**, **Publish Docker Image**, **Release Apptainer Image**.
6. Confirm Read the Docs build for ``main`` / the tag.
7. Optional: PR to `bids-standard/bids-website` using ``registry/bids-website-apps.yml`` (see :doc:`bids_apps_hub`).
8. Enable `Zenodo-GitHub integration <https://zenodo.org/account/settings/github/>`_ and add the
   release DOI to ``CITATION.cff`` (remove the placeholder after the first Zenodo archive).

Read the Docs
-------------

One-time setup:

1. Sign in at `<https://readthedocs.org>`_ with GitHub.
2. Import the repository (direct link):
   `<https://readthedocs.org/dashboard/import/manual/?url=https://github.com/phindagijimana/AutoHS>`_
3. Set the project **slug** to ``autohs`` so docs resolve at ``autohs.readthedocs.io``.
4. RTD reads ``.readthedocs.yaml`` automatically.
5. Set the default branch to ``main`` and enable PR previews (optional).

Run ``./scripts/setup_ecosystem.sh`` for a full maintainer checklist (RTD, Docker Hub, Zenodo).

Local doc build:

.. code-block:: bash

   pip install -r docs/requirements.txt
   make -C docs html

Docker Hub
----------

One-time setup:

1. Create a Docker Hub repository: ``autohs/autohs`` (or your org namespace).
2. Add GitHub repository secrets:

   * ``DOCKERHUB_USERNAME``
   * ``DOCKERHUB_TOKEN`` (access token, not password)

3. Push a semver tag to trigger **Publish Docker Image**, or run the workflow manually.

Without ``DOCKERHUB_USERNAME`` / ``DOCKERHUB_TOKEN``, CI still **builds** the image but
does not push to Docker Hub (see ``scripts/setup_ecosystem.sh``).

Users install with:

.. code-block:: bash

   docker pull autohs/autohs:latest

Apptainer on HPC:

.. code-block:: bash

   apptainer build autohs.sif docker://autohs/autohs:latest

Or download ``autohs_<version>.sif`` from `GitHub Releases <https://github.com/phindagijimana/AutoHS/releases>`_.

BIDS Apps hub
-------------

See :doc:`bids_apps_hub` for listing AutoHS on the BIDS website and optional ``bids-apps`` org onboarding.

Roadmap
-------

See :doc:`roadmap` for the full staged plan.
