# Update Rules Per File

Follow these strict semantics on every compaction pass. These rules prevent documentation from decaying into either a stale snapshot nobody trusts or an unmanageable log nobody reads.

---

## `dev_com_agent.md` — Universal Root Router & Ground Rules

**Principle:** Universal entry point for any autonomous agent entering the repository. Directs agents to `dev_md_guides/agent.md` and enforces progressive context disclosure and inviolable ground rules.

**Rules:**
1. Maintain at the repository root worktree.
2. Link directly to `dev_md_guides/agent.md` as the master index.
3. Establish the core ground rules: zero hardcoded directories/endpoints, zero credential exposure (with mandatory security warning protocol), and proactive compaction triggers.
4. Keep concise and structural. Never duplicate deep code details or historical logs.

**Size Limit:** ~40 lines.

---

## `dev_md_guides/agent.md` — Master Summary & Dynamic Inventory

**Principle:** Single source of indexation and progressive disclosure. Provides agents with an executive overview of all files in `dev_md_guides/` so they can load only relevant guides for their current task.

**Rules:**
1. Maintain 1–3 line executive summaries per guide in the Executive Summary Table.
2. Index dynamic topic guides (`commands.md`, `mcp.md`) with focus areas and spawning triggers.
3. Automatically maintain the Structural Documentation Inventory table (file, line count, category, status, last modified) via `run_compactor.py`.
4. Update executive summaries whenever a guide's scope or purpose shifts.

**Size Limit:** ~150 lines.

---

## `dev_md_guides/structure.md` — Regenerate Fully

**Principle:** This document's sole responsibility is "what exists where right now." There is no historical narrative to lose. Incrementally hand-patching directory structures across sessions inevitably leads to silent drift.

**Rules:**
1. Re-scan the project directory tree and top-level manifests.
2. Group files by module/folder and summarize architectural roles (e.g. gateway, domain model, persistent store).
3. Explicitly document main entry points (e.g., `main.py`, `server.ts`, `cli.py`, `Cargo.toml`).
4. Note discovered inter-module import relationships and dependency gates.
5. Reference environment endpoints and directory pointers via `dev_md_guides/directory.md`.
6. Reference credentials schema via `dev_md_guides/credentials.md.sample`.
7. Overwrite the file completely.

**Size Limit:** ~150 lines. If the tree exceeds this limit, summarize nested subdirectories in prose instead of listing every file path.

---

## `dev_md_guides/features.md` — Surgically Patch

**Principle:** `features.md` maintains status progression across tasks (`Planned` → `In Progress` → `Done` → `Removed`). Full regeneration from disk loses this state history.

**Rules:**
1. Always read existing `features.md` before applying edits.
2. Update the status and path pointers of any feature or sub-task touched during the active session.
3. For new capabilities, append a row under the matching status heading.
4. **Never delete a feature row** merely because it was untouched in the current session.
5. When a feature is intentionally deprecated or removed from code, move it to the `Removed` section with a session date rather than deleting it outright.

**Format:**
```markdown
- **Feature Name** — Concise capability description. Location: `path/to/module/`. Status: Done | In Progress | Planned.
```

**Size Limit:** ~250 lines. When exceeded, collapse older items in the `Removed` section into a single pointer to `changelog.md`.

---

## `dev_md_guides/branch.md` — Overwrite Fully

**Principle:** This file reflects the exact ephemeral state of the active Git branch and worktree. Its lifetime is tied to the current branch. Historical branch context belongs in `changelog.md` and `memory.md`, never here.

**Rules:**
1. Overwrite completely on each compaction run.
2. Record active branch name, tracking upstream, HEAD commit, and divergence.
3. Detail uncommitted working tree modifications (staged, unstaged, untracked).
4. Highlight current milestones, blockers, or required integration steps.

**Size Limit:** ~40 lines. If this file grows beyond 40 lines, historical narrative has leaked in and should be migrated to `changelog.md`.

---

## `dev_md_guides/memory.md` — Append-Only + Explicit Supersession

**Principle:** Captures durable architectural decisions (ADRs) and immutable system invariants. Routine bug fixes and failure modes are tracked in `gotchas.md`.

**Rules:**
1. Capture durable architecture decisions (ADRs), invariants, conventions, and rejected alternatives.
2. Append new ADRs with standard fields: Date, Status, Context, Decision, Consequences, Rejected Alternatives.
3. **Pruning Gate:** Only prune or replace an entry if an architectural decision is explicitly superseded. When superseding, note: `(supersedes decision from YYYY-MM-DD; see changelog)`. Never delete decisions silently.
4. Capture critical security invariants: zero credential exposure, gitignore rules for `credentials.md`, and mandatory user-warning protocol before committing any secrets.

**Size Limit:** ~300 lines. When approaching the threshold, re-read and tighten descriptions, merging related constraints while preserving core invariants.

---

## `dev_md_guides/gotchas.md` — Categorized Failure Modes & Fix Mechanics

**Principle:** Central repository for operational errors, fatal crashes, platform-specific bugs, and API quirks discovered during execution. Prevents agents and engineers from repeating identical debugging loops across sessions.

**Rules:**
1. Categorize entries by severity:
   - **Major Blockers**: Fatal crashes, data loss risks, blocking bugs, environment breakages, security vulnerabilities.
   - **Minor Quirks**: Silent defaults, formatting discrepancies, platform-specific edge cases, CLI quirks.
2. Adhere strictly to the **Resolution Anatomy**:
   - **Trigger / Symptom**: Concrete error message, command failure, or unintended symptom.
   - **Root Cause ("Why it failed")**: Technical explanation of why the failure occurred.
   - **Exact Fix**: The precise code, flag, or environment adjustment applied.
   - **Mechanics ("Why the fix worked")**: Why this solution succeeded and why it is resilient.
3. When a specific failure mode recurs 3+ times with deep nuances, extract it into a dynamic topic guide (e.g. `commands.md` or `mcp.md`).

**Size Limit:** ~300 lines. When approaching limit, consolidate related minor quirks or prune obsolete library versions.

---

## `dev_md_guides/flow.md` — Procedural Execution Recipes & Workflows

**Principle:** Tested, step-by-step procedural playbooks for multi-step tasks, tool-chain recipes, build sequences, and verification protocols.

**Rules:**
1. Structure each recipe with numbered steps and explicit shell/code blocks.
2. Include explicit verification criteria or post-conditions for each flow.
3. Maintain common operational pipelines:
   - Test & Quality Gate Execution Flow
   - Context Compaction & Living Documentation Sync Flow
   - Git Branching, Secret Safety & PR Update Flow
   - Deployment, Mirroring & Installation Sync Flow
4. If an operational recipe exceeds ~30 lines or focuses on a specialized domain, extract it into a dedicated dynamic topic guide.

**Size Limit:** ~250 lines.

---

## `dev_md_guides/changelog.md` — Append-Only, Reverse Chronological

**Principle:** The deterministic ground truth of operational session history. Every other document can be reconstructed or reconciled against this audit trail. Past entries must never be edited, deleted, or reordered.

**Rules:**
1. Prepend or append new timestamped entries for each operational run (newest first).
2. Record trigger event, active branch, HEAD commit, AST code modifications (modified functions, classes, line numbers), and executed terminal commands with exit codes.
3. Reference `memory.md` for architectural reasoning and `gotchas.md` for error resolution rather than duplicating verbose discussion.
4. Never log unredacted secret values or live credentials into changelog entries.

**Size Limit & Archiving:** When the file exceeds ~500 lines, extract entries older than the latest milestone into `dev_md_guides/archive/changelog-<date-range>.md` and leave a one-line link at the bottom. Never delete historical entries.

---

## `dev_md_guides/directory.md` & `dev_md_guides/directory.md.sample` — Centralized Catalog & Sample Template

**Principle:** Documentation and agents must never hardcode machine-specific paths, private IPs, backend links, frontend links, or server URLs directly into `structure.md`, `branch.md`, `memory.md`, or codebase markdown. Hardcoding breaks cross-machine portability and risks leaking private network topology to GitHub.

**Rules:**
1. Maintain `directory.md.sample` in Git as the canonical schema and current example template containing sanitized placeholders (e.g. `http://localhost:3000`, `http://localhost:8000`, `./data`).
2. The actual runtime `directory.md` is populated locally (seeded from `directory.md.sample` if missing) and added to `.gitignore`.
3. All other guides (`structure.md`, `memory.md`, `features.md`) must refer to services and directories by logical alias or relative reference defined in `directory.md`.
4. When new services, ports, or directory aliases are added to the project, update both `directory.md` and `directory.md.sample` with a sanitized example.
5. Never commit private credentials, auth tokens, internal IPs, or machine-specific absolute directories to GitHub.

**Size Limit:** ~100 lines.

---

## `dev_md_guides/credentials.md` & `dev_md_guides/credentials.md.sample` — Centralized Secrets Catalog & Security Protocol

**Principle:** Live credentials, API tokens, database connection strings, private encryption keys, and service secrets must NEVER be committed to Git or pushed to GitHub. Leaking secrets into version control causes critical infrastructure vulnerability, immediate compromise by automated crawlers, and irreversible git tree pollution.

**Rules:**
1. Maintain `credentials.md.sample` in Git containing sanitized, mock placeholders (e.g., `ENC[...]`, `sk-ant-api03-SAMPLE_PLACEHOLDER_KEY`, `postgresql://postgres:REDACTED@localhost:5432/app_db`).
2. The active runtime `credentials.md` is kept strictly local on the developer's machine and MUST be added to `.gitignore`.
3. **Mandatory User Warning Protocol**: If the user ever requests, instructs, or specifies committing `credentials.md` or any live secrets to git/GitHub, the agent MUST NOT comply immediately. The agent MUST first issue an explicit, high-visibility security warning detailing:
   - Severe security consequences: unauthorized database/cloud access, data theft, credential invalidation.
   - Permanence of git history: commits remain reachable in git packfiles even after deletion.
   - Requirement for explicit user confirmation before any `git add` or `git commit` involving credentials can proceed.
4. Run the deterministic credential scanner (`run_compactor.py`) on living guides to catch accidental secret exposure before pushing.
5. Never log unredacted secret values in `changelog.md` or output them to standard execution logs.

**Size Limit:** ~100 lines.

---

## Dynamic Topic Guides (e.g. `commands.md`, `mcp.md`) — Spawning & Lifecycle

**Principle:** Provide specialized operational depth for recurring tool domains without bloating core guide files beyond their size budgets.

**Rules:**
1. **Spawning Heuristic**: Create a dynamic topic guide when a tool, command, or service recurs 3+ times with distinct nuances, or when a subsection in `gotchas.md` or `flow.md` grows beyond ~30 lines.
2. Register the dynamic guide in `dev_md_guides/agent.md` under Dynamic Topic Guides and update the structural inventory.
3. Structure with purpose, catalog table, exact invocation syntax, and known quirks.
4. Prune or merge dynamic guides if the underlying technology is deprecated from the project.

**Size Limit:** ~150 lines per dynamic guide.
