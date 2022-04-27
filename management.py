from datetime import datetime, timedelta
import pandas as pd

_database = None


class IncorrectFormattedDateAndTime(ValueError):
    pass


def us_date_to_uk(date=""):
  date.replace("-", "/")
  date = "{}/{}/{}".format(date[8:10], date[5:7], date[0:4])
  return date

class FormattedTimeAndDateError(ValueError):
  pass

class FormattedTimeAndDate:

    @property
    def date(self):
        return self._datetime

    @date.setter
    def date(self, value):
      if "-" in value:
        raise FormattedTimeAndDateError("Please provide a valid date.")
        return

      try:
        date_time = datetime.strptime("{} {}:{}".format(value, self.hour, self.minute), "%d/%m/%Y %H:%M")
        self._datetime = date_time
      except:
        raise FormattedTimeAndDateError("Please provide a valid date.")
        return
  
    @property
    def hour(self):
        return int(self._hour)

    @hour.setter
    def hour(self, value=0):
      if value >= 0 and value <= 23:
        self._hour = value
      else:
        raise FormattedTimeAndDateError("Please provide a valid hour.")
  
    @property
    def minute(self):
        return int(self._min)

    @minute.setter
    def minute(self, value=0):
      if value >= 0 and value <= 60:
        self._min = value
      else:
        raise FormattedTimeAndDateError("Please provide a valid date.")

    def __del__(self):
        pass

    def __init__(self, date="", hour=0, min=0):
        def remove_non_number(item=""):
          item = str(item)
          new_item = ""
          for c in item:
            c = str(c)
            if c.isnumeric():
              new_item = f"{new_item}{c}"

          if new_item == "":
            new_item = "00"
          
          return new_item

        hour = remove_non_number(hour)
        min = remove_non_number(min)
      
        if int(hour) > 23:
            raise IncorrectFormattedDateAndTime("The hour parameter is greater than 23.")
        elif int(hour) < 0:
            raise IncorrectFormattedDateAndTime("The hour parameter is less than 0.")

        if date == "":
            raise IncorrectFormattedDateAndTime("The Date parameter is empty.")

        if min == "" or " " or "  ":
          min = str(0)

        if hour == "" or " " or "  ":
          hour = str(0)
      
        print(min)
        if int(min) <= 9:
          min = str(f"0{min}")
        else:
          min = str(min)

        if int(hour) <= 9:
          hour = str(f"0{hour}")
        else:
          hour = str(hour)
        
        combined_string = "{} {}:{}".format(date, hour, min)
        try:
            self._datetime = datetime.strptime(combined_string, "%d/%m/%Y %H:%M")
        except ValueError as r:
            raise IncorrectFormattedDateAndTime(r)

        self._hour = hour
        self._min = min

class FormattedUserError(ValueError):
  pass

class FormattedUserBookingData:
  """
    Used to store booking information about a user.
  """

  @property
  def first_name(self):
    return self._first_name


  @first_name.setter
  def first_name(self, name=""):
    if len(name) >= 3 and len(name) <= 20:
      self._first_name = name
    else:
      raise FormattedUserError("First name must be 3 - 20 characters long.")
  
  @property
  def last_name(self):
    return self._last_name

  @last_name.setter
  def last_name(self, name=""):
    if len(name) >= 3 and len(name) <= 30:
      self._last_name = name
    else:
      raise FormattedUserError("Last name must be 3 - 30 Characters long.")

  @property
  def name(self):
    return f"{self._first_name} {self._last_name}"

  @name.setter
  def name(self, name=""):
    first_name, last_name = "", ""
    try:
      first_name, last_name = name.split(" ", 2)
    except:
      raise FormattedUserError("Both a first name and a last name must be provided.")
      return
      
    if len(first_name) >= 3 and len(first_name) <= 20:
      self._first_name = first_name
    else:
      raise FormattedUserError("First name must be 3 - 20 characters long.")
    
    if len(last_name) >= 3 and len(last_name) <= 30:
      self._last_name = last_name
    else:
      raise FormattedUserError("Last name must be 3 - 30 Characters long.")
      
  
  @property
  def phone_number(self):
    return self._phone_number

  @phone_number.setter
  def phone_number(self, value=""):
    if len(value) == 11:
      bad_char_found = False
      for i in value:
        if not i.isnumeric():
          raise FormattedUserError("The phone number should only include numbers.")
          bad_char_found = True
          break
          
      if bad_char_found:
        return
        
      self._phone_number = value
    else:
      raise FormattedUserError("Phone number must be 11 characters but you have {} characters.".format(str(len(value))))

  @property
  def email(self):
    return self._email

  @email.setter
  def email(self, email=""):
    dot_count = 0
    at_count = 0

    for c in email:
      if c == ".":
        dot_count += 1
      elif c == "@":
        at_count += 1

    if dot_count > 3 or at_count > 1 or len(email) > 50 or len(email) < 6:
      raise FormattedUserError("Please provide a valid email address.")
      return

    self._email = email
  
  @property
  def pets(self):
    return self._pets

  @pets.setter
  def pets(self, value=0):
    if value >= 0 and value <= 2:
      self._pets = value
    else:
      raise FormattedUserError("Please choose a number of pets between 0 and 2.")

  @property
  def postcode(self):
    return self._postcode

  @postcode.setter
  def postcode(self, code=""):
    index = 0
    def raise_post_error():
      raise FormattedUserError("Please provide a valid postcode.")

    if len(code) >= 5 and len(code) <= 7:
      self._postcode = code
      return
    else:
      raise_post_error()
    
  
  def __str__(self):
    output_string = "Name: {}\nEmail: {}\nPostcode: {}\nNumber: {}\nPets: {}".format(self.name, self._email, self._postcode, self._phone_number, self._pets)
    return output_string
  
  def __del__(self):
    pass

  def __init__(self, first_name="", last_name="", postcode="", email="", phone_number="", pets=0):
    self._first_name, self._last_name = first_name, last_name
    self._postcode = postcode
    self._email = email
    self._phone_number = phone_number
    self._pets = pets

class BookingError(ValueError):
  pass

class BookingSaveError(SystemError):
  pass

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
            print(row)
            if row[0] is not None:
              start_id = row[0]

        return start_id
  
    @property
    def start(self):
      return self._start_date

    @start.setter
    def start(self, value=FormattedTimeAndDate):
      if self._valid_start_and_end(value, self._end_date):
        self._start_date = value
        
  
    @property
    def end(self):
      return self._end_date

    @end.setter
    def end(self, value=FormattedTimeAndDate):
      if self._valid_start_and_end(self._start_date, value):
        self._end_date = value
  
    @property
    def user(self):
      return self._user_data
      
    @property
    def cost(self):
      total_cost = 0
      date_format = "%d/%m/%Y"
      start = self._start_date.date.strftime(date_format)
      end = self._end_date.date.strftime(date_format)
      date_range = pd.date_range(start=start, end=end, freq="1d")
      month_prices = pd.DataFrame({
        "month": [],
        "price": []
      })
      
      for row in _database.con.execute("SELECT month, price FROM holiday_prices"):
        month_prices.loc[len(month_prices.index)] = [int(row[0]), row[1]]
        
      for date in date_range.date:
        date = us_date_to_uk(str(date))
        month = str(int(date[3:5]))
        print("Month", month)
        price = 0
        for i in month_prices.index:
          if int(month) == int(month_prices.loc[i, "month"]):
            price = month_prices.loc[i, "price"]
            total_cost += price

      pet_cost = float(int(self._user_data.pets) * 25)
      total_cost += pet_cost
      
      return total_cost

      
    def _valid_start_and_end(self, start=FormattedTimeAndDate, end=FormattedTimeAndDate):
      return True

    def _remove_item(self, item=None):
      try:
        del item
      except:
        pass

    def save(self):
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
        start = "{} {}:{}".format(start, self.start.hour, self.start.minute)
        end = "{} {}:{}".format(end, self.end.hour, self.end.minute)
        start = us_date_to_uk(start)
        end = us_date_to_uk(end)
      
        try:
          data = (first_name, last_name, phone_number, email, postcode, pets, start, end, bid)
          print(bid ,data)
          
          _database.con.execute('''
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
                
          _database.save()
          return True
        except Exception as e:
          raise BookingSaveError(e)
          return False

    def delete(self):
      if self._booking_id is None:
        print("Booking ID is none.")
        return False

      try:
        _database.con.execute('''
                              DELETE FROM bookings
                              WHERE ID=?
                              ''', (self._booking_id, ))
        _database.save()
        return True
      except Exception as e:
        print(e)
        return False
      
  
    def __str__(self):
      format_date = "%d/%m/%Y"
      start_date = self._start_date.date.strftime(format_date)
      end_date = self._end_date.date.strftime(format_date)
      name = self.user.name
      booking_data = "{} - {}: {}".format(start_date, end_date, name)
      return booking_data
    
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
        start = self._start_date.date.strftime("%d/%m/%Y")
        end = self._end_date.date.strftime("%d/%m/%Y")
        start = "{} {}:{}".format(start, start_time.hour, start_time.minute)
        end = "{} {}:{}".format(end, end_time.hour, end_time.minute)
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
        
        data = (bid, first_name, last_name, phone_number, email, postcode, pets, start, end)
        
        _database.con.execute('''
                                INSERT INTO bookings 
                                (ID, first_name, last_name, mobile_number, email_address, postcode, pets, start_time, end_time)
                                VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?)
                                ''', data)
        _database.save()
        

def get_dates():
  start_date = []
  end_date = []

  for row in _database.con.execute("SELECT start_time, end_time FROM bookings"):
    format = "%d/%m/%Y %H:%M"
    if len(row[0]) != len(format):
      format = "%d/%m/%Y"
      
    s_d = datetime.strptime(row[0], format)
    e_d = datetime.strptime(row[0], format)
    start_date.append(s_d)
    end_date.append(e_d)
  return start_date, end_date

class BookingManagement:
      
    @classmethod
    def booking_count(self):
        for count_db in _database.con.execute("SELECT COUNT(*) FROM bookings"):
            return count_db[0] or 0
        return 0

    @classmethod
    def booking_available(self, start_date=FormattedTimeAndDate, end_date=FormattedTimeAndDate):
      available = True
      start_date_string = start_date.date
      end_date_string = end_date.date
      if start_date_string > end_date_string:
        raise BookingError("The booking start date cannot be after the end date.")
        return
      elif start_date_string == end_date_string:
        raise BookingError("The booking start date cannot be the same as the end date.")

      start_dates, end_dates = get_dates()

      for start_date in start_dates:
        if start_date_string >=  start_date + timedelta(days=1):
          raise BookingError("You must choose a different end date.")
          
      for end_date in end_dates:
        if end_date_string >= end_date - timedelta(days=1):
          raise BookingError("You must choose a different date,#.")
        
      booking_range = pd.date_range(start=start_date_string, end=end_date_string, freq="1H").date

      for row in _database.con.execute("SELECT start_time, end_time FROM bookings"):
        start = str(row[0])[0:10]
        end = str(row[1])[0:10]
        
        db_booking_range = pd.date_range(start=start, end=end, freq="1H").date
        
        for date in db_booking_range:
          if date in booking_range:
            available = False

      return available
  
    @classmethod
    def get_bookings(self):
      bookings = []
      
      for row in _database.con.execute("SELECT ID, first_name, last_name, mobile_number, email_address, postcode, start_time, end_time, pets FROM bookings"):
        user_data = FormattedUserBookingData(first_name=row[1], last_name=row[2], phone_number=row[3], email=row[4], postcode=row[5], pets=row[8])

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
