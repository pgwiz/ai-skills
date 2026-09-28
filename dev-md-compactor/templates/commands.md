# Recurring CLI Commands & Tool Invocations (`commands.md`)

_Reference catalog of recurring CLI commands, flags, and platform-specific execution recipes._
_Spawned dynamically when CLI commands recur 3+ times with unique quirks._

---

## 1. Environment & Setup Commands

```bash
# Example environment initialization
python -m venv .venv
source .venv/bin/activate # or .venv\Scripts\Activate.ps1
```

---

## 2. Test Execution Commands

```bash
# Run unit test suite
python -m unittest discover tests

# Verbose single test execution
python -m unittest tests/test_compactor.py -v
```

---

## 3. Maintenance & Compaction Commands

```bash
# Preview compaction state
python dev-md-compactor/scripts/run_compactor.py --report-only

# Run living doc synchronization
python dev-md-compactor/scripts/run_compactor.py
```
