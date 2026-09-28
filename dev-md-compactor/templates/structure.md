# Codebase Architecture & Directory Dependency Graph
_Last regenerated: (date) by dev-md-compactor_

## Project Manifests & Build Tools
- *(Discovered build manifests)*

## Module Directory Topography

### `src/`
- **Files**: Entry points and core implementations.
- **Discovered Module Dependencies**: (Dependencies)

## Environment & Directory Catalog Reference
- Central Catalog: `dev_md_guides/directory.md` (sample committed as `dev_md_guides/directory.md.sample`).
- All workspace paths, servers, backend links, frontend links, and external endpoints are centralized in this catalog.
- Invariant: Never hardcode local filesystem paths or network URLs directly across project markdown files.

## Architectural Invariants & Boundary Rules
- Modules adhere to layered boundaries without cyclical references.
- Zero Hardcoded Endpoints: Do not hardcode machine directories, server IPs, backend links, or frontend links across markdown docs; resolve and reference them via directory.md (only directory.md.sample is committed to version control).
