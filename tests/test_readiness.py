from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INSTALLER = ROOT / "scripts/install_pcs.py"


def run(*args: str, cwd: Path | None = None) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        list(args),
        cwd=cwd,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )


def init_repo(root: Path) -> None:
    run("git", "init", "-b", "main", cwd=root)
    run("git", "config", "user.email", "pcs-test@example.invalid", cwd=root)
    run("git", "config", "user.name", "PCS Test", cwd=root)
    (root / "README.md").write_text("# Example Product\n", encoding="utf-8")
    run("git", "add", "README.md", cwd=root)
    result = run("git", "commit", "-m", "initial product baseline", cwd=root)
    if result.returncode != 0:
        raise RuntimeError(result.stderr)


class ReadinessTests(unittest.TestCase):
    def test_ready_requires_real_context(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            init_repo(root)

            install = run(sys.executable, str(INSTALLER), str(root), "--profile", "standard")
            self.assertEqual(install.returncode, 0, install.stdout + install.stderr)

            validator = root / "scripts/validate_context.py"

            structural = run(sys.executable, str(validator), str(root))
            self.assertEqual(structural.returncode, 0, structural.stdout + structural.stderr)
            self.assertIn("structural validation: PASS", structural.stdout)

            not_ready = run(sys.executable, str(validator), str(root), "--ready")
            self.assertNotEqual(not_ready.returncode, 0)
            self.assertIn("readiness validation: FAIL", not_ready.stdout)
            self.assertIn("bootstrap", not_ready.stdout.lower())

            (root / "docs/PROJECT_STATE.md").write_text(
                "# Project State\n\n"
                "Status: development\n\n"
                "## Purpose\nExample Product is a test application used to verify PCS readiness.\n\n"
                "## Confirmed current truth\n- Git repository exists.\n- PCS standard profile is installed.\n\n"
                "## Implemented\n- Initial repository baseline.\n\n"
                "## In progress\n- Product development has not started.\n\n"
                "## Known limitations\n- Runtime is not configured.\n\n"
                "## Important constraints\n- Runtime access requires a later explicit live task.\n",
                encoding="utf-8",
            )
            (root / "docs/ARCHITECTURE.md").write_text(
                "# Architecture\n\n"
                "## System purpose\nExample Product is currently a repository-only test fixture.\n\n"
                "## Components\n- Repository source tree.\n- PCS context layer.\n\n"
                "## Data flow\nNo application data flow is implemented yet.\n\n"
                "## Deployment/runtime\nUNKNOWN; runtime is intentionally deferred.\n",
                encoding="utf-8",
            )
            (root / "docs/ROADMAP.md").write_text(
                "# Roadmap\n\n"
                "## Now\nEstablish the project baseline.\n\n"
                "## Next\nImplement the first product feature.\n\n"
                "## Later\nAdd runtime only after repository implementation is ready.\n\n"
                "## Explicitly deferred\nProduction deployment.\n",
                encoding="utf-8",
            )
            (root / "docs/ACTIVE_WORK.md").write_text(
                "# Active Work\n\n"
                "## Current goal\nFinish PCS bootstrap for the product repository.\n\n"
                "## Branch / PR\nBranch: `main`\nPR: not required for this temporary test repository.\n\n"
                "## Base commit\nInitial product baseline.\n\n"
                "## Accepted baseline\nGit repository exists and PCS is installed.\n\n"
                "## Current blocker\nNone.\n\n"
                "## Next step\nBegin the first bounded product task.\n\n"
                "## Tests already accepted\nPCS structural validation.\n\n"
                "## Approval gate\nServer/runtime changes require explicit approval.\n",
                encoding="utf-8",
            )

            state_path = root / ".project/state.json"
            state = json.loads(state_path.read_text(encoding="utf-8"))
            state["status"] = "development"
            state_path.write_text(json.dumps(state, indent=2) + "\n", encoding="utf-8")

            ready = run(sys.executable, str(validator), str(root), "--ready")
            self.assertEqual(ready.returncode, 0, ready.stdout + ready.stderr)
            self.assertIn("readiness validation: PASS", ready.stdout)


if __name__ == "__main__":
    unittest.main()
