# Evidence Ledger

This file records acceptance evidence for scenarios where `code review` or `CI PASS` alone is not enough.

It is especially useful for infrastructure, deployment, OS integration, external services, migrations, and expensive/destructive live tests.

## Rule

Do not repeat an already accepted live scenario without a concrete regression reason.

## Scenario template

```md
## SCENARIO-ID — Name

Status: PASS | FAIL | PARTIAL | NOT_RUN
Commit: <immutable SHA>
Environment: <environment/device/runtime>
Date: YYYY-MM-DD

### Verification

Exact commands/actions performed.

### Evidence

Logs, artifacts, checks, screenshots, hashes, or external observations.

### Limitations

What was not covered.

### Regression reason

If repeated, why the previous evidence was no longer sufficient.
```

## Current scenarios

No external PCS installation scenario has been accepted yet.
