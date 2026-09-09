# dev_md_guides File Formats

Adhere to these structural markdown formats to guarantee consistent, diff-friendly documents across sessions.

---

## `dev_md_guides/structure.md`

```markdown
# Codebase Architecture & Directory Dependency Graph
_Last regenerated: YYYY-MM-DD HH:MM:SS UTC by dev-md-compactor_

## Project Manifests & Build Tools
- `pyproject.toml`
- `package.json`

## Module Directory Topography

### `src/api/`
- **Files (5)**: `server.py`, `routes.py`, `middleware.py`
- **Discovered Module Dependencies**: `fastapi`, `pydantic`, `src/auth`

### `src/auth/`
- **Files (3)**: `service.py`, `pkce.py`, `tokens.py`
- **Discovered Module Dependencies**: `cryptography`, `jwt`

## Architectural Invariants & Boundary Rules
- Gateway layer (`src/api`) must not directly access database session pool without passing through domain service.
```

---

## `dev_md_guides/features.md`

```markdown
# Feature Roadmap & SDD Progress Matrix
_Last updated: YYYY-MM-DD_

## Done
- **Stateless PKCE Auth** — RFC 7636 compliant verifier and challenge flow. Location: `src/auth/pkce.py`.

## In Progress
- **Token Blacklist Bloom Filter** — In-memory synchronization for revoked JWTs. Location: `src/auth/blacklist.py`. Blocked by: HSM mock in CI.

## Planned
- **Refresh Token Rotation** — Sliding session refresh endpoint.

## Removed
- **Redis Session Storage** — Deprecated 2026-03-29; superseded by stateless JWT. See changelog.
```

---

## `dev_md_guides/branch.md`

```markdown
# Branch State & Worktree Topology

- **Active Branch**: `feat/oauth2-stateless-flow`
- **HEAD Commit**: `a1c4e9f` — feat(auth): add PKCE challenge generator
- **Tracking Status**: Ahead 2 commits relative to origin/main
- **Last Updated**: 2026-03-30 15:00:00 UTC

## Divergence Analysis

### Recent Commits (Local)
- `a1c4e9f` (2026-03-30): feat(auth): add PKCE challenge generator
- `7d2e09a` (2026-03-30): test(auth): add failing unit tests for PKCE

### Uncommitted Working Tree State
- `M src/auth/pkce.py`
- `?? src/auth/crypto_utils.py`

## Integration Checklist
- [ ] Working tree cleanly committed or stashed before branch switch
- [ ] Rebase / sync with upstream verified
- [ ] Code passes test and lint gates
```

---

## `dev_md_guides/memory.md`

```markdown
# Project Memory Bank & Architecture Decision Records (ADR)
_Durable knowledge — decisions, gotchas, conventions. Not a log._

## Architecture decisions

### ADR-0001: Migration to Stateless JWT with PKCE
- **Date**: 2026-03-29
- **Status**: ACCEPTED
- **Context**: Multi-region deployment required sub-5ms auth verification without Redis lock overhead.
- **Decision**: All auth endpoints must use RFC 7636 PKCE code challenges and short-lived RS256 JWTs.
- **Consequences**: Zero external session store dependency; revoked token tracking requires Bloom filter.
- **Rejected Alternatives**: Sticky sessions (uneven edge load), Distributed Redis locks (cross-region partition risk).

## Gotchas
- **Token Claims**: `iss` and `aud` must match exactly or PyJWT raises `InvalidIssuerError` silently.

## Conventions
- Always sort imports per PEP 8 (standard library, third-party, local).

## Dead ends
- **Client-side session cookies**: Abandoned due to Safari third-party cookie blocking.
```

---

## `dev_md_guides/changelog.md`

```markdown
# Session Operational Changelog
_Append-only. Newest first. Never edit past entries._

## [2026-03-30 15:45:00 UTC] — Branch `feat/oauth2-stateless-flow` (HEAD: `a1c4e9f`)
- **Event**: Automated Context Compaction at Task Boundary
- **Operational Scope**: Implemented PKCE challenge generator and wired into auth router.

### AST & Code Modifications
- **File**: `src/auth/pkce.py` (python)
  - *Functions*: `generate_code_verifier(length) [line:15]`, `generate_code_challenge(verifier) [line:30]`
  - *Classes*: none
- **File**: `tests/auth/test_pkce.py` (python)
  - *Functions*: `test_verifier_entropy() [line:10]`, `test_challenge_hash() [line:25]`

---
```
