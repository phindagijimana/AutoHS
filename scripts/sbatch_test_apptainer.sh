#!/bin/bash
#SBATCH --job-name=autohs-test
#SBATCH --output=logs/slurm-test-%j.out
#SBATCH --error=logs/slurm-test-%j.err
#SBATCH --cpus-per-task=2
#SBATCH --mem=8G
#SBATCH --time=00:10:00
#SBATCH --partition=general

set -euo pipefail
set -x

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"
mkdir -p logs

: "${FREESURFER_SIF:?Set FREESURFER_SIF to your FreeSurfer Apptainer image (.sif)}"

which apptainer podman singularity
ls -la "$FREESURFER_SIF"
apptainer exec "$FREESURFER_SIF" /bin/bash -c 'export FS_FREESURFERENV_NO_OUTPUT=1; source /usr/local/freesurfer/FreeSurferEnv.sh; recon-all -version'
