import pandas as pd
import csv
from datetime import datetime
from data_entry import get_amount,get_category,get_date,get_description
from plot import plot_transaction
from body import CSV

def add():
    CSV.initialize_csv()
    date=get_date(
        "Enter the date of transaction (dd-mm-yyyy) or press Enter for today's date: ",
        allow_default=True)
    amount=get_amount()
    category=get_category()
    description = get_description()
    CSV.add_entry(date,amount,category,description)

def update():
    serial_number=int(input(f'Enter Serial number of Transaction to update: '))
    date=get_date("Enter date you want to update in dd-mm-yyyy format : ")
    amount=get_amount()
    category=get_category()
    description = get_description()
    CSV.update_entry(serial_number,date, amount, category, description)


def delete():
    serial_no=int(input(f'Enter Serial Number of Transaction to delete: '))
    CSV.delete_entry(serial_no)


def main():
    while True:
        print("\n1. Add a new Transaction")
        print("2. Update an existing transaction")
        print("3. Delete a transaction")
        print("4. View Transaction and summary within a date range")
        print("5. Exit")
        choice = input("Enter your choice (1-5): ")
        if choice == "1":
            add()
        elif choice == "2":
            update()
        elif choice == "3":
            delete()
        elif choice == "4":
            start_date = get_date("Enter Start date (dd-mm-yyyy): ")
            end_date = get_date("Enter end date (dd-mm-yyyy): ")
            df = CSV.get_transaction(start_date,end_date)
            if not df.empty and input(f'Do you want to see plot? (Y/N): ').lower() == 'y':
                timeframe = input("Choose timeframe: D (Day), M (Month), Y (Year): ").lower()
                plot_transaction(df,timeframe)
        elif choice == "5":
            print("Exiting...")
            break
        else:
            print("Invalid choice. Enter any number between 1 to 5.")

if __name__ == "__main__":
    main()