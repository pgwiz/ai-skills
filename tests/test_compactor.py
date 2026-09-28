import unittest
import tempfile
from pathlib import Path
import sys
import shutil
import subprocess

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
            run_compactor.update_agent_inventory(guides_dir)

            # Validate generated files (all living guide files and root router)
            self.assertTrue((root_dir / "dev_com_agent.md").exists())
            self.assertTrue((guides_dir / "agent.md").exists())
            self.assertTrue((guides_dir / "gotchas.md").exists())
            self.assertTrue((guides_dir / "flow.md").exists())
            self.assertTrue((guides_dir / "branch.md").exists())
            self.assertTrue((guides_dir / "structure.md").exists())
            self.assertTrue((guides_dir / "changelog.md").exists())
            self.assertTrue((guides_dir / "features.md").exists())
            self.assertTrue((guides_dir / "memory.md").exists())
            self.assertTrue((guides_dir / "directory.md.sample").exists())
            self.assertTrue((guides_dir / "directory.md").exists())
            self.assertTrue((guides_dir / "credentials.md.sample").exists())
            self.assertTrue((guides_dir / "credentials.md").exists())

            # Validate agent.md inventory table populated
            agent_content = (guides_dir / "agent.md").read_text(encoding="utf-8")
            self.assertIn("branch.md", agent_content)
            self.assertIn("gotchas.md", agent_content)
            self.assertIn("flow.md", agent_content)

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

    def test_secret_scanner_false_negative_resistance_near_example_words(self):
        """
        Ensures that real live secrets are NEVER ignored merely because words like
        'example', 'sample', or 'redacted' appear in surrounding headers or sentences.
        """
        cases = [
            (
                "## Example Configuration\nAWS Key: " + "A" + "KIA1234567890ABCDEF\n",
                "AWS Access Key ID",
            ),
            (
                "Sample request token: " + "g" + "hp_1234567890abcdefghijklmnopqrstuvwxyz",
                "GitHub Personal Access / OAuth Token",
            ),
            (
                "# Sample Architecture\nProduction OpenAI: " + "s" + "k-1234567890abcdef1234567890abcdef",
                "OpenAI / Anthropic API Key (sk-...)",
            ),
            (
                "Example database connection:\n" + "postgre" + "sql://appuser:supersecretpass123@db.prod.internal:5432/myapp",
                "Database connection URI with embedded credentials",
            ),
            (
                "## Examples\napi_key = 'abcdef1234567890abcdef'",
                "Potential unredacted credential / secret assignment",
            ),
        ]

        for text, expected_type in cases:
            findings = run_compactor.scan_text_for_secrets(text)
            self.assertGreater(
                len(findings), 0,
                f"Expected scanner to catch secret near example/sample words: '{text}'"
            )
            self.assertTrue(
                any(f["type"] == expected_type for f in findings),
                f"Expected finding type '{expected_type}' in {findings}"
            )

    def test_extended_database_uris_and_private_keys(self):
        """Tests that modern sub-protocol database connection URIs and PGP private keys are caught."""
        extended_secrets = [
            ("mongo" + "db+srv://admin:pass123456@cluster0.mongodb.net/prod", "Database connection URI"),
            ("postgre" + "sql+psycopg2://scott:tiger12345@localhost/mydatabase", "Database connection URI"),
            ("my" + "sql+pymysql://root:mysecretpass@127.0.0.1:3306/db", "Database connection URI"),
            ("redis" + "s://default:supersecretkey@myredis.cache.amazonaws.com:6380", "Database connection URI"),
            ("am" + "qp://guest:secretbrokerpass@localhost:5672//", "Database connection URI"),
            ("-----BEGIN PGP PRIVATE KEY BLOCK-----\n[KEY_DATA]\n-----END PGP PRIVATE KEY BLOCK-----", "Private Key block"),
        ]

        for secret_str, expected_substr in extended_secrets:
            findings = run_compactor.scan_text_for_secrets(secret_str)
            self.assertGreater(
                len(findings), 0,
                f"Expected scanner to catch extended secret pattern: '{secret_str}'"
            )
            self.assertTrue(
                any(expected_substr in f["type"] for f in findings),
                f"Expected '{expected_substr}' in findings for '{secret_str}': {findings}"
            )

    def test_git_tracked_credentials_detection_and_security_check(self):
        """Tests is_credentials_file_tracked and check_credentials_security in a live Git repository."""
        with tempfile.TemporaryDirectory() as tmpdir:
            root_dir = Path(tmpdir)
            guides_dir = root_dir / "dev_md_guides"
            guides_dir.mkdir()

            # Initialize real git repo
            subprocess.run(["git", "init"], cwd=str(root_dir), check=True, capture_output=True)
            subprocess.run(["git", "config", "user.name", "Test Agent"], cwd=str(root_dir), check=True)
            subprocess.run(["git", "config", "user.email", "test@example.com"], cwd=str(root_dir), check=True)

            # Initially credentials.md does not exist
            self.assertFalse(run_compactor.is_credentials_file_tracked(root_dir, guides_dir))

            # Create credentials.md and gitignore
            cred_file = guides_dir / "credentials.md"
            cred_file.write_text("API_KEY=" + "s" + "k-1234567890abcdef1234567890abcdef\n", encoding="utf-8")
            run_compactor.ensure_credentials_gitignored(root_dir, guides_dir)

            # Properly ignored -> not tracked, not staged
            sec_clean = run_compactor.check_credentials_security(root_dir, guides_dir)
            self.assertFalse(sec_clean["is_tracked"])
            self.assertFalse(sec_clean["is_staged"])
            self.assertEqual(len(sec_clean["issues"]), 0)

            # Scanner skips it when safely gitignored
            leaks_clean = run_compactor.scan_guides_for_secrets(guides_dir, root_dir=root_dir)
            self.assertNotIn("credentials.md", leaks_clean)

            # Now simulate accidental force-staging of credentials.md: git add -f
            subprocess.run(["git", "add", "-f", str(cred_file)], cwd=str(root_dir), check=True, capture_output=True)

            # Now it IS tracked in git index!
            self.assertTrue(run_compactor.is_credentials_file_tracked(root_dir, guides_dir))
            sec_staged = run_compactor.check_credentials_security(root_dir, guides_dir)
            self.assertTrue(sec_staged["is_tracked"])
            self.assertTrue(sec_staged["is_staged"])
            self.assertIn("CRITICAL", sec_staged["warning"])
            self.assertGreater(len(sec_staged["issues"]), 0)

            # And scanner now DOES NOT skip it because it is tracked in Git!
            leaks_flagged = run_compactor.scan_guides_for_secrets(guides_dir, root_dir=root_dir)
            self.assertIn("credentials.md", leaks_flagged)

    def test_gitignore_root_and_nested_output_formatting(self):
        """Tests that rel_guides == '.' and nested paths do not produce invalid './' gitignore patterns."""
        with tempfile.TemporaryDirectory() as tmpdir:
            root_dir = Path(tmpdir)
            (root_dir / ".git").mkdir()

            # Case 1: guides_dir is root itself (--output .)
            run_compactor.ensure_credentials_gitignored(root_dir, root_dir)
            content = (root_dir / ".gitignore").read_text(encoding="utf-8")
            self.assertIn("\ncredentials.md\n", "\n" + content)
            self.assertIn("\n!credentials.md.sample\n", "\n" + content)
            self.assertNotIn("./credentials.md", content)

            # Case 2: nested guides_dir
            nested_guides = root_dir / "docs" / "dev_md_guides"
            nested_guides.mkdir(parents=True)
            run_compactor.ensure_credentials_gitignored(root_dir, nested_guides)
            content_nested = (root_dir / ".gitignore").read_text(encoding="utf-8")
            self.assertIn("docs/dev_md_guides/credentials.md", content_nested)
            self.assertIn("!docs/dev_md_guides/credentials.md.sample", content_nested)

    def test_new_architecture_templates_and_fallbacks(self):
        """Tests that dev_com_agent.md, agent.md, gotchas.md, and flow.md seed properly from templates and fallback."""
        templates_dir = Path(__file__).resolve().parent.parent / "dev-md-compactor" / "templates"

        # Case A: Seed with real templates
        with tempfile.TemporaryDirectory() as tmpdir:
            root_dir = Path(tmpdir)
            guides_dir = root_dir / "dev_md_guides"
            guides_dir.mkdir()

            run_compactor.seed_static_templates(guides_dir, templates_dir=templates_dir, root_dir=root_dir)

            self.assertTrue((root_dir / "dev_com_agent.md").exists())
            self.assertTrue((guides_dir / "agent.md").exists())
            self.assertTrue((guides_dir / "gotchas.md").exists())
            self.assertTrue((guides_dir / "flow.md").exists())

            root_agent_text = (root_dir / "dev_com_agent.md").read_text(encoding="utf-8")
            self.assertIn("Universal Agent Entry Point", root_agent_text)
            self.assertIn("dev_md_guides/agent.md", root_agent_text)

            agent_text = (guides_dir / "agent.md").read_text(encoding="utf-8")
            self.assertIn("Executive Summary Table", agent_text)
            self.assertIn("Dynamic Topic Guides", agent_text)

            gotchas_text = (guides_dir / "gotchas.md").read_text(encoding="utf-8")
            self.assertIn("Major Blockers", gotchas_text)
            self.assertIn("Minor Quirks", gotchas_text)

            flow_text = (guides_dir / "flow.md").read_text(encoding="utf-8")
            self.assertIn("Test & Quality Gate Execution Flow", flow_text)

        # Case B: Fallback generator (templates_dir=None)
        with tempfile.TemporaryDirectory() as tmpdir:
            root_dir = Path(tmpdir)
            guides_dir = root_dir / "dev_md_guides"
            guides_dir.mkdir()

            run_compactor.seed_static_templates(guides_dir, templates_dir=None, root_dir=root_dir)

            self.assertTrue((root_dir / "dev_com_agent.md").exists())
            self.assertTrue((guides_dir / "agent.md").exists())
            self.assertTrue((guides_dir / "gotchas.md").exists())
            self.assertTrue((guides_dir / "flow.md").exists())

            self.assertIn("Universal Agent Entry Point", (root_dir / "dev_com_agent.md").read_text(encoding="utf-8"))
            self.assertIn("Executive Summary Table", (guides_dir / "agent.md").read_text(encoding="utf-8"))
            self.assertIn("Major Blockers", (guides_dir / "gotchas.md").read_text(encoding="utf-8"))
            self.assertIn("Procedural Execution Flows", (guides_dir / "flow.md").read_text(encoding="utf-8"))

    def test_dynamic_discovery_and_inventory_generation(self):
        """Tests that discover_guide_files accurately categorizes core and dynamic files, and update_agent_inventory writes the table."""
        with tempfile.TemporaryDirectory() as tmpdir:
            guides_dir = Path(tmpdir)
            # Create core guides
            (guides_dir / "agent.md").write_text("# Master Index\n<!-- AUTO-GENERATED BY COMPACTOR: DO NOT EDIT DIRECTLY -->\n| old |\n<!-- END AUTO-GENERATED INVENTORY -->\n", encoding="utf-8")
            (guides_dir / "branch.md").write_text("# Branch\nline2\n", encoding="utf-8")
            (guides_dir / "gotchas.md").write_text("# Gotchas\nline2\nline3\n", encoding="utf-8")
            (guides_dir / "flow.md").write_text("# Flow\nline2\n", encoding="utf-8")
            (guides_dir / "credentials.md").write_text("API_KEY=mock\n", encoding="utf-8")
            (guides_dir / "credentials.md.sample").write_text("API_KEY=sample\n", encoding="utf-8")
            (guides_dir / "directory.md").write_text("HOST=localhost\n", encoding="utf-8")
            (guides_dir / "directory.md.sample").write_text("HOST=sample\n", encoding="utf-8")

            # Create dynamic topic guides
            (guides_dir / "commands.md").write_text("# Commands\n```bash\ngit status\n```\n", encoding="utf-8")
            (guides_dir / "mcp.md").write_text("# MCP\n- tool: test\n", encoding="utf-8")
            (guides_dir / "database.md").write_text("# Database\nmigrations\n", encoding="utf-8")

            discovered = run_compactor.discover_guide_files(guides_dir)
            disc_map = {d["filename"]: d for d in discovered}

            self.assertIn("agent.md", disc_map)
            self.assertEqual(disc_map["agent.md"]["category"], "Master Index")
            self.assertEqual(disc_map["branch.md"]["category"], "Worktree State")
            self.assertEqual(disc_map["gotchas.md"]["category"], "Failure Modes")
            self.assertEqual(disc_map["flow.md"]["category"], "Execution Flows")
            self.assertEqual(disc_map["commands.md"]["category"], "Dynamic Topic")
            self.assertEqual(disc_map["mcp.md"]["category"], "Dynamic Topic")
            self.assertEqual(disc_map["database.md"]["category"], "Dynamic Topic")

            self.assertEqual(disc_map["credentials.md"]["status"], "Gitignored")
            self.assertEqual(disc_map["credentials.md.sample"]["status"], "Committed")
            self.assertEqual(disc_map["directory.md"]["status"], "Gitignored")
            self.assertEqual(disc_map["directory.md.sample"]["status"], "Committed")
            self.assertEqual(disc_map["branch.md"]["status"], "Active")

            # Test updating inventory in agent.md
            run_compactor.update_agent_inventory(guides_dir)
            agent_content = (guides_dir / "agent.md").read_text(encoding="utf-8")

            self.assertIn("`database.md`", agent_content)
            self.assertIn("`commands.md`", agent_content)
            self.assertIn("`mcp.md`", agent_content)
            self.assertIn("`gotchas.md`", agent_content)
            self.assertIn("`flow.md`", agent_content)
            self.assertIn("Dynamic Topic", agent_content)
            self.assertIn("Gitignored", agent_content)

    def test_gotchas_and_workflows_counting(self):
        """Tests count_gotchas and count_workflows parsers."""
        with tempfile.TemporaryDirectory() as tmpdir:
            guides_dir = Path(tmpdir)

            # Non-existent files return zero gracefully
            self.assertEqual(run_compactor.count_gotchas(guides_dir), {"total": 0, "major": 0, "minor": 0})
            self.assertEqual(run_compactor.count_workflows(guides_dir), 0)

            # Gotchas file with structured issues
            gotchas_md = guides_dir / "gotchas.md"
            gotchas_md.write_text("""# Failure Modes
## 1. Major Blockers
### GOTCHA-001: First major
- **Severity**: Major Blocker
### GOTCHA-002: Second major
- **Severity**: Major Blocker

## 2. Minor Quirks
### GOTCHA-003: First minor
- **Severity**: Minor Quirk
""", encoding="utf-8")

            counts = run_compactor.count_gotchas(guides_dir)
            self.assertEqual(counts["total"], 3)
            self.assertEqual(counts["major"], 2)
            self.assertEqual(counts["minor"], 1)

            # Flow file with numbered flows
            flow_md = guides_dir / "flow.md"
            flow_md.write_text("""# Execution Flows
## 1. Test Execution Flow
Step 1
## 2. Compaction Flow
Step 2
## 3. Git Release Flow
Step 3
## 4. Deploy Flow
Step 4
""", encoding="utf-8")

            flows = run_compactor.count_workflows(guides_dir)
            self.assertEqual(flows, 4)

    def test_report_with_inventory_gotchas_and_workflows(self):
        """Tests that print_report outputs inventory, gotchas, workflows, and dynamic topics cleanly."""
        import io

        git_info = {
            "branch": "feat/test",
            "head_hash": "abcdef1",
            "head_msg": "test commit",
            "tracking": "up to date",
        }
        inventory = [
            {"filename": "agent.md", "lines": 50, "category": "Master Index", "status": "Active"},
            {"filename": "gotchas.md", "lines": 40, "category": "Failure Modes", "status": "Active"},
            {"filename": "flow.md", "lines": 30, "category": "Execution Flows", "status": "Active"},
            {"filename": "commands.md", "lines": 20, "category": "Dynamic Topic", "status": "Active"},
        ]
        gotchas = {"total": 5, "major": 3, "minor": 2}

        buf = io.StringIO()
        old_stdout = sys.stdout
        try:
            sys.stdout = buf
            run_compactor.print_report(
                git_info=git_info,
                modified_nodes=[],
                dir_summary={"src": ["app.py"]},
                manifests=["package.json"],
                guides_inventory=inventory,
                gotchas_counts=gotchas,
                workflow_count=2,
            )
        finally:
            sys.stdout = old_stdout

        output = buf.getvalue()
        self.assertIn("Active Guides: 4 living guide files", output)
        self.assertIn("Dynamic Topics:commands.md", output)
        self.assertIn("Gotchas Bank:  5 entries (3 major blockers, 2 minor quirks)", output)
        self.assertIn("Workflows:     2 execution flows documented in flow.md", output)

    def test_count_gotchas_robustness_and_section_fallback(self):
        """Tests count_gotchas when total < major + minor, and when explicit severity tags are omitted."""
        with tempfile.TemporaryDirectory() as tmpdir:
            guides_dir = Path(tmpdir)
            gotchas_file = guides_dir / "gotchas.md"

            # Case 1: 1 GOTCHA- prefix, but 2 Major Blockers with severity tags -> total must be >= 2
            gotchas_file.write_text("""# Failure Modes
## 1. Major Blockers
### GOTCHA-001: First major
- **Severity**: Major Blocker

### Bug Without Gotcha Prefix
- **Severity**: Major Blocker
""", encoding="utf-8")
            counts = run_compactor.count_gotchas(guides_dir)
            self.assertEqual(counts["major"], 2)
            self.assertEqual(counts["minor"], 0)
            self.assertEqual(counts["total"], 2)

            # Case 2: No explicit severity tags, but headings placed under section titles
            gotchas_file.write_text("""# Failure Modes
## 1. Major Blockers (Fatal Crashes)
### Memory leak in background worker
Root cause...

### Data race in database connection pool
Root cause...

## 2. Minor Quirks (CLI & Formatting)
### CLI flag casing mismatch
Root cause...
""", encoding="utf-8")
            counts_sec = run_compactor.count_gotchas(guides_dir)
            self.assertEqual(counts_sec["major"], 2)
            self.assertEqual(counts_sec["minor"], 1)
            self.assertEqual(counts_sec["total"], 3)

    def test_count_workflows_unnumbered_headings(self):
        """Tests count_workflows with unnumbered markdown headings."""
        with tempfile.TemporaryDirectory() as tmpdir:
            guides_dir = Path(tmpdir)
            flow_file = guides_dir / "flow.md"
            flow_file.write_text("""# Execution Flows
## Test Execution Flow
Commands...

## Context Compaction Flow
Commands...

## Release Deployment Flow
Commands...
""", encoding="utf-8")
            flows = run_compactor.count_workflows(guides_dir)
            self.assertEqual(flows, 3)

    def test_seed_static_templates_inferred_root(self):
        """Tests that seed_static_templates infers root_dir from guides_dir.parent when root_dir is None."""
        templates_dir = Path(__file__).resolve().parent.parent / "dev-md-compactor" / "templates"
        with tempfile.TemporaryDirectory() as tmpdir:
            root_dir = Path(tmpdir)
            guides_dir = root_dir / "dev_md_guides"
            guides_dir.mkdir()

            run_compactor.seed_static_templates(guides_dir, templates_dir=templates_dir, root_dir=None)

            # dev_com_agent.md should be seeded at root_dir
            self.assertTrue((root_dir / "dev_com_agent.md").exists())
            self.assertTrue((guides_dir / "agent.md").exists())
            self.assertTrue((guides_dir / "gotchas.md").exists())
            self.assertTrue((guides_dir / "flow.md").exists())

    def test_agent_md_inventory_self_consistent_line_count(self):
        """Tests that agent.md's recorded line count inside its own inventory matches actual line count."""
        with tempfile.TemporaryDirectory() as tmpdir:
            guides_dir = Path(tmpdir)
            (guides_dir / "agent.md").write_text("""# Master Agent Index
<!-- AUTO-GENERATED BY COMPACTOR: DO NOT EDIT DIRECTLY -->
| old |
<!-- END AUTO-GENERATED INVENTORY -->
""", encoding="utf-8")
            (guides_dir / "branch.md").write_text("line1\nline2\nline3\n", encoding="utf-8")
            (guides_dir / "features.md").write_text("line1\nline2\n", encoding="utf-8")

            run_compactor.update_agent_inventory(guides_dir)

            agent_text = (guides_dir / "agent.md").read_text(encoding="utf-8")
            actual_lines = len(agent_text.splitlines())

            # Find agent.md row in the generated table
            import re
            match = re.search(r"\|\s*`agent\.md`\s*\|\s*(\d+)\s*\|", agent_text)
            self.assertIsNotNone(match, "agent.md should be in the inventory table")
            recorded_lines = int(match.group(1))
            self.assertEqual(
                recorded_lines, actual_lines,
                f"Recorded lines ({recorded_lines}) should match actual lines ({actual_lines})"
            )

    def test_gather_context_sh_with_dynamic_topic_guide(self):
        """Tests gather_context.sh reporting dynamic topic guides if bash is available."""
        git_bash = Path(r"C:\Program Files\Git\bin\bash.exe")
        bash_cmd = str(git_bash) if git_bash.exists() else shutil.which("bash")
        if not bash_cmd:
            self.skipTest("Bash executable not available")

        script_path = Path(__file__).resolve().parent.parent / "dev-md-compactor" / "scripts" / "gather_context.sh"
        if not script_path.exists():
            self.skipTest("gather_context.sh not found")

        with tempfile.TemporaryDirectory() as tmpdir:
            root_dir = Path(tmpdir)
            guides_dir = root_dir / "dev_md_guides"
            guides_dir.mkdir()

            # Init minimal git repo
            subprocess.run(["git", "init"], cwd=str(root_dir), check=True, capture_output=True)
            subprocess.run(["git", "config", "user.name", "Test"], cwd=str(root_dir), check=True)
            subprocess.run(["git", "config", "user.email", "test@example.com"], cwd=str(root_dir), check=True)

            # Create dynamic topic file
            dynamic_file = guides_dir / "database.md"
            dynamic_file.write_text("# Database Operations\nRun migrations\n", encoding="utf-8")

            res = subprocess.run([bash_cmd, str(script_path), "."], cwd=str(root_dir), capture_output=True, text=True, encoding="utf-8", errors="replace")
            self.assertEqual(res.returncode, 0, f"gather_context.sh failed: {res.stderr}")
            self.assertIn("database.md (dynamic topic guide detected", res.stdout)
            self.assertIn("=== database.md ===", res.stdout)
            self.assertIn("Run migrations", res.stdout)


class TestInstallerScripts(unittest.TestCase):
    def test_installer_files_exist_and_pure_ascii(self):
        repo_root = Path(__file__).resolve().parent.parent
        install_dir = repo_root / "install"
        ps1_file = install_dir / "install.ps1"
        sh_file = install_dir / "install.sh"
        md_file = install_dir / "INSTALL.md"

        self.assertTrue(ps1_file.exists(), "install.ps1 must exist")
        self.assertTrue(sh_file.exists(), "install.sh must exist")
        self.assertTrue(md_file.exists(), "INSTALL.md must exist")

        # Verify pure ASCII compliance for install.ps1 and install.sh
        # to prevent Windows PowerShell 5.1 CP1252 parsing bugs
        for script_file in [ps1_file, sh_file]:
            raw_bytes = script_file.read_bytes()
            non_ascii = [b for b in raw_bytes if b > 127]
            self.assertEqual(len(non_ascii), 0, f"{script_file.name} contains non-ASCII bytes: {non_ascii[:5]}")

    def test_agent_memory_path_resolution_antigravity(self):
        repo_root = Path(__file__).resolve().parent.parent
        skill_md = repo_root / "agent-memory" / "SKILL.md"
        self.assertTrue(skill_md.exists())
        content = skill_md.read_text(encoding="utf-8")
        self.assertIn(".gemini/config/skills/agent-memory/.agent-config", content)
        self.assertIn("AGENT_SYSTEM_PATH", content)

    def test_powershell_installer_dry_run_override(self):
        # Verify install.ps1 runs with -SkillFolderOverride in a temp directory
        ps_cmd = shutil.which("powershell.exe") or shutil.which("pwsh")
        if not ps_cmd:
            self.skipTest("PowerShell not available")

        repo_root = Path(__file__).resolve().parent.parent
        ps1_file = repo_root / "install" / "install.ps1"

        with tempfile.TemporaryDirectory() as tmpdir:
            dest_dir = Path(tmpdir) / "skills"
            cmd = [
                ps_cmd,
                "-ExecutionPolicy", "Bypass",
                "-File", str(ps1_file),
                "-SkillFolderOverride", str(dest_dir),
                "-Skill", "all",
                "-Yes"
            ]
            res = subprocess.run(cmd, cwd=str(repo_root), capture_output=True, text=True, errors="replace")
            self.assertEqual(res.returncode, 0, f"install.ps1 failed: {res.stderr}\n{res.stdout}")
            self.assertTrue((dest_dir / "agent-memory" / "SKILL.md").exists(), "agent-memory SKILL.md not installed")
            self.assertTrue((dest_dir / "dev-md-compactor" / "SKILL.md").exists(), "dev-md-compactor SKILL.md not installed")
            self.assertTrue((dest_dir / "dev-md-compactor" / "scripts" / "run_compactor.py").exists(), "run_compactor.py not installed")


if __name__ == "__main__":
    unittest.main()

