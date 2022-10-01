"""
    This file contains all the classes that are
    used to modify the format of the data for the
    management module.
"""

from datetime import datetime

from management_exceptions import FormattedTimeAndDateError
from management_exceptions import FormattedUserError, IncorrectFormattedDateAndTime

# Coversion of date from US format to UK format
def us_date_to_uk(date=""):
    """
        This is used to convert a date from US format to UK format.
    """
    date.replace("-", "/")
    date = f"{date[8:10]}/{date[5:7]}/{date[0:4]}"
    return date

class FormattedTimeAndDate:
    """
        This is used to ensure that the date and time is formatted correctly.
    """
    @property
    def date(self):
        """
            This is used to get the date.
        """
        return self._datetime

    @date.setter
    def date(self, value):
        """
            This is used to set the date.
        """
        if "-" in value:
            raise FormattedTimeAndDateError("Please provide a valid date.")

        try:
            date_time = datetime.strptime(
                f"{value} {self.hour}:{self.minute}", "%d/%m/%Y %H:%M"
            )
            self._datetime = date_time
        except ValueError as error:
            raise FormattedTimeAndDateError("Please provide a valid date. \
            Error: {error}") from error

    @property
    def hour(self):
        """
            This is used to get the hour.
        """
        return int(self._hour)

    @hour.setter
    def hour(self, value=0):
        """
            This is used to set the hour.
        """
        if value >= 0 and value <= 23:
            self._hour = value
        else:
            raise FormattedTimeAndDateError("Please provide a valid hour.")

    @property
    def minute(self):
        """
            This is used to get the minute.
        """
        return int(self._min)

    @minute.setter
    def minute(self, value=0):
        """
            This is used to set the minute.
        """
        if value >= 0 and value <= 60:
            self._min = value
        else:
            raise FormattedTimeAndDateError("Please provide a valid date.")

    def __init__(self, date="", hour=0, minutes=0):
        """
            This is used to initialise the class.
        """
        def remove_non_number(item=""):
            """
                This is used to remove non number characters from a string.
            """
            items = str(item)
            new_item = ""
            for item in items:
                item = str(item)
                if item.isnumeric():
                    new_item = f"{new_item}{item}"
            if new_item == "":
                new_item = "00"
            return new_item

        if minutes == "":
            minutes = str(0)

        if hour == "":
            hour = str(0)

        if int(hour) > 23:
            print("JJ1")
            raise FormattedTimeAndDateError(
                """The hour parameter is greater
                                            than 23."""
            )

        if int(hour) < 0:
            print("JJ2")
            raise FormattedTimeAndDateError(
                """The hour parameter is less
                                             than 0."""
            )

        if int(minutes) > 60:
            print("JJ4")
            raise FormattedTimeAndDateError(
                """The Minute cannot be higher
                                             than 60."""
            )

        if int(minutes) < 0:
            raise FormattedTimeAndDateError(
                """The Minute cannot be lower
                                             than 0."""
            )
        hour = remove_non_number(hour)
        minutes = remove_non_number(minutes)

        if date == "":
            print("JJ3")
            raise FormattedTimeAndDateError("The Date parameter is empty.")
        if int(minutes) <= 9:
            minutes = str(f"0{minutes}")
        else:
            minutes = str(minutes)

        if int(hour) <= 9:
            hour = str(f"0{hour}")
        else:
            hour = str(hour)

        combined_string = f"{date} {hour}:{minutes}"
        try:
            self._datetime = datetime.strptime(combined_string, "%d/%m/%Y %H:%M")
        except ValueError as error:
            raise IncorrectFormattedDateAndTime(error) from error

        self._hour = hour
        self._min = minutes

class FormattedUserBookingData:
    """
    Used to store booking information about a user.
    """

    @property
    def first_name(self):
        """
            This is used to get the first name.
        """
        return self._first_name

    @first_name.setter
    def first_name(self, name=""):
        """
            This is used to set the first name.
        """
        if len(name) >= 3 and len(name) <= 20:
            self._first_name = name
        else:
            raise FormattedUserError(
                """First name must be 3 - 20
                                     characters long."""
            )

    @property
    def last_name(self):
        """
            This is used to get the last name.
        """
        return self._last_name

    @last_name.setter
    def last_name(self, name=""):
        """
            This is used to set the last name.
        """
        if len(name) >= 3 and len(name) <= 30:
            self._last_name = name
        else:
            raise FormattedUserError(
                """Last name must be 3 - 30
                                     Characters long.""")

    @property
    def name(self):
        """
            This is used to get the name.
        """
        return f"{self._first_name} {self._last_name}"

    @name.setter
    def name(self, name=""):
        """
            This is used to set the name.
        """
        first_name, last_name = "", ""
        try:
            first_name, last_name = name.split(" ", 2)
        except ValueError as error:
            raise FormattedUserError(
                f"Both a first name and a last name must be provided. Error: {error}"
            ) from error

        if len(first_name) >= 3 and len(first_name) <= 20:
            self._first_name = first_name
        else:
            raise FormattedUserError(
                """First name must be 3 - 20
                                     characters long."""
            )

        if len(last_name) >= 3 and len(last_name) <= 30:
            self._last_name = last_name
        else:
            raise FormattedUserError(
                """Last name must be 3 - 30
                                     Characters long."""
            )

    @property
    def phone_number(self):
        """
            This is used to get the phone number.
        """
        return self._phone_number

    @phone_number.setter
    def phone_number(self, value=""):
        """
            This is used to set the phone number.
        """
        if len(value) == 11:
            for i in value:
                if not i.isnumeric():
                    raise FormattedUserError(
                        "The phone number should only include numbers."
                    )

            self._phone_number = value
        else:
            raise FormattedUserError(
                f"Phone number must be 11 characters but you have {str(len(value))} characters.")

    @property
    def email(self):
        """
            This is used to get the email.
        """
        return self._email

    @email.setter
    def email(self, email=""):
        """
            This is used to set the email.
        """
        dot_count = 0
        at_count = 0

        for email_part in email:
            if email_part == ".":
                dot_count += 1
            elif email_part == "@":
                at_count += 1

        if dot_count > 3 or at_count > 1 or len(email) > 50 or len(email) < 6:
            raise FormattedUserError("Please provide a valid email address.")
        self._email = email

    @property
    def pets(self):
        """
            This is used to get the pets.
        """
        return self._pets

    @pets.setter
    def pets(self, value=0):
        """
            This is used to set the pets.
        """
        if value >= 0 and value <= 2:
            self._pets = value
        else:
            raise FormattedUserError(
                "Please choose a number of pets\
                between 0 and 2.")

    @property
    def postcode(self):
        """
            This is used to get the postcode.
        """
        return self._postcode

    @postcode.setter
    def postcode(self, code=""):
        """
            This is used to set the postcode.
        """

        def raise_post_error():
            raise FormattedUserError("Please provide a valid postcode.")

        if len(code) >= 5 and len(code) <= 7:
            self._postcode = code
        else:
            raise_post_error()

    def __str__(self):
        """
            This is used to return the string representation of the class.
        """
        output_string = (
            "Name: {self.name}\nEmail: {self._email}\n\
            Postcode: {self._postcode}\nNumber: {self._phone_number}\n\
            Pets: {self._pets}"
        )
        return output_string

    def __init__(
        self,
        first_name="",
        last_name="",
        postcode="",
        email="",
        phone_number="",
        pets=0,
    ):
        """
            This is used to initialise the class.
        """

        self._first_name, self._last_name = first_name, last_name
        self._postcode = postcode
        self._email = email
        self._phone_number = phone_number
        self._pets = pets
