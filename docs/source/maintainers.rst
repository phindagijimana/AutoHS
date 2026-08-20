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
8. Optional: reopen the BIDS website listing PR (see `BIDS Apps hub listing`_ below).

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

BIDS Apps hub listing
---------------------

Listing AutoHS on the `BIDS Apps directory <https://bids.neuroimaging.io/bids_apps.html>`_
is **optional and currently deferred**. To submit when ready:

1. Fork `bids-standard/bids-website <https://github.com/bids-standard/bids-website>`_.
2. Add an entry to ``data/tools/apps.yml`` using the template in
   ``registry/bids-website-apps.yml``.
3. Open a pull request — draft text is in ``registry/bids-website-pr.md``. Reference the
   Docker Hub namespace (``autohs/autohs``) and the CI workflow name (``CI`` on ``main``).

Publishing a Docker Hub image first is recommended, since the listing advertises it.

To host the repository under `github.com/bids-apps <https://github.com/bids-apps>`_, email
``bids.maintenance+apps@gmail.com`` with the repository URL and Docker Hub namespace.

Roadmap
-------

See :doc:`roadmap` for staged completion status.
