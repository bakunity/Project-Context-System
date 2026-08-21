# PCS Architecture

## 1. Goal

PCS is a context continuity subsystem for software repositories.

It separates ephemeral conversation context from durable, versioned project truth.

## 2. Layers

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

## 3. Authoritative ownership

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

README is user-facing documentation and is not authoritative project memory.

## 4. Bootstrap protocol

A fresh agent reads small/high-value context first and expands only when relevant.

The agent compares current HEAD with `state_based_on_commit`. A mismatch means potential context drift and triggers diff inspection before trusting the snapshot.

## 5. Truth classification

PCS uses five states:

- CONFIRMED
- INFERRED
- UNKNOWN
- STALE
- CONFLICT

This prevents missing project-specific information from being silently invented.

## 6. Context lifecycle

Persistent context changes only on semantic state transitions, such as:

- architecture decision accepted;
- feature genuinely completed;
- root cause confirmed;
- acceptance status changed;
- active workstream changed;
- roadmap/release boundary changed.

## 7. Profiles

PCS supports progressive adoption:

- minimal — durable project truth and decisions;
- standard — execution, incidents, evidence, PR/CI workflow;
- large — domain context and research archives.

## 8. Derived handoff

A session handoff is generated from current authoritative sources:

```text
PROJECT_STATE + ACTIVE_WORK + Git + recent evidence -> handoff
```

A permanent `HANDOFF.md` is avoided because it tends to duplicate and drift from current truth.

## 9. Global memory boundary

Cross-project/user/research memory may exist outside the repository.
It may point to a repository, but repository-specific architecture, decisions, incidents, and accepted state remain in Git.
