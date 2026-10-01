# Procedural Execution Flows & Operational Recipes

_Standard execution workflows, tool-chain recipes, and step-by-step verification procedures._
_Maintained by the dev-md-compactor Conversational Reflection Protocol._

---

## 1. Test & Quality Gate Execution Flow

Follow this sequence to execute test suites and verify codebase integrity:

```bash
# Step 1: Run comprehensive test discovery
python -m unittest discover tests

# Step 2: Run specific compactor tests with verbosity
python -m unittest tests/test_compactor.py -v

# Step 3: Verify zero unhandled exceptions and 100% pass rate
```

- **Verification Criteria**:
  - All test methods report `ok`.
  - Zero warnings of secret leaks or malformed gitignore entries.
  - Total elapsed time typically under 5 seconds.

---

## 2. Context Compaction & Living Documentation Sync Flow

Execute when concluding a coding task or before context resets:

```bash
# Step 1: Preview ground truth state without writing files
python dev-md-compactor/scripts/run_compactor.py --report-only

# Step 2: Run deterministic compactor to synchronize dev_md_guides/
python dev-md-compactor/scripts/run_compactor.py

# Step 3: Run bash extractor to verify cross-platform parity (in bash environments)
bash dev-md-compactor/scripts/gather_context.sh .

# Step 4: Verify secret scanner output reports zero leaks in tracked guides
```

- **Post-Compaction Checklist**:
  - `branch.md` reflects current HEAD commit and working tree state.
  - `structure.md` reflects latest modules and manifest files.
  - `changelog.md` contains the new timestamped operational session record.
  - `agent.md` inventory reflects current line counts and modified dates.
  - `gotchas.md` contains entries for any blockers encountered during the session.

---

## 3. Git Branching, Secret Safety & PR Update Flow

```bash
# Step 1: Check git status and ensure working tree is organized
git status

# Step 2: Verify dev_md_guides/credentials.md is NOT tracked in git index
git ls-files dev_md_guides/credentials.md
# (Output must be empty. If tracked, immediately run: git rm --cached dev_md_guides/credentials.md)

# Step 3: Run secret scanner to prevent accidental leaks
python dev-md-compactor/scripts/run_compactor.py --report-only

# Step 4: Stage modified and new files (excluding credentials.md and directory.md)
git add dev_com_agent.md GEMINI.md README.md dev-md-compactor/ dev_md_guides/ tests/

# Step 5: Commit changes using conventional commit style
git commit -m "feat(dev-md-compactor): expand agent knowledge architecture with dev_com_agent.md, agent.md, gotchas.md, and flow.md"

# Step 6: Push to active branch and verify PR status
git push origin feat/dev-md-compactor
gh pr view 2
```

---

## 4. Multi-Skill Mirroring & Deployment Flow

When modifying core skills (`dev-md-compactor`, `agent-memory`), propagate changes to project mirrors and global user installations using the universal installer:

```bash
# Windows (PowerShell) - Update all skills for Google Antigravity:
.\install\install.ps1 -Target antigravity -Skill all -Yes

# POSIX (macOS/Linux/WSL) - Update all skills for Google Antigravity:
./install/install.sh --target antigravity --skill all -y

# Verify synchronization to global user Antigravity directory:
# ~/.gemini/config/skills/dev-md-compactor/
# ~/.gemini/config/skills/agent-memory/
# ~/agent-system/.agent-config

# Run test suite to verify all locations pass:
python -m unittest discover tests
```

---

## 5. Codebase Audit & Anti-Hallucination Inspection Flow

Follow this protocol when auditing or inspecting an existing codebase to prevent model hallucinations:

1. **Non-Mutative Discovery**:
   - Inspect existing manifests, directories, and route files via read-only tools (`find`, `git status`, `grep`).
   - Touch zero source files; stage zero commits; execute zero mutative commands.
2. **Ground-Truth Source Verification**:
   - For every feature, route, or model investigated, locate the physical file on disk.
   - Extract the exact file path and function/symbol definition (e.g. `src/services/order.ts#createOrder`).
3. **Negative Evidence Assertion ("NOT FOUND")**:
   - If an endpoint, helper, or configuration does not exist in code, explicitly report **`NOT FOUND`**.
   - Never speculate, invent boilerplate, or assume framework defaults exist.
4. **Structured Grounded Reporting**:
   - Present every finding with exact citations:
     - **Confirmed Active**: `[Capability]` → `path/to/file.ext#function_or_route`
     - **Missing / Unimplemented**: `[Capability]` → `NOT FOUND`

