from datetime import datetime, timedelta

_database = None


class IncorrectFormattedDateAndTime(ValueError):
    pass


class FormattedTimeAndDate:

    @property
    def date(self):
        return self._datetime

    @property
    def hour(self):
        return int(self._hour)

    @property
    def minute(self):
        return int(self._min)

    def __del__(self):
        pass

    def __init__(self, date="", hour=0, min=0):
        if int(hour) > 23:
            raise IncorrectFormattedDateAndTime("The hour parameter is greater than 23.")
        elif int(hour) < 0:
            raise IncorrectFormattedDateAndTime("The hour parameter is less than 0.")

        if date == "":
            raise IncorrectFormattedDateAndTime("The Date parameter is empty.")

        hour = str(hour)
        min = str(min)

        combined_string = "{} {}:{}".format(date, hour, min)
        try:
            self._datetime = datetime.strptime(combined_string, "%d/%m/%Y %H:%M")
        except ValueError as r:
            raise IncorrectFormattedDateAndTime(r)

        self._hour = hour
        self._min = min

class FormattedUserBookingData:
  """
    Used to store booking information about a user.
  """

  @property
  def first_name(self):
    return self._first_name

  @property
  def last_name(self):
    return self._last_name

  @property
  def phone_number(self):
    return self._phone_number

  @property
  def email(self):
    return self._email

  @property
  def pets(self):
    return self._pets
  
  def __del__(self):
    pass

  def __init__(self, first_name="", last_name="", postcode="", email="", phone_number="", pets=0):
    self._first_name, self._last_name = first_name, last_name
    self._postcode = postcode
    self._email = email
    self.phone_number = phone_number
    self._pets = pets
    

class Booking:
    """
      Used to both view and create
      bookings within the application,
      this class is used to make it easier
      to integrate with the database and the
      application.
    """
    
    def _get_booking_id(self):
        start_id = 100000
        for row in _database.con.execute("SELECT MAX(ID) + 1 AS new_id FROM bookings"):
            start_id = row

        return start_id

    @property
    def start(self):
      return self.start_date

    @property
    def end(self):
      return self._end_date

    @property
    def user(self):
      return self._user_data

    @property
    def cost(self):
      total_cost = 0
      total_days = self._start_date.date - self._end_date.date
      days = total_days.days()
      month_prices = {
        
      }
      for row in _database.con.execute("SELECT month, price FROM holiday_prices"):
        month_prices[row[0]] = row[1]
        
      for day in range(0, days):
        current_day = self._start_date + timedelta(days=day)
        current_day = current_day.strftime("%d/%m/%Y")
        current_month = int(current_day[3:4])
        current_day_cost = month_prices[current_month]
        total_cost += current_day_cost

      pet_cost = self._user_data.pets * 25
      total_cost += pet_cost
      
      return total_cost

      
    def _valid_start_and_end(self, start=FormattedTimeAndDate, end=FormattedTimeAndDate):
      return True

    def _remove_item(self, item=None):
      try:
        del item
      except:
        pass
  
    def __del__(self):
      items = [self._start_date, self._end_date, self._user_data]
      for i in items:
        self._remove_item(i)
      
    def __init__(self, start_time=FormattedTimeAndDate, end_time=FormattedTimeAndDate, user_data=FormattedUserBookingData, create=False, booking_id=0):

      if not self._valid_start_and_end(start_time, end_time):
        raise IncorrectFormattedDateAndTime("The times provided are not valid.")
        return
        
      self._start_date = start_time
      self._end_date = end_time
      self._user_data = user_data
      self._booking_id = booking_id

      if create:
        try:
          start = self._start_date.strftime("%d/%m/%Y")
          end = self._end_date.strftime("%d/%m/%Y")
          start = "{} {}:{}".format(start, start_time.hour, start_time.minute)
          end = "{} {}:{}".format(end, end_time.hour, end_time.minute)
          bid = 0
          if booking_id != 0:
            bid = booking_id
          else:
            bid = self._get_booking_id()
            
          data = (bid, user_data.first_name, user_data.last_name, user_data.phone_number, user_data.email, user_data._postcode, user_data.pets, start, end)
          
          _database.con.execute('''
                                INSERT INTO bookings 
                                (ID, first_name, last_name, mobile_number, email_address, postcode, pets, start_time, end_time)
                                VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?)
                                ''', data)
          _database.save()
        except:
          pass


class BookingManagement:
  
    @classmethod
    def booking_count(self):
        count = 0
        for count_db in _database.con.execute("SELECT COUNT(ID) FROM bookings"):
            count_db = count

        return count

    @classmethod
    def get_bookings(self):
      bookings = []
      
      for row in _database.con.execute("SELECT ID, first_name, last_name, mobile_number, email_address, postcode, start_time, end_time, pets FROM bookings"):
        user_data = FormattedUserBookingData(first_name=row[1], last_name=row[2], phone_number=row[3], email=row[4], postcode=row[5], pets=row[8])

        start_time_before_slicing = row[6]
        start_time_date = start_time_before_slicing[0:10]
        start_time_hour = start_time_before_slicing[11:13]
        start_time_min = start_time_before_slicing[14:16]

        end_time_before_slicing = row[7]
        end_time_date = end_time_before_slicing[0:10]
        end_time_hour = end_time_before_slicing[11:13]
        end_time_min = end_time_before_slicing[14:16]
        
        start_time = FormattedTimeAndDate(start_time_date, start_time_hour, start_time_min)
        end_time = FormattedTimeAndDate(end_time_date, end_time_hour, end_time_min)
        
        booking = Booking(start_time, end_time, user_data, booking_id=row[0])
        bookings.append(booking)

      return bookings

    
  
    def __del__(self):
        pass

    def __init__(self):
        self.__del__()


class FailedToLoginToUser(ValueError):
    pass


class PermissionDeniedToCreateAccount(ValueError):
    pass


class PermissionDenied(SystemError):
    pass


class InvalidAccountLevel(ValueError):
    pass


class FailedToCreateFor(SystemError):
    pass


class FailedToMakeUserInstance(ValueError):
    pass


class PasswordValidationError(ValueError):
    pass


class User:
    """
      This is used to manage users within
      the system.
    """

    def _login(self):
        # This is used to create
        # a user object by checking the username
        # and password with the one within the database.
        username, password = self._username, self._password

        for row in _database.con.execute("SELECT level FROM users WHERE username=? AND password=?",
                                         (username, password)):
            self._permission_level = row[0]
            self._logged_in = True

        if not self._logged_in:
            raise FailedToLoginToUser("Either the username or the password does not match our records.")

    @property
    def level_text(self):
        if self.super_admin:
            return "Super Admin"
        elif self.admin:
            return "Admin"
        else:
            return "Guest"

    @property
    def level(self):
        return self._permission_level

    @property
    def admin(self):
        if self._permission_level >= 2:
            return True
        else:
            return False

    def __del__(self):
        pass

    @property
    def super_admin(self):
        if self._permission_level >= 3:
            return True
        else:
            return False

    @property
    def logged_in(self):
        return self._logged_in

    @logged_in.setter
    def logged_in(self, value=False):
        if value == False:
            self._logged_in = False
        elif value == True:
            self._login()

    @property
    def change_password_required(self):
        return self._password_reset

    @change_password_required.setter
    def change_password_required(self, password=""):
        self._password = password
        self._login()

    @property
    def username(self):
        return self._username

    def __init__(self, username="", password="", permission_level=0, login=False):

        self._username = username
        self._password_reset = False

        self._permission_level = permission_level

        if permission_level is None and login == False:
            raise FailedToMakeUserInstance("A Permission level is required if the user is not being logged in.")

        self._password = password

        self._logged_in = False

        if login:
            self._login()


class UserManager:

    @classmethod
    def change_password(self, password="", acting_user=User, user=User):
        if password >= 255:
            raise PasswordValidationError("Password is too large, please choose a password under 255 characters.")
            return False
        elif password <= 7:
            raise PasswordValidationError("Password is too short, please choose a longer password. (8 + Characters)")
            return False

        upper_letter_included = False
        lower_letter_included = False
        number_included = False
        character_included = False

        for character in password:
            if character.isalpha():
                character_included = True
            elif character.isnumeric():
                number_included = True
            elif character.islower():
                lower_letter_included = True
            elif character.isupper():
                upper_letter_included = True

        if not upper_letter_included:
            raise PasswordValidationError("Password does not include an uppercase letter.")
            return False
        elif not lower_letter_included:
            raise PasswordValidationError("Password does not include a lowercase letter.")
            return False
        elif not number_included:
            raise PasswordValidationError("Password does not include a number.")
            return False
        elif not character_included:
            raise PasswordValidationError("Password does not include a letter.")
            return False

        if acting_user.logged_in:
            if acting_user == user or acting_user.level > user:
                _database.con.execute('''
                              UPDATE users
                              SET password='?'
                              WHERE username=?
                              ''', (password, user.username))

                _database.save()
            else:
                raise PermissionDenied("You are not authorised to modify this account.")
        else:
            raise PermissionDenied("You must be logged in, to change the user's account password.")

    @classmethod
    def remove_user(self, admin_user=User, user_to_remove=User):
        if admin_user.logged_in:
            if admin_user.level > user_to_remove.level and admin_user.username != user_to_remove.username:
                try:
                    username = user_to_remove.username
                    _database.con.execute('''
                                DELETE FROM users
                                WHERE username=?
                                ''', (username,))
                    _database.save()
                    del user_to_remove
                    return True
                except Exception as e:
                    return e
            else:
                raise PermissionDenied("You are not authorised to modify this account.")
        else:
            raise PermissionDenied("Admin account is not logged in.")

    @classmethod
    def usernames(self):
        rows = _database.con.execute("SELECT username FROM users")
        row_list = []
        for row in rows:
            row_list.append(row[0])

        if len(row_list) == 0:
            row_list.append("")

        return row_list

    @classmethod
    def admin_usernames(self):
        rows = _database.con.execute("SELECT username FROM users WHERE level >= ?", (str(2)))

        row_list = []
        for row in rows:
            row_list.append(row[0])

        if len(row_list) == 0:
            row_list.append("")

        return row_list

    @classmethod
    def guest_usernames(self):
        rows = _database.con.execute("SELECT username FROM users WHERE level = ?", (str(1)))
        row_list = []
        for row in rows:
            row_list.append(row[0])

        if len(row_list) == 0:
            row_list.append("")

        return row_list

    @classmethod
    def create(self, admin_user=User, user=User, password=""):
        global admin_level, guest_level
        if not admin_user.logged_in:
            raise PermissionDenied("Admin user is not logged in.")

        if user.level > 2:
            raise InvalidAccountLevel(
                "Level provided is too high as it does not meet the current level systems standards.")
        elif user.level < 1:
            raise InvalidAccountLevel(f"The Level provided is too low as the minimum level is {guest_level}")

        if admin_user.super_admin and admin_user.level > user.level:
            _database.con.execute('''
                            INSERT INTO users(username, password, level)
                  VALUES(?, ?, ?)
                            ''', (str(user.username), str(password), int(user.level)))
            _database.con.commit()
            return True
        else:
            raise PermissionDeniedToCreateAccount(
                f"User is required to be a Super Admin but the user provided is only a {admin_user.level_text}")
            return

    def __del__(self):
        pass

    def __init__(self):
        self.__del__()


class ManagementSetupFailure(SystemError):
    """
      Used to notify the user if the file has not
      correctly setup.
    """

    pass


def setup(database=None, test=False):
    global _database

    if database is None:
        raise ManagementSetupFailure("Failed to find a database instance.")
    else:
        try:
            if not database.con:
                raise ManagementSetupFailure("Failed to find database connection.")
        except ManagementSetupFailure as error:
            raise ManagementSetupFailure(error)
        except:
            pass

    _database = database

    return True
