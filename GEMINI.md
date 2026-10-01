# Project Agent Instructions

## Master Entry Point & Context Router
- **Universal Entry Point**: [`dev_com_agent.md`](dev_com_agent.md) at repository root is the master entry point and context router. Follow its progressive disclosure protocol before arbitrary exploration.

## Session Memory & Context Compaction

This project uses the **dev-md-compactor** skill (`dev-md-compactor/SKILL.md` or `.agent/skills/dev-md-compactor/SKILL.md`) to persist project state across sessions into a `dev_md_guides/` directory at the project root:

- `dev_md_guides/agent.md` — master index & progressive disclosure summary table of all active guides
- `dev_md_guides/branch.md` — active branch worktree, upstream tracking, divergence, and uncommitted diffs
- `dev_md_guides/features.md` — capabilities matrix and Spec-Driven Development (SDD) statuses
- `dev_md_guides/structure.md` — codebase topology, entry points, and module dependency graph
- `dev_md_guides/memory.md` — durable architecture decisions (ADRs) and system invariants
- `dev_md_guides/gotchas.md` — categorized major blockers vs minor quirks, root causes, exact fixes, mechanics
- `dev_md_guides/flow.md` — multi-step execution workflows and operational recipes
- `dev_md_guides/changelog.md` — reverse-chronological, append-only operational audit log
- `dev_md_guides/directory.md` & `directory.md.sample` — environment catalog for directories, servers, backend/frontend links, and ports (deploy sample only)
- `dev_md_guides/credentials.md` & `credentials.md.sample` — credentials and secrets reference (deploy sample only with mock placeholders; real secrets stay strictly local and gitignored)
- Dynamic topic guides (e.g. `commands.md`, `mcp.md`) — spawned dynamically when recurring patterns or tool quirks emerge

### Proactive Trigger Protocol
- **Trigger automatically** whenever a non-trivial engineering task wraps up (multiple files modified, a feature delivered, a refactor concluded, or a bug root-caused) — do not wait to be asked.
- It can also be invoked explicitly with `/compact-docs` or when the user asks to "compact memory", "save progress", or "update dev guides".

### Rehydration & Security Rules
- Before starting any non-trivial coding task, consult [`dev_com_agent.md`](dev_com_agent.md) and [`dev_md_guides/agent.md`](dev_md_guides/agent.md) first to identify which targeted guides to read (`branch.md`, `memory.md`, `gotchas.md`, `flow.md`).
- Never hardcode directory paths, server IPs, backend URLs, or frontend URLs across markdown files; rely on `dev_md_guides/directory.md`.
- **Zero Credential Exposure**: NEVER commit real credentials, API tokens, private keys, or passwords to git/GitHub. Keep `dev_md_guides/credentials.md` strictly local and gitignored.
- **Mandatory Agent Warning Protocol**: If the user ever specifies or instructs committing credentials or `credentials.md` to version control, the agent MUST NOT proceed without first issuing an explicit, high-visibility security warning detailing the severe risks of secret exposure and requiring explicit user confirmation.
- **Strict Anti-Hallucination Audit Protocol**: When auditing, reporting on, or exploring codebases, report ONLY what ACTUALLY exists on disk today. Never assume or infer framework defaults. If code, routes, or configurations cannot be found, explicitly state "NOT FOUND" instead of guessing. For every claim, cite the exact relative file path and function/symbol/route name. Perform audits in read-only mode.
