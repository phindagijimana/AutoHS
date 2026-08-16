#!/bin/bash
#SBATCH --job-name=autohs-bindtest
#SBATCH --output=logs/slurm-bindtest-%j.out
#SBATCH --error=logs/slurm-bindtest-%j.err
#SBATCH --cpus-per-task=2
#SBATCH --mem=8G
#SBATCH --time=00:15:00
#SBATCH --partition=general

set -euo pipefail
set -x

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"
mkdir -p logs

: "${FREESURFER_SIF:?Set FREESURFER_SIF to your FreeSurfer Apptainer image (.sif)}"
: "${AUTOHS_BINDTEST_INPUT:?Set AUTOHS_BINDTEST_INPUT to a test T1w NIfTI path}"
: "${AUTOHS_BINDTEST_SUBJECT_ID:=bindtest}"

FREESURFER_DIR="$ROOT/work/bindtest/freesurfer"
INPUT_DIR="$(dirname "$AUTOHS_BINDTEST_INPUT")"
LICENSE="${FREESURFER_LICENSE:-$ROOT/license.txt}"
SUBJECT_ID="$AUTOHS_BINDTEST_SUBJECT_ID"
INPUT_NAME="$(basename "$AUTOHS_BINDTEST_INPUT")"

rm -rf "$FREESURFER_DIR/$SUBJECT_ID"
mkdir -p "$FREESURFER_DIR"

apptainer exec \
  --bind "${FREESURFER_DIR}:/subjects" \
  --bind "${INPUT_DIR}:/input:ro" \
  --bind "${LICENSE}:/usr/local/freesurfer/license.txt:ro" \
  --env "FS_LICENSE=/usr/local/freesurfer/license.txt" \
  --env "SUBJECTS_DIR=/subjects" \
  "$FREESURFER_SIF" \
  /bin/bash -c "export FS_FREESURFERENV_NO_OUTPUT=1; source /usr/local/freesurfer/FreeSurferEnv.sh; recon-all -i /input/${INPUT_NAME} -s ${SUBJECT_ID} -autorecon1 -autorecon2-volonly" 2>&1 | head -40

echo "bind test exit=$?"
ls -la "$FREESURFER_DIR/$SUBJECT_ID/scripts/" 2>/dev/null | head -5
