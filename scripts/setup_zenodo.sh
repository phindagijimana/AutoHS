#!/usr/bin/env bash
# Zenodo DOI setup helper for AutoHS.
#
# Steps (one-time, in browser):
#   1. https://zenodo.org/account/settings/github/
#   2. Enable GitHub integration and toggle ON for phindagijimana/AutoHS
#   3. Create or refresh GitHub release v0.1.8 (archive is created automatically)
#   4. Copy the new Zenodo DOI into CITATION.cff identifiers section
#
# This script checks whether a Zenodo badge/DOI exists on the latest release.

set -euo pipefail

REPO="${1:-phindagijimana/AutoHS}"
TAG="${2:-v0.1.8}"

echo "Zenodo setup checklist for $REPO $TAG"
echo "========================================"
echo
echo "1. Open: https://zenodo.org/account/settings/github/"
echo "2. Connect GitHub and enable repository: AutoHS"
echo "3. Ensure release exists: https://github.com/$REPO/releases/tag/$TAG"
echo "4. After Zenodo archives the release, add DOI to CITATION.cff:"
echo "     identifiers:"
echo "       - type: doi"
echo "         value: 10.5281/zenodo.XXXXXXX"
echo

if command -v gh >/dev/null 2>&1; then
  echo "Release notes:"
  gh release view "$TAG" --repo "$REPO" --json url,isDraft 2>/dev/null || echo "  (release not found)"
fi
