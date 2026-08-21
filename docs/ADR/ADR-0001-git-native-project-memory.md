# ADR-0001 — Git-native project memory

Status: Accepted
Date: 2026-08-21

## Context

Long-running AI-assisted projects lose important state when work moves between chat sessions, devices, agents, pull requests, and runtime verification.

Raw conversation history is large, noisy, non-versioned from the repository perspective, and often unavailable to a fresh coding agent.

## Decision

PCS stores repository-specific durable context in the same Git repository as the code.

Chat/session memory is treated as ephemeral workspace.

Cross-project memory may reference the repository, but it must not duplicate repository-specific truth.

## Options considered

1. Keep project truth in chat history.
2. Maintain one large exported context document.
3. Maintain a repository-local generic `memories/` directory.
4. Maintain scoped, versioned truth documents in Git.

## Why

Git provides immutable commits, diffs, timestamps, branches, pull requests, rollback, authorship, and a direct relationship between context and code versions.

Scoped truth documents reduce noise and context drift compared with one large memory dump.

## Consequences

- Context changes become reviewable engineering changes.
- Agents can bootstrap without previous chat history.
- Documentation freshness becomes an engineering concern.
- Duplicate truth files must be avoided.
- CI can validate part of the context contract.

## Evidence

The PCS design is derived from prior project experience where durable state, evidence, exact SHA references, bounded task briefs, and Git-based context significantly reduced repeated investigation and lost context.

## Supersedes

None.

## Superseded by

None.
