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
At session start, read `~/.copilot/skills/agent-memory/.agent-config`
(or `%USERPROFILE%\.copilot\skills\agent-memory\.agent-config` on Windows).
This file is written by the installer and contains:
  AGENT_SYSTEM_PATH=...
  AGENT_USER=...
  AGENT_HOME=...
Use these values wherever you see {AGENT_SYSTEM_PATH} in this skill.

## USERNAME SETUP (FIRST RUN)
If `AGENT_USER` is missing, empty, or still a copied template value:
1. Ask the user what username should be used for git identity.
2. Use that value as `{AGENT_USER}` for the current session.
3. Tell the user to persist it in `.agent-config` as `AGENT_USER=<their-username>`.
Never default to `pgwiz` or any other hardcoded username.

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

## REFERENCE FILES
Load on demand:
- `references/GLOBAL_PROTOCOL.md`
- `references/GLOBAL_WARNINGS.md`
- `references/CONVENTIONS.md`
- `references/AGENT_BOOTSTRAP.md`
- `references/SESSION_START.md`

