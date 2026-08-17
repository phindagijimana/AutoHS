Contributing
============

AutoHS welcomes bug reports, documentation improvements, and pull requests.

Report issues
-------------

Open a GitHub issue with:

* AutoHS version (``python run.py --version``)
* Full command line and runtime (Docker / Apptainer / source)
* Last ~50 lines of relevant logs

Development setup
-----------------

.. code-block:: bash

   git clone https://github.com/phindagijimana/AutoHS.git
   cd AutoHS
   pip install -r requirements-bids.txt
   pip install -r workflow/requirements.txt

Run tests
---------

.. code-block:: bash

   export PYTHONPATH="$PWD"
   python -m unittest discover -s workflow/tests -p 'test_*.py' -v

Build documentation locally
---------------------------

.. code-block:: bash

   pip install -r docs/requirements.txt
   sphinx-build -W -b html docs/source docs/_build/html

Documentation changes
---------------------

* User-facing prose lives in ``docs/source/`` (reStructuredText).
* Keep **science and thresholds** on :doc:`theory` only; link from other pages.
* Keep **run examples** on :doc:`quickstart`; :doc:`installation` covers install and architecture.
* Update ``CHANGELOG.md`` and ``docs/source/changes.rst`` when releasing.

Pull requests
-------------

1. Fork and branch from ``main``.
2. Run the test suite (above).
3. If you change docs, run ``sphinx-build -W``.
4. Describe what changed and how you tested it.

Maintainers: see :doc:`maintainers` for release and ecosystem steps.
