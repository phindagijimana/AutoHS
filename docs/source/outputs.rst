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
               ├── sub-<label>_ses-<label>_desc-autohs_metrics.json
               ├── sub-<label>_ses-<label>_desc-autohs_summary.txt
               ├── sub-<label>_ses-<label>_desc-autohs_provenance.json
               ├── report.json        # legacy alias of metrics JSON
               └── figures/
                   ├── sub-<label>_ses-<label>_desc-autohs_report.pdf
                   └── sub-<label>_ses-<label>_desc-autohs_hippocampus-coronal*.png

Participant reports
---------------------

``*_desc-autohs_metrics.json``
   BIDS-style metrics file with ``Sources``, ``SpatialReference``, and
   ``GeneratedBy`` metadata plus hippocampal volumes, asymmetry index, and HS
   classification.

``*_desc-autohs_summary.txt``
   Human-readable one-page summary suitable for clinical review.

``figures/*_desc-autohs_report.pdf``
   Formatted PDF report with metrics and interpretation.

``*_desc-autohs_provenance.json``
   AI-compute provenance sidecar with pipeline outputs and source T1w URI.

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
