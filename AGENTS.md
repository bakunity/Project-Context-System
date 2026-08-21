# Repository Agent Rules

## Source of truth

Repository state beats chat/session memory.

Do not use previous conversation memory as authoritative project-specific truth when repository evidence is available or required.

## Bootstrap

Before planning or changing code:

1. Read `.project/state.json`.
2. Read `docs/PROJECT_STATE.md`.
3. Read `docs/ARCHITECTURE.md`.
4. Read `docs/ACTIVE_WORK.md` when it exists.
5. Read only ADR/context documents relevant to the task.
6. Inspect `git status --short`.
7. Inspect recent commits.
8. Compare current HEAD with `state_based_on_commit`.
9. If they differ, inspect the diff and classify context as current, stale, or conflicting.
10. Summarize current understanding before implementation.

## Knowledge status

Use these labels when project truth is uncertain:

- `CONFIRMED` — backed by repository/runtime evidence.
- `INFERRED` — strongly implied by code but not recorded as authoritative truth.
- `UNKNOWN` — not found.
- `STALE` — documentation is older than relevant code/state.
- `CONFLICT` — authoritative sources disagree.

Never silently turn `INFERRED` or `UNKNOWN` into `CONFIRMED`.

## Scope

Respect task-specific allowed and forbidden paths.
Do not expand scope silently.
Prefer the smallest change that satisfies the task unless refactoring is explicitly allowed.

## Architecture changes

An architecture change is incomplete unless relevant code, tests, `docs/ARCHITECTURE.md`, and an ADR are updated together.

## Bug fixes

Significant bug fixes should record root cause, regression protection, evidence, and an incident entry when appropriate.

## Verification

The phrase `done` is not evidence.
Report exact tests, smoke checks, environment, limitations, and anything not verified.

Static CI PASS does not automatically mean live/runtime PASS.
A failing test harness does not automatically mean the product is broken; verify independent state when reasonable.

## Git

Work from an explicit base commit for bounded agent tasks.
Do not claim a moving branch was tested when only an older SHA was tested.

## Context updates

Update persistent context in the same change that changes project truth.
Do not create duplicate truth files for the same responsibility.

Ownership:

- `PROJECT_STATE.md` = current project truth.
- `ACTIVE_WORK.md` = current execution/workstream.
- `ARCHITECTURE.md` = system structure.
- `ROADMAP.md` = future direction.
- `ADR/*` = why a decision was made.
- `INCIDENTS/*` = failure/root-cause memory.
- `EVIDENCE.md` = accepted verification memory.
- Git = history.

## Secrets

Never write secrets, tokens, private keys, credentials, or sensitive raw logs into context, docs, evidence, ADRs, or incidents.

## Approval boundaries

Merge, deploy, release, destructive operations, production mutation, and irreversible actions require explicit approval unless the task explicitly grants it.

## Codex / agent task brief

For substantial delegated work, define:

- Goal
- Base commit
- Context to read
- Allowed files/paths
- Forbidden files/paths
- Required behavior
- Must preserve
- Change policy
- Tests to run
- Smoke test
- Context/docs that may need update
- Approval required before
- Expected report

Expected report should contain plan, changed files, diff summary, tests, smoke, evidence, not verified, known limitations, context updates, and next safe action.
