# Codebase Architecture & Directory Dependency Graph
_Last regenerated: 2026-09-14 09:35:15 UTC by dev-md-compactor_

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
- **Files (7)**: `branch.md, changelog.md, directory.md, directory.md.sample, features.md, memory.md, structure.md`

### `install/`
- **Files (3)**: `INSTALL.md, install.ps1, install.sh`

### `research/`
- **Files (2)**: `Agent Memory Compaction Research.docx, Agent Memory Compaction Research.md`

### `root/`
- **Files (7)**: `CODE_OF_CONDUCT.md, GEMINI.md, INSTALL_PLAN_v2.md, MARKETPLACE.md, README.md, SECURITY.md, verification_request.md`

## Architectural Invariants & Boundary Rules
- Internal modules should adhere to defined dependency boundaries without cyclic imports.
- Configuration, secrets, and environment overrides must not be hardcoded in application logic.
- Zero Hardcoded Endpoints: Do not hardcode machine directories, server IPs, backend links, or frontend links across markdown docs; resolve and reference them via directory.md (only directory.md.sample is committed to version control).
