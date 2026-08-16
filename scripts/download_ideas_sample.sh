#!/usr/bin/env bash
# Download two IDEAS (OpenNeuro ds005602) subjects for AutoHS examples and tests.
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
OUT="${1:-$ROOT/sample_data/ideas_bids}"
BASE="https://s3.amazonaws.com/openneuro.org/ds005602"

mkdir -p "$OUT/sub-1/anat" "$OUT/sub-2/anat"

echo "Downloading IDEAS sample BIDS data to $OUT"

curl -fsSL "$BASE/dataset_description.json" -o "$OUT/dataset_description.json"
curl -fsSL "$BASE/README" -o "$OUT/README"

for sub in 1 2; do
  curl -fsSL "$BASE/sub-${sub}/anat/sub-${sub}_T1w.nii.gz" \
    -o "$OUT/sub-${sub}/anat/sub-${sub}_T1w.nii.gz"
  curl -fsSL "$BASE/sub-${sub}/anat/sub-${sub}_T1w.json" \
    -o "$OUT/sub-${sub}/anat/sub-${sub}_T1w.json"
done

echo "Done. Subjects: sub-1, sub-2 (IDEAS / OpenNeuro ds005602)."
echo "See sample_data/ideas_bids/README.md for required citations."
