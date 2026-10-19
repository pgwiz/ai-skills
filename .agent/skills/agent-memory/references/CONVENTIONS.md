# GLOBAL CONVENTIONS
# Author: {AGENT_USER}
# Location: {AGENT_SYSTEM_PATH}\CONVENTIONS.md
# These apply across ALL projects unless MEMORY.md explicitly overrides

---

## GENERAL

### Naming
- Variables / functions: `camelCase` (JS/TS/Go), `snake_case` (PHP/Python)
- Classes: `PascalCase` always
- Constants: `UPPER_SNAKE_CASE`
- Database columns: `snake_case`
- Database tables: `snake_case`, plural (`staff_members`, `content_edits`)
- File names: `kebab-case` for views/templates, `PascalCase` for classes

### Comments
- Write comments for WHY, not WHAT
- No commented-out dead code in commits
- No TODO comments unless explicitly part of the task

### Error Handling
- Always handle errors — no silent `catch {}` or bare `except: pass`
- User-facing errors: friendly message, not stack traces
- Log errors server-side — never expose internals to client

### Security
- Never hardcode secrets, passwords, API keys
- Always validate and sanitize user input
- Never trust client-side data for auth decisions
- CSRF protection on all state-changing routes

---

## GIT

```bash
# Commit message format
type: short description

# Types: feat, fix, chore, refactor, style, docs, test
# Examples:
feat: add pagination to properties listing
fix: enquire button not showing feedback
chore: extract stats section to Blade component
refactor: move hardcoded content to JSON files
```

- One logical change per commit
- Never commit: `.env`, `node_modules/`, `vendor/`, `__pycache__/`, `.agent/`
- Always on active branch — check MEMORY.md for branch name
- Author: `{AGENT_USER}` — no AI co-author strings ever

---

## LARAVEL / PHP

### Structure
```
Controllers → thin, delegate to services or models
Models → relationships, scopes, accessors
Services → business logic if complex
Requests → validation (FormRequest classes)
Resources → API response transformation
```

### Patterns
```php
// Auth check — always use middleware, not inline
// WRONG:
if (!auth()->check()) return redirect('/login');

// RIGHT: use middleware on route definition

// Response — be consistent with project pattern (check MEMORY.md)
// Common patterns:
return response()->json(['success' => true, 'data' => $data]);
return back()->with('success', 'Message here');
return redirect()->route('route.name')->with('success', 'Message');

// Validation — always use FormRequest or validate()
$request->validate([
    'field' => 'required|string|max:255',
]);
```

### Blade
```blade
{{-- Use directives, not raw PHP --}}
@auth ... @endauth
@can('permission') ... @endcan
@foreach($items as $item) ... @endforeach

{{-- Always escape output --}}
{{ $variable }}          ← escaped (safe)
{!! $variable !!}        ← raw (only for trusted HTML)

{{-- Component pattern --}}
<x-component-name :prop="$value" />
```

### Migrations
- Additive only — never modify existing migration files
- Always add `->nullable()` or `->default()` for new columns on existing tables
- Descriptive names: `add_role_to_staff_table`, `create_content_edit_history_table`

---

## PYTHON / DJANGO / FASTAPI

### Structure (Django)
```
views.py → thin, delegate to services
models.py → fields, relationships, model methods
services.py → business logic
serializers.py → validation + serialization
urls.py → routing only
```

### Structure (FastAPI)
```
routers/ → route definitions
schemas/ → Pydantic models
services/ → business logic
models/ → SQLAlchemy models
dependencies/ → FastAPI Depends()
```

### Patterns
```python
# Always use type hints
def get_user(user_id: int) -> User:

# Async: if project is async, everything is async
async def get_user(user_id: int, db: AsyncSession) -> User:

# Never catch Exception broadly
try:
    ...
except SpecificError as e:
    logger.error(f"Context: {e}")
    raise HTTPException(status_code=400, detail="Friendly message")

# Environment variables
import os
value = os.getenv("KEY", "default")  # always provide default or handle None
```

---

## JAVASCRIPT / NODE / REACT

### Patterns
```javascript
// Always use const/let — never var
const value = ...
let mutable = ...

// Async/await over .then() chains
const data = await fetchData()

// Error handling
try {
    const data = await fetchData()
} catch (error) {
    console.error('Context:', error)
    // handle gracefully
}

// No console.log in committed code
// Use a logger or remove before commit
```

### React
```jsx
// Functional components only
const MyComponent = ({ prop }) => {
    return <div>{prop}</div>
}

// Always handle loading and error states
if (loading) return <Spinner />
if (error) return <ErrorMessage message={error} />
```

---

## GO

```go
// Always handle errors
result, err := someFunc()
if err != nil {
    return fmt.Errorf("context: %w", err)
}

// Use context for cancellation
func handler(ctx context.Context) error {
    select {
    case <-ctx.Done():
        return ctx.Err()
    default:
        // work
    }
}

// No global mutable state
// Pass dependencies explicitly
```

---

## C# / .NET

```csharp
// Always use CancellationToken in workers
public async Task ExecuteAsync(CancellationToken stoppingToken)
{
    while (!stoppingToken.IsCancellationRequested)
    {
        await Task.Delay(1000, stoppingToken);
    }
}

// Task.Delay not Thread.Sleep
await Task.Delay(TimeSpan.FromSeconds(5), cancellationToken);

// Null safety — always check
var value = obj?.Property ?? defaultValue;
```

---

## FLUTTER / DART

```dart
// Always const where possible
const Text('Hello')

// Handle async properly
Future<void> loadData() async {
    try {
        final data = await api.fetch();
        setState(() => _data = data);
    } catch (e) {
        setState(() => _error = e.toString());
    }
}

// No hardcoded strings — use constants or localization
```

---

## DOCKER

```yaml
# Always pin image versions
FROM php:8.3-fpm  ← not php:latest

# Always set working directory
WORKDIR /var/www/html

# Non-root user for app containers
USER www-data

# Health checks on production services
healthcheck:
    test: ["CMD", "curl", "-f", "http://localhost/health"]
    interval: 30s
```

---

## DESIGN (Frontend Projects)

### {AGENT_USER} aesthetic defaults (override per project in MEMORY.md)
- Dark backgrounds preferred
- Typography-forward — pick distinctive fonts, not Inter/Roboto
- Glassmorphism where appropriate
- Grain overlays for depth
- Smooth transitions (200-300ms)
- Mobile-first

### CSS
- Use CSS variables for design tokens
- BEM or utility-first (Tailwind) — check MEMORY.md for project preference
- Never `!important` unless overriding a third-party library
- Never inline styles in production components

---

*Agent: read this file during bootstrap. Do not patch it unless {AGENT_USER} says to.*
*{AGENT_USER}: update this manually when you establish a new global convention.*

