#!/bin/bash
#SBATCH --job-name=autohs-bindtest
#SBATCH --output=logs/slurm-bindtest-%j.out
#SBATCH --error=logs/slurm-bindtest-%j.err
#SBATCH --cpus-per-task=2
#SBATCH --mem=8G
#SBATCH --time=00:15:00
#SBATCH --partition=general
#SBATCH --chdir=/mnt/nfs/home/urmc-sh.rochester.edu/pndagiji/Documents/AutoHS

set -euo pipefail
set -x

ROOT=/mnt/nfs/home/urmc-sh.rochester.edu/pndagiji/Documents/AutoHS
JOB_ID=85f5179e
FREESURFER_DIR=$ROOT/data/jobs/$JOB_ID/freesurfer
INPUT_DIR=$ROOT/data/jobs/$JOB_ID/input
LICENSE=$ROOT/license.txt
SIF=/mnt/nfs/home/urmc-sh.rochester.edu/pndagiji/Documents/others/containers/freesurfer_7.4.1.sif
SUBJECT_ID=job_${JOB_ID}

rm -rf "$FREESURFER_DIR/$SUBJECT_ID"
mkdir -p "$FREESURFER_DIR"

apptainer exec \
  --bind "${FREESURFER_DIR}:/subjects" \
  --bind "${INPUT_DIR}:/input:ro" \
  --bind "${LICENSE}:/usr/local/freesurfer/license.txt:ro" \
  --env "FS_LICENSE=/usr/local/freesurfer/license.txt" \
  --env "SUBJECTS_DIR=/subjects" \
  "$SIF" \
  /bin/bash -c 'export FS_FREESURFERENV_NO_OUTPUT=1; source /usr/local/freesurfer/FreeSurferEnv.sh; recon-all -i /input/sub-001_ses-1_T1w.nii.gz -s job_85f5179e -autorecon1 -autorecon2-volonly' 2>&1 | head -40

echo "bind test exit=$?"
ls -la "$FREESURFER_DIR/$SUBJECT_ID/scripts/" 2>/dev/null | head -5
