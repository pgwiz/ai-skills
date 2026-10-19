# AGENT BOOTSTRAP
# Location: {AGENT_SYSTEM_PATH}\AGENT_BOOTSTRAP.md
# Run this when: starting on a new project OR .agent/ files are missing/corrupt

---

## WHEN TO RUN BOOTSTRAP

Run bootstrap if ANY of these are true:
- `.agent/` directory does not exist in the project root
- Any file inside `.agent/` is missing
- MEMORY.md first line does not match the current project
- You are starting work on a project for the first time

---

## BOOTSTRAP SEQUENCE

### STEP 1 — Scan the project

Run these commands and read the output:

```bash
# Project root structure (2 levels)
find . -maxdepth 2 -not -path '*/node_modules/*' \
  -not -path '*/.git/*' \
  -not -path '*/vendor/*' \
  -not -path '*/__pycache__/*' \
  -not -path '*/.venv/*' \
  -not -path '*/storage/*' \
  -not -path '*/dist/*' \
  -not -path '*/build/*' \
  | sort

# Detect stack
ls composer.json package.json requirements.txt go.mod Cargo.toml \
   pubspec.yaml *.csproj 2>/dev/null

# Git info
git remote -v
git branch --show-current
git log --oneline -5

# Framework version (Laravel)
php artisan --version 2>/dev/null

# Framework version (Django/FastAPI)  
python -m django --version 2>/dev/null
grep fastapi requirements.txt 2>/dev/null

# Database config hint
cat .env | grep -E "DB_|DATABASE_" 2>/dev/null | head -10

# Existing routes (Laravel)
php artisan route:list --compact 2>/dev/null | head -40

# Existing models (Laravel)
ls app/Models/ 2>/dev/null

# Existing apps (Django)
cat */apps.py 2>/dev/null | grep "name ="
```

### STEP 2 — Create `.agent/` directory

```bash
mkdir -p .agent
```

### STEP 3 — Generate each file using the templates below

Fill in `[PLACEHOLDER]` values from your scan in STEP 1.

---

## FILE TEMPLATES

### `.agent/MEMORY.md`

```md
# Agent Memory — [PROJECT NAME]
# Stack: [STACK e.g. Laravel 11 / Blade / MySQL]
# Branch: [ACTIVE BRANCH]
# Last updated: [DATE]

## Project Overview
[One paragraph: what this project does, who it's for]

## Established Patterns
- [Pattern discovered during scan e.g. "Controllers extend BaseController"]
- [e.g. "Auth guard is auth('staff') not auth()"]
- [e.g. "All API responses use ApiResponse::success() wrapper"]
- [Add more as discovered during work]

## Database
- Connection: [mysql/postgresql/sqlite]
- DB name: [name from .env]
- Key tables: [list main tables if discoverable]
- ORM: [Eloquent / SQLAlchemy / Prisma / raw / etc.]

## Key Models / Entities
- [ModelName] → [what it represents, key relationships]
- [Add more as discovered]

## Key Controllers / Handlers
- [ControllerName] → [what routes it handles]
- [Add more as discovered]

## Design System (if frontend project)
- Colors: [primary, accent, background]
- Fonts: [heading font, body font]
- Component pattern: [glassmorphism / material / custom / etc.]

## Decisions Made
- [DATE]: [Decision and why]
```

---

### `.agent/CODEBASE.md`

```md
# Codebase Map — [PROJECT NAME]
# Last updated: [DATE]
# Auto-patched by agent — never full rewrite

## Stack
- Framework: [e.g. Laravel 11]
- Language: [e.g. PHP 8.3]
- Database: [e.g. MySQL 8]
- Frontend: [e.g. Blade + Alpine.js + Tailwind]
- Build tool: [e.g. Vite]
- Deployment: [e.g. Serv00 WSGI / Oracle Cloud VPS / Vercel]

## Directory Structure
```
[paste trimmed output of find command from STEP 1]
```

## Routes
[For Laravel: paste trimmed route:list output]
[For Django: list urlpatterns from urls.py]
[For FastAPI: list @router decorators]
[For Express: list router files]

## Controllers / Views / Handlers
- [file path] → [what it does]

## Models
- [ModelName] (app/Models/ModelName.php) → [table, key fields]

## Key Config Files
- [file] → [what it controls]

## External Services / APIs
- [service name] → [what it's used for, where credentials are]

## Active Branch
- [branch name] — all commits go here

## Deployment Notes
- [how to deploy, any special steps]
```

---

### `.agent/CURRENT_TASK.md`

```md
# Current Task — [PROJECT NAME]

STATUS: IDLE

## When a task is active, this file looks like:
---
STATUS: IN PROGRESS
Task: [what is being built]
Started: [date]
Files to touch:
  - [file 1]
  - [file 2]
Do NOT touch:
  - [file 3]
Notes:
  - [any relevant context for this specific task]
---
```

---

### `.agent/DONE.md`

```md
# Done Log — [PROJECT NAME]
# Append only — never edit previous lines
# Format: [YYYY-MM-DD] task: description

[DATE] bootstrap: initialized .agent/ memory system for this project
```

---

### `.agent/WARNINGS.md`

```md
# Project-Specific Warnings — [PROJECT NAME]
# READ BEFORE EVERY SESSION
# Also read: {AGENT_SYSTEM_PATH}\GLOBAL_WARNINGS.md

## Project-Specific Gotchas
- [Add as discovered during work]

## Files That Are Fragile / Do Not Touch Without Confirmation
- [file path] → [why it's sensitive]

## Known Broken Things (do not fix unless tasked)
- [thing] → [what's wrong, why we're leaving it]

## Environment Notes
- [anything specific to this project's environment]

## CHANGELOG
- [DATE] bootstrap: created
```

---

## STEP 4 — Add `.agent/` to `.gitignore`

```bash
echo ".agent/" >> .gitignore
```

> **Why gitignore?** Agent memory is local dev context — not deployment config.
> It should NOT be committed. Each developer/agent maintains their own.
> Exception: if {AGENT_USER} explicitly wants to commit it, remove from gitignore.

---

## STEP 5 — Report bootstrap completion

After bootstrap, report to {AGENT_USER}:
```
Bootstrap complete for [PROJECT NAME].
Stack detected: [stack]
Branch: [branch]
Files created: .agent/MEMORY.md, CODEBASE.md, CURRENT_TASK.md, DONE.md, WARNINGS.md

⚠️ Review .agent/CODEBASE.md — I filled what I could from the scan.
   Fill in any missing sections before the first task.

Ready for task.
```

---

## STEP 6 — Generate README.env

After bootstrap scan is complete:
1. Scan for `.env.example`, `.env.sample`, `settings.py`, and `config/database.php`
   to discover required environment variables.
2. Generate `README.env` in the project root using this structure:
   - Required variables table
   - Setup steps
   - Detected stack/runtime
   - Environment notes
3. Commit:
   - `git add README.env`
   - `git commit -m "docs: add README.env — environment setup guide"`
4. Push to active branch:
   - `git push origin [branch]`
5. Report:
   - `README.env generated and pushed`

---

*This bootstrap should take ~2 minutes. Do not skip steps.*
*Do not start any task until bootstrap is confirmed complete.*

