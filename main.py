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
      
    
  def _login_page_submit(self, event=None):
    username = self._login_page_name_entry.get()
    password = self._login_page_pass_entry.get()

    self._login_page_name_entry.delete(0, END)
    self._login_page_pass_entry.delete(0, END)
    user = None
    try:
      user = management.User.login(username, password)
    except management.FailedToLoginToUser as error:
      box.showerror("Login Failed", error)
      self._login_page_name_entry.focus()
      return
    except:
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
  
  def __init__(self):
    self._pages = []
    self._db = None
    self._root = Tk()
    self._root.geometry(f"{self._app_size_x}x{self._app_size_y}") # Sets size of window
    self._menu = Menu(self._root, tearoff=0)
    self._root.title('Booking System')  # Set name of window
    # Set background
    img = PhotoImage(file="windowbackground.png")  # Select background image
    
    self._root.config(menu=self._menu)
    self._root.resizable(False, False) # Prevents window resizing

    # Login page
    # Login Page is just a frame
    # instance from tkinter
    login_page = self._create_page() 
    admin_page = self._create_page()
    make_booking_page = self._create_page()
    manage_accounts_page = self._create_page()
    self._manage_accounts_page = manage_accounts_page
    
    
    # This creates the text object which
    # can be placed on to the frame.
    
    login_page_title = Label(login_page,text="Login Page", font = 25)




        #ImageTk.PhotoImage(Image.open("logo.png"))  # Sets logo to 'logo.png'
        #panel = Label(self._root, image="logo")  # Sets panel to the image
        #panel.pack()
    self._login_page_ID_text = Label(login_page, text="User ID:")
    self._login_page_ID_text.grid(row=0, column=1)
                            
    self._login_page_name_entry = Entry(login_page)
    self._login_page_name_entry.grid(row = 0, column = 2)


    self._login_page_pass_text= Label(login_page, text="Password:")
    self._login_page_pass_text.grid(row = 1, column = 1)

    self._login_page_pass_entry = Entry(login_page)
    self._login_page_pass_entry.grid(row = 1, column = 2)
    self._login_page_error_label = Label(login_page, text="", fg = "red")
    
    self._login_page_error_label.grid(row=3, column=2)

    self._login_page_submit_button = Button(login_page, text = "Submit", command = self._login_page_submit)
    self._login_page_submit_button.grid(row = 2, column = 2)

    self._login_page_name_entry.bind("<Return>", self._focus_on_password)
    self._login_page_pass_entry.bind("<Return>", self._login_page_submit)
    # This places the object onto the frame
    # using rows and columns.
    
    login_page_title.grid(row=1, column=1, columnspan=3)
    
    self._login_page = login_page

    # Make a Booking page
    img_x, img_y = 0,0
    make_booking = self._create_page()
    self._make_booking = make_booking
    img_label_make_booking = Label(make_booking, image=img)
    img_label_make_booking.place(x=img_x, y=img_y)
    # Contents of the page
    # Current date and time

    
    # Start date input box
    self._start_date_label = Label(make_booking, text="Start date:")
    self._start_date_label.grid(row=0, column=1, padx=(150,0), pady=(15,0))

    self._start_data_entry=DateEntry(make_booking, selectmode='day', date_pattern="DD/MM/YYYY")
    self._start_data_entry.grid(row=1, column=1, padx=15)
    
    # End date input box
    self._end_date_label = Label(make_booking, text="End date:")
    self._end_date_label.grid(row=0, column=2, padx=(150,0), pady=(15,0))
    
    self._start_data_entry=DateEntry(make_booking, selectmode='day', date_pattern="DD/MM/YYYY")
    self._start_data_entry.grid(row=1, column=2, padx=15)

    # Check in time box
    
    
    # Check out time box
    
    
    # Booking details box
    
    
    # Available or Unavailable status
    
    
    # Book Button
    
        
    # Exit button
    
    
    
    # Main menu page
    img_x, img_y = 0,0
    main_menu = self._create_page()
    img_label_main_menu = Label(main_menu, image=img)
    img_label_main_menu.place(x=img_x, y=img_y)
    # Contents of the page
    # View booking button
    view_booking_button = tkinter.Button(main_menu, text="  View Bookings", command="", height=1, width=20, font=fnt.Font(size=25), anchor='w')
    view_booking_button.grid(column=0, row=2, padx=5, pady=(160, 3))

    # Make a booking button
    make_a_booking_button = tkinter.Button(main_menu, text="  Make a Booking", command=self._go_to_make_booking, height=1, width=20, font=fnt.Font(size=25), anchor='w')
    make_a_booking_button.grid(column=0, row=4, padx=5, pady=3)

    # Admin panel button
    admin_panel_button = tkinter.Button(main_menu, text="  Admin panel", command= lambda: self._select_page(admin_page), height=1, width=20, font=fnt.Font(size=25), anchor='w')
    admin_panel_button.grid(column=0, row=5, padx=5, pady=3)

    # Log out button
    log_out_button = tkinter.Button(main_menu, text="  Log out", command=self._logout, height=1, width=20, font=fnt.Font(size=25), anchor='w')
    log_out_button.grid(column=0, row=6, padx=5, pady=3)

    

    admin_true = tkinter.Label(main_menu, text="Loading", font=('Helvetica', 12), fg='green')
    admin_true.grid(row=1, column=3, padx=(274, 0))

    self._admin_label = admin_true
    
    self._menu.add_command(label="Exit Program", command=self.close)
    self._main_menu = main_menu

    self._select_page(main_menu)

#admin page    
    
    manage_bookings = tkinter.Button(admin_page, text = "Manage Bookings", command="", height=1, width=20, font=fnt.Font(size=25), anchor='w')
    manage_bookings.grid(column=0, row=3, padx=5, pady=3)
    

    manage_accounts = tkinter.Button(admin_page, text= "Manage Accounts",  command=self._go_to_manage_accounts, height=1, width=20, font=fnt.Font(size=25), anchor='w')
    manage_accounts.grid(column=0, row=4, padx=5, pady=3)

    return_menu = tkinter.Button(admin_page, text= "Return To Menu",command=self._go_to_main_menu, height=1, width=20, font=fnt.Font(size=25), anchor='w')
    return_menu.grid(column=0, row=5, padx=5, pady=3)

    self._admin_page = admin_page


    
    img_label_manage_accounts = Label(manage_accounts_page, image=img)
    img_label_manage_accounts.place(x=img_x, y=img_y)
    admin_accounts_label = tkinter.Label(manage_accounts_page, text = "Admin Accounts")
    admin_accounts_label.grid(column = 0, row = 0, padx=150, pady=(25,0))

    guest_accounts_label = tkinter.Label(manage_accounts_page, text = "Guest Accounts")
    guest_accounts_label.grid(column = 1, row=0, padx=150, pady=(25,0))

    admin_variable = StringVar(manage_accounts_page)
    admin_variable.set(management.UserManager.admin_usernames()[0]) # default value
    guest_variable = StringVar(manage_accounts_page)
    guest_variable.set(management.UserManager.admin_usernames()[0])
    

    admin_list = OptionMenu(manage_accounts_page, admin_variable,   management.UserManager.admin_usernames)
    admin_list.grid(column = 0, row = 1, padx = 150, pady= 30)
    self._root.mainloop()

    guest_list = OptionMenu(manage_accounts_page, guest_variable, management.UserManager.guest_usernames)
    guest_list.grid(column = 0, row = 1, padx = 150, pady = 30 )

    new_account_button = tkinter.Button(manage_accounts_page, text="New", command="")
    new_account_button.grid(column=0, row = 2, padx = 180, pady = 60)

    edit_account_button = tkinter.Button(manage_accounts_page, text="Edit", command="")
    edit_account_button.grid(column=0, row = 2, padx = 140, pady = 60)

    

if __name__ == "__main__":
  database = storage.Database("database")
  management.setup(database)
  
  
  application = Application()




