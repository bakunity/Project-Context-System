# PCS Agent Install Protocol

This document is the canonical entrypoint for an AI/coding agent when a user says something like:

> Добавь в проект систему контекста https://github.com/bakunity/Project-Context-System

The user should not have to manually copy PCS files or explain the setup procedure.

## Goal

Install PCS into the current project repository, reconstruct an initial truthful project context from repository evidence, validate that the context is actually ready, and report a concise completion result.

Default profile: `standard`.

PCS installation is repository/local/CI work only. It does **not** grant permission to connect to application servers, staging, production, cloud infrastructure, databases, or other live runtime systems.

## Agent contract

When the user asks to add PCS by repository URL, do the following without asking them to repeat PCS setup instructions.

### 1. Identify the target repository

Determine the current project root and Git repository.

Before changing anything:

- inspect existing repository instructions such as `AGENTS.md`, `CONTRIBUTING.md`, README, package manifests, CI, and existing docs;
- inspect `git status` and recent commits;
- preserve unrelated uncommitted user work;
- never overwrite existing project instructions blindly.

If the target is not a Git repository, initialize Git only when that is clearly consistent with the user's request. Do not commit secrets or local-only files.

### 2. Acquire PCS

Preferred shell workflow:

```bash
git clone --depth 1 https://github.com/bakunity/Project-Context-System.git <temporary-pcs-dir>
python <temporary-pcs-dir>/scripts/install_pcs.py <target-repo> --profile standard
```

If PCS is already available locally, reuse it instead of cloning another copy.

If only a GitHub/API file interface is available, use the repository templates and manifests as the source, preserve existing target files, and state clearly which local validation could not be executed.

### 3. Inspect the product before writing context

Read enough of the target repository to understand the actual product:

- source layout;
- entrypoints;
- package/dependency manifests;
- database/schema files;
- API/routes;
- frontend structure;
- tests;
- CI;
- existing deployment files;
- existing architecture/docs.

Do not infer project-specific facts merely from generic framework conventions.

Classify uncertain facts as:

- `CONFIRMED` — repository/runtime evidence exists;
- `INFERRED` — strongly implied by code but not authoritative;
- `UNKNOWN` — not found;
- `STALE` — documentation is older than relevant code;
- `CONFLICT` — sources disagree.

Never silently convert `INFERRED` or `UNKNOWN` to `CONFIRMED`.

### 4. Populate initial PCS truth

Replace bootstrap prompts with real project information in:

- `docs/PROJECT_STATE.md`;
- `docs/ARCHITECTURE.md`;
- `docs/ROADMAP.md`;
- `docs/ACTIVE_WORK.md` for the standard profile;
- `.project/state.json` status/pointers as appropriate.

Keep responsibilities separated:

- `PROJECT_STATE` = what is true now;
- `ACTIVE_WORK` = what is being done now;
- `ARCHITECTURE` = how the system is structured;
- `ROADMAP` = future direction;
- `ADR` = why durable decisions were made;
- `INCIDENTS` = failure/root-cause memory;
- `EVIDENCE` = accepted verification memory;
- Git = chronology.

Do not create fake ADRs, incidents, or evidence just to fill files.

### 5. Respect the runtime boundary

During PCS installation, do not:

- SSH to servers;
- deploy;
- mutate staging/production;
- access production databases;
- rotate credentials/certificates;
- run destructive live tests.

If runtime facts are not available from repository evidence, mark them `UNKNOWN` or record that live verification is deferred to a future `Live gate`.

### 6. Validate

First run structural validation:

```bash
python <target-repo>/scripts/validate_context.py <target-repo>
```

Then run readiness validation:

```bash
python <target-repo>/scripts/validate_context.py <target-repo> --ready
```

`--ready` must fail while bootstrap/template prompts remain or `.project/state.json` is still in `bootstrap` state.

The agent must **not** report PCS as ready until readiness validation passes, unless execution of the validator is impossible. In that case report `NOT VERIFIED`, not `READY`.

### 7. Review the diff

Before completion:

- inspect all changed files;
- confirm unrelated project files were not overwritten;
- confirm no secrets or private runtime data were written into PCS docs;
- confirm server/runtime was not touched;
- run relevant repository tests when the PCS change interacts with existing tooling.

### 8. Commit/push according to repository policy

PCS should live inside the product repository.

Respect the target repository's workflow:

- use the current allowed branch or create a bounded branch such as `chore/pcs-bootstrap`;
- create a commit for the initial PCS context baseline when commits are within scope;
- use PR workflow when required by repository policy;
- do not merge, deploy, or release without the required approval.

### 9. Completion report

When everything above is complete, report in this compact format:

```text
PCS READY
Profile: standard
Target: <repo>
Context: READY
Structural validation: PASS
Readiness validation: PASS
Runtime/server touched: NO
Changed: <short list>
Unknown / deferred: <short list or none>
Next safe action: <next product-development action>
```

If any required condition is missing, use:

```text
PCS NOT READY
Reason: ...
```

Do not use the word `READY` as a substitute for evidence.

## Expected user experience

After PCS is installed and committed into the product repository, the user can start a fresh AI session and simply ask to continue development.

A fresh agent should bootstrap from the product repository's `AGENTS.md`, `.project/state.json`, project state, architecture, active work, relevant ADR/context, Git state, and linked Issue/task before making changes.

The previous chat is optional convenience, not required project memory.
