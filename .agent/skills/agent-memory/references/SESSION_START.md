# SESSION START PROMPT
# Location: {AGENT_SYSTEM_PATH}\SESSION_START.md
# Usage: Copy the block below and paste it as your FIRST message to the agent
#        every single session. Edit the [TASK] line only.

---

## THE PROMPT (copy everything between the lines)

─────────────────────────────────────────────────────────────
You are a coding agent working for {AGENT_USER}.

BEFORE ANYTHING ELSE, read these files in order:
1. {AGENT_SYSTEM_PATH}\GLOBAL_PROTOCOL.md
2. {AGENT_SYSTEM_PATH}\GLOBAL_WARNINGS.md
3. .agent/MEMORY.md
4. .agent/CODEBASE.md
5. .agent/WARNINGS.md

If any .agent/ file is missing, run the bootstrap sequence from:
{AGENT_SYSTEM_PATH}\AGENT_BOOTSTRAP.md

After reading all files, confirm:
- Project name
- Active branch
- The task you are about to do
- Files you will touch

Then begin.

TASK: [describe the task here]
─────────────────────────────────────────────────────────────

---

## EXAMPLES

### Example 1 — Bug fix
```
TASK: Fix the enquire button on the property detail page.
      It submits but shows no success/error feedback to the user.
      File is likely resources/views/pages/property-detail.blade.php
      and EnquiryController@store.
```

### Example 2 — New feature
```
TASK: Add pagination to the admin properties listing.
      Currently loads all records. Use Laravel paginate(15).
      Route: admin/properties (GET)
```

### Example 3 — Refactor
```
TASK: Extract the stats section from resources/views/pages/home.blade.php
      into a Blade component at resources/views/components/stats-section.blade.php
      No logic change — pure extraction.
```

### Example 4 — New project bootstrap
```
TASK: Bootstrap the .agent/ memory system for this project.
      Then give me a summary of what you found.
```

---

## TIPS

- **One task per session** — don't stack multiple unrelated tasks
- **Be specific about files** — "the navbar" is vague, "resources/views/components/navbar.blade.php" is not
- **State what you expect** — "it should show a toast on success" gives the agent a clear acceptance criterion
- **If continuing a previous session** — start with "Continue from last session. Check DONE.md for what was completed."

---

## FOR JETBRAINS USERS (your setup)

In PyCharm / Rider, you can set this up as a Live Template:
- Go to Settings → Editor → Live Templates
- Create template abbreviation: `agentstart`
- Paste the prompt block as the template body
- Use `$TASK$` as the variable

Then type `agentstart` + Tab in any editor and it expands.

---

## CONTINUING A SESSION (task was interrupted)

```
─────────────────────────────────────────────────────────────
Read .agent/CURRENT_TASK.md — there is an interrupted task.
Read .agent/MEMORY.md and .agent/CODEBASE.md for context.
Read {AGENT_SYSTEM_PATH}\GLOBAL_PROTOCOL.md for rules.

Summarize where you left off based on CURRENT_TASK.md,
then ask if you should continue or the task changed.
─────────────────────────────────────────────────────────────
```

---

## REVIEWING WHAT WAS DONE (audit session)

```
─────────────────────────────────────────────────────────────
Read .agent/DONE.md and summarize the last 5 completed tasks.
Read .agent/MEMORY.md and tell me if any patterns look wrong
or outdated based on recent DONE.md entries.
Do not touch any source files.
─────────────────────────────────────────────────────────────
```

