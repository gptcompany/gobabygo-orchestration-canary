# Implementation Plan: Dependency-free `is_even` helper

**Branch**: `001-is-even` | **Date**: 2026-08-21 | **Spec**: [spec.md](./spec.md)

**Input**: Feature specification from `/specs/001-is-even/spec.md`

## Summary

Expose one pure function `is_even(value: int) -> bool` in a standard-library-only
module under `src/`, guarded by an explicit `int`-and-not-`bool` type check, and
cover every acceptance scenario with focused `pytest` tests under `tests/`. Add a
short README usage section and a CI workflow that runs the suite so merge can be
gated on green evidence. Parity is computed as `value % 2 == 0`, which is correct
for negative operands in Python because `%` returns a non-negative remainder for
a positive modulus; comparing against `0` rather than `1` avoids the classic
negative-operand bug.

## Technical Context

**Language/Version**: Python 3.11+ (CI pins 3.11; local workstation runs 3.14.4)

**Primary Dependencies**: none at runtime; `pytest` as a development-only runner

**Storage**: N/A

**Testing**: `pytest`, invoked as `python -m pytest` from the repository root

**Target Platform**: any CPython 3.11+ host; pure library code, no OS coupling

**Project Type**: single-project library

**Performance Goals**: N/A beyond exact results for arbitrarily large integers

**Constraints**: no third-party runtime imports, no I/O, no network, no logging

**Scale/Scope**: one function, one module, one test file, one README section

## Constitution Check

*GATE: evaluated before design and re-checked after task generation.*

| Principle | Status | Evidence |
| --- | --- | --- |
| I. Minimal Surface | PASS | One function, one module, one test file. Zero runtime dependencies. |
| II. Test-First | PASS | Tasks order the test file before the implementation and require observed RED output. |
| III. Explicit Contracts | PASS | FR-003/FR-004/FR-005 mandate a typed error naming the rejected type. |
| IV. Authoritative Git Ledger | PASS | `github-ledger.json` binding is committed in the planning PR; issues are published only by the pinned Action. |
| V. Independent Review | PASS | Writer and reviewer are separate sessions; CI green plus review PASS gate the merge. |

No complexity deviations are requested.

## Project Structure

### Documentation (this feature)

```text
specs/001-is-even/
├── spec.md               # Feature specification
├── plan.md               # This file
├── tasks.md              # Dependency-ordered work items
└── github-ledger.json    # Immutable repository/feature ledger binding
```

### Source Code (repository root)

```text
pyproject.toml            # pytest configuration only (pythonpath = ["src"])
src/
└── is_even.py            # The helper module
tests/
└── test_is_even.py       # Focused tests for every acceptance scenario
README.md                 # Usage section
.github/workflows/
├── speckit-ledger.yml    # Existing pinned ledger caller (unchanged)
└── tests.yml             # New CI workflow, added by the implementation branch
```

**Structure Decision**: A `src/` layout keeps the importable surface explicit and
prevents the repository root from shadowing standard-library names during test
collection. `pyproject.toml` carries only `[tool.pytest.ini_options]` with
`pythonpath = ["src"]`, which pytest supports natively, so no packaging metadata,
no `conftest.py` path hacks and no installation step are required.

## Design Decisions

**D-001 — Parity expression**: use `value % 2 == 0`. Rejected alternatives:
`value & 1 == 0` (correct but less readable, and identical in cost here) and
`divmod` (needless). Comparing to `0` rather than `1` is what makes negative
operands correct without a special case.

**D-002 — Reject `bool`**: `isinstance(True, int)` is `True` in Python, so a
plain `isinstance(value, int)` check would let `is_even(True)` return `False` and
`is_even(False)` return `True`. Those answers are meaningless. The guard is
`isinstance(value, bool) or not isinstance(value, int) -> TypeError`, checked
before the parity computation.

**D-003 — Error type and message**: `TypeError` (not `ValueError`) because the
defect is the operand's type. The message includes `type(value).__name__` to
satisfy FR-005.

**D-004 — Return a real `bool`**: `value % 2 == 0` already evaluates to `bool`,
so no `bool(...)` wrapper is needed; the test asserts identity against `True` and
`False` to prevent a future refactor from returning a truthy non-bool.

**D-005 — CI**: a single `tests.yml` workflow on `push` and `pull_request`,
running `python -m pytest -q` on Python 3.11 with `pip install pytest` and no
other install step. It is added by the implementation branch rather than by the
planning pull request: a test workflow merged before any test exists would make
`pytest` exit with code 5 ("no tests collected") and report a misleading red run
on `main`. Workflows introduced on a same-repository pull-request branch do run
for that pull request, so the implementation pull request is still gated by real
CI evidence.

## Milestones and Dependency Ordering

1. **M1 — Planning merged** (this PR): spec, plan, tasks and the ledger binding
   land on `main`; the pinned Action publishes the derived issues.
2. **M2 — RED**: the test file exists and fails because `src/is_even.py` does not
   yet exist. Failure output is captured as evidence.
3. **M3 — GREEN**: the module is added; the focused suite passes locally and in
   CI on the implementation branch.
4. **M4 — Documentation**: README usage section added; suite still green.
5. **M5 — Review and merge**: independent read-only review over the frozen commit
   range returns PASS, CI is green, the implementation PR is merged.
6. **M6 — Reconciliation**: `tasks.md` checkboxes are marked on `main`; the
   ledger Action closes the derived issues.

M2 blocks M3 (test-first). M3 blocks M4 and M5. M5 blocks M6.

## Risk Controls

- **R-001 — Silent wrong answer for `bool`**: mitigated by D-002 plus a dedicated
  test asserting `TypeError` for both `True` and `False`.
- **R-002 — Negative-operand bug**: mitigated by D-001 plus tests for `-3` and
  `-8`.
- **R-003 — Import path breaks in CI but not locally**: mitigated by running the
  suite in CI on the implementation branch before merge, on a clean checkout.
- **R-004 — Writer self-review**: mitigated by delegating review to a different
  session with a read-only brief over an immutable commit range.
- **R-005 — Ledger drift**: mitigated by never mutating issues locally and by
  requiring `mesh speckit github check` to report aligned before delegating.

## Rollback Considerations

Every artefact is additive: `src/is_even.py`, `tests/test_is_even.py`,
`pyproject.toml`, `.github/workflows/tests.yml` and a README section. Rollback is
a revert of the implementation merge commit; nothing else in the repository
depends on the helper, so revert cannot break another consumer. The planning
commit can be reverted independently, at the cost of leaving already-published
issues open until `tasks.md` is restored.
