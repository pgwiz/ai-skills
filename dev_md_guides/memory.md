# Project Memory Bank & Architecture Decision Records (ADR)
_Durable knowledge — decisions, gotchas, conventions. Not a log._

## Architecture decisions

### ADR-0001: Separation of dev-md-compactor from agent-memory
- **Date**: 2026-09-09
- **Status**: ACCEPTED
- **Context**: Autonomous software engineering agents need both general session bootstrap/conventions and specialized AST-driven context compaction. Combining them into one monolithic skill inflates per-turn token spend.
- **Decision**: Keep `agent-memory` as the developer identity/session convention skill, and establish `dev-md-compactor` as a dedicated, specialized living documentation & AST context compaction skill.
- **Consequences**: Clear separation of concerns; low persistent token overhead; progressive disclosure enabled.
- **Rejected Alternatives**: Merging into a single monolithic skill (rejected due to token overhead and role confusion).

### ADR-0002: Dual Python Engine and Shell Context Extractor
- **Date**: 2026-09-09
- **Status**: ACCEPTED
- **Context**: Agent runtimes run across diverse operating systems (Windows PowerShell, macOS zsh, Linux bash). Shell-only scripts break in native Windows environments lacking bash in PATH.
- **Decision**: Implement `run_compactor.py` using Python 3.10+ standard library (`ast`, `subprocess`, `pathlib`) as the primary cross-platform engine, while retaining `gather_context.sh` for bash parity.
- **Consequences**: Zero external dependencies; 100% cross-platform parity on Windows, Linux, and macOS.

### ADR-0003: Centralized Environment & Directory Catalog (directory.md / directory.md.sample)
- **Date**: 2026-09-14
- **Status**: ACCEPTED
- **Context**: Hardcoding local filesystem paths, server IP addresses, backend API endpoints, and frontend URLs across markdown files causes cross-developer portability issues, documentation drift, and severe risk of leaking internal infrastructure or private paths when pushed to GitHub.
- **Decision**: Introduce `directory.md` in `dev_md_guides/` as the single source of truth for all environment paths, servers, backend links, frontend links, and ports. All other markdown guides must reference keys from `directory.md` instead of hardcoding paths. To protect private network configurations, `directory.md` is gitignored by default and only `directory.md.sample` (with sanitized example schemas) is committed and deployed to GitHub.
- **Consequences**: Zero hardcoded environment paths in documentation; seamless git safety; deterministic onboarding across local, staging, and production environments.
- **Rejected Alternatives**: Committing actual `directory.md` directly (rejected due to privacy and local machine path leaks); environment variable interpolation in markdown (rejected due to markdown renderer incompatibility).

## Gotchas
- On Windows PowerShell, output encoding for git commands must use UTF-8 with error replacement to prevent character encoding crashes with non-ASCII commit logs.

## Conventions
- Every skill in this repository must provide a valid `SKILL.md` compliant with the Agent Skills open standard (agentskills.io).
- `dev_md_guides/changelog.md` is strictly append-only; never rewrite or delete past entries.
- Never hardcode machine directories, server hostnames, backend links, or frontend links across markdown docs — always resolve and document via `directory.md`.

## Dead ends
- Monolithic memory-bank reads on every prompt turn: abandoned due to severe context window consumption (>5,000 tokens per turn).
