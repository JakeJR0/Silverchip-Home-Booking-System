import pytest
from storage import *


class TestDatabase:
    def test___init__(self):

        # These test the data validation
        # that is applied to the name of
        # the database.

        # This test checks if the class will
        # raise an error if the name is over
        # 20 characters.

        with pytest.raises(DatabaseNamingError):
            assert Database(db_name="i" * 21, test_mode=True)

            # This test checks if the database will
            # raise an error if the name is empty.

        with pytest.raises(DatabaseNamingError):
            assert Database(db_name="", test_mode=True)

            # This tests if the class will raise an
            # error if the name is 3 characters or
            # less.

        with pytest.raises(DatabaseNamingError):
            assert Database(db_name="tes", test_mode=True)

            # This tests if the database raise an error
            # if just restriced characters have been entered
            # into the name.

        with pytest.raises(DatabaseNamingError):
            assert Database(db_name="____", test_mode=True)

            # This tests if the database will raise an error
            # if the name includes any mix of both allowed and
            # restricted characters

        with pytest.raises(DatabaseNamingError):
            assert Database(db_name="Test_Database", test_mode=True)

        # These test makes sure the database was correctly setup.

        # This test makes sure the System user was added with level 3 access.

        setup_test_db = Database(db_name="test", delete_on_close=True)
        found = False

        for row in setup_test_db.con.execute(
            "SELECT level FROM users WHERE username='System'"
        ):
            assert (
                row[0] == 3
            ), "System User level is not at level 3 instead it is at level {}.".format(
                str(row[0])
            )
            found = True

        assert found == True, "System User was not found within the database."

        # This test checks if the database is able to save
        # changes.

        setup_test_db.con.execute(
            """
                              INSERT INTO users(username, password, level)
                              VALUES(?, ?, ?)
                              """,
            ("test_user", "test", 1),
        )

        saved = setup_test_db.save()

        assert saved == True, "Failed to add a new row into the users table."

        # This test checks to verify the correct
        # prices have been assigned to the prices.

        for row in setup_test_db.con.execute("SELECT month, price FROM holiday_prices"):
            correct_price = month_prices[row[0]]
            assert row[1] == correct_price, "Incorrect Month Price set in the database."

        del setup_test_db
