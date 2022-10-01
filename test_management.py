"""
    This is a test file for the management file.
"""

# Import modules
import pytest
import management
from storage import Database


class TestUser:
    """
        This is used to test the User Class.
    """
    def test_username(self):
        """
            This tests the username property.
        """
        test_user = management.User("System", "root")

        # Tests that the username is the same as the assigned
        # username.

        assert (
            test_user.username == "System"
        ), """Username does not
         match expected result."""
        del test_user

    def test_logged_in(self):
        """
            This tests the logged_in property.
        """
        # This creates a database to test on.
        # which will not have any effect on the
        # real database.
        test_db = Database("loggedIn", delete_on_close=True)
        management.setup(test_db)

        # Creates a user instance which should be
        # logged out.

        test_user = management.User("testing", "account", 1)

        assert test_user.logged_in is False, "User should be logged out."
        del test_user

        # Creates a user instance which is logged in.

        logged_in_user = management.User("System", "root", login=True)
        assert (
            logged_in_user.logged_in is True
        ), """System Account should be
         logged in."""
        del logged_in_user
        del test_db

    def test_super_admin(self):
        """
            This tests the super_admin property.
        """
        # This creates a database to test on.
        # which will not have any effect on the
        # real database.
        test_db = Database("superAdmin", delete_on_close=True)
        management.setup(test_db)

        # This test is used to see if a user will
        # be set to super admin if they are not
        # logged in.

        test_user = management.User("System", "root")
        super_admin = test_user.super_admin

        assert (
            super_admin is False
        ), """Expected System to not be a super
         admin till the user is logged in."""

        del test_user

        # This tests if a super user will
        # be classed as a super user by the
        # method.

        test_user = management.User("System", "root", login=True)

        assert (
            test_user.super_admin is True
        ), """System is expected to be a
         super admin."""

        del test_user
        del test_db

    def test_admin(self):
        """
            This tests the admin property.
        """
        # This creates a database to test on.
        # which will not have any effect on the
        # real database.

        test_db = Database("admin", delete_on_close=True)
        management.setup(test_db)

        # This test is used to see if a user will
        # be set to admin if they are not
        # logged in.

        test_user = management.User("System", "root")
        super_admin = test_user.super_admin

        assert (
            super_admin is False
        ), """Expected System to not be a admin till
         the user is logged in."""

        del test_user

        # This tests if a admin user will
        # be classed as a admin user by the
        # method.

        test_user = management.User("System", "root", login=True)

        assert test_user.admin is True, "System is expected to be admin."

        del test_user
        del test_db


class TestUserManager:
    """
        This is used to test the UserManager Class.
    """
    def test_remove_user(self):
        """
            This tests the remove_user method.
        """
        # This creates a database to test on.
        # which will not have any effect on the
        # real database.

        test_db = Database("remove", delete_on_close=True)
        management.setup(test_db)

        admin_user = management.User("System", "root", login=True)
        guest_user = management.User("Guest", "root", login=True)

        result = management.UserManager.remove_user(admin_user, guest_user)
        assert result is True, "Failed to delete guest user."

        with pytest.raises(management.PermissionDenied):
            assert management.UserManager.remove_user(
                admin_user, admin_user
            ), "The admin should not be able to delete them selfs."

        del test_db


def test_us_date_to_uk():
    """
        This tests the us_date_to_uk method.
    """
    # This tests the function to verify that the result is the expected result.

    # Sets default month for test.
    month = "04"

    # Sets default year for test.
    year = "2020"

    # Creates a loop for the
    # days.

    for day in range(1, 30):
        # Converts the day to a string.
        day = str(day)

        # Creates a US Style date for
        # the function to convert.

        us_date = f"{year}/{month}/{day}"

        # Creates a UK Style date to assert against.

        uk_date = f"{day}/{month}/{year}"

        # Converts the US Style date to UK style date.

        converted_date = management.us_date_to_uk(us_date)

        # Checks if the date is correct.
        assert uk_date == converted_date, f"Expected: {converted_date}, result: {uk_date}"


def test__get_dates():
    """
        This tests the _get_dates method.
    """
    test_db = Database("admin", delete_on_close=True)
    management.setup(test_db)

    data = (1, "J", "J", "J", "0", "0", "0", "27/04/2022", "28/04/2022")
    with test_db as cur:
        cur.execute(
            """
                        INSERT INTO bookings(
                        ID,
                        first_name,
                        last_name,
                        mobile_number,
                        email_address,
                        postcode,
                        pets,
                        start_time,
                        end_time)
                        VALUES(
                            ?,
                            ?,
                            ?,
                            ?,
                            ?,
                            ?,
                            ?,
                            ?,
                            ?
                        )

                        """,
            data,
        )

    dates = management.get_dates()
    for i in dates.index:
        start_date = dates.loc[i, "start_date"]
        end_date = dates.loc[i, "end_date"]
        assert (
            start_date.strftime("%d/%m/%Y") == "27/04/2022"
        ), "The start date should be 27/04/2022"
        assert (
            end_date.strftime("%d/%m/%Y") == "27/04/2022"
        ), "The end date should be 27/04/2022"
    del test_db
