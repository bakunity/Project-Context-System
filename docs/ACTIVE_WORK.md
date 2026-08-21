# Active Work

## Current goal

Finish PCS V1 as a reusable Git-native, GitHub-first context layer that can be added to a new product by giving an AI only the PCS repository URL, before server/runtime work begins.

## Branch / PR

Branch: `feat/pcs-v1-foundation`
PR: `#1`

## Base / verified commit

Context baseline: `b87c63ae20ed70b6834c6f0fd65494521dfcd4e3`
Last verified commit: `b87c63ae20ed70b6834c6f0fd65494521dfcd4e3`

## Accepted baseline

- Core PCS document model exists.
- Minimal / standard / large profile overlays work in automated tests.
- Existing project files are protected unless `--force` is used.
- GitHub-first operational layer is installed by the standard profile.
- Agent rules default to repository/local/CI development and prohibit implicit server/runtime mutation.
- `AGENT_INSTALL.md` defines natural-language installation behavior.
- `pcs-manifest.json` exposes the agent entrypoint and default profile.
- Structural installation and contextual readiness are separate states.
- `validate_context.py --ready` rejects untouched bootstrap context and passes after evidence-backed context is populated.

## Current work

- Review PR #1 as the V1 release candidate.
- Use the next new product repository as the first real external installation target.
- Keep Project/Ruleset application explicit until V1.1 automation is separately accepted.

## Current blocker

No code blocker. External real-product installation is still not verified.

## Next safe action

In the next product repository, give the AI the PCS repository URL only, let it follow `AGENT_INSTALL.md`, require `PCS READY`, record exact product commit/evidence in Issue #2, and continue product development without server access until a separate Live gate.

## Tests already accepted

For commit `b87c63ae20ed70b6834c6f0fd65494521dfcd4e3`:

- context validator PASS;
- minimal installer PASS;
- standard installer + validator PASS;
- large installer PASS;
- existing-file protection PASS;
- GitHub integration assertions PASS;
- CODEOWNERS owner rendering PASS;
- untouched bootstrap `--ready` FAIL as designed;
- populated context `--ready` PASS.

Do not repeat these exact CI scenarios without a concrete regression reason after unchanged implementation.

## Approval gate

PR remains draft. Merge/tag of V1 requires explicit review/approval and preferably the external smoke evidence from Issue #2.
