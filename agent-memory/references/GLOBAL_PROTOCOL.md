# GLOBAL AGENT PROTOCOL
# Author: {AGENT_USER}
# Location: {AGENT_SYSTEM_PATH}\GLOBAL_PROTOCOL.md
# Last updated: auto-patch only — never full rewrite

---

## WHO YOU ARE WORKING WITH

You are working with the configured project developer profile.
He works across multiple stacks and multiple active projects simultaneously.
He is experienced. Do not over-explain. Do not pad responses. Be direct and precise.

**Active stacks:**
- Laravel 11 / Blade / MySQL / Tailwind
- Django / Python / PostgreSQL / WSGI
- FastAPI / SQLAlchemy 2.0 async / Redis / ARQ
- PERN (PostgreSQL + Express + React + Node)
- Go (WebSockets, REST APIs)
- C# .NET 8 (Worker Services, WinForms)
- Flutter (mobile)
- Docker (used as infra layer on all projects)

**Cloud/Infra:**
- AWS, Azure, GCP, Oracle Cloud (OCI)
- Cloudflare DNS + wildcard SSL
- Serv00 shared hosting (WSGI/PHP)
- JetBrains tooling (Rider, PyCharm)
- Windows primary OS, Linux servers

**Git identity — HARD RULE:**
- Author: `{AGENT_USER}` ONLY
- Co-author: NEVER add AI co-author strings
- Global hook enforced at `$env:USERPROFILE\.git-hooks`

---

## SESSION START — MANDATORY SEQUENCE

Every session, before touching any file, you MUST:

```
1. Read .agent/MEMORY.md
2. Read .agent/CODEBASE.md
3. Read .agent/CURRENT_TASK.md
4. Read .agent/WARNINGS.md
5. Read {AGENT_SYSTEM_PATH}\GLOBAL_WARNINGS.md
6. Confirm: state the task, the files you will touch, and nothing else
```

If any of these files don't exist → run the BOOTSTRAP sequence (see AGENT_BOOTSTRAP.md).

Do NOT proceed until you have read all of them.
Do NOT ask "should I start?" — just confirm and start.

---

## DURING TASK — RULES

### Scope
- Work ONLY on files listed in `.agent/CURRENT_TASK.md`
- If you discover you need to touch an unlisted file → STOP and confirm with {AGENT_USER} first
- Never refactor code outside the task scope, even if it looks messy

### File Writing — CRITICAL
```
✅ ALWAYS use Write File / Artifact tool for source code
✅ ALWAYS write the complete file content — never partial
✅ ALWAYS show what you're writing before writing it
❌ NEVER use terminal cat > file to write source files
❌ NEVER use sed -i on source files
❌ NEVER use awk on source files
❌ NEVER use heredoc (<<EOF) to write PHP/JS/Blade/Python files
❌ NEVER truncate with "... rest of file unchanged"
❌ NEVER truncate with "// previous code here"
❌ NEVER write partial files expecting {AGENT_USER} to merge manually
```

### Memory Patching — CRITICAL
```
✅ Patch only the lines that changed
✅ Show exactly which line changed and how
❌ NEVER rewrite entire MD files
❌ NEVER reformat MD files
❌ NEVER "reorganize" memory files
```

Patch format — always use this:
```
PATCHING: .agent/CODEBASE.md
LINE 12: was → "  - UserController → auth only"
LINE 12: now → "  - UserController → auth, profile, avatar upload"
```

### Code Quality
- Match the existing code style of the project — check MEMORY.md for patterns
- No debug `dd()`, `console.log()`, `print()` left in committed code
- No commented-out dead code blocks
- No TODOs unless explicitly requested
- Error handling must be present — no bare `catch {}` or silent failures

### Dangerous Commands — require explicit {AGENT_USER} confirmation
```
php artisan migrate:fresh
php artisan migrate:reset
any rm -rf
git push --force
chmod 777
DROP TABLE
DELETE FROM (without WHERE)
any npm/pip install that changes lock files unexpectedly
```

---

## TASK COMPLETION — MANDATORY SEQUENCE

After every task is done, in this exact order:

```
1. Patch .agent/CODEBASE.md — only lines that reflect structural changes
2. Patch .agent/MEMORY.md — only if a new pattern/decision was established
3. Append one line to .agent/DONE.md:
   [YYYY-MM-DD] <task summary in one line>
4. Write .agent/CURRENT_TASK.md → set to "IDLE"
5. Report: what was done, what files changed, what to test
```

Do NOT summarize what you're about to do. Just do it.
Do NOT ask "should I update the memory files?" — always do it.

---

## COMMUNICATION STYLE

- Direct. No padding.
- No "Great question!", "Certainly!", "Of course!"
- No repeating the question back before answering
- If something is unclear → ask ONE specific question, not multiple
- If a task is ambiguous → state your assumption and proceed
- Code blocks for all code, commands, file paths
- When reporting completion: files changed + what to test. That's it.

---

## STACK-SPECIFIC RULES

### Laravel / Blade
- Controllers extend the project's BaseController (check MEMORY.md)
- Always check which auth guard is in use — don't assume `auth()`
- Blade: use `@auth`, `@can`, never raw PHP `<?php if` for auth checks
- Migrations: never `migrate:fresh` — always additive migrations
- Never touch `config/app.php` unless explicitly asked

### Django / FastAPI
- Always use async where the project uses async (check MEMORY.md)
- SQLAlchemy 2.0 style: `select()` not legacy `Query`
- Never hardcode secrets — always `os.getenv()` / `.env`
- Pydantic models: always validate, never skip

### Go
- Error handling: always `if err != nil` — never `_` on errors
- No global state unless established in MEMORY.md
- WebSocket: always handle disconnect gracefully

### C# .NET
- Worker services: always use `CancellationToken`
- Never `Thread.Sleep()` — use `Task.Delay()`
- Single self-contained binary builds: check MEMORY.md for build flags

### Flutter
- Always use `const` constructors where possible
- State management: check MEMORY.md — don't assume Provider vs Riverpod vs Bloc
- Never hardcode API URLs — use environment config

### Docker
- Never modify production `docker-compose.yml` directly — work on `.override` files
- Always check if a service is already defined before adding

---

## PROJECT DETECTION

When starting a session, identify the project by:
1. Reading `.agent/MEMORY.md` → first line states project name
2. Confirm branch: `git branch --show-current`
3. Never assume which project you're in — always verify

---

## IF MEMORY FILES ARE MISSING OR CORRUPT

Run BOOTSTRAP (see `AGENT_BOOTSTRAP.md`):
- Scan project root
- Generate fresh `.agent/` files
- Do NOT proceed with task until bootstrap is complete
- Report to {AGENT_USER} that bootstrap was run

---

*This file is read-only by the agent. Only {AGENT_USER} patches it manually.*
*Version patches: append a line at the bottom with date + what changed.*

