# AGENT CONTROL & LIVING DOCUMENTATION SKILLS — GLOBAL INSTALL IMPLEMENTATION PLAN v2
# Cross-platform. Multi-runtime. Web-installable. Self-configuring.
# Repo: https://github.com/pgwiz/ai-skills
# Status: RECONCILED & COMPLETED (Audited October 2026)

---

## 1. OVERVIEW

This plan defines the architecture, cross-platform installation pipeline, and implementation milestones for the `ai-skills` suite:
- **Multi-Skill Suite**:
  1. [`dev-md-compactor`](dev-md-compactor/SKILL.md) — Living markdown compactor and documentation maintenance engine (`dev_md_guides/`, `dev_com_agent.md`).
  2. [`agent-memory`](agent-memory/SKILL.md) — Persistent developer identity, safe file-writing rules, and cross-session context bootstrap.
- **Cross-platform**: Windows (PowerShell), macOS/Linux/WSL (POSIX shell).
- **Multi-runtime**: Google Antigravity, GitHub Copilot (VS Code & CLI), Claude Code, and any [Agent Skills](https://agentskills.io) open-standard runtime.
- **Web-installable**: One-liner PowerShell (`irm ... | iex`), POSIX curl pipe (`curl ... | bash`), or GitHub CLI (`gh skills install`).
- **Self-configuring**: Automatically resolves `{AGENT_SYSTEM_PATH}`, `{AGENT_USER}`, and `{AGENT_HOME}`, and writes machine-specific `.agent-config`.
- **Zero-Credential Safety**: Strict gitignore enforcement for `credentials.md`, `directory.md`, and local sensitive overrides (`local.*.md`), with automated secret leak scanning and mandatory user warnings.

---

## 2. PRODUCTION REPOSITORY STRUCTURE

```
pgwiz/ai-skills (GitHub)
  dev_com_agent.md                  ← Universal agent root entry point & context router
  GEMINI.md                         ← Project agent instructions & rehydration protocol
  README.md                         ← Repository landing page & installation matrix
  .gitignore                        ← Gitignore rules (ignores credentials.md, directory.md, local.*.md)
  
  dev-md-compactor/                 ← Living documentation compactor skill
    SKILL.md                        ← Compactor skill definition & conversational reflection protocol
    references/                     ← Compaction rules, budgets, and file schemas
      file-formats.md
      update-rules.md
    scripts/                        ← Extraction engines & security scanner
      gather_context.sh             ← POSIX shell context extractor
      run_compactor.py              ← AST extraction, living guide generator & secret scanner
    templates/                      ← Seed templates for dev_com_agent.md and dev_md_guides/
      agent.md                      ← Master summary index & dynamic inventory
      branch.md                     ← Ephemeral git worktree & diff tracker
      changelog.md                  ← Append-only session audit log
      commands.md                   ← Dynamic topic guide template
      credentials.md                ← Local secrets template (gitignored)
      credentials.md.sample         ← Committed secrets reference schema
      dev_com_agent.md              ← Root router template
      directory.md                  ← Local environment catalog (gitignored)
      directory.md.sample           ← Committed environment reference schema
      features.md                   ← Spec-Driven Development status matrix
      flow.md                       ← Procedural execution flows & recipes
      gotchas.md                    ← Categorized failure mode analysis
      local.agent.md                ← Local sensitive agent override template (gitignored)
      mcp.md                        ← Dynamic MCP tool reference template
      memory.md                     ← Architecture Decision Records (ADRs) & invariants
      structure.md                  ← Codebase topography & module architecture

  agent-memory/                     ← Memory bootstrap & session control skill
    SKILL.md                        ← Memory skill definition & developer identity loader
    references/                     ← Protocol documents loaded on demand
      AGENT_BOOTSTRAP.md            ← First-run codebase bootstrap workflow
      CONVENTIONS.md                ← Multi-stack coding & formatting conventions
      GLOBAL_PROTOCOL.md            ← Core agent rules, audit standards, & safety gates
      GLOBAL_WARNINGS.md            ← Critical destructive command warnings
      README.md                     ← Memory system overview
      SESSION_START.md              ← Session initialization checklist

  install/                          ← Universal installation package
    install.ps1                     ← Production Windows PowerShell installer
    install.sh                      ← Production POSIX shell installer
    INSTALL.md                      ← Human-readable universal install guide

  research/                         ← Background research & architectural studies
    Agent Memory Compaction Research.docx
    Agent Memory Compaction Research.md

  tests/                            ← Automated verification suite
    test_compactor.py               ← Unit tests for compactor, templates, gitignore & security
```

---

## 3. SUPPORTED AGENT RUNTIMES & INSTALL PATHS

The installer auto-detects or accepts explicit target flags (`-Target` / `--target`) to install skills into the appropriate runtime directory:

| Runtime | Platform | Target Path | Selection Flag |
|---|---|---|---|
| **Google Antigravity** | Windows | `%USERPROFILE%\.gemini\config\skills\<skill-name>\` | `-Target antigravity` |
| **Google Antigravity** | macOS / Linux | `~/.gemini/config/skills/<skill-name>/` | `--target antigravity` |
| **GitHub Copilot** | Windows | `%USERPROFILE%\.copilot\skills\<skill-name>\` | `-Target copilot` |
| **GitHub Copilot** | macOS / Linux | `~/.copilot/skills/<skill-name>/` | `--target copilot` |
| **Agent Skills / Claude Code** | Windows | `%USERPROFILE%\.agents\skills\<skill-name>\` | `-Target agents` |
| **Agent Skills / Claude Code** | macOS / Linux | `~/.agents/skills/<skill-name>/` | `--target agents` |
| **All Detected Runtimes** | Cross-platform | Installs to all present runtimes simultaneously | `-Target all` / `--target all` |
| **Custom Path Override** | Cross-platform | Any user-specified directory | `-SkillFolderOverride <path>` |
| **Global Memory Files** | Windows / Unix | `%USERPROFILE%\agent-system\` or `~/agent-system/` | Auto-configured |

---

## 4. WEB INSTALLATION METHODS

### Method 1 — Windows PowerShell (One-Liner)
```powershell
# Interactive installation (auto-detects runtimes and prompts for confirmation)
irm https://raw.githubusercontent.com/pgwiz/ai-skills/main/install/install.ps1 | iex

# Unattended install for Google Antigravity (all skills):
& ([scriptblock]::Create((irm https://raw.githubusercontent.com/pgwiz/ai-skills/main/install/install.ps1))) -Target antigravity -Skill all -Yes

# Unattended install for dev-md-compactor only:
& ([scriptblock]::Create((irm https://raw.githubusercontent.com/pgwiz/ai-skills/main/install/install.ps1))) -Skill dev-md-compactor -Yes
```

### Method 2 — macOS / Linux / WSL (POSIX Curl Pipe)
```bash
# Interactive installation:
curl -fsSL https://raw.githubusercontent.com/pgwiz/ai-skills/main/install/install.sh | bash

# Unattended install for Google Antigravity (all skills):
curl -fsSL https://raw.githubusercontent.com/pgwiz/ai-skills/main/install/install.sh | bash -s -- --target antigravity --skill all -y

# Unattended install for dev-md-compactor only:
curl -fsSL https://raw.githubusercontent.com/pgwiz/ai-skills/main/install/install.sh | bash -s -- --skill dev-md-compactor -y
```

### Method 3 — GitHub CLI (`gh skills`)
```bash
# Install living documentation compactor
gh skills install pgwiz/ai-skills dev-md-compactor

# Install memory & session control skill
gh skills install pgwiz/ai-skills agent-memory
```

### Method 4 — Local Repository Execution
```bash
git clone https://github.com/pgwiz/ai-skills.git
cd ai-skills

# Windows:
.\install\install.ps1 -Target antigravity -Skill all -Yes

# macOS / Linux:
./install/install.sh --target antigravity --skill all -y
```

---

## 5. USER-AGNOSTIC PLACEHOLDER ARCHITECTURE

All distributed skill files use dynamic placeholders so the repository remains 100% portable and free of machine-specific usernames or hardcoded paths:

| Placeholder | Resolved By Installer (Windows) | Resolved By Installer (POSIX) | Description |
|---|---|---|---|
| `{AGENT_USER}` | `$env:USERNAME` | `$(whoami)` | Operating system user account name |
| `{AGENT_HOME}` | `$env:USERPROFILE` | `$HOME` | User home directory path |
| `{AGENT_SYSTEM_PATH}` | `$env:USERPROFILE\agent-system` | `$HOME/agent-system` | Central location for global memory protocols |

### Machine Configuration `.agent-config`
During installation, the installer generates an `.agent-config` file in both the global system path and skill directories:
```ini
AGENT_SYSTEM_PATH=/home/username/agent-system
AGENT_USER=username
AGENT_HOME=/home/username
INSTALLED_ON=2026-10-01 20:30
PLATFORM=Linux
```

---

## 6. PRODUCTION INSTALLER IMPLEMENTATIONS

### 6.1 Windows PowerShell Installer (`install/install.ps1`)
The production PowerShell installer supports runtime targeting, skill filtering, GitHub download fallbacks (via git clone or zip extraction), file placeholder replacement, and `.agent-config` creation:

```powershell
# install.ps1 - Universal AI Skills installer (Windows)
# Source: https://github.com/pgwiz/ai-skills
# Run: irm https://raw.githubusercontent.com/pgwiz/ai-skills/main/install/install.ps1 | iex

param(
    [string]$SkillFolderOverride = "",
    [ValidateSet("auto", "antigravity", "copilot", "agents", "all")]
    [string]$Target = "auto",
    [ValidateSet("all", "agent-memory", "dev-md-compactor")]
    [string]$Skill = "all",
    [switch]$Yes
)

$AgentUser = $env:USERNAME
$AgentHome = $env:USERPROFILE
$AgentSystemPath = "$AgentHome\agent-system"

# Determine target directories
$TargetBaseDirs = @{}

if ($SkillFolderOverride -ne "") {
    $TargetBaseDirs["custom"] = $SkillFolderOverride
} else {
    $TargetsToProcess = @()
    if ($Target -eq "all") {
        $TargetsToProcess = @("antigravity", "copilot", "agents")
    } elseif ($Target -ne "auto") {
        $TargetsToProcess = @($Target)
    } else {
        if (Test-Path "$AgentHome\.gemini\config\skills") { $TargetsToProcess += "antigravity" }
        if (Test-Path "$AgentHome\.copilot")              { $TargetsToProcess += "copilot" }
        if (Test-Path "$AgentHome\.agents")               { $TargetsToProcess += "agents" }
        if ($TargetsToProcess.Count -eq 0) {
            if (Test-Path "$AgentHome\.gemini") { $TargetsToProcess += "antigravity" }
            else { $TargetsToProcess += "copilot" }
        }
    }

    foreach ($t in $TargetsToProcess) {
        switch ($t) {
            "antigravity" { $TargetBaseDirs["antigravity"] = "$AgentHome\.gemini\config\skills" }
            "copilot"     { $TargetBaseDirs["copilot"]     = "$AgentHome\.copilot\skills" }
            "agents"      { $TargetBaseDirs["agents"]      = "$AgentHome\.agents\skills" }
        }
    }
}

# Determine skills to install
$SkillsToInstall = if ($Skill -eq "all") { @("agent-memory", "dev-md-compactor") } else { @($Skill) }

Write-Host "`n=== AI Skills Universal Installer (Windows) ===" -ForegroundColor Cyan
Write-Host "User        : $AgentUser"
Write-Host "Home        : $AgentHome"
Write-Host "System Path : $AgentSystemPath"
Write-Host "Skills      : $($SkillsToInstall -join ', ')"
Write-Host "Targets     : $($TargetBaseDirs.Keys -join ', ')"
foreach ($kv in $TargetBaseDirs.GetEnumerator()) {
    Write-Host "  -> $($kv.Key): $($kv.Value)" -ForegroundColor DarkGray
}
Write-Host ""

if (-not $Yes) {
    $confirm = Read-Host "Proceed? (y/n)"
    if ($confirm -ne "y") {
        Write-Host "Installation cancelled." -ForegroundColor Yellow
        exit 0
    }
}

# Locate source files
if ((Test-Path ".\agent-memory\SKILL.md") -or (Test-Path ".\dev-md-compactor\SKILL.md")) {
    $SourceRoot = "."
    $TempRoot = $null
} elseif ((Test-Path "..\agent-memory\SKILL.md") -or (Test-Path "..\dev-md-compactor\SKILL.md")) {
    $SourceRoot = ".."
    $TempRoot = $null
} else {
    $TempRoot = Join-Path $env:TEMP ("ai-skills-" + [guid]::NewGuid().ToString("N"))
    New-Item -ItemType Directory -Force -Path $TempRoot | Out-Null
    Write-Host "Fetching skills source from GitHub..." -ForegroundColor Cyan
    if (Get-Command git -ErrorAction SilentlyContinue) {
        git clone --depth=1 https://github.com/pgwiz/ai-skills.git "$TempRoot\repo" 2>$null
        $SourceRoot = "$TempRoot\repo"
    } else {
        $zipPath = Join-Path $TempRoot "repo.zip"
        $extractPath = Join-Path $TempRoot "extract"
        New-Item -ItemType Directory -Force -Path $extractPath | Out-Null
        Invoke-WebRequest -Uri "https://github.com/pgwiz/ai-skills/archive/refs/heads/main.zip" -OutFile $zipPath
        Expand-Archive -Path $zipPath -DestinationPath $extractPath -Force
        $SourceRoot = Join-Path $extractPath "ai-skills-main"
    }
}

function Patch-File([string]$FilePath) {
    $c = Get-Content -Path $FilePath -Raw -Encoding UTF8
    $c = $c.Replace('{AGENT_SYSTEM_PATH}', $AgentSystemPath)
    $c = $c.Replace('{AGENT_USER}', $AgentUser)
    $c = $c.Replace('{AGENT_HOME}', $AgentHome)
    Set-Content -Path $FilePath -Value $c -Encoding UTF8
}

$InstalledLocations = @()

# 1. Install agent-memory
if ($SkillsToInstall -contains "agent-memory") {
    Write-Host "Installing global memory files for agent-memory..." -ForegroundColor Cyan
    New-Item -ItemType Directory -Force -Path $AgentSystemPath | Out-Null

    @("GLOBAL_PROTOCOL.md","GLOBAL_WARNINGS.md","CONVENTIONS.md","AGENT_BOOTSTRAP.md","SESSION_START.md","README.md") | ForEach-Object {
        $src = "$SourceRoot\agent-memory\references\$_"
        $dest = "$AgentSystemPath\$_"
        if (Test-Path $src) {
            Copy-Item $src $dest -Force
            Patch-File $dest
            Write-Host "  + $_" -ForegroundColor DarkGray
        }
    }

    $nowStr = Get-Date -Format 'yyyy-MM-dd HH:mm'
    $config = "AGENT_SYSTEM_PATH=$AgentSystemPath`nAGENT_USER=$AgentUser`nAGENT_HOME=$AgentHome`nINSTALLED_ON=$nowStr`nPLATFORM=Windows`n"
    Set-Content "$AgentSystemPath\.agent-config" -Value $config -Encoding UTF8

    foreach ($entry in $TargetBaseDirs.GetEnumerator()) {
        $baseDir = $entry.Value
        $skillDir = if ($entry.Key -eq "custom" -and ($baseDir -match "agent-memory$")) { $baseDir } else { Join-Path $baseDir "agent-memory" }
        Write-Host "Installing agent-memory to $($entry.Key) [$skillDir]..." -ForegroundColor Cyan

        New-Item -ItemType Directory -Force -Path "$skillDir\references" | Out-Null
        Copy-Item "$SourceRoot\agent-memory\SKILL.md" "$skillDir\SKILL.md" -Force
        Patch-File "$skillDir\SKILL.md"

        Get-ChildItem "$SourceRoot\agent-memory\references\*.md" | ForEach-Object {
            Copy-Item $_.FullName "$skillDir\references\" -Force
            Patch-File "$skillDir\references\$($_.Name)"
        }

        Set-Content "$skillDir\.agent-config" -Value $config -Encoding UTF8
        $InstalledLocations += $skillDir
    }
}

# 2. Install dev-md-compactor
if ($SkillsToInstall -contains "dev-md-compactor") {
    foreach ($entry in $TargetBaseDirs.GetEnumerator()) {
        $baseDir = $entry.Value
        $skillDir = if ($entry.Key -eq "custom" -and ($baseDir -match "dev-md-compactor$")) { $baseDir } else { Join-Path $baseDir "dev-md-compactor" }
        Write-Host "Installing dev-md-compactor to $($entry.Key) [$skillDir]..." -ForegroundColor Cyan

        New-Item -ItemType Directory -Force -Path $skillDir | Out-Null
        Copy-Item "$SourceRoot\dev-md-compactor\SKILL.md" "$skillDir\SKILL.md" -Force

        # references
        $refDest = Join-Path $skillDir "references"
        New-Item -ItemType Directory -Force -Path $refDest | Out-Null
        Get-ChildItem -Path "$SourceRoot\dev-md-compactor\references" -Filter "*.md" | ForEach-Object {
            Copy-Item $_.FullName "$refDest\" -Force
        }

        # scripts
        $scriptDest = Join-Path $skillDir "scripts"
        New-Item -ItemType Directory -Force -Path $scriptDest | Out-Null
        Get-ChildItem -Path "$SourceRoot\dev-md-compactor\scripts" -File | ForEach-Object {
            Copy-Item $_.FullName "$scriptDest\" -Force
        }

        # templates
        $tplDest = Join-Path $skillDir "templates"
        New-Item -ItemType Directory -Force -Path $tplDest | Out-Null
        Get-ChildItem -Path "$SourceRoot\dev-md-compactor\templates" -File | ForEach-Object {
            Copy-Item $_.FullName "$tplDest\" -Force
        }

        $InstalledLocations += $skillDir
    }
}

Write-Host "`nInstall complete!" -ForegroundColor Green
if ($SkillsToInstall -contains "agent-memory") {
    Write-Host "Global memory files : $AgentSystemPath\"
}
Write-Host "Installed skill locations:"
foreach ($loc in $InstalledLocations) {
    Write-Host "  + $loc" -ForegroundColor Green
}

if ($TempRoot -and (Test-Path $TempRoot)) {
    Remove-Item -Recurse -Force $TempRoot
}
```

---

### 6.2 POSIX Shell Installer (`install/install.sh`)
The POSIX installer runs on macOS, Linux, and WSL using pure `/bin/sh` syntax without non-portable bashisms, providing identical CLI switches (`--target`, `--skill`, `--override`, `-y`):

```sh
#!/usr/bin/env sh
# install.sh - Universal AI Skills installer (macOS, Linux, WSL)
# Source: https://github.com/pgwiz/ai-skills

set -eu

AGENT_USER="$(whoami)"
AGENT_HOME="${HOME}"
AGENT_SYSTEM_PATH="${HOME}/agent-system"

TARGET="auto"
SKILL="all"
SKILL_FOLDER_OVERRIDE=""
ASSUME_YES=0

while [ $# -gt 0 ]; do
  case "$1" in
    --target|-t)   TARGET="$2"; shift 2 ;;
    --skill|-s)    SKILL="$2"; shift 2 ;;
    --override|-o) SKILL_FOLDER_OVERRIDE="$2"; shift 2 ;;
    -y|--yes)      ASSUME_YES=1; shift ;;
    *) echo "Unknown option: $1" >&2; exit 1 ;;
  esac
done

# (Resolves TARGET_DIRS, downloads source if needed, patches files, copies references, scripts, templates)
```

---

## 7. LIVING DOCUMENTATION & CONTEXT COMPACTION ARCHITECTURE

The `dev-md-compactor` skill introduces a structured documentation system designed for persistent agent context:

```
[Universal Router: dev_com_agent.md]
  │
  ├──► [Master Index: dev_md_guides/agent.md]
  │      ├──► branch.md         (Ephemeral worktree, branch, HEAD, uncommitted diffs)
  │      ├──► features.md       (Spec-Driven Development status matrix)
  │      ├──► structure.md      (Module topography, entry points, dependencies)
  │      ├──► memory.md         (Architecture Decision Records & system invariants)
  │      ├──► gotchas.md        (Categorized failure modes: Major Blockers vs Minor Quirks)
  │      ├──► flow.md           (Execution flows, test recipes, verification checklists)
  │      ├──► changelog.md      (Reverse-chronological append-only operational audit log)
  │      ├──► directory.md      (Environment catalog; gitignored locally; deploy sample only)
  │      ├──► credentials.md    (Active secrets; strictly gitignored; deploy sample only)
  │      ├──► local.agent.md    (Local sensitive agent notes; strictly gitignored)
  │      └──► Dynamic Guides    (commands.md, mcp.md - spawned on 3+ recurring patterns)
```

### Core Security & Privacy Invariants
1. **Zero Hardcoded Endpoints**: All servers, backend links, frontend URLs, and ports are resolved via [`dev_md_guides/directory.md`](dev_md_guides/directory.md). Only [`directory.md.sample`](dev_md_guides/directory.md.sample) is committed to GitHub.
2. **Zero Credential Exposure**: Real API keys and passwords live exclusively in [`dev_md_guides/credentials.md`](dev_md_guides/credentials.md) (strictly gitignored). Only [`credentials.md.sample`](dev_md_guides/credentials.md.sample) with mock placeholders is committed.
3. **Local Sensitive Overrides (`local.*.md` / `*.local.md`)**:
   - Any sensitive or machine-specific notes (e.g., `local.agent.md`, `dev_md_guides/local.agent.md`) are gitignored by default and never pushed to GitHub.
   - The compactor engine recognizes these files as `Local Private Override` (`Gitignored`).
4. **Automated Secret Leak Scanner**: `run_compactor.py` scans tracked markdown guides for unredacted API keys, private keys, or passwords, issuing high-visibility security alerts before commits are pushed.
5. **Mandatory Warning Protocol**: If a user ever requests committing credentials or `credentials.md`, the agent must refuse to proceed without first issuing an explicit security warning detailing the risks.

---

## 8. RECONCILED IMPLEMENTATION MILESTONES & VERIFICATION AUDIT

All planned phases have been executed and verified in the codebase:

- [x] **MILESTONE 1 — User-Agnostic Placeholders & Template Sanitization**
  - Replaced hardcoded paths with `{AGENT_SYSTEM_PATH}`, `{AGENT_USER}`, and `{AGENT_HOME}` across all reference markdown files.
  - Verified that identity specifics are removed and loaded dynamically via `GLOBAL_PROTOCOL.md` and `.agent-config`.

- [x] **MILESTONE 2 — Reference Directory Reorganization**
  - Moved all protocol documents into `agent-memory/references/` (`GLOBAL_PROTOCOL.md`, `GLOBAL_WARNINGS.md`, `CONVENTIONS.md`, `AGENT_BOOTSTRAP.md`, `SESSION_START.md`, `README.md`).

- [x] **MILESTONE 3 — Universal Cross-Platform Installers**
  - Created `install/install.ps1` with multi-target support (`antigravity`, `copilot`, `agents`, `all`), skill selection, and unattended flags.
  - Created `install/install.sh` with strict POSIX compatibility and identical command-line flags.
  - Authored `install/INSTALL.md` with full usage instructions for PowerShell, curl, `gh skills`, and manual cloning.

- [x] **MILESTONE 4 — Living Documentation Compactor (`dev-md-compactor`)**
  - Implemented `dev_com_agent.md` universal entry point router and `dev_md_guides/` directory structure.
  - Built `run_compactor.py` Python extraction engine with AST symbol tracking, directory/credentials catalog loaders, and dynamic inventory management.
  - Built `gather_context.sh` POSIX context gathering script with secret audit and branch inspection.
  - Added failure mode tracking in `gotchas.md` (Major Blockers vs Minor Quirks) and procedural flows in `flow.md`.
  - Added dynamic topic guide spawning for recurring patterns (`commands.md`, `mcp.md`).

- [x] **MILESTONE 5 — Local Sensitive Overrides & Privacy Hardening**
  - Implemented `local.<filename>.md` / `*.local.md` sensitive override protocol.
  - Ensured `.gitignore` ignores `dev_md_guides/directory.md`, `dev_md_guides/credentials.md`, and all `local.*.md` files while whitelisting `.sample` files.
  - Updated `run_compactor.py` and `gather_context.sh` to audit git status and prevent accidental tracking of sensitive overrides.

- [x] **MILESTONE 6 — Automated Unit Testing & Continuous Verification**
  - Implemented comprehensive test suite in `tests/test_compactor.py` covering catalog parsing, AST symbol extraction, template seeding, inventory generation, secret leak scanning, and gitignore enforcement.
  - Test suite passes with 100% success rate across all 27 unit tests.

- [x] **MILESTONE 7 — Global Skill Installation & Mirror Synchronization**
  - Successfully synced skills to Google Antigravity global directory (`~/.gemini/config/skills/`), project `.agent/skills/`, and `~/agent-system/`.

---

*AI Skills Installation Implementation Plan v2.0 (Reconciled & Up-to-Date)*  
*Repository: https://github.com/pgwiz/ai-skills*
