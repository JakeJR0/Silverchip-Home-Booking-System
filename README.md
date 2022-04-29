# Silverchip Home Booking System
[![Python Application](https://github.com/JakeJR0/Silverchip-Home-Booking-System/actions/workflows/python-app.yml/badge.svg)](https://github.com/JakeJR0/Silverchip-Home-Booking-System/actions/workflows/python-app.yml)
[![codecov](https://codecov.io/gh/JakeJR0/Silverchip-Home-Booking-System/branch/main/graph/badge.svg?token=NSBRVLBD3H)](https://codecov.io/gh/JakeJR0/Silverchip-Home-Booking-System)
[![Pylint](https://github.com/JakeJR0/Silverchip-Home-Booking-System/actions/workflows/pylint.yml/badge.svg)](https://github.com/JakeJR0/Silverchip-Home-Booking-System/actions/workflows/pylint.yml)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
## Table of contents:
- [About](#about)
- [Project Brief](#project-brief)
- [Authors](#authors)
- [The Booking System](#the-booking-system)


## About
A booking system for a single location holiday home. Features included are:
- Log in system
- Make new Bookings
- View bookings
- Manage bookings
- Manage Accounts
- Create and delete accounts


The Booking System Project is designed to help administrators to book holidays for the guests.
Branded with the Silverchip logo the "Holiday Home Booking System" was developed by the [Authors](#authors) 
credited below during their work placement at Silverchip.

## Project Brief

### Project Scenario
Holiday Home Booking System

Our client has a holiday home and is looking to build a booking system that they can use to manage the property.
You are tasked with designing, developing and testing the platform.

### Key Requirements

The key requirements are as follows (One administration system as bookings are always taken over the phone):

1) Be able to book a stay at the property<br>
  a) Due to cleaning, there must be a gap of 6 hours between a booking ending and one starting.<br>
  b) Bookings on the weekend can only be made for Friday to Sunday unless there is less that 2 weeks before the 
date where we allow smaller breaks.<br>
  c) Bookings can be made 18 months in advance<br>

2) For the booking to be confirmed we need to capture, full name, address, phone number and email of the person making the booking.<br>

4) The pricing is as follows:<br>
  a) Jan-April-£125 per night<br>
  b) May-August-£200 per night<br>
  c) September-December-£150 per night<br>
  d) Pets are also an additional £25 per pet (Max 2 pets)<br>
  
4) A place where we can see the current viewings<br>

#### Optional Extra Features

1) The ability for each user to have a login (And an administrator account to add new logins)<br>
2) Ability to edit bookings<br>
3) Ability to cancel bookings<br>


## The booking system
Bookings can be made up to 18 months in advance and no further. There are no restrictions on booking on dates in the past as if the user
wanted to store past bookings that were made prior to the system being available, then storing bookings in the past allows for there
to be a digital archive.

Bookings over the weekend can't be made if the booking start date is within 2 weeks of booking, as requested by the brief.


## Viewing Bookings
The view bookings system is accessible to both the admin and guest user accounts. All the details of the booking, including the price 
are displayed in this section. The information is displayed in 'Label' and can not be edited.


## Manage Bookings
The same idea as the view booking system however with the one major difference of each detail except the price, which is automatically
updated by the system when a change is made, can be altered by the user. The same data validation as the make a booking system applies 
to the changes made to the bookings.


## Manage Accounts
Accounts split into two lists, the 'Admin Accounts' list and the 'Guest Accounts' list. The admin with access to this page can: create 
new accounts, delete existing ones and create new passwords for existings accounts.


## Account types
There are 2 account types: Guest and Admin. Admins have access to the Admin Panel, which allows the user to manage bookings and accounts.
Guests can only view and create new bookings. The admin has the same permissions as the guest and can access the same thing however with 
the extra access mentioned above.


## Permanent Admin Account
Hard-coded into the code, an admin account exists even when deleted in the account page and whenthe database is deleted.
Username: System
Password: root
This account exists to ensure the program can't lock every user out and it remains functional.

## Authors
- [JakeJR0](https://github.com/JakeJR0)
- [MitchStreet](https://github.com/MitchStreet)
- [Alezu23](https://github.com/Alezu23)
