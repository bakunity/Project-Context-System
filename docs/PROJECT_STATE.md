# Project State

Last updated: 2026-08-21
State based on commit: `d2aa8e0f7ad4f44f1dbc1c112e295ff77a37d9d8`
Last verified commit: `d2aa8e0f7ad4f44f1dbc1c112e295ff77a37d9d8`
Status: review

## Purpose

Project Context System (PCS) is a reusable, Git-native context continuity layer for AI-first software projects.

Its purpose is to let a new AI session or developer reconstruct current project truth without depending on previous chat history.

## Confirmed principles

- Git repository is authoritative project memory.
- Chat/session is ephemeral workspace, not source of truth.
- One type of truth has one owner document.
- Context updates happen on semantic state transitions, not after every code edit.
- Evidence is required for acceptance claims.
- Project-specific `memories/` is intentionally avoided because it duplicates repository truth.
- Handoff is a derived artifact, not a permanent truth file.
- Machine-readable state points to human-readable truth; it does not duplicate architecture prose.
- `state_based_on_commit` is a baseline SHA used for drift inspection, not a self-reference to the commit containing `state.json`.

## Implemented

- Repository and user-facing README initialized.
- Canonical `AGENTS.md` behavior contract.
- Machine-readable `.project/state.json`.
- Project state, active work, architecture, roadmap, ADR, incident, and evidence layers.
- `minimal`, `standard`, and `large` installation profiles.
- Cross-platform Python installer.
- Structural context validator.
- GitHub Actions context check.
- Evidence-oriented pull request template.
- Automated installer tests for all profiles and existing-file protection.

## Verified

Commit `d2aa8e0f7ad4f44f1dbc1c112e295ff77a37d9d8` passed:

- PCS structural validation;
- minimal profile installation test;
- standard profile installation + validation test;
- large profile installation test;
- existing-file non-overwrite protection test.

See `docs/EVIDENCE.md`.

## In progress

- Review of PR #1.
- External repository installation smoke test before V1 merge.

## Known limitations

- Installer has not yet been smoke-tested against a separate real repository outside the automated temporary-repository test.
- Automatic semantic drift detection is intentionally conservative in V1.
- `--force` is replacement-oriented, not yet a schema-aware upgrade/migration engine.
- Secret scanning, ADR linting, and internal-link validation are planned but not implemented.

## Current truth boundaries

`PROJECT_STATE.md` describes what is true now.
It must not become a chronological development diary.

Detailed historical reasoning belongs in ADRs, incidents, evidence, and Git history.
