from datetime import datetime

_database = None

class IncorrectFormatedDate(ValueError):
  pass

class IncorrectHour(ValueError):
  pass

class FormattedTime:

  @property
  def date(self):
    return self._date

  @property
  def hour(self):
    return self._hour

  @property
  def minute(self):
    return self._min
  
  def __init__(self, date="", hour="", min=""):
    pass

    if int(hour) > 23:
      pass
      
    if int(min) > 60:
      raise 
    combined_string = "{} {}:{}".format(date, hour, min)
    try:
      self._datetime = datetime.strftime(combined_string, "%d/%m/%Y %H:%M")
    except:
      raise IncorrectFormatedDate("Please provided the date with the date as DD/MM/YYYY.")

    
    self._date = date
    self._hour = hour
    self._min = min

    
    

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
    
  def __init__(self, start_time=FormattedTime, end_time = FormattedTime):
    pass

class BookingManagement:

  @classmethod
  def booking_count():
    count = 0
    for i in _database.con.execute("SELECT ID FROM bookings"):
      count += 1

    return count
  
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
    
    for row in _database.con.execute("SELECT level FROM users WHERE username=? AND password=?", (username, password)):
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

  @property
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
      if admin_user.level > user_to_remove.level:
        username = user_to_remove.username
        _database.con.execute('''
                              DELETE FROM users
                              WHERE username=?
                              ''', (username))
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
      
    if user.level > admin_level:
      raise InvalidAccountLevel("Level provided is too high as it does not meet the current level systems standards.")
    elif user.level < guest_level:
      raise InvalidAccountLevel(f"The Level provided is too low as the minimum level is {guest_level}")

    if admin_user.super_admin and admin_user.level > user.level:
      _database.con.execute('''
                            INSERT INTO users(username, password, level)
                  VALUES(?, ?, ?)
                            ''', (str(user.username), str(password), int(user.level)))
      _database.con.commit()
      return True
    else:
      raise PermissionDeniedToCreateAccount(f"User is required to be a Super Admin but the user provided is only a {admin_user.level_text}")
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

   
class LogFailedRequirement(ValueError):
  pass

  
class Logs:

  @classmethod
  def _get_user_log_assignable_id(self):
    for row in _database.con.execute("SELECT MAX(ID) + 1 as new_id FROM user_action_log"):
      return row
    return 1000000
  
  @classmethod
  def create_action_report(self, acting_user=User, user=User, action=""):
    if len(action) >= 10:
      log_id = self._get_assignable_id()
      timestamp = datetime.now()
      timestamp = timestamp.strftime("%d/%m/%Y %H:%M")
      _database.con.execute('''
                            INSERT INTO user_action_log(ID, acting_user, user, action, timestamp)
                            VALUES(?,?,?,?,?)
                          ''', (log_id, acting_user.username, user.username, action, timestamp))
    else:
      raise LogFailedRequirement("Action is below the minimum character requirements.")
  

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