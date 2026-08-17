Maintaining AutoHS
==================

Release checklist
-----------------

1. Bump ``version`` in the repository root and ``CITATION.cff`` (``version`` / ``date-released``).
2. Update ``CHANGELOG.md`` and ``docs/source/changes.rst``.
3. Merge to ``main``.
4. Tag and push: ``git tag v0.1.10 && git push origin v0.1.10``
5. Confirm GitHub Actions: **CI**, **Documentation**, **Publish Docker Image**, **Release Apptainer Image**.
6. Confirm Read the Docs build for ``main`` / the tag.
7. After Zenodo archives the release, add the concept DOI to ``CITATION.cff`` ``identifiers``.
8. Optional: reopen BIDS website listing PR using ``registry/bids-website-apps.yml`` (see :doc:`bids_apps_hub`).

Read the Docs
-------------

Live site: `<https://autohs.readthedocs.io/en/latest/>`_

Configuration is in ``.readthedocs.yaml``. Local build:

.. code-block:: bash

   pip install -r docs/requirements.txt
   sphinx-build -W -b html docs/source docs/_build/html

Docker Hub
----------

1. Create repository ``autohs/autohs`` on Docker Hub.
2. Add GitHub secrets ``DOCKERHUB_USERNAME`` and ``DOCKERHUB_TOKEN``.
3. Push a semver tag to trigger **Publish Docker Image**, or run the workflow manually.

Without secrets, CI still **builds** the image but does not push (see ``scripts/setup_ecosystem.sh``).

Zenodo
------

1. Enable GitHub integration at `<https://zenodo.org/account/settings/github/>`_ for AutoHS.
2. Publish a semver GitHub release — Zenodo archives automatically.
3. Copy the **concept DOI** into ``CITATION.cff``.

Run ``./scripts/setup_ecosystem.sh`` for a printable checklist.

BIDS Apps hub
-------------

See :doc:`bids_apps_hub` (listing is optional and currently deferred).

Roadmap
-------

See :doc:`roadmap` for staged completion status.
