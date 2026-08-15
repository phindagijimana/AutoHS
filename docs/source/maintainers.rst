Maintaining AutoHS
==================

This page describes how maintainers publish releases to match the production bar used
by apps such as QSIPrep.

Release checklist
-----------------

1. Bump ``version`` in the repository root.
2. Update ``docs/source/changes.rst`` (create on first release).
3. Merge to ``main``.
4. Tag and push: ``git tag v0.1.0 && git push origin v0.1.0``
5. Confirm GitHub Actions: **CI**, **Documentation**, **Publish Docker Image**.
6. Confirm Read the Docs build for ``main`` / the tag.

Read the Docs
-------------

One-time setup:

1. Sign in at `<https://readthedocs.org>`_ with GitHub.
2. Import the ``phindagijimana/AutoHS`` repository.
3. RTD reads ``.readthedocs.yaml`` automatically.
4. Set the default branch to ``main`` and enable PR previews (optional).

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

Users install with:

.. code-block:: bash

   docker pull autohs/autohs:latest

Apptainer on HPC:

.. code-block:: bash

   apptainer build autohs.sif docker://autohs/autohs:latest

Roadmap to QSIPrep-level maturity
-----------------------------------

See :doc:`roadmap` for the full staged plan.
