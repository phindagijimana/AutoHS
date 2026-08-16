#!/usr/bin/env bash
# Run one AutoHS job using Apptainer (FreeSurfer or FastSurfer) + native Python (AI-compute).
# Used on HPC nodes where Docker is unavailable.

set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
JOB_ID=""
FASTSURFER=0

while [[ $# -gt 0 ]]; do
  case "$1" in
    --fastsurfer)
      FASTSURFER=1
      shift
      ;;
    *)
      if [[ -z "$JOB_ID" ]]; then
        JOB_ID="$1"
        shift
      else
        echo "ERROR: Unexpected argument: $1" >&2
        exit 1
      fi
      ;;
  esac
done

if [[ -z "$JOB_ID" ]]; then
  echo "Usage: run_job_apptainer.sh <job_id> [--fastsurfer]" >&2
  exit 1
fi

WORK_DIR="$ROOT/data/jobs/$JOB_ID"
INPUT_DIR="$WORK_DIR/input"
FREESURFER_DIR="$WORK_DIR/freesurfer"
OUTPUT_DIR="$WORK_DIR/output"
SUBJECT_ID="job_${JOB_ID}"
LICENSE="$ROOT/license.txt"
FREESURFER_SIF="${FREESURFER_SIF:-}"
FASTSURFER_SIF="${FASTSURFER_SIF:-}"

INPUT_FILE="$(find "$INPUT_DIR" -maxdepth 1 \( -name '*.nii' -o -name '*.nii.gz' \) | head -1)"
if [[ -z "$INPUT_FILE" ]]; then
  echo "ERROR: No NIfTI found in $INPUT_DIR" >&2
  exit 1
fi

mkdir -p "$FREESURFER_DIR" "$OUTPUT_DIR"
SUBJECT_DIR="$FREESURFER_DIR/$SUBJECT_ID"
if [[ -d "$SUBJECT_DIR" ]]; then
  rm -rf "$SUBJECT_DIR"
fi

PY="$ROOT/venv/bin/python"
export PYTHONPATH="$ROOT${PYTHONPATH:+:$PYTHONPATH}"
NUM_THREADS="${AUTOHS_THREADS:-$(( $(nproc 2>/dev/null || echo 4) - 2 ))}"
if [[ "$NUM_THREADS" -lt 1 ]]; then
  NUM_THREADS=1
fi

if [[ "$FASTSURFER" -eq 1 ]]; then
  if [[ -z "$FASTSURFER_SIF" || ! -f "$FASTSURFER_SIF" ]]; then
    echo "ERROR: Set FASTSURFER_SIF to your FastSurfer Apptainer image (.sif)" >&2
    exit 1
  fi
  SEG_STEP="fastsurfer-processing"
  SEG_LABEL="FastSurfer"
else
  if [[ -z "$FREESURFER_SIF" || ! -f "$FREESURFER_SIF" ]]; then
    echo "ERROR: Set FREESURFER_SIF to your FreeSurfer Apptainer image (.sif)" >&2
    exit 1
  fi
  SEG_STEP="freesurfer-processing"
  SEG_LABEL="FreeSurfer"
fi

echo "[$(date)] Starting ${SEG_LABEL} (Apptainer) for job $JOB_ID"
"$PY" - <<PY
from pathlib import Path
from datetime import datetime, timezone
from workflow.runner import WorkflowRunner
runner = WorkflowRunner(Path("$ROOT"))
runner.queue.update_job(
    "$JOB_ID",
    status="running",
    step="$SEG_STEP",
    progress=5,
    started_at=datetime.now(timezone.utc).isoformat(),
)
PY

if [[ "$FASTSURFER" -eq 1 ]]; then
  apptainer exec \
    --bind "${INPUT_DIR}:/input:ro" \
    --bind "${FREESURFER_DIR}:/output" \
    --env "TQDM_DISABLE=1" \
    --cleanenv \
    "$FASTSURFER_SIF" \
    /fastsurfer/run_fastsurfer.sh \
    --t1 "/input/$(basename "$INPUT_FILE")" \
    --sid "$SUBJECT_ID" \
    --sd /output \
    --seg_only \
    --device cpu \
    --batch 1 \
    --threads "$NUM_THREADS" \
    --viewagg_device cpu
else
  apptainer exec \
    --bind "${FREESURFER_DIR}:/subjects" \
    --bind "${INPUT_DIR}:/input:ro" \
    --bind "${LICENSE}:/usr/local/freesurfer/license.txt:ro" \
    --env "FS_LICENSE=/usr/local/freesurfer/license.txt" \
    --env "SUBJECTS_DIR=/subjects" \
    "$FREESURFER_SIF" \
    /bin/bash -c "export FS_FREESURFERENV_NO_OUTPUT=1; source /usr/local/freesurfer/FreeSurferEnv.sh; recon-all -i /input/$(basename "$INPUT_FILE") -s ${SUBJECT_ID} -autorecon1 -autorecon2-volonly; mri_segstats --seg /subjects/${SUBJECT_ID}/mri/aseg.auto.mgz --excludeid 0 --sum /subjects/${SUBJECT_ID}/stats/aseg.stats --i /subjects/${SUBJECT_ID}/mri/brain.mgz"
fi

echo "[$(date)] ${SEG_LABEL} complete — starting AI-compute"
"$PY" - <<PY
from pathlib import Path
from workflow.runner import WorkflowRunner
runner = WorkflowRunner(Path("$ROOT"))
runner.queue.update_job("$JOB_ID", step="ai-compute", progress=60)
PY

"$PY" -m ai_compute.main \
  --job-id "$JOB_ID" \
  --input "$INPUT_FILE" \
  --freesurfer "$FREESURFER_DIR" \
  --output "$OUTPUT_DIR" \
  --subject-id "$SUBJECT_ID"

"$PY" - <<PY
from pathlib import Path
from datetime import datetime, timezone
from workflow.runner import WorkflowRunner
runner = WorkflowRunner(Path("$ROOT"))
runner.queue.update_job(
    "$JOB_ID",
    status="completed",
    step="done",
    progress=100,
    result_path=str(Path("$OUTPUT_DIR")),
    completed_at=datetime.now(timezone.utc).isoformat(),
)
PY

echo "[$(date)] Job $JOB_ID completed"
echo "  report: $OUTPUT_DIR/report.json"
echo "  pdf:    $OUTPUT_DIR/report.pdf"
