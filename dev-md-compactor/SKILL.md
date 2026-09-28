---
name: dev-md-compactor
description: Compacts the ongoing coding session, conversational state, AST code modifications, and git changes into a persistent dev_md_guides/ folder of living Markdown docs (dev_com_agent.md, agent.md, branch.md, features.md, structure.md, memory.md, gotchas.md, flow.md, changelog.md, directory.md.sample, credentials.md.sample). Use whenever the user asks to "compact memory", "save session state", "update dev guides", "compact context", "save our progress", "sync memory", "update docs", or when concluding a substantial engineering task or approaching context token limits.
---

# Dev MD Compactor

Turns an interactive coding session into durable, structured repository memory instead of ephemeral chat buffer or raw diff dumps. Produces and maintains deterministic files in a `dev_md_guides/` folder at the project root:

- **`dev_com_agent.md`** — universal root entry point and context router directing agents to `agent.md` and establishing inviolable ground rules (at project root)
- **`dev_md_guides/agent.md`** — executive master summary table, progressive disclosure router, and structural inventory of all living guides
- **`dev_md_guides/branch.md`** — active branch worktree, upstream tracking, divergence, and uncommitted diffs (overwritten each run)
- **`dev_md_guides/features.md`** — specification-driven development (SDD) status matrix (surgically patched)
- **`dev_md_guides/structure.md`** — repository topology, module roles, entry points, and dependency graph (regenerated from tree & AST)
- **`dev_md_guides/memory.md`** — durable architectural invariants, ADRs, trade-offs, and design conventions (append-only with explicit supersession)
- **`dev_md_guides/gotchas.md`** — categorized operational failures, non-obvious runtime bugs, root causes, exact fixes, and fix mechanics (Major Blockers vs. Minor Quirks)
- **`dev_md_guides/flow.md`** — procedural execution workflows, testing sequences, context compaction protocols, and git release pipelines
- **`dev_md_guides/changelog.md`** — chronological, append-only audit trail of operational runs, modified AST symbols, and test/build outcomes (append-only)
- **`dev_md_guides/directory.md` & `directory.md.sample`** — environment catalog for project directories, servers, backend links, frontend links, and ports. All other markdown guides rely on this catalog instead of hardcoding paths or URLs. Only `directory.md.sample` is committed to GitHub with sanitized current examples; `directory.md` stays gitignored for active machine/environment values.
- **`dev_md_guides/credentials.md` & `credentials.md.sample`** — credentials and secrets reference. Real secrets remain strictly local in gitignored `credentials.md`; only sanitized `credentials.md.sample` with mock placeholders is committed to GitHub. Never commit credentials to GitHub; if the user ever specifies doing so, the agent MUST first explicitly warn the user about critical security risks.
- **Dynamic Topic Guides** (e.g. `commands.md`, `mcp.md`) — spawned dynamically when recurring tool invocations, commands, or MCP services accumulate 3+ occurrences with specific quirks.

## Core Architectural Rules

1. **Progressive Context Disclosure**:
   - New agents entering the repository read [`dev_com_agent.md`](../dev_com_agent.md) at root, then inspect [`dev_md_guides/agent.md`](agent.md) to locate relevant guides. Never dump all markdown files into prompt context at once.
2. **Strictly bifurcate current-state files from historical files:**
   - *Current-state files* (`branch.md`, `structure.md`, `features.md`, `agent.md`) can be safely regenerated or patched from repository truth. If they drift, rebuild them directly from the codebase.
   - *Historical files* (`changelog.md`) must NEVER be rewritten, reordered, or summarized away. Only append new dated entries.
   - *Durable decision memory* (`memory.md`) is protected against lossy summarization. It captures the "why", invariants, and rejected alternatives. Pruning is permitted only when an earlier decision is explicitly superseded.
   - *Error & Flow separation*: Failure modes belong in `gotchas.md` (not lost in chat or buried in `memory.md`); procedural execution sequences belong in `flow.md`.
3. **Zero Hardcoded Directories & Endpoints:**
   - Never hardcode local filesystem paths, internal server IPs, backend API URLs, or frontend URLs across any markdown files. All markdown guides and agent prompts must rely on `directory.md`. Only `directory.md.sample` is deployed/committed to GitHub with current example values.
4. **Zero Credential Exposure & User Warning Protocol:**
   - Real credentials, private keys, database passwords, and API tokens must NEVER be committed to GitHub or exposed in git-tracked living guides. Active secrets reside exclusively in `credentials.md` (which MUST be gitignored). Only sanitized `credentials.md.sample` is committed.
   - If the user ever specifies or requests committing `credentials.md` or any unredacted secrets to git/GitHub, the agent MUST NEVER execute this action without first explicitly warning the user about the critical security risks (credential theft, permanent git history pollution, unauthorized cloud access, data compromise) and requiring explicit user confirmation.

---

## When to Trigger

1. **User Explicit Request**: The user says "compact", "save progress", "update docs", "sync memory", "write changelog", or invokes `/compact-docs`.
2. **Context Saturation Boundary**: When approaching context token limits (~60–80% utilization) or prior to a manual or automated context compaction event.
3. **Task Completion Boundary**: Proactively at the conclusion of any non-trivial coding task (multiple files touched, feature delivered, bug root-caused, refactoring finished). Treat documentation compaction like committing code: never leave a completed task uncompacted.

Do **NOT** trigger for trivial one-off edits (e.g., fixing a typo, renaming a single variable) unless explicitly asked.

---

## Execution Protocol

### Phase 0: Ground-Truth Gathering

Execute the deterministic extraction engine against the project root:

```bash
# Cross-platform Python extraction (recommended)
python dev-md-compactor/scripts/run_compactor.py

# Alternatively, in shell environments:
bash dev-md-compactor/scripts/gather_context.sh .
```

This inspects:
- Git status, branch name, HEAD hash, tracking upstream, and recent commit log.
- Uncommitted hunks and modified files.
- Python AST function and class signatures for changed files.
- Directory topography and inter-module import dependencies.
- Project manifest files (`pyproject.toml`, `package.json`, `Cargo.toml`, `go.mod`, etc.).
- Active directory catalog (`directory.md` / `directory.md.sample`).
- Credential leak detection across git-tracked living guides.

If `dev_md_guides/` does not exist yet at the project root:
- The script automatically seeds all files from `dev-md-compactor/templates/` (including `dev_com_agent.md`, `agent.md`, `gotchas.md`, and `flow.md`).
- If running manually, copy all templates from `templates/` to `dev_md_guides/`.

If `dev_md_guides/` already exists:
- Read `agent.md` first, then inspect targeted guide files before making changes. Never blind-overwrite.
- Note line counts. If any file approaches its size threshold (see `references/update-rules.md`), archive or tighten per specifications.

---

### Phase 1: Reconstruct Session Delta & Conversational Reflection

Review recent conversation turns, executed commands, tool failures, and the gathered extraction report to assemble an operational ledger:

1. **Code Mutations**: Files added, modified, deleted, and specific functions/classes touched (captured from AST diff).
2. **Feature States**: What feature or sub-task was moved forward, completed, or unblocked (routes to `features.md`).
3. **Architectural Decisions (ADRs)**: Framework migrations, dependency additions, protocol changes, and trade-offs (routes to `memory.md`).
4. **Conversational Reflection Protocol**:
   - **What Worked**: Identify verified tool chains, commands, and procedural flows that succeeded; capture them in `flow.md`.
   - **What Failed & Why**: Review errors, command non-zero exits, and API quirks. Document each failure mode in `gotchas.md` with full resolution anatomy:
     * *Trigger / Symptom*: Stack trace, error message, or unintended behavior.
     * *Root Cause*: Exactly why the underlying library, tool, or runtime failed.
     * *Exact Fix*: Code change or parameter correction applied.
     * *Mechanics*: Why this fix resolved the issue and why it won't recur.
   - **Heuristic Dynamic Topic Spawning**:
     * When a specific CLI tool, command chain, or MCP server recurs **3+ times** with non-trivial quirks, spawn a dedicated topic guide (e.g. `commands.md` or `mcp.md`).
     * When a section in `flow.md` or `gotchas.md` exceeds **~30 lines**, extract it into a dynamic topic guide and link it in `agent.md`.
5. **Master Index Sync**: Update `dev_md_guides/agent.md` summary rows to reflect newly added or updated knowledge.

---

### Phase 2: Apply Per-File Update Rules

Follow `references/update-rules.md` and `references/file-formats.md` strictly:

| File | Operation | Size Cap | Target Content |
|---|---|---|---|
| `dev_com_agent.md` | **Seed + Router Sync** | ~40 lines | Universal root router directing agents to `agent.md` and core invariants. |
| `dev_md_guides/agent.md` | **Surgical / Auto-Sync** | ~150 lines | Master summary table, dynamic topic index, and auto-generated file inventory. |
| `dev_md_guides/structure.md` | **Regenerate fully** | ~150 lines | Folder purpose, key entry points, architectural boundaries, and discovered dependency links. |
| `dev_md_guides/features.md` | **Surgical Patch** | ~250 lines | Keep status current (Done / In Progress / Planned / Removed). Never delete an unmentioned feature row. |
| `dev_md_guides/branch.md` | **Overwrite fully** | ~40 lines | Active branch, current milestone, status (in progress / blocked / ready), uncommitted diffs, and blockers. |
| `dev_md_guides/memory.md` | **Append + Prune** | ~300 lines | ADR entries (context, decision, consequences, rejected alternatives) and immutable system invariants. Prune only if superseded. |
| `dev_md_guides/gotchas.md` | **Append + Categorize**| ~300 lines | Major Blockers vs. Minor Quirks, root cause analysis, exact fixes, and fix mechanics. |
| `dev_md_guides/flow.md` | **Append + Maintain** | ~250 lines | Procedural execution recipes, pipeline workflows, test sequences, and verification checklists. |
| `dev_md_guides/changelog.md` | **Append-only** | ~500 lines | Prepend new timestamped session audit with AST modifications and command results. Archive older entries when limit exceeded. |
| `dev_md_guides/directory.md.sample` (and `directory.md`) | **Seed + Local Maintain** | ~100 lines | Workspace paths, servers, backend/frontend links, ports. Only `directory.md.sample` is committed to GitHub. |
| `dev_md_guides/credentials.md.sample` (and `credentials.md`) | **Seed + Local Maintain** | ~100 lines | Sanitized credentials schema. Only `credentials.md.sample` is committed to GitHub. Real secrets stay local in `credentials.md`. |
| Dynamic Topics (`commands.md`, `mcp.md`) | **Create when triggered** | ~150 lines | In-depth operational reference for recurring commands or MCP integrations. |

---

### Phase 3: Cross-Link and Verify

- Ensure `dev_com_agent.md` links correctly to `dev_md_guides/agent.md`.
- Ensure every living guide is represented with an executive summary in `dev_md_guides/agent.md`.
- Ensure every active feature in `features.md` maps to a physical directory or module documented in `structure.md`.
- Ensure decision entries in `changelog.md` reference corresponding ADR entries in `memory.md` rather than duplicating long rationale.
- Ensure failure resolutions in `changelog.md` point to entries in `gotchas.md`.
- Ensure markdown guides reference services and directories via `directory.md` instead of hardcoding raw paths, IPs, or ports.
- Verify that both `dev_md_guides/directory.md` and `dev_md_guides/credentials.md` are ignored in `.gitignore`, and only `*.sample` files are tracked.
- Run the credential leak scanner to verify zero unredacted secrets exist in tracked files.
- Validate that all markdown headers adhere to `references/file-formats.md`.
- Ensure line count limits are respected.

---

### Phase 4: Report and Rehydrate

1. **Terse Chat Report**: Provide a concise 3–5 line summary of what was written and updated. Do not dump the full file contents into the chat.
2. **Context Rehydration**:
   - In subsequent sessions or after a context reset, start at [`dev_com_agent.md`](../dev_com_agent.md), read [`dev_md_guides/agent.md`](agent.md), then read targeted guides (`branch.md`, `gotchas.md`, `flow.md`, `features.md`) to rehydrate state and resume execution.
   - For architectural tasks, consult `dev_md_guides/memory.md` to guarantee alignment with immutable project invariants.
   - When resolving local paths, backend APIs, or frontend dev servers, consult `dev_md_guides/directory.md`.
   - For secret requirements and auth configurations, reference `dev_md_guides/credentials.md.sample` for schema and local `dev_md_guides/credentials.md` for active values.

---

## Skill Assets

- `scripts/run_compactor.py`: Deterministic Python extraction engine with secret leak scanner, dynamic guide discovery, and gitignore guard.
- `scripts/gather_context.sh`: Shell extraction script with credential tracking audit and agent index reporting.
- `references/update-rules.md`: Complete update semantics, size boundaries, credential security rules, and archiving procedures per file.
- `references/file-formats.md`: Required markdown section structures for all guide files (including `dev_com_agent.md`, `agent.md`, `gotchas.md`, `flow.md`, `commands.md`, `mcp.md`).
- `templates/*.md`: Starting skeletons for `dev_com_agent.md`, `agent.md`, `branch.md`, `features.md`, `structure.md`, `memory.md`, `gotchas.md`, `flow.md`, `commands.md`, `mcp.md`, `changelog.md`, `directory.md.sample`, `directory.md`, `credentials.md.sample`, `credentials.md`.

