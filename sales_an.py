import mysql.connector
import tkinter as tk
from tkinter import ttk
from datetime import datetime, timedelta
import numpy as np
import statsmodels.api as sm
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
    sales_data[name].append((datetime.strptime(str(date), "%Y-%m-%d"), int(qty_sold), int(current_stock)))

# Function for Holt-Winters Forecasting
def holt_winters_forecast(sales, days=7):
    if len(sales) < 3:
        return [round(np.mean(sales))] * days  # Use average if data is too short
    model = sm.tsa.ExponentialSmoothing(sales, trend="add", seasonal="add", seasonal_periods=7).fit()
    forecast = model.forecast(days)
    return [max(1, round(val)) for val in forecast]  # Ensure at least 1 sale/day

# Extract past sales for forecasting
aggregated_predictions = {}
today = datetime.today().date()
last_14_days = [(today - timedelta(days=i)).strftime("%Y-%m-%d") for i in range(13, -1, -1)]

for product, data in sales_data.items():
    sales_dict = {date.strftime("%Y-%m-%d"): qty_sold for date, qty_sold, _ in data}
    past_sales = [sales_dict.get(day, 0) for day in last_14_days]
    
    if sum(past_sales) == 0:
        continue  # Skip products with no recent sales
    
    forecasted_sales = holt_winters_forecast(past_sales, days=7)
    total_predicted_sales = sum(forecasted_sales)
    current_stock = data[-1][2] if data else 0
    total_required_stock = max(0, total_predicted_sales - current_stock)
    
    aggregated_predictions[product] = (total_predicted_sales, total_required_stock)

# GUI for displaying predictions and graph
class SalesAnalysisApp:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1290x700+380+150")
        self.root.resizable(False, False)
        self.root.title("AI Sales Predictor - Restocking Suggestion")
        self.root.config(bg="white")
        
        lbl_title = tk.Label(self.root, text="Sales Prediction & Restocking", font=("goudy old style", 20, "bold"), bg="#212f3d", fg="white", bd=3, relief=tk.RIDGE)
        lbl_title.pack(side=tk.TOP, fill=tk.X, padx=10, pady=5)
        
        main_frame = tk.Frame(self.root, bg="white")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        table_frame = tk.Frame(main_frame, width=600, height=550)
        table_frame.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=5)
        
        self.tree = ttk.Treeview(table_frame, columns=("Product", "Total Predicted Sales", "Total Restocking Needed"), show="headings", height=15)
        for col in ("Product", "Total Predicted Sales", "Total Restocking Needed"):
            self.tree.heading(col, text=col, command=lambda c=col: self.sort_data(c, False))
        self.tree.pack(fill=tk.BOTH, expand=True)
        self.load_data()
        
        graph_frame = tk.Frame(main_frame, bg="white", width=650, height=550)
        graph_frame.pack(side=tk.RIGHT, fill=tk.BOTH, padx=10, pady=5)
        self.plot_graph(graph_frame)
    
    def load_data(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        for product, values in aggregated_predictions.items():
            self.tree.insert("", tk.END, values=(product, round(values[0]), round(values[1])))
    
    def sort_data(self, column, reverse):
        def convert(val):
            try:
                return float(val)
            except ValueError:
                return val
        data = [(convert(self.tree.set(child, column)), child) for child in self.tree.get_children()]
        data.sort(reverse=reverse, key=lambda x: x[0])
        for index, (_, child) in enumerate(data):
            self.tree.move(child, "", index)
        self.tree.heading(column, command=lambda: self.sort_data(column, not reverse))
    
    def plot_graph(self, parent_frame):
        fig, ax = plt.subplots(figsize=(7, 4))
        days = [(today - timedelta(days=i)).strftime("%d-%b") for i in range(13, -1, -1)]
        
        for product, data in sales_data.items():
            sales_dict = {date.strftime("%Y-%m-%d"): qty_sold for date, qty_sold, _ in data}
            past_sales = [sales_dict.get(day, 0) for day in last_14_days]
            ax.plot(days, past_sales[-14:], marker="o", linestyle="-", label=product)
        
        ax.set_title("Past 14 Days Sales Trend (Click to View Last 30 Days)", fontsize=12)
        ax.set_xlabel("Date", fontsize=10)
        ax.set_ylabel("Units Sold", fontsize=10)
        ax.legend(loc="upper right", fontsize=8, ncol=2)
        ax.grid(True, linestyle="--", alpha=0.6)
        ax.tick_params(axis="x", rotation=45)
        
        canvas = FigureCanvasTkAgg(fig, master=parent_frame)
        canvas.draw()
        widget = canvas.get_tk_widget()
        widget.pack(fill=tk.BOTH, expand=True)
        widget.bind("<Button-1>", lambda event: self.open_detailed_graph())
    
    def open_detailed_graph(self):
        new_window = tk.Toplevel(self.root)
        new_window.title("Last 30 Days Sales Trend")
        new_window.geometry("800x500")
        
        fig, ax = plt.subplots(figsize=(8, 4))
        last_30_days = [(today - timedelta(days=i)).strftime("%d-%b") for i in range(29, -1, -1)]
        for product, data in sales_data.items():
            sales_dict = {date.strftime("%Y-%m-%d"): qty_sold for date, qty_sold, _ in data}
            past_sales_30 = [sales_dict.get(day, 0) for day in [(today - timedelta(days=i)).strftime("%Y-%m-%d") for i in range(29, -1, -1)]]
            ax.plot(last_30_days, past_sales_30, marker="o", linestyle="-", label=product)
        ax.set_title("Last 30 Days Sales Trend", fontsize=12)
        ax.legend(loc="upper right", fontsize=8, ncol=2)
        canvas = FigureCanvasTkAgg(fig, master=new_window)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

# Run the application
if __name__ == "__main__":
    root = tk.Tk()
    app = SalesAnalysisApp(root)
    root.mainloop()