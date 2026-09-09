# **Advanced Context Compaction and Living Documentation Architecture for Autonomous Engineering Agents**

Context window saturation is one of the most critical failure modes in autonomous AI software engineering agents1. As interactive coding sessions progress, conversation logs accumulate terminal outputs, Abstract Syntax Tree (AST) representations, file diffs, and intermediate tool responses2. This unmanaged expansion degrades agent reasoning, dilutes system prompt instructions, and drastically increases token expenditure3.  
To overcome the inherent statelessness of Large Language Model (LLM) agent sessions without suffering from cumulative context degradation, software systems require a deterministic externalized memory architecture1. Rather than relying on lossy end-of-session natural language summarization, modern agent architectures employ structured, file-based compaction engines4.  
This report provides an in-depth technical analysis and implementation framework for an automated context compaction engine. The system transforms transient agent conversations, code mutations, and execution logs into a consolidated repository memory bank housed within a dedicated directory (dev\_md\_guides/), structured across five core schemas: branch.md, features.md, structure.md, memory.md, and changelog.md2.

## **Theoretical Frameworks and Precedents in Agentic Memory Persistence**

Managing persistent agent state requires balancing retrieval accuracy, operational token overhead, and document staleness5. Several industry frameworks have emerged to tackle these dynamics.

### **Memory Bank Architecture: Cline and Roo Code**

The Memory Bank methodology, popularized within the Cline and Roo Code ecosystems, operationalizes agent context by transforming ephemeral memory into an explicit file-based cache stored within the project tree, conventionally inside a memory-bank/ directory2. In this paradigm, the agent is instructed through system rules that its internal cognitive state resets completely between operational sessions1. Continuity is preserved through a mandatory initialization and update lifecycle governed by structured Markdown files, typically separating product rationale, architectural patterns, active tasks, and milestone progress1.  
While effective at maintaining continuity across disconnected development sessions, naive implementations of the Memory Bank pattern suffer from significant operational overhead2. Forcing an agent to read five to six comprehensive Markdown files at the onset of every turn consumes thousands of tokens before execution begins2. In larger codebases, this overhead inflates input costs and crowds out the context window required for deep code comprehension10. Consequently, advanced implementations transition from monolithic read cycles to progressive disclosure, wherein the agent accesses broad architectural overviews by default and selectively queries detailed operational logs only on demand5.

### **The Claude Code Compaction Lifecycle**

Within Anthropic’s Claude Code CLI ecosystem, context window management is divided into three distinct operational mechanisms: microcompaction, auto-compaction, and manual task-boundary compaction4.  
Microcompaction monitors high-volume tool outputs, such as comprehensive file dumps or compilation logs, for token bloat4. When outputs surpass designated boundaries, the agent offloads the full verbose buffer to local disk storage and preserves only an abstracted reference or file path in the active context, maintaining reasoning capacity while preventing conversational buffer blowup4.  
Auto-compaction triggers automatically when conversational history approaches the physical limit of the model's context window, typically around 95% capacity3. At this stage, the runtime calculates an operational headroom ceiling:  
![][image1]  
The engine appends a system-level compact boundary document into the session log, replacing preceding conversational turns with an abstracted summary checkpoint4.  
Task-boundary compaction addresses the cognitive degradation inherent to automated compactions executed under memory strain6. Because late-stage context is heavily diluted by irrelevant intermediate failures, automated summaries often discard critical project invariants and subtle architectural rules6. Industry best practices dictate triggering compaction manually via dedicated commands at approximately 60% context utilization or immediately upon completing discrete engineering milestones4.

### **Hierarchical Three-Layer Memory Topology**

To prevent documentation from devolving into unmaintainable bloat, modern autonomous architectures bifurcate memory into three discrete operational tiers5:  
Hot Memory serves as the execution protocol and is injected directly into the system prompt or root-level agent instructions, such as AGENTS.md or CLAUDE.md5. This layer contains deterministic command strings, lint gates, build triggers, and active path pointers, strictly bounded to fewer than 500 lines to minimize persistent per-turn token spend5.  
Working Memory encompasses session ephemera, including active conversation buffers, short-term scratchpads, AST search fragments, and recent tool outputs3. Working memory is kept transient and is subject to aggressive microcompaction and terminal pruning3.  
Cold Memory functions as externalized living documentation, storing structured on-disk records such as Architecture Decision Records (ADRs), repository blueprints, and changelogs5. Cold memory is never parsed in its entirety into the active prompt; instead, the agent utilizes deterministic Just-In-Time (JIT) retrieval tools to read specific document slices when relevant5.

## **Comparative Analysis of State Persistence and Repository Packing Architectures**

To establish the technical foundation for the dev\_md\_guides/ engine, it is necessary to evaluate how various agentic persistence and repository packing architectures handle state extraction, token overhead, and file structures.

| Tool / Framework | Primary State Medium | Structural Code Awareness | Token Overhead Profile | Primary Strength | Critical Failure Mode |
| :---- | :---- | :---- | :---- | :---- | :---- |
| **Cline / Roo Code Memory Bank** \[cite: 2, 8, 12, 13\] | Monolithic Markdown files (memory-bank/\*.md)2 | Manual agent narration; lacks native AST parser1 | High (![][image2]–![][image3] tokens injected per session turn)2 | Clear human-readable separation of business and technical goals1 | Severe token burn; context thrashing on rapid iterative loops2 |
| **Claude Code Native Compaction** \[cite: 3, 4, 7, 9\] | Local JSONL logs \+ inline summary boundary tokens9 | None; relies on prompt-based conversational compression4 | Variable; compresses active context by 60%–85% upon trigger9 | Zero-configuration operational continuation; native CLI integration4 | Cumulative information loss; system rules and edge constraints frequently lost across boundaries3 |
| **Aider Repo Map** \[cite: 19, 20, 21, 22\] | Dynamic in-memory AST context window injection20 | High; tree-sitter AST queries with personalized PageRank19 | Optimized; strict token budget fitting (default 1,024 tokens)20 | Surfaces relevant function signatures and call graphs dynamically20 | Transient; retains no historical decision memory or long-term operational narrative11 |
| **Repomix / Repoprep** \[cite: 25, 26, 27\] | Single flat file (XML, Markdown, or JSON export)25 | Medium; parses ignore files and can extract signatures via tree-sitter25 | Massive when uncompressed; 60%–90% reduction in signature/tree mode5 | Excellent for bootstrapping cold models lacking filesystem access5 | Read-only static snapshot; lacks differential update capabilities for active agent workflows5 |
| **Sentra / Graph Memory** \[cite: 11\] | Bi-temporal knowledge graph database11 | High; live semantic dependency indexing with code sync11 | Highly compressed; queries pull resolved facts rather than file trees11 | Eliminates hallucination on deprecated patterns via absence tracking11 | Requires dedicated external database infrastructure and runtime service11 |

The analysis indicates that an optimal architecture must combine the file-based simplicity and human-readability of the Memory Bank with the token discipline of Aider’s AST-based extraction and Claude Code's task-boundary compaction hooks4.

## **Schema Specification for the dev\_md\_guides Documentation Engine**

The compaction directory (dev\_md\_guides/) serves as a deterministic external storage engine. To maximize retention and minimize parsing errors during rehydration, each file adheres to a standardized structural schema governed by RFC 2119 constraints and non-skipping heading hierarchies5.

### **Target File Roles and Update Dynamics**

| File Name | Functional Scope and Core Responsibility | Update Trigger | Primary Data Sources | Ingestion Strategy |
| :---- | :---- | :---- | :---- | :---- |
| branch.md | Tracks active Git branch state, base diverge commit, upstream tracking, and uncommitted diff surface5 | Git branch switch, initial session load, pre-merge verification | git status, git log, git rev-parse | Injected into Hot Memory during planning phases5 |
| features.md | Tracks Specification-Driven Development (SDD) states, active feature matrices, acceptance criteria, and task checklists5 | Feature requirement additions, completion of task steps | Agent conversation, user prompts, test suites | Read by agent when planning or picking up pending tasks4 |
| structure.md | Maps repository topology, module classification, package roles, and cross-folder import dependencies5 | Creation, movement, or deletion of files/directories | Filesystem scan, AST import analyzers, package manifests | Selective retrieval via section headers or JIT search5 |
| memory.md | Captures immutable architectural invariants, Architecture Decision Records (ADRs), trade-offs, and rejected options5 | Explicit architectural decisions, framework migrations | User constraints, agent debate logs, ADR authoring | Read during system design; preserved across compactions4 |
| changelog.md | Detailed chronological audit log of operational actions, modified functions/classes, build executions, and test runs5 | Successful execution of compaction pipeline | git diff \--function-context, AST diff, bash exit codes5 | Cold append-only storage; historical audit trail5 |

### **Structural File Schemas**

#### **dev\_md\_guides/branch.md**

This document tracks the working Git topology, ensuring that an agent rehydrating after context loss does not attempt invalid merges, push to protected targets, or misidentify the base lineage5.

# **Branch State & Worktree Topology**

* **Active Branch**: feat/oauth2-stateless-flow  
* **Base Integration Branch**: origin/main  
* **Tracking Status**: Ahead 3 commits, behind 0 commits  
* **HEAD Commit**: a1c4e9f \- *feat(auth): add PKCE challenge generator*  
* **Base Ancestor Commit**: e8b2110 \- *chore: bump core dependencies*

## **Divergence Analysis**

* **Commits on Branch (Local)**:  
  * a1c4e9f (2026-03-30 14:10:02 UTC) \- feat(auth): add PKCE challenge generator  
  * 7d2e09a (2026-03-30 11:22:15 UTC) \- test(auth): add failing test for state mismatch  
  * c0128fa (2026-03-29 18:45:00 UTC) \- refactor(session): isolate token storage  
* **Uncommitted Working Tree State**:  
  * M src/auth/pkce.py (Staged: No, Unstaged: Yes, Lines: \+42/-5)  
  * ?? src/auth/crypto\_utils.py (Untracked)

## **Integration Checklist**

* \[ \] Working tree cleanly committed or stashed  
* \[ \] Rebase onto latest origin/main verified  
* \[ \] No fast-forward conflicts detected

#### **dev\_md\_guides/features.md**

This file implements Spec-Driven Development (SDD), tracking feature scope, operational rationale, validation criteria, and granular task completion states4.

# **Feature Roadmap & SDD Progress Matrix**

## **Active Feature: Stateless PKCE OAuth2 Implementation**

* **Status**: IN\_PROGRESS (Phase 2 of 3\)  
* **Initiating User Prompt**: "Refactor auth flow to support PKCE for single-page applications without server-side session stores."  
* **Target Completion Metric**: All cryptographic assertions pass; zero state stored in memory; coverage \>= 90%.

### **Sub-Task Breakdown**

* \[x\] **Task 1: Challenge Generation** (Completed: 2026-03-30)  
  * *Details*: Implement RFC 7636 compliant code verifier and S256 code challenge generator.  
  * *Verification Command*: pytest tests/auth/test\_pkce.py \-k test\_generate\_challenge (Passed).  
* \[/\] **Task 2: Verification Endpoint** (In Progress)  
  * *Details*: Create route handler validating code\_verifier against hashed session token.  
  * *Blockers*: Needs crypto provider abstraction to support HSM mock in CI.  
* \[ \] **Task 3: Production Build & Deployment Pipeline** (Pending)  
  * *Details*: Add Docker build stage and production environment variables.

### **Acceptance Verification Log**

* tests/auth/test\_pkce.py: 12 passed, 0 failed.  
* Static type check: mypy \--strict src/auth/: 0 errors found.

#### **dev\_md\_guides/structure.md**

structure.md provides an AST-derived structural map of the repository5. Instead of listing every raw file verbatim, it categorizes modules by architectural function and documents explicit inter-folder import dependencies5.

# **Codebase Architecture & Directory Dependency Graph**

## **Top-Level Module Topography**

* src/api/ \[Role: Gateway & Controllers\]  
  * Entry point: src/api/server.py  
  * Responsibilities: HTTP routing, parameter validation, rate limiting.  
  * Internal Consumers: Client applications, reverse proxy.  
  * External Dependencies: fastapi, pydantic.  
* src/auth/ \[Role: Domain Engine\]  
  * Entry point: src/auth/service.py  
  * Responsibilities: Token issuance, PKCE validation, signature verification.  
  * Internal Consumers: src/api/routes/auth.py.  
  * External Dependencies: cryptography, pyjwt.  
* src/db/ \[Role: Persistence Layer\]  
  * Entry point: src/db/session.py  
  * Responsibilities: SQLAlchemy ORM mappings, Alembic migration runners.  
  * Internal Consumers: src/auth/, src/api/.

## **Architectural Invariant Rules**

* **Dependency Flow**: src/api/ \-\> src/auth/ \-\> src/db/.  
* **Prohibited Imports**: Code in src/db/ MUST NOT import from src/api/ or src/auth/.  
* **Boundary Gates**: Database models are never directly exposed to HTTP handlers; models MUST map through Pydantic schemas in src/api/schemas/.

#### **dev\_md\_guides/memory.md**

memory.md preserves project decisions, system invariants, and historical constraints, preventing the agent from repeating previously rejected technical attempts across multiple compactions4.

# **Project Memory Bank & Architecture Decision Records (ADR)**

## **ADR-0004: Migration from State-Backed Sessions to Stateless JWT with PKCE**

* **Date**: 2026-03-29  
* **Status**: ACCEPTED  
* **Context**: Scaling the user service across multiple geographic regions resulted in high Redis replication latency for session lookups.  
* **Decision**: Deprecate Redis-backed sessions. All new authentication requests must utilize RFC 7636 PKCE code challenges paired with short-lived RS256-signed JWTs.  
* **Consequences**:  
  * *Positive*: Redis cluster requirement eliminated for read-heavy authentication paths; latency dropped from 45ms to 2ms.  
  * *Negative*: Client revocation requires blacklisting compromised JWT IDs in a synchronized Bloom filter.  
* **Rejected Alternatives**:  
  * *Sticky Session Routing*: Rejected due to uneven load distribution on edge instances.  
  * *Distributed Redis Locks*: Rejected due to cross-region WAN partition vulnerabilities.

## **Operational Invariants & Ground Truths**

* All environment variables MUST be validated via pydantic-settings at startup.  
* Under zero circumstances may API secrets be written to terminal outputs, tests, or error logs.  
* Python imports MUST follow PEP 8 grouping: standard library, third-party, local modules.

#### **dev\_md\_guides/changelog.md**

The changelog provides an append-only, deterministic record of every operational step performed during the agent's interactive run, capturing modified functions, command outputs, and build results5.

# **Session Operational Changelog**

## **Session Run: 2026-03-30 15:45:12 UTC**

* **Trigger**: Compaction Phase at Task Boundary (Task 1 completion)  
* **User Intent**: Implement PKCE challenge generator and wire into auth router.

### **AST & Code Modifications**

* **Modified File**: src/auth/pkce.py  
  * *Added Functions*:  
    * generate\_code\_verifier(length: int \= 64\) \-\> str (Lines 15-28)  
    * generate\_code\_challenge(verifier: str) \-\> str (Lines 30-44)  
  * *Modified Functions*:  
    * validate\_pkce\_request(req: AuthRequest) \-\> bool (Lines 60-85; added S256 transform logic)  
* **Modified File**: tests/auth/test\_pkce.py  
  * *Added Test Cases*:  
    * test\_generate\_code\_verifier\_entropy()  
    * test\_challenge\_hash\_rfc7636\_vector()

### **Operational Commands & Execution Audit**

* **Command**: poetry run pytest tests/auth/test\_pkce.py  
  * *Exit Code*: 0 (SUCCESS)  
  * *Execution Time*: 1.42s  
  * *Result*: 12 passed, 0 failures.  
* **Command**: docker build \-t app-service:test .  
  * *Exit Code*: 0 (SUCCESS)  
  * *Output Artifact*: Image ID sha256:8f1e29c0 (Size: 184MB).

### **Context Continuity State**

* **Compacted Tokens Reclaimed**: \~34,500 tokens  
* **Active Context Injected**: dev\_md\_guides/features.md, dev\_md\_guides/branch.md  
* **Next Required Step**: Implement verification route handler in src/api/routes/auth.py.

## **Deterministic Operational Data Extraction Pipelines**

A key flaw in traditional memory frameworks is relying entirely on the LLM's conversational memory to recount what functions changed, what builds occurred, and how directories are linked1. Relying on model recall leads to hallucinations, missing parameters, and omitted error traces11. Instead, context compaction must use a hybrid extraction model: native system utilities and AST parsers extract deterministic ground truth, while the LLM generates higher-level architectural summaries5.

### **Extraction of Modified Functions and AST Signatures**

To identify the exact functions and methods modified during a development turn, the system should avoid reading raw, unparsed Git diffs, which consume excessive token space5. Instead, two complementary mechanisms provide function-level granularity:  
Git function-context parsing utilizes flags such as \-W and \--function-context to instruct Git's internal diff engine to extend hunk boundaries across the entire surrounding function or class scope31. Configuring .gitattributes with language-specific diff definitions (such as mapping Python or TypeScript files to their corresponding internal drivers) guarantees that hunk headers accurately surface semantic function signatures in diff outputs rather than showing ambiguous parent scopes34.  
For exact structural analysis, an Abstract Syntax Tree visitor parses source code into an in-memory syntax tree, comparing AST nodes between revisions to identify added, modified, or removed functions and classes without executing runtime code20. This syntactic differentiation isolates exported interfaces, parameters, and return types, producing a clean structural digest for inclusion in the operational changelog20.

### **Automated Dependency Graph and Directory Structure Extraction**

Constructing an accurate architectural map requires extracting inter-module dependencies while filtering out transient build artifacts and external vendor packages26. The extraction engine systematically walks the repository root, ignoring directories matching standard exclusion patterns (such as version control directories, virtual environments, and package caches)26. Within each source file, top-level import declarations are parsed to construct a directed dependency graph:  
![][image4]  
Where ![][image5] represents the set of project modules and top-level directories, and ![][image6] represents the directed dependency edges between modules. By aggregating file-level imports up to the directory level, the engine automatically calculates module dependencies30.

### **Build Pipeline and Production Verification Capture**

Capturing build and test status requires intercepting terminal tool executions4. The compaction engine intercepts command invocations, capturing:

* The exact CLI command executed (e.g., package build, test runner, container compile)5.  
* Process execution duration and system exit codes35.  
* A compressed extraction of standard error or standard output, preserving tracebacks and build digests while discarding high-volume progress streams7.

## **Agent Skill Specification and Automation Framework**

The Agent Skills open standard (agentskills.io), adopted natively across modern agent environments such as Claude Code, defines a portable, file-based interface for extending agent capabilities15. A skill is packaged as a self-contained directory containing a required SKILL.md file (composed of YAML frontmatter and instructional Markdown) alongside optional executable scripts and reference documentation15.

### **Skill Directory Structure**

The skill is organized within the local or global agent configuration tree according to standard filesystem conventions:

* Root directory: .claude/skills/compact-session/  
* Specification file: .claude/skills/compact-session/SKILL.md  
* Executable script directory: .claude/skills/compact-session/scripts/  
* Extraction engine script: .claude/skills/compact-session/scripts/run\_compactor.py

### **The SKILL.md Specification**

The SKILL.md file declares when the agent should trigger compaction, what tools it is permitted to invoke, and how it must rehydrate context15.

## **name: compact-session description: Compacts the ongoing conversation, code changes, AST modifications, and build actions into dev\_md\_guides/ documentation files (branch.md, features.md, structure.md, memory.md, changelog.md). Use when the user asks to "compact memory", "save session state", "update dev guides", "compact context", or when approaching token capacity limits. version: 1.0.0 license: MIT compatibility: Python \>= 3.10, git \>= 2.25 allowed-tools: Bash(python:*) Bash(git:*) Read Write metadata: category: workflow-optimization target\_directory: dev\_md\_guides**

# **Session Compactor & Living Documentation Engine**

## **Operational Purpose**

This skill deterministically aggregates interactive session context, AST code modifications, directory structure, and Git metadata into persistent, structured files within dev\_md\_guides/.

## **Execution Protocol**

When this skill is activated:

> 1. **Execute Extraction Script**: Run the deterministic Python compaction engine:bash python .claude/skills/compact-session/scripts/run\_compactor.py  
> 2. **Review Extracted Files**: Inspect the modified files in dev\_md\_guides/:  
   * branch.md  
   * features.md  
   * structure.md  
   * memory.md  
   * changelog.md  
> 3. **LLM Enrichment Pass**:  
   * Open dev\_md\_guides/features.md and ensure the current task description and completion status reflect the immediate conversational intent.  
   * Open dev\_md\_guides/memory.md and append any newly established architectural decisions or explicit user constraints made during this session.  
> 4. **Context Rehydration**: Inform the user that context has been preserved in dev\_md\_guides/. If continuing under a new or cleared session, read features.md and branch.md to resume execution without loss of momentum.

\#\#\# The Deterministic Extraction Script (\`run\_compactor.py\`)

This standalone Python script extracts the repository's ground truth, parses modified functions via Python's AST parser, generates an import dependency map, and populates \`dev\_md\_guides/\` \[cite: 35, 37, 38\].

\`\`\`python  
\#\!/usr/bin/env python3  
"""  
Deterministic Context Compactor & Markdown Guide Generator  
Target Directory: dev\_md\_guides/  
Files Managed: branch.md, features.md, structure.md, memory.md, changelog.md  
"""

import os  
import sys  
import subprocess  
import datetime  
import ast  
from pathlib import Path

GUIDES\_DIR \= Path("dev\_md\_guides")

def run\_cmd(cmd: list\[str\]) \-\> str:  
    try:  
        res \= subprocess.run(cmd, capture\_output=True, text=True, check=True)  
        return res.stdout.strip()  
    except Exception:  
        return ""

def get\_git\_branch\_info() \-\> dict:  
    branch \= run\_cmd(\["git", "rev-parse", "--abbrev-ref", "HEAD"\]) or "unknown"  
    head\_hash \= run\_cmd(\["git", "rev-parse", "--short", "HEAD"\]) or "none"  
    head\_msg \= run\_cmd(\["git", "log", "-1", "--pretty=%B"\]) or "No commits"  
    status\_raw \= run\_cmd(\["git", "status", "--porcelain"\])  
      
    uncommitted \= \[\]  
    if status\_raw:  
        for line in status\_raw.splitlines():  
            uncommitted.append(line.strip())  
              
    recent\_commits \= \[\]  
    log\_raw \= run\_cmd(\["git", "log", "-5", "--pretty=format:%h|%ad|%s", "--date=iso"\])  
    if log\_raw:  
        for line in log\_raw.splitlines():  
            parts \= line.split("|", 2\)  
            if len(parts) \== 3:  
                recent\_commits.append(parts)

    return {  
        "branch": branch,  
        "head\_hash": head\_hash,  
        "head\_msg": head\_msg.splitlines()\[0\] if head\_msg else "",  
        "uncommitted": uncommitted,  
        "recent\_commits": recent\_commits  
    }

def extract\_ast\_functions(file\_path: Path) \-\> dict\[str, list\[str\]\]:  
    """Extracts top-level functions and class methods from a Python file."""  
    if not file\_path.exists() or file\_path.suffix \!= ".py":  
        return {"functions": \[\], "classes": \[\]}  
      
    try:  
        content \= file\_path.read\_text(encoding="utf-8")  
        tree \= ast.parse(content, filename=str(file\_path))  
    except Exception:  
        return {"functions": \[\], "classes": \[\]}

    functions \= \[\]  
    classes \= \[\]  
    for node in tree.body:  
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):  
            functions.append(f"{node.name}(line:{node.lineno})")  
        elif isinstance(node, ast.ClassDef):  
            methods \= \[  
                n.name for n in node.body   
                if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef))  
            \]  
            classes.append(f"{node.name} \[methods: {', '.join(methods)}\]")

    return {"functions": functions, "classes": classes}

def get\_modified\_functions() \-\> list\[dict\]:  
    """Identifies modified Python files and extracts modified identifiers."""  
    diff\_output \= run\_cmd(\["git", "diff", "--name-only", "HEAD"\])  
    changed\_files \= \[Path(f) for f in diff\_output.splitlines() if f.endswith(".py")\]  
      
    results \= \[\]  
    for f in changed\_files:  
        if f.exists():  
            signatures \= extract\_ast\_functions(f)  
            results.append({  
                "file": str(f),  
                "functions": signatures\["functions"\],  
                "classes": signatures\["classes"\]  
            })  
    return results

def build\_structure\_graph(root\_dir: Path) \-\> tuple\[dict, dict\]:  
    """Scans directories and maps internal cross-folder import dependencies."""  
    ignored \= {".git", ".venv", "venv", "node\_modules", "\_\_pycache\_\_", "dev\_md\_guides"}  
    dir\_summary \= {}  
    imports\_map \= {}

    for path in root\_dir.rglob("\*.py"):  
        if any(part in ignored for part in path.parts):  
            continue  
          
        parent \= str(path.parent)  
        dir\_summary.setdefault(parent, \[\]).append(path.name)  
          
        try:  
            tree \= ast.parse(path.read\_text(encoding="utf-8"))  
            for node in ast.walk(tree):  
                if isinstance(node, ast.ImportFrom) and node.module:  
                    mod\_root \= node.module.split(".")\[0\]  
                    imports\_map.setdefault(parent, set()).add(mod\_root)  
        except Exception:  
            continue

    return dir\_summary, imports\_map

def write\_branch\_md(branch\_info: dict):  
    out \= \[  
        "\# Branch State & Worktree Topology",  
        f"- \*\*Active Branch\*\*: \`{branch\_info\['branch'\]}\`",  
        f"- \*\*HEAD Commit\*\*: \`{branch\_info\['head\_hash'\]}\` \- {branch\_info\['head\_msg'\]}",  
        f"- \*\*Last Updated\*\*: {datetime.datetime.now(datetime.timezone.utc).isoformat()}",  
        "",  
        "\#\# Recent Commits",  
    \]  
    for c in branch\_info\["recent\_commits"\]:  
        out.append(f"- \`{c\[0\]}\` ({c\[1\]}): {c\[2\]}")  
      
    out.extend(\["", "\#\# Uncommitted Working Tree State"\])  
    if branch\_info\["uncommitted"\]:  
        for u in branch\_info\["uncommitted"\]:  
            out.append(f"- \`{u}\`")  
    else:  
        out.append("- \*Working tree clean. No uncommitted modifications.\*")  
      
    (GUIDES\_DIR / "branch.md").write\_text("\\n".join(out) \+ "\\n", encoding="utf-8")

def write\_structure\_md(dir\_summary: dict, imports\_map: dict):  
    out \= \[  
        "\# Codebase Architecture & Directory Dependency Graph",  
        f"- \*\*Generated At\*\*: {datetime.datetime.now(datetime.timezone.utc).isoformat()}",  
        "",  
        "\#\# Module Directory Topography"  
    \]  
    for d, files in sorted(dir\_summary.items()):  
        out.append(f"\#\#\# \`{d}/\`")  
        out.append(f"- \*\*Files ({len(files)})\*\*: {', '.join(files\[:10\])}{'...' if len(files) \> 10 else ''}")  
        deps \= imports\_map.get(d, set())  
        if deps:  
            out.append(f"- \*\*Discovered Module References\*\*: {', '.join(sorted(deps))}")  
        out.append("")  
          
    (GUIDES\_DIR / "structure.md").write\_text("\\n".join(out) \+ "\\n", encoding="utf-8")

def write\_changelog\_md(modified\_nodes: list\[dict\]):  
    log\_path \= GUIDES\_DIR / "changelog.md"  
    existing \= log\_path.read\_text(encoding="utf-8") if log\_path.exists() else "\# Session Operational Changelog\\n"  
      
    timestamp \= datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")  
    entry \= \[  
        f"\\n\#\# Operational Run: {timestamp}",  
        "- \*\*Event\*\*: Automated Context Compaction",  
        "\#\#\# AST Code Inspections"  
    \]  
      
    if modified\_nodes:  
        for mod in modified\_nodes:  
            entry.append(f"- \*\*File\*\*: \`{mod\['file'\]}\`")  
            if mod\["functions"\]:  
                entry.append(f"  \- \*Functions\*: {', '.join(mod\['functions'\])}")  
            if mod\["classes"\]:  
                entry.append(f"  \- \*Classes\*: {', '.join(mod\['classes'\])}")  
    else:  
        entry.append("- \*No Python AST structural alterations detected in diff.\*")  
          
    entry.append("\\n---\\n")  
    log\_path.write\_text(existing \+ "\\n".join(entry), encoding="utf-8")

def init\_static\_files():  
    """Initializes features.md and memory.md if they do not exist."""  
    features\_path \= GUIDES\_DIR / "features.md"  
    if not features\_path.exists():  
        features\_path.write\_text(  
            "\# Feature Roadmap & SDD Progress Matrix\\n\\n"  
            "\#\# Active Feature: Session Compaction Engine\\n"  
            "- \*\*Status\*\*: IN\_PROGRESS\\n"  
            "- \*\*Current Milestone\*\*: Initializing automated guide structures.\\n\\n"  
            "\#\#\# Tasks\\n"  
            "- \[x\] Create deterministic extraction scripts\\n"  
            "- \[/\] Execute compaction lifecycle pass\\n"  
            "- \[ \] Verify AST diffs in changelog\\n",  
            encoding="utf-8"  
        )  
          
    memory\_path \= GUIDES\_DIR / "memory.md"  
    if not memory\_path.exists():  
        memory\_path.write\_text(  
            "\# Project Memory Bank & Architecture Decision Records (ADR)\\n\\n"  
            "\#\# ADR-0001: Structured File-Based Compaction\\n"  
            "- \*\*Status\*\*: ACCEPTED\\n"  
            "- \*\*Context\*\*: LLM agent sessions lose operational context across restarts.\\n"  
            "- \*\*Decision\*\*: Externalize memory into \`dev\_md\_guides/\` directory.\\n"  
            "- \*\*Invariants\*\*:\\n"  
            "  \- All compaction operations MUST update \`branch.md\` and \`changelog.md\`.\\n"  
            "  \- Code modifications MUST pass lint and test gates before PR creation.\\n",  
            encoding="utf-8"  
        )

def main():  
    GUIDES\_DIR.mkdir(parents=True, exist\_ok=True)  
    init\_static\_files()  
      
    branch\_info \= get\_git\_branch\_info()  
    write\_branch\_md(branch\_info)  
      
    dir\_summary, imports\_map \= build\_structure\_graph(Path("."))  
    write\_structure\_md(dir\_summary, imports\_map)  
      
    modified\_nodes \= get\_modified\_functions()  
    write\_changelog\_md(modified\_nodes)  
      
    print("\[COMPACTOR\] Successfully refreshed dev\_md\_guides/ documentation.")

if \_\_name\_\_ \== "\_\_main\_\_":  
    main()

### **Automation Hooks for Seamless Execution**

Relying entirely on manual invocation introduces human error, as developers frequently forget to trigger compaction before ending sessions or switching git branches5. Integrating execution hooks guarantees that documentation remains synchronized with underlying code changes16.  
Within Claude Code environments, this is achieved by registering a lifecycle hook under PostToolUse targeting the compact event16. Whenever a compaction boundary is generated, the runtime executes the extraction script automatically:

JSON  
{  
  "hooks": {  
    "PostToolUse": \[  
      {  
        "matcher": "compact",  
        "command": "python .claude/skills/compact-session/scripts/run\_compactor.py"  
      }  
    \]  
  }  
}

Within Cursor environments, the workflow is governed using a project rule configured via .cursor/rules/compaction.mdc14. By enforcing global application across the project tree, the rule ensures that the agent reads and updates the living documentation throughout execution14:

## **description: Enforces session state continuity from dev\_md\_guides globs: \["/\*"\] alwaysApply: true**

# **Operational Memory Protocol**

Before initiating any multi-file code modifications:

> 1. Verify active tasks in dev\_md\_guides/features.md.  
> 2. Ensure working branch status matches dev\_md\_guides/branch.md.  
> 3. Read architectural invariants in dev\_md\_guides/memory.md.  
> 4. When concluding a major task, invoke the compact-session skill to persist operational changes.

## **Operational Trade-Offs and Governance Dynamics**

Implementing automated compaction workflows introduces distinct engineering trade-offs regarding execution latency, token expenditure, and semantic fidelity5.

### **Maintenance Paradigms: Manual vs. Hook-Based vs. Subagent Execution**

Choosing how to maintain project state determines the long-term reliability and operational overhead of the development environment5.

| Operational Vector | Manual Markdown Updates | Automated Shell/Tool Hooks | Autonomous Subagent Forking |
| :---- | :---- | :---- | :---- |
| **Trigger Mechanism** | Explicit user request or developer edit2 | Event-driven lifecycle hooks (PostToolUse)16 | Automated background delegation (context: fork)7 |
| **Token Cost Profile** | High in-session overhead; updates consume primary context2 | Zero prompt tokens for extraction; CLI runs out-of-band16 | Isolated context tokens; runs in secondary subagent window7 |
| **Information Nuance** | High qualitative depth; captures human intent and rationale5 | High structural precision; lacks qualitative synthesis5 | Balanced; combines AST extraction with LLM reasoning7 |
| **Failure Vulnerability** | High omission risk; developers forget to document during rapid iterations5 | Execution brittleness; script failures fail silently39 | API orchestration latency; higher background token spend7 |

Manual authoring delivers rich qualitative explanations of architectural intent, yet frequently suffers from omission during high-velocity coding sessions, causing documentation to drift from code reality5. Automated lifecycle hooks resolve this omission risk by enforcing deterministic filesystem updates, but they lack the capacity to synthesize abstract architectural intent without an accompanying LLM turn5.  
The most robust paradigm leverages autonomous subagents running in isolated execution contexts7. When conversational memory approaches operational thresholds, a secondary subagent is spawned via a forked context6. This subagent runs the deterministic extraction script, synthesizes high-level rationale from conversational logs, writes the updated Markdown artifacts to dev\_md\_guides/, and reports completion back to the primary session without consuming primary context tokens4.

### **Mitigating Cumulative Information Loss and Semantic Drift**

A critical failure mode in recurrent compaction architectures is cumulative degradation, often termed the "game of telephone" effect3. When an agent compresses a conversational history that was itself reconstructed from an earlier compression, subtle architectural invariants degrade exponentially:  
![][image7]  
Where ![][image8] represents the loss coefficient per compaction cycle and ![][image9] represents the compaction generation index.  
To halt this exponential loss, dev\_md\_guides/memory.md must be treated as an immutable ground truth5. Compaction scripts must never overwrite historical ADR entries or system invariants with lossy conversational summaries5. Instead, the compaction engine executes append-only operations on memory.md and changelog.md, while executing deterministic, full-state refreshes on branch.md and structure.md5. Anchoring the agent to durable filesystem records eliminates semantic drift and maintains structural coherence across extended development lifecycles1.

## **Operational Deployment Sequence**

Rolling out the dev\_md\_guides/ compaction engine requires a structured deployment sequence to ensure deterministic execution, accurate AST parsing, and proper rehydration hooks across agent sessions5.

| Deployment Phase | Objective | Key Actions and Deliverables | Verification Gate |
| :---- | :---- | :---- | :---- |
| **Phase 1: Environment Preparation** | Establish local extraction tooling and git diff attributes15 | Configure .gitattributes with language diff drivers (\*.py diff=python); verify Python 3.10+ runtime15 | git diff \-W displays full function headers on modified files31 |
| **Phase 2: Directory and Schema Initialization** | Instantiate living documentation storage in the project root5 | Create dev\_md\_guides/; generate baseline templates for branch.md, features.md, structure.md, memory.md, and changelog.md \[cite: 5, 8\] | All five Markdown files exist and validate against RFC 2119 schemas5 |
| **Phase 3: Automation Script Deployment** | Install deterministic extraction logic40 | Place run\_compactor.py into .claude/skills/compact-session/scripts/ and set executable permissions15 | Executing python run\_compactor.py successfully updates directory structure and branch state15 |
| **Phase 4: Agent Skill and Hook Registration** | Connect the script to the agent lifecycle16 | Author SKILL.md with explicit tool permissions; register PostToolUse compaction hooks in settings15 | Triggering /compact or "compact session" updates changelog.md and preserves continuity4 |

Once established, the deployment pipeline transforms transient conversational state into a robust, deterministic repository memory layer1. By combining AST-driven structural analysis with structured Markdown documentation, the agent maintains comprehensive architectural awareness across deep development workflows while operating under strict token constraints4.

#### **Works cited**

> 1. Memory Bank: How to Make Cline an AI Agent That Never Forgets, [https://cline.bot/blog/memory-bank-how-to-make-cline-an-ai-agent-that-never-forgets](https://cline.bot/blog/memory-bank-how-to-make-cline-an-ai-agent-that-never-forgets)  
> 2. Memory Bank \- Cline documentation, [https://docs.cline.bot/best-practices/memory-bank](https://docs.cline.bot/best-practices/memory-bank)  
> 3. Context Compaction Research: Claude Code, Codex ... \- GitHub Gist, [https://gist.github.com/badlogic/cd2ef65b0697c4dbe2d13fbecb0a0a5f](https://gist.github.com/badlogic/cd2ef65b0697c4dbe2d13fbecb0a0a5f)  
> 4. Inside Claude Code's Compaction System, [https://decodeclaude.com/compaction-deep-dive/](https://decodeclaude.com/compaction-deep-dive/)  
> 5. Living Architecture Documentation for AI Coding Agents \- CEAKSAN, [https://ceaksan.com/en/ai-agent-living-architecture-documentation](https://ceaksan.com/en/ai-agent-living-architecture-documentation)  
> 6. How to Use the /compact Command in Claude Code to Prevent, [https://www.mindstudio.ai/blog/claude-code-compact-command-context-management](https://www.mindstudio.ai/blog/claude-code-compact-command-context-management)  
> 7. Claude Code Compaction and Long-Session Operations Guide, [https://hidekazu-konishi.com/entry/claude\_code\_compaction\_and\_long\_session\_guide.html](https://hidekazu-konishi.com/entry/claude_code_compaction_and_long_session_guide.html)  
> 8. Cline Memory Bank | MCP Servers \- LobeHub, [https://lobehub.com/nl/mcp/dazeb-cline-mcp-memory-bank](https://lobehub.com/nl/mcp/dazeb-cline-mcp-memory-bank)  
> 9. What Actually Happens When You Run \`/compact\` in Claude Code, [https://dev.to/rigby\_/what-actually-happens-when-you-run-compact-in-claude-code-3kl9](https://dev.to/rigby_/what-actually-happens-when-you-run-compact-in-claude-code-3kl9)  
> 10. Memory Bank (Cline/Roo) explained: setup, pros/cons, user feedback, [https://research.meetless.ai/methods/memory-bank](https://research.meetless.ai/methods/memory-bank)  
> 11. Best Codebase Memory Tools for AI Agents (2026) \- Sentra, [https://www.sentra.app/articles/best-codebase-context-memory-tools](https://www.sentra.app/articles/best-codebase-context-memory-tools)  
> 12. Roo Code Memory Bank MCP Server, [https://mcp.so/servers/roo-code-memory-bank-mcp-server](https://mcp.so/servers/roo-code-memory-bank-mcp-server)  
> 13. GreatScottyMac/roo-code-memory-bank \- GitHub, [https://github.com/GreatScottyMac/roo-code-memory-bank](https://github.com/GreatScottyMac/roo-code-memory-bank)  
> 14. Cursor Rules Best Practices: Complete .mdc Guide (2026) \- Morph, [https://www.morphllm.com/cursor-rules-best-practices](https://www.morphllm.com/cursor-rules-best-practices)  
> 15. Specification \- Agent Skills, [https://agentskills.io/specification](https://agentskills.io/specification)  
> 16. Claude Code: Post-Compaction Hooks for Context Renewal \- Medium, [https://medium.com/@porter.nicholas/claude-code-post-compaction-hooks-for-context-renewal-7b616dcaa204](https://medium.com/@porter.nicholas/claude-code-post-compaction-hooks-for-context-renewal-7b616dcaa204)  
> 17. Cursor Rules for Non-Developers: A PM's Setup Guide, [https://www.cursorforpms.com/guides/cursor-rules-for-non-developers](https://www.cursorforpms.com/guides/cursor-rules-for-non-developers)  
> 18. \[Feature\]: Structured Memory Bank — persistent file-based context, [https://github.com/openclaw/openclaw/issues/21853](https://github.com/openclaw/openclaw/issues/21853)  
> 19. PageRank Repo Map — Automatic Codebase Context Selection via, [https://github.com/NousResearch/hermes-agent/issues/535](https://github.com/NousResearch/hermes-agent/issues/535)  
> 20. Repository Map Pattern: AST \+ PageRank for Dynamic Code Context, [https://agentpatterns.ai/context-engineering/repository-map-pattern/](https://agentpatterns.ai/context-engineering/repository-map-pattern/)  
> 21. Aider Deep Dive: The CLI Agentic Coding Tutorial 2026, [https://www.digitalapplied.com/blog/aider-deep-dive-cli-agentic-coding-tutorial-2026](https://www.digitalapplied.com/blog/aider-deep-dive-cli-agentic-coding-tutorial-2026)  
> 22. Building a better repository map with tree sitter \- Aider, [https://aider.chat/2023/10/22/repomap.html](https://aider.chat/2023/10/22/repomap.html)  
> 23. How I use LLMs | Karan Sharma, [https://mrkaran.dev/posts/using-llm/](https://mrkaran.dev/posts/using-llm/)  
> 24. Tree-sitter-based Repo Map · Issue \#3382 · aaif-goose/goose \- GitHub, [https://github.com/aaif-goose/goose/issues/3382](https://github.com/aaif-goose/goose/issues/3382)  
> 25. Repomix | Pack your codebase into AI-friendly formats, [https://repomix.com/](https://repomix.com/)  
> 26. Repoprep — Prepare Your Projects for AI, [https://www.repoprep.com/](https://www.repoprep.com/)  
> 27. Repomix Alternative: Fast Go-Based AI Context Generator \- r3d hills, [https://r3dhills.com/repomix-alternative-project2markdown/](https://r3dhills.com/repomix-alternative-project2markdown/)  
> 28. Repomix is a powerful tool that packs your entire repository ... \- GitHub, [https://github.com/yamadashy/repomix](https://github.com/yamadashy/repomix)  
> 29. Compacting Claude Code Sessions | Developing with AI Tools, [https://stevekinney.com/courses/ai-development/claude-code-compaction](https://stevekinney.com/courses/ai-development/claude-code-compaction)  
> 30. I built code health agents that run on your dependency graph, [https://dev.to/cyber\_audiomind\_3a9f839c/i-built-code-health-agents-that-run-on-your-dependency-graph-no-database-just-markdown-3a40](https://dev.to/cyber_audiomind_3a9f839c/i-built-code-health-agents-that-run-on-your-dependency-graph-no-database-just-markdown-3a40)  
> 31. git-diff Documentation \- Git, [https://git-scm.com/docs/git-diff](https://git-scm.com/docs/git-diff)  
> 32. Memory Bank \- 10X Your AI Agent Productivity\! Cline, Roo, Kilo, [https://www.youtube.com/watch?v=w6AJqZ5KpmI](https://www.youtube.com/watch?v=w6AJqZ5KpmI)  
> 33. Improving GPT-4's codebase understanding with ctags \- Aider, [https://aider.chat/docs/ctags.html](https://aider.chat/docs/ctags.html)  
> 34. Using \--function-context with Elixir and git 2.25 \- Reddit, [https://www.reddit.com/r/elixir/comments/eozrqd/using\_functioncontext\_with\_elixir\_and\_git\_225/](https://www.reddit.com/r/elixir/comments/eozrqd/using_functioncontext_with_elixir_and_git_225/)  
> 35. git-diff \- Show changes between commits, commit and working tree, etc, [https://manpages.ubuntu.com/manpages/focal/man1/git-diff.1.html](https://manpages.ubuntu.com/manpages/focal/man1/git-diff.1.html)  
> 36. Create Git diffs with proper function context \- drunken monkey, [https://drunkenmonkey.at/blog/diffs\_with\_proper\_function\_context](https://drunkenmonkey.at/blog/diffs_with_proper_function_context)  
> 37. Extracting the Module and Function Names from Python ASTs, [https://arumoy.me/blogs/python-ast-extract-module-method-names/](https://arumoy.me/blogs/python-ast-extract-module-method-names/)  
> 38. Dependency Graph Visualizer in Python \- kit, [https://kit.cased.com/tutorials/dependency\_graph\_visualizer/](https://kit.cased.com/tutorials/dependency_graph_visualizer/)  
> 39. SKILL.md Frontmatter Reference | Docs, [https://tonsofskills.com/docs/reference/skill-frontmatter/](https://tonsofskills.com/docs/reference/skill-frontmatter/)  
> 40. SKILL.md Format Specification: Complete YAML Frontmatter, [https://www.agensi.io/learn/skill-md-format-reference](https://www.agensi.io/learn/skill-md-format-reference)  
> 41. What Are Agent Skills and How To Use Them \- Strapi, [https://strapi.io/blog/what-are-agent-skills-and-how-to-use-them](https://strapi.io/blog/what-are-agent-skills-and-how-to-use-them)  
> 42. The Complete Guide to Building Skills for Claude | Anthropic, [https://resources.anthropic.com/hubfs/The-Complete-Guide-to-Building-Skill-for-Claude.pdf](https://resources.anthropic.com/hubfs/The-Complete-Guide-to-Building-Skill-for-Claude.pdf)  
> 43. Cursor Rules Best Practices: Types, Globs, and Examples \- AxonBuild, [https://axonbuild.com/blog/cursor-rules-best-practices/](https://axonbuild.com/blog/cursor-rules-best-practices/)

[image1]: <data:image/png;base64,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>

[image2]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAACkAAAAWCAYAAABdTLWOAAACpklEQVR4Xu2WS8hNURiGP6HILVESkksupRCRQv9ALomEgRgYyKU/JYSRIhlQJgYGkkuSS6akGPxiIEYGDFxySURJlAFyeZ/zrXX22vv/1zkx0Bmct57O3mt9a613r8u3jllbbbWuBosd4qQ4KCaJXqWIvNK2+8XIcnVN9DVXHBcnxHLRuxThmiyOmve1XvSPFdNFl+gQQ8VW8V3stuZGx4qHYrPoJ5aJJ2JOEkMfe8VtMU4MExfMjfRN4taIx2KGGCgOiZuxkq/7KVaGd4w+EB/F1BjUg/qIU+JqeI46LG5YMQuzxHsxvx5hNl68EkvD+xjxVGyoRxQ+ajomfotN4X2QuCO+mM9yTgz0TuyrlK8WX83NIUxjKN0GcYwz5jONubQNopwZr4kpH27FHpkmPplvAaY9p0Xil3U3ucL8oxmYLXDNupuk3y7zmWLGWM2qSXSu8l4ThwD3r833RiNFMzmTlEczOZOxHDNNTQ4Ql8zNPRdLrOfTlwoTzUxiACONTE4Mz01Nppoi3orz5uZz2mXNTY4w/+hGJieIW/aXJuOGZaBtlbpU/225OTQ7A2nOikuZ/RLzlPLD8iY55aQmUlTOJCeck04GyJqkkMpqAJUMxKmLomMSMTONRomXVo5BXAZpjuUjqjmXbPLIirbkaHI1GSMqZoZ6Ej0rhoRKjNw3T0MzkzJulm9iXijDLLfCPSvashpXxEUrEjwH441YF97RAvHBir7imAdigBXtauIqeyaOmHeE+8+hPIpZvG6eF/ck5Zij/LJ5/GlxV4xOYhBL/0JsERvNr79OK1+7s0MMV+ha8xyKp7qY2o5QudDK+zMVy7G9UkaqYqvQlt9c6mK22K/Ac08imywWq8xX+Z/EV8Ylaklxj/OHov73qRXFMlX3WlvoDxtQn1I5WhVhAAAAAElFTkSuQmCC>

[image3]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAACkAAAAWCAYAAABdTLWOAAACrElEQVR4Xu2WS8hNURiG3z8UuSUkIbmUSFFEiplEIqGIYoSSUv4QpZQMGBoYSGQgkZREwsAtiYEMGLjkkhJlaCC5vM/59jr7wt6nDPQPzltP56y1117rXZfvW1vqqqu+q0FmgzlhjpoZpqfUol7DzE7FuwfM2PLjluhrvjlmjpvlpl+pRWiaYnz6wg++WhpuLplNigFmmbumV52NTjRPzRYz0CwzL8y8Qhv62GPumElmpDmrMDKg0G6NeW5mmyHmkLmZHu4w+1Mh00zzRNFpnfqbk+Zi9j/psLmufBXmmE9mYbuFNNm8M0uz8gTz0mxst5BGmMepcMYcUXnVWFFMsqp1YqCPZm+lfrX5qjCHMI2h4jEYau6Z04pxMVd8B1HPirdEJ78U52VwVrfOXFUse50Wm5/60+QKRX8MzBGgn6pJ+r2tWClWjLGrJhEL2BLninNEx68Uppkl9U1KZupMUp/M1JlM9ZhpNImmm/eKzoGHRG2TMNHJJAYw0mRyava/0eR4xcptU0Q4jRnkgSIS67RLnU2OMa/VbHKKuaUGk0TgFZUHwvRlxUBEfp3+23YTvZxHtrsozJNGSmeiIlLKd9WbJMpJTaSoOpPsIJFOHNSapJIESjqpitxJ1CXRMdvfk5XHmbcqt0Ecmy/KJ84kimU0yjxT/u5K80ORMZJSZmgNfMPsUzlPjlbMdEFWxhw3y7dCHe25FR4qbi3EDXLBnFOe4AmMD2Z9VkaLzGeV+39kDqYGyt9rFzCAWXIbK8gsCaJknMlcU+TF3Vkdwhz15xVX4ilzX3Gui2Lr35itZrNi97arvDBzszZcoWsVOZRLpi0ue7aeh0uUJ/Wq2I5qMBXf5fdvHw6I1eK8Ql3WYFzGX6W4Kv9JzDJtUZ8UmYAPivbnU18U21Q9a12h3xCkn8jPI2OfAAAAAElFTkSuQmCC>

[image4]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAmwAAABMCAYAAADQpus6AAAFTklEQVR4Xu3dW8h1cx4H8L8cIjQzEQmN0dzMNOVMQrmQSCRMjWbu5kJNSpFDrl7JBRdyuqCUwxQRyYVDEcoFZWqGTHOl0AxFkxIaZ7+vtZdnPcve+9nvs/fzMN7Pp7697fVf+2nt9+rX739YrQEAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAsGv4WWXP8cUfkd0rv6jsNh4AAFiFfSpXVj6q/L1yU+XaysuVv1R+X3m0snf/hW10TOX5ykGTzwdWXqx8PchnlTMm47FX5cHRPVcNxhdxdlv//Xm5fPKdFJT3Vy6cfAYAWInfVP7VukLtt6OxFCAPVb5qXQG33VJIPl75w3ignNu6Yum+8cBEOl4PtO65l+nM5e9/Xjl1dD2dtGMrb1UuGFz/XeWlyuGDawAAm3Z85f3Ks62bcpwmnatxB2u7nFV5tXLweKAcV/m48khlj9FYnFT5a+uKvs3KFOcrlTcrh64f+s7dbf3/TZ4l3b0dg2sAAJuSKcbXK+9Ufj0aG0ph9FrlsPHAFksH657KbeOBiSMr71ZeqOy3fujbIu3e1k2nLuOoyodtfVGYf49ua127Wyf3Df2xdYVeCj4AgE1JMXR966YUrx6NjaVgy9Tidq9fy1q1f7b1041D6bq90bopyUNGY3+qXNeW3wCQwmv8f5ROW7pq+04+5/l+vjb8rRRwea4TRtcBABb2q8q/K/9t3Rq2edJJmjVdupVSKL49+XeadNVeaN//DUdUHmtrmxSWkcLsi8r5rSsKf1m5q3LD8KYpcu94bRsAwE45r3WdoyfaajpnmVL9W+sKrEVycfe1ubKpIFOemfqcJlOTmar8pK11stJRu7F1v29Z/fq1L1tX3Oa535t83mg9X19MbtS9BACYKYVECrZp68NSwKVDNEymH5fZabkZKdimTXcOpQOW35F747TKHW01zzptU8P+lYfbWhGZnai5NtYXbBt14gAAZuoLtmkdoFNad5THf1p3TzpYWfx/xOCe7bBIwdb/jpyDlmnb7M6ct4FiZ/Tr1/oz1iKF6+1trSuZ40ZyTt1YX7CloAQA2JRL2uyCrddPmy7SJUqnKWvGxp25WRnv6pxmkYIta8T6Z0xhld+1Cv0O1Wnnr/XyG3JsSNYDjpkSBQCWlsNdP6g83WafU5bp0hyYu9F6rciOyXMqFy2YjTY6RAqlHDkyPjJjKM+WZ8zBvymeFikEc88Bbf4O0n79WnahTjsDLrITNd22aX+n//6wOwcAsFNSZORVTVlAf9nk89CJrSvo5i3632op6lKwzSsY+3VmSQ7KXUQO4v20cvJ4YGDa+rVeitNrWnfg8Ky/kTPrUuzNe3YAgA1lYX7eH/q/1r2WKgXcn1tXpDxTOb1yS1vNLtLN6KcV501zZro006Y5U25cdM7yZOu6cvntYymwUiRmmjUZ7hBN8saHfmxedzLdwZwhN+vtCAAAOyUF2emtm6o8s3XThT8WO9r0LlcvRWc2SfSH2C4qhdml44srtKN1GyBmPTcAwE9Gdnz+o3Vr7lYp3cRZ05nLSsH7XOuOGAEA2CVcUbm5LT7luZFsYshxG7OmM5eVzQh3ttWcBQcA8H8hhU92Y144HtikHBeyVS+yT0fwqda9wgoAYJeSNWrZWPBD7VhdRN54kPPgtqoYBAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAICfsm8AlOLToS+cqigAAAAASUVORK5CYII=>

[image5]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABEAAAAZCAYAAADXPsWXAAAA7ElEQVR4Xu2SvQ4BQRSFr/hJhEQjRCeiUYqIQnRansBTKEh0otIrFURCI/EKm3gIlUKlUlIocK5Zm9m7uzKh3S/5mnvu7iRzhijEjyzcw6fmHba1nQTciJ2Bljt0SIVLGdhE4RqOYFxkDjV4hVsYExnTgCuYlIFOCZ6hBdPu6P3hAlbF3EMeHuEJFkTWg2MYEXMPfLoFL7CizYtwB3PaLBC+B76PG6zbMz55CrufJRPmpBrippgWnNGXNvwYkvpJH2ZIvY2ya8MAfmAPeCBVp2zJiM9bYfld/ARXyxVPyKDOIPgCmzAlg5CQf3kBE1AmXeAJjTAAAAAASUVORK5CYII=>

[image6]: <data:image/png;base64,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>

[image7]: <data:image/png;base64,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>

[image8]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAoAAAAaCAYAAACO5M0mAAAA5klEQVR4Xu3RMQtBURQH8CMpSpSBDBYpsSqlTCYGZovdJ6AYZZfBbvABZDEYjCYx+AAWJovNgv955z3OvVaDwb9+5d3zf8999xH9VPIwhg4UIWiOJVmYkBTm8ICu0XBTh6H7209yQ+Q9ficHW8jYAzshWMIKotbsIy24wwB81sxJDGawgB3coGQ0kCRsSI6En9IkeeOeLvFgRFL09sUvdYGpV+Kk4UzmefE/HMl6Yo1kP2W1xjefoKHWnOIVCmqNCwdIqDVKuYtV95rPkj9f+9VQqcCeZPNr6ENAF3T428YhbA/++V6edoEhw7l7aiQAAAAASUVORK5CYII=>

[image9]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAsAAAAbCAYAAACqenW9AAAA9UlEQVR4Xu3SoYsCQRTH8ScqKOqhGC+IeAjX/AMuarJpNPgPWLQYxSheunbRfigGu2C0mkwGsVmMd3B33+fOwDK7cggXDP7gAztvht03Mytyk4kgj6w74WaET/yg58yFpoEvvLgTYXnDDo9OPZAMVlgg4cwF8owj+masmy2jhqRdZNPCN6qIY4gx5hKyYdtvCQNUxFsUOJ0c1tjgXbyWNNpGFykzPsf2exLv7drCg3+BP1ct9l/GE7aYyYUjdC9jIt4edC91tE1d0ljiAzFT08U61vN9RdHUpYADOrZAmthjaup6Qefog34uagsm+sU/f9V7/j+/q+oqHbeR1QMAAAAASUVORK5CYII=>