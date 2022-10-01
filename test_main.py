"""
    This is a test file for the main.py file.
"""
import pytest
import main

class TestInvalidPageParent:
    """
        This is used to ensure that the page error works.
    """
    def test___init__(self):
        """
        This tests that the __init__ method works.
        """
        with pytest.raises(main.InvalidPageParent):
            error = main.InvalidPageParent("Test")
            assert (
                main.InvalidPageParent("Test") is not None
            ), "Invalid Page Parent Error, failed to create instance."
            raise error
