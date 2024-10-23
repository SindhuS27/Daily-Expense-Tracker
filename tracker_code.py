import csv
from tkinter import *
from tkinter import messagebox
from datetime import datetime

# File to store expenses
EXPENSE_FILE = 'expenses.csv'

# Initialize CSV file if it doesn't exist
def init_expense_file():
    try:
        with open(EXPENSE_FILE, mode='x', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Date', 'Category', 'Amount', 'Description'])
    except FileExistsError:
        pass

# Add expense function
def add_expense():
    category = category_entry.get()
    amount = amount_entry.get()
    description = description_entry.get()

    if not category or not amount or not description:
        messagebox.showwarning("Input Error", "All fields are required!")
        return

    try:
        float(amount)
    except ValueError:
        messagebox.showwarning("Input Error", "Amount must be a number!")
        return

    date = datetime.now().strftime("%Y-%m-%d")
    with open(EXPENSE_FILE, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([date, category, amount, description])
    
    messagebox.showinfo("Expense Added", f"Expense '{description}' added successfully!")
    category_entry.delete(0, END)
    amount_entry.delete(0, END)
    description_entry.delete(0, END)

# View today's expenses
def view_today_expenses():
    today = datetime.now().strftime("%Y-%m-%d")
    total = 0
    expenses = []
    
    with open(EXPENSE_FILE, mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row['Date'] == today:
                expenses.append(f"{row['Description']}: ${row['Amount']} ({row['Category']})")
                total += float(row['Amount'])
    
    if expenses:
        expenses_str = "\n".join(expenses)
        messagebox.showinfo("Today's Expenses", f"Expenses for today:\n\n{expenses_str}\n\nTotal spent: ${total}")
    else:
        messagebox.showinfo("Today's Expenses", "No expenses recorded for today.")

# Analyze expenses by category
def analyze_expenses():
    categories = {}
    
    with open(EXPENSE_FILE, mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            category = row['Category']
            amount = float(row['Amount'])
            categories[category] = categories.get(category, 0) + amount
    
    if categories:
        breakdown = "\n".join([f"{category}: ${total}" for category, total in categories.items()])
        messagebox.showinfo("Expense Breakdown", f"Expense Breakdown by Category:\n\n{breakdown}")
    else:
        messagebox.showinfo("Expense Breakdown", "No expenses recorded yet.")

# Initialize the main GUI
def main():
    init_expense_file()

    root = Tk()
    root.title("Daily Expense Tracker")

    # Input Fields
    global category_entry, amount_entry, description_entry

    Label(root, text="Category:").grid(row=0, column=0, padx=10, pady=10)
    category_entry = Entry(root, width=30)
    category_entry.grid(row=0, column=1, padx=10, pady=10)

    Label(root, text="Amount:").grid(row=1, column=0, padx=10, pady=10)
    amount_entry = Entry(root, width=30)
    amount_entry.grid(row=1, column=1, padx=10, pady=10)

    Label(root, text="Description:").grid(row=2, column=0, padx=10, pady=10)
    description_entry = Entry(root, width=30)
    description_entry.grid(row=2, column=1, padx=10, pady=10)

    # Buttons
    add_button = Button(root, text="Add Expense", command=add_expense)
    add_button.grid(row=3, column=0, padx=10, pady=10)

    view_button = Button(root, text="View Today's Expenses", command=view_today_expenses)
    view_button.grid(row=3, column=1, padx=10, pady=10)

    analyze_button = Button(root, text="Analyze Expenses", command=analyze_expenses)
    analyze_button.grid(row=4, column=0, padx=10, pady=10, columnspan=2)

    # Start the GUI loop
    root.mainloop()

if __name__ == '__main__':
    main()
