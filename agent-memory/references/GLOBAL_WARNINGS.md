# GLOBAL WARNINGS
# Author: {AGENT_USER}
# Location: {AGENT_SYSTEM_PATH}\GLOBAL_WARNINGS.md
# READ THIS BEFORE EVERY SESSION — NO EXCEPTIONS

---

## THINGS THAT HAVE GONE WRONG — NEVER REPEAT

### File Writing
- **sed -i on Blade files** — broke PHP syntax, spent hours reverting
- **heredoc to write files** — encoding issues, invisible characters introduced
- **Partial file output** ("rest unchanged") — {AGENT_USER} had to manually merge, introduced bugs
- **cat > file in terminal** — overwrote files without showing content first

### Git
- **AI co-author strings in commits** — violates gitpush.md policy, had to rewrite history
- **Committing to main** — always use the active branch (check MEMORY.md)
- **Force push without confirmation** — catastrophic on shared remotes

### Database
- **migrate:fresh on a project with seed data** — lost test data, never again
- **DELETE without WHERE** — obvious, still happens
- **Assuming the ORM** — always check if project uses raw queries, Eloquent, SQLAlchemy, Prisma etc.

### Auth
- **Assuming `auth()->user()`** — some projects use `auth('staff')`, `auth('admin')`, custom guards
- **Assuming `Auth::user()` is the same guard everywhere** — it isn't
- **Assuming `$request->user()` works in all middleware** — check the guard

### Environment
- **Hardcoding localhost** — breaks on server
- **Hardcoding port 8000** — breaks in Docker
- **Reading .env directly** — always use the framework's config system
- **Editing .env in code** — never write to .env programmatically

### Docker / Server
- **OCI (Oracle Cloud) iptables** — OCI has its own firewall rules ABOVE iptables
  Always open ports in OCI console security lists, not just ufw/iptables
- **Serv00 shared hosting** — no root, no systemd, WSGI only, PHP 8 / Slim 4 / MySQL only
  Never suggest Docker or systemd services for Serv00
- **chmod 777 anything** — security risk, never

### Laravel Specific
- **Using `User` model when project has `Staff` model** — always check MEMORY.md
- **Assuming Spatie for permissions** — some projects use a custom role column
- **`php artisan optimize:clear` in production** — confirm first
- **Touching `config/app.php`** — usually not needed, usually breaks something

### Django Specific  
- **`DEBUG=True` in production** — always check settings file being used
- **Sync views in async project** — check if project is ASGI or WSGI first
- **Running migrations without backup on production** — always confirm

### FastAPI Specific
- **Mixing sync and async** — if project is async, everything must be async
- **Not using `await` on async DB calls** — silent failures
- **SQLAlchemy 1.x style in a 2.0 project** — breaks

### Go Specific
- **Ignoring errors with `_`** — every error must be handled
- **Global mutable state** — causes race conditions in concurrent handlers

### Memory Files
- **Rewriting entire CODEBASE.md** — loses established context, creates drift
- **Not updating DONE.md** — tasks get lost, work gets repeated
- **Updating MEMORY.md with task-specific details** — MEMORY.md is for patterns, not todos

---

## COMMANDS THAT REQUIRE EXPLICIT CONFIRMATION

Never run these without {AGENT_USER} saying "yes, run it":

```bash
# Database
php artisan migrate:fresh
php artisan migrate:reset
python manage.py flush
DROP TABLE
TRUNCATE TABLE
DELETE FROM table (no WHERE)

# File system  
rm -rf anything
find . -delete
git clean -fd

# Git
git push --force
git push --force-with-lease
git rebase (on shared branches)
git reset --hard (past last commit)

# Permissions
chmod 777
chown -R (on system dirs)

# Process
kill -9
pkill

# Package management (lock file changes)
composer update (not install)
pip install --upgrade (unpinned)
npm update
```

---

## STACK GOTCHAS BY PROJECT TYPE

### Serv00 Projects (submit.example-host.tld etc.)
- PHP 8 / Slim 4 / MySQL ONLY
- No Docker, no Node, no Python workers
- Deployment: git pull + file copy only
- Never suggest systemd or pm2

### Oracle Cloud VPS Projects
- Always open ports in OCI Security Lists (console) FIRST
- Then iptables / ufw second
- Forgetting OCI console = port looks open locally, closed externally

### Cloudflare Projects (example-host.tld)
- Free wildcard SSL covers `*.example-host.tld` only — one level deep
- `tenant.smw.example-host.tld` is NOT covered — use `tenant.example-host.tld`
- Always proxy through Cloudflare (orange cloud) for SSL to work
- Never set A record to private IP

### Windows Dev Machine
- Aliases at `{AGENT_HOME}\aliases\`
- sudo.ps1 elevates executables/scripts/shells — blocks documents/media
- Global git hook at `$env:USERPROFILE\.git-hooks`
- Never override git hooks per-repo

---

*Append new warnings at the bottom with date.*
*Format: `- [YYYY-MM-DD] what happened and what to never do again`*

## CHANGELOG
- [2025-05-06] Initial global warnings compiled from all active projects

