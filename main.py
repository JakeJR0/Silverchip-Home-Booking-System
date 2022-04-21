# Silverchip Holiday Home Booking Program
# Designed and programmed by: Alex Unsworth, Mitchell Street and Jake James-Robinson

# Import Python modules
from tkinter import *
from PIL import ImageTk, Image
import management
import storage
import tkinter
import tkinter.font as fnt
from tkinter import messagebox as box
from tkcalendar import DateEntry
import time

class InvalidPageParent(ValueError):
  """
    This is used to provide a custom 
    error if the user is providing an 
    invalid parent when creating a new page.
  """
  pass

class Application:

  _app_size_x = 800
  _app_size_y = 500
  
  def close(self):
    self._root.destroy()

  def __del__(self):
    try:
      if self._root:
        self._root.destroy()
    except:
      pass

    try:
      if self._db and self._db is not None:
        self._db.con.close()
    except:
      pass
  
  def _create_page(self, parent=None):
    # Creates a new frame
    # and adds it to the 
    # page list which 
    # allows for swaping between
    # pages.

    if parent is None:
      parent = self._root
      
    temp = None
    
    try:
      temp = Frame(self._root, width=self._app_size_x, height=self._app_size_y)
      self._pages.append(temp)
    finally:
      return temp

  def _focus_on_password(self, event=None):
    self._login_page_pass_entry.focus()
    
  def _select_page(self, selected_page=None):
    # This goes though all pages
    # within the list and checks if
    # it is the page that was provided
    # if it was then the page will be shown
    # if not it will hide the page from the user.
    
    for page in self._pages:
      if page == selected_page:
        page.pack()
        print("Packed ", page)
      else:
        page.pack_forget()
        print("Unpacked ", page)
        
  def _logout(self):
    failed = False
    try:
      if self._user is not None:
        del self._user
    except Exception as error:
      failed = True
      box.showerror("Internal Error", error)
    
    try:
      self._select_page(self._login_page)
      if not failed:
        box.showinfo("Success", "You have been successfully logged out of the application.")
    except Exception as error:
      box.showerror("Internal Error", error)

  def _add_new_account(self, admin_user=management.User, user=management.User, password=""):
    if not admin_user.logged_in:
      return

    if user.level < admin_user.level:
      result = management.UserManager.create(admin_user, user, password)
      if result:
        if user.level == 1:
          self._admin_list.insert(END, user.username)
        elif user.level == 2:
          self._guest_list.insert(END, user.username)
          
    
    
  
  def _get_account(self):
    account = {
      "type": None,
      "name": None, 
      "position": None
    }
    

    admins, guests = self._admin_list, self._guest_list

    found_selection = False
    
    for i in admins.curselection():
      item = admins.get(i)
      account["type"] = "admin"
      account["name"] = item
      account["position"] = i
      found_selection = True
      break

    for i in guests.curselection():
      if found_selection:
        break
        
      item = guests.get(i)
      account["type"] = "guest"
      account["name"] = item
      account["position"] = i
      found_selection = True
      break

    return account

  def _new_account_page_submit(self, event=None):
    new_user_name = self._new_page_name_entry.get()
    new_user = management.User("Username", new_user_name, permission_level=2,)
    success = management.UserManager.create(self._user, new_user, "password")
    creation_successful= tkinter.Label(main_menu, text="Account Creation Successful", font=('Helvetica', 12), fg='green')
    creation_successful.grid(row=1, column=3, padx=(274, 0))
    return
    
    
  def _login_page_submit(self, event=None):
    username = self._login_page_name_entry.get()
    password = self._login_page_pass_entry.get()

    self._login_page_name_entry.delete(0, END)
    self._login_page_pass_entry.delete(0, END)
    user = None
    try:
      user = management.User(username, password, login=True)
    except management.FailedToLoginToUser as error:
      box.showerror("Login Failed", error)
      self._login_page_name_entry.focus()
      return
    except Exception as error:
      print(error)
      self._login_page_name_entry.focus()
      return

    self._user = user

    box.showinfo("Login Message", "You have been logged in.")
    self._select_page(self._main_menu)

    if self._user.admin:
      self._admin_label.config(fg="red", text="Admin Account") 
    elif not self._user.admin:
      self._admin_label.config(fg="blue", text="Guest Account") 
    else:
      box.showerror("Failed to load", "Account level was not found.")

  def _focus_on(self, object=None):
    object.focus()

  def _go_to_main_menu(self, event=None):
    self._select_page(self._main_menu)

  def _go_to_make_booking(self, event=None):
    self._select_page(self._make_booking)

  def _go_to_manage_accounts(self, event=None):
    self._select_page(self._manage_accounts_page)

  def _go_to_edit_accounts(self, event=None):
    self._select_page(self._new_accounts_page)
 
  def _go_to_new_password_page(self, event=None):
    self._select_page(self._new_password_page)

  def _hide_booking_status_message(self, event=None):
    self._booking_availability.config(text="")
      
    
  def _check_booking_availability(self, event=None):
    make_booking = self._make_booking
    booking_available = True
    # Available or Unavailable status
    
    if booking_available == True:
      self._booking_availability.config(text="Booking available", fg="green")
    if booking_available == False:
      self._booking_availability.config(text="Booking unavailable", fg="red")
    else:
      self._booking_availability.config(text="Checking availability...", fg="yellow")

    self._booking_availability.after(3000, self._hide_booking_status_message)

  def _create_account_action(self):
    pass # Alex

  def _remove_account_action(self):
    account_details = self._get_account()
    user_to_remove = management.User(account_details["name"])     
    management.UserManager.remove_user(self._user, user_to_remove)
    
  def _open_admin_panel(self):
    print("Username: {} Level: {}".format(self._user.username, self._user.level))
    if self._user.level > 1:
      self._select_page(self._admin_page)
    else:
      box.showwarning("Access Denied", "You are not authorised to access this area.")

  def _open_system_analytics(self):
    self._select_page(self._system_analytics_page)
    print("Opened")
  
  def __init__(self):
    self._pages = []
    self._db = None
    self._root = Tk()
    self._root.geometry("800x500") # Sets size of window
    self._menu = Menu(self._root, tearoff=0)
    self._root.title('Booking System')  # Set name of window
    # Set background
    img = PhotoImage(file="")  # Select background image
    background = Label(self._root, image=img)
    
    
    self._root.config(menu=self._menu)
    self._root.resizable(False, False) # Prevents window resizing

    # Login page
    # Login Page is just a frame
    # instance from tkinter
    login_page = self._create_page() 
    admin_page = self._create_page()
    make_booking_page = self._create_page()
    manage_accounts_page = self._create_page()
    new_accounts_page = self._create_page()
    new_password_page = self._create_page()
    system_analytics_page = self._create_page()
    
    background.place(x=0, y=0)
    self._manage_accounts_page = manage_accounts_page
    self._new_accounts_page = new_accounts_page
    self._system_analytics_page = system_analytics_page

    # New password page
    # Username Label
    self._username_display_label = Label(new_password_page, text="Username:")
    self._username_display_label.grid(column=0, row=0, padx=(0,300), pady=(15,0))
    self._username_display = Label(new_password_page, textvar="")  # Add username variable
    self._username_display.grid(column=0, row=1)
    
    # Enter new password
    self._new_pass_label = Label(new_password_page, text="Enter new password:")
    self._new_pass_label.grid(column=0, row=2, padx=(0,180), pady=(30,0))
    self._new_pass_entry = Entry(new_password_page, width=30)
    self._new_pass_entry.grid(column=0, row=3)

    # Confirm new password
    self._confirm_new_pass_label = Label(new_password_page, text="Confirm new password:")
    self._confirm_new_pass_label.grid(column=0, row=4, padx=(0,150), pady=(30,0))
    self._confirm_new_pass_entry = Entry(new_password_page, width=30)
    self._confirm_new_pass_entry.grid(column=0, row=5)

    # Confirm Button
    self._confirm_button = Button(new_password_page, text="Confirm")
    self._confirm_button.grid(column=0, row=6, pady=(25,0), padx=(0,200))

    # Cancel Button
    new_page_submit_button = Button(new_password_page, text = "Cancel", command =self._go_to_manage_accounts)
    new_page_submit_button.grid(row = 6, column = 0, pady=(25,0), padx=(200,0))
    
    # This creates the text object which
    # can be placed on to the frame.

    
    login_page_title = Label(login_page,text="Login Page", font = 25)
    login_page_title.grid(row=1, column=2, pady=(155,0))

        #ImageTk.PhotoImage(Image.open("logo.png"))  # Sets logo to 'logo.png'
        #panel = Label(self._root, image="logo")  # Sets panel to the image
        #panel.pack()
    self._login_page_ID_text = Label(login_page, text="User ID:")
    self._login_page_ID_text.grid(row=2, column=1, pady=(5,0))
                            
    self._login_page_name_entry = Entry(login_page)
    self._login_page_name_entry.grid(row = 2, column = 2, pady=(5,0))


    self._login_page_pass_text= Label(login_page, text="Password:")
    self._login_page_pass_text.grid(row = 3, column = 1)

    self._login_page_pass_entry = Entry(login_page, show="*")
    self._login_page_pass_entry.grid(row = 3, column = 2)
    self._login_page_error_label = Label(login_page, text="", fg = "red")
    
    self._login_page_error_label.grid(row=5, column=2)

    self._login_page_submit_button = Button(login_page, text = "Submit", command = self._login_page_submit)
    self._login_page_submit_button.grid(row = 4, column = 2)

    self._login_page_name_entry.bind("<Return>", self._focus_on_password)
    self._login_page_pass_entry.bind("<Return>", self._login_page_submit)
    # This places the object onto the frame
    # using rows and columns.
    
    
    self._login_page = login_page

    # Make a Booking page
    make_booking = self._create_page()
    self._make_booking = make_booking
    # Contents of the page
    # Current date and time
    
    
    # Start date input box
    self._start_date_label = Label(make_booking, text="Start date:")
    self._start_date_label.grid(row=0, column=0, padx=(0,0), pady=(15,0))

    self._start_date_entry=DateEntry(make_booking, selectmode='day', date_pattern="DD/MM/YYYY")
    self._start_date_entry.grid(row=1, column=0, padx=15)
    
    # End date input box
    self._end_date_label = Label(make_booking, text="End date:")
    self._end_date_label.grid(row=0, column=1, padx=(0,0), pady=(15,0))
    
    self._end_date_entry=DateEntry(make_booking, selectmode='day', date_pattern="DD/MM/YYYY")
    self._end_date_entry.grid(row=1, column=1, padx=15)

    # Check in time box
    self._check_in_label = Label(make_booking, text="Check in time:")
    self._check_in_label.grid(row=2, column=0, padx=(0,0), pady=(15,0))
    # Hour
    check_in_hour = tkinter.StringVar(value="0")
    self._check_in_time_hour = tkinter.Spinbox(make_booking, from_=0, to=23, textvariable=check_in_hour, wrap=True, width=3)
    self._check_in_time_hour.grid(row=3, column=0, padx=(0,50))
    
    self._in_hour_label = Label(make_booking, text="Hour")
    self._in_hour_label.grid(row=3, column=0, padx=(0,50), pady=(45,0))
    
    # Minute
    check_in_min = tkinter.StringVar(value=0)
    self._check_in_time_min = tkinter.Spinbox(make_booking, from_=0, to=59, textvariable=check_in_min, wrap=True, width=3)
    self._check_in_time_min.grid(row=3, column=0, padx=(50,0))
    
    self._in_min_label = Label(make_booking, text="Min")
    self._in_min_label.grid(row=3, column=0, padx=(50,0), pady=(45,0))
    
    # Check out time box
    self._check_out_label = Label(make_booking, text="Check out time:")
    self._check_out_label.grid(row=2, column=1, padx=(0,0), pady=(15,0))
    # Hour
    check_out_hour = tkinter.StringVar(value="0")
    self._check_out_time_hour = tkinter.Spinbox(make_booking, from_=0, to=23, textvariable=check_out_hour, wrap=True, width=3)
    self._check_out_time_hour.grid(row=3, column=1, padx=(0,50))
    
    self._out_hour_label = Label(make_booking, text="Hour")
    self._out_hour_label.grid(row=3, column=1, padx=(0,50), pady=(45,0))
    
    # Minute
    check_out_min = tkinter.StringVar(value=0)
    self._check_out_time_min = tkinter.Spinbox(make_booking, from_=0, to=59, textvariable=check_out_min, wrap=True, width=3)
    self._check_out_time_min.grid(row=3, column=1, padx=(50,0))
    
    self._out_min_label = Label(make_booking, text="Min")
    self._out_min_label.grid(row=3, column=1, padx=(50,0), pady=(45,0))
    
    # Booking details box
    # Start and end date
    start_date = tkinter.Label(make_booking, textvar=self._start_date_entry.get())
    start_date.grid(row=4, column=0)  # Start
    end_date = tkinter.Label(make_booking, textvar=self._end_date_entry.get())
    end_date.grid(row=4, column=1)  # End

    # Check in time
    check_in_time = tkinter.Label(make_booking, textvar=self._check_in_time_hour.get()+self._check_in_time_min.get())
    check_in_time.grid(row=4, column=0)  # Hour

    # Check out time
    check_in_time = tkinter.Label(make_booking, textvar=self._check_in_time_hour.get())
    check_in_time.grid(row=4, column=0)  # Hour
    check_out_time = tkinter.Label(make_booking, textvar=self._check_in_time_min.get())
    check_out_time.grid(row=4, column=1)  # Minute
    
    # Book Button
    book_button = tkinter.Button(make_booking, text= "Book",command="", height=1, anchor='w')
    book_button.grid(column=0, row=6, pady=50)

    # Check Button
    check_button = tkinter.Button(make_booking, text= "Check",command=self._check_booking_availability, height=1, anchor='w')
    check_button.grid(column=1, row=6, pady=50)
        
    # Exit button
    return_menu = tkinter.Button(make_booking, text= "Return To Menu",command=self._go_to_main_menu, height=1, anchor='w')
    return_menu.grid(column=2, row=6, pady=50)
    
    
    # Main menu page
    main_menu = self._create_page()
    img_label_main_menu = Label(main_menu, image=img)
    img_label_main_menu.place(x=0, y=0)
    # Contents of the page
    # View booking button
    view_booking_button = tkinter.Button(main_menu, text="  View Bookings", command="", height=1, width=20, font=fnt.Font(size=25), anchor='w')
    view_booking_button.grid(column=0, row=2, padx=5, pady=(145, 3))

    # Make a booking button
    make_a_booking_button = tkinter.Button(main_menu, text="  Make a Booking", command=self._go_to_make_booking, height=1, width=20, font=fnt.Font(size=25), anchor='w')
    make_a_booking_button.grid(column=0, row=4, padx=5, pady=3)

    # Admin panel button
    admin_panel_button = tkinter.Button(main_menu, text="  Admin panel", command=self._open_admin_panel, height=1, width=20, font=fnt.Font(size=25), anchor='w')
    admin_panel_button.grid(column=0, row=5, padx=5, pady=3)
    self._admin_page = admin_page
    # Log out button
    log_out_button = tkinter.Button(main_menu, text="  Log out", command=self._logout, height=1, width=20, font=fnt.Font(size=25), anchor='w')
    log_out_button.grid(column=0, row=6, padx=5, pady=3)

    

    admin_true = tkinter.Label(main_menu, text="Loading", font=('Helvetica', 12), fg='green')
    admin_true.grid(row=1, column=3, padx=(274, 0))

    self._admin_label = admin_true
    
    self._menu.add_command(label="Exit Program", command=self.close)
    self._main_menu = main_menu

#admin page    
    
    manage_bookings = tkinter.Button(admin_page, text = "Manage Bookings", command="", height=1, width=20, font=fnt.Font(size=25), anchor='w')
    
    manage_bookings.grid(column=0, row=3, padx=5, pady=3)
    

    manage_accounts = tkinter.Button(admin_page, text= "Manage Accounts",  command=self._go_to_manage_accounts, height=1, width=20, font=fnt.Font(size=25), anchor='w')
    manage_accounts.grid(column=0, row=4, padx=5, pady=3)

    system_analytics = tkinter.Button(admin_page, text= "System Analytics",command=self._open_system_analytics, height=1, width=20, font=fnt.Font(size=25), anchor='w')
    system_analytics.grid(column=0, row=5, padx=5, pady=3)
    
    return_menu = tkinter.Button(admin_page, text= "Return To Menu",command=self._go_to_main_menu, height=1, width=20, font=fnt.Font(size=25), anchor='w')
    return_menu.grid(column=0, row=6, padx=5, pady=3)
    self._admin_page = admin_page


    # Manage accounts
    img_label_manage_accounts = Label(manage_accounts_page, image=img)
    img_label_manage_accounts.place(x=0, y=0, relwidth=1, relheight=1)
    admin_accounts_label = tkinter.Label(manage_accounts_page, text = "Admin Accounts")
    admin_accounts_label.grid(column = 0, row = 0, padx=60, pady=(25,0))

    guest_accounts_label = tkinter.Label(manage_accounts_page, text = "Guest Accounts")
    guest_accounts_label.grid(column = 1, row=0, padx=60, pady=(25,0))

    admin_variable = StringVar(manage_accounts_page)
    admin_variable.set(management.UserManager.admin_usernames()[0]) # default value
    guest_variable = StringVar(manage_accounts_page)
    guest_variable.set(management.UserManager.guest_usernames()[0])
    
    admins_from_db = management.UserManager.admin_usernames()
    admin_list = Listbox(manage_accounts_page, height=3)
    for i in admins_from_db:
      admin_list.insert(END, i)
    admin_list.grid(column = 0, row = 1, padx=(0,0), pady=(20,0))
    self._admin_list = admin_list
    guests_from_db = management.UserManager.guest_usernames()
    guest_list = Listbox(manage_accounts_page, height=3)
    self._guest_list = guest_list
    for i in guests_from_db:
      guest_list.insert(END, i)
      
    guest_list.grid(column = 1, row=1, padx=(0,0), pady=(20,0))

    


      
    new_account_button = tkinter.Button(manage_accounts_page, text="New", command=self._go_to_edit_accounts)  
    new_account_button.grid(column=0, row=2, padx = (150,0), pady = 60)
    
    delete_account_button = tkinter.Button(manage_accounts_page, text="Delete", command=self._remove_account_action)
    delete_account_button.grid(column=0, row = 2, padx = (0,150), pady = 60)

    new_password_button = tkinter.Button(manage_accounts_page, text = "New Password", command=self._go_to_new_password_page)
    new_password_button.grid(column =1, row = 2, padx = (0,230), pady= (60))
    
    return_to_menu = tkinter.Button(manage_accounts_page, text= "Exit", command=self._go_to_main_menu, anchor='w')
    return_to_menu.grid(column=1, row = 2, padx = (250,0), pady = 60)
    self._booking_availability = tkinter.Label(self._make_booking, text="")
      #new account page

    new_page_ID_text = Label(new_accounts_page, text="Enter New User ID:")
    new_page_ID_text.grid(row=0, column=1)
                            
    new_page_name_entry = Entry(new_accounts_page,text = "")
    new_page_name_entry.grid(row = 0, column = 2)

    new_page_pass_text= Label(new_accounts_page, text="Enter New Password:")
    new_page_pass_text.grid(row = 1, column = 1)

    new_page_pass_entry = Entry(new_accounts_page, text = "")
    new_page_pass_entry.grid(row = 1, column = 2)

    menu_button = tkinter.Button(new_accounts_page, text= "Exit", command=self._go_to_main_menu, anchor='w')
    menu_button.grid(column=1, row=2)

    new_page_submit_button = Button(new_accounts_page, text = "Submit", command = self._new_account_page_submit)
    new_page_submit_button.grid(row = 4, column = 2)

    
    

   # new_user_name = new_page_name_entry.get()
   # new_user = management.User("Username", new_user_name, permission_level=2,)
    #success = management.UserManager.create(self._user, new_user, "password")
    self._select_page(self._login_page)
    self._root.mainloop()




    

if __name__ == "__main__":
  database = storage.Database("database")
  management.setup(database)
  application = Application()
