# Codebase Architecture & Directory Dependency Graph
_Last regenerated: 2026-10-01 15:43:54 UTC by dev-md-compactor_

## Project Manifests & Build Tools
- *(No standard build manifests detected at root)*

## Module Directory Topography

### `agent-memory/`
- **Files (1)**: `SKILL.md`

### `agent-memory/references/`
- **Files (6)**: `AGENT_BOOTSTRAP.md, CONVENTIONS.md, GLOBAL_PROTOCOL.md, GLOBAL_WARNINGS.md, README.md, SESSION_START.md`

### `dev-md-compactor/`
- **Files (1)**: `SKILL.md`

### `dev-md-compactor/references/`
- **Files (2)**: `file-formats.md, update-rules.md`

### `dev-md-compactor/scripts/`
- **Files (2)**: `gather_context.sh, run_compactor.py`
- **Discovered Module Dependencies**: `argparse, ast, datetime, os, pathlib, re, subprocess, sys`

### `dev-md-compactor/templates/`
- **Files (15)**: `agent.md, branch.md, changelog.md, commands.md, credentials.md, credentials.md.sample, dev_com_agent.md, directory.md` (+7 more)

### `install/`
- **Files (3)**: `INSTALL.md, install.ps1, install.sh`

### `research/`
- **Files (2)**: `Agent Memory Compaction Research.docx, Agent Memory Compaction Research.md`

### `root/`
- **Files (8)**: `CODE_OF_CONDUCT.md, GEMINI.md, INSTALL_PLAN_v2.md, MARKETPLACE.md, README.md, SECURITY.md, dev_com_agent.md, verification_request.md`

### `tests/`
- **Files (1)**: `test_compactor.py`
- **Discovered Module Dependencies**: `io, pathlib, re, run_compactor, shutil, subprocess, sys, tempfile, unittest`

## Environment & Directory Catalog Reference
- Central Catalog: `dev_md_guides/directory.md` (sample committed as `dev_md_guides/directory.md.sample`).
- All workspace paths, servers, backend links, frontend links, and external endpoints are centralized in this catalog.
- Invariant: Never hardcode local filesystem paths or network URLs directly across project markdown files.

## Credentials & Secrets Reference
- Central Secrets Schema: `dev_md_guides/credentials.md` (sample committed as `dev_md_guides/credentials.md.sample`).
- Real secrets and sensitive tokens are kept strictly local in `credentials.md` and MUST NEVER be committed to GitHub.
- Invariant: Never commit credentials to GitHub; if the user ever specifies committing credentials, the agent must first explicitly warn the user about critical security risks.

## Architectural Invariants & Boundary Rules
- Internal modules should adhere to defined dependency boundaries without cyclic imports.
- Configuration, secrets, and environment overrides must not be hardcoded in application logic.
- Zero Hardcoded Endpoints: Do not hardcode machine directories, server IPs, backend links, or frontend links across markdown docs; resolve and reference them via directory.md (only directory.md.sample is committed to version control).
- Zero Credential Exposure: Never commit credentials.md or real secrets to git/GitHub. Only credentials.md.sample with sanitized placeholders is tracked. If the user explicitly asks to commit credentials, issue a critical security warning and require confirmation before proceeding.
