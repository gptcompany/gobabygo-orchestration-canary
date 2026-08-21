"""Dependency-free integer parity helper module."""


def is_even(value: int) -> bool:
    """Return True if value is an even integer, False if odd.

    Accepted domain: integer (int) values. Raises TypeError for non-int or bool.
    """
    if isinstance(value, bool) or not isinstance(value, int):
        raise TypeError(f"Expected int, got {type(value).__name__}")
    return value % 2 == 0
