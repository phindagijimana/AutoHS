#!/usr/bin/env bash
# Maintainer checklist for Read the Docs, Docker Hub, and Zenodo.
set -euo pipefail

echo "AutoHS ecosystem setup checklist"
echo "================================"
echo

echo "1) Read the Docs (documentation currently 404 until imported)"
echo "   Open: https://readthedocs.org/dashboard/import/manual/?url=https://github.com/phindagijimana/AutoHS"
echo "   - Project slug: autohs"
echo "   - Config file: .readthedocs.yaml (already in repo)"
echo "   - Enable builds on tag pushes after first import"
echo

echo "2) Docker Hub (image push skipped in CI without secrets)"
echo "   Run: DOCKERHUB_USERNAME=... DOCKERHUB_TOKEN=... ./scripts/setup_dockerhub.sh"
echo "   Or manually:"
echo "   - Create repository: https://hub.docker.com/repository/create?name=autohs"
echo "   - Add GitHub secrets on phindagijimana/AutoHS:"
echo "       DOCKERHUB_USERNAME"
echo "       DOCKERHUB_TOKEN"
echo "   - Re-run workflow: Publish Docker Image (workflow_dispatch)"
echo

echo "3) Zenodo DOI (add to CITATION.cff after first archive)"
echo "   Run: ./scripts/setup_zenodo.sh"
echo "   Or: https://zenodo.org/account/settings/github/ → enable AutoHS"
echo

echo "4) BIDS Apps hub"
echo "   - PR: https://github.com/bids-standard/bids-website/pull/905"
echo

if command -v gh >/dev/null 2>&1; then
  echo "GitHub CLI secrets currently configured:"
  gh secret list -R phindagijimana/AutoHS 2>/dev/null || true
fi
