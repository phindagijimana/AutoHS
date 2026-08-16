#!/usr/bin/env bash
# Configure Docker Hub publishing for AutoHS GitHub Actions.
#
# Usage:
#   DOCKERHUB_USERNAME=youruser DOCKERHUB_TOKEN=yourtoken ./scripts/setup_dockerhub.sh
#
# Create a Docker Hub access token at:
#   https://hub.docker.com/settings/security
# Create the repository (if needed):
#   https://hub.docker.com/repository/create?name=autohs

set -euo pipefail

REPO="${GITHUB_REPOSITORY:-phindagijimana/AutoHS}"
USER="${DOCKERHUB_USERNAME:-}"
TOKEN="${DOCKERHUB_TOKEN:-}"

if [[ -z "$USER" || -z "$TOKEN" ]]; then
  echo "Set DOCKERHUB_USERNAME and DOCKERHUB_TOKEN environment variables." >&2
  echo "Example:" >&2
  echo "  DOCKERHUB_USERNAME=autohs DOCKERHUB_TOKEN=dckr_pat_... ./scripts/setup_dockerhub.sh" >&2
  exit 1
fi

if ! command -v gh >/dev/null 2>&1; then
  echo "GitHub CLI (gh) is required." >&2
  exit 1
fi

echo "Setting GitHub secrets on $REPO ..."
gh secret set DOCKERHUB_USERNAME --repo "$REPO" --body "$USER"
gh secret set DOCKERHUB_TOKEN --repo "$REPO" --body "$TOKEN"

echo "Triggering Publish Docker Image workflow for tag 0.1.9 ..."
gh workflow run "Publish Docker Image" --repo "$REPO" -f tag=0.1.9

echo "Done. Watch: https://github.com/$REPO/actions/workflows/docker-publish.yml"
echo "After success: docker pull autohs/autohs:0.1.9"
