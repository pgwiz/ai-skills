---
name: dev-md-compactor
description: Compacts the ongoing coding session, conversational state, AST code modifications, and git changes into a persistent dev_md_guides/ folder of living Markdown docs (branch.md, features.md, structure.md, memory.md, changelog.md, directory.md.sample). Use whenever the user asks to "compact memory", "save session state", "update dev guides", "compact context", "save our progress", "sync memory", "update docs", or when concluding a substantial engineering task or approaching context token limits.
---

# Dev MD Compactor

Turns an interactive coding session into durable, structured repository memory instead of ephemeral chat buffer or raw diff dumps. Produces and maintains deterministic files in a `dev_md_guides/` folder at the project root:

- **branch.md** — what the active branch/session is doing right now (overwritten each run)
- **features.md** — specification-driven development (SDD) status matrix (surgically patched)
- **structure.md** — repository topology, module roles, entry points, and dependency graph (regenerated from tree & AST)
- **memory.md** — durable architectural invariants, ADRs, trade-offs, and non-obvious gotchas (append-only with explicit supersession)
- **changelog.md** — chronological, append-only audit trail of operational runs, modified AST symbols, and test/build outcomes (append-only)
- **directory.md** & **directory.md.sample** — environment catalog for project directories, servers, backend links, frontend links, and ports. All other markdown guides rely on this catalog instead of hardcoding paths or URLs. Only `directory.md.sample` is committed to GitHub with sanitized current examples; `directory.md` stays gitignored for active machine/environment values.

## Core Architectural Rules

1. **Strictly bifurcate current-state files from historical files:**
   - *Current-state files* (`branch.md`, `structure.md`, `features.md`) can be safely regenerated or patched from repository truth. If they drift, rebuild them directly from the codebase.
   - *Historical files* (`changelog.md`) must NEVER be rewritten, reordered, or summarized away. Only append new dated entries.
   - *Durable decision memory* (`memory.md`) is protected against lossy summarization. It captures the "why", invariants, and rejected alternatives. Pruning is permitted only when an earlier decision is explicitly superseded.
2. **Zero Hardcoded Directories & Endpoints:**
   - Never hardcode local filesystem paths, internal server IPs, backend API URLs, or frontend URLs across any markdown files. All markdown guides and agent prompts must rely on `directory.md`. Only `directory.md.sample` is deployed/committed to GitHub with current example values.


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

If `dev_md_guides/` does not exist yet at the project root:
- The script automatically seeds the files from `dev-md-compactor/templates/`.
- If running manually, copy all templates from `templates/` to `dev_md_guides/`.

If `dev_md_guides/` already exists:
- Read every existing guide file before making changes. Never blind-overwrite.
- Note line counts. If any file approaches its size threshold (see `references/update-rules.md`), archive or tighten per specifications.

---

### Phase 1: Reconstruct Session Delta

From conversational context, tool executions, and the gathered extraction report, assemble a mental ledger of:
1. **Code Mutations**: Files added, modified, deleted, and specific functions/classes touched.
2. **Feature States**: What feature or sub-task was moved forward, completed, or unblocked.
3. **Architectural Decisions (ADRs)**: Framework migrations, dependency additions, protocol changes, and trade-offs.
4. **Discovered Gotchas & Invariants**: Silent API behaviors, edge cases, test requirements, environment constraints.
5. **Execution Verification**: Exact test commands executed, build results, and exit codes.

---

### Phase 2: Apply Per-File Update Rules

Follow `references/update-rules.md` and `references/file-formats.md` strictly:

| File | Operation | Size Cap | Target Content |
|---|---|---|---|
| `dev_md_guides/structure.md` | **Regenerate fully** | ~150 lines | Folder purpose, key entry points, architectural boundaries, and discovered dependency links. |
| `dev_md_guides/features.md` | **Surgical Patch** | ~250 lines | Keep status current (Done / In Progress / Planned / Removed). Never delete an unmentioned feature row. |
| `dev_md_guides/branch.md` | **Overwrite fully** | ~40 lines | Active branch, current milestone, status (in progress / blocked / ready), uncommitted diffs, and blockers. |
| `dev_md_guides/memory.md` | **Append + Prune** | ~300 lines | ADR entries (context, decision, consequences, rejected alternatives), invariants, and gotchas. Prune only if superseded. |
| `dev_md_guides/changelog.md` | **Append-only** | ~500 lines | Prepend or append new timestamped session audit with AST modifications and command results. Archive older entries when limit exceeded. |
| `dev_md_guides/directory.md.sample` (and `directory.md`) | **Seed + Local Maintain** | ~100 lines | Workspace paths, servers, backend/frontend links, ports. Only `directory.md.sample` is committed to GitHub. |

---

### Phase 3: Cross-Link and Verify

- Ensure every active feature in `features.md` maps to a physical directory or module documented in `structure.md`.
- Ensure decision entries in `changelog.md` reference corresponding ADR entries in `memory.md` rather than duplicating long rationale.
- Ensure markdown guides reference services and directories via `directory.md` instead of hardcoding raw paths, IPs, or ports.
- Verify that `dev_md_guides/directory.md` is ignored in `.gitignore` and only `dev_md_guides/directory.md.sample` is staged for version control.
- Validate that all markdown headers adhere to `references/file-formats.md`.
- Ensure line count limits are respected.

---

### Phase 4: Report and Rehydrate

1. **Terse Chat Report**: Provide a concise 3–5 line summary of what was written and updated. Do not dump the full file contents into the chat.
2. **Context Rehydration**:
   - In subsequent sessions or after a context reset, immediately read `dev_md_guides/branch.md` and `dev_md_guides/features.md` to rehydrate state and resume execution without loss of momentum.
   - For architectural tasks, consult `dev_md_guides/memory.md` to guarantee alignment with immutable project invariants.
   - When resolving local paths, backend APIs, or frontend dev servers, consult `dev_md_guides/directory.md`.

---

## Skill Assets

- `scripts/run_compactor.py`: Deterministic Python extraction engine (stdlib: ast, subprocess, pathlib).
- `scripts/gather_context.sh`: Shell extraction script for bash-native environments.
- `references/update-rules.md`: Complete update semantics, size boundaries, and archiving procedures per file.
- `references/file-formats.md`: Required markdown section structures for all guide files (including `directory.md.sample` and `directory.md`).
- `templates/*.md`: Starting skeletons for `branch.md`, `features.md`, `structure.md`, `memory.md`, `changelog.md`, `directory.md.sample`, `directory.md`.
