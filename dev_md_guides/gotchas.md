# Project Gotchas & Failure Mode Analysis

_Categorized operational failures, non-obvious runtime bugs, and battle-tested fixes._
_Maintained by the dev-md-compactor Conversational Reflection Protocol._

---

## 1. Major Blockers (Fatal Crashes, Leaks & Data Loss Risks)

### GOTCHA-001: Secret Scanner False-Negatives from Contextual "Example" Words
- **Severity**: Major Blocker (Security / Credential Exposure)
- **Trigger / Symptom**: Secret scanner failed to detect live API keys when the word "example", "sample", or "test" appeared anywhere in the preceding 5 lines or surrounding markdown headers.
- **Root Cause ("Why it failed")**: The detection logic checked whether `any(kw in window_text.lower() for kw in PLACEHOLDER_KEYWORDS)` on a multi-line window around the match. This allowed real secrets placed under `## Example Configuration` headers to silently bypass detection.
- **Exact Fix**: Removed multi-line contextual keyword checks. Switched to evaluating only the matched secret token itself (`is_placeholder(matched_str, line)`) and checking if the token directly contains template placeholders (e.g. `<val>`, `[val]`, `${val}`, `ENC[...]`).
- **Mechanics ("Why the fix worked")**: Evaluating token-level structure prevents false negatives caused by surrounding explanatory prose while maintaining false-positive resistance for sanitized placeholders.

### GOTCHA-002: Accidental Staging of Gitignored `credentials.md`
- **Severity**: Major Blocker (Version Control Leak)
- **Trigger / Symptom**: `credentials.md` was staged via `git add -f` or pre-existing tracking, but `.gitignore` checks reported it as "ignored", masking the active leak risk.
- **Root Cause ("Why it failed")**: Git's `.gitignore` rules only apply to untracked files. Once a file is added to the git index or committed, `.gitignore` has zero effect, allowing credentials to be pushed to GitHub despite being in `.gitignore`.
- **Exact Fix**: Implemented `is_credentials_file_tracked()` using `git ls-files dev_md_guides/credentials.md` in `run_compactor.py` and `gather_context.sh`, alongside `check_credentials_security()` to verify whether the file is staged in `git status --porcelain`.
- **Mechanics ("Why the fix worked")**: Querying the git index directly guarantees detection of staged or committed secrets regardless of `.gitignore` presence.

### GOTCHA-003: Subprocess `UnicodeDecodeError` on Windows Git Logs
- **Severity**: Major Blocker (Process Crash)
- **Trigger / Symptom**: Compactor crashed on Windows when extracting git log messages containing emojis or non-ASCII developer names.
- **Root Cause ("Why it failed")**: Python's `subprocess.run(capture_output=True, text=True)` defaults to the system locale encoding (e.g., `cp1252` on Western Windows), failing when encountering UTF-8 multibyte sequences.
- **Exact Fix**: Explicitly pass `encoding="utf-8", errors="replace"` to all `subprocess.run` invocations.
- **Mechanics ("Why the fix worked")**: Forces UTF-8 decoding while gracefully replacing unmappable bytes with replacement characters (``), preventing unhandled decode exceptions.

---

## 2. Minor Quirks (Silent Defaults, Formatting & Syntax Edge Cases)

### GOTCHA-004: AST Syntax Errors in In-Progress or Non-Python Code
- **Severity**: Minor Quirk
- **Trigger / Symptom**: `extract_ast_symbols()` raised uncaught `SyntaxError` when scanning files with incomplete syntax or mixed syntax.
- **Root Cause ("Why it failed")**: `ast.parse()` raises exceptions on syntax errors; unhandled exceptions halted the compactor run prematurely.
- **Exact Fix**: Wrapped AST parsing and traversal in `try/except Exception: return {"functions": [], "classes": []}`.
- **Mechanics ("Why the fix worked")**: Degrades gracefully to empty symbol lists when code is actively being edited and syntax is temporarily invalid.

### GOTCHA-005: Markdown Table Delimiter and Backtick Truncation
- **Severity**: Minor Quirk
- **Trigger / Symptom**: Environment catalog entries containing multiple backticks (e.g. `host=`node1` port=`9000``) or descriptive comments were truncated or malformed.
- **Root Cause ("Why it failed")**: Naive `split("`")` and indiscriminate stripping discarded internal backticks and trailing notes.
- **Exact Fix**: Check if the string begins and ends with backticks and contains exactly 2 backticks before stripping (`val.startswith("`") and val.endswith("`") and val.count("`") == 2`).
- **Mechanics ("Why the fix worked")**: Strips only true wrapping quotes while preserving internal code formatting and parameter comments.
