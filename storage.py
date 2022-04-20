# Imports the required modules

import sqlite3
import os

_database_file_extention = "db"

class DatabaseNamingError(ValueError):
  """
    Used to create a naming error, for the program
    if the database file name is incorrect.
  """
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
  
  @property
  def con(self):
    return self._con

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
                  INSERT INTO users(username, password, level)
                  VALUES(?, ?, ?)
                  ''', ("System", "root", 3))
      
      con.commit()
      
    except:
      if self._remove_on_setup_failure:
        os.remove(f"{self._db_name}.{_database_file_extention}")

  def __del__(self):
    try:
      if self._auto_save:
        self._con.commit()

      self._con.close()
    except:
      pass
  
  def __init__(self, db_name="", test_mode=False):
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
      elif len(db_name) < 3:
        raise DatabaseNamingError("File Name provided is too short.")
      elif not db_name.isalpha():
        raise DatabaseNamingError("File Name includes forbidden characters.")
      
      if test_mode:
        # Stops the code before
        # it creates a database connection.
        return
        
      setup = os.path.exists(db_name)
      self._con = sqlite3.connect(f"{db_name}.{_database_file_extention}")
      self._db_name = db_name
      if not setup:
        self._setup()
      