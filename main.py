# Silverchip Holiday Home Booking Program
# Designed and programmed by: Alex Unsworth, Mitchell Street
# and Jake James-Robinson

# Import Python modules
import tkinter
import tkinter.font as fnt
from tkinter import *
from tkinter import messagebox as box
import management
import storage
from tkcalendar import DateEntry


class InvalidPageParent(ValueError):
    # This is used to provide a custom error if the user is providing an
    # invalid parent when creating a new page.
    pass


class ApplicationError(ValueError):
    pass


# Contains the entire GUI and its functions


class Application:
    _app_size_x = 800
    _app_size_y = 500

    @property
    def app_size(self):
        return (self._app_size_x, self._app_size_y)

    @property
    def app_size_x(self):
        return (self._app_size_x,)

    @property
    def app_size_y(self):
        return (self._app_size_y,)

    @app_size.setter
    def app_size(self, value=()):
        try:
            x = int(value[0])
            y = int(value[0])
        except AttributeError:
            raise ApplicationError("Application size has not been provided.")
        except BaseException:
            raise ApplicationError("Application size must be an integer.")

        if y > 20 and y < 10000 and x > 20 and x < 10000:
            self._app_size_x = x
            self._app_size_y = y
            self._root.geometry(f"{x}x{y}")
        else:
            raise ApplicationError(
                "Value must be within the range of 20 - 10000 for both x and y."
            )

    @app_size_x.setter
    def app_size_x(self, value=500):
        if value > 20 and value < 10000:
            self._app_size_x = value
            self._root.geometry(f"{value}x{self._app_size_y}")
        else:
            raise ApplicationError("Value must be within the range of 20 - 10000.")

    @app_size_y.setter
    def app_size_y(self, value=250):
        if value > 20 and value < 10000:
            self._app_size_y = value
            self._root.geometry(f"{self._app_size_x}x{value}")
        else:
            raise ApplicationError("Value must be within the range of 20 - 10000.")

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

    # Focus on the password entry
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
            else:
                page.pack_forget()

    def _logout(self):  # Logs the user out of the program, returning them to login page
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
                box.showinfo(
                    "Success",
                    "You have been successfully logged out of the application.",
                )
        except Exception as error:
            box.showerror("Internal Error", error)

    def _add_new_account(
        self, admin_user=management.User, user=management.User, password=""
    ):
        if not admin_user.logged_in:
            return

        if user.level < admin_user.level:
            result = management.UserManager.create(admin_user, user, password)
            if result:
                if user.level == 1:
                    self._admin_list.insert(END, user.username)
                elif user.level == 2:
                    self._guest_list.insert(END, user.username)

    # Saves all information edited on the edit booking page
    def _save_edit_booking(self):
        booking = self._booking_manage_instance
        try:
            booking.start.date = self._edit_selected_start_date_output.get()

            booking.end.date = self._edit_selected_end_date_output.get()

            booking.start.hour = int(self._edit_selected_check_in_output_hour.get())
            booking.start.minute = int(self._edit_selected_check_in_output_minute.get())
            booking.user.postcode = self._edit_selected_postcode_output.get()
            booking.end.hour = int(self._edit_selected_check_out_output_hour.get())
            booking.end.min = int(self._edit_selected_check_out_output_minute.get())
            booking.user.name = self._edit_selected_full_name_output.get()
            value = self._edit_selected_phone_number_output.get()
            booking.user.phone_number = value
            booking.user.email = self._edit_selected_email_output.get()
            booking.user.pets = int(self._edit_selected_pet_amount_output.get())

        except management.FormattedUserError as e:
            box.showwarning("User Data Error", e)
            return
        except management.FormattedTimeAndDateError as e:
            box.showwarning("Date and Time Error", e)
            return
        except:
            pass

        try:
            success = booking.save()
        except management.BookingSaveError as e:
            box.showerror("Booking Save Error", e)
            return

        if success:
            box.showinfo("Booking Saved", "The booking has been successfully saved.")
            self._view_booking_manage = None
            self._go_to_main_menu()
        else:
            box.showwarning("Booking Error", "Booking failed to save.")

    # This saves all the information entered in the booking page
    # to the database
    def _book_stay(self):
        start_date = self._start_date_entry.get_date()
        start_date_hour = self
        end_date = self._end_date_entry.get_date()
        if start_date >= end_date:
            box.showerror(
                "Booking Error",
                "The start date cannot be after or the same as the end date.",
            )

        try:
            start_date = str(start_date).replace("-", "/")
            start_date = "{}/{}/{}".format(
                start_date[8:10], start_date[5:7], start_date[0:4]
            )

            end_date = str(end_date).replace("-", "/")
            end_date = "{}/{}/{}".format(end_date[8:10], end_date[5:7], end_date[0:4])

            hour = self._check_in_hour.get()
            mins = self._check_in_min.get()

            start_date = management.FormattedTimeAndDate(
                start_date, int(hour), int(mins)
            )
            end_date = management.FormattedTimeAndDate(end_date, int(18), int(0))

        except management.IncorrectFormattedDateAndTime as e:
            box.showwarning("Date Provided is invalid", e)
        except Exception as e:
            print(e)

        # Recieves the phone number from the entry box and validates it.
        phone_number = self._phone_number_entry.get()
        found_issue_number = False
        for i in phone_number:
            if not i.isnumeric():
                box.showwarning(
                    "Phone Number",
                    "The phone number provided includes invalid characters.",
                )
                found_issue_number = True
                break
        if found_issue_number:
            return
        elif len(phone_number) != 11:
            box.showwarning(
                "Phone Number",
                "The phone number provided is {} numbers long it should be 11.".format(
                    len(phone_number)
                ),
            )
            return

        # Recieves the email from the entry box and validates it.
        email_entry = self._email_entry.get()
        at_count = 0
        dot_count = 0
        invalid_count = 0
        for c in email_entry:
            if c == "@":
                at_count += 1
            elif c == ".":
                dot_count += 1
            elif c == " ":
                invalid_count += 1
        if invalid_count > 0:
            box.showerror("Error", "Please enter a valid email address")
            return
        elif dot_count > 2:
            box.showerror("Error", "Please enter a valid email address")
            return
        elif at_count > 1:
            box.showerror("Error", "Please enter a valid email address")
            return

        pet_amount = self._pet_amount.get()

        if int(pet_amount) > 2:
            box.showerror("Error", "Please enter a pet number less than 2")
            return
        elif int(pet_amount) < 0:
            box.showerror("Error", "Please enter a valid pet number")
            return

        # Recieves the address from the entry box.
        address_entry = self._address_entry.get()

        if len(address_entry) > 8:
            box.showerror("Error", "Please enter a valid postcode...")
            return
        elif len(address_entry) < 6:
            box.showerror("Error", "Please enter a valid postcode...")
            return
        first_name, last_name = None, None
        try:
            first_name, last_name = self._full_name_entry.get().split(" ", 2)
        except ValueError as e:
            if e == "too many values to unpack (expected 2)":
                box.showwarning(
                    "Name Error", "Please provided both your first and last name."
                )

        user_data = None
        try:

            user_data = management.FormattedUserBookingData(
                first_name,
                last_name,
                address_entry,
                email_entry,
                phone_number,
                pet_amount,
            )
        except:
            pass

        if management.BookingManagement.booking_available(start_date, end_date):
            booking = management.Booking(start_date, end_date, user_data, create=True)
        box.showinfo("Booking Complete", "You have made a booking...")
        self._go_to_main_menu()

    def _get_account(self):
        account = {"type": None, "name": None, "position": None}

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
        new_user_pass = self._new_page_pass_entry.get()

        if len(new_user_name) >= 16:
            box.showwarning(
                """Username is too large, please choose a username
                under 16 characters."""
            )
            return
        elif len(new_user_name) <= 3:

            box.showwarning(
                "Username Error",
                """Username is too short, please choose a longer username.
                (3 + Characters)""",
            )
            return

        if len(new_user_pass) >= 16:
            box.showwarning(
                "Password Error",
                """Password is too large, please choose a password
                under 16 characters.""",
            )
            return
        elif len(new_user_pass) <= 3:
            box.showwarning(
                "Password Error",
                """Password is too short, please choose a longer password.
                (8 + Characters)""",
            )
            return

        new_user = management.User(new_user_name, permission_level=2)
        success = management.UserManager.create(self._user, new_user, new_user_pass)
        creation_successful = tkinter.Label(
            main_menu,
            text="Account Creation Successful",
            font=("Helvetica", 12),
            fg="green",
        )
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

    # these go to different sections of code when called

    def _go_to_manage_accounts(self, event=None):
        self._select_page(self._manage_accounts_page)

    def _go_to_edit_accounts(self, event=None):
        booking = self._booking_manage_instance

        self._select_page(self._new_accounts_page)

    def _go_to_new_password_page(self, event=None):
        self._select_page(self._new_password_page)

    def _go_to_view_booking_page(self, event=None):
        if not self._user.admin and not self._user.super_admin:
            box.showwarning(
                "Access Denied", "You are not authorised to access this area."
            )
            return

        self._bookings_list.delete(0, END)

        bookings = management.BookingManagement.get_bookings()
        self._bookings_list_list = []
        for i in bookings:
            self._bookings_list.insert(END, str(i))
            self._bookings_list_list.append(i)

        self._select_page(self._view_booking_page)

    def _set_edit_selected_with_booking(self, booking=management.Booking):
        def format_time(time=""):
            if int(time) <= 9:
                time = "0{}".format(time)
            else:
                time = str(time)

            return time

        def format_price(price=0.0):
            new_price = "{:.2f}".format(price)
            return new_price

        self._edit_selected_start_date_output.insert(
            END, booking.start.date.strftime("%d/%m/%Y")
        )
        self._edit_selected_end_date_output.insert(
            END, booking.end.date.strftime("%d/%m/%Y")
        )

        self._edit_selected_check_in_output_hour.insert(
            END, format_time(booking.start.hour)
        )
        self._edit_selected_check_in_output_minute.insert(END, booking.start.minute)
        self._edit_selected_check_out_output_hour.insert(
            END, format_time(booking.end.hour)
        )
        self._edit_selected_check_out_output_minute.insert(
            END, format_time(booking.end.minute)
        )
        self._edit_selected_full_name_output.insert(END, "{}".format(booking.user.name))
        self._edit_selected_email_output.insert(END, "{}".format(booking.user.email))
        self._edit_selected_postcode_output.insert(END, booking.user.postcode)
        self._edit_selected_pet_amount_output.insert(
            END, "{}".format(booking.user.pets)
        )
        self._edit_selected_phone_number_output.insert(END, booking.user.phone_number)
        self._edit_selected_price_output.config(
            text="£{}".format(format_price(booking.cost))
        )

    def _set_edit_selected_to_empty(self):
        self._edit_selected_start_date_output.delete(0, END)
        self._edit_selected_end_date_output.delete(0, END)
        self._edit_selected_check_in_output_hour.delete(0, END)
        self._edit_selected_check_in_output_minute.delete(0, END)
        self._edit_selected_check_out_output_hour.delete(0, END)
        self._edit_selected_check_out_output_minute.delete(0, END)
        self._edit_selected_full_name_output.delete(0, END)
        self._edit_selected_email_output.delete(0, END)
        self._edit_selected_postcode_output.delete(0, END)
        self._edit_selected_pet_amount_output.delete(0, END)
        self._edit_selected_price_output.config(text="")

    def _edit_selected_booking_delete(self):
        booking = None

        for i in self._manage_bookings_list.curselection():
            booking = self._manage_bookings_list_list[i]

        if booking is None:
            box.showwarning("No Booking Selected", "Please select a booking to view.")

        success = booking.delete()

        if success:
            box.showinfo("Success", "Successfully deleted booking.")
        else:  # JJ
            box.showwarning("Failed", "Failed to delete booking.")

        self._go_to_main_menu()

    def _go_to_edit_selected_booking_page(self, event=None):
        booking = None

        for i in self._manage_bookings_list.curselection():
            booking = self._manage_bookings_list_list[i]

        if booking is None:
            box.showwarning("No Booking Selected", "Please select a booking to view.")
            return
        self._booking_manage_instance = booking
        self._set_edit_selected_to_empty()
        self._set_edit_selected_with_booking(booking)

        self._select_page(self._edit_selected_booking)

    def _go_to_manage_booking_page(self, event=None):
        if not self._user.admin and not self._user.super_admin:
            box.showwarning(
                "Access Denied", "You are not authorised to access this area."
            )
            return

        self._manage_bookings_list.delete(0, END)

        bookings = management.BookingManagement.get_bookings()
        self._manage_bookings_list_list = []

        for i in bookings:
            self._manage_bookings_list.insert(END, str(i))
            self._manage_bookings_list_list.append(i)

        self._select_page(self._manage_booking_page)

    def _hide_booking_status_message(self, event=None):
        self._booking_availability.config(text="")

    def _check_booking_availability(self, event=None):
        make_booking = self._make_booking
        booking_available = True
        start_date = self._start_date_entry.get_date()
        end_date = self._end_date_entry.get_date()

        start_date = str(start_date).replace("-", "/")
        start_date = "{}/{}/{}".format(
            start_date[8:10], start_date[5:7], start_date[0:4]
        )

        end_date = str(end_date).replace("-", "/")
        end_date = "{}/{}/{}".format(end_date[8:10], end_date[5:7], end_date[0:4])

        start_date = management.FormattedTimeAndDate(start_date)
        end_date = management.FormattedTimeAndDate(end_date)
        booking_available = management.BookingManagement.booking_available(
            start_date, end_date
        )
        # Available or Unavailable status

        if booking_available:
            self._booking_availability.config(text="Booking available", fg="green")
        if not booking_available:
            self._booking_availability.config(text="Booking unavailable", fg="red")
        else:
            self._booking_availability.config(
                text="Checking availability...", fg="yellow"
            )

        self._booking_availability.after(3000, self._hide_booking_status_message)

    def _create_account_action(self):
        new_account_permission_level = self._new_page_level.get()
        level = 0
        if new_account_permission_level == "Guest":
            level = 1
        elif new_account_permission_level == "Admin":
            level = 2
        else:
            level = 10

        # This sets the permission level of a user

        new_account_username = self._new_page_name_entry.get()
        new_account_password = self._new_page_pass_entry.get()

        # This takes the username and password input
        self._new_page_name_entry.delete(0, END)
        self._new_page_pass_entry.delete(0, END)

        # This deletes the username and password input

        new_user = management.User(new_account_username, new_account_password, level)

        # This adds a new user
        success = management.UserManager.create(
            self._user, new_user, new_account_password
        )

        # This adds the new user to the database
        if success:
            box.showinfo(
                "User Created",
                """User {} with password {} has been created with
                level {} access.""".format(
                    new_account_username,
                    new_account_password,
                    new_account_permission_level,
                ),
            )
            # This confirms that the user has been created

            if level == 1:
                self._guest_list.insert(END, new_account_username)
            elif level == 2:
                self._admin_list.insert(END, new_account_username)

            self._go_to_manage_accounts()

        # This goes back to the manage accounts page

    def _remove_account_action(self):
        account_details = self._get_account()
        user_to_remove = management.User(account_details["name"])

        # This gets the account the user wishes to remove

        result = False

        try:
            result = management.UserManager.remove_user(self._user, user_to_remove)

        # This removes the account
        except management.PermissionDenied as reason:
            box.showwarning("Permission Denied", reason)

        # This tells the user if an account could not be removed
        except:
            pass

        if result:
            if account_details["type"] == "guest":
                self._guest_list.delete(account_details["position"])
            elif account_details["type"] == "admin":
                self._admin_list.delete(account_details["position"])

            # This deletes the account

    def _view_booking_view(self):
        booking = None

        for i in self._bookings_list.curselection():
            booking = self._bookings_list_list[i]

        if booking is None:
            box.showwarning("No Booking Selected", "Please select a booking to view.")
            return

        def format_time(time=""):
            if int(time) <= 9:
                time = "0{}".format(time)
            else:
                time = str(time)

            return time

        def format_price(price=0.0):
            new_price = "{:.2f}".format(price)
            print(price)
            return new_price

        self._view_selected_start_date_output.config(
            text=booking.start.date.strftime("%d/%m/%Y")
        )
        self._view_selected_end_date_output.config(
            text=booking.end.date.strftime("%d/%m/%Y")
        )
        self._view_selected_check_in_output.config(
            text="{}:{}".format(
                format_time(booking.start.hour), format_time(booking.start.minute)
            )
        )
        self._view_selected_check_out_output.config(
            text="{}:{}".format(
                format_time(booking.end.hour), format_time(booking.end.minute)
            )
        )
        self._view_selected_full_name_output.config(text="{}".format(booking.user.name))
        self._view_selected_email_output.config(text="{}".format(booking.user.email))
        self._view_selected_postcode_output.config(text=booking.user.postcode)
        self._view_selected_pet_amount_output.config(
            text="{}".format(booking.user.pets)
        )
        self._view_selected_phone_number_output.config(text=booking.user.phone_number)
        self._view_selected_price_output.config(
            text="£{}".format(format_price(booking.cost))
        )

        self._select_page(self._view_selected_booking)

    def _view_booking_manage(self):
        booking = None

        for i in self._manage_bookings_list.curselection():
            booking = self._manage_bookings_list_list[i]

        if booking is None:
            box.showwarning("No Booking Selected", "Please select a booking to view.")
            return

        def format_time(time=""):
            if int(time) <= 9:
                time = "0{}".format(time)
            else:
                time = str(time)

            return time

        def format_price(price=0.0):
            new_price = "{:.2f}".format(price)
            return new_price

        self._view_selected_start_date_output.config(
            text=booking.start.date.strftime("%d/%m/%Y")
        )
        self._view_selected_end_date_output.config(
            text=booking.end.date.strftime("%d/%m/%Y")
        )
        self._view_selected_check_in_output.config(
            text="{}:{}".format(
                format_time(booking.start.hour), format_time(booking.start.minute)
            )
        )
        self._view_selected_check_out_output.config(
            text="{}:{}".format(
                format_time(booking.end.hour), format_time(booking.end.minute)
            )
        )
        self._view_selected_full_name_output.config(text="{}".format(booking.user.name))
        self._view_selected_email_output.config(text="{}".format(booking.user.email))
        self._view_selected_postcode_output.config(text=booking.user.postcode)
        self._view_selected_pet_amount_output.config(
            text="{}".format(booking.user.pets)
        )
        self._view_selected_phone_number_output.config(text=booking.user.phone_number)
        self._view_selected_price_output.config(
            text="£{}".format(format_price(booking.cost))
        )

        self._select_page(self._view_selected_booking)

    def _open_admin_panel(self):
        print("Username: {} Level: {}".format(self._user.username, self._user.level))
        if self._user.level > 1:
            self._select_page(self._admin_page)
        else:
            box.showwarning(
                "Access Denied", "You are not authorised to access this area."
            )

    def _open_system_analytics(self):
        self._select_page(self._system_analytics_page)
        print("Opened")

    def __init__(self, test_mode=False):
        self._pages = []
        self._db = None
        self._root = Tk()
        bg = PhotoImage(file="background.png")
        self._root.geometry(
            f"{self._app_size_x}x{self._app_size_y}"
        )  # Sets size of window
        self._menu = Menu(self._root, tearoff=0)
        self._menu.add_command(
            label="Return to main menu",
            command=lambda: self._select_page(self._main_menu),
        )
        self._root.title("Booking System")  # Set name of window
        # Set background
        if not test_mode:
            img = PhotoImage(file="background.png")  # Select background image
            background = tkinter.Label(self._root, image=img)

        self._root.config(menu=self._menu)
        self._root.resizable(False, False)  # Prevents window resizing

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
        view_booking_page = self._create_page()
        self._edit_selected_booking = self._create_page()
        self._view_selected_booking = self._create_page()
        view_selected_booking = self._view_selected_booking
        edit_selected_booking = self._edit_selected_booking

        manage_booking_page = self._create_page()
        self._view_booking_page = view_booking_page
        self._manage_booking_page = manage_booking_page
        if not test_mode:
            background.place(x=0, y=0)
        self._manage_accounts_page = manage_accounts_page
        self._new_accounts_page = new_accounts_page
        self._system_analytics_page = system_analytics_page

        # New password page
        # Username Label
        self._username_display_label = tkinter.Label(
            new_password_page, text="Username:"
        )
        self._username_display_label.grid(column=0, row=0, padx=(0, 300), pady=(15, 0))
        self._username_display = tkinter.Label(
            new_password_page, textvar=""
        )  # Add username variable
        self._username_display.grid(column=0, row=1)

        # Enter new password
        self._new_pass_label = tkinter.Label(
            new_password_page, text="Enter new password:"
        )
        self._new_pass_label.grid(column=0, row=2, padx=(0, 180), pady=(30, 0))
        self._new_pass_entry = tkinter.Entry(new_password_page, width=30, show="*")
        self._new_pass_entry.grid(column=0, row=3)

        # Confirm new password
        self._confirm_new_pass_label = tkinter.Label(
            new_password_page, text="Confirm new password:"
        )
        self._confirm_new_pass_label.grid(column=0, row=4, padx=(0, 150), pady=(30, 0))
        self._confirm_new_pass_entry = tkinter.Entry(new_password_page, width=30)
        self._confirm_new_pass_entry.grid(column=0, row=5)

        # Confirm Button
        self._confirm_button = tkinter.Button(new_password_page, text="Confirm")
        self._confirm_button.grid(column=0, row=6, pady=(25, 0), padx=(0, 200))

        # Cancel Button
        new_page_submit_button = tkinter.Button(
            new_password_page, text="Cancel", command=self._go_to_manage_accounts
        )
        new_page_submit_button.grid(row=6, column=0, pady=(25, 0), padx=(200, 0))

        # This creates the text object which
        # can be placed on to the frame.

        login_page_title = tkinter.Label(login_page, text="Login Page", font=25)
        login_page_title.grid(row=1, column=2, pady=(155, 0))

        # ImageTk.PhotoImage(Image.open("logo.png"))  # Sets logo to 'logo.png'
        # panel = tkinter.Label(self._root, image="logo")  # Sets panel to the image
        # panel.pack()
        self._login_page_ID_text = tkinter.Label(login_page, text="User ID:")
        self._login_page_ID_text.grid(row=2, column=1, pady=(5, 0))

        self._login_page_name_entry = tkinter.Entry(login_page)
        self._login_page_name_entry.grid(row=2, column=2, pady=(5, 0))

        self._login_page_pass_text = tkinter.Label(login_page, text="Password:")
        self._login_page_pass_text.grid(row=3, column=1)

        self._login_page_pass_entry = tkinter.Entry(login_page, show="*")
        self._login_page_pass_entry.grid(row=3, column=2)
        self._login_page_error_label = tkinter.Label(login_page, text="", fg="red")

        self._login_page_error_label.grid(row=5, column=2)

        self._login_page_submit_button = tkinter.Button(
            login_page, text="Submit", command=self._login_page_submit
        )
        self._login_page_submit_button.grid(row=4, column=2)

        self._login_page_name_entry.bind("<Return>", self._focus_on_password)
        self._login_page_pass_entry.bind("<Return>", self._login_page_submit)

        placeholder_label1 = tkinter.Label(login_page, text="")
        placeholder_label1.place(anchor="nw")

        placeholder_label2 = tkinter.Label(login_page, text="")
        placeholder_label2.place(anchor="ne")

        placeholder_label3 = tkinter.Label(login_page, text="")
        placeholder_label3.place(anchor="sw")

        placeholder_label4 = tkinter.Label(login_page, text="")
        placeholder_label4.place(anchor="se")

        # This places the object onto the frame
        # using rows and columns.

        self._login_page = login_page

        # Make a Booking page
        make_booking = self._create_page()
        self._make_booking = make_booking
        # Contents of the page
        # Current date and time

        # Start date input box
        self._bookings_list_list = []
        self._manage_booking_list_list = []
        self._start_date_label = tkinter.Label(make_booking, text="Start date:")
        self._start_date_label.grid(row=0, column=0, padx=(0, 0), pady=(15, 0))

        self._start_date_entry = DateEntry(
            make_booking, selectmode="day", date_pattern="DD/MM/YYYY"
        )
        self._start_date_entry.grid(row=1, column=0, padx=15)

        # End date input box
        self._end_date_label = tkinter.Label(make_booking, text="End date:")
        self._end_date_label.grid(row=0, column=1, padx=(0, 0), pady=(15, 0))

        self._end_date_entry = DateEntry(
            make_booking, selectmode="day", date_pattern="DD/MM/YYYY"
        )
        self._end_date_entry.grid(row=1, column=1, padx=15)

        # Check in time box
        self._check_in_label = tkinter.Label(make_booking, text="Check in time:")
        self._check_in_label.grid(row=3, column=0, padx=(0, 0), pady=(0, 45))
        # Hour
        check_in_hour = tkinter.StringVar(value="0")

        self._check_in_time_hour = tkinter.Spinbox(
            make_booking, from_=0, to=23, textvariable=check_in_hour, wrap=True, width=3
        )
        self._check_in_time_hour.grid(row=3, column=0, padx=(0, 50))

        self._in_hour_label = tkinter.Label(make_booking, text="Hour")
        self._in_hour_label.grid(row=3, column=0, padx=(0, 50), pady=(45, 0))

        # Minute
        check_in_min = tkinter.StringVar(value=0)
        self._check_in_time_min = tkinter.Spinbox(
            make_booking, from_=0, to=59, textvariable=check_in_min, wrap=True, width=3
        )
        self._check_in_time_min.grid(row=3, column=0, padx=(50, 0))
        self._check_in_min = check_in_min
        self._check_in_hour = check_in_hour

        self._in_min_label = tkinter.Label(make_booking, text="Min")
        self._in_min_label.grid(row=3, column=0, padx=(50, 0), pady=(45, 0))

        # Check out time box
        self._check_out_label = tkinter.Label(make_booking, text="Check out time:")
        self._check_out_label.grid(row=3, column=1, padx=(0, 0), pady=(0, 45))
        # Hour
        check_out_hour = tkinter.StringVar(value="0")
        self._check_out_time_hour = tkinter.Spinbox(
            make_booking,
            from_=0,
            to=23,
            textvariable=check_out_hour,
            wrap=True,
            width=3,
        )
        self._check_out_time_hour.grid(row=3, column=1, padx=(0, 50))

        self._out_hour_label = tkinter.Label(make_booking, text="Hour")
        self._out_hour_label.grid(row=3, column=1, padx=(0, 50), pady=(45, 0))

        # Minute
        check_out_min = tkinter.StringVar(value=0)
        self._check_out_time_min = tkinter.Spinbox(
            make_booking, from_=0, to=59, textvariable=check_out_min, wrap=True, width=3
        )
        self._check_out_time_min.grid(row=3, column=1, padx=(50, 0))

        self._out_min_label = tkinter.Label(make_booking, text="Min")
        self._out_min_label.grid(row=3, column=1, padx=(50, 0), pady=(45, 0))

        # Start and end date
        start_date = tkinter.Label(make_booking, textvar=self._start_date_entry.get())
        start_date.grid(row=4, column=0)  # Start
        end_date = tkinter.Label(make_booking, textvar=self._end_date_entry.get())
        end_date.grid(row=4, column=1)  # End

        # Check in time
        check_in_time = tkinter.Label(
            make_booking,
            textvar=self._check_in_time_hour.get() + self._check_in_time_min.get(),
        )
        check_in_time.grid(row=4, column=0)  # Hour

        # Check out time
        check_in_time = tkinter.Label(
            make_booking, textvar=self._check_in_time_hour.get()
        )
        check_in_time.grid(row=4, column=0)  # Hour
        check_out_time = tkinter.Label(
            make_booking, textvar=self._check_in_time_min.get()
        )
        check_out_time.grid(row=4, column=1)  # Minute

        # Information input
        # Name input
        full_name_entry_label = tkinter.Label(make_booking, text="Full name:")

        full_name_entry_label.grid(row=6, column=0, padx=(0, 110))
        full_name_entry = tkinter.Entry(make_booking)
        self._full_name_entry = full_name_entry
        full_name_entry.grid(row=7, column=0)

        # Address input
        address_entry_label = tkinter.Label(make_booking, text="Postcode:")
        address_entry_label.grid(row=6, column=1, padx=(0, 115))
        address_entry = tkinter.Entry(make_booking)
        address_entry.grid(row=7, column=1)
        self._address_entry = address_entry
        # Number input
        number_entry_label = tkinter.Label(make_booking, text="Phone number:")
        number_entry_label.grid(row=8, column=0, padx=(0, 80))
        number_entry = tkinter.Entry(make_booking)
        number_entry.grid(row=9, column=0)
        self._phone_number_entry = number_entry  # Email input
        email_label = tkinter.Label(make_booking, text="Email:")
        email_label.grid(row=8, column=1, padx=(0, 135))
        email_entry = tkinter.Entry(make_booking)
        email_entry.grid(row=9, column=1)
        self._email_entry = email_entry
        # Amount of pets input
        pet_amount = tkinter.StringVar(value=0)
        pet_amount_label = tkinter.Label(make_booking, text="Number of pets:")
        pet_amount_label.grid(column=1, row=8, padx=(380, 0))
        pet_amount_entry = tkinter.Spinbox(
            make_booking, from_=0, to=2, textvariable=pet_amount, wrap=True, width=3
        )
        pet_amount_entry.grid(column=1, row=9, padx=(300, 0))
        self._pet_amount = pet_amount_entry

        # Book Button
        book_button = tkinter.Button(
            make_booking, text="Book", command=self._book_stay, height=1, anchor="w"
        )

        book_button.grid(column=0, row=10, pady=50, padx=(0, 100))

        # Check Button
        check_button = tkinter.Button(
            make_booking,
            text="Check",
            command=self._check_booking_availability,
            height=1,
            anchor="w",
        )
        check_button.grid(column=0, row=10, pady=50, padx=(100, 0))

        # Exit button
        return_menu = tkinter.Button(
            make_booking,
            text="Return To Menu",
            command=self._go_to_main_menu,
            height=1,
            anchor="w",
        )
        return_menu.grid(column=1, row=10, pady=50)

        # View booking page
        # Contents of Page
        bookings_list_label = tkinter.Label(
            view_booking_page, text="Please select a booking:"
        )
        bookings_list_label.grid(column=0, row=0)

        bookings_list = tkinter.Listbox(view_booking_page, height=15, width=50)
        bookings_list.grid(column=0, row=1)
        self._bookings_list = bookings_list
        view_button = tkinter.Button(
            view_booking_page, text="View", command=self._view_booking_view
        )
        view_button.grid(column=0, row=2, padx=(0, 290), pady=15)

        exit_button = tkinter.Button(
            view_booking_page,
            text="Exit",
            command=lambda: self._select_page(self._main_menu),
        )
        exit_button.grid(column=0, row=2, padx=(290, 0), pady=15)
        # Manage booking page
        # Contents of Page
        bookings_list_label = tkinter.Label(
            manage_booking_page, text="Please select a booking:"
        )
        bookings_list_label.grid(column=0, row=0)

        bookings_list = tkinter.Listbox(manage_booking_page, height=15, width=50)
        bookings_list.grid(column=0, row=1)
        self._manage_bookings_list = bookings_list
        view_button = tkinter.Button(
            manage_booking_page, text="View", command=self._view_booking_manage
        )
        view_button.grid(column=0, row=2, padx=(0, 400), pady=15)

        edit_button = tkinter.Button(
            manage_booking_page,
            text="Edit",
            command=self._go_to_edit_selected_booking_page,
        )
        edit_button.grid(column=0, row=2, padx=(0, 145), pady=15)

        delete_button = tkinter.Button(
            manage_booking_page,
            text="Delete",
            command=self._edit_selected_booking_delete,
        )
        delete_button.grid(column=0, row=2, padx=(145, 0), pady=15)

        exit_button = tkinter.Button(
            manage_booking_page,
            text="Exit",
            command=lambda: self._select_page(self._main_menu),
        )
        exit_button.grid(column=0, row=2, padx=(400, 0), pady=15)

        # Main menu page
        main_menu = self._create_page()
        if not test_mode:
            img_label_main_menu = tkinter.Label(main_menu, image=img)
            img_label_main_menu.place(x=0, y=0)

        # Contents of the page
        # View booking button
        view_booking_button = tkinter.Button(
            main_menu,
            text="  View Bookings",
            command=self._go_to_view_booking_page,
            height=1,
            width=20,
            font=fnt.Font(size=25),
            anchor="w",
        )
        view_booking_button.grid(column=0, row=2, padx=5, pady=(145, 3))

        # Make a booking button
        make_a_booking_button = tkinter.Button(
            main_menu,
            text="  Make a Booking",
            command=self._go_to_make_booking,
            height=1,
            width=20,
            font=fnt.Font(size=25),
            anchor="w",
        )
        make_a_booking_button.grid(column=0, row=4, padx=5, pady=3)

        # Admin panel button
        admin_panel_button = tkinter.Button(
            main_menu,
            text="  Admin panel",
            command=self._open_admin_panel,
            height=1,
            width=20,
            font=fnt.Font(size=25),
            anchor="w",
        )
        admin_panel_button.grid(column=0, row=5, padx=5, pady=3)
        self._admin_page = admin_page
        # Log out button
        log_out_button = tkinter.Button(
            main_menu,
            text="  Log out",
            command=self._logout,
            height=1,
            width=20,
            font=fnt.Font(size=25),
            anchor="w",
        )
        log_out_button.grid(column=0, row=6, padx=5, pady=3)

        admin_true = tkinter.Label(
            main_menu, text="Loading", font=("Helvetica", 12), fg="green"
        )
        admin_true.grid(row=1, column=3, padx=(10, 0))

        self._admin_label = admin_true

        self._menu.add_command(label="Exit Program", command=self.close)
        self._main_menu = main_menu

        # View Selected Booking
        # Contents of the page
        # Start date
        start_date_label = tkinter.Label(view_selected_booking, text="Start date:")
        start_date_label.grid(column=0, row=0, padx=(0, 140), pady=(30, 0))
        start_date_output = tkinter.Label(
            view_selected_booking, textvar=""
        )  # add variable
        start_date_output.grid(column=0, row=1, padx=(0, 140))
        self._view_selected_start_date_output = start_date_output

        # End date
        end_date_label = tkinter.Label(view_selected_booking, text="End date:")
        end_date_label.grid(column=1, row=0, padx=(140, 0), pady=(30, 0))
        end_date_output = tkinter.Label(
            view_selected_booking, textvar=""
        )  # add variable
        end_date_output.grid(column=1, row=1, padx=(140, 0))
        self._view_selected_end_date_output = end_date_output

        # Check in time
        check_in_label = tkinter.Label(view_selected_booking, text="Check in time:")
        check_in_label.grid(column=0, row=2, padx=(0, 140), pady=(30, 0))
        check_in_output = tkinter.Label(
            view_selected_booking, textvar=""
        )  # add variable
        check_in_output.grid(column=0, row=3, padx=(0, 140))
        self._view_selected_check_in_output = check_in_output

        # Check out time
        check_out_label = tkinter.Label(view_selected_booking, text="Check out time:")
        check_out_label.grid(column=1, row=2, padx=(140, 0), pady=(30, 0))
        check_out_output = tkinter.Label(
            view_selected_booking, textvar=""
        )  # add variable
        check_out_output.grid(column=1, row=3, padx=(140, 0))
        self._view_selected_check_out_output = check_out_output

        # Full name
        full_name_label = tkinter.Label(view_selected_booking, text="Full name:")
        full_name_label.grid(column=0, row=4, padx=(0, 140), pady=(30, 0))
        full_name_output = tkinter.Label(
            view_selected_booking, textvar=""
        )  # add variable
        full_name_output.grid(column=0, row=5, padx=(0, 140))
        self._view_selected_full_name_output = full_name_output

        # Postcode
        postcode_label = tkinter.Label(view_selected_booking, text="Postcode:")
        postcode_label.grid(column=1, row=4, padx=(140, 0), pady=(30, 0))
        postcode_output = tkinter.Label(
            view_selected_booking, textvar=""
        )  # add variable
        postcode_output.grid(column=1, row=5, padx=(140, 0))
        self._view_selected_postcode_output = postcode_output

        # Phone number
        phone_number_label = tkinter.Label(view_selected_booking, text="Phone number:")
        phone_number_label.grid(column=0, row=6, padx=(0, 140), pady=(30, 0))
        phone_number_output = tkinter.Label(
            view_selected_booking, textvar=""
        )  # add variable
        phone_number_output.grid(column=0, row=7, padx=(0, 140))
        self._view_selected_phone_number_output = phone_number_output

        # Email
        email_label = tkinter.Label(view_selected_booking, text="Email:")
        email_label.grid(column=1, row=6, padx=(140, 0), pady=(30, 0))
        email_output = tkinter.Label(view_selected_booking, textvar="")  # add variable
        email_output.grid(column=1, row=7, padx=(140, 0))
        self._view_selected_email_output = email_output

        # Number of pets
        pet_amount_label = tkinter.Label(view_selected_booking, text="Number of pets:")
        pet_amount_label.grid(column=0, row=8, padx=(0, 140), pady=(30, 0))
        pet_amount_output = tkinter.Label(
            view_selected_booking, textvar=""
        )  # add variable
        pet_amount_output.grid(column=0, row=9, padx=(0, 140))
        self._view_selected_pet_amount_output = pet_amount_output

        # Price
        price_label = tkinter.Label(view_selected_booking, text="Price:")
        price_label.grid(column=1, row=8, padx=(140, 0), pady=(30, 0))
        price_output = tkinter.Label(view_selected_booking, textvar="")  # add variable
        price_output.grid(column=1, row=9, padx=(140, 0))
        self._view_selected_price_output = price_output

        # Save button - not needed on this page
        # save_button = tkinter.Button(edit_selected_booking, text="Save", command="")
        # save_button.grid(column=0,row=10,padx=(0,140))

        # Exit button
        exit_button = tkinter.Button(
            view_selected_booking, text="Exit", command=self._go_to_main_menu
        )
        exit_button.grid(column=1, row=10, padx=(140, 0), pady=(30, 0))

        # Edit Selected Booking
        # Contents of the page
        # Start date
        start_date_label = tkinter.Label(edit_selected_booking, text="Start date:")
        start_date_label.grid(column=0, row=0, padx=(0, 140), pady=(30, 0))
        start_date_output = DateEntry(
            edit_selected_booking, selectmode="day", date_pattern="DD/MM/YYYY"
        )
        start_date_output.grid(column=0, row=1, padx=(0, 140))
        self._edit_selected_start_date_output = start_date_output

        # End date
        end_date_label = tkinter.Label(edit_selected_booking, text="End date:")
        end_date_label.grid(column=1, row=0, padx=(140, 0), pady=(30, 0))
        end_date_output = DateEntry(
            edit_selected_booking, selectmode="day", date_pattern="DD/MM/YYYY"
        )
        end_date_output.grid(column=1, row=1, padx=(140, 0))
        self._edit_selected_end_date_output = end_date_output

        # Check in time
        check_in_label = tkinter.Label(edit_selected_booking, text="Check in time:")
        check_in_label.grid(column=0, row=2, padx=(0, 140), pady=(30, 0))

        check_in_hour = tkinter.StringVar(0)
        check_in_hour_output = tkinter.Spinbox(
            edit_selected_booking,
            from_=0,
            to=23,
            textvariable=check_in_hour,
            wrap=True,
            width=3,
        )  # add variable
        check_in_hour_output.grid(column=0, row=3, padx=(0, 190))

        check_in_min = tkinter.StringVar(0)
        check_in_min_output = tkinter.Spinbox(
            edit_selected_booking,
            from_=0,
            to=59,
            textvariable=check_in_min,
            wrap=True,
            width=3,
        )
        check_in_min_output.grid(column=0, row=3, padx=(0, 80))

        self._edit_selected_check_in_output_hour = check_in_hour_output
        self._edit_selected_check_in_output_minute = check_in_min_output

        # Check out time
        check_out_label = tkinter.Label(edit_selected_booking, text="Check out time:")
        check_out_label.grid(column=1, row=2, padx=(140, 0), pady=(30, 0))

        check_out_hour = tkinter.StringVar(0)
        check_out_hour_output = tkinter.Spinbox(
            edit_selected_booking,
            from_=0,
            to=23,
            textvariable=check_out_hour,
            wrap=True,
            width=3,
        )  # add variable
        check_out_hour_output.grid(column=1, row=3, padx=(80, 0))

        check_out_min = tkinter.StringVar(0)
        check_out_min_output = tkinter.Spinbox(
            edit_selected_booking,
            from_=0,
            to=59,
            textvariable=check_out_min,
            wrap=True,
            width=3,
        )
        check_out_min_output.grid(column=1, row=3, padx=(190, 0))

        self._edit_selected_check_out_output_hour = check_out_hour_output
        self._edit_selected_check_out_output_minute = check_out_min_output

        # Full name
        full_name_label = tkinter.Label(edit_selected_booking, text="Full name:")
        full_name_label.grid(column=0, row=4, padx=(0, 140), pady=(30, 0))
        full_name_output = tkinter.Entry(
            edit_selected_booking, textvar=""
        )  # add variable
        full_name_output.grid(column=0, row=5, padx=(0, 140))
        self._edit_selected_full_name_output = full_name_output

        # Postcode
        postcode_label = tkinter.Label(edit_selected_booking, text="Postcode:")
        postcode_label.grid(column=1, row=4, padx=(140, 0), pady=(30, 0))
        postcode_output = tkinter.Entry(
            edit_selected_booking, textvar=""
        )  # add variable
        postcode_output.grid(column=1, row=5, padx=(140, 0))
        self._edit_selected_postcode_output = postcode_output

        # Phone number
        phone_number_label = tkinter.Label(edit_selected_booking, text="Phone number:")
        phone_number_label.grid(column=0, row=6, padx=(0, 140), pady=(30, 0))
        phone_number_output = tkinter.Entry(
            edit_selected_booking, textvar=""
        )  # add variable
        phone_number_output.grid(column=0, row=7, padx=(0, 140))
        self._edit_selected_phone_number_output = phone_number_output

        # Email
        email_label = tkinter.Label(edit_selected_booking, text="Email:")
        email_label.grid(column=1, row=6, padx=(140, 0), pady=(30, 0))
        email_output = tkinter.Entry(edit_selected_booking, textvar="")  # add variable
        email_output.grid(column=1, row=7, padx=(140, 0))
        self._edit_selected_email_output = email_output

        # Number of pets
        pet_amount = tkinter.StringVar(0)
        pet_amount_label = tkinter.Label(edit_selected_booking, text="Number of pets:")
        pet_amount_label.grid(column=0, row=8, padx=(0, 140), pady=(30, 0))
        pet_amount_output = tkinter.Spinbox(
            edit_selected_booking,
            from_=0,
            to=2,
            textvariable=pet_amount,
            wrap=True,
            width=3,
        )  # add variable
        pet_amount_output.grid(column=0, row=9, padx=(0, 140))
        self._edit_selected_pet_amount_output = pet_amount_output

        # Price
        price_label = tkinter.Label(edit_selected_booking, text="Price:")
        price_label.grid(column=1, row=8, padx=(140, 0), pady=(30, 0))
        price_output = tkinter.Label(edit_selected_booking, textvar="")  # add variable
        price_output.grid(column=1, row=9, padx=(140, 0))
        self._edit_selected_price_output = price_output

        # Save button
        save_button = tkinter.Button(
            edit_selected_booking, text="Save", command=self._save_edit_booking
        )  # Alex
        save_button.grid(column=0, row=10, padx=(0, 140), pady=(30, 0))

        # Exit button
        exit_button = tkinter.Button(
            edit_selected_booking, text="Exit", command=self._go_to_main_menu
        )
        exit_button.grid(column=1, row=10, padx=(140, 0), pady=(30, 0))

        # admin page

        manage_bookings = tkinter.Button(
            admin_page,
            text="Manage Bookings",
            command=self._go_to_manage_booking_page,
            height=1,
            width=20,
            font=fnt.Font(size=25),
            anchor="w",
        )

        manage_bookings.grid(column=0, row=3, padx=5, pady=3)

        manage_accounts = tkinter.Button(
            admin_page,
            text="Manage Accounts",
            command=self._go_to_manage_accounts,
            height=1,
            width=20,
            font=fnt.Font(size=25),
            anchor="w",
        )
        manage_accounts.grid(column=0, row=4, padx=5, pady=3)

        return_menu = tkinter.Button(
            admin_page,
            text="Return To Menu",
            command=self._go_to_main_menu,
            height=1,
            width=20,
            font=fnt.Font(size=25),
            anchor="w",
        )
        return_menu.grid(column=0, row=6, padx=5, pady=3)
        self._admin_page = admin_page

        # Manage accounts
        if not test_mode:
            img_label_manage_accounts = tkinter.Label(manage_accounts_page, image=img)
            img_label_manage_accounts.place(x=0, y=0, relwidth=1, relheight=1)
        admin_accounts_label = tkinter.Label(
            manage_accounts_page, text="Admin Accounts"
        )
        admin_accounts_label.grid(column=0, row=0, padx=60, pady=(25, 0))

        guest_accounts_label = tkinter.Label(
            manage_accounts_page, text="Guest Accounts"
        )
        guest_accounts_label.grid(column=1, row=0, padx=60, pady=(25, 0))

        admin_variable = tkinter.StringVar(manage_accounts_page)
        admin_variable.set(management.UserManager.admin_usernames()[0])  # default value
        guest_variable = tkinter.StringVar(manage_accounts_page)
        guest_variable.set(management.UserManager.guest_usernames()[0])

        admins_from_db = management.UserManager.admin_usernames()
        admin_list = tkinter.Listbox(manage_accounts_page, height=3)
        for i in admins_from_db:
            admin_list.insert(END, i)
        admin_list.grid(column=0, row=1, padx=(0, 0), pady=(20, 0))
        self._admin_list = admin_list
        guests_from_db = management.UserManager.guest_usernames()
        guest_list = tkinter.Listbox(manage_accounts_page, height=3)
        self._guest_list = guest_list
        for i in guests_from_db:
            guest_list.insert(END, i)

        guest_list.grid(column=1, row=1, padx=(0, 0), pady=(20, 0))

        new_account_button = tkinter.Button(
            manage_accounts_page, text="New", command=self._go_to_edit_accounts
        )
        new_account_button.grid(column=0, row=2, padx=(150, 0), pady=60)

        # This button takes the user to the account creation page

        delete_account_button = tkinter.Button(
            manage_accounts_page, text="Delete", command=self._remove_account_action
        )
        delete_account_button.grid(column=0, row=2, padx=(0, 150), pady=60)

        # This button removes a selected account

        new_password_button = tkinter.Button(
            manage_accounts_page,
            text="New Password",
            command=self._go_to_new_password_page,
        )
        new_password_button.grid(column=1, row=2, padx=(0, 230), pady=(60))

        # This button takes the user to the account creation page

        return_to_menu = tkinter.Button(
            manage_accounts_page, text="Exit", command=self._go_to_main_menu, anchor="w"
        )
        return_to_menu.grid(column=1, row=2, padx=(250, 0), pady=60)
        self._booking_availability = tkinter.Label(self._make_booking, text="")
        self._booking_availability.grid(
            row=10, column=1, columnspan=3, padx=(0, 340), pady=(0, 15)
        )
        # new account page
        permission_level = 1
        self._new_page_level = tkinter.StringVar(new_accounts_page)
        self._new_page_level.set("Guest")
        new_page_admin_check = OptionMenu(
            new_accounts_page, self._new_page_level, *["Admin", "Guest"]
        )
        new_page_admin_check.grid(column=1, row=4)

        new_page_ID_text = tkinter.Label(new_accounts_page, text="Enter New User ID:")
        new_page_ID_text.grid(row=0, column=1)

        new_page_name_entry = tkinter.Entry(new_accounts_page, text="")
        new_page_name_entry.grid(row=0, column=2)
        self._new_page_name_entry = new_page_name_entry

        new_page_pass_text = tkinter.Label(
            new_accounts_page, text="Enter New Password:"
        )
        new_page_pass_text.grid(row=1, column=1)

        new_page_pass_entry = tkinter.Entry(new_accounts_page, text="")
        new_page_pass_entry.grid(row=1, column=2)
        self._new_page_pass_entry = new_page_pass_entry

        menu_button = tkinter.Button(
            new_accounts_page, text="Exit", command=self._go_to_main_menu, anchor="w"
        )
        menu_button.grid(column=1, row=2)

        new_page_submit_button = tkinter.Button(
            new_accounts_page, text="Submit", command=self._create_account_action
        )
        new_page_submit_button.grid(row=4, column=2)

        # This wont work needs to be in a function / hooked to access
        # self._user

        # new_user_name = new_page_name_entry.get()
        # new_user = management.User("Username", new_user_name,
        #                               permission_level=2,)
        # success = management.UserManager.create(self._user, new_user,
        #                                           "password")
        self._select_page(self._login_page)
        print(
            "Booking Count: {}".format(management.BookingManagement.booking_count())
        )  # DELETE THIS
        self._booking_manage_instance = None

        if not test_mode:
            self._root.mainloop()


if __name__ == "__main__":
    database = storage.Database("database")
    management.setup(database)
    application = Application()
