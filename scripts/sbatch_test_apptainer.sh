#!/bin/bash
#SBATCH --job-name=autohs-test
#SBATCH --output=logs/slurm-test-%j.out
#SBATCH --error=logs/slurm-test-%j.err
#SBATCH --cpus-per-task=2
#SBATCH --mem=8G
#SBATCH --time=00:10:00
#SBATCH --partition=general
#SBATCH --chdir=/mnt/nfs/home/urmc-sh.rochester.edu/pndagiji/Documents/AutoHS

set -x
which apptainer podman singularity
SIF=/mnt/nfs/home/urmc-sh.rochester.edu/pndagiji/Documents/others/containers/freesurfer_7.4.1.sif
ls -la "$SIF"
apptainer exec "$SIF" /bin/bash -c 'export FS_FREESURFERENV_NO_OUTPUT=1; source /usr/local/freesurfer/FreeSurferEnv.sh; recon-all -version'
