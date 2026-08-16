Background and theory
=====================

This page explains the **clinical motivation**, **imaging measurements**, and **classification
logic** behind AutoHS. It is written for clinicians, researchers, and engineers who land on
the documentation site without prior context.

Clinical context
----------------

**Hippocampal sclerosis (HS)** is a common pathological substrate in temporal lobe epilepsy
(TLE). In surgical workup, MRI is used to detect **asymmetric hippocampal atrophy** on the
side of seizure onset. Quantitative hippocampal volumetry and asymmetry metrics can support
screening when visual read is equivocal.

AutoHS automates a reproducible workflow:

1. Segment the T1-weighted scan (FreeSurfer or FastSurfer)
2. Read left and right hippocampal volumes from segmentation statistics
3. Compute the **asymmetry index (AI)**
4. Apply published thresholds for **volume laterality** and **HS screening**

AutoHS is a **decision-support** tool. It does not replace clinical judgment, histopathology,
EEG, or multidisciplinary epilepsy conference review.

What AutoHS measures
--------------------

From each participant's T1w scan, AutoHS extracts:

* **Left hippocampus volume** (mm³) — ``Left-Hippocampus`` in ``aseg.stats`` or ``aseg+DKT.stats``
* **Right hippocampus volume** (mm³) — ``Right-Hippocampus``

Volumes come from whole-brain subcortical segmentation (FreeSurfer ``recon-all`` volume-only
stages, or FastSurfer ``--seg_only``). AutoHS does **not** use FLAIR, diffusion, or
hippocampal subfield segmentation in the default pipeline.

The asymmetry index (AI)
------------------------

The asymmetry index quantifies relative left–right hippocampal volume difference:

.. math::

   \mathrm{AI} = \frac{V_{\mathrm{left}} - V_{\mathrm{right}}}{V_{\mathrm{left}} + V_{\mathrm{right}}}

Properties:

* **AI = 0** — equal volumes (perfect symmetry in this metric)
* **AI > 0** — left hippocampus larger than right
* **AI < 0** — right hippocampus larger than left
* Range is approximately **(−1, +1)** when both volumes are positive

AutoHS reports AI rounded to **four decimal places** in derivative JSON and PDF reports.

Two layers of interpretation
----------------------------

AutoHS applies **two related but distinct** classification layers.

Volume laterality (descriptive)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Uses a symmetric band around zero with threshold **±0.05**:

+---------------------------+----------------------------------+
| Condition                 | Label                            |
+===========================+==================================+
| AI > 0.05                 | Left > Right                     |
+---------------------------+----------------------------------+
| AI < −0.05                | Right > Left                     |
+---------------------------+----------------------------------+
| −0.05 ≤ AI ≤ 0.05         | Symmetric                        |
+---------------------------+----------------------------------+

This layer describes **direction of volume imbalance** without invoking HS pathology.

HS screening (pathology-oriented)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Uses **asymmetric thresholds** derived from the AutoHS validation study (Brain Communications,
in press). These thresholds are stricter on the negative side because hippocampal atrophy
in HS typically makes the **affected side smaller**:

+-------------------------------+----------------------------------------+
| Condition                     | HS screening label                     |
+===============================+========================================+
| AI > 0.046915816971433        | Left-dominant (**Right HS suspected**) |
+-------------------------------+----------------------------------------+
| AI < −0.070839747728063       | Right-dominant (**Left HS suspected**) |
+-------------------------------+----------------------------------------+
| otherwise                     | Balanced (**No HS**)                   |
+-------------------------------+----------------------------------------+

**Naming convention:** “Left HS suspected” means pathology on the **left** hippocampus is
suspected, which manifests as **right-dominant** volumes (smaller left hippocampus, more
negative AI). Similarly, “Right HS suspected” corresponds to **left-dominant** volumes.

These thresholds are **fixed constants** in ``ai_compute/asymmetry.py`` and match the values
written to ``*_desc-autohs_metrics.json``.

End-to-end workflow (theory view)
---------------------------------

.. code-block:: text

   T1w MRI (BIDS)
        │
        ▼
   ┌─────────────────────────────────────┐
   │ Step 1: Whole-brain segmentation    │
   │  FreeSurfer vol-only OR FastSurfer    │
   │  → subcortical volume labels          │
   └─────────────────────────────────────┘
        │
        ▼
   ┌─────────────────────────────────────┐
   │ Step 2: AI-compute                  │
   │  Parse Left/Right Hippocampus mm³   │
   │  AI = (L − R) / (L + R)             │
   │  Laterality + HS screening labels   │
   │  JSON / PDF / summary reports       │
   └─────────────────────────────────────┘
        │
        ▼
   BIDS derivatives under output/autohs/

Step 1 establishes **anatomical correspondence** and voxel-wise labels; Step 2 is purely
**tabular arithmetic and rule-based classification** on hippocampal volumes. No additional
machine-learning model is trained at runtime in Step 2.

Segmentation backends
---------------------

FreeSurfer (default)
~~~~~~~~~~~~~~~~~~~~

Uses ``recon-all -autorecon1 -autorecon2-volonly`` plus ``mri_segstats`` on the automated
segmentation. This is the conventional neuroimaging approach for subcortical volumes and
has extensive literature support.

FastSurfer (``--fastsurfer``)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Uses a deep-learning segmentation pipeline in ``--seg_only`` mode, reading
``aseg+DKT.stats``. It is typically **much faster** on CPU and does not require a FreeSurfer
license, but volumes may differ slightly from FreeSurfer. For research comparability, pick
one backend per study and report it in methods (see :doc:`methods`).

Expected inputs and limitations
-------------------------------

**Inputs**

* One T1w NIfTI per subject/session (BIDS ``*_T1w.nii.gz``)
* FreeSurfer license when using the default backend

**Limitations**

* Single time-point T1w only; no longitudinal atrophy rates
* No FLAIR hyperintensity or hippocampal T2/T1W signal analysis
* Thresholds were validated in the AutoHS publication cohort; external validation on your
  scanner population is recommended before clinical deployment
* Group-level statistics are **not** computed (participant-level BIDS App only)

Scientific reference
--------------------

The asymmetry index formulation and HS screening thresholds implemented in AutoHS are
described in:

   **Ndagijimana P**, **Brennan D**, **Shinohara R**, **Gugger J**. MRI derived hippocampal
   asymmetry identifies hippocampal sclerosis in epilepsy surgical specimens. *Brain
   Communications*. **Accepted (in press)**.

See :doc:`citation` for BibTeX and third-party tool references (FreeSurfer, FastSurfer, BIDS).

Further reading in this documentation
-------------------------------------

* :doc:`preprocessing` — commands, containers, and runtime details for each step
* :doc:`outputs` — derivative filenames and report fields
* :doc:`methods` — copy-paste methods text for manuscripts
* :doc:`sample_data` — public IDEAS example dataset
