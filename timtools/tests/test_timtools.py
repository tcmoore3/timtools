"""
Unit and regression test for the timtools package.
"""

# Import package, test suite, and other packages as needed
import timtools
import pytest
import sys

def test_timtools_imported():
    """Sample test, will always pass so long as import statement worked"""
    assert "timtools" in sys.modules
