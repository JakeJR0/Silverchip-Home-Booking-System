# Imports the required modules

import sqlite3
import os

_database_file_extention = "db"
month_prices = {
    1: 125,
    2: 125,
    3: 125,
    4: 125,
    5: 200,
    6: 200,
    7: 200,
    8: 200,
    9: 150,
    10: 150,
    11: 150,
    12: 150
  }

class DatabaseNamingError(ValueError):
  """
    Used to create a naming error, for the program
    if the database file name is incorrect.
  """
  pass

class DatabaseStatupFailure(SystemError):
  pass
  
class Database:
  """
    This database object is used to handle
    the connection to the database, this makes
    sure that the database is closed when the instance
    is deleted.

    This could also be used to moderate queries which
    could be useful for security purposes.
  """
  
  _auto_save = True
  _remove_on_setup_failure = True
  active_count = 0

  @property
  def con(self):
    return self._con
    
  def save(self):
    try:
      self._con.commit()
      return True
    except:
      return False
    
  def _setup(self):
    try:
      con = self._con
      con.execute('''
                  CREATE TABLE users(
                    username CHAR(30) PRIMARY KEY NOT NULL,
                    password CHAR(255) NOT NULL,
                    level INT(1) NOT NULL
                  );
                  ''')

      con.execute('''
                  CREATE TABLE bookings(
                    ID INTEGER PRIMARY KEY NOT NULL,
                    first_name CHAR(20) NOT NULL,
                    last_name CHAR(30) NOT NULL,
                    mobile_number CHAR(11) NOT NULL,
                    email_address CHAR(50) NOT NULL,
                    booking_date CHAR(10) NOT NULL,
                    time CHAR(5) NOT NULL
                  );
                  ''')

      con.execute('''
                  CREATE TABLE user_action_log(
                    ID INTEGER PRIMARY KEY NOT NULL,
                    acting_user CHAR(30) NOT NULL,
                    user CHAR(30),
                    action CHAR(30) NOT NULL,
                    timestamp CHAR(16) NOT NULL
                  );
                  ''')

      con.execute('''
                  CREATE TABLE holiday_prices(
                    month INTEGER(2) PRIMARY KEY NOT NULL,
                    price REAL(5) NOT NULL
                  );
                  ''')
      
      con.execute('''
                  INSERT INTO users(username, password, level)
                  VALUES(?, ?, ?)
                  ''', ("System", "root", 3))

      con.execute('''
                  INSERT INTO users(username, password, level)
                  VALUES(?, ?, ?)
                  ''', ("Admin", "root", 2))

      con.execute('''
                  INSERT INTO users(username, password, level)
                  VALUES(?, ?, ?)
                  ''', ("Guest", "root", 1))

      super_admins = ["JakeJR0", "squashedbanana2", "MStreet5"]
      
      for i in super_admins:
        con.execute('''
                  INSERT INTO users(username, password, level)
                  VALUES(?, ?, ?)
                  ''', (i, "root", 3))


        
      for month_id in month_prices:
        self._con.execute('''
                              INSERT INTO holiday_prices(month, price)
                              VALUES(?,?)''', (month_id, month_prices[month_id]))
        
      con.commit()
      
    except Exception as e:
      if self._remove_on_setup_failure:
        if os.path.exists(f"{self._db_name}.{_database_file_extention}"):
          os.remove(f"{self._db_name}.{_database_file_extention}")
          
        if os.path.exists("{}.db-journal".format(self._db_name)):
          os.remove("{}.db-journal".format(self._db_name))
      print("Database Error: {}".format(e))
      raise DatabaseStatupFailure(e)
      

  def __del__(self):
    try:
      if self._auto_save:
        self._con.commit()
      self._con.close()

      if self._delete_on_close:
        if os.path.exists(os.path.exists("{}.{}".format(self._db_name, _database_file_extention))):
          os.remove("{}.{}".format(self._db_name, _database_file_extention))
    except:
      pass

    if not self._test_mode:
      Database.active_count -= 1
  
  def __init__(self, db_name="", test_mode=False, delete_on_close=False):
      self._test_mode = test_mode
    
      # Slices the name to isolate
      # any extention within the file
      # name.
      
      file_name_extention = db_name[:-len(_database_file_extention)]

      # Checks if the file file
      # extention is present for any
      # of the file extentions below.
      if file_name_extention == ".db":
        # Removes the extention from
        # the file name as this will
        # count towards the data 
        # validation.
        db_name = db_name[0:-3]
      if db_name == "":
        raise DatabaseNamingError("No File Name has been provided, please specify a file name.")
      elif len(db_name) > 20:
        raise DatabaseNamingError("File Name provided is longer than 20 characters, please choose a shorter name.")
      elif len(db_name) <= 3:
        raise DatabaseNamingError("File Name provided is too short.")
      elif not db_name.isalpha():
        raise DatabaseNamingError("File Name includes forbidden characters.")
      
      if test_mode:
        # Stops the code before
        # it creates a database connection.
        return
        
      setup = os.path.exists("{}.{}".format(db_name, _database_file_extention))
      self._con = sqlite3.connect(f"{db_name}.{_database_file_extention}")
      self._db_name = db_name
      self._delete_on_close = delete_on_close
    
      if not setup:
        self._setup()

      Database.active_count += 1


      