# Active Work

## Current goal

Finish PCS V1 as a reusable Git-native, GitHub-first context layer that can be installed directly into the next product repository before server/runtime work begins.

## Branch / PR

Branch: `feat/pcs-v1-foundation`
PR: `#1`

## Base / verified commit

Context baseline: `50912e530a21e722ce3eff1b94410ae3c8fe84b1`
Last verified commit: `50912e530a21e722ce3eff1b94410ae3c8fe84b1`

## Accepted baseline

- Core PCS document model exists.
- Minimal / standard / large profile overlays work in automated tests.
- Files that existed before installation are protected unless `--force` is used.
- Structural validator passes.
- GitHub Actions installer test suite passes.
- Standard profile installs GitHub Issue Forms, CODEOWNERS, PR/CI workflow, GitHub manifests, integration docs, and `setup_github.py`.
- Installer renders CODEOWNERS from GitHub `origin` when available.
- Agent rules default to repository/local/CI development and prohibit implicit server/runtime mutation.

## Current work

- Review PR #1 as the V1 release candidate.
- Use the next new product repository as the first real installation smoke target.
- Keep Project/Ruleset application explicit until their automation is separately designed and accepted.

## Current blocker

No code blocker. External real-repository installation is still not verified.

## Next safe action

When the new product repository is created, install PCS `standard` into it, fill initial truth, validate, commit the baseline, push to GitHub, and begin development through Issues -> branch/task -> PR -> CI. Do not connect the server until an explicit Live gate task exists.

## Tests already accepted

For commit `50912e530a21e722ce3eff1b94410ae3c8fe84b1`:

- context validator PASS;
- minimal installer PASS;
- standard installer + validator PASS;
- large installer PASS;
- existing-file protection PASS;
- GitHub integration files installed by standard profile PASS;
- CODEOWNERS owner rendering PASS.

Do not repeat these exact CI scenarios without a concrete regression reason after an unchanged implementation.

## Approval gate

PR remains draft. Merge of V1 foundation requires explicit review/approval.
