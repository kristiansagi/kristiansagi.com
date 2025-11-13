#!/bin/bash
# sync-main-from-staging.sh
# Make 'main' match 'staging' content while preserving 'main' history.
# Creates a merge commit (two parents) with the tree from 'staging'.
# No history rewrite; no force push.

set -euo pipefail

echo "---------------------------------------------"
echo " Sync 'main' with 'staging' (preserve history)"
echo "---------------------------------------------"

# Ensure we're in a git repository
if [ ! -d ".git" ]; then
  echo "❌ Not a git repository."
  exit 1
fi

# Ensure required branches exist
if ! git show-ref --verify --quiet refs/heads/staging; then
  echo "❌ Branch 'staging' does not exist."
  exit 1
fi
if ! git show-ref --verify --quiet refs/heads/main; then
  echo "❌ Branch 'main' does not exist."
  exit 1
fi

# Save current branch
CURRENT_BRANCH="$(git rev-parse --abbrev-ref HEAD)"

# Ensure clean working tree
if [ -n "$(git status --porcelain)" ]; then
  echo "⚠️  Uncommitted changes on ${CURRENT_BRANCH}."
  echo "Creating a safety commit..."
  git add -A
  git commit -m "Auto-commit: save work before syncing main with staging"
fi

# Optionally update remotes (comment out if undesired)
if git remote get-url origin >/dev/null 2>&1; then
  echo "→ Fetching latest from origin..."
  git fetch --all --prune
fi

# Switch to main
echo "→ Checking out 'main'..."
git checkout main

# Optional: pull latest main to avoid diverging from remote
if git ls-remote --exit-code --heads origin main >/dev/null 2>&1; then
  echo "→ Pulling latest 'main'..."
  git pull --ff-only || {
    echo "⚠️  'main' cannot fast-forward; continuing locally. You may need to push with merge."
  }
fi

# Create a rollback tag (safety net)
TAG="backup/main-before-sync-$(date +%Y%m%d-%H%M%S)"
echo "→ Tagging current main for rollback: ${TAG}"
git tag -a "${TAG}" -m "Backup before syncing main with staging"

# Prepare a merge that preserves main history but will use staging's tree
echo "→ Preparing merge commit (strategy ours, no commit)..."
git merge -s ours --no-commit staging

# Replace index & working tree with EXACT tree from staging
echo "→ Replacing content with staging tree..."
git read-tree --reset -u staging

# Compose commit message
STAGING_SHA="$(git rev-parse --short staging)"
DATE="$(date +%Y-%m-%d)"
MSG="Sync main with staging (snapshot ${DATE}, staging ${STAGING_SHA})"

# Commit the merge (now with staging content)
echo "→ Committing merge: ${MSG}"
git commit -m "${MSG}"

# Push main (no force)
echo "→ Pushing 'main' to origin..."
git push origin main

# Return to previous branch (staging)
echo "→ Returning to '${CURRENT_BRANCH}'..."
git checkout "${CURRENT_BRANCH}"

echo
echo "✅ Done. 'main' now matches 'staging' while preserving 'main' history."
echo "   Rollback tag: ${TAG}"
