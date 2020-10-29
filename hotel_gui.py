import os
import tkinter as tk
from tkinter import filedialog, font, filedialog, messagebox, ttk
from tkcalendar import Calendar,DateEntry
import pandas as pd
from datetime import datetime, timedelta

root = tk.Tk()

root.title('Hotel Booking Finder')
root.iconbitmap('/icon.ico')

s = ttk.Style()
s.theme_use('clam')

HEIGHT = 500
WIDTH = 600

#creating canvas for all elements to
canvas = tk.Canvas(root, height= HEIGHT, width = WIDTH)
canvas.pack()


def browsefunc():
    #this function opens a window to select a file
    file_path = filedialog.askopenfilename(title="Select A File")
    filename = r"{}".format(file_path)
    if filename[-4:] == ".csv":
        label_file["text"] = filename
    else:
        messagebox.showerror("Invalid file type", "Please pick a .csv file.")
        return browsefunc()

    


def load_data():
    #uses the file from browsefunc() and the date to find all bookings in the next 7 days
    #and the total adults, children and babies.

    #the file path
    file_path = label_file["text"]

    #the date from the form
    date = date_entry.get()
    date = datetime.strptime(date, '%Y-%m-%d')


    #combining the year, month and day columns to get into yyyy-mm-dd format.
    bookings_df['arrival_date'] = pd.to_datetime(bookings_df[['arrival_date_year', 
                                                                'arrival_date_month', 
                                                                'arrival_date_day_of_month']].astype(str).sum(axis=1), 
                                                                format='%Y%B%d')


    #removing all cancelled bookings
    bookings_df = bookings_df[bookings_df['is_canceled'] == 0]

    #combining the days stayed in the week and weekend to get the total
    bookings_df['total_days_stayed'] = pd.to_timedelta(bookings_df['stays_in_weekend_nights'] + bookings_df['stays_in_week_nights'], unit="D")

    #adding the total days stayed to the arrival to find the customer's leaving date
    bookings_df['leaving_date'] = bookings_df['arrival_date'] + bookings_df['total_days_stayed']


    #creating a mask that finds all customers who are checked-in to the hotels on the date queried
    #and all customers who are arriving within the next 7 days
    final_df_mask = ((bookings_df['arrival_date'] <= date)
                    & (date <= bookings_df['leaving_date'])) | ((date <= bookings_df['arrival_date'])  
                    & (bookings_df['arrival_date'] <= (date + timedelta(days=7)) ))

    #filtering the df to only show the entries in the mask above
    df = bookings_df.loc[final_df_mask]
    df.to_csv("bookings" + str(date.date()) + ".csv", index=False)

    #picking just the adults, childen and babies and summing to find the total count of each column
    total_df = df[['adults', 'children', 'babies']].sum(axis=0) 

    #saving as guest + date
    total_df.to_csv("guests" + str(date.date()) + ".csv", index=False)

    #showing text to indiciate the files have been created
    generator["text"] = " Dataframes created:\n bookings" + str(date.date()) + ".csv\n guests" + str(date.date()) + ".csv"




#creating a background which is just white
background = tk.Label(root, background = "white")
background.place(relwidth = 1, relheight=1)


#picking a background component for the main app
BACKGROUND_COLOUR = "#F2F2F2"


#TOP FRAME - FOR TITLE
top_frame = tk.Frame(root, 
            bd=10, 
            background = BACKGROUND_COLOUR)

top_frame.place(relx=0.5, 
                rely=0.05, 
                relwidth=0.9, 
                relheight=0.15, 
                anchor = 'n')

title = "HOTEL BOOKING FINDER"

heading = tk.Label(top_frame, 
            bd = 4, 
            text=title, 
            justify='center', 
            font = ("TkDefaultFont", 30), 
            bg = BACKGROUND_COLOUR, 
            fg = "#0c0d0e")

heading.place(relwidth = 1, 
                relheight=1)


#SELECT FRAME - FOR FILE SELECTOR AND LABEL FOR PATH

select_frame = tk.Frame(root, 
                bd=10, 
                background = BACKGROUND_COLOUR) 

select_frame.place(relx = 0.5, 
                    rely = 0.2, 
                    relwidth = 0.90,  
                    relheight= 0.1, 
                    anchor = 'n')

select_button_txt = tk.Button(select_frame, 
                    text='SELECT', 
                    justify='center', 
                    font = ("TkDefaultFont", 15), 
                    fg = "#0c0d0e", 
                    command=lambda: browsefunc())

select_button_txt.place(relx = 0.7, 
                        relwidth= 0.3, 
                        relheight=0.9)


label_bg = tk.Label(select_frame, 
                    bg = '#cdc9c3', 
                    justify='center')

label_bg.place(rely=0.14, 
                relx=0, 
                relheight=0.82, 
                relwidth = 0.65)

label_file = tk.Label(select_frame, 
            bg = 'white', 
            text="No File Selected")

label_file.place(rely=0.2, 
                    relx=0.003, 
                    relheight=0.70, 
                    relwidth = 0.642)



#MIDDLE FRAME - FOR DATE PICKER AND CREATING THE DATAFRAMES

middle_frame = tk.Frame(root,   
                bd=10, 
                background = BACKGROUND_COLOUR) 

middle_frame.place(relx=0.5, 
                    rely=0.3, 
                    relwidth = 0.90,  
                    relheight= 0.1, 
                    anchor = 'n')



date_entry = DateEntry(middle_frame, year=2015, date_pattern = 'y-mm-dd', bg = '#f9f9f9', justify='center',
                 selectbackground='gray80',
                 selectforeground='black',
                 normalbackground='white',
                 normalforeground='black',
                 background='gray90',
                 foreground='black',
                 bordercolor='gray90',
                 othermonthforeground='gray50',
                 othermonthbackground='white',
                 othermonthweforeground='gray50',
                 othermonthwebackground='white',
                 weekendbackground='white',
                 weekendforeground='black',
                 headersbackground='white',
                 headersforeground='gray70')
date_entry.place(relwidth = 0.65, relheight = 1)


button_create = tk.Button(middle_frame, text='CREATE', justify='center', font = ("TkDefaultFont", 15), fg = "#0c0d0e", command=lambda: load_data())
button_create.place(relx = 0.7, relwidth= 0.3, relheight=0.9)



#GENERATOR FRAME - TO SHOW TEXT TO INDICATE THE DATAFRAMES HAVE BEEN CREATED
generator_frame = tk.Frame(root, bd=10, background = BACKGROUND_COLOUR)
generator_frame.place(relx=0.5, rely=0.4, relwidth=0.9, relheight=0.17, anchor = 'n')

generator_bg = tk.Label(generator_frame, anchor = 'nw', bg = '#cdc9c3', justify = 'left', bd = 4, borderwidth = 0.5)
generator_bg.place(relwidth = 1, relheight=1)

generator = tk.Label(generator_frame, anchor = 'nw', justify = 'left', bd = 4,  bg = 'white', borderwidth = 0.5)
generator.place(relx=0.003, rely=0.03,relwidth = .994, relheight=.94)


#INSTRUCTIONS FRAME
instructions_frame = tk.Frame(root, bd=10, background = BACKGROUND_COLOUR)
instructions_frame.place(relx=0.5, rely=0.57, relwidth=0.9, relheight=0.35, anchor = 'n')

instructions = ("This application creates two dataframes:\n" +
        "'Bookings' detailing all bookings within the next 7 days.\n" +
        "'Guests' stating at the total adults, children and babies in same period.\n\n" +
        "Instructions:\n" +
        "1. Press ‘SELECT’ to pick a .csv file\n" +
        "2. Choose a date\n" +
        "3. Press 'CREATE'")

instructions = tk.Label(instructions_frame, 
                anchor = 'nw', 
                justify = 'center', 
                bd = 4, 
                text=instructions, 
                bg = BACKGROUND_COLOUR, 
                font = ("TkDefaultFont", 12), 
                fg = "#404040")

instructions.place(relwidth = 1, 
                    relheight=1, 
                    relx = 0.12)

root.mainloop()