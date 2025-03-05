import mysql.connector
import tkinter as tk
from tkinter import ttk
from datetime import datetime, timedelta
from decimal import Decimal

# Connect to MySQL database
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="ishan",
    database="ims"
)
cursor = db.cursor()

# Fetch past sales data from the database
cursor.execute("SELECT name, date, qty_sold, current_stock FROM sales ORDER BY date")
rows = cursor.fetchall()

# Organizing data for processing
sales_data = {}
for name, date, qty_sold, current_stock in rows:
    if name not in sales_data:
        sales_data[name] = []
    sales_data[name].append((datetime.strptime(str(date), "%Y-%m-%d"), Decimal(qty_sold), Decimal(current_stock)))

# Calculate restocking requirement for next 7 days
predictions = []
today = datetime.today().date()

for product, data in sales_data.items():
    recent_sales = [sales for _, sales, _ in data[-7:]]  # Last 7 days sales
    avg_sales = sum(recent_sales) / len(recent_sales) if recent_sales else 0
    current_stock = data[-1][2] if data else 0  # Get last known stock
    required_stock = 0  # To track how much needs restocking

    for i in range(7):
        predicted_date = today + timedelta(days=i)
        predicted_sales = max(1, int(avg_sales))  # Ensure at least 1 sale per day
        
        if current_stock >= predicted_sales:
            current_stock -= predicted_sales
        else:
            required_stock += (predicted_sales - current_stock)
            current_stock = 0  # Stock is depleted
        
        predictions.append((product, predicted_date, predicted_sales, required_stock))

# GUI for displaying predictions
class sales_analysis_Class:
    def __init__(self, root):
        root.title("AI Sales Analyzer - Restocking Suggestion")  # Use the existing root
        self.root=root
        self.root.geometry("1290x700+380+150")
        self.root.title("Inventory Management System")
        self.root.config(bg="white")
        self.root.focus_force()

        frame = ttk.Frame(root, padding="10")
        frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        tree = ttk.Treeview(frame, columns=("Product", "Date", "Predicted Sales (7 Days)", "Restocking Needed"), show="headings")
        tree.heading("Product", text="Product")
        tree.heading("Date", text="Date")
        tree.heading("Predicted Sales (7 Days)", text="Predicted Sales (7 Days)")
        tree.heading("Restocking Needed", text="Restocking Needed")

        tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        for prediction in predictions:
            tree.insert("", tk.END, values=prediction)

# Main execution
if __name__ == "__main__":
    root = tk.Tk()  # Create main Tkinter window once
    obj = sales_analysis_Class(root)
    root.mainloop()
