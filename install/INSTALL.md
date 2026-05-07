# Agent Memory Skill — Install Guide
# https://github.com/pgwiz/ai-skills

A self-installing agent memory system that gives your AI coding agent
persistent project memory, safe file-writing rules, and cross-session context.

Works with: GitHub Copilot (VS Code), Claude Code, any .agents/skills runtime.

Installers are self-configuring: if local source files are present, they install from local;
if not, they automatically pull from GitHub and continue.

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
bash install.sh
./install.ps1

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
