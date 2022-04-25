import pytest
from management import *
from storage import Database


class TestUser:

    def test_username(self):
        test_user = User("System", "root")

        # Tests that the username is the same as the assigned
        # username.

        assert test_user.username == "System", "Username does not match expected result."
        del test_user

    def test_logged_in(self):
        # This creates a database to test on.
        # which will not have any effect on the
        # real database.
        test_db = Database("loggedIn", delete_on_close=True)
        setup(test_db)

        # Creates a user instance which should be
        # logged out.

        test_user = User("testing", "account", permission_level=1)

        assert test_user.logged_in == False, "User should be logged out."
        del test_user

        # Creates a user instance which is logged in.

        logged_in_user = User("System", "root", login=True)
        assert logged_in_user.logged_in == True, "System Account should be logged in."
        del logged_in_user
        del test_db

    def test_super_admin(self):
        # This creates a database to test on.
        # which will not have any effect on the
        # real database.
        test_db = Database("superAdmin", delete_on_close=True)
        setup(test_db)

        # This test is used to see if a user will
        # be set to super admin if they are not 
        # logged in.

        test_user = User("System", "root")
        super_admin = test_user.super_admin

        assert super_admin == False, "Expected System to not be a super admin till the user is logged in."

        del test_user

        # This tests if a super user will 
        # be classed as a super user by the
        # method.

        test_user = User("System", "root", login=True)

        assert test_user.super_admin == True, "System is expected to be a super admin."

        del test_user
        del test_db

    def test_admin(self):
        # This creates a database to test on.
        # which will not have any effect on the
        # real database.

        test_db = Database("admin", delete_on_close=True)
        setup(test_db)

        # This test is used to see if a user will
        # be set to admin if they are not 
        # logged in.

        test_user = User("System", "root")
        super_admin = test_user.super_admin

        assert super_admin == False, "Expected System to not be a admin till the user is logged in."

        del test_user

        # This tests if a admin user will 
        # be classed as a admin user by the
        # method.

        test_user = User("System", "root", login=True)

        assert test_user.admin == True, "System is expected to be admin."

        del test_user
        del test_db


class TestUserManager:
    def test_remove_user(self):
        # This creates a database to test on.
        # which will not have any effect on the
        # real database.

        test_db = Database("remove", delete_on_close=True)
        setup(test_db)

        admin_user = User("System", "root", login=True)
        guest_user = User("Guest", "root", login=True)

        result = UserManager.remove_user(admin_user, guest_user)
        assert result == True, "Failed to delete guest user."

        with pytest.raises(PermissionDenied):
            assert UserManager.remove_user(admin_user, admin_user), "The admin should not be able to delete them selfs."

        del test_db


class TestFormattedTimeAndDate:
    def test_hour(self):
        # Checks every possible hour.
        for hour in range(0, 23):
            assert FormattedTimeAndDate(date="22/04/2022", hour=hour, min=0).hour == hour

    def test_minute(self):
        # Checks every possible minute.
        for minute in range(0, 60):
            assert FormattedTimeAndDate(date="22/04/2022", hour=0, min=minute).minute == minute

    def test___init__(self):
        # These tests make sure that the class
        # verifys the data provided.

        # This tests that the class works
        # with valid data.
        valid_data = FormattedTimeAndDate("22/04/2022", 16, 58)
        assert valid_data is not None, "The class should have accepted the data provided."

        # This tests the class can handle
        # no data being provided.

        with pytest.raises(IncorrectFormattedDateAndTime):
            assert FormattedTimeAndDate(hour=0, min=0)

            # This tests that the class does not
            # allow more than 60  in the
            # hour parameter.

        with pytest.raises(IncorrectFormattedDateAndTime):
            assert FormattedTimeAndDate("22/04/2022", 61,
                                        58), "The formatted time class accepted more than 60 in the hour parameter."

            # This tests that the class does not
            # allow less than 0 in the
            # hour parameter

        with pytest.raises(IncorrectFormattedDateAndTime):
            assert FormattedTimeAndDate("22/04/2022", -1,
                                        58), "The formatted time class accepted less than 0 in the hour parameter"

            # This tests that the class does not 
            # accept more than 60 in the minutes
            # parameter

        with pytest.raises(IncorrectFormattedDateAndTime):
            assert FormattedTimeAndDate("22/04/2022", 16,
                                        61), "The formatted time class accepted more than 60 in the minutes parameter."

            # This tests that the class does not
            # allow less than 0 in the
            # minutes parameter

        with pytest.raises(IncorrectFormattedDateAndTime):
            assert FormattedTimeAndDate("22/04/2022", 16,
                                        -1), "The formatted time class accepted less than 0 in the minutes parameter"

            # This tests that the class will
            # not accept a US style date.

        with pytest.raises(IncorrectFormattedDateAndTime):
            assert FormattedTimeAndDate("04/22/2022", 16, 58), "The formatted time class accepted a US style date."

class TestFormattedTimeAndDate:

  def test___init__(self):
    # This tests that the class will only accept valid parameters.
    pass