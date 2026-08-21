# GitHub Integration

This project uses PCS as a Git-native context layer with GitHub as the operational layer.

## Ownership

- `PROJECT_STATE.md` = current project truth.
- `ACTIVE_WORK.md` = current execution.
- `ARCHITECTURE.md` + ADR = architecture and rationale.
- `ROADMAP.md` = strategy.
- GitHub Issues = units of work.
- GitHub Project = execution visibility.
- Pull Requests = implementation review.
- Actions = automated verification.
- Evidence = accepted verification memory.

## Default development phase

Server/runtime access is **not** implied.

Use repository code, local tests, CI, Issues and PRs first. Staging/server/live work starts only when a task explicitly grants runtime scope and the project reaches a live gate.

## Recommended flow

```text
Issue -> bounded branch/task -> implementation -> tests/CI -> PR -> merge -> next issue
```

When runtime verification is needed:

```text
repository implementation accepted -> explicit staging task -> deploy -> smoke/live evidence -> production approval if required
```

## GitHub configuration manifests

- `.project/github/labels.json`
- `.project/github/project-model.json`
- `.project/github/ruleset-policy.json`

Run `python scripts/setup_github.py --apply-labels` after reviewing the repository and GitHub authentication.
