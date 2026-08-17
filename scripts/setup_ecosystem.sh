#!/usr/bin/env bash
# Maintainer checklist for Docker Hub and Zenodo.
set -euo pipefail

echo "AutoHS ecosystem setup checklist"
echo "================================"
echo

echo "1) Read the Docs — live at https://autohs.readthedocs.io/en/latest/"
echo "   Config: .readthedocs.yaml"
echo

echo "2) Docker Hub (image push skipped in CI without secrets)"
echo "   Run: DOCKERHUB_USERNAME=... DOCKERHUB_TOKEN=... ./scripts/setup_dockerhub.sh"
echo "   Or:"
echo "   - Create repository: https://hub.docker.com/repository/create?name=autohs"
echo "   - Add GitHub secrets: DOCKERHUB_USERNAME, DOCKERHUB_TOKEN"
echo "   - Push a semver tag or re-run: Publish Docker Image (workflow_dispatch)"
echo

echo "3) Zenodo DOI"
echo "   - Enable: https://zenodo.org/account/settings/github/ → AutoHS"
echo "   - Publish a semver GitHub release → Zenodo archives automatically"
echo "   - Add concept DOI to CITATION.cff identifiers (see ./scripts/setup_zenodo.sh)"
echo

echo "4) BIDS Apps hub (optional — deferred)"
echo "   - Template: registry/bids-website-apps.yml"
echo "   - Open PR to bids-standard/bids-website when ready"
echo

if command -v gh >/dev/null 2>&1; then
  echo "GitHub CLI secrets currently configured:"
  gh secret list -R phindagijimana/AutoHS 2>/dev/null || true
fi
