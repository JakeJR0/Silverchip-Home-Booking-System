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

class TestApplication:

  def test_app_size(self):
    test_db = Database("mainTest", delete_on_close=True)
    setup(test_db)
    app_in_test = main.Application(True)

    for i in range(0, 20000):
      if i > 20 and i < 10000:
        app_in_test.app_size = (i, i)
        assert app_in_test.app_size == (i, i), "App size not set at expected."
      else:
        with pytest.raises(main.ApplicationError):
          app_in_test.app_size = (i, i)
          
    with pytest.raises(main.ApplicationError):
      app_in_test.app_size = ("Size", "Size")

    with pytest.raises(main.ApplicationError):
      app_in_test.app_size = ()
    del test_db
          
  def test_app_size_x(self):
    test_db = Database("mainTest", delete_on_close=True)
    setup(test_db)
    app_in_test = main.Application(True)

    for i in range(0, 30):
      if i > 20 and i < 10000:
        app_in_test.app_size_x = i
        assert app_in_test.app_size_x[0] == i, "App size not set at expected."
      else:
        with pytest.raises(main.ApplicationError):
          app_in_test.app_size_x = i
          assert app_in_test.app_size_x[0] != i, "Application should not have set size."
    with pytest.raises(TypeError):
      app_in_test.app_size_x = "Size"
    del test_db

  def test_app_size_y(self):
    test_db = Database("mainTest", delete_on_close=True)
    setup(test_db)
    app_in_test = main.Application(True)

    for i in range(0, 30):
      if i > 20 and i < 10000:
        app_in_test.app_size_y = i
      else:
        with pytest.raises(main.ApplicationError):
          app_in_test.app_size_y = i


    with pytest.raises(TypeError):
      app_in_test.app_size_y = "Size"
    
    del test_db
          