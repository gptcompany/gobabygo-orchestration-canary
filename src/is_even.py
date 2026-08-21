"""Dependency-free integer parity helper module."""


def is_even(value: int) -> bool:
    """Return True if value is an even integer, False if odd.

    Accepted domain: integer (int) values.
    """
    return value % 2 == 0
