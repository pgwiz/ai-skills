# pgwiz Agent Memory System
# Location: {AGENT_SYSTEM_PATH}\
# Version: 1.0

---

## WHAT THIS IS

A global memory + protocol system for coding agents (Claude, Cursor, Copilot, etc.)
that keeps them focused, consistent, and non-destructive across all your projects.

**Problem it solves:**
- Agent forgets codebase structure mid-session
- Agent rewrites files it shouldn't touch
- Agent uses dangerous terminal commands instead of writing files properly
- You repeat yourself every session explaining the same context
- Agent loses memory between sessions

**How it works:**
- Global files (this folder) = rules that never change
- Per-project `.agent/` files = project-specific memory that auto-updates
- Agent reads both at session start → has full context without you explaining

---

## FILES IN THIS FOLDER

| File | Purpose | Who updates it |
|------|---------|----------------|
| `GLOBAL_PROTOCOL.md` | Universal agent rules, your dev identity, stack rules | pgwiz manually |
| `GLOBAL_WARNINGS.md` | Cross-project mistakes never to repeat | pgwiz (append only) |
| `AGENT_BOOTSTRAP.md` | How to initialize `.agent/` for a new project | Read-only |
| `CONVENTIONS.md` | Coding standards across all stacks | pgwiz manually |
| `SESSION_START.md` | The exact prompt to start every session | Read-only (copy from it) |
| `README.md` | This file | pgwiz manually |

---

## PER-PROJECT FILES (in each project root)

```
[project-root]/
  .agent/
    MEMORY.md        ← patterns, decisions, key info about this project
    CODEBASE.md      ← file structure, routes, models, controllers map
    CURRENT_TASK.md  ← what's being worked on right now
    DONE.md          ← completed tasks log (append only)
    WARNINGS.md      ← project-specific gotchas
```

---

## QUICK START — NEW PROJECT

1. Open the project in your editor
2. Copy the SESSION_START prompt from `SESSION_START.md`
3. Set TASK to: `Bootstrap the .agent/ memory system for this project`
4. Paste to agent
5. Agent scans project, creates `.agent/` files
6. You review `.agent/MEMORY.md` and fill in anything the agent missed
7. Done — all future sessions start with full context

---

## QUICK START — EXISTING PROJECT (already bootstrapped)

1. Copy SESSION_START prompt from `SESSION_START.md`
2. Set TASK to whatever you need done
3. Paste to agent
4. Agent reads all memory files, confirms context, does the task
5. Agent patches only the changed lines in `.agent/` files
6. Done

---

## ACTIVE PROJECTS

| Project | Stack | Branch | Location |
|---------|-------|--------|----------|
| Premier Valuers Limited | Laravel 11 / Blade / MySQL | me-right | [path] |
| UniMarket | Django / PostgreSQL / django-tenants | main | [path] |
| RAGCORE | FastAPI / PostgreSQL / Redis | main | [path] |
| FERMM | C# .NET 8 / FastAPI / React | main | [path] |
| Afri-Agro AI | Python / TFLite / Raspberry Pi | main | [path] |
| Hermes | Rust / Python / Node / Nginx | main | [path] |
| Casino Engine | Go / WebSockets | main | [path] |

> Update this table as projects are added/completed.

---

## MAINTENANCE

### When to update GLOBAL_PROTOCOL.md
- You've added a new stack you work in
- You've established a new global rule
- Your dev environment changed

### When to update GLOBAL_WARNINGS.md
- Something went wrong on ANY project that could happen again
- Append at the bottom with date — never edit existing lines

### When to update CONVENTIONS.md
- You've settled on a new global coding pattern
- A stack-specific convention has changed

### When NOT to update global files
- Project-specific things → go in `.agent/MEMORY.md` or `.agent/WARNINGS.md`
- Task-specific things → go in `.agent/CURRENT_TASK.md`

---

## AGENT MEMORY UPDATE RULES (for the agent)

```
ALLOWED:
✅ Patch specific lines in .agent/*.md files
✅ Append to .agent/DONE.md
✅ Set .agent/CURRENT_TASK.md to IDLE after task

NOT ALLOWED:
❌ Full rewrite of any .agent/ file
❌ Full rewrite of any global file
❌ Modifying GLOBAL_PROTOCOL.md or GLOBAL_WARNINGS.md
❌ Modifying CONVENTIONS.md
❌ Modifying AGENT_BOOTSTRAP.md or SESSION_START.md
```

---

## TOKEN EFFICIENCY TIPS

1. **Specific file references** in task description = agent reads less = fewer tokens
   - Bad: "fix the navbar"  
   - Good: "fix resources/views/components/navbar.blade.php line 34"

2. **One task per session** = smaller context = less drift

3. **CURRENT_TASK.md** = agent's scratchpad = keep it lean, task-specific only

4. **DONE.md** = one line per task = cheap history without bulk

5. **CODEBASE.md** = route map only, no code = agent navigates without reading every file

---

*Last updated: 2025-05-06*
*System designed by pgwiz × Claude*
