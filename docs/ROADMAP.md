# Roadmap

## Now — V1 Foundation

- Canonical PCS repository structure.
- `AGENTS.md` behavior contract.
- `.project/state.json` bootstrap/freshness index.
- Project state, active work, architecture, roadmap, ADR, incident, evidence templates.
- Minimal / standard / large installation profiles.
- Cross-platform Python installer.
- Local validator.
- GitHub Actions context check.
- PR template for evidence-based acceptance.

## Next — V1.1 Hardening

- JSON Schema validation for `.project/state.json`.
- Stronger Git freshness checks.
- Context drift diagnostics.
- Secret-pattern scanning for context files.
- Broken internal-link checks.
- ADR and incident schema/lint rules.
- Installer update mode for existing PCS installations.

## Later — V2

- `pcs init`, `pcs validate`, `pcs status`, `pcs handoff` CLI.
- Automatic session checkpoint/handoff generation.
- Repository context graph for large monorepos.
- Multi-agent task registry and ownership boundaries.
- Evidence scenario IDs with immutable commit/environment references.
- Reusable GitHub Action published from this repository.

## Explicitly deferred

- Storing raw chat transcripts as canonical memory.
- Repository-local generic `memories/` folder.
- Automatic mutation of project truth without review.
- Central hosted service requirement; PCS should remain useful as plain Git files.
