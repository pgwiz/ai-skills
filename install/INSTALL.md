# AI Skills — Universal Install Guide
# https://github.com/pgwiz/ai-skills

Automated installers for Google Antigravity, GitHub Copilot, Claude Code, and any agent runtime adhering to the [Agent Skills open standard](https://agentskills.io).

Supported skills:
- **`dev-md-compactor`**: Living markdown compactor and documentation maintenance engine (`dev_md_guides/`).
- **`agent-memory`**: Persistent developer identity, safe file-writing rules, and cross-session memory bootstrap.

Installers are self-configuring: if local source files are present, they install from local files; if not, they automatically pull from GitHub.

---

## 1. Quick Install (Recommended)

### Windows (PowerShell)
To install all skills for auto-detected runtimes (Google Antigravity, GitHub Copilot, Claude Code):
```powershell
irm https://raw.githubusercontent.com/pgwiz/ai-skills/main/install/install.ps1 | iex
```

To target a specific runtime or skill:
```powershell
# Install all skills into Google Antigravity only:
& ([scriptblock]::Create((irm https://raw.githubusercontent.com/pgwiz/ai-skills/main/install/install.ps1))) -Target antigravity -Skill all -Yes

# Install only dev-md-compactor:
& ([scriptblock]::Create((irm https://raw.githubusercontent.com/pgwiz/ai-skills/main/install/install.ps1))) -Skill dev-md-compactor -Yes
```

### macOS / Linux / WSL (POSIX Shell)
To install all skills for auto-detected runtimes:
```bash
curl -fsSL https://raw.githubusercontent.com/pgwiz/ai-skills/main/install/install.sh | bash
```

To target a specific runtime or skill:
```bash
# Install all skills into Google Antigravity only:
curl -fsSL https://raw.githubusercontent.com/pgwiz/ai-skills/main/install/install.sh | bash -s -- --target antigravity --skill all -y

# Install only dev-md-compactor:
curl -fsSL https://raw.githubusercontent.com/pgwiz/ai-skills/main/install/install.sh | bash -s -- --skill dev-md-compactor -y
```

---

## 2. GitHub CLI (`gh skills`)

If you use GitHub CLI with the skills extension:
```bash
# Install dev-md-compactor
gh skills install pgwiz/ai-skills dev-md-compactor

# Install agent-memory
gh skills install pgwiz/ai-skills agent-memory
```

---

## 3. Local Repository Execution

When you have cloned the repository locally:
```bash
git clone https://github.com/pgwiz/ai-skills.git
cd ai-skills
```

**PowerShell:**
```powershell
.\install\install.ps1 -Target antigravity -Skill all -Yes
```

**Bash:**
```bash
./install/install.sh --target antigravity --skill all -y
```

---

## 4. What Gets Installed

| Component | Target Location | Description |
|---|---|---|
| **Global memory files** | `~/agent-system/` (`%USERPROFILE%\agent-system\`) | System protocol, bootstrap rules, and global conventions |
| **Google Antigravity** | `~/.gemini/config/skills/<skill-name>/` | Globally active skills for Google Antigravity sessions |
| **GitHub Copilot** | `~/.copilot/skills/<skill-name>/` | Globally active skills for Copilot CLI & VS Code |
| **Agent Skills / Claude** | `~/.agents/skills/<skill-name>/` | Standard agent skills runtime directory |
| **Configuration** | `.agent-config` | Machine-specific path bindings and identity tokens |

---

## 5. Usage & Verification

### dev-md-compactor
- In Antigravity: Trigger via `/compact-docs` or ask `"compact memory"`, `"update dev guides"`.
- Proactive compaction: Automatically runs when tasks conclude.
- Deterministic CLI:
  ```bash
  python dev-md-compactor/scripts/run_compactor.py
  ```

### agent-memory
- In any new project root, prompt your agent:
  > *"Bootstrap .agent/ for this project"*
- The agent will initialize `.agent/` memory files, configure `README.env`, and enforce conventions.

---

## 6. Uninstall

```bash
# Antigravity:
rm -rf ~/.gemini/config/skills/dev-md-compactor ~/.gemini/config/skills/agent-memory

# Copilot:
rm -rf ~/.copilot/skills/dev-md-compactor ~/.copilot/skills/agent-memory

# Global system files:
rm -rf ~/agent-system
```

On Windows (PowerShell):
```powershell
Remove-Item -Recurse -Force "$env:USERPROFILE\.gemini\config\skills\dev-md-compactor", "$env:USERPROFILE\.gemini\config\skills\agent-memory", "$env:USERPROFILE\agent-system" -ErrorAction SilentlyContinue
```
