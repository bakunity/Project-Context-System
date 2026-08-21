# Evidence Ledger

This file records acceptance evidence for scenarios where `code review` or `CI PASS` alone is not enough, and also anchors important automated verification to immutable commits.

## Rule

Do not repeat an already accepted scenario without a concrete regression reason when the relevant implementation has not changed.

## PCS-V1-CI-001 — Foundation structure and installer profiles

Status: PASS
Commit: `d2aa8e0f7ad4f44f1dbc1c112e295ff77a37d9d8`
Environment: GitHub Actions / Ubuntu 24.04 / Python 3.12
Date: 2026-08-21
Workflow run: `PCS Context Check #3`

### Verification

- `python scripts/validate_context.py .`
- `python -m unittest discover -s tests -v`

Automated scenarios:

1. minimal profile installs required core files;
2. standard profile installs active work, incidents, evidence, validator and workflow;
3. standard installation passes PCS validator;
4. large profile installs subsystem context and research archive;
5. pre-existing project files are not overwritten without `--force`.

### Evidence

GitHub Actions job `validate-context` completed successfully for the immutable commit above.
Both workflow steps `Validate PCS context` and `Test installer profiles` completed with `success`.

### Limitations

- This is an automated temporary Git repository test, not an external real-project smoke test.
- Windows execution is not separately tested; installer logic is Python/pathlib based and intended to be cross-platform.
- `--force` replacement behavior is not a migration engine and has not received dedicated migration tests.

### Regression reason

Not applicable. First accepted automated baseline.

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
