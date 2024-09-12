import pandas as pd
import csv
from datetime import datetime

class CSV:
    #variables
    CSV_FILE = "dup.csv"
    Columns = ["Serial No","Date","Amount","Category","Description"]
    Format = "%d-%m-%Y"

    @classmethod
    def initialize_csv(cls):
        try:
            pd.read_csv(cls.CSV_FILE)
        except FileNotFoundError:
            df = pd.DataFrame(columns=cls.Columns)
            df.to_csv(cls.CSV_FILE, index=False)


    @classmethod
    def serial_number(cls):
        try:
            df = pd.read_csv(cls.CSV_FILE)
            if not df.empty:
                return len(df) + 1
            return 1
        except FileNotFoundError:
            return 1


    @classmethod
    def add_entry(cls,date,amount,category,description):
        serial=cls.serial_number()
        new_entry = {
            "Serial No": serial,
            "Date":date,
            "Amount":amount,
            "Category":category,
            "Description":description
        }
        with open(cls.CSV_FILE, "a", newline="") as csvfile: #context manager
            writer = csv.DictWriter(csvfile, fieldnames=cls.Columns)
            writer.writerow(new_entry)
        print("Entry added successfully")

    @classmethod
    def update_entry(cls,serial_no,date,amount,category,description):
        df = pd.read_csv(cls.CSV_FILE)
        if 0<=serial_no <len(df):
            index = df[df["Serial No"] == serial_no].index[0]
            df.at[index, 'Date'] = date
            df.at[index, 'Amount'] = amount
            df.at[index, 'Category'] = category
            df.at[index, 'Description'] = description
            df["Serial No"] = range(1,len(df) + 1)
            df.to_csv(cls.CSV_FILE, index=False)
            print(f'File Updated Successfully')
        else:
            print(f'Invalid S.no. No entry updated')

    @classmethod
    def delete_entry(cls,serial_no):
        try:
            df = pd.read_csv(cls.CSV_FILE)
            if df.empty:
                print(f'No data found to delete')
                return
            if 0 <= serial_no < len(df):
                index = df[df["Serial No"] == serial_no].index[0]
                df = df.drop(index).reset_index(drop=True)
                df["Serial No"] = range(1, len(df)+1)
                df.to_csv(cls.CSV_FILE,index=False)
                print("Entry deleted Successfully")
            else:
                print("Incorrect Index. No entry deleted")
        except FileNotFoundError:
            print(f'No data found to delete')



    @classmethod
    def get_transaction(cls,start_date,end_date):
        df = pd.read_csv(cls.CSV_FILE)
        df["Date"] = pd.to_datetime(df["Date"],format=CSV.Format)
        start_date = datetime.strptime(start_date, CSV.Format)
        end_date = datetime.strptime(end_date, CSV.Format)

        mask = (df["Date"] >= start_date) & (df["Date"] <= end_date)
        filtered_df = df.loc[mask]

        if filtered_df.empty:
            print("No transaction found in given date range")
        else:
            print(
                f'Transaction from {start_date.strftime(CSV.Format)} to {end_date.strftime(cls.Format)}'
            )
            print(
                filtered_df.to_string(
                    index=False, formatters={"Date" : lambda x : x.strftime(CSV.Format)}
                )
            )

            total_income = filtered_df[filtered_df["Category"] == "Income"]["Amount"].sum()
            total_expense = filtered_df[filtered_df["Category"] =="Expense"]["Amount"].sum()
            print("\nSummary : ")
            print(f'Total Income : ${total_income:.2f}')
            print(f'Total Expense : ${total_expense:.2f}')
            print(f'Net Saving : ${(total_income-total_expense):.2f}')
        return filtered_df