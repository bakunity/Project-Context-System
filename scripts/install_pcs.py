#!/usr/bin/env python3
"""Install Project Context System into an existing repository."""

from __future__ import annotations

import argparse
import re
import shutil
import subprocess
import sys
from datetime import date
from pathlib import Path

PCS_ROOT = Path(__file__).resolve().parents[1]
TEMPLATES = PCS_ROOT / "templates"


def git_value(root: Path, *args: str, fallback: str) -> str:
    try:
        proc = subprocess.run(
            ["git", "-C", str(root), *args],
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
        )
    except FileNotFoundError:
        return fallback
    value = proc.stdout.strip()
    return value if proc.returncode == 0 and value else fallback


def github_owner(root: Path) -> str | None:
    remote = git_value(root, "config", "--get", "remote.origin.url", fallback="")
    if not remote:
        return None
    match = re.search(r"github\.com[/:]([^/]+)/[^/]+(?:\.git)?$", remote)
    return match.group(1) if match else None


def render(text: str, values: dict[str, str]) -> str:
    for key, value in values.items():
        text = text.replace("{{" + key + "}}", value)
    return text


def existing_files(root: Path) -> set[Path]:
    return {path.relative_to(root) for path in root.rglob("*") if path.is_file()}


def copy_overlay(source: Path, target: Path, values: dict[str, str], force: bool, protected: set[Path]) -> tuple[list[str], list[str]]:
    created: list[str] = []
    skipped: list[str] = []
    for src in sorted(source.rglob("*")):
        if not src.is_file():
            continue
        rel = src.relative_to(source)
        dst = target / rel
        if rel in protected and not force:
            skipped.append(str(rel))
            continue
        dst.parent.mkdir(parents=True, exist_ok=True)
        text = src.read_text(encoding="utf-8")
        dst.write_text(render(text, values), encoding="utf-8")
        created.append(str(rel))
    return created, skipped


def copy_file(src: Path, dst: Path, target: Path, force: bool, protected: set[Path]) -> str:
    rel = dst.relative_to(target)
    if rel in protected and not force:
        return "skipped"
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dst)
    return "created"


def main() -> int:
    parser = argparse.ArgumentParser(description="Install PCS into a Git project")
    parser.add_argument("target", nargs="?", default=".", help="Target repository path")
    parser.add_argument("--profile", choices=["minimal", "standard", "large"], default="standard")
    parser.add_argument("--force", action="store_true", help="Overwrite files that existed before installation")
    args = parser.parse_args()

    target = Path(args.target).resolve()
    target.mkdir(parents=True, exist_ok=True)
    protected = existing_files(target)

    project_name = target.name
    base_commit = git_value(target, "rev-parse", "HEAD", fallback="UNCOMMITTED")
    branch = git_value(target, "branch", "--show-current", fallback="UNKNOWN")
    owner = github_owner(target)
    if owner:
        codeowner_line = f"* @{owner}"
        codeowner_context = f"/.project/ @{owner}\n/AGENTS.md @{owner}\n/docs/ARCHITECTURE.md @{owner}\n/docs/ADR/ @{owner}\n/.github/ @{owner}"
    else:
        codeowner_line = "# * @your-github-user-or-team"
        codeowner_context = "# Review CODEOWNERS after connecting the GitHub origin."

    values = {
        "PROJECT_NAME": project_name,
        "DATE": date.today().isoformat(),
        "BASE_COMMIT": base_commit,
        "ACTIVE_BRANCH": branch,
        "CODEOWNER_LINE": codeowner_line,
        "CODEOWNER_CONTEXT_LINE": codeowner_context,
    }

    overlays = [TEMPLATES / "minimal"]
    if args.profile in {"standard", "large"}:
        overlays.append(TEMPLATES / "standard")
    if args.profile == "large":
        overlays.append(TEMPLATES / "large")

    all_created: list[str] = []
    all_skipped: list[str] = []
    for overlay in overlays:
        created, skipped = copy_overlay(overlay, target, values, args.force, protected)
        all_created.extend(created)
        all_skipped.extend(skipped)

    if args.profile in {"standard", "large"}:
        extras = [
            (PCS_ROOT / "scripts/validate_context.py", target / "scripts/validate_context.py"),
            (PCS_ROOT / "scripts/setup_github.py", target / "scripts/setup_github.py"),
            (PCS_ROOT / ".github/workflows/pcs-context-check.yml", target / ".github/workflows/pcs-context-check.yml"),
        ]
        for src, dst in extras:
            result = copy_file(src, dst, target, args.force, protected)
            rel = str(dst.relative_to(target))
            (all_created if result == "created" else all_skipped).append(rel)

    print(f"PCS installed: profile={args.profile} target={target}")
    print(f"Created/updated: {len(all_created)}")
    for item in all_created:
        print(f"  + {item}")

    if all_skipped:
        print(f"Protected existing files: {len(all_skipped)}")
        for item in sorted(set(all_skipped)):
            print(f"  = {item}")
        print("Use --force only after reviewing existing project context.")

    print("\nNext steps:")
    print("1. Fill PROJECT_STATE, ARCHITECTURE and ROADMAP with real project truth.")
    if args.profile in {"standard", "large"}:
        print("2. Fill ACTIVE_WORK and review GitHub Issue/CODEOWNERS integration.")
        print(f"3. Run: python {target / 'scripts/validate_context.py'} {target}")
        print("4. Review diff and commit PCS as the initial context baseline.")
        print("5. Push to GitHub; optionally run setup_github.py --apply-labels.")
        print("6. Develop through Issues/branches/PR/CI; keep server access outside scope until an explicit live gate.")
    else:
        print("2. Review diff and commit PCS together with its initial context snapshot.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
