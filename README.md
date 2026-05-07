# ai-skills

Agent memory and session control skills for GitHub Copilot, Claude Code,
and any agent runtime that supports the Agent Skills open standard.

## Skills

### agent-memory
Gives your agent persistent project memory, safe file-writing rules,
and cross-session context. Works across all projects without re-explaining
your stack, conventions, or codebase every session.

## Install

### Using GitHub CLI (recommended)

Follow these steps to install or upgrade the GitHub CLI (`gh`), authenticate, and install the skill.

Windows (winget)

```powershell
# Install
winget install --id GitHub.cli
# Upgrade
winget upgrade --id GitHub.cli
```

Linux (Debian/Ubuntu - apt)

```bash
# Ensure curl is present
type -p curl >/dev/null || (sudo apt update && sudo apt install curl -y)
# Add GitHub CLI package repo and key
curl -fsSL https://cli.github.com/packages/githubcli-archive-keyring.gpg | sudo dd of=/usr/share/keyrings/githubcli-archive-keyring.gpg
sudo chmod go+r /usr/share/keyrings/githubcli-archive-keyring.gpg
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/githubcli-archive-keyring.gpg] https://cli.github.com/packages stable main" | sudo tee /etc/apt/sources.list.d/github-cli.list > /dev/null
sudo apt update && sudo apt install gh -y
```

Authenticate with GitHub:

```bash
gh auth login
```

Finally, install the skill:

```bash
gh skills install pgwiz/ai-skills agent-memory
```

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
