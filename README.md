# ai-skills

Agent memory, context compaction, and living documentation skills for Google Antigravity, Claude Code, GitHub Copilot, and any agent runtime adhering to the [Agent Skills open standard](https://agentskills.io).

## Available Skills

### 1. `dev-md-compactor`
A specialized context compactor and living documentation engine. Transforms conversational context, AST code changes, git worktrees, and dependency graphs into persistent repository guides within `dev_md_guides/` orchestrated by a root router:
- `dev_com_agent.md` — Universal root entry point and context router enforcing progressive disclosure and inviolable ground rules.
- `agent.md` — Master summary index, dynamic topic catalog, and auto-generated structural documentation inventory.
- `branch.md` — Active branch, upstream divergence, and uncommitted diff surface.
- `features.md` — Spec-Driven Development (SDD) progress and feature matrices.
- `structure.md` — Module topography, entry points, and inter-folder import dependencies.
- `memory.md` — Durable Architecture Decision Records (ADRs) and immutable system invariants.
- `gotchas.md` — Categorized failure mode analysis (Major Blockers vs. Minor Quirks), root causes, exact fixes, and fix mechanics.
- `flow.md` — Procedural execution flows, test sequences, context compaction protocols, and git release pipelines.
- `changelog.md` — Append-only chronological audit log of operational runs and modified AST symbols.
- `directory.md` & `directory.md.sample` — Centralized environment and routing catalog (servers, backend/frontend links, project directories). Prevents hardcoded paths and protects private endpoints by committing only `directory.md.sample` to GitHub.
- `credentials.md` & `credentials.md.sample` — Centralized secrets schema. Real credentials remain strictly local in gitignored `credentials.md`; only `credentials.md.sample` with mock placeholders is committed. Includes automated secret leak scanning and a mandatory warning protocol if secret commits are ever attempted.
- **Dynamic Topic Guides** (e.g. `commands.md`, `mcp.md`) — Spawned dynamically when recurring CLI patterns or MCP tool quirks emerge.

Backed by in-depth research: see [research/Agent Memory Compaction Research.md](research/Agent%20Memory%20Compaction%20Research.md).

### 2. `agent-memory`
Gives your agent persistent developer identity, safe file-writing rules, and cross-session context. Bootstraps project memory across codebases without re-explaining stack conventions or guidelines each session.

---

## Installation

### Google Antigravity

#### Global Install (All Projects)
Copy `dev-md-compactor` into your global Antigravity skills directory:

**Windows (PowerShell):**
```powershell
New-Item -ItemType Directory -Force -Path "$HOME\.gemini\config\skills\dev-md-compactor"
Copy-Item -Path "dev-md-compactor\*" -Destination "$HOME\.gemini\config\skills\dev-md-compactor\" -Recurse -Force
```

**macOS / Linux:**
```bash
mkdir -p ~/.gemini/config/skills/dev-md-compactor
cp -r dev-md-compactor/* ~/.gemini/config/skills/dev-md-compactor/
```

#### Project-Local Install
Place the skill inside your project's `.agent/skills/` directory and add `.agent/workflows/compact-docs.md`. Antigravity will discover it automatically and enable the `/compact-docs` command.

---

### Claude Code & GitHub Copilot CLI

#### Using GitHub CLI (`gh skills`)

```bash
# Install agent-memory
gh skills install pgwiz/ai-skills agent-memory

# Install dev-md-compactor
gh skills install pgwiz/ai-skills dev-md-compactor
```

See [install/INSTALL.md](install/INSTALL.md) for curl, PowerShell, and manual installation options.

---

## Usage

### dev-md-compactor

- **Explicit Command:** Run `/compact-docs` in chat.
- **Natural Language:** Ask the agent to `"compact memory"`, `"save our progress"`, `"update dev guides"`, or `"write changelog"`.
- **Proactive Execution:** Agents configured with `GEMINI.md` or `AGENTS.md` automatically trigger compaction at task-completion boundaries before context resets.
- **Standalone CLI:** You can also run the deterministic compactor script directly from terminal:
  ```bash
  python dev-md-compactor/scripts/run_compactor.py
  ```

---

## Compatibility

| Runtime | Supported |
|---------|-----------|
| Google Antigravity | ✓ |
| Claude Code | ✓ |
| GitHub Copilot (VS Code) | ✓ |
| GitHub Copilot CLI | ✓ |
| Any Agent Skills runtime (`.agents/skills`) | ✓ |
| Windows / macOS / Linux | ✓ |

---

## Author
pgwiz — https://github.com/pgwiz
