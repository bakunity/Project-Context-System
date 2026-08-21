# Active Work

## Current goal

Use PCS V1 in the next real product repository and prove the one-sentence installation workflow end to end.

## Branch / PR

Branch: `main`
PR: none

## Base / verified baseline

Context baseline: `1746d224ccfa80a719784f9c4ba652d21e3cde88`
V1 merged from PR #1.

## Accepted baseline

- PCS V1 is merged into `main`.
- Natural-language agent installation contract exists.
- Standard profile installs core context plus GitHub-first workflow files.
- Structural and readiness validation are separate.
- Regression tests protect installer overlays, existing-file safety, GitHub integration, CODEOWNERS rendering, and readiness behavior.
- Runtime/server access is forbidden by default during PCS installation.

## Current work

- Issue #2: first external installation in the next real product repository.
- Issue #3: V1.1 safe automation for GitHub Project and Ruleset setup.

## Current blocker

No PCS V1 code blocker.
External real-product smoke evidence is not yet recorded.

## Next safe action

In the next product repository, tell the AI only:

`Добавь в проект систему контекста https://github.com/bakunity/Project-Context-System`

Require the agent to follow `AGENT_INSTALL.md`, reach `PCS READY`, record exact evidence in Issue #2, and then continue product development. Keep server/runtime out of scope until a separate Live gate.

## Approval gate

No production/server mutation is implied by PCS installation.
Future release/governance changes should follow Issues -> branch -> PR -> CI unless explicitly approved otherwise.
