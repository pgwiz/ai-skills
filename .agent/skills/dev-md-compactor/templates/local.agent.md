# Local Private Agent Overrides (`local.agent.md`)

_Developer-specific, confidential, and machine-local agent configuration._  
_This file is strictly gitignored by default and must NEVER be committed to version control._

> [!CAUTION]
> **LOCAL PRIVATE FILE — NEVER COMMIT TO GITHUB**
> - All `local.*.md` and `*.local.md` files (at root or in `dev_md_guides/`) are strictly ignored by `.gitignore`.
> - Use this file for machine-specific instructions, private internal URLs, developer notes, personal sandbox configurations, or staging keys that must not be published to public repositories.

---

## 1. Local Developer Preferences

- **Developer Alias**: `[YOUR_NAME_OR_ALIAS]`
- **Local Dev Workstation**: `[LOCAL_MACHINE_HOSTNAME]`
- **Preferred Shell / Terminal**: `pwsh` / `bash` / `zsh`

---

## 2. Machine-Specific Overrides

- **Custom Local Test Database**: `postgresql://localhost:5432/my_dev_db`
- **Private Staging Gateway**: `https://staging-internal.example.com`
- **Internal CI / Sandbox Tokens**: `ENC[YOUR_LOCAL_TOKEN]`

---

## 3. Ephemeral Scratchpad Notes

_Use this section for active scratchpad notes during complex multi-step refactoring sessions._
