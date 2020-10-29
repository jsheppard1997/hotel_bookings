import tkinter as tk
from tkinter import filedialog
from datetime import datetime, timedelta
import pandas as pd

root = tk.Tk()
root.withdraw()


#ensuring the uploaded file is a .csv
while True:
    try:
        file_path = filedialog.askopenfilename()
        bookings_df = pd.read_csv(file_path)

    except:
        print('Please open a .csv file')
        continue
    else:
        break


#combing the three columns for date, month and year into one in the format yyyy-mm-dd
bookings_df['arrival_date'] = pd.to_datetime(bookings_df[['arrival_date_year', 
                                                            'arrival_date_month', 
                                                            'arrival_date_day_of_month']].astype(str).sum(axis=1), 
                                                            format='%Y%B%d')




#removing all cancelled bookings
bookings_df = bookings_df[bookings_df['is_canceled'] == 0]

#finding the total days stayed by adding together the weekdays and weekend nights stayed
bookings_df['total_days_stayed'] = pd.to_timedelta(bookings_df['stays_in_weekend_nights'] +
                                    bookings_df['stays_in_week_nights'], unit="D")

#calculating the leaving date
bookings_df['leaving_date'] = bookings_df['arrival_date'] + \
                                bookings_df['total_days_stayed']

#getting user input for date and ensuring in yyyy-mm-dd format
while True:
    try:
        date = input("Enter date (YYYY-MM-DD):")
        date = datetime.strptime(date, '%Y-%m-%d')

    except:
        print('Invalid date')
        continue
    else:
        break



#creating a mask that finds all customers who are checked-in to the hotels on the date queried
#and all customers who are arriving within the next 7 days
final_df_mask = ((bookings_df['arrival_date'] <= date) &
                 (date <= bookings_df['leaving_date'])) | ((date <= bookings_df['arrival_date'])  &
                 (bookings_df['arrival_date'] <= (date + timedelta(days=7)) ))

#filtering the df to only show the entries in the mask above
final_df = bookings_df.loc[final_df_mask]

#saving as .csv
final_df.to_csv("bookings" + str(date.date()) + ".csv", index=False)

#letting the user know the file has been saved
print("A bookings dataframe for " + str(date.date()) + 
        " has been saved as bookings" + str(date.date()) + ".csv")

#picking just the adults, childen and babies and summing to find the total count of each column
total_df = final_df[['adults', 'children', 'babies']].sum(axis=0) 

#saving as .csv
total_df.to_csv("guests" + str(date.date()) + ".csv", index=False)

#letting the user know the file has been saved
print("A guest dataframe for " + str(date.date()) + 
        "has been saved as guests" + str(date.date()) + ".csv")

