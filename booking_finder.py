import tkinter as tk
from tkinter import filedialog
from datetime import datetime, timedelta
import pandas as pd

root = tk.Tk()
root.withdraw()


while True:
    try:
        file_path = filedialog.askopenfilename()
        bookings_df = pd.read_csv(file_path)

    except:
        print('Please open a .csv file')
        continue
    else:
        break



bookings_df['arrival_date'] = pd.to_datetime(bookings_df[['arrival_date_year', 
                                                            'arrival_date_month', 
                                                            'arrival_date_day_of_month']].astype(str).sum(axis=1), 
                                                            format='%Y%B%d')





bookings_df = bookings_df[bookings_df['is_canceled'] == 0]

bookings_df['total_days_stayed'] = pd.to_timedelta(bookings_df['stays_in_weekend_nights'] + bookings_df['stays_in_week_nights'], unit="D")

bookings_df['leaving_date'] = bookings_df['arrival_date'] + bookings_df['total_days_stayed']

print(bookings_df[['arrival_date', 'total_days_stayed','leaving_date', 'is_canceled']])


while True:
    try:
        date = input("Enter date (YYYY-MM-DD):")
        date = datetime.strptime(date, '%Y-%m-%d')

    except:
        print('Invalid date')
        continue
    else:
        break




final_df_mask = ((bookings_df['arrival_date'] <= date) & (date <= bookings_df['leaving_date'])) | ((date <= bookings_df['arrival_date'])  & (bookings_df['arrival_date'] <= (date + timedelta(days=7)) ))

final_df = bookings_df.loc[final_df_mask]

final_df.to_csv("bookings_" + str(date.date()) + ".csv", index=False)

total_df = final_df[['adults', 'children', 'babies']].sum(axis=0) 

final_df.to_csv("total_adults_children_babies_" + str(date.date()) + ".csv", index=False)













