# AGENT CONTROL SKILL — GLOBAL INSTALL IMPLEMENTATION PLAN v2
# Cross-platform. Web-installable. Self-configuring.
# Repo: https://github.com/pgwiz/ai-skills

---

## OVERVIEW

This plan upgrades the skill to be:
- **Cross-platform** — Windows (PowerShell), macOS/Linux (bash)
- **Web-installable** — one `gh skills install` command or a curl pipe
- **Self-configuring** — agent scans the environment, writes `README.env`, then pushes
- **Standard-compliant** — follows the Agent Skills open standard (agentskills.io)
  compatible with GitHub Copilot, Claude Code, and any `.agents/skills`-aware runtime

---

## TARGET REPO STRUCTURE

```
pgwiz/ai-skills (GitHub)
  README.md                         ← repo landing page + install instructions
  agent-memory/                     ← the skill (name used by gh skills install)
    SKILL.md                        ← skill entrypoint, user-agnostic
    references/
      GLOBAL_PROTOCOL.md            ← loaded on demand by skill
      GLOBAL_WARNINGS.md
      CONVENTIONS.md
      AGENT_BOOTSTRAP.md
      SESSION_START.md
  install/
    install.ps1                     ← Windows installer
    install.sh                      ← macOS/Linux installer
    INSTALL.md                      ← human-readable install guide
```

**Why `references/` folder?**
The Agent Skills spec supports progressive loading — `SKILL.md` stays lean,
and the agent reads reference files only when needed. This saves tokens.

---

## SKILL INSTALL PATHS (per platform)

The installer copies the skill to the correct personal skills directory:

| Platform | Path |
|----------|------|
| Windows | `%USERPROFILE%\.copilot\skills\agent-memory\` |
| Windows (alt) | `%USERPROFILE%\.agents\skills\agent-memory\` |
| macOS/Linux | `~/.copilot/skills/agent-memory/` |
| macOS/Linux (alt) | `~/.agents/skills/agent-memory/` |
| Any project (local) | `.github/skills/agent-memory/` or `.claude/skills/agent-memory/` |

The installer tries the primary path first, falls back to alt if primary doesn't exist.
Both `.copilot/skills` and `.agents/skills` work — Copilot and Claude Code read both.

---

## WEB INSTALL METHODS

### Method 1 — GitHub CLI (recommended, one command)
```bash
gh skills install pgwiz/ai-skills agent-memory
```

### Method 2 — curl pipe (macOS/Linux, no GitHub CLI needed)
```bash
curl -fsSL https://raw.githubusercontent.com/pgwiz/ai-skills/main/install/install.sh | bash
```

### Method 3 — PowerShell (Windows, no GitHub CLI needed)
```powershell
irm https://raw.githubusercontent.com/pgwiz/ai-skills/main/install/install.ps1 | iex
```

### Method 4 — Manual clone
```bash
git clone https://github.com/pgwiz/ai-skills.git
cd ai-skills/install
./install.sh        # or install.ps1 on Windows
```

All four methods produce the same result.

---

## PHASE 1 — REWRITE ALL FILES TO BE USER-AGNOSTIC

### 1.1 — Remove all hardcoded references

Scan every file and replace:

| Find | Replace with |
|------|-------------|
| `E:\Backup\pgwiz\agent-system` | `{AGENT_SYSTEM_PATH}` |
| `pgwiz` (as Windows username/path) | `{AGENT_USER}` |
| `E:\Backup\pgwiz\aliases\` | `{AGENT_HOME}\aliases` |
| `Nairobi, Kenya` (location) | remove — not relevant globally |

**Keep as-is (do NOT replace):**
- `pgwiz (Juju)` — author attribution in README only
- `$env:USERPROFILE` — already a Windows dynamic variable
- `$env:USERNAME` — already dynamic
- `$HOME` / `~` — already dynamic on Unix

### 1.2 — SKILL.md identity section

Replace the pgwiz-specific identity paragraph with:

```md
## DEVELOPER IDENTITY
Read `references/GLOBAL_PROTOCOL.md` for the full developer profile,
stack preferences, git identity rules, and communication style.
The installer writes these details to `{AGENT_SYSTEM_PATH}/GLOBAL_PROTOCOL.md`
based on the user's environment at install time.
```

### 1.3 — Path resolution in SKILL.md

The skill must resolve `{AGENT_SYSTEM_PATH}` at runtime. Add this to SKILL.md:

```md
## PATH RESOLUTION
At session start, read `~/.copilot/skills/agent-memory/.agent-config`
(or `%USERPROFILE%\.copilot\skills\agent-memory\.agent-config` on Windows).
This file is written by the installer and contains:
  AGENT_SYSTEM_PATH=...
  AGENT_USER=...
  AGENT_HOME=...
Use these values wherever you see {AGENT_SYSTEM_PATH} in this skill.
```

---

## PHASE 2 — CREATE install.sh (macOS / Linux)

```bash
#!/usr/bin/env bash
# install.sh — Agent Memory Skill installer
# Source: https://github.com/pgwiz/ai-skills
# Works on: macOS, Linux, WSL

set -e

# ── Detect environment ───────────────────────────────────────────────────────
AGENT_USER="$(whoami)"
AGENT_HOME="$HOME"
AGENT_SYSTEM_PATH="$HOME/agent-system"

# Skill install location — try .copilot/skills first, fall back to .agents/skills
if [ -d "$HOME/.copilot" ]; then
    SKILL_PATH="$HOME/.copilot/skills/agent-memory"
elif [ -d "$HOME/.agents" ]; then
    SKILL_PATH="$HOME/.agents/skills/agent-memory"
else
    mkdir -p "$HOME/.copilot/skills"
    SKILL_PATH="$HOME/.copilot/skills/agent-memory"
fi

echo ""
echo "=== Agent Memory Skill Installer ==="
echo "User      : $AGENT_USER"
echo "Home      : $AGENT_HOME"
echo "System    : $AGENT_SYSTEM_PATH"
echo "Skill dir : $SKILL_PATH"
echo ""
read -p "Proceed? (y/n): " confirm
[ "$confirm" != "y" ] && echo "Aborted." && exit 0

# ── Locate source files ──────────────────────────────────────────────────────
# Support both: run from repo root OR curl pipe (downloads to tmp)
if [ -f "./agent-memory/SKILL.md" ]; then
    SOURCE_ROOT="."
elif [ -f "/tmp/ai-skills/agent-memory/SKILL.md" ]; then
    SOURCE_ROOT="/tmp/ai-skills"
else
    echo "Downloading from GitHub..."
    git clone --depth=1 https://github.com/pgwiz/ai-skills.git /tmp/ai-skills 2>/dev/null
    SOURCE_ROOT="/tmp/ai-skills"
fi

# ── Helper: patch placeholders in a file ────────────────────────────────────
patch_file() {
    local file="$1"
    sed -i.bak \
        -e "s|{AGENT_SYSTEM_PATH}|$AGENT_SYSTEM_PATH|g" \
        -e "s|{AGENT_USER}|$AGENT_USER|g" \
        -e "s|{AGENT_HOME}|$AGENT_HOME|g" \
        "$file" && rm -f "${file}.bak"
}

# ── Install global memory files ──────────────────────────────────────────────
echo "Installing global memory files..."
mkdir -p "$AGENT_SYSTEM_PATH"

for f in GLOBAL_PROTOCOL.md GLOBAL_WARNINGS.md CONVENTIONS.md \
          AGENT_BOOTSTRAP.md SESSION_START.md README.md; do
    src="$SOURCE_ROOT/agent-memory/references/$f"
    dest="$AGENT_SYSTEM_PATH/$f"
    if [ -f "$src" ]; then
        cp "$src" "$dest"
        patch_file "$dest"
        echo "  ✓ $f"
    fi
done

# ── Install skill ────────────────────────────────────────────────────────────
echo "Installing skill..."
mkdir -p "$SKILL_PATH/references"

cp "$SOURCE_ROOT/agent-memory/SKILL.md" "$SKILL_PATH/SKILL.md"
patch_file "$SKILL_PATH/SKILL.md"

for f in "$SOURCE_ROOT/agent-memory/references/"*.md; do
    cp "$f" "$SKILL_PATH/references/"
    patch_file "$SKILL_PATH/references/$(basename $f)"
done

# ── Write .agent-config ──────────────────────────────────────────────────────
CONFIG_CONTENT="AGENT_SYSTEM_PATH=$AGENT_SYSTEM_PATH
AGENT_USER=$AGENT_USER
AGENT_HOME=$AGENT_HOME
INSTALLED_ON=$(date '+%Y-%m-%d %H:%M')
PLATFORM=$(uname -s)"

echo "$CONFIG_CONTENT" > "$AGENT_SYSTEM_PATH/.agent-config"
echo "$CONFIG_CONTENT" > "$SKILL_PATH/.agent-config"

# ── Done ─────────────────────────────────────────────────────────────────────
echo ""
echo "✓ Install complete!"
echo ""
echo "Global files : $AGENT_SYSTEM_PATH/"
echo "Skill        : $SKILL_PATH/"
echo ""
echo "NEXT STEPS:"
echo "  1. Open any project root"
echo "  2. Tell the agent: Bootstrap .agent/ for this project"
echo "  3. From now on, just type your task"
echo ""
```

---

## PHASE 3 — CREATE install.ps1 (Windows)

```powershell
# install.ps1 — Agent Memory Skill installer (Windows)
# Source: https://github.com/pgwiz/ai-skills
# Run: irm https://raw.githubusercontent.com/pgwiz/ai-skills/main/install/install.ps1 | iex

param([string]$SkillFolderOverride = "")

$AgentUser       = $env:USERNAME
$AgentHome       = $env:USERPROFILE
$AgentSystemPath = "$AgentHome\agent-system"

# Skill path detection
if ($SkillFolderOverride -ne "") {
    $SkillPath = $SkillFolderOverride
} elseif (Test-Path "$AgentHome\.copilot") {
    $SkillPath = "$AgentHome\.copilot\skills\agent-memory"
} elseif (Test-Path "$AgentHome\.agents") {
    $SkillPath = "$AgentHome\.agents\skills\agent-memory"
} else {
    $SkillPath = "$AgentHome\.copilot\skills\agent-memory"
}

Write-Host ""
Write-Host "=== Agent Memory Skill Installer ===" -ForegroundColor Cyan
Write-Host "User      : $AgentUser"
Write-Host "Home      : $AgentHome"
Write-Host "System    : $AgentSystemPath"
Write-Host "Skill dir : $SkillPath"
Write-Host ""
$confirm = Read-Host "Proceed? (y/n)"
if ($confirm -ne "y") { exit 0 }

# Locate source — support local clone or temp download
if (Test-Path ".\agent-memory\SKILL.md") {
    $SourceRoot = "."
} else {
    Write-Host "Cloning from GitHub..."
    git clone --depth=1 https://github.com/pgwiz/ai-skills.git "$env:TEMP\ai-skills" 2>$null
    $SourceRoot = "$env:TEMP\ai-skills"
}

function Patch-File($FilePath) {
    $c = Get-Content $FilePath -Raw -Encoding UTF8
    $c = $c `
        -replace '\{AGENT_SYSTEM_PATH\}', $AgentSystemPath `
        -replace '\{AGENT_USER\}',        $AgentUser `
        -replace '\{AGENT_HOME\}',        $AgentHome
    Set-Content $FilePath -Value $c -Encoding UTF8
}

# Install global memory files
Write-Host "Installing global memory files..." -ForegroundColor Cyan
New-Item -ItemType Directory -Force -Path $AgentSystemPath | Out-Null

@("GLOBAL_PROTOCOL.md","GLOBAL_WARNINGS.md","CONVENTIONS.md",
  "AGENT_BOOTSTRAP.md","SESSION_START.md","README.md") | ForEach-Object {
    $src  = "$SourceRoot\agent-memory\references\$_"
    $dest = "$AgentSystemPath\$_"
    if (Test-Path $src) {
        Copy-Item $src $dest -Force
        Patch-File $dest
        Write-Host "  v $_" -ForegroundColor DarkGray
    }
}

# Install skill
Write-Host "Installing skill..." -ForegroundColor Cyan
New-Item -ItemType Directory -Force -Path "$SkillPath\references" | Out-Null

Copy-Item "$SourceRoot\agent-memory\SKILL.md" "$SkillPath\SKILL.md" -Force
Patch-File "$SkillPath\SKILL.md"

Get-ChildItem "$SourceRoot\agent-memory\references\*.md" | ForEach-Object {
    Copy-Item $_.FullName "$SkillPath\references\" -Force
    Patch-File "$SkillPath\references\$($_.Name)"
}

# Write .agent-config
$config = @"
AGENT_SYSTEM_PATH=$AgentSystemPath
AGENT_USER=$AgentUser
AGENT_HOME=$AgentHome
INSTALLED_ON=$(Get-Date -Format 'yyyy-MM-dd HH:mm')
PLATFORM=Windows
"@
Set-Content "$AgentSystemPath\.agent-config" -Value $config -Encoding UTF8
Set-Content "$SkillPath\.agent-config"       -Value $config -Encoding UTF8

Write-Host ""
Write-Host "Install complete!" -ForegroundColor Green
Write-Host "Global files : $AgentSystemPath\"
Write-Host "Skill        : $SkillPath\"
Write-Host ""
Write-Host "NEXT STEPS:" -ForegroundColor Cyan
Write-Host "  1. Open any project root"
Write-Host "  2. Tell the agent: Bootstrap .agent/ for this project"
Write-Host "  3. From now on, just type your task"
```

---

## PHASE 4 — README.env GENERATION (post-first-push task)

After the agent bootstraps a project for the first time, it must:

1. Scan the environment
2. Generate `README.env` in the project root
3. Commit and push

### What `README.env` contains:

```md
# Environment Configuration — [PROJECT NAME]
# Auto-generated by agent-memory skill on first bootstrap
# Commit this file. Do NOT commit .env

## Required Environment Variables

| Variable | Description | Example |
|----------|-------------|---------|
| APP_ENV | Application environment | local / production |
| APP_KEY | Laravel app key / Django secret key | base64:... |
| DB_HOST | Database host | 127.0.0.1 |
| DB_PORT | Database port | 3306 |
| DB_DATABASE | Database name | myapp_db |
| DB_USERNAME | Database user | root |
| DB_PASSWORD | Database password | — |
| [add more as discovered from .env.example or settings files] |

## Setup Steps
1. Copy `.env.example` to `.env`
2. Fill in values from the table above
3. Run: [stack-appropriate setup command]

## Stack
- [Detected stack e.g. Laravel 11 / MySQL]
- [Runtime version e.g. PHP 8.3]

## Notes
- [Any environment-specific notes discovered during scan]

---
Generated: [date]
Agent-memory skill: https://github.com/pgwiz/ai-skills
```

### Add to `AGENT_BOOTSTRAP.md` — STEP 6:

```
STEP 6 — Generate README.env
After bootstrap scan is complete:
1. Scan for .env.example, .env.sample, settings.py, config/database.php
   to discover required environment variables
2. Generate README.env in the project root using the template above
3. Commit:
   git add README.env
   git commit -m "docs: add README.env — environment setup guide"
4. Push to active branch:
   git push origin [branch]
5. Report: "README.env generated and pushed"
```

---

## PHASE 5 — INSTALL.MD (human-readable, ships in repo)

```md
# Agent Memory Skill — Install Guide
# https://github.com/pgwiz/ai-skills

A self-installing agent memory system that gives your AI coding agent
persistent project memory, safe file-writing rules, and cross-session context.

Works with: GitHub Copilot (VS Code), Claude Code, any .agents/skills runtime.

---

## Install (pick your method)

### GitHub CLI — recommended
gh skills install pgwiz/ai-skills agent-memory

### macOS / Linux
curl -fsSL https://raw.githubusercontent.com/pgwiz/ai-skills/main/install/install.sh | bash

### Windows (PowerShell)
irm https://raw.githubusercontent.com/pgwiz/ai-skills/main/install/install.ps1 | iex

### Manual
git clone https://github.com/pgwiz/ai-skills.git
cd ai-skills/install
bash install.sh          # macOS/Linux
./install.ps1            # Windows

---

## What gets installed

- Global memory files → ~/agent-system/ (or %USERPROFILE%\agent-system\ on Windows)
- Skill → ~/.copilot/skills/agent-memory/ (auto-detected)
- Config → .agent-config (paths baked in for your machine)

---

## After install

Open any project and tell the agent:
  Bootstrap .agent/ for this project

The agent will:
1. Scan the codebase
2. Generate .agent/ memory files
3. Generate README.env
4. Commit and push README.env

From then on, just type your task. No more repeating yourself.

---

## Per-project (no install needed)

Add the skill directly to any repo:
  mkdir -p .github/skills
  gh skills install pgwiz/ai-skills agent-memory --local

---

## Uninstall

rm -rf ~/agent-system ~/.copilot/skills/agent-memory
# Windows: Remove-Item -Recurse $env:USERPROFILE\agent-system, $env:USERPROFILE\.copilot\skills\agent-memory
```

---

## PHASE 6 — REPO README.md (the GitHub landing page)

```md
# ai-skills

Agent memory and session control skills for GitHub Copilot, Claude Code,
and any agent runtime that supports the Agent Skills open standard.

## Skills

### agent-memory
Gives your agent persistent project memory, safe file-writing rules,
and cross-session context. Works across all projects without re-explaining
your stack, conventions, or codebase every session.

## Install

gh skills install pgwiz/ai-skills agent-memory

Or see [install/INSTALL.md](install/INSTALL.md) for curl/PowerShell/manual options.

## Compatibility

| Runtime | Supported |
|---------|-----------|
| GitHub Copilot (VS Code) | ✓ |
| Claude Code | ✓ |
| GitHub Copilot CLI | ✓ |
| Any .agents/skills runtime | ✓ |
| Windows / macOS / Linux | ✓ |

## Author
pgwiz — https://github.com/pgwiz
```

---

## GITHUB REPOSITORY DESCRIPTION

Paste this exactly into the GitHub repo description field:

```
Agent memory + session control skills for GitHub Copilot and Claude Code. Persistent project memory, safe file-writing rules, cross-platform install.
```

And for the **Topics** field, add:
```
agent-skills  copilot  claude-code  ai-agent  github-copilot  developer-tools  productivity  agent-memory
```

---

## ORDERED TODO FOR AGENT

Execute in order. Report after each step.

- [ ] **STEP 1** — Scan all files. List every hardcoded path or username.
- [ ] **STEP 2** — Replace hardcoded references with `{AGENT_SYSTEM_PATH}` / `{AGENT_USER}` placeholders in all MD files
- [ ] **STEP 3** — Move reference MDs into `agent-memory/references/` folder
- [ ] **STEP 4** — Rewrite `SKILL.md` — add path resolution section, remove identity specifics
- [ ] **STEP 5** — Create `install/install.sh` from Phase 2 template
- [ ] **STEP 6** — Create `install/install.ps1` from Phase 3 template
- [ ] **STEP 7** — Create `install/INSTALL.md` from Phase 5 template
- [ ] **STEP 8** — Create repo `README.md` from Phase 6 template
- [ ] **STEP 9** — Add README.env generation to `AGENT_BOOTSTRAP.md` (Phase 4)
- [ ] **STEP 10** — Verify: grep for remaining hardcoded paths — must come back clean
- [ ] **STEP 11** — Report: every file changed, final folder structure

---

## CONSTRAINTS

- `install.sh` must be POSIX-compatible (no bashisms) — works on macOS + Linux
- `install.ps1` must work without admin on Windows 10/11
- Both installers must be idempotent — safe to re-run
- Never commit `.env` or `.agent-config` — add both to `.gitignore`
- `README.env` IS committed — it is documentation, not secrets
- Skill must work offline after install — no runtime web calls

---

*Implementation plan v2.0 — cross-platform, web-installable*
*pgwiz × Claude — https://github.com/pgwiz/ai-skills*
