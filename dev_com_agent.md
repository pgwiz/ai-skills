# Universal Agent Entry Point & Context Router (`dev_com_agent.md`)

> **Single Source of Agent Entry & Context Routing**
> Welcome, Agent. Before executing commands or inspecting arbitrary code files, follow this progressive context disclosure protocol to understand repository ground truths, architectural invariants, and operational workflows.

---

## 1. Master Context Router

Do **not** read every markdown guide in `dev_md_guides/` at once. Follow **progressive disclosure**:

1. **Step 1: Read the Master Index**
   - Read [`dev_md_guides/agent.md`](dev_md_guides/agent.md) first.
   - It provides an executive summary of all active guide files, line counts, and operational roles so you only load what you need.

2. **Step 2: Read Targeted Guides Based on Your Current Task**
   - **Branch / Worktree State**: [`dev_md_guides/branch.md`](dev_md_guides/branch.md) (active branch, uncommitted diffs, upstream divergence).
   - **Feature Tracking**: [`dev_md_guides/features.md`](dev_md_guides/features.md) (SDD status matrix: Done / In Progress / Planned).
   - **Code Architecture**: [`dev_md_guides/structure.md`](dev_md_guides/structure.md) (module topography, entry points, dependency graph).
   - **Decisions & Invariants**: [`dev_md_guides/memory.md`](dev_md_guides/memory.md) (Architecture Decision Records [ADRs], immutable project invariants).
   - **Failure Analysis & Fixes**: [`dev_md_guides/gotchas.md`](dev_md_guides/gotchas.md) (Major blockers, minor quirks, root causes, exact fixes, and mechanics).
   - **Execution Workflows**: [`dev_md_guides/flow.md`](dev_md_guides/flow.md) (Multi-step build/test/release execution pipelines and operational recipes).
   - **Environment Endpoints**: [`dev_md_guides/directory.md`](dev_md_guides/directory.md) (local workspace paths, servers, backend links, frontend links, ports).
   - **Secrets & Credentials**: [`dev_md_guides/credentials.md.sample`](dev_md_guides/credentials.md.sample) (sanitized secrets schema) and local [`dev_md_guides/credentials.md`](dev_md_guides/credentials.md) (gitignored).
   - **Operational Audit Log**: [`dev_md_guides/changelog.md`](dev_md_guides/changelog.md) (append-only timestamped history of compaction runs and AST symbol modifications).
   - **Dynamic Topic Guides**: Inspect [`dev_md_guides/agent.md`](dev_md_guides/agent.md) for dynamic topic guides (e.g. `commands.md`, `mcp.md`).

---

## 2. Inviolable Core Ground Rules

1. **Zero Hardcoded Directories & Endpoints**
   - Never hardcode filesystem paths, server hostnames, backend API links, or frontend URLs across markdown files.
   - Always resolve and document them via [`dev_md_guides/directory.md`](dev_md_guides/directory.md). Only [`directory.md.sample`](dev_md_guides/directory.md.sample) with sanitized example keys is committed to version control.

2. **Zero Credential Exposure & Mandatory Warning Protocol**
   - Never commit real credentials, API keys, private tokens, or passwords to git/GitHub.
   - Active secrets reside exclusively in local [`dev_md_guides/credentials.md`](dev_md_guides/credentials.md), which must always be gitignored.
   - Only [`dev_md_guides/credentials.md.sample`](dev_md_guides/credentials.md.sample) with sanitized mock placeholders is tracked in version control.
   - **MANDATORY WARNING PROTOCOL**: If any user prompt requests or implies committing credentials or `credentials.md`, you MUST NOT proceed without issuing an explicit, high-visibility security warning detailing the severe risks of credential exposure and obtaining explicit user confirmation.

3. **Proactive Context Compaction Triggers**
   - **Task Completion Boundary**: Automatically trigger context compaction whenever a non-trivial engineering task concludes (multiple files touched, feature delivered, bug fixed, refactor completed). Do not wait for user prompts.
   - **Context Token Saturation**: Proactively compact when approaching context limits (~60–80% utilization) to persist state into living guides.
   - **Execution Command**: Run `python dev-md-compactor/scripts/run_compactor.py` (or `bash dev-md-compactor/scripts/gather_context.sh .`).

---

## 3. Conversational Reflection & Operational Knowledge Capture

When concluding tasks:
- **Record Errors in `gotchas.md`**: Capture the symptom, root cause ("why it failed"), exact fix, and mechanics ("why the fix worked").
- **Record Multi-Step Pipelines in `flow.md`**: Record verified command chains, testing sequences, or build flows.
- **Dynamic Topic Spawning**: When a tool, command, or MCP integration recurs 3+ times with unique quirks, create a dedicated guide (e.g., `commands.md`, `mcp.md`) and register it in `agent.md`.
