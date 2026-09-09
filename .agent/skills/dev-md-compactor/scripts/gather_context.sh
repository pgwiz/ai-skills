#!/usr/bin/env bash
# gather_context.sh — deterministic repository state extractor
# Part of dev-md-compactor (https://github.com/pgwiz/ai-skills)
#
# Usage: bash gather_context.sh [path-to-project-root] [since-ref]

set -uo pipefail

ROOT="${1:-.}"
SINCE="${2:-}"
cd "$ROOT" || { echo "Cannot cd into $ROOT"; exit 1; }

hr() { printf '\n=== %s ===\n' "$1"; }

hr "PROJECT ROOT"
pwd

# ---------------------------------------------------------------------------
hr "GIT STATUS"
if git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  git status --short --branch
else
  echo "(not a git repository)"
fi

# ---------------------------------------------------------------------------
hr "CURRENT BRANCH"
git branch --show-current 2>/dev/null || echo "(n/a)"

# ---------------------------------------------------------------------------
hr "RECENT COMMITS"
if [ -n "$SINCE" ]; then
  git log --oneline --decorate "${SINCE}..HEAD" 2>/dev/null | head -100
else
  git log --oneline --decorate -20 2>/dev/null
fi

# ---------------------------------------------------------------------------
hr "UNCOMMITTED DIFF (name + stat only, not full patch)"
git diff --stat 2>/dev/null
echo "--- staged ---"
git diff --cached --stat 2>/dev/null

# ---------------------------------------------------------------------------
hr "FILES CHANGED SINCE LAST dev_md_guides UPDATE"
if [ -f "dev_md_guides/changelog.md" ]; then
  LAST_TS=$(git log -1 --format=%ct -- dev_md_guides/changelog.md 2>/dev/null || echo "")
  if [ -n "$LAST_TS" ]; then
    LAST_COMMIT=$(git log -1 --format=%H -- dev_md_guides/changelog.md 2>/dev/null)
    echo "Since commit $LAST_COMMIT:"
    git diff --stat "${LAST_COMMIT}..HEAD" 2>/dev/null
  fi
else
  echo "(no existing changelog.md found — first run)"
fi

# ---------------------------------------------------------------------------
hr "DIRECTORY TREE (pruned)"
if command -v tree >/dev/null 2>&1; then
  tree -L 3 -I 'node_modules|.git|dist|build|__pycache__|*.pyc|.venv|venv|target|.next|coverage|.turbo|vendor|dev_md_guides' --dirsfirst
else
  find . \
    -path './node_modules' -prune -o \
    -path './.git' -prune -o \
    -path './dist' -prune -o \
    -path './build' -prune -o \
    -path './__pycache__' -prune -o \
    -path './.venv' -prune -o \
    -path './venv' -prune -o \
    -path './target' -prune -o \
    -path './.next' -prune -o \
    -path './dev_md_guides' -prune -o \
    -path './vendor' -prune -o \
    -maxdepth 3 -print 2>/dev/null | sed 's|[^/]*/|  |g'
fi

# ---------------------------------------------------------------------------
hr "PROJECT MANIFESTS"
for f in package.json pyproject.toml requirements.txt go.mod Cargo.toml \
         Gemfile composer.json pom.xml build.gradle CMakeLists.txt; do
  if [ -f "$f" ]; then
    echo "--- $f ---"
    cat "$f"
    echo
  fi
done

# ---------------------------------------------------------------------------
hr "EXISTING dev_md_guides/ FILE SIZES (if present)"
if [ -d "dev_md_guides" ]; then
  wc -l dev_md_guides/*.md 2>/dev/null
else
  echo "(dev_md_guides/ does not exist yet — will be created)"
fi

hr "DONE"
