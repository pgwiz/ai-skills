# Update Rules Per File

Follow these strict semantics on every compaction pass. These rules prevent documentation from decaying into either a stale snapshot nobody trusts or an unmanageable log nobody reads.

---

## `dev_md_guides/structure.md` — Regenerate Fully

**Principle:** This document's sole responsibility is "what exists where right now." There is no historical narrative to lose. Incrementally hand-patching directory structures across sessions inevitably leads to silent drift.

**Rules:**
1. Re-scan the project directory tree and top-level manifests.
2. Group files by module/folder and summarize architectural roles (e.g. gateway, domain model, persistent store).
3. Explicitly document main entry points (e.g., `main.py`, `server.ts`, `cli.py`, `Cargo.toml`).
4. Note discovered inter-module import relationships and dependency gates.
5. Overwrite the file completely.

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

**Principle:** Captures immutable architectural invariants, Architecture Decision Records (ADRs), non-obvious gotchas, and rejected alternatives. This is the highest-signal document for surviving context resets and preventing repeated errors.

**Rules:**
1. Capture durable rationale ("why we chose X over Y"), non-obvious runtime gotchas, and conventions not covered by linters.
2. **Do NOT log routine events** here (routine events belong in `changelog.md`).
3. Append new ADRs under their respective headers with standard fields: Date, Status, Context, Decision, Consequences, Rejected Alternatives.
4. **Pruning Gate:** Only prune or replace an entry if an architectural decision is explicitly superseded. When superseding, note: `(supersedes decision from YYYY-MM-DD; see changelog)`. Never delete decisions silently.

**Size Limit:** ~300 lines. When approaching the threshold, re-read and tighten descriptions, merging related constraints while preserving core invariants.

---

## `dev_md_guides/changelog.md` — Append-Only, Reverse Chronological

**Principle:** The deterministic ground truth of operational session history. Every other document can be reconstructed or reconciled against this audit trail. Past entries must never be edited, deleted, or reordered.

**Rules:**
1. Prepend or append new timestamped entries for each operational run (newest first).
2. Record trigger event, active branch, HEAD commit, AST code modifications (modified functions, classes, line numbers), and executed terminal commands with exit codes.
3. Reference `memory.md` for architectural reasoning rather than duplicating verbose discussion.

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

