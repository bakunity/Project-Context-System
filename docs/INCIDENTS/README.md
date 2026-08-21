# Incidents

Incidents store significant failure/root-cause memory.

A bug is worth an incident record when forgetting it could cause repeated investigation, regression, destructive retesting, or architecture mistakes.

## Naming

`INC-YYYY-NNN-short-name.md`

## Required fields

```md
# INC-YYYY-NNN — Title

Status:
Detected:
Affected versions/commits:

## Symptom
## Impact
## Root cause
## False leads
## Fix
## Evidence
## Regression test
## New invariant
## Follow-up
```

`False leads` is intentional: a later agent should not restart already disproven investigations without new evidence.

An incident should produce regression protection or a new invariant when practical.
