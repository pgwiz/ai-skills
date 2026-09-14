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
            self.assertIn("dev_md_guides/credentials.md", content)
            self.assertIn("!dev_md_guides/credentials.md.sample", content)

            # Case B: .gitignore exists with directory.md but missing whitelist
            gitignore.write_text("dev_md_guides/directory.md\n", encoding="utf-8")
            run_compactor.ensure_directory_gitignored(root_dir, guides_dir)
            content_updated = gitignore.read_text(encoding="utf-8")
            self.assertIn("!dev_md_guides/directory.md.sample", content_updated)
            self.assertIn("dev_md_guides/credentials.md", content_updated)
            self.assertIn("!dev_md_guides/credentials.md.sample", content_updated)

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
            cred_sample_file = guides_dir / "credentials.md.sample"
            cred_local_file = guides_dir / "credentials.md"

            self.assertTrue(sample_file.exists())
            self.assertTrue(local_file.exists())
            self.assertTrue(cred_sample_file.exists())
            self.assertTrue(cred_local_file.exists())

            self.assertIn("Environment, Service & Directory Catalog", sample_file.read_text(encoding="utf-8"))
            self.assertIn("Environment, Service & Directory Catalog", local_file.read_text(encoding="utf-8"))
            self.assertIn("Project Credentials & Secrets Reference", cred_sample_file.read_text(encoding="utf-8"))
            self.assertIn("CRITICAL SECURITY RULE", cred_sample_file.read_text(encoding="utf-8"))
            self.assertIn("Project Credentials & Secrets Reference", cred_local_file.read_text(encoding="utf-8"))

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

    def test_credentials_catalog_parsing(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            guides_dir = Path(tmpdir)
            cred_file = guides_dir / "credentials.md"
            cred_file.write_text("""# Project Credentials & Secrets Reference
## 1. Application Secrets
- **Database Password**: `ENC[MY_DB_PASS]`
- **Encryption Key**: `ENC[AES256_KEY_BASE64]`

## 2. API Keys
- **Anthropic API Key**: `sk-ant-api03-SAMPLE_PLACEHOLDER_KEY`
- **OpenAI API Key**: `sk-proj-SAMPLE_PLACEHOLDER_KEY`

## 3. Tabular Secrets
| Service | Key Name | Value |
|---|---|---|
| Stripe | Webhook Secret | `whsec_mock_sample` |
| GitHub | App Private Key | `-----BEGIN PRIVATE KEY-----\\n[MOCK]\\n-----END PRIVATE KEY-----` |
""", encoding="utf-8")

            catalog = run_compactor.load_credentials_catalog(guides_dir)
            grouped = run_compactor.load_credentials_catalog_grouped(guides_dir)

            self.assertEqual(catalog.get("Database Password"), "ENC[MY_DB_PASS]")
            self.assertEqual(catalog.get("Encryption Key"), "ENC[AES256_KEY_BASE64]")
            self.assertEqual(catalog.get("Anthropic API Key"), "sk-ant-api03-SAMPLE_PLACEHOLDER_KEY")
            self.assertEqual(catalog.get("Webhook Secret"), "whsec_mock_sample")

            self.assertIn("Application Secrets", grouped)
            self.assertIn("Database Password", grouped["Application Secrets"])
            self.assertIn("Tabular Secrets", grouped)
            self.assertIn("Webhook Secret", grouped["Tabular Secrets"])

            # Fallback when credentials.md is missing but credentials.md.sample exists
            cred_file.unlink()
            sample_file = guides_dir / "credentials.md.sample"
            sample_file.write_text("""# Project Credentials Sample
## 1. Secrets
- **Sample API Token**: `sample_token_xyz`
""", encoding="utf-8")

            fallback_catalog = run_compactor.load_credentials_catalog(guides_dir)
            self.assertEqual(fallback_catalog.get("Sample API Token"), "sample_token_xyz")

    def test_secret_scanner_detection_and_placeholders(self):
        # 1. Real secrets should be detected (dynamically constructed to prevent push protection false positives)
        real_secrets = [
            ("s" + "k-1234567890abcdef1234567890abcdef", "OpenAI / Anthropic API Key"),
            ("g" + "hp_1234567890abcdefghijklmnopqrstuvwxyz", "GitHub Personal Access"),
            ("A" + "KIA1234567890ABCDEF", "AWS Access Key ID"),
            ("s" + "k_live_1234567890abcdef12345678", "Stripe Live Secret Key"),
            ("A" + "IzaSyDa9_abcdefghijklmnopqrstuvwxyz12", "Google API Key"),
            ("postgre" + "sql://appuser:supersecretpass123@db.prod.internal:5432/myapp", "Database connection URI"),
            ("api_key = 'abcdef1234567890abcdef'", "unredacted credential"),
        ]

        for secret_str, label in real_secrets:
            findings = run_compactor.scan_text_for_secrets(secret_str)
            self.assertGreater(
                len(findings), 0,
                f"Expected scanner to detect real secret: '{secret_str}' ({label})"
            )

        # 2. Mock and sanitized placeholders should NOT be detected (false-positive resistance)
        sanitized_placeholders = [
            "sk-proj-SAMPLE_PLACEHOLDER_KEY",
            "sk-ant-api03-SAMPLE_PLACEHOLDER_KEY",
            "AIzaSy_SAMPLE_PLACEHOLDER_KEY",
            "ENC[YOUR_DB_PASSWORD_HERE]",
            "postgresql://postgres:REDACTED@localhost:5432/app_db",
            "-----BEGIN PRIVATE KEY-----\n[MOCK_PKCS8_KEY_CONTENT]\n-----END PRIVATE KEY-----",
            "whsec_SAMPLE_WEBHOOK_SECRET",
            "- **Database Password**: `ENC[YOUR_DB_PASSWORD_HERE]`",
            "api_key: 'YOUR_API_KEY_PLACEHOLDER'",
            "password = 'CHANGE_ME'",
        ]

        for placeholder_str in sanitized_placeholders:
            findings = run_compactor.scan_text_for_secrets(placeholder_str)
            self.assertEqual(
                len(findings), 0,
                f"Sanitized placeholder was falsely flagged: '{placeholder_str}' -> {findings}"
            )

    def test_scan_guides_for_secrets_skips_gitignored(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            guides_dir = Path(tmpdir)
            # Local credentials.md contains live secret (allowed locally in gitignored file)
            (guides_dir / "credentials.md").write_text(
                "API_KEY=" + "s" + "k-1234567890abcdef1234567890abcdef", encoding="utf-8"
            )
            # Clean tracked guide
            (guides_dir / "branch.md").write_text(
                "# Branch State\nActive branch is feat/dev-md-compactor\n", encoding="utf-8"
            )

            # Scanner by default should skip credentials.md and directory.md
            leaks = run_compactor.scan_guides_for_secrets(guides_dir, include_gitignored=False)
            self.assertEqual(len(leaks), 0, "Scanner should not flag local gitignored credentials.md")

            # But if a leak is in a tracked file like branch.md
            (guides_dir / "branch.md").write_text(
                "Leaked token: " + "g" + "hp_1234567890abcdefghijklmnopqrstuvwxyz", encoding="utf-8"
            )
            leaks_found = run_compactor.scan_guides_for_secrets(guides_dir, include_gitignored=False)
            self.assertIn("branch.md", leaks_found)
            self.assertEqual(leaks_found["branch.md"][0]["type"], "GitHub Personal Access / OAuth Token")

    def test_credential_commit_warning_generation(self):
        warning = run_compactor.generate_credential_commit_warning("dev_md_guides/credentials.md")
        self.assertIn("CRITICAL SECURITY WARNING", warning)
        self.assertIn("Target: 'dev_md_guides/credentials.md'", warning)
        self.assertIn("DANGER & SECURITY RISKS", warning)
        self.assertIn("REQUIRED AGENT PROTOCOL", warning)
        self.assertIn("Git history is permanent", warning)
        self.assertIn("user confirmation", warning.lower())

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

            # Validate generated files (all 8 living guide files)
            self.assertTrue((guides_dir / "branch.md").exists())
            self.assertTrue((guides_dir / "structure.md").exists())
            self.assertTrue((guides_dir / "changelog.md").exists())
            self.assertTrue((guides_dir / "features.md").exists())
            self.assertTrue((guides_dir / "memory.md").exists())
            self.assertTrue((guides_dir / "directory.md.sample").exists())
            self.assertTrue((guides_dir / "directory.md").exists())
            self.assertTrue((guides_dir / "credentials.md.sample").exists())
            self.assertTrue((guides_dir / "credentials.md").exists())

            # Validate .gitignore entries
            gitignore = root_dir / ".gitignore"
            self.assertTrue(gitignore.exists())
            git_lines = gitignore.read_text(encoding="utf-8")
            self.assertIn("dev_md_guides/directory.md", git_lines)
            self.assertIn("!dev_md_guides/directory.md.sample", git_lines)
            self.assertIn("dev_md_guides/credentials.md", git_lines)
            self.assertIn("!dev_md_guides/credentials.md.sample", git_lines)

            # Validate structure.md content mentions credentials and zero exposure rule
            structure_content = (guides_dir / "structure.md").read_text(encoding="utf-8")
            self.assertIn("Credentials & Secrets Reference", structure_content)
            self.assertIn("dev_md_guides/credentials.md", structure_content)
            self.assertIn("Zero Credential Exposure", structure_content)

            # Validate secret scan on generated directory
            leaks = run_compactor.scan_guides_for_secrets(guides_dir)
            self.assertEqual(len(leaks), 0, f"Generated sample files should not leak secrets: {leaks}")

    def test_edge_cases_scanner_and_catalogs(self):
        # 1. Empty and whitespace input to scanner
        self.assertEqual(run_compactor.scan_text_for_secrets(""), [])
        self.assertEqual(run_compactor.scan_text_for_secrets("   \n\n\t  "), [])

        # 2. Non-existent file / non-file path
        self.assertEqual(run_compactor.scan_file_for_secrets(Path("non_existent_random_file.md")), [])

        # 3. Non-existent directory for scanner and catalogs
        fake_dir = Path("non_existent_guides_dir")
        self.assertEqual(run_compactor.scan_guides_for_secrets(fake_dir), {})
        self.assertEqual(run_compactor.load_credentials_catalog(fake_dir), {})
        self.assertEqual(run_compactor.load_credentials_catalog_grouped(fake_dir), {})

        # 4. UTF-8 BOM in credentials.md
        with tempfile.TemporaryDirectory() as tmpdir:
            guides_dir = Path(tmpdir)
            cred_file = guides_dir / "credentials.md"
            content = "\ufeff# Credentials\n## 1. Secrets\n- **API Key**: `my-secret-value`\n"
            cred_file.write_bytes(content.encode("utf-8-sig"))
            parsed = run_compactor.load_credentials_catalog(guides_dir)
            self.assertEqual(parsed.get("API Key"), "my-secret-value")


if __name__ == "__main__":
    unittest.main()
