"""Tests for the is_even helper."""

import pytest
from is_even import is_even


def test_is_even_positive_even():
    assert is_even(4) is True


def test_is_even_positive_odd():
    assert is_even(7) is False


def test_is_even_zero():
    assert is_even(0) is True


def test_is_even_negative_odd():
    assert is_even(-3) is False


def test_is_even_negative_even():
    assert is_even(-8) is True


def test_is_even_large_integer():
    assert is_even(10**30) is True


def test_is_even_large_odd_integer():
    assert is_even(10**30 + 1) is False


def test_is_even_large_negative_odd_integer():
    assert is_even(-(10**30 + 1)) is False


def test_is_even_rejects_float():
    with pytest.raises(TypeError) as excinfo:
        is_even(4.0)
    assert "float" in str(excinfo.value)


def test_is_even_rejects_str():
    with pytest.raises(TypeError) as excinfo:
        is_even("4")
    assert "str" in str(excinfo.value)


def test_is_even_rejects_none():
    with pytest.raises(TypeError) as excinfo:
        is_even(None)
    assert "NoneType" in str(excinfo.value)


def test_is_even_rejects_bool_true():
    with pytest.raises(TypeError) as excinfo:
        is_even(True)
    assert "bool" in str(excinfo.value)


def test_is_even_rejects_bool_false():
    with pytest.raises(TypeError) as excinfo:
        is_even(False)
    assert "bool" in str(excinfo.value)


class _ParitySpy:
    """Its __mod__ succeeds, so a missing guard yields a wrong answer, not an error."""

    def __mod__(self, other):
        return 0


def test_is_even_guard_runs_before_parity():
    with pytest.raises(TypeError) as excinfo:
        is_even(_ParitySpy())
    assert "_ParitySpy" in str(excinfo.value)
