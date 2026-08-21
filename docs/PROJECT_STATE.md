# Project State

Last updated: 2026-08-21
State based on commit: `1746d224ccfa80a719784f9c4ba652d21e3cde88`
Status: active

## Purpose

Project Context System (PCS) is a reusable, Git-native and GitHub-first context continuity layer for AI-first software projects.

Its purpose is to let a fresh AI session reconstruct current project truth and continue development without depending on previous chat history.

## Confirmed principles

- Git repository is authoritative project memory.
- Chat/session is ephemeral workspace, not source of truth.
- One type of truth has one owner document.
- Project-specific facts are CONFIRMED, INFERRED, UNKNOWN, STALE, or CONFLICT; missing facts are not invented.
- Context is updated with semantic project changes.
- Evidence is required for acceptance claims.
- Handoff is derived from repository truth and is not a second permanent truth file.
- GitHub Issues/Projects/PRs coordinate execution but do not replace repository truth.
- Server/runtime access is outside default agent scope until an explicit live task grants it.
- Natural-language installation is supported: a user may give an AI only the PCS repository URL and ask it to add the system.
- `PCS READY` means readiness validation passed, not merely that files were copied.

## Implemented

- `AGENTS.md` behavior contract.
- `AGENT_INSTALL.md` natural-language installation protocol.
- `pcs-manifest.json` machine-readable entrypoint.
- `.project/state.json` bootstrap/freshness index.
- `PROJECT_STATE`, `ACTIVE_WORK`, `ARCHITECTURE`, `ROADMAP`, ADR, INCIDENTS, and EVIDENCE layers.
- `minimal`, `standard`, and `large` installation profiles.
- Cross-platform Python installer.
- Structural validation and `--ready` readiness validation.
- GitHub Issue Forms, PR template, CODEOWNERS, Actions, labels/Project/ruleset manifests, and safe GitHub setup helper.
- Automated installer, integration, regression, and readiness tests.

## Accepted V1 baseline

PR #1 was merged into `main` as squash commit `1746d224ccfa80a719784f9c4ba652d21e3cde88`.

The PR implementation and final context commits passed the PCS Context Check before merge, including:

- minimal / standard / large installation;
- existing-file protection;
- GitHub integration assertions;
- CODEOWNERS rendering;
- untouched bootstrap readiness FAIL as designed;
- populated context readiness PASS.

The squash merge created a new immutable `main` SHA, so this context snapshot was reconciled to that SHA immediately after merge.

## Current work

- First external real-product installation smoke test: Issue #2.
- V1.1 safe GitHub Project/Ruleset automation: Issue #3.

## Known limitations

- First external installation in a real product repository is still pending Issue #2.
- Semantic drift detection beyond structural/readiness checks is conservative in V1.
- `--force` is replacement-oriented, not a schema-aware migration engine.
- Secret scanning, ADR lint, internal-link validation, and automatic Project/Ruleset reconciliation are future work.

## Current truth boundaries

`PROJECT_STATE.md` describes what is true now, not chronological history.
Decision rationale belongs in ADRs, failure learning in INCIDENTS, acceptance in EVIDENCE, and chronology in Git.
