import mysql.connector
import tkinter as tk
from tkinter import ttk
from datetime import datetime, timedelta
from decimal import Decimal
from tkinter import *
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

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
    sales_data[name].append((datetime.strptime(str(date), "%Y-%m-%d"), int(qty_sold), int(current_stock)))  # Ensure whole numbers

# Function for Exponential Smoothing
def exponential_smoothing(sales, alpha=0.3):
    """Apply exponential smoothing to predict future sales."""
    if not sales:
        return 0
    smoothed = sales[0]
    for sale in sales[1:]:
        smoothed = alpha * sale + (1 - alpha) * smoothed
    return round(smoothed)  # Ensure whole number

# Extract past 14 days sales for graph
past_sales_over_time = {}
today = datetime.today().date()
last_14_days = [(today - timedelta(days=i)).strftime("%Y-%m-%d") for i in range(13, -1, -1)]  # Last 14 days

for product, data in sales_data.items():
    sales_dict = {date.strftime("%Y-%m-%d"): qty_sold for date, qty_sold, _ in data}
    past_sales = [sales_dict.get(day, 0) for day in last_14_days]
    past_sales_over_time[product] = past_sales

# Calculate total restocking requirement for next 7 days per product
aggregated_predictions = {}
for product, data in sales_data.items():
    recent_sales = [sales for _, sales, _ in data[-7:]]  # Last 7 days
    smoothed_sales = exponential_smoothing(recent_sales)  # Apply smoothing
    avg_sales = smoothed_sales if recent_sales else 0
    current_stock = data[-1][2] if data else 0
    total_predicted_sales = 0
    total_required_stock = 0

    for i in range(7):  # Predict next 7 days
        predicted_sales = max(1, avg_sales)  # Ensure at least 1 sale per day
        total_predicted_sales += predicted_sales

        if current_stock >= predicted_sales:
            current_stock -= predicted_sales
        else:
            total_required_stock += (predicted_sales - current_stock)
            current_stock = 0

    if total_required_stock > 0:
        aggregated_predictions[product] = (total_predicted_sales, total_required_stock)

# GUI for displaying predictions and graph
class sales_analysis_Class:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1290x700+380+150")  # Fixed size
        self.root.resizable(False, False)  # Prevent resizing
        self.root.title("AI Sales Analyzer - Restocking Suggestion")
        self.root.config(bg="white")
        self.root.focus_force()

        lbl_title = Label(self.root, text="View Sales Analysis", font=("goudy old style", 20, "bold"),
                          bg="#212f3d", fg="white", bd=3, relief=RIDGE)
        lbl_title.pack(side=TOP, fill=X, padx=10, pady=5)

        # Create a frame for the table and graph
        main_frame = Frame(self.root, bg="white")
        main_frame.pack(fill=BOTH, expand=True, padx=10, pady=5)

        # Left Side: Table Frame
        table_frame = Frame(main_frame, width=600, height=550)
        table_frame.pack(side=LEFT, fill=Y, padx=10, pady=5)

        self.tree = ttk.Treeview(table_frame, columns=("Product", "Total Predicted Sales", "Total Restocking Needed"),
                                 show="headings", height=15)
        self.tree.heading("Product", text="Product", command=lambda: self.sort_data("Product", False))
        self.tree.heading("Total Predicted Sales", text="Total Predicted Sales (7 Days)",
                          command=lambda: self.sort_data("Total Predicted Sales", False))
        self.tree.heading("Total Restocking Needed", text="Total Restocking Needed",
                          command=lambda: self.sort_data("Total Restocking Needed", False))

        self.tree.pack(fill=BOTH, expand=True)

        self.load_data()

        # Right Side: Graph Frame
        graph_frame = Frame(main_frame, bg="white", width=650, height=550)
        graph_frame.pack(side=RIGHT, fill=BOTH, padx=10, pady=5)

        self.plot_graph(graph_frame)

    def load_data(self):
        """Load data into the Treeview."""
        for row in self.tree.get_children():
            self.tree.delete(row)

        for product, values in aggregated_predictions.items():
            total_sales = round(values[0])  # Ensure whole number
            restocking_needed = round(values[1])
            self.tree.insert("", tk.END, values=(product, total_sales, restocking_needed))

    def sort_data(self, column, reverse):
        """Sort the data in the Treeview."""
        def convert(val):
            """Convert value for sorting (numeric if possible)."""
            try:
                return float(val)
            except ValueError:
                return val  # Keep as string

        data = [(convert(self.tree.set(child, column)), child) for child in self.tree.get_children()]
        data.sort(reverse=reverse, key=lambda x: x[0])

        for index, (val, child) in enumerate(data):
            self.tree.move(child, "", index)

        self.tree.heading(column, command=lambda: self.sort_data(column, not reverse))

    def plot_graph(self, parent_frame):
        """Plot the past 14 days of sales for all products."""
        fig, ax = plt.subplots(figsize=(7, 4))  # Adjusted to fit the window

        days = [(today - timedelta(days=i)).strftime("%d-%b") for i in range(13, -1, -1)]  # Last 14 days

        for product, sales in past_sales_over_time.items():
            ax.plot(days, sales, marker="o", linestyle="-", label=product)

        ax.set_title("Past 14 Days Sales Trend", fontsize=12)
        ax.set_xlabel("Date", fontsize=10)
        ax.set_ylabel("Units Sold", fontsize=10)
        ax.legend(loc="upper right", fontsize=8, ncol=2)
        ax.grid(True, linestyle="--", alpha=0.6)
        ax.tick_params(axis="x", rotation=45)  # Rotate x-axis labels for readability

        # Embed the figure inside Tkinter
        canvas = FigureCanvasTkAgg(fig, master=parent_frame)
        canvas.draw()
        widget = canvas.get_tk_widget()
        widget.pack(fill=tk.BOTH, expand=True)  # Ensure it fills available space


# Main execution
if __name__ == "__main__":
    root = tk.Tk()
    obj = sales_analysis_Class(root)
    root.mainloop()
