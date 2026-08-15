#!/bin/bash
#SBATCH --job-name=autohs
#SBATCH --output=logs/slurm-%x-%j.out
#SBATCH --error=logs/slurm-%x-%j.err
#SBATCH --cpus-per-task=8
#SBATCH --mem=64G
#SBATCH --time=24:00:00
#SBATCH --partition=general
#SBATCH --chdir=/mnt/nfs/home/urmc-sh.rochester.edu/pndagiji/Documents/AutoHS

set -euo pipefail

ROOT="/mnt/nfs/home/urmc-sh.rochester.edu/pndagiji/Documents/AutoHS"
cd "$ROOT"
mkdir -p logs

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
  echo "Usage: sbatch scripts/sbatch_run_job.sh <job_id> [--fastsurfer]" >&2
  exit 1
fi

echo "=== AutoHS Slurm job ==="
echo "Job ID:   ${JOB_ID}"
echo "Backend:  $([[ $FASTSURFER -eq 1 ]] && echo FastSurfer || echo FreeSurfer)"
echo "Host:     $(hostname)"
echo "Start:    $(date)"
echo "Root:     ${ROOT}"
echo "========================"

args=("$JOB_ID")
if [[ "$FASTSURFER" -eq 1 ]]; then
  args+=("--fastsurfer")
fi

exec bash "$ROOT/scripts/run_job_apptainer.sh" "${args[@]}"
