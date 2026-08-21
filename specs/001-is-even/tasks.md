---
description: "Dependency-ordered task list for feature 001-is-even"
---

# Tasks: Dependency-free `is_even` helper

**Input**: Design documents from `/specs/001-is-even/`

**Prerequisites**: [plan.md](./plan.md) (required), [spec.md](./spec.md) (required for user stories)

**Tests**: Tests are REQUIRED. The constitution mandates test-first for
behaviour-changing source code, and FR-007 requires coverage of every acceptance
scenario in User Stories 1 and 2.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (US1, US2, US3)

## Path Conventions

Single project: `src/` and `tests/` at the repository root, per plan.md.

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: make the suite runnable and give the implementation branch live CI.

- [x] T001 [P] Create `pyproject.toml` at the repository root containing only a `[tool.pytest.ini_options]` table with `pythonpath = ["src"]` and `testpaths = ["tests"]`. Add no packaging metadata, no build backend and no dependency declarations.
- [x] T002 [P] Create `.github/workflows/tests.yml` that runs on `push` and `pull_request`, checks out the repository, sets up Python 3.11, installs only `pytest`, and runs `python -m pytest -q` from the repository root. Do not modify `.github/workflows/speckit-ledger.yml`.

**Checkpoint**: `python -m pytest -q` runs and reports no tests collected.

---

## Phase 2: User Story 1 - Determine integer parity (Priority: P1) 🎯 MVP

**Goal**: `is_even` returns correct parity for positive, negative, zero and very large integers.

**Independent Test**: call the helper with `4`, `7`, `0`, `-3`, `-8` and `10**30` and compare against mathematical parity.

### Tests for User Story 1

- [x] T003 [US1] Create `tests/test_is_even.py` importing `from is_even import is_even` and covering every US1 acceptance scenario: `4` is even, `7` is odd, `0` is even, `-3` is odd, `-8` is even, and `10**30` is even. Assert identity against `True` and `False` (`is True` / `is False`) so a truthy non-bool return fails. Run `python -m pytest -q` and capture the failing output as RED evidence before writing any production code.

### Implementation for User Story 1

- [x] T004 [US1] Create `src/is_even.py` defining `is_even(value: int) -> bool` that returns `value % 2 == 0`, with a module docstring and a function docstring stating the accepted domain. Import nothing. Make only the minimum change that turns the US1 tests green, then run `python -m pytest -q` and capture the passing output.

**Checkpoint**: US1 is independently usable and its tests pass.

---

## Phase 3: User Story 2 - Fail loudly on unsupported input (Priority: P2)

**Goal**: unsupported operand types raise `TypeError` naming the rejected type.

**Independent Test**: call the helper with `4.0`, `"4"`, `None`, `True` and `False` and confirm each raises `TypeError`.

### Tests for User Story 2

- [x] T005 [US2] Extend `tests/test_is_even.py` with cases asserting `TypeError` for `4.0`, `"4"`, `None`, `True` and `False`, and assert that the raised message contains the rejected type name (`float`, `str`, `NoneType`, `bool`). Run `python -m pytest -q` and capture the failing output as RED evidence before changing `src/is_even.py`.

### Implementation for User Story 2

- [x] T006 [US2] In `src/is_even.py`, guard the parity computation with `if isinstance(value, bool) or not isinstance(value, int): raise TypeError(...)`, where the message includes `type(value).__name__`. Reject `bool` explicitly because it is a subclass of `int`. Run `python -m pytest -q` and capture the passing output.

**Checkpoint**: the contract is explicit and both user stories pass together.

---

## Phase 4: User Story 3 - Discover usage from the README (Priority: P3)

**Goal**: the README shows copy-pasteable usage.

**Independent Test**: execute the README snippet verbatim and observe the documented results.

- [x] T007 [US3] Add a `## Usage` section to `README.md` with one fenced `python` block showing the import, an even call returning `True`, an odd call returning `False`, and the `TypeError` raised for a non-integer, plus the exact command used to run the tests. Keep it under twenty lines and do not restate the specification.

---

## Phase 5: Verification

- [x] T008 Run the full suite from the repository root with `python -m pytest -q`, confirm every test passes with no collection errors, and report the exact command, the summary line and the list of changed files.

---

## Dependencies

- T001 and T002 are independent of each other and of everything else; both must land before T008.
- T003 blocks T004 (test-first). T004 blocks T005.
- T005 blocks T006 (test-first). T006 blocks T007.
- T007 blocks T008.
