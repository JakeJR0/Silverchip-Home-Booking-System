"""
    Management system for the booking system
"""

# Import modules
from datetime import datetime, timedelta
import pandas as pd
import storage
from management_formatters import us_date_to_uk, FormattedTimeAndDate
from management_formatters import FormattedUserBookingData
from management_exceptions import IncorrectFormattedDateAndTime, BookingError
from management_exceptions import BookingSaveError, FailedToLoginToUser
from management_exceptions import PermissionDeniedToCreateAccount, PermissionDenied
from management_exceptions import InvalidAccountLevel, FailedToMakeUserInstance
from management_exceptions import PasswordValidationError

DATABASE = storage.Database()
GUEST_LEVEL = 1
ADMIN_LEVEL = 2
SUPER_ADMIN_LEVEL = 3
class Booking:
    """
    Used to both view and create
    bookings within the application,
    this class is used to make it easier
    to integrate with the database and the
    application.
    """

    def _get_booking_id(self):
        """
            This is used to get the booking id.
        """
        start_id = 100000
        rows = None
        with DATABASE as cur:
            rows = cur.execute('''
                SELECT MAX(ID) + 1 AS new_id
                FROM Bookings
            ''')

            for row in rows:
                print(row)
                if row[0] is not None:
                    start_id = row[0]

        return start_id

    @property
    def start(self):
        """
            This is used to get the start date.
        """
        return self._start_date

    def get_instance_dates(self):
        """
            This is used to get the instance dates.
        """
        return [self._start_date, self._end_date]

    @start.setter
    def start(self, value=FormattedTimeAndDate):
        """
            This is used to set the start date.
        """
        if self._valid_start_and_end(value, self._end_date):
            self._start_date = value

    @property
    def end(self):
        """
            This is used to get the end date.
        """
        return self._end_date

    @end.setter
    def end(self, value=FormattedTimeAndDate):
        """
            This is used to set the end date.
        """
        if self._valid_start_and_end(self._start_date, value):
            self._end_date = value

    @property
    def user(self):
        """
            This is used to get the user.
        """
        return self._user_data

    @property
    def cost(self):
        """
            This is used to get the cost.
        """
        total_cost = 0
        date_format = "%d/%m/%Y"
        start = self._start_date.date.strftime(date_format)
        end = self._end_date.date.strftime(date_format)
        date_range = pd.date_range(start=start, end=end, freq="1d")

        month_prices = {}
        rows = None
        with DATABASE as cur:
            rows = cur.execute('''
                SELECT month, price
                FROM holiday_prices
            ''')

            for row in rows:
                month_prices[row[0]] = row[1]
        print(month_prices)
        for date in date_range.date:
            date = us_date_to_uk(str(date))
            month = int(date[3:5])
            print("Month", month)
            price = month_prices[month]
            print(month, price)
            total_cost += price

        pet_cost = float(int(self._user_data.pets) * 25)
        total_cost += pet_cost

        return total_cost

    def _valid_start_and_end(
        self, start=FormattedTimeAndDate, end=FormattedTimeAndDate
    ):
        print("Start", start)
        print("End", end)
        return True

    def _remove_item(self, item=None):
        try:
            del item
        except AttributeError:
            pass

    def save(self):
        """
            This is used to save the booking.
        """
        bid = self._booking_id
        first_name = str(self._user_data.first_name)
        last_name = str(self._user_data.last_name)
        phone_number = str(self._user_data.phone_number)
        email = str(self._user_data.email)
        postcode = str(self._user_data.postcode)
        pets = int(self._user_data.pets)
        start = self.start.date
        end = self.end.date
        start = str(start).replace("-", "/")
        end = str(end).replace("-", "/")
        start = f"{start} {self.start.hour}:{self.start.minute}"
        end = f"{end} {self.end.hour}:{self.end.minute}"
        start = us_date_to_uk(start)
        end = us_date_to_uk(end)

        try:
            data = (
                first_name,
                last_name,
                phone_number,
                email,
                postcode,
                pets,
                start,
                end,
                bid,
            )
            print(bid, data)
            with DATABASE as cur:
                cur.execute('''
                    UPDATE bookings
                    SET
                        first_name=?,
                        last_name=?,
                        mobile_number=?,
                        email_address=?,
                        postcode=?,
                        pets=?,
                        start_time=?,
                        end_time=?
                    WHERE
                        ID=?
                ''', data)
            return True
        except Exception as error:
            raise BookingSaveError(error) from error

    def delete(self):
        """
            This is used to delete the booking.
        """
        if self._booking_id is None:
            print("Booking ID is none.")
            return False

        try:
            with DATABASE as cur:
                cur.execute('''
                    DELETE FROM bookings
                    WHERE ID=?
                ''', (self._booking_id,))
            return True
        except Exception as error:
            raise BookingSaveError(error) from error

    def __str__(self):
        """
            This is used to get the string representation of the class.
        """
        format_date = "%d/%m/%Y"
        start_date = self._start_date.date.strftime(format_date)
        end_date = self._end_date.date.strftime(format_date)
        name = self.user.name
        booking_data = f"{start_date} - {end_date}: {name}"
        return booking_data

    def __del__(self):
        """
            This is used to delete the class.
        """
        items = [self._start_date, self._end_date, self._user_data]
        for i in items:
            self._remove_item(i)

    def __init__(
        self,
        start_time=FormattedTimeAndDate,
        end_time=FormattedTimeAndDate,
        user_data=FormattedUserBookingData,
        create=False,
        booking_id=0,
    ):
        """
            This is used to initialise the class.
        """
        if not self._valid_start_and_end(start_time, end_time):
            raise IncorrectFormattedDateAndTime(
                """The times provided are not valid."""
            )

        self._start_date = start_time
        self._end_date = end_time
        self._user_data = user_data
        self._booking_id = booking_id

        if create:
            start = self._start_date.date.strftime("%d/%m/%Y")
            end = self._end_date.date.strftime("%d/%m/%Y")
            start = f"{start} {start_time.hour}:{start_time.minute}"
            end = f"{end} {end_time.hour}:{end_time.minute}"

            bid = 0
            if booking_id != 0:
                bid = booking_id
            else:
                bid = self._get_booking_id()

            bid = int(bid)
            first_name = str(self._user_data.first_name)
            last_name = str(self._user_data.last_name)
            phone_number = str(self._user_data.phone_number)
            email = str(self._user_data.email)
            postcode = str(self._user_data.postcode)
            pets = int(self._user_data.pets)
            start = str(start)
            end = str(end)

            data = (
                bid,
                first_name,
                last_name,
                phone_number,
                email,
                postcode,
                pets,
                start,
                end,
            )
            with DATABASE as cur:
                cur.execute('''
                    INSERT INTO bookings
                        (ID, first_name, last_name, mobile_number,
                        email_address, postcode, pets, start_time,
                        end_time)
                    VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', data)


def get_dates():
    """
        This is used to get the dates from the database.
    """
    pandas_df = pd.DataFrame({"start_date": [], "end_date": []})
    with DATABASE as cur:
        for row in cur.execute(
        """SELECT start_time, end_time
        FROM bookings"""
        ):

            date_format = "%d/%m/%Y %H:%M"
            if len(row[0]) != len(date_format):
                date_format = "%d/%m/%Y"

            s_d = datetime.strptime(row[0], date_format)
            e_d = datetime.strptime(row[0], date_format)
            pandas_df.loc[len(pandas_df.index)] = [s_d, e_d]
    return pandas_df


class BookingManagement:
    """
        This is used to manage the bookings.
    """
    @classmethod
    def booking_count(cls):
        """
            This is used to get the number of bookings.
        """
        with DATABASE as cur:
            for count_db in cur.execute("SELECT COUNT(*) FROM bookings"):
                return count_db[0] or 0
        return 0

    @classmethod
    def booking_available(
        cls, start_date=FormattedTimeAndDate, end_date=FormattedTimeAndDate
    ):
        """
            This is used to check if the booking is available.
        """
        available = True
        start_date_string = start_date.date
        end_date_string = end_date.date

        if start_date_string > end_date_string:
            raise BookingError(
                """The booking start date cannot be after
                                the end date."""
            )
        elif start_date_string == end_date_string:
            raise BookingError(
                "The booking start date cannot be the same as the end date."
            )

        booking_range = pd.date_range(
            start=start_date_string, end=end_date_string, freq="1H"
        ).date
        booking_rows = None
        with DATABASE as cur:
            booking_rows = cur.execute(
                """SELECT start_time, end_time
                FROM bookings"""
            )
            for row in booking_rows:
                start = str(row[0])[0:10]
                end = str(row[1])[0:10]
                start_time = datetime.strptime(start, "%d/%m/%Y") - timedelta(days=2)
                end_time = datetime.strptime(end, "%d/%m/%Y") + timedelta(days=2)

                db_booking_range = pd.date_range(
                    start=start_time,
                    end=end_time,
                    freq="1H",
                ).date

                for date in db_booking_range:
                    if date in booking_range:
                        available = False
                        print("Banned Date.")

            weekend_allowed = False
            current_time = datetime.now()

            db_booking_range = pd.date_range(
                start=start_date_string, end=end_date_string, freq="1d"
            ).date

            print(abs(current_time - start_date_string).days)
            if abs(current_time - start_date_string).days >= 14:
                weekend_allowed = True
                print("Allowed")
            else:
                print("Not Allowed")

                for date in db_booking_range:
                    if date in booking_range:
                        available = False

                    if date.strftime("%A") == "Sunday" or "Saturday":
                        if not weekend_allowed:
                            available = False
        return available

    @classmethod
    def get_bookings(cls):
        """
            This is used to get the bookings from the database.
        """
        bookings = []
        booking_rows = None
        with DATABASE as cur:
            booking_rows = cur.execute(
                """SELECT ID, first_name, last_name, mobile_number, email_address,
            postcode, start_time, end_time, pets FROM bookings""")
            for row in booking_rows:
                user_data = FormattedUserBookingData(
                    first_name=row[1],
                    last_name=row[2],
                    phone_number=row[3],
                    email=row[4],
                    postcode=row[5],
                    pets=row[8],
                )

                start_time_before_slicing = row[6]
                start_time_date = start_time_before_slicing[0:10]
                print(start_time_date)
                start_time_hour = start_time_before_slicing[11:13]
                start_time_min = start_time_before_slicing[14:16]

                if ":" in start_time_hour:
                    start_time_hour = start_time_hour[:-1]

                end_time_before_slicing = row[7]
                end_time_date = end_time_before_slicing[0:10]
                end_time_hour = end_time_before_slicing[11:13]
                end_time_min = end_time_before_slicing[14:16]

                start_time = FormattedTimeAndDate(
                    start_time_date, start_time_hour, start_time_min
                )
                end_time = FormattedTimeAndDate(end_time_date, end_time_hour, end_time_min)

                booking = Booking(start_time, end_time, user_data, booking_id=row[0])
                bookings.append(booking)

        return bookings

    def __del__(self):
        pass

    def __init__(self):
        self.__del__()
class User:
    """
    This is used to manage users within
    the system.
    """

    @classmethod
    def get_user_from_username(cls, username=""):
        """
            This is used to get a user from the database by their username.
        """
        if username == "":
            return

        sql_select = """
                            SELECT username, level
                            FROM users
                            WHERE username=?
                            """
        with DATABASE as cur:
            for row in cur.execute(sql_select, username):
                user = User(row[0], permission_level=row[1])
                return user

    def _login(self):
        """
            This is used to login the user.

            This is used to create
            a user object by checking the username
            and password with the one within the database.
        """
        username, password = self._username, self._password
        sql_selected_users = None
        with DATABASE as cur:
            sql_selected_users = cur.execute(
                "SELECT level FROM users WHERE username=? AND password=?",
                (username, password)
            )

            for row in sql_selected_users:
                self._pl = row[0]
                self._logged_in = True

        if not self._logged_in:
            raise FailedToLoginToUser(
                """Either the username or the password does not match
                 our records."""
            )

    @property
    def level_text(self):
        """
            This is used to get the level in text form.
        """
        if self.super_admin:
            return "Super Admin"
        elif self.admin:
            return "Admin"
        else:
            return "Guest"

    @property
    def level(self):
        """
            This is used to get the level of the user.
        """
        return self._pl

    @property
    def admin(self):
        """
            This is used to check if the user is an admin.
        """
        if self._pl >= ADMIN_LEVEL:
            return True
        return False

    @property
    def super_admin(self):
        """
            This is used to check if the user is a super admin.
        """
        if self._pl >= SUPER_ADMIN_LEVEL:
            return True
        return False

    @property
    def logged_in(self):
        """
            This is used to check if the user is logged in.
        """
        return self._logged_in

    @logged_in.setter
    def logged_in(self, value=False):
        """
            This is used to set the logged in status of the user.
        """
        if value is False:
            self._logged_in = False
        elif value is True:
            self._login()

    @property
    def change_password_required(self):
        """
            This is used to check if the user needs to change their password.
        """
        return self._password_reset

    @change_password_required.setter
    def change_password_required(self, password=""):
        """
            This is used to set the password reset status of the user.
        """
        self._password = password
        self._login()

    @property
    def username(self):
        """
            This is used to get the username of the user.
        """
        return self._username

    def __init__(self, username="", password="", permission_level=0, login=False):
        """
            This is used to initialise the class.
        """
        self._username = username
        self._password_reset = False

        self._pl = permission_level

        if permission_level is None and login is False:
            raise FailedToMakeUserInstance(
                """A Permission level is required if the user is not being
                logged in."""
            )

        self._password = password

        self._logged_in = False

        if login:
            self._login()

class UserManager:
    """
        This is used to manage users within the system.
    """
    @classmethod
    def change_password(cls, password="", acting_user=User, user=User):
        """
            This is used to change the password of a user.
        """
        if len(password) >= 255:
            raise PasswordValidationError(
                """Password is too large, please choose a password under
                 255 characters."""
            )

        if len(password) <= 8:
            raise PasswordValidationError(
                """Password is too short, please choose a longer password.
                 (8 + Characters)"""
            )

        upper_letter_included = False
        lower_letter_included = False
        number_included = False
        character_included = False

        for character in password:
            if character.isalpha():
                character_included = True
                if character.islower():
                    lower_letter_included = True
                elif character.isupper():
                    upper_letter_included = True
            elif character.isnumeric():
                number_included = True

        if not upper_letter_included:
            raise PasswordValidationError(
                "Password does not include an uppercase letter."
            )
        elif not lower_letter_included:
            raise PasswordValidationError(
                "Password does not include a lowercase letter."
            )
        elif not number_included:
            raise PasswordValidationError(
                """Password does not include a
             number."""
            )
        elif not character_included:
            raise PasswordValidationError(
                """Password does not include a
             letter."""
            )

        if acting_user.logged_in:
            if acting_user == user.level or acting_user.level > user:
                username = user.username
                with DATABASE as cur:
                    cur.execute('''
                        UPDATE users
                        SET password=?
                        WHERE username=?
                    ''', (password, username))
            else:
                raise PermissionDenied(
                    """You are not authorised to modify
                 this account."""
                )
        else:
            raise PermissionDenied(
                "You must be logged in, to change the user's account password."
            )

    @classmethod
    def remove_user(cls, admin_user=User, user_to_remove=User):
        """
            This is used to remove a user from the system.
        """
        if admin_user.logged_in:
            if (
                admin_user.level > user_to_remove.level
                and admin_user.username != user_to_remove.username
            ):
                try:
                    username = user_to_remove.username
                    with DATABASE as cur:
                        cur.execute('''
                        DELETE FROM users
                        WHERE username=?
                        ''', (username,))
                    del user_to_remove
                    return True
                except AttributeError as error:
                    return error
            else:
                raise PermissionDenied(
                    """You are not authorised to modify
                 this account."""
                )
        else:
            raise PermissionDenied("Admin account is not logged in.")

    @classmethod
    def usernames(cls):
        """
            This is used to get all the usernames in the system.
        """
        with DATABASE as cur:
            rows = cur.execute("SELECT username FROM users")

        row_list = []
        for row in rows:
            row_list.append(row[0])

        if len(row_list) == 0:
            row_list.append("")

        return row_list

    @classmethod
    def admin_usernames(cls):
        """
            This is used to get all the admin usernames in the system.
        """

        row_list = []
        with DATABASE as cur:
            rows = cur.execute("SELECT username FROM users WHERE level >= ?", (str(2)))
            for row in rows:
                row_list.append(row[0])

        if len(row_list) == 0:
            row_list.append("")

        return row_list

    @classmethod
    def guest_usernames(cls):
        """
            This is used to get all the guest usernames in the system.
        """
        row_list = []
        with DATABASE as cur:
            rows = cur.execute("SELECT username FROM users WHERE level = ?", (str(1)))

            for row in rows:
                row_list.append(row[0])

        if len(row_list) == 0:
            row_list.append("")

        return row_list

    @classmethod
    def create(cls, admin_user=User, user=User, password=""):
        """
            This is used to create a new user.
        """
        if not admin_user.logged_in:
            raise PermissionDenied("Admin user is not logged in.")

        if user.level > 2:
            raise InvalidAccountLevel(
                """Level provided is too high as it does not meet the
                 current level systems standards."""
            )
        elif user.level < 1:
            raise InvalidAccountLevel(
                f"""The Level provided is too low as the minimum
                 level is {GUEST_LEVEL}"""
            )

        permission_error = True

        if admin_user.super_admin and admin_user.level > user.level:
            permission_error = False
            with DATABASE as cur:
                cur.execute("""
                    INSERT INTO users(username, password, level)
                    VALUES(?, ?, ?)
                """, (str(user.username), str(password), int(user.level)))

            return True

        if permission_error:
            raise PermissionDeniedToCreateAccount(
                f"""User is required to be a Super Admin but the user
                 provided is only a {admin_user.level_text}"""
            )

