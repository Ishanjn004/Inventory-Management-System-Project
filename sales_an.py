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

# Calculate total restocking requirement for next 7 days per product
aggregated_predictions = {}
today = datetime.today().date()

for product, data in sales_data.items():
    recent_sales = [sales for _, sales, _ in data[-7:]]  # Last 7 days sales
    avg_sales = sum(recent_sales) / len(recent_sales) if recent_sales else 0
    current_stock = data[-1][2] if data else 0  # Get last known stock
    total_predicted_sales = 0  # Sum of predicted sales over 7 days
    total_required_stock = 0  # Sum of restocking needed

    for i in range(7):
        predicted_sales = max(1, int(avg_sales))  # Ensure at least 1 sale per day
        total_predicted_sales += predicted_sales  # Aggregate total sales

        if current_stock >= predicted_sales:
            current_stock -= predicted_sales
        else:
            total_required_stock += (predicted_sales - current_stock)
            current_stock = 0  # Stock is depleted

    aggregated_predictions[product] = (total_predicted_sales, total_required_stock)

# GUI for displaying predictions
class sales_analysis_Class:
    def __init__(self, root):
        root.title("AI Sales Analyzer - Restocking Suggestion")

        frame = ttk.Frame(root, padding="10")
        frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        tree = ttk.Treeview(frame, columns=("Product", "Total Predicted Sales", "Total Restocking Needed"), show="headings")
        tree.heading("Product", text="Product")
        tree.heading("Total Predicted Sales", text="Total Predicted Sales (7 Days)")
        tree.heading("Total Restocking Needed", text="Total Restocking Needed")

        tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        for product, values in aggregated_predictions.items():
            tree.insert("", tk.END, values=(product, values[0], values[1]))

# Main execution
if __name__ == "__main__":
    root = tk.Tk()  # Create main Tkinter window once
    obj = sales_analysis_Class(root)
    root.mainloop()
