_database = None
guest_level = 1
admin_level = 2
super_admin_level = 3

class Booking:
  """
    Used to both view and create
    bookings within the application,
    this class is used to make it easier
    to integrate with the database and the
    application.
  """


  
  def __init__(self):
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

class InvalidAccountLevel(ValueError):
  pass

class FailedToCreateFor(SystemError):
  pass

class User:
  """
    This is used to manage users within
    the system.
  """
    
  
  @classmethod
  def login(self, username="", password=""):
    # This is used to create
    # a user object by checking the username
    # and password with the one within the database.
    
    for row in _database.con.execute("SELECT level FROM users WHERE username=? AND password=?", (username, password)):
      return User(username, row[0])
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
    if self._permission_level >= self.admin_level:
      return True
    else:
      return False
  
  def __del__(self):
    pass

  @property
  def super_admin(self):
    if self._permission_level >= super_admin_level:
      return True
    else:
      return False

  @property
  def username(self):
    return self._username
  
  def __init__(self, username="", permission_level=0, password=""):
    
      
    self._username = username
    self._permission_level = permission_level
    self._password = password
  
class UserManager:

  
  @classmethod
  def usernames(self):
    rows = _database.con.execute("SELECT username FROM users")
    row_list = []
    for row in rows:
      row_list.append(row[0])
      
    return row_list

  @classmethod
  def admin_usernames(self):
    rows = _database.con.execute("SELECT username FROM users WHERE level >= ?", (str(admin_level)))
    
    row_list = []
    for row in rows:
      row_list.append(row[0])
      
    return row_list

  @classmethod
  def guest_usernames(self):
    rows = _database.con.execute("SELECT username FROM users WHERE level = ?", (str(guest_level)))
    row_list = []
    for row in rows:
      row_list.append(row[0])
      
    return row_list

  @classmethod
  def create(self, admin_user=User, user=User, password=""):
    global admin_level, guest_level
    if user.level > admin_level:
      raise InvalidAccountLevel("Level provided is too high as it does not meet the current level systems standards.")
    elif user.level < guest_level:
      raise InvalidAccountLevel(f"The Level provided is too low as the minimum level is {guest_level}")

    if admin_user.super_admin and admin_user.level > user.level:
      _database.con.execute('''
                            INSERT INTO users(username, password, level)
                  VALUES(?, ?, ?)
                            ''', (str(user.username), str(password), int(user.level)))

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

def setup(database=None):
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