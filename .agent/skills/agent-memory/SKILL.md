---
name: agent-memory
description: >
  Use this skill to bootstrap and enforce persistent project memory, safe file
  writing practices, and consistent session flow across projects.
---

# Agent Memory Skill

## DEVELOPER IDENTITY
Read `references/GLOBAL_PROTOCOL.md` for the full developer profile,
stack preferences, git identity rules, and communication style.
The installer writes these details to `{AGENT_SYSTEM_PATH}/GLOBAL_PROTOCOL.md`
based on the user's environment at install time.

## PATH RESOLUTION
At session start, resolve `.agent-config` by checking the first available location:
1. Google Antigravity: `~/.gemini/config/skills/agent-memory/.agent-config` (Windows: `%USERPROFILE%\.gemini\config\skills\agent-memory\.agent-config`)
2. GitHub Copilot: `~/.copilot/skills/agent-memory/.agent-config` (Windows: `%USERPROFILE%\.copilot\skills\agent-memory\.agent-config`)
3. Agent Skills: `~/.agents/skills/agent-memory/.agent-config` (Windows: `%USERPROFILE%\.agents\skills\agent-memory\.agent-config`)
4. Global System Path: `~/agent-system/.agent-config` (Windows: `%USERPROFILE%\agent-system\.agent-config`)
5. Current skill directory: `.agent-config`

This file is written by the installer and contains:
  AGENT_SYSTEM_PATH=...
  AGENT_USER=...
  AGENT_HOME=...

If `.agent-config` is not yet present, use safe defaults:
  AGENT_SYSTEM_PATH = `~/agent-system` (Windows: `%USERPROFILE%\agent-system`)
  AGENT_HOME = `~` (Windows: `%USERPROFILE%`)
  AGENT_USER = current OS login user or git user

Use these values wherever you see {AGENT_SYSTEM_PATH} in this skill.

## USERNAME SETUP (FIRST RUN)
If `AGENT_USER` is missing, empty, or still a copied template value:
1. Ask the user what username should be used for git identity.
2. Use that value as `{AGENT_USER}` for the current session.
3. Tell the user to persist it in `.agent-config` as `AGENT_USER=<their-username>`.
Never default to any hardcoded username.

## SESSION ENTRY FLOW
1. Read:
   - `{AGENT_SYSTEM_PATH}/GLOBAL_PROTOCOL.md`
   - `{AGENT_SYSTEM_PATH}/GLOBAL_WARNINGS.md`
   - `{AGENT_SYSTEM_PATH}/CONVENTIONS.md`
2. Read project memory files:
   - `.agent/MEMORY.md`
   - `.agent/CODEBASE.md`
   - `.agent/WARNINGS.md`
   - `.agent/CURRENT_TASK.md`
3. If `.agent/` files are missing, run bootstrap from:
   - `{AGENT_SYSTEM_PATH}/AGENT_BOOTSTRAP.md`
4. Confirm:
   - Project name
   - Active branch
   - Files to touch
   - Files not to touch

## FILE SAFETY RULES
- Always write full file contents when editing source files.
- Never use partial-file placeholders like "...unchanged".
- Never use destructive commands without explicit confirmation.
- Patch memory files surgically; do not rewrite full history/log files.

## ANTI-HALLUCINATION & AUDIT RULES
- Report ONLY what actually exists on disk; never assume framework defaults.
- If a route, function, or file is missing, explicitly report "NOT FOUND" instead of guessing.
- For every architectural or code claim, cite exact file paths and function/route names (`path/to/file.ext#symbol`).
- Audits and explorations are strictly read-only (zero file modifications).


## REFERENCE FILES
Load on demand:
- `references/GLOBAL_PROTOCOL.md`
- `references/GLOBAL_WARNINGS.md`
- `references/CONVENTIONS.md`
- `references/AGENT_BOOTSTRAP.md`
- `references/SESSION_START.md`

