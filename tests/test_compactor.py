import unittest
import tempfile
from pathlib import Path
import sys
import shutil

# Add scripts directory to path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "dev-md-compactor" / "scripts"))
import run_compactor

class TestCompactorEngine(unittest.TestCase):
    def test_catalog_parsing_formats(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            guides_dir = Path(tmpdir)
            dir_md = guides_dir / "directory.md"
            dir_md.write_text("""# Environment, Service & Directory Catalog
## 1. Local Workspace & Project Directories
- **Project Root**: `.` (Repository root worktree)
- **Living Guides Directory**: `./dev_md_guides`
- **Agent Configuration Directory**: `~/.gemini/config/skills` (or `.agent/skills`)
- **Distribution / Build Directory**: `./dist`
- **Data & Artifacts Directory**: `./data`

## 2. Infrastructure & Servers
- **Development Host**: `localhost`
- **Application Server (Local Dev)**: `127.0.0.1` (Port: `3000`)
- **Backend API Server (Local Dev)**: `127.0.0.1` (Port: `8000`)
- **Database Server (Local Dev)**: `127.0.0.1` (Port: `5432`)
- **Cluster Node**: host=`node1.internal` port=`9000` status=`active`
* **Star Bullet Server**: `10.0.0.5`
+ **Plus Bullet Server**: `10.0.0.6`
  - **Indented Server**: `10.0.0.7`
1. **Numbered Server**: `10.0.0.8`

## 3. Frontend Links & Portals
- **Web App (Local Dev)**: `http://localhost:3000`
- **Admin Dashboard**: http://localhost:3000/admin

## 4. Backend Links & APIs
- **Webhook Listener**: `http://localhost:8000/webhook?token=xyz&debug=1`

## 5. Tabular Catalog
| Service Name | Endpoint URL | Description |
|---|---|---|
| Metrics Collector | http://metrics.internal:9090 | Prometheus scrape target |
| Trace Collector | `http://tempo.internal:3200` | OpenTelemetry traces |
""", encoding="utf-8")

            catalog = run_compactor.load_directory_catalog(guides_dir)
            grouped = run_compactor.load_directory_catalog_grouped(guides_dir)

            # 1. Standard keys preserved
            self.assertEqual(catalog.get("Development Host"), "localhost")
            self.assertEqual(catalog.get("Web App (Local Dev)"), "http://localhost:3000")

            # 2. Ports and comments are NOT truncated
            self.assertIn("Port: `3000`", catalog.get("Application Server (Local Dev)", ""))
            self.assertIn("Repository root worktree", catalog.get("Project Root", ""))

            # 3. Multiple inline backticks are NOT truncated
            self.assertEqual(
                catalog.get("Cluster Node"),
                "host=`node1.internal` port=`9000` status=`active`"
            )

            # 4. Star, plus, numbered, and indented bullets are parsed
            self.assertEqual(catalog.get("Star Bullet Server"), "10.0.0.5")
            self.assertEqual(catalog.get("Plus Bullet Server"), "10.0.0.6")
            self.assertEqual(catalog.get("Indented Server"), "10.0.0.7")
            self.assertEqual(catalog.get("Numbered Server"), "10.0.0.8")

            # 5. Tabular entries parsed
            self.assertEqual(catalog.get("Metrics Collector"), "http://metrics.internal:9090")
            self.assertEqual(catalog.get("Trace Collector"), "http://tempo.internal:3200")

            # 6. Grouped catalog structure
            self.assertIn("Infrastructure & Servers", grouped)
            self.assertIn("Application Server (Local Dev)", grouped["Infrastructure & Servers"])
            self.assertIn("Tabular Catalog", grouped)
            self.assertIn("Metrics Collector", grouped["Tabular Catalog"])

    def test_gitignore_creation_and_preservation(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            root_dir = Path(tmpdir)
            guides_dir = root_dir / "dev_md_guides"
            guides_dir.mkdir()

            # Case A: .gitignore doesn't exist yet in a git repo
            (root_dir / ".git").mkdir()
            run_compactor.ensure_directory_gitignored(root_dir, guides_dir)

            gitignore = root_dir / ".gitignore"
            self.assertTrue(gitignore.exists())
            content = gitignore.read_text(encoding="utf-8")
            self.assertIn("dev_md_guides/directory.md", content)
            self.assertIn("!dev_md_guides/directory.md.sample", content)

            # Case B: .gitignore exists with directory.md but missing whitelist
            gitignore.write_text("dev_md_guides/directory.md\n", encoding="utf-8")
            run_compactor.ensure_directory_gitignored(root_dir, guides_dir)
            content_updated = gitignore.read_text(encoding="utf-8")
            self.assertIn("!dev_md_guides/directory.md.sample", content_updated)

            # Case C: Idempotent - running again does not duplicate entries
            run_compactor.ensure_directory_gitignored(root_dir, guides_dir)
            content_third = gitignore.read_text(encoding="utf-8")
            self.assertEqual(content_updated.strip(), content_third.strip())

    def test_fallback_sample_content(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            root_dir = Path(tmpdir)
            guides_dir = root_dir / "dev_md_guides"
            guides_dir.mkdir()

            # Pass templates_dir as None to force fallback generator
            run_compactor.seed_static_templates(guides_dir, templates_dir=None, root_dir=root_dir)

            sample_file = guides_dir / "directory.md.sample"
            local_file = guides_dir / "directory.md"

            self.assertTrue(sample_file.exists())
            self.assertTrue(local_file.exists())
            self.assertIn("Environment, Service & Directory Catalog", sample_file.read_text(encoding="utf-8"))
            self.assertIn("Environment, Service & Directory Catalog", local_file.read_text(encoding="utf-8"))

    def test_utf8_bom_and_complex_urls(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            guides_dir = Path(tmpdir)
            dir_md = guides_dir / "directory.md"
            # Write with UTF-8 BOM
            content = (
                "\ufeff# Environment, Service & Directory Catalog\n"
                "> [!IMPORTANT]\n"
                "> Deployment rule blockquote\n\n"
                "## 1. Local Workspace\n"
                "- **Root Path**: `/var/www/app`\n"
                "- **Complex URL**: `https://api.example.com/v2/items?filter=active&sort=desc#main`\n"
                "---\n"
                "## 2. Servers\n"
                "- **API Host**: `api.internal.local` (Port: `8443`, Protocol: `https`)\n"
            )
            dir_md.write_bytes(content.encode("utf-8-sig"))

            catalog = run_compactor.load_directory_catalog(guides_dir)
            self.assertEqual(catalog.get("Root Path"), "/var/www/app")
            self.assertEqual(
                catalog.get("Complex URL"),
                "https://api.example.com/v2/items?filter=active&sort=desc#main"
            )
            self.assertIn("Port: `8443`", catalog.get("API Host", ""))

    def test_end_to_end_compaction_flow(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            root_dir = Path(tmpdir)
            guides_dir = root_dir / "dev_md_guides"

            # Create dummy repo structure
            (root_dir / ".git").mkdir()
            (root_dir / "src").mkdir()
            (root_dir / "src" / "app.py").write_text("def hello():\n    return 'world'\n", encoding="utf-8")

            # Run compactor logic
            dir_summary, imports_map, manifests = run_compactor.build_structure_graph(root_dir)
            git_info = run_compactor.get_git_info(root_dir)
            modified_nodes = run_compactor.get_modified_code_symbols(root_dir)

            guides_dir.mkdir(parents=True, exist_ok=True)
            run_compactor.seed_static_templates(guides_dir, templates_dir=None, root_dir=root_dir)
            run_compactor.write_branch_md(guides_dir, git_info)
            run_compactor.write_structure_md(guides_dir, dir_summary, imports_map, manifests)
            run_compactor.append_changelog_md(guides_dir, modified_nodes, git_info)

            # Validate generated files
            self.assertTrue((guides_dir / "branch.md").exists())
            self.assertTrue((guides_dir / "structure.md").exists())
            self.assertTrue((guides_dir / "changelog.md").exists())
            self.assertTrue((guides_dir / "features.md").exists())
            self.assertTrue((guides_dir / "memory.md").exists())
            self.assertTrue((guides_dir / "directory.md.sample").exists())
            self.assertTrue((guides_dir / "directory.md").exists())

            # Validate .gitignore
            gitignore = root_dir / ".gitignore"
            self.assertTrue(gitignore.exists())
            git_lines = gitignore.read_text(encoding="utf-8")
            self.assertIn("dev_md_guides/directory.md", git_lines)
            self.assertIn("!dev_md_guides/directory.md.sample", git_lines)


if __name__ == "__main__":
    unittest.main()
