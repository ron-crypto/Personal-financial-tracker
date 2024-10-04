import csv
from datetime import datetime
import pandas as pd # type: ignore

# Function to log a transaction (income/expense)
def log_transaction(transaction_type, amount, category, description):
    date = datetime.now().strftime('%Y-%m-%d')
    # Append the transaction to a CSV file
    with open('finance_log.csv', mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([date, transaction_type, amount, category, description])
    print(f"{transaction_type.capitalize()} logged successfully.")

def display_transactions():
    try:
        df = pd.read_csv('finance_log.csv')
        if df.empty:
            print("No transactions found.")
        else:
            print("\n--- All Transactions ---")
            print(df.to_string(index=False))
    except FileNotFoundError:
        print("No transactions found. Start by logging some transactions!")

def calculate_totals():
    try:
        df = pd.read_csv('finance_log.csv')
        print("columns in csv:", df.columns.tolist())

        if df.empty:
            print("No transactions to calculate totals.")
            return

        # Fix the column name if there are any typos
        df.rename(columns={"Tansaction_type": "transaction_type"}, inplace=True)

        # Ensure the amount is numeric for calculation
        df['amount'] = pd.to_numeric(df['amount'], errors='coerce')

        total_income = df[df['transaction_type'] == 'income']['amount'].sum()
        total_expenses = df[df['transaction_type'] == 'expense']['amount'].sum()
        net_savings = total_income - total_expenses

        print(f"\n--- Financial Summary ---")
        print(f"Total Income: Ksh {total_income:.2f}")
        print(f"Total Expenses: Ksh {total_expenses:.2f}")
        print(f"Net Savings: Ksh {net_savings:.2f}")

    except FileNotFoundError:
        print("No transactions found. Start by logging some transactions!")
    except KeyError:
        print("The required columns are missing in the CSV file.")

def main():
    while True:
        print("\n--- Personal Finance Log ---")
        print("1. Log a Transaction")
        print("2. Display all transactions")
        print("3. Calculate Totals")
        print("4. Quit")
        choice = input("Enter your choice: ")

        if choice == '1':
            while True:
                transaction_type = input("Enter transaction type (income/expense): ").strip().lower()
                if transaction_type in ['income', 'expense']:
                    break
                else:
                    print("Invalid transaction type. Please enter 'income' or 'expense'.")

            while True:
                try:
                    amount = float(input("Enter amount (Ksh): "))
                    break
                except ValueError:
                    print("Invalid amount. Please enter a valid number.")

            category = input("Enter category (e.g., Food, Rent, Salary): ")
            description = input("Enter description: ")
            log_transaction(transaction_type, amount, category, description)

        elif choice == '2':
            display_transactions()

        elif choice == '3':
            calculate_totals()

        elif choice == '4':
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please select a valid option.")

if __name__ == "__main__":
    main()



