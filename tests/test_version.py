"""Test version information."""

import re

import pymeepo


def test_version() -> None:
    """Test that version is a valid semver string."""
    assert pymeepo.__version__, "Version should not be empty"
    assert re.match(
        r"^\d+\.\d+\.\d+", pymeepo.__version__
    ), "Version should be a valid semver string"
