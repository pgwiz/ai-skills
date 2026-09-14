# Project Agent Instructions

## Session Memory & Context Compaction

This project uses the **dev-md-compactor** skill (`dev-md-compactor/SKILL.md` or `.agent/skills/dev-md-compactor/SKILL.md`) to persist project state across sessions into a `dev_md_guides/` directory at the project root:

- `dev_md_guides/branch.md` — active branch worktree, upstream tracking, divergence, and uncommitted diffs
- `dev_md_guides/features.md` — capabilities matrix and Spec-Driven Development (SDD) statuses
- `dev_md_guides/structure.md` — codebase topology, entry points, and module dependency graph
- `dev_md_guides/memory.md` — durable architecture decisions (ADRs), system invariants, conventions, and gotchas
- `dev_md_guides/changelog.md` — reverse-chronological, append-only operational audit log
- `dev_md_guides/directory.md` & `directory.md.sample` — environment catalog for directories, servers, backend/frontend links, and ports (deploy sample only)
- `dev_md_guides/credentials.md` & `credentials.md.sample` — credentials and secrets reference (deploy sample only with mock placeholders; real secrets stay strictly local and gitignored)

### Proactive Trigger Protocol
- **Trigger automatically** whenever a non-trivial engineering task wraps up (multiple files modified, a feature delivered, a refactor concluded, or a bug root-caused) — do not wait to be asked.
- It can also be invoked explicitly with `/compact-docs` or when the user asks to "compact memory", "save progress", or "update dev guides".

### Rehydration & Security Rules
- Before starting any non-trivial coding task, read `dev_md_guides/branch.md` and `dev_md_guides/memory.md` first if they exist — they contain project ground truths and invariants that cannot be recovered by reading code alone.
- Never hardcode directory paths, server IPs, backend URLs, or frontend URLs across markdown files; rely on `dev_md_guides/directory.md`.
- **Zero Credential Exposure**: NEVER commit real credentials, API tokens, private keys, or passwords to git/GitHub. Keep `dev_md_guides/credentials.md` strictly local and gitignored.
- **Mandatory Agent Warning Protocol**: If the user ever specifies or instructs committing credentials or `credentials.md` to version control, the agent MUST NOT proceed without first issuing an explicit, high-visibility security warning detailing the severe risks of secret exposure and requiring explicit user confirmation.
