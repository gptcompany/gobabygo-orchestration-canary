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
