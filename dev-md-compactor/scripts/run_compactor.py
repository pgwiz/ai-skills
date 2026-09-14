#!/usr/bin/env python3
"""
Deterministic Context Compactor & Living Documentation Engine
Part of the dev-md-compactor agent skill (https://github.com/pgwiz/ai-skills)

Extracts repository ground truth using git and AST parsers to maintain:
  dev_md_guides/
    ├── branch.md            (overwritten: current branch, HEAD, uncommitted diffs)
    ├── structure.md         (regenerated: directory topography, imports, manifests)
    ├── changelog.md         (append-only: timestamped operational & AST audit)
    ├── features.md          (seeded if missing: feature matrix & SDD progress)
    ├── memory.md            (seeded if missing: ADRs and immutable invariants)
    ├── directory.md.sample  (seeded if missing: committed sample service/path catalog)
    └── directory.md         (seeded if missing: local environment catalog, gitignored)
"""

import ast
import datetime
import os
import re
import subprocess
import sys
from pathlib import Path

# Directories ignored during structural and import scans
IGNORED_DIRS = {
    ".git",
    ".github",
    ".agent",
    ".agents",
    ".gemini",
    ".copilot",
    ".vscode",
    ".idea",
    ".venv",
    "venv",
    "env",
    "__pycache__",
    "node_modules",
    "dist",
    "build",
    "target",
    "coverage",
    ".pytest_cache",
    ".mypy_cache",
    "dev_md_guides",
}

MANIFEST_FILES = [
    "pyproject.toml",
    "setup.py",
    "requirements.txt",
    "package.json",
    "go.mod",
    "Cargo.toml",
    "Gemfile",
    "composer.json",
    "pom.xml",
    "build.gradle",
    "CMakeLists.txt",
]


def run_cmd(cmd: list[str], cwd: Path | None = None) -> str:
    """Execute a shell/git command safely and return stripped stdout."""
    try:
        res = subprocess.run(
            cmd,
            cwd=str(cwd) if cwd else None,
            capture_output=True,
            text=True,
            check=True,
            encoding="utf-8",
            errors="replace",
        )
        return res.stdout.strip()
    except Exception:
        return ""


def get_git_info(root_dir: Path) -> dict:
    """Extracts git branch, commit lineage, tracking, and uncommitted changes."""
    is_git = run_cmd(["git", "rev-parse", "--is-inside-work-tree"], cwd=root_dir)
    if is_git != "true":
        return {
            "is_git": False,
            "branch": "not-a-git-repo",
            "head_hash": "none",
            "head_msg": "none",
            "upstream": "none",
            "tracking": "no upstream",
            "uncommitted": [],
            "recent_commits": [],
        }

    branch = run_cmd(["git", "rev-parse", "--abbrev-ref", "HEAD"], cwd=root_dir) or "HEAD"
    head_hash = run_cmd(["git", "rev-parse", "--short", "HEAD"], cwd=root_dir) or "none"
    head_msg = run_cmd(["git", "log", "-1", "--pretty=%B"], cwd=root_dir) or ""
    head_first_line = head_msg.splitlines()[0] if head_msg else "No commits"

    # Upstream & Tracking
    upstream = run_cmd(["git", "rev-parse", "--abbrev-ref", "@{upstream}"], cwd=root_dir) or "none"
    tracking = "Up to date"
    if upstream != "none":
        counts = run_cmd(["git", "rev-list", "--left-right", "--count", f"HEAD...{upstream}"], cwd=root_dir)
        if counts:
            parts = counts.split()
            if len(parts) == 2:
                ahead, behind = parts[0], parts[1]
                tracking = f"Ahead {ahead} commits, behind {behind} commits relative to {upstream}"

    # Uncommitted working tree state
    status_raw = run_cmd(["git", "status", "--porcelain"], cwd=root_dir)
    uncommitted = [line.strip() for line in status_raw.splitlines() if line.strip()]

    # Recent commits (last 10)
    recent_commits = []
    log_raw = run_cmd(["git", "log", "-10", "--pretty=format:%h|%ad|%s", "--date=iso"], cwd=root_dir)
    if log_raw:
        for line in log_raw.splitlines():
            parts = line.split("|", 2)
            if len(parts) == 3:
                recent_commits.append(parts)

    return {
        "is_git": True,
        "branch": branch,
        "head_hash": head_hash,
        "head_msg": head_first_line,
        "upstream": upstream,
        "tracking": tracking,
        "uncommitted": uncommitted,
        "recent_commits": recent_commits,
    }


def extract_ast_symbols(file_path: Path) -> dict:
    """Extracts top-level functions and class method signatures using Python AST."""
    if not file_path.exists() or file_path.suffix != ".py":
        return {"functions": [], "classes": []}

    try:
        content = file_path.read_text(encoding="utf-8", errors="replace")
        tree = ast.parse(content, filename=str(file_path))
    except Exception:
        return {"functions": [], "classes": []}

    functions = []
    classes = []

    for node in tree.body:
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            args = [a.arg for a in node.args.args]
            functions.append(f"{node.name}({', '.join(args)}) [line:{node.lineno}]")
        elif isinstance(node, ast.ClassDef):
            methods = []
            for item in node.body:
                if isinstance(item, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    m_args = [a.arg for a in item.args.args if a.arg != "self"]
                    methods.append(f"{item.name}({', '.join(m_args)})")
            classes.append(f"{node.name} (methods: {', '.join(methods) if methods else 'none'}) [line:{node.lineno}]")

    return {"functions": functions, "classes": classes}


def get_modified_code_symbols(root_dir: Path) -> list[dict]:
    """Identifies modified code files and extracts AST / symbol changes."""
    diff_output = run_cmd(["git", "diff", "--name-only", "HEAD"], cwd=root_dir)
    if not diff_output:
        # Also check unstaged or untracked changes
        diff_output = run_cmd(["git", "status", "--porcelain"], cwd=root_dir)
        changed_paths = []
        for line in diff_output.splitlines():
            if len(line) > 3:
                changed_paths.append(line[3:].strip())
    else:
        changed_paths = [f.strip() for f in diff_output.splitlines() if f.strip()]

    results = []
    for rel_path in changed_paths:
        full_path = root_dir / rel_path
        if full_path.exists() and full_path.is_file():
            if full_path.suffix == ".py":
                signatures = extract_ast_symbols(full_path)
                results.append({
                    "file": rel_path,
                    "type": "python",
                    "functions": signatures["functions"],
                    "classes": signatures["classes"],
                })
            elif full_path.suffix in {".js", ".ts", ".jsx", ".tsx", ".go", ".rs", ".java"}:
                results.append({
                    "file": rel_path,
                    "type": full_path.suffix[1:],
                    "functions": [],
                    "classes": [],
                })
    return results


def build_structure_graph(root_dir: Path) -> tuple[dict, dict, list]:
    """Scans directories, maps module hierarchies, and discovers manifest files."""
    dir_summary: dict[str, list[str]] = {}
    imports_map: dict[str, set[str]] = {}
    found_manifests: list[str] = []

    # Identify manifests at root and subfolders
    for manifest in MANIFEST_FILES:
        manifest_path = root_dir / manifest
        if manifest_path.exists():
            found_manifests.append(manifest)

    for root, dirs, files in os.walk(root_dir):
        # Prune ignored directories in place
        dirs[:] = [d for d in dirs if d not in IGNORED_DIRS and not d.startswith(".")]

        rel_dir = os.path.relpath(root, root_dir)
        if rel_dir == ".":
            rel_dir_label = "root"
        else:
            rel_dir_label = rel_dir.replace("\\", "/")

        # Collect code and config files
        meaningful_files = [
            f for f in files
            if not f.startswith(".")
            and not f.endswith((".pyc", ".pyo", ".log", ".tmp"))
        ]
        if meaningful_files:
            dir_summary[rel_dir_label] = sorted(meaningful_files)

        # Parse Python imports
        for f in files:
            if f.endswith(".py"):
                file_path = Path(root) / f
                try:
                    content = file_path.read_text(encoding="utf-8", errors="replace")
                    tree = ast.parse(content, filename=str(file_path))
                    for node in ast.walk(tree):
                        if isinstance(node, ast.Import):
                            for alias in node.names:
                                top_mod = alias.name.split(".")[0]
                                imports_map.setdefault(rel_dir_label, set()).add(top_mod)
                        elif isinstance(node, ast.ImportFrom) and node.module:
                            top_mod = node.module.split(".")[0]
                            imports_map.setdefault(rel_dir_label, set()).add(top_mod)
                except Exception:
                    continue

    return dir_summary, imports_map, found_manifests


def write_branch_md(guides_dir: Path, git_info: dict) -> None:
    """Overwrites dev_md_guides/branch.md with active worktree and divergence status."""
    now_utc = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
    lines = [
        "# Branch State & Worktree Topology",
        "",
        f"- **Active Branch**: `{git_info['branch']}`",
        f"- **HEAD Commit**: `{git_info['head_hash']}` — {git_info['head_msg']}",
        f"- **Tracking Status**: {git_info['tracking']}",
        f"- **Last Updated**: {now_utc}",
        "",
        "## Divergence Analysis",
        "",
        "### Recent Commits (Local)",
    ]

    if git_info["recent_commits"]:
        for commit in git_info["recent_commits"]:
            lines.append(f"- `{commit[0]}` ({commit[1]}): {commit[2]}")
    else:
        lines.append("- *(No commit history found)*")

    lines.extend([
        "",
        "### Uncommitted Working Tree State",
    ])

    if git_info["uncommitted"]:
        for item in git_info["uncommitted"]:
            lines.append(f"- `{item}`")
    else:
        lines.append("- *Working tree clean. No uncommitted modifications.*")

    lines.extend([
        "",
        "## Integration Checklist",
        "",
        "- [ ] Working tree cleanly committed or stashed before branch switch",
        "- [ ] Rebase / sync with upstream verified",
        "- [ ] Code passes test and lint gates",
        "",
    ])

    (guides_dir / "branch.md").write_text("\n".join(lines), encoding="utf-8")


def write_structure_md(
    guides_dir: Path,
    dir_summary: dict,
    imports_map: dict,
    manifests: list[str],
    catalog: dict[str, str] | None = None,
) -> None:
    """Regenerates dev_md_guides/structure.md with directory map and dependency graph."""
    now_utc = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
    lines = [
        "# Codebase Architecture & Directory Dependency Graph",
        f"_Last regenerated: {now_utc} by dev-md-compactor_",
        "",
        "## Project Manifests & Build Tools",
    ]

    if manifests:
        for m in sorted(manifests):
            lines.append(f"- `{m}`")
    else:
        lines.append("- *(No standard build manifests detected at root)*")

    lines.extend([
        "",
        "## Module Directory Topography",
        "",
    ])

    for dir_name, files in sorted(dir_summary.items()):
        lines.append(f"### `{dir_name}/`")
        sample_files = files[:8]
        overflow = f" (+{len(files) - 8} more)" if len(files) > 8 else ""
        lines.append(f"- **Files ({len(files)})**: `{', '.join(sample_files)}`{overflow}")

        deps = sorted(imports_map.get(dir_name, set()))
        if deps:
            lines.append(f"- **Discovered Module Dependencies**: `{', '.join(deps)}`")
        lines.append("")

    lines.extend([
        "## Environment & Directory Catalog Reference",
        "- Central Catalog: `dev_md_guides/directory.md` (sample committed as `dev_md_guides/directory.md.sample`).",
        "- All workspace paths, servers, backend links, frontend links, and external endpoints are centralized in this catalog.",
        "- Invariant: Never hardcode local filesystem paths or network URLs directly across project markdown files.",
        "",
        "## Architectural Invariants & Boundary Rules",
        "- Internal modules should adhere to defined dependency boundaries without cyclic imports.",
        "- Configuration, secrets, and environment overrides must not be hardcoded in application logic.",
        "- Zero Hardcoded Endpoints: Do not hardcode machine directories, server IPs, backend links, or frontend links across markdown docs; resolve and reference them via directory.md (only directory.md.sample is committed to version control).",
        "",
    ])

    (guides_dir / "structure.md").write_text("\n".join(lines), encoding="utf-8")


def append_changelog_md(guides_dir: Path, modified_nodes: list[dict], git_info: dict) -> None:
    """Appends an operational compaction record to dev_md_guides/changelog.md."""
    log_path = guides_dir / "changelog.md"
    header = "# Session Operational Changelog\n_Append-only. Newest first. Never edit past entries._\n\n"

    now_utc = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
    entry_lines = [
        f"## [{now_utc}] — Branch `{git_info['branch']}` (HEAD: `{git_info['head_hash']}`)",
        "- **Event**: Automated Context Compaction",
        "- **Operational Scope**: Synchronized repository ground-truth into `dev_md_guides/`",
        "",
        "### AST & Code Modifications",
    ]

    if modified_nodes:
        for node in modified_nodes:
            entry_lines.append(f"- **File**: `{node['file']}` ({node['type']})")
            if node.get("functions"):
                entry_lines.append(f"  - *Functions*: {', '.join(node['functions'])}")
            if node.get("classes"):
                entry_lines.append(f"  - *Classes*: {', '.join(node['classes'])}")
    else:
        entry_lines.append("- *No AST code modifications detected in active diff.*")

    entry_lines.extend(["", "---", ""])
    new_entry = "\n".join(entry_lines)

    if log_path.exists():
        existing = log_path.read_text(encoding="utf-8")
        # Prepend new entry right after header
        if existing.startswith("# Session Operational Changelog"):
            parts = existing.split("\n\n", 1)
            updated = parts[0] + "\n\n" + new_entry + (parts[1] if len(parts) > 1 else "")
        else:
            updated = header + new_entry + existing
    else:
        updated = header + new_entry

    log_path.write_text(updated, encoding="utf-8")


def ensure_directory_gitignored(root_dir: Path, guides_dir: Path) -> None:
    """Ensures local directory.md is added to .gitignore so private paths/servers aren't committed."""
    gitignore_path = root_dir / ".gitignore"

    try:
        try:
            rel_guides = guides_dir.relative_to(root_dir).as_posix()
        except ValueError:
            rel_guides = guides_dir.name

        target_ignore = f"{rel_guides}/directory.md"
        target_allow = f"!{rel_guides}/directory.md.sample"

        content = ""
        lines = []
        if gitignore_path.exists():
            content = gitignore_path.read_text(encoding="utf-8", errors="replace")
            lines = [line.strip() for line in content.splitlines()]
        elif not (root_dir / ".git").exists() and not any(root_dir.glob(".git*")):
            # Not in a git repo and no existing .gitignore, skip creating
            return

        needs_ignore = target_ignore not in lines and "directory.md" not in lines and f"/{target_ignore}" not in lines
        needs_allow = target_allow not in lines and f"!/{target_allow[1:]}" not in lines

        additions = []
        if needs_ignore:
            additions.append(target_ignore)
        if needs_allow:
            additions.append(target_allow)

        if additions:
            block = "# dev_md_guides local environment catalog (deploy sample only)\n" + "\n".join(additions) + "\n"
            if content.strip():
                new_content = content.rstrip() + "\n\n" + block
            else:
                new_content = block
            gitignore_path.write_text(new_content, encoding="utf-8")
    except Exception:
        pass


def load_directory_catalog_grouped(guides_dir: Path) -> dict[str, dict[str, str]]:
    """
    Parses key-value mappings from directory.md (or directory.md.sample fallback)
    grouped by category header.
    """
    target = guides_dir / "directory.md"
    if not target.exists():
        target = guides_dir / "directory.md.sample"
    if not target.exists():
        return {}

    grouped: dict[str, dict[str, str]] = {}
    current_category = "General"
    in_code_block = False

    try:
        content = target.read_text(encoding="utf-8-sig", errors="replace")
        for raw_line in content.splitlines():
            line = raw_line.strip()
            if not line:
                continue

            # Code fence toggle
            if line.startswith("```"):
                in_code_block = not in_code_block
                continue
            if in_code_block:
                continue

            # Category headers: e.g. ## 1. Local Workspace & Project Directories
            header_match = re.match(r"^#{2,4}\s+(?:(?:\d+[\.\)]\s*)?)(.*)$", line)
            if header_match:
                cat_title = header_match.group(1).strip()
                current_category = cat_title
                grouped.setdefault(current_category, {})
                continue

            # Table rows: | Key | Value | Notes |
            if line.startswith("|") and line.endswith("|"):
                cells = [c.strip() for c in line.strip("|").split("|")]
                if len(cells) >= 2:
                    # Ignore separator rows like |---|---|
                    if all(set(c) <= {"-", ":", " "} for c in cells):
                        continue
                    # Ignore table header rows
                    if cells[0].lower() in ("key", "name", "service", "service name", "directory", "item", "variable", "endpoint") and \
                       cells[1].lower() in ("value", "url", "path", "endpoint", "endpoint url", "link"):
                        continue
                    key = cells[0].strip("*_`")
                    val = cells[1]
                    if val.startswith("`") and val.endswith("`") and val.count("`") == 2:
                        val = val[1:-1].strip()
                    if key:
                        grouped.setdefault(current_category, {})[key] = val
                continue

            # Bullet points: - **Key**: Value, * `Key`: Value, + Key: Value, 1. **Key**: Value
            bullet_match = re.match(r"^(?:[-*+]|\d+\.)\s+(?:\*\*|__)?`?([^`*_\r\n:]+?)`?(?:\*\*|__)?:\s*(.*)$", line)
            if bullet_match:
                key = bullet_match.group(1).strip()
                val = bullet_match.group(2).strip()
                # If entire value is enclosed in a single pair of backticks, strip them
                if val.startswith("`") and val.endswith("`") and val.count("`") == 2:
                    val = val[1:-1].strip()
                if key:
                    grouped.setdefault(current_category, {})[key] = val
    except Exception:
        pass

    return grouped


def load_directory_catalog(guides_dir: Path) -> dict[str, str]:
    """
    Parses flat key-value mappings from directory.md (or directory.md.sample fallback).
    Allows agents and scripts to resolve logical references without hardcoding.
    """
    grouped = load_directory_catalog_grouped(guides_dir)
    flat: dict[str, str] = {}
    for cat_entries in grouped.values():
        flat.update(cat_entries)
    return flat


def seed_static_templates(guides_dir: Path, templates_dir: Path | None, root_dir: Path | None = None) -> None:
    """Seeds features.md, memory.md, directory.md.sample, and directory.md from templates if they do not exist."""
    features_path = guides_dir / "features.md"
    if not features_path.exists():
        template_features = templates_dir / "features.md" if templates_dir else None
        if template_features and template_features.exists():
            features_path.write_text(template_features.read_text(encoding="utf-8"), encoding="utf-8")
        else:
            features_path.write_text(
                "# Feature Roadmap & SDD Progress Matrix\n"
                "_Last updated: " + datetime.date.today().isoformat() + "_\n\n"
                "## Done\n\n"
                "## In Progress\n\n"
                "## Planned\n\n"
                "## Removed\n",
                encoding="utf-8",
            )

    memory_path = guides_dir / "memory.md"
    if not memory_path.exists():
        template_memory = templates_dir / "memory.md" if templates_dir else None
        if template_memory and template_memory.exists():
            memory_path.write_text(template_memory.read_text(encoding="utf-8"), encoding="utf-8")
        else:
            memory_path.write_text(
                "# Project Memory Bank & Architecture Decision Records (ADR)\n"
                "_Durable knowledge — decisions, gotchas, conventions. Not a log._\n\n"
                "## Architecture decisions\n\n"
                "## Gotchas\n\n"
                "## Conventions\n\n"
                "## Dead ends\n",
                encoding="utf-8",
            )

    # Seed directory.md.sample (committed template with sanitized examples)
    sample_path = guides_dir / "directory.md.sample"
    if not sample_path.exists():
        template_sample = templates_dir / "directory.md.sample" if templates_dir else None
        if template_sample and template_sample.exists():
            sample_content = template_sample.read_text(encoding="utf-8")
        else:
            sample_content = (
                "# Environment, Service & Directory Catalog\n"
                "_Single source of truth for workspace paths, servers, backend links, frontend links, and ports._\n"
                "_All living guides in `dev_md_guides/` rely on the keys defined here rather than hardcoding paths or URLs._\n\n"
                "> [!IMPORTANT]\n"
                "> **Deployment Rule**: Only deploy `directory.md.sample` with sanitized examples to GitHub.\n"
                "> Keep `directory.md` gitignored for active machine/environment values and private endpoints.\n\n"
                "## 1. Local Workspace & Project Directories\n"
                "- **Project Root**: `.` (Repository root worktree)\n"
                "- **Living Guides Directory**: `./dev_md_guides`\n"
                "- **Agent Configuration Directory**: `~/.gemini/config/skills` (or `.agent/skills`)\n"
                "- **Distribution / Build Directory**: `./dist`\n"
                "- **Data & Artifacts Directory**: `./data`\n\n"
                "## 2. Infrastructure & Servers\n"
                "- **Development Host**: `localhost`\n"
                "- **Application Server (Local Dev)**: `127.0.0.1` (Port: `3000`)\n"
                "- **Backend API Server (Local Dev)**: `127.0.0.1` (Port: `8000`)\n"
                "- **Database Server (Local Dev)**: `127.0.0.1` (Port: `5432`)\n"
                "- **Redis / Cache Server**: `127.0.0.1` (Port: `6379`)\n"
                "- **Staging Gateway Host**: `staging.internal.example.com`\n"
                "- **Production Gateway Host**: `api.example.com`\n\n"
                "## 3. Frontend Links & Portals\n"
                "- **Web App (Local Dev)**: `http://localhost:3000`\n"
                "- **Web App (Staging)**: `https://staging-app.example.com`\n"
                "- **Web App (Production)**: `https://app.example.com`\n"
                "- **Admin Dashboard**: `http://localhost:3000/admin`\n"
                "- **Component Explorer / Storybook**: `http://localhost:6006`\n\n"
                "## 4. Backend Links & APIs\n"
                "- **API Base URL (Local Dev)**: `http://localhost:8000/api/v1`\n"
                "- **API Base URL (Staging)**: `https://staging-api.example.com/api/v1`\n"
                "- **API Base URL (Production)**: `https://api.example.com/api/v1`\n"
                "- **API Interactive Docs (Swagger / OpenAPI)**: `http://localhost:8000/docs`\n"
                "- **Health / Liveness Check**: `http://localhost:8000/healthz`\n"
                "- **GraphQL Endpoint**: `http://localhost:8000/graphql`\n\n"
                "## 5. External Services & Cloud Resources\n"
                "- **Identity / Auth Provider (SSO)**: `https://auth.example.com`\n"
                "- **Cloud Storage Bucket**: `https://storage.googleapis.com/sample-bucket`\n"
                "- **Webhook Listener**: `http://localhost:8000/webhooks/incoming`\n"
            )
        sample_path.write_text(sample_content, encoding="utf-8")

    # Seed directory.md (local active overrides, gitignored)
    directory_path = guides_dir / "directory.md"
    if not directory_path.exists():
        template_dir = templates_dir / "directory.md" if templates_dir else None
        if template_dir and template_dir.exists():
            directory_path.write_text(template_dir.read_text(encoding="utf-8"), encoding="utf-8")
        else:
            directory_path.write_text(sample_path.read_text(encoding="utf-8"), encoding="utf-8")

    if root_dir:
        ensure_directory_gitignored(root_dir, guides_dir)


def print_report(
    git_info: dict,
    modified_nodes: list[dict],
    dir_summary: dict,
    manifests: list[str],
    catalog: dict[str, str] | None = None,
    grouped_catalog: dict[str, dict[str, str]] | None = None,
) -> None:
    """Prints plain-text context report for agent consumption."""
    print("=== PROJECT GROUND TRUTH REPORT ===")
    print(f"Active Branch: {git_info['branch']}")
    print(f"HEAD Commit:   {git_info['head_hash']} ({git_info['head_msg']})")
    print(f"Tracking:      {git_info['tracking']}")
    print(f"Manifests:     {', '.join(manifests) if manifests else 'none'}")
    print(f"Directories:   {len(dir_summary)} modules scanned")
    if catalog:
        print(f"Directory Map: {len(catalog)} environment/service entries resolved")
        if grouped_catalog:
            for cat, entries in grouped_catalog.items():
                print(f"  [{cat}]")
                for k, v in entries.items():
                    print(f"    - {k}: {v}")
        else:
            for k, v in catalog.items():
                print(f"    - {k}: {v}")
    print(f"Changed Files: {len(modified_nodes)} files with code changes")
    if modified_nodes:
        for node in modified_nodes:
            print(f"  - {node['file']} ({node['type']})")
            if node.get("functions"):
                print(f"    functions: {', '.join(node['functions'])}")
            if node.get("classes"):
                print(f"    classes: {', '.join(node['classes'])}")
    print("===================================")


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Deterministic Context Compactor & Markdown Guide Generator")
    parser.add_argument("--root", type=str, default=".", help="Root directory of the project (default: .)")
    parser.add_argument("--output", type=str, default="dev_md_guides", help="Target guides directory (default: dev_md_guides)")
    parser.add_argument("--report-only", action="store_true", help="Print ground-truth context report without writing files")
    args = parser.parse_args()

    root_dir = Path(args.root).resolve()
    guides_dir = root_dir / args.output

    # Locate templates directory if packaged with skill
    skill_dir = Path(__file__).resolve().parent.parent
    templates_dir = skill_dir / "templates" if (skill_dir / "templates").exists() else None

    # Extraction pass
    git_info = get_git_info(root_dir)
    modified_nodes = get_modified_code_symbols(root_dir)
    dir_summary, imports_map, manifests = build_structure_graph(root_dir)
    catalog = load_directory_catalog(guides_dir)
    grouped_catalog = load_directory_catalog_grouped(guides_dir)

    if args.report_only:
        print_report(git_info, modified_nodes, dir_summary, manifests, catalog, grouped_catalog)
        return

    # Write guides
    guides_dir.mkdir(parents=True, exist_ok=True)
    seed_static_templates(guides_dir, templates_dir, root_dir)
    write_branch_md(guides_dir, git_info)
    write_structure_md(guides_dir, dir_summary, imports_map, manifests, catalog=catalog)
    append_changelog_md(guides_dir, modified_nodes, git_info)

    print(f"[COMPACTOR] Successfully synchronized {guides_dir.name}/ (branch.md, structure.md, changelog.md, features.md, memory.md, directory.md.sample)")


if __name__ == "__main__":
    main()
