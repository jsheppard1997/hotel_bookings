import tkinter as tk
from tkinter import filedialog

from tkcalendar import Calendar,DateEntry

from tkinter import filedialog, messagebox, ttk

import pandas as pd

from datetime import datetime, timedelta

root = tk.Tk()

HEIGHT = 1000
WIDTH = 1200

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

    df.to_csv("bookings_" + str(date.date()) + ".csv", index=False)

    df = df.head(100)

    total_df = df[['adults', 'children', 'babies']].sum(axis=0) 

    total_df.to_csv("total_adults_children_babies_" + str(date.date()) + ".csv", index=False)

    total_df = df.head(2)

    clear_data()

    tv1["column"] = list(df.columns)
    tv1["show"] = "headings"
    for column in tv1["columns"]:
        tv1.heading(column, text=column) # let the column heading = column name

    df_rows = df.to_numpy().tolist()
    print(df_rows) # turns the dataframe into a list of lists
    for row in df_rows:
        tv1.insert("", "end", values=row) # inserts each list into the treeview. For parameters see https://docs.python.org/3/library/tkinter.ttk.html#tkinter.ttk.Treeview.insert
    return None

    tv2["column"] = list(total_df.columns)
    tv2["show"] = "headings"
    # loop through column list for headers
    for column in tv2["column"]:
        tv2.heading(column, text = column)

    
    #put data in treeview
    df_total_rows = df_total.to_numpy.tolist()
    for row in df_total_rows:
        tv2.insert("", "end", value=row)








def clear_data():
    tv1.delete(*tv1.get_children())
    tv2.delete(*tv2.get_children())
    return None


"""background_image = tk.PhotoImage(file='name.png')
background_label = tk.label(root, image=background_image)
background.place(relwidth = 1, relheight=1)"""

frame = tk.Frame(root, bg = '#80c1ff', bd=10) 
frame.place( relx = 0.5, rely = 0.1, relwidth = 0.90,  relheight= 0.05, anchor = 'n')

button = tk.Button(frame, text = "Select File", bg = 'gray', fg = 'red', command= lambda: browsefunc())
button.place(relx = 0.7, relwidth= 0.3, relheight=1)

# The file/file path text
label_file = ttk.Label(frame, text="No File Selected")
label_file.place(rely=0, relx=0.005, relheight=0.9, relwidth = 0.65)

pathlabel = tk.Label(root)
pathlabel.pack()

middle_frame = tk.Frame(root, bg = '#80c1ff', bd=10) 
middle_frame.place(relx=0.5, rely=0.15, relwidth = 0.90,  relheight= 0.05, anchor = 'n')

entry = DateEntry(middle_frame,bg="darkblue",fg="white",year=2015, date_pattern = 'y-mm-dd')
entry.place(relwidth = 0.65, relheight = 1)

button_load = tk.Button(middle_frame, text = "Load Data", bg = 'gray', fg = 'red', command=lambda: load_data())
button_load.place(relx = 0.7, relwidth= 0.3, relheight=1)

lower_frame = tk.Frame(root, bg = '#80c1ff', bd=10)
lower_frame.place(relx=0.5, rely=0.2, relwidth=0.9, relheight=0.6, anchor = 'n')

## Treeview Widget
tv1 = ttk.Treeview(lower_frame)
tv1.place(relheight=1, relwidth=1) # set the height and width of the widget to 100% of its container (frame1).

treescrolly = tk.Scrollbar(lower_frame, orient="vertical", command=tv1.yview) # command means update the yaxis view of the widget
treescrollx = tk.Scrollbar(lower_frame, orient="horizontal", command=tv1.xview) # command means update the xaxis view of the widget
tv1.configure(xscrollcommand=treescrollx.set, yscrollcommand=treescrolly.set) # assign the scrollbars to the Treeview Widget
treescrollx.pack(side="bottom", fill="x") # make the scrollbar fill the x axis of the Treeview widget
treescrolly.pack(side="right", fill="y") # make the scrollbar fill the y axis of the Treeview widget


bottom_frame = tk.Frame(root, bg = '#80c1ff', bd=10) 
bottom_frame.place(relx=0.5, rely=0.8, relwidth = 0.90,  relheight= 0.1, anchor = 'n')

tv2 = ttk.Treeview(bottom_frame)
tv2.place(relheight=1, relwidth=1)

root.mainloop()