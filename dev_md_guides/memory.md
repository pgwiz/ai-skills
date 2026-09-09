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

## Gotchas
- On Windows PowerShell, output encoding for git commands must use UTF-8 with error replacement to prevent character encoding crashes with non-ASCII commit logs.

## Conventions
- Every skill in this repository must provide a valid `SKILL.md` compliant with the Agent Skills open standard (agentskills.io).
- `dev_md_guides/changelog.md` is strictly append-only; never rewrite or delete past entries.

## Dead ends
- Monolithic memory-bank reads on every prompt turn: abandoned due to severe context window consumption (>5,000 tokens per turn).
