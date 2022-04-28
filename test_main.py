import main
from storage import Database
from management import setup
import pytest

class TestInvalidPageParent:
  def test___init__(self):
    with pytest.raises(main.InvalidPageParent):
        error = main.InvalidPageParent("Test")
        assert main.InvalidPageParent("Test") is not None, "Invalid Page Parent Error, failed to create instance."
        raise error

