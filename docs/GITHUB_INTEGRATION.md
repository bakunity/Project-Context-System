# GitHub Integration

PCS is **Git-native and GitHub-first**, not GitHub-only.

The repository files are the durable context protocol. GitHub adds an operational layer that helps humans and agents coordinate work without moving project truth out of Git.

## Responsibility split

| Concern | Owner |
| --- | --- |
| Current project truth | `docs/PROJECT_STATE.md` |
| Current execution/workstream | `docs/ACTIVE_WORK.md` |
| Architecture and invariants | `docs/ARCHITECTURE.md` + ADR |
| Strategy | `docs/ROADMAP.md` |
| Unit of work | GitHub Issue |
| Implementation review | Pull Request |
| Automated verification | GitHub Actions |
| Operational planning | GitHub Project |
| Merge governance | GitHub Rulesets / CODEOWNERS |
| Runtime acceptance | Evidence + explicit staging/live task |

## Default development lifecycle

```text
New GitHub repository
  -> install PCS
  -> fill initial project truth
  -> commit baseline
  -> create Issues
  -> agent works on bounded branch/task
  -> tests + CI
  -> Pull Request
  -> review/merge
  -> repeat
```

The server is intentionally outside the default loop.

When product implementation reaches a runtime milestone:

```text
repository implementation accepted
  -> explicit staging/server task
  -> deploy staging
  -> smoke/live verification
  -> EVIDENCE update
  -> production approval if needed
```

An agent must not infer server access from the existence of deployment files or credentials.

## Issues

Issues are the canonical **unit of work**, but they are not project truth. Closing an issue means the work item is resolved according to its acceptance criteria; it does not automatically prove production behavior.

PCS ships forms for bug, feature, architecture change, incident, and context drift.

## GitHub Project

Use a Project for execution visibility. Recommended fields are stored in `.project/github/project-model.json`.

`ROADMAP.md` answers *where the product is going*.
The GitHub Project answers *which concrete work items are moving now*.

## Pull Requests

Every substantial change should connect issue -> branch -> PR -> tests/evidence. Agent-generated work must report the exact base SHA and exact tests executed.

## Rulesets and CODEOWNERS

Rulesets turn PCS rules into enforcement: require PRs, status checks, resolved conversations, and protection from force-push/deletion on the main branch.

`CODEOWNERS` is useful when ownership exists. The installer renders the GitHub repository owner when it can detect one; review it after installation.

## No Wiki

PCS intentionally does not use GitHub Wiki as a project truth layer. Long-lived engineering knowledge belongs in repository docs so it is versioned and reviewed with code.
