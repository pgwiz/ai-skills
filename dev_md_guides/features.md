# Feature Roadmap & SDD Progress Matrix
_Last updated: 2026-09-09_

## Done
- **`dev-md-compactor` Agent Skill** — AST-aware deterministic context compactor maintaining `dev_md_guides/` (branch.md, features.md, structure.md, memory.md, changelog.md, directory.md.sample, credentials.md.sample). Location: `dev-md-compactor/`.
- **Zero-Hardcoded Directory Catalog (`directory.md` & `directory.md.sample`)** — Centralized environment, servers, frontend/backend links catalog; gitignored local file with tracked sanitized sample deployed to GitHub. Location: `dev-md-compactor/templates/`, `dev_md_guides/directory.md.sample`.
- **Zero-Exposure Credentials Management (`credentials.md` & `credentials.md.sample`)** — Isolated secrets schema; gitignored local credentials, tracked mock sample, automated secret scanner, and mandatory user warning protocol before any credential commit. Location: `dev-md-compactor/templates/`, `dev_md_guides/credentials.md.sample`, `dev-md-compactor/scripts/run_compactor.py`.
- **Antigravity `/compact-docs` Workflow** — Workspace slash command and project instructions for autonomous compaction. Location: `.agent/workflows/compact-docs.md`, `GEMINI.md`.
- **Research Documentation Archive** — Formal technical analysis on context compaction and memory persistence. Location: `research/`.
- **`agent-memory` Skill** — Persistent developer identity, safe file writing rules, and cross-session bootstrap. Location: `agent-memory/`.

## In Progress

## Planned
- **Multi-language AST Parser expansion** — Tree-sitter or native syntax parsers for TypeScript/Rust/Go in `run_compactor.py`.

## Removed
- **Prototype `mem-bank-skill/`** — Retired 2026-09-09 in favor of standardized `dev-md-compactor/` at repository root.
