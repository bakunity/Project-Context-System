# PCS Architecture

## 1. Goal

PCS is a context continuity subsystem for software repositories.

It separates ephemeral conversation context from durable, versioned project truth.

PCS is **Git-native and GitHub-first**, not GitHub-only. The core protocol lives in repository files and Git; GitHub provides an optional first-class operational adapter.

## 2. Core layers

```text
Chat / session / scratch
        |
        | ephemeral
        v
Agent bootstrap contract (AGENTS.md)
        |
        v
Machine index (.project/state.json)
        |
        v
Current truth (PROJECT_STATE + ACTIVE_WORK)
        |
        +--> Architecture / Roadmap
        +--> ADR decision memory
        +--> Incident failure memory
        +--> Evidence acceptance memory
        +--> Optional domain context/research
        |
        v
Git history + code + tests
```

## 3. GitHub operational adapter

```text
PCS Core / Git truth
        |
        +--> Issues      = bounded units of work
        +--> Project     = execution visibility
        +--> Pull Request= implementation review
        +--> Actions     = automated verification
        +--> Rulesets    = merge governance
        +--> CODEOWNERS  = review ownership
```

GitHub objects coordinate execution; they do not become duplicate truth stores.

## 4. Authoritative ownership

Each information category has exactly one primary owner:

- behavior contract -> `AGENTS.md`
- current project truth -> `PROJECT_STATE.md`
- current workstream -> `ACTIVE_WORK.md`
- system structure -> `ARCHITECTURE.md`
- future direction -> `ROADMAP.md`
- decision rationale -> `ADR/*`
- failure/root cause -> `INCIDENTS/*`
- accepted verification -> `EVIDENCE.md`
- bootstrap/freshness pointers -> `.project/state.json`
- chronology -> Git
- work item -> GitHub Issue when GitHub is used
- execution view -> GitHub Project when GitHub is used

README is user-facing documentation and is not authoritative project memory.

## 5. Bootstrap protocol

A fresh agent reads small/high-value context first and expands only when relevant.

The agent compares current HEAD with `state_based_on_commit`. A mismatch means potential context drift and triggers diff inspection before trusting the snapshot.

If an Issue/task brief exists, it is read after repository truth so task scope cannot silently redefine architecture.

## 6. Truth classification

PCS uses five states:

- CONFIRMED
- INFERRED
- UNKNOWN
- STALE
- CONFLICT

This prevents missing project-specific information from being silently invented.

## 7. Development/runtime boundary

Repository development and live runtime are separate acceptance layers.

Default lifecycle:

```text
repo -> Issue -> branch/task -> code -> tests/CI -> PR -> merge
```

Server/staging work begins only through an explicit runtime task:

```text
accepted implementation -> Live gate -> staging/server task -> smoke/live evidence -> production approval
```

This prevents an agent from treating credentials, deployment files, or server knowledge as implicit permission to mutate runtime systems.

## 8. Context lifecycle

Persistent context changes only on semantic state transitions, such as:

- architecture decision accepted;
- feature genuinely completed;
- root cause confirmed;
- acceptance status changed;
- active workstream changed;
- roadmap/release boundary changed.

## 9. Profiles

PCS supports progressive adoption:

- minimal — durable project truth and decisions;
- standard — execution, incidents, evidence, GitHub Issue/PR/CI integration;
- large — domain context and research archives.

## 10. Derived handoff

A session handoff is generated from current authoritative sources:

```text
PROJECT_STATE + ACTIVE_WORK + Git + recent evidence -> handoff
```

A permanent `HANDOFF.md` is avoided because it tends to duplicate and drift from current truth.

## 11. Global memory boundary

Cross-project/user/research memory may exist outside the repository.
It may point to a repository, but repository-specific architecture, decisions, incidents, and accepted state remain in Git.
