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
  tree -L 3 -I 'node_modules|.git|dist|build|__pycache__|*.pyc|.venv|venv|target|.next|coverage|.turbo|vendor|dev_md_guides' --dirsfirst 2>/dev/null
elif find --version >/dev/null 2>&1; then
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
else
  git ls-files 2>/dev/null | head -50
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
if [ -f "dev_com_agent.md" ]; then
  echo "--- dev_com_agent.md (root universal router detected: $(wc -l < dev_com_agent.md) lines) ---"
fi
if [ -d "dev_md_guides" ]; then
  wc -l dev_md_guides/*.md dev_md_guides/*.md.sample 2>/dev/null
  if [ -f "dev_md_guides/agent.md" ]; then
    echo "--- agent.md (master index detected) ---"
  fi
  if [ -f "dev_md_guides/gotchas.md" ]; then
    echo "--- gotchas.md (failure mode bank detected) ---"
  fi
  if [ -f "dev_md_guides/flow.md" ]; then
    echo "--- flow.md (procedural recipes detected) ---"
  fi
  if [ -f "dev_md_guides/directory.md" ]; then
    echo "--- directory.md (local active catalog detected) ---"
  elif [ -f "dev_md_guides/directory.md.sample" ]; then
    echo "--- directory.md.sample (template sample detected) ---"
  fi
  if [ -f "dev_md_guides/credentials.md" ]; then
    echo "--- credentials.md (local active credentials detected) ---"
  elif [ -f "dev_md_guides/credentials.md.sample" ]; then
    echo "--- credentials.md.sample (template sample detected) ---"
  fi
  # Detect and report dynamic topic guides
  for df in dev_md_guides/*.md; do
    [ -f "$df" ] || continue
    base=$(basename "$df")
    case "$base" in
      agent.md|branch.md|structure.md|changelog.md|features.md|memory.md|gotchas.md|flow.md|directory.md|credentials.md)
        ;;
      *)
        echo "--- $base (dynamic topic guide detected: $(wc -l < "$df") lines) ---"
        ;;
    esac
  done
else
  echo "(dev_md_guides/ does not exist yet — will be created)"
fi

# ---------------------------------------------------------------------------
hr "AGENT MASTER INDEX (dev_md_guides/agent.md)"
if [ -f "dev_md_guides/agent.md" ]; then
  cat "dev_md_guides/agent.md"
elif [ -f "dev_com_agent.md" ]; then
  echo "(agent.md not found, displaying dev_com_agent.md root router)"
  cat "dev_com_agent.md"
else
  echo "(no agent master index found)"
fi

# ---------------------------------------------------------------------------
hr "DYNAMIC TOPIC GUIDES (if present)"
DYNAMIC_FOUND=0
if [ -d "dev_md_guides" ]; then
  for df in dev_md_guides/*.md; do
    [ -f "$df" ] || continue
    base=$(basename "$df")
    case "$base" in
      agent.md|branch.md|structure.md|changelog.md|features.md|memory.md|gotchas.md|flow.md|directory.md|credentials.md)
        ;;
      *)
        DYNAMIC_FOUND=1
        echo "=== $base ==="
        cat "$df"
        echo
        ;;
    esac
  done
fi
if [ "$DYNAMIC_FOUND" -eq 0 ]; then
  echo "(no dynamic topic guides present)"
fi

# ---------------------------------------------------------------------------
hr "DIRECTORY & ENDPOINT CATALOG (dev_md_guides/directory.md)"
if [ -f "dev_md_guides/directory.md" ]; then
  cat "dev_md_guides/directory.md"
elif [ -f "dev_md_guides/directory.md.sample" ]; then
  echo "(directory.md not found, displaying directory.md.sample)"
  cat "dev_md_guides/directory.md.sample"
else
  echo "(no directory catalog found in dev_md_guides/)"
fi

# ---------------------------------------------------------------------------
hr "CREDENTIALS & SECRETS SCHEMA (dev_md_guides/credentials.md.sample)"
if [ -f "dev_md_guides/credentials.md" ]; then
  echo "(local credentials.md detected — keeping live secret values redacted from stdout)"
fi
if [ -f "dev_md_guides/credentials.md.sample" ]; then
  cat "dev_md_guides/credentials.md.sample"
elif [ -f "dev_md_guides/credentials.md" ]; then
  echo "(credentials.md exists locally but no credentials.md.sample found)"
else
  echo "(no credentials catalog found in dev_md_guides/)"
fi

# ---------------------------------------------------------------------------
hr "CREDENTIAL TRACKING & SECURITY CHECK"
if git ls-files --error-unmatch dev_md_guides/credentials.md >/dev/null 2>&1; then
  echo "CRITICAL SECURITY WARNING: dev_md_guides/credentials.md is tracked in git index/history!"
  echo "Immediately run: git rm --cached dev_md_guides/credentials.md"
elif git diff --cached --name-only 2>/dev/null | grep -E '(^|/)credentials\.md$' >/dev/null 2>&1; then
  echo "CRITICAL SECURITY WARNING: credentials.md is staged in git index!"
  echo "Immediately run: git reset HEAD dev_md_guides/credentials.md"
elif git status --porcelain dev_md_guides/credentials.md 2>/dev/null | grep -q '??'; then
  echo "SECURITY WARNING: dev_md_guides/credentials.md is untracked and NOT ignored by .gitignore!"
  echo "Ensure dev_md_guides/credentials.md is added to .gitignore immediately."
else
  echo "OK: dev_md_guides/credentials.md is safely gitignored and not tracked in git worktree."
fi

hr "DONE"
