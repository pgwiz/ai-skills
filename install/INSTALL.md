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

Step-by-step to get to the skill install command:

1. **Install or upgrade `gh` on Windows (winget):**
   - Install: `winget install --id GitHub.cli`
   - Upgrade: `winget upgrade --id GitHub.cli`
2. **Install `gh` on Linux (apt):**
   - `type -p curl >/dev/null || (sudo apt update && sudo apt install curl -y)`
   - `curl -fsSL https://cli.github.com/packages/githubcli-archive-keyring.gpg | sudo dd of=/usr/share/keyrings/githubcli-archive-keyring.gpg`
   - `sudo chmod go+r /usr/share/keyrings/githubcli-archive-keyring.gpg`
   - `echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/githubcli-archive-keyring.gpg] https://cli.github.com/packages stable main" | sudo tee /etc/apt/sources.list.d/github-cli.list > /dev/null`
   - `sudo apt update && sudo apt install gh -y`
3. **Upgrade `gh` on Linux:** `sudo apt update && sudo apt install gh -y`
4. **Authenticate:** `gh auth login`
5. **Install the skill:** `gh skills install pgwiz/ai-skills agent-memory`

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
