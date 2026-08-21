#!/usr/bin/env python3
"""Validate the structural contract of a Project Context System installation."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

REQUIRED_CORE = [
    "AGENTS.md",
    ".project/state.json",
    "docs/PROJECT_STATE.md",
    "docs/ARCHITECTURE.md",
    "docs/ROADMAP.md",
    "docs/ADR/README.md",
]

REQUIRED_STATE_KEYS = {
    "schema_version",
    "project",
    "state_doc",
    "architecture_doc",
    "roadmap_doc",
    "adr_dir",
    "state_based_on_commit",
    "status",
    "updated_at",
}

POINTER_KEYS = {
    "state_doc",
    "active_work_doc",
    "architecture_doc",
    "roadmap_doc",
    "adr_dir",
    "incidents_dir",
    "evidence_doc",
}


def git(root: Path, *args: str) -> tuple[int, str]:
    p = subprocess.run(
        ["git", "-C", str(root), *args],
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    return p.returncode, (p.stdout or p.stderr).strip()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("root", nargs="?", default=".")
    args = parser.parse_args()

    root = Path(args.root).resolve()
    errors: list[str] = []
    warnings: list[str] = []

    for rel in REQUIRED_CORE:
        if not (root / rel).exists():
            errors.append(f"missing required file: {rel}")

    state_path = root / ".project/state.json"
    state: dict = {}
    if state_path.exists():
        try:
            state = json.loads(state_path.read_text(encoding="utf-8"))
        except Exception as exc:
            errors.append(f"invalid .project/state.json: {exc}")

    if state:
        missing = sorted(REQUIRED_STATE_KEYS - set(state))
        for key in missing:
            errors.append(f"state.json missing key: {key}")

        if state.get("schema_version") != 1:
            errors.append("unsupported schema_version; expected 1")

        for key in POINTER_KEYS:
            value = state.get(key)
            if not value:
                continue
            if not (root / value).exists():
                errors.append(f"state pointer {key} does not exist: {value}")

        base = state.get("state_based_on_commit")
        if base:
            code, _ = git(root, "rev-parse", "--git-dir")
            if code == 0:
                code, output = git(root, "cat-file", "-e", f"{base}^{{commit}}")
                if code != 0:
                    warnings.append(
                        "state_based_on_commit is not present in local Git history; "
                        "this can be normal immediately after installation before first context commit"
                    )
                else:
                    code, _ = git(root, "merge-base", "--is-ancestor", base, "HEAD")
                    if code != 0:
                        errors.append("state_based_on_commit is not an ancestor of HEAD")
                    else:
                        code, head = git(root, "rev-parse", "HEAD")
                        if code == 0 and not head.startswith(base):
                            warnings.append(
                                "HEAD differs from state_based_on_commit; inspect relevant diff for context drift"
                            )

    if errors:
        print("PCS validation: FAIL")
        for item in errors:
            print(f"ERROR: {item}")
        for item in warnings:
            print(f"WARN: {item}")
        return 1

    print("PCS validation: PASS")
    for item in warnings:
        print(f"WARN: {item}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
