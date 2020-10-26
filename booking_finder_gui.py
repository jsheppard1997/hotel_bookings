import tkinter as tk
from tkinter import filedialog, font, PhotoImage
from tkcalendar import Calendar,DateEntry
import os

from tkinter import filedialog, messagebox, ttk

import pandas as pd

from datetime import datetime, timedelta

root = tk.Tk()

s = ttk.Style()
s.theme_use('clam')

HEIGHT = 500
WIDTH = 600

canvas = tk.Canvas(root, height= HEIGHT, width = WIDTH)
canvas.pack()


def browsefunc():
    filename = filedialog.askopenfilename(title="Select A File")
    label_file["text"] = filename


def load_data():
    """If the file selected is valid this will load the file into the Treeview"""
    file_path = label_file["text"]
    date = entry.get()
    date = datetime.strptime(date, '%Y-%m-%d')

    try:
        filename = r"{}".format(file_path)
        if filename[-4:] == ".csv":
            bookings_df = pd.read_csv(filename)
        else:
            bookings_df = pd.read_excel(filename)

    except ValueError:
        tk.messagebox.showerror("Information", "The file you have chosen is invalid")
        return None
    except FileNotFoundError:
        tk.messagebox.showerror("Information", f"No such file as {file_path}")
        return None

    bookings_df['arrival_date'] = pd.to_datetime(bookings_df[['arrival_date_year', 
                                                                'arrival_date_month', 
                                                                'arrival_date_day_of_month']].astype(str).sum(axis=1), 
                                                                format='%Y%B%d')





    bookings_df = bookings_df[bookings_df['is_canceled'] == 0]

    bookings_df['total_days_stayed'] = pd.to_timedelta(bookings_df['stays_in_weekend_nights'] + bookings_df['stays_in_week_nights'], unit="D")

    bookings_df['leaving_date'] = bookings_df['arrival_date'] + bookings_df['total_days_stayed']



    final_df_mask = ((bookings_df['arrival_date'] <= date) & (date <= bookings_df['leaving_date'])) | ((date <= bookings_df['arrival_date'])  & (bookings_df['arrival_date'] <= (date + timedelta(days=7)) ))

    df = bookings_df.loc[final_df_mask]

    df.to_csv("bookings" + str(date.date()) + ".csv", index=False)

    df = df.head(100)

    total_df = df[['adults', 'children', 'babies']].sum(axis=0) 

    total_df.to_csv("guests" + str(date.date()) + ".csv", index=False)

    generator["text"] = " Dataframes created:\n bookings" + str(date.date()) + ".csv\n guests" + str(date.date()) + ".csv"










background_label = tk.Label(root, background = "#d8dfde")
background_label.place(relwidth = 1, relheight=1)


BACKGROUND_COLOUR = "#fffafa"


top_frame = tk.Frame(root, bd=10, background = BACKGROUND_COLOUR)
top_frame.place(relx=0.5, rely=0.05, relwidth=0.9, relheight=0.15, anchor = 'n')

text = "Hotel Bookings Dataframe Creator"

heading = tk.Label(top_frame, bd = 4, text=text, justify='center', font = ("TkDefaultFont", 30), bg = BACKGROUND_COLOUR, fg = "#0c0d0e")
heading.place(relwidth = 1, relheight=1)

frame = tk.Frame(root, bd=10, background = BACKGROUND_COLOUR) 
frame.place( relx = 0.5, rely = 0.2, relwidth = 0.90,  relheight= 0.1, anchor = 'n')

select_button_img = PhotoImage(file = "hotel_bookings/select.png")

select_button = tk.Button(frame, image = select_button_img, command=lambda: browsefunc())
select_button.place(relx = 0.7, relwidth= 0.3, relheight=0.9)



# The file/file path text

label_bg = tk.Label(frame, bg = '#cdc9c3', text="No File Selected", justify='center')
label_bg.place(rely=0, relx=0 , relheight=0.95, relwidth = 0.65)

label_file = tk.Label(frame, bg = 'white', text="No File Selected")
label_file.place(rely=0.07, relx=0.003, relheight=0.80, relwidth = 0.642)



middle_frame = tk.Frame(root, bd=10, background = BACKGROUND_COLOUR) 
middle_frame.place(relx=0.5, rely=0.3, relwidth = 0.90,  relheight= 0.1, anchor = 'n')

entry = DateEntry(middle_frame, year=2015, date_pattern = 'y-mm-dd', bg = '#f9f9f9',
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
entry.place(relwidth = 0.65, relheight = 1)


create_button_img = PhotoImage(file = "hotel_bookings/create.png")

button_create = tk.Button(middle_frame, image = create_button_img, command=lambda: load_data())
button_create.place(relx = 0.7, relwidth= 0.3, relheight=1)

lower_frame = tk.Frame(root, bd=10, background = BACKGROUND_COLOUR)
lower_frame.place(relx=0.5, rely=0.4, relwidth=0.9, relheight=0.17, anchor = 'n')

generator_bg = tk.Label(lower_frame, anchor = 'nw', bg = '#cdc9c3', justify = 'left', bd = 4, borderwidth = 0.5)
generator_bg.place(relwidth = 1, relheight=1)

generator = tk.Label(lower_frame, anchor = 'nw', justify = 'left', bd = 4,  bg = 'white', borderwidth = 0.5)
generator.place(relx=0.005, rely=0.04,relwidth = .99, relheight=.92)


bottom_frame = tk.Frame(root, bd=10, background = BACKGROUND_COLOUR)
bottom_frame.place(relx=0.5, rely=0.57, relwidth=0.9, relheight=0.35, anchor = 'n')

text = "This application creates two dataframes:\n'Bookings' detailing all bookings within the next 7 days. \n'Guests' stating at the total adults, children and babies in same period.\n\n To use:\n1. Upload a '.csv' file with all bookings.\n2. Pick a date\n3. Press 'Create'."

label3 = tk.Label(bottom_frame, anchor = 'nw', justify = 'left', bd = 4, text=text, bg = BACKGROUND_COLOUR)
label3.place(relwidth = 1, relheight=1)






root.mainloop()