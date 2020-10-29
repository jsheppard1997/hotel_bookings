# hotel_bookings

This app takes the dataframe 'hotel_bookings.csv' and finds all bookings on a given date and the following 7 days. It also finds the total adults, children and babies in the same time period.


There are two versions of this app:

- 'hotel_terminal.py' runs from command line

- 'hotel_gui.py' that has a tkinter interface







TO RUN THE COMMAND LINE VERSION

To run this code type 'python hotel_terminal.py' into terminal.

A file selector window will appear. 

Pick the 'hotel_bookings.csv' - if any other file picked, the application will ask you to select another file.

The user will then be prompted to put a date in YYYY-MM-DD - if any other format given, they will be prompted again.

If a valid date is given, two files are created:

[date = date entered above]

- 'bookings_' + date : Shows all bookings currently active or starting in next 7 days

- 'total_adults_children_babies' + date : Shows total adults, children and babies active or starting in next 7 days. 







TO RUN THE TKINTER INTERFACE

To run this code type 'python hotel_gui.py' into terminal.     

The interface will pop up - fill in the form as prompted.


