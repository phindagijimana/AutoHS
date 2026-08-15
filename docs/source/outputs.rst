Outputs
=======

AutoHS writes BIDS derivatives under ``<output_dir>/autohs/``, following the same
organizational pattern as QSIPrep (pipeline name as top-level derivatives folder).

Directory layout
----------------

.. code-block:: text

   output_dir/
   ├── work/                          # intermediate files (optional -w path)
   └── autohs/
       ├── dataset_description.json   # BIDS derivative metadata
       ├── autohs_run.json            # run summary
       └── sub-<label>/
           └── ses-<label>/           # omitted when no session
               ├── report.json
               ├── report.pdf
               ├── summary.txt
               ├── ai_compute_result.json
               └── visualizations/
                   └── coronal/
                       └── slice_*.png

Participant reports
---------------------

``report.json``
   Machine-readable metrics: left/right hippocampal volumes (mm³), asymmetry index,
   volume laterality, and HS classification with publication thresholds.

``summary.txt``
   Human-readable one-page summary suitable for clinical review.

``report.pdf``
   Formatted PDF report with metrics and interpretation.

Visual reports
--------------

When nibabel and matplotlib are available, coronal overlay PNGs are saved under
``visualizations/coronal/`` showing hippocampal labels (FreeSurfer labels 17 and 53).

Quality control
---------------

Check ``autohs_run.json`` for the number of processed scans, pipeline backend
(FreeSurfer vs FastSurfer), and completion timestamp.

Hippocampal sclerosis classification
------------------------------------

Metrics follow the Brain Communications (in press) thresholds:

+-------------------------------+-----------------------------------+
| Condition                     | Interpretation                    |
+===============================+===================================+
| AI > 0.046915816971433        | Left-dominant (Right HS suspected)|
+-------------------------------+-----------------------------------+
| AI < −0.070839747728063       | Right-dominant (Left HS suspected)|
+-------------------------------+-----------------------------------+
| otherwise                     | Balanced (No HS)                  |
+-------------------------------+-----------------------------------+

Volume laterality uses ±0.05 (AutoHS defaults).

Provenance
----------

``dataset_description.json`` records AutoHS version and citation text in
``HowToAcknowledge``.
