"""
    This is a test file for the main.py file.
"""
import pytest
import main

def test_invalid_page_parent():
    """
        This tests the InvalidPageParent class.
    """
    with pytest.raises(main.InvalidPageParent):
        raise main.InvalidPageParent("Test")

def test_application_error():
    """
        This tests the ApplicationError class.
    """
    with pytest.raises(main.ApplicationError):
        raise main.ApplicationError("Test")
