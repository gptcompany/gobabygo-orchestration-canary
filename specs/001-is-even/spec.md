# Feature Specification: Dependency-free `is_even` helper

**Feature Branch**: `001-is-even`

**Created**: 2026-08-21

**Status**: Ready for planning

**Input**: User description: "Add dependency-free Python is_even helper with focused tests and README usage"

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Determine integer parity (Priority: P1)

A developer working inside this repository imports a single helper and asks
whether an integer is even, without adding any third-party dependency and
without writing their own modulo expression each time.

**Why this priority**: This is the entire value of the feature. Without it there
is nothing to test, document or review.

**Independent Test**: Import the helper in a Python session or test file, call
it with a set of integers, and confirm the returned booleans match mathematical
parity. Delivers value on its own with no other story implemented.

**Acceptance Scenarios**:

1. **Given** the integer `4`, **When** `is_even(4)` is called, **Then** it returns `True`.
2. **Given** the integer `7`, **When** `is_even(7)` is called, **Then** it returns `False`.
3. **Given** the integer `0`, **When** `is_even(0)` is called, **Then** it returns `True`.
4. **Given** the integer `-3`, **When** `is_even(-3)` is called, **Then** it returns `False`.
5. **Given** the integer `-8`, **When** `is_even(-8)` is called, **Then** it returns `True`.
6. **Given** an arbitrarily large integer such as `10**30`, **When** `is_even(10**30)` is called, **Then** it returns `True` without overflow or precision loss.

---

### User Story 2 - Fail loudly on unsupported input (Priority: P2)

A developer accidentally passes a value that is not an integer. Instead of a
silently wrong answer, they get an immediate, explicit error naming the problem.

**Why this priority**: Parity of a non-integer is undefined. Silent coercion
would produce confidently wrong results, which the constitution forbids. It is
P2 because the happy path already delivers the MVP.

**Independent Test**: Call the helper with a float, a string, `None` and a
boolean, and confirm each call raises `TypeError` rather than returning a value.

**Acceptance Scenarios**:

1. **Given** the float `4.0`, **When** `is_even(4.0)` is called, **Then** `TypeError` is raised.
2. **Given** the string `"4"`, **When** `is_even("4")` is called, **Then** `TypeError` is raised.
3. **Given** `None`, **When** `is_even(None)` is called, **Then** `TypeError` is raised.
4. **Given** the boolean `True`, **When** `is_even(True)` is called, **Then** `TypeError` is raised, even though `bool` is a subclass of `int` in Python.

---

### User Story 3 - Discover usage from the README (Priority: P3)

A newcomer opening the repository README finds a short, copy-pasteable usage
block showing the import path, a couple of calls and the error behaviour.

**Why this priority**: Documentation makes the feature discoverable but the code
is usable without it.

**Independent Test**: Read `README.md` and reproduce the shown snippet verbatim
in a Python session; the observed output matches what the README states.

**Acceptance Scenarios**:

1. **Given** the repository README, **When** a reader looks for usage, **Then** a fenced Python block shows the import and at least one `True` result, one `False` result and the `TypeError` behaviour.
2. **Given** the README snippet, **When** it is executed as written, **Then** it runs without modification.

---

### Edge Cases

- Zero is even; the sign of the operand must not affect the result.
- Negative odd integers must return `False` (Python's `%` on negatives returns a
  non-negative remainder, so the implementation must not rely on `== 1`).
- `bool` is a subclass of `int`; `True` and `False` must still be rejected.
- Arbitrarily large integers must be handled exactly, with no float conversion.
- Integer-like objects that are not `int` (for example `decimal.Decimal(4)` or a
  NumPy integer, were NumPy present) are rejected; only exact `int` is accepted.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The system MUST expose a callable `is_even(value: int) -> bool`.
- **FR-002**: `is_even` MUST return `True` when `value` is an even integer and `False` when `value` is an odd integer, for positive, negative and zero operands.
- **FR-003**: `is_even` MUST raise `TypeError` when `value` is not an instance of `int`.
- **FR-004**: `is_even` MUST raise `TypeError` when `value` is a `bool`, despite `bool` being a subclass of `int`.
- **FR-005**: The `TypeError` message MUST name the rejected type so the caller can diagnose the mistake without a debugger.
- **FR-006**: The implementation MUST import nothing outside the Python standard library, and MUST NOT perform I/O, network access or logging.
- **FR-007**: The repository MUST contain focused automated tests covering every acceptance scenario in User Stories 1 and 2.
- **FR-008**: `README.md` MUST contain a usage section satisfying User Story 3.
- **FR-009**: The test suite MUST be runnable from the repository root with a single documented command.

### Key Entities

Not applicable: the feature introduces no persistent data or entities.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: 100% of the acceptance scenarios in User Stories 1 and 2 are covered by an executing automated test, and the full suite passes.
- **SC-002**: Running the documented test command from a clean checkout succeeds with zero collection errors and zero failures.
- **SC-003**: The runtime module declares zero third-party imports, verifiable by reading its import block.
- **SC-004**: A reader can copy the README usage block into a Python session and reproduce the documented results without editing it.
- **SC-005**: Continuous integration reports a green run for the implementation branch before merge.

## Assumptions

- Python 3.11 or newer is available; the repository targets the interpreter used
  by CI (`3.11`) and the local workstation (`3.14`).
- `pytest` is available as a development-only tool and is not a runtime
  dependency of the shipped module.
- Exact `int` is the only accepted input type; broadening to other numeric
  protocols is explicitly deferred.
- The helper is imported as a library; no CLI entry point is required.

## Out of Scope

- Any `is_odd` counterpart, parity of non-integer numeric types, or vectorised
  parity over collections.
- Packaging and publishing to an index, versioning policy, or a public API
  stability guarantee.
- Performance optimisation: correctness at any input magnitude is the only
  performance-relevant requirement.
- Type-checker configuration, linting rules, or formatting enforcement.
