# Repository Agent Rules

## Source of truth

Repository state beats chat/session memory.

## Bootstrap

Before changing the project:

1. Read `.project/state.json`.
2. Read `docs/PROJECT_STATE.md`.
3. Read `docs/ARCHITECTURE.md`.
4. Read relevant ADRs.
5. If `docs/ACTIVE_WORK.md` exists, read it.
6. Inspect Git status and recent commits.
7. Compare HEAD with `state_based_on_commit`.
8. Resolve any context drift before implementation.

## No guessing

Classify project-specific claims as `CONFIRMED`, `INFERRED`, `UNKNOWN`, `STALE`, or `CONFLICT`.
Never silently invent missing project truth.

## Scope

Respect task-specific allowed/forbidden paths and approval boundaries.
Do not expand scope silently.

## Context ownership

- `PROJECT_STATE.md` = current truth.
- `ACTIVE_WORK.md` = current execution, if present.
- `ARCHITECTURE.md` = system structure.
- `ROADMAP.md` = future direction.
- `ADR/*` = decision rationale.
- `INCIDENTS/*` = failure/root-cause memory, if present.
- `EVIDENCE.md` = accepted verification, if present.
- Git = history.

Update persistent context in the same change that changes project truth.

## Verification

`Done` is not evidence. Report exact tests, smoke checks, limitations, and what was not verified.

## Secrets

Never write secrets, tokens, private keys, credentials, or sensitive raw logs into project context.

## Approval

Merge, deploy, release, destructive operations, production mutation, and irreversible actions require explicit approval unless the task explicitly grants it.
