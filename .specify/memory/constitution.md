# Gobabygo Orchestration Canary Constitution

## Core Principles

### I. Minimal Surface (NON-NEGOTIABLE)
This repository is a disposable end-to-end canary for the Gobabygo development
orchestration flow. Every feature stays as small as it can be while still
exercising the full pipeline: spec, plan, tasks, ledger, delegated
implementation, independent review, CI, merge, reconciliation. No feature may
introduce a runtime third-party dependency.

### II. Test-First (NON-NEGOTIABLE)
Behaviour-changing source code requires a focused automated test that is
observed failing (RED) before the production edit, then the minimum change that
makes it pass (GREEN), then refactoring only while green. Tests use the Python
standard library plus pytest as the runner. No mocks are used where the real
value is directly observable.

### III. Explicit Contracts
Every public function documents its accepted input domain and its failure mode.
Silent coercion of unsupported types is forbidden; unsupported input raises a
typed error.

### IV. Authoritative Git Ledger
`spec.md`, `plan.md` and `tasks.md` under `specs/` are authoritative. GitHub
Issues are a one-way derived work ledger published only by the pinned
`speckit-ledger` GitHub Action. No local process and no worker prompt may mutate
issues directly.

### V. Independent Review
The author of a change never reviews it. Review runs read-only against an
immutable commit range and must end with an explicit verdict. CI evidence is
required in addition to human-or-agent review before merge.

## Additional Constraints

- Language: Python 3.11+ standard library only for runtime code.
- Runtime dependencies: none. Development dependencies: pytest only.
- No production services, no secrets, no network access from library code.

## Development Workflow

1. Specification, plan and tasks are committed before implementation.
2. A planning-only pull request is merged first; the ledger Action publishes the
   derived issues from `main`.
3. Implementation happens on a dedicated branch, delegated to a single writer.
4. An independent reviewer inspects the frozen commit range read-only.
5. Merge requires review PASS and green CI.
6. `tasks.md` checkboxes are updated on `main` afterwards so the Action closes
   the derived issues.

## Governance

This constitution supersedes ad-hoc practice inside this repository. Amendments
require a commit that states the rationale. Any complexity beyond the minimum
required to exercise the orchestration flow must be justified in `plan.md`.

**Version**: 1.0.0 | **Ratified**: 2026-08-21 | **Last Amended**: 2026-08-21
