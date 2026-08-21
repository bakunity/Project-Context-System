from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INSTALLER = ROOT / "scripts/install_pcs.py"
VALIDATOR = ROOT / "scripts/validate_context.py"


def run(*args: str, cwd: Path | None = None) -> subprocess.CompletedProcess[str]:
    return subprocess.run(list(args), cwd=cwd, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)


def init_repo(root: Path) -> str:
    run("git", "init", "-b", "main", cwd=root)
    run("git", "config", "user.email", "pcs-test@example.invalid", cwd=root)
    run("git", "config", "user.name", "PCS Test", cwd=root)
    run("git", "remote", "add", "origin", "https://github.com/example-org/example-repo.git", cwd=root)
    (root / "README.md").write_text("# Fixture\n", encoding="utf-8")
    run("git", "add", "README.md", cwd=root)
    result = run("git", "commit", "-m", "fixture", cwd=root)
    if result.returncode != 0:
        raise RuntimeError(result.stderr)
    return run("git", "rev-parse", "HEAD", cwd=root).stdout.strip()


class InstallerTests(unittest.TestCase):
    def install(self, profile: str) -> tuple[Path, str, tempfile.TemporaryDirectory[str]]:
        tmp = tempfile.TemporaryDirectory()
        root = Path(tmp.name)
        base = init_repo(root)
        result = run(sys.executable, str(INSTALLER), str(root), "--profile", profile)
        self.assertEqual(result.returncode, 0, result.stderr)
        return root, base, tmp

    def test_minimal_profile(self) -> None:
        root, base, tmp = self.install("minimal")
        self.addCleanup(tmp.cleanup)
        self.assertTrue((root / "AGENTS.md").exists())
        self.assertTrue((root / "docs/PROJECT_STATE.md").exists())
        self.assertTrue((root / "docs/ARCHITECTURE.md").exists())
        self.assertTrue((root / "docs/ROADMAP.md").exists())
        self.assertTrue((root / "docs/ADR/README.md").exists())
        self.assertFalse((root / "docs/ACTIVE_WORK.md").exists())
        state = json.loads((root / ".project/state.json").read_text(encoding="utf-8"))
        self.assertEqual(state["project"], root.name)
        self.assertEqual(state["state_based_on_commit"], base)
        self.assertIsNone(state["active_work_doc"])

    def test_standard_profile_and_validator(self) -> None:
        root, base, tmp = self.install("standard")
        self.addCleanup(tmp.cleanup)
        required = [
            "docs/ACTIVE_WORK.md",
            "docs/INCIDENTS/README.md",
            "docs/EVIDENCE.md",
            "docs/GITHUB_INTEGRATION.md",
            "scripts/validate_context.py",
            "scripts/setup_github.py",
            ".github/workflows/pcs-context-check.yml",
            ".github/ISSUE_TEMPLATE/bug.yml",
            ".github/ISSUE_TEMPLATE/feature.yml",
            ".github/ISSUE_TEMPLATE/architecture.yml",
            ".github/ISSUE_TEMPLATE/incident.yml",
            ".github/ISSUE_TEMPLATE/context-drift.yml",
            ".github/CODEOWNERS",
            ".project/github/labels.json",
            ".project/github/project-model.json",
            ".project/github/ruleset-policy.json",
        ]
        for rel in required:
            self.assertTrue((root / rel).exists(), rel)
        codeowners = (root / ".github/CODEOWNERS").read_text(encoding="utf-8")
        self.assertIn("@example-org", codeowners)
        state = json.loads((root / ".project/state.json").read_text(encoding="utf-8"))
        self.assertEqual(state["state_based_on_commit"], base)
        self.assertEqual(state["active_work_doc"], "docs/ACTIVE_WORK.md")
        validation = run(sys.executable, str(VALIDATOR), str(root))
        self.assertEqual(validation.returncode, 0, validation.stdout + validation.stderr)

    def test_large_profile(self) -> None:
        root, _, tmp = self.install("large")
        self.addCleanup(tmp.cleanup)
        for name in ["PRODUCT.md", "BACKEND.md", "FRONTEND.md", "INFRASTRUCTURE.md"]:
            self.assertTrue((root / "docs/CONTEXT" / name).exists())
        self.assertTrue((root / "docs/research/README.md").exists())

    def test_existing_files_are_not_overwritten_without_force(self) -> None:
        root, _, tmp = self.install("minimal")
        self.addCleanup(tmp.cleanup)
        sentinel = "# custom agent rules\n"
        (root / "AGENTS.md").write_text(sentinel, encoding="utf-8")
        result = run(sys.executable, str(INSTALLER), str(root), "--profile", "minimal")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual((root / "AGENTS.md").read_text(encoding="utf-8"), sentinel)


if __name__ == "__main__":
    unittest.main()
