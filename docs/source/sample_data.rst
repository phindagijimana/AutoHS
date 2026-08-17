Sample data
===========

AutoHS ships a **two-subject IDEAS sample** for tutorials, integration testing, and
method development. The data are real T1-weighted scans from the Imaging Database for
Epilepsy And Surgery (`IDEAS <https://sites.google.com/view/cnnp-lab/ideas-data>`_).

Location
--------

.. code-block:: text

   sample_data/ideas_bids/
   ├── dataset_description.json
   ├── participants.tsv
   ├── README.md
   ├── SOURCES.json
   ├── sub-1/anat/sub-1_T1w.nii.gz
   └── sub-2/anat/sub-2_T1w.nii.gz

Download
--------

NIfTI files are **not stored in git** (size). Fetch them with:

.. code-block:: bash

   chmod +x scripts/download_ideas_sample.sh
   ./scripts/download_ideas_sample.sh

Data are pulled from `OpenNeuro ds005602 <https://openneuro.org/datasets/ds005602>`_ (CC0).

Example run
-----------

See :doc:`quickstart` for a full IDEAS example command.

Citations
---------

When using this sample, cite the IDEAS dataset and OpenNeuro deposit. See :doc:`citation`
for BibTeX entries and third-party tool references (FreeSurfer, FastSurfer, BIDS, PyBIDS).

Full IDEAS resources (442+ subjects, FLAIR, diffusion MRI, resection masks, clinical
metadata) are listed on the
`CNNP Lab IDEAS page <https://sites.google.com/view/cnnp-lab/ideas-data>`_.
