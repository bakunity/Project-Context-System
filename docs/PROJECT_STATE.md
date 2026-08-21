# Project State

Last updated: 2026-08-21
State based on commit: `d6b8aaa4e1450841a601daa77d9da26aae101c88`
Status: implementation

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

## Implemented

- Project repository initialized.
- PCS concept and bootstrap documented in README.
- V1 foundation workstream started.

## In progress

- Canonical agent rules.
- Machine-readable project state.
- Project documentation model.
- Reusable installation profiles.
- Context validator and CI integration.

## Known limitations

- V1 has not yet been exercised against an external repository.
- Automatic semantic drift detection is intentionally conservative in V1.
- Runtime/live evidence handling is document-based; no evidence service exists.

## Current truth boundaries

`PROJECT_STATE.md` describes what is true now.
It must not become a chronological development diary.

Detailed historical reasoning belongs in ADRs, incidents, evidence, and Git history.
