# Project State

Last updated: 2026-08-21
State based on commit: `50912e530a21e722ce3eff1b94410ae3c8fe84b1`
Last verified commit: `50912e530a21e722ce3eff1b94410ae3c8fe84b1`
Status: review

## Purpose

Project Context System (PCS) is a reusable, Git-native context continuity layer for AI-first software projects.

Its purpose is to let a new AI session or developer reconstruct current project truth without depending on previous chat history.

PCS is GitHub-first for operational workflow, but the core context protocol remains Git-native and repository-local.

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
- GitHub Issues are units of work, Projects are execution views, and PRs are implementation review; none replaces repository truth.
- Server/runtime access is outside default agent scope until an explicit live/staging task grants it.

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
- GitHub Issue Forms for bug, feature, architecture, incident, and context drift.
- GitHub CODEOWNERS template with installer owner detection from `origin`.
- GitHub label, Project-model, and ruleset-policy manifests.
- Safe `setup_github.py` helper for applying labels through GitHub CLI.
- Explicit development-vs-runtime boundary in agent rules and architecture.
- `docs/GITHUB_INTEGRATION.md` installed with the standard profile.

## Verified

Commit `50912e530a21e722ce3eff1b94410ae3c8fe84b1` passed:

- PCS structural validation;
- minimal profile installation test;
- standard profile installation + validation test;
- large profile installation test;
- existing-file non-overwrite protection test;
- standard profile assertions for Issue Forms, CODEOWNERS, GitHub manifests, integration docs, and `setup_github.py`;
- CODEOWNERS owner rendering from a GitHub `origin` URL.

See `docs/EVIDENCE.md`.

## In progress

- Review of PR #1 as the first mergeable PCS release candidate.
- External installation smoke test against the next real product repository before or immediately after V1 merge.
- Decide when to automate GitHub Project and Ruleset application; V1 keeps those governance mutations declarative/manual by design.

## Known limitations

- Installer has not yet been smoke-tested against a separate real repository outside the automated temporary-repository test.
- Automatic semantic drift detection is intentionally conservative in V1.
- `--force` is replacement-oriented, not yet a schema-aware upgrade/migration engine.
- Secret scanning, ADR linting, internal-link validation, Project automation, and Ruleset automation are not yet implemented.
- GitHub Issue Form syntax is repository content but is not independently schema-validated by the current Python test suite.

## Current truth boundaries

`PROJECT_STATE.md` describes what is true now.
It must not become a chronological development diary.

Detailed historical reasoning belongs in ADRs, incidents, evidence, and Git history.
