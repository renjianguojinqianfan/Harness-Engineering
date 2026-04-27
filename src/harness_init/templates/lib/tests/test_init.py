"""Tests for {package_name}."""

from {package_name} import hello


def test_hello_default() -> None:
    """hello should return greeting with default name."""
    assert hello() == "Hello, World!"


def test_hello_with_name() -> None:
    """hello should return greeting with provided name."""
    assert hello("Alice") == "Hello, Alice!"
