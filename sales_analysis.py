import mysql.connector
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime, timedelta
import numpy as np
import statsmodels.api as sm
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from matplotlib import style

# Use a modern matplotlib style
import seaborn as sns
sns.set_theme()

# Connect to MySQL database
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="ishan",
    database="ims"
)
cursor = db.cursor()

def fetch_sales_data():
    """Fetch fresh sales data from database and organize it"""
    cursor.execute("SELECT name, date, qty_sold, current_stock FROM sales ORDER BY date")
    rows = cursor.fetchall()
    
    sales_data = {}
    for name, date, qty_sold, current_stock in rows:
        date_obj = datetime.strptime(str(date), "%Y-%m-%d")
        if name not in sales_data:
            sales_data[name] = []
        
        # Check if we already have an entry for this product on this date
        found = False
        for i, (existing_date, existing_qty, existing_stock) in enumerate(sales_data[name]):
            if existing_date.date() == date_obj.date():
                # Aggregate quantities for same product on same day
                sales_data[name][i] = (existing_date, existing_qty + int(qty_sold), int(current_stock))
                found = True
                break
        
        if not found:
            sales_data[name].append((date_obj, int(qty_sold), int(current_stock)))
    
    return sales_data

def fetch_current_stocks():
    """Fetch current stock levels for all products"""
    cursor.execute("SELECT name, qty FROM product")
    return {name: int(stock) for name, stock in cursor.fetchall()}

def calculate_predictions(sales_data):
    """Calculate sales predictions based on sales data"""
    today = datetime.today().date()
    last_14_days = [(today - timedelta(days=i)).strftime("%Y-%m-%d") for i in range(14, -1, -1)]
    current_stocks = fetch_current_stocks()
    aggregated_predictions = {}
    
    for product, data in sales_data.items():
        # Create sales dictionary with aggregated daily totals
        sales_dict = {}
        for date, qty_sold, _ in data:
            date_str = date.strftime("%Y-%m-%d")
            if date_str in sales_dict:
                sales_dict[date_str] += qty_sold
            else:
                sales_dict[date_str] = qty_sold
        
        past_sales = [sales_dict.get(day, 0) for day in last_14_days]
        forecasted_sales = holt_winters_forecast(past_sales, days=7)
        
        if sum(forecasted_sales) > 0:
            current_stock = current_stocks.get(product, 0)
            total_predicted_sales = sum(forecasted_sales)
            total_required_stock = max(0, total_predicted_sales - current_stock)
            aggregated_predictions[product] = (total_predicted_sales, total_required_stock)
    
    return aggregated_predictions

# Improved Holt-Winters Forecasting function
def holt_winters_forecast(sales, days=7):
    if sum(sales[-7:]) == 0:
        return [0] * days
    
    if len(sales) < 7:
        if sum(sales) < 3:
            return [0] * days
        avg_sales = np.mean([x for x in sales if x > 0]) if any(x > 0 for x in sales) else 0
        return [round(avg_sales)] * days if avg_sales > 0 else [0] * days
    
    try:
        seasonal_periods = 7
        model = sm.tsa.ExponentialSmoothing(
            sales,
            trend="add",
            seasonal="add" if len(sales) >= 2*seasonal_periods else None,
            seasonal_periods=seasonal_periods if len(sales) >= 2*seasonal_periods else None
        ).fit()
        forecast = model.forecast(days)
        return [max(0, round(val)) for val in forecast]
    except Exception as e:
        print(f"Forecasting error: {e}")
        return [0] * days

# Fetch initial data
sales_data = fetch_sales_data()
aggregated_predictions = calculate_predictions(sales_data)
today = datetime.today().date()
last_14_days = [(today - timedelta(days=i)).strftime("%Y-%m-%d") for i in range(14, -1, -1)]

class ModernSalesAnalysisApp:
    def __init__(self, root):
        self.root = root
        self.setup_window()
        self.create_widgets()
        self.load_data()
        
    def setup_window(self):
        self.root.geometry("1350x750+330+150")
        self.root.resizable(True, True)
        self.root.title("AI Sales Predictor - Inventory Management System")
        self.root.configure(bg="#f5f6fa")
        
        # Custom title bar
        self.title_frame = tk.Frame(self.root, bg="#2f3640", height=50)
        self.title_frame.pack(fill=tk.X)
        
        self.title_label = tk.Label(
            self.title_frame,
            text="Sales Prediction & Restocking Analysis",
            font=("Segoe UI", 14, "bold"),
            bg="#2f3640",
            fg="white"
        )
        self.title_label.pack(side=tk.LEFT, padx=20)
        
        # Close button in title bar
        self.close_btn = tk.Button(
            self.title_frame,
            text="×",
            font=("Segoe UI", 16),
            bg="#2f3640",
            fg="white",
            bd=0,
            activebackground="#e84118",
            command=self.root.quit
        )
        self.close_btn.pack(side=tk.RIGHT, padx=10)
        
        # Main content frame
        self.main_frame = tk.Frame(self.root, bg="#f5f6fa")
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
    def create_widgets(self):
        # Create notebook for tabs
        self.notebook = ttk.Notebook(self.main_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True)
        
        # Tab 1: Predictions
        self.tab1 = tk.Frame(self.notebook, bg="#f5f6fa")
        self.notebook.add(self.tab1, text="Restocking Recommendations")
        
        # Tab 2: Trends
        self.tab2 = tk.Frame(self.notebook, bg="#f5f6fa")
        self.notebook.add(self.tab2, text="Sales Trends")
        
        # Tab 3: Insights
        self.tab3 = tk.Frame(self.notebook, bg="#f5f6fa")
        self.notebook.add(self.tab3, text="Key Insights")
        
        # Build each tab
        self.build_predictions_tab()
        self.build_trends_tab()
        self.build_insights_tab()
        
    def build_predictions_tab(self):
        # Header frame
        header_frame = tk.Frame(self.tab1, bg="#f5f6fa")
        header_frame.pack(fill=tk.X, pady=(0, 10))
        
        tk.Label(
            header_frame,
            text="Products Requiring Restocking",
            font=("Segoe UI", 12, "bold"),
            bg="#f5f6fa",
            fg="#2f3640"
        ).pack(side=tk.LEFT)
        
        # Filter frame
        filter_frame = tk.Frame(self.tab1, bg="#f5f6fa")
        filter_frame.pack(fill=tk.X, pady=(0, 10))
        
        tk.Label(
            filter_frame,
            text="Filter:",
            font=("Segoe UI", 9),
            bg="#f5f6fa"
        ).pack(side=tk.LEFT, padx=(0, 5))
        
        self.filter_var = tk.StringVar()
        self.filter_entry = ttk.Entry(
            filter_frame,
            textvariable=self.filter_var,
            width=30,
            font=("Segoe UI", 9)
        )
        self.filter_entry.pack(side=tk.LEFT, padx=(0, 10))
        self.filter_entry.bind("<KeyRelease>", self.filter_table)
        
        # Add Clear Filter button
        ttk.Button(
            filter_frame,
            text="Clear Filter",
            command=self.clear_filter,
            style="TButton"
        ).pack(side=tk.LEFT, padx=(0, 10))
        
        ttk.Button(
            filter_frame,
            text="Export to CSV",
            command=self.export_to_csv,
            style="Accent.TButton"
        ).pack(side=tk.RIGHT)
        
        # Add Refresh button
        ttk.Button(
            filter_frame,
            text="Refresh Data",
            command=self.refresh_data,
            style="Accent.TButton"
        ).pack(side=tk.RIGHT, padx=(0, 10))
        
        # Table frame
        table_frame = tk.Frame(self.tab1, bg="#f5f6fa")
        table_frame.pack(fill=tk.BOTH, expand=True)
        
        # Treeview with style
        style = ttk.Style()
        style.configure("Treeview.Heading", font=("Segoe UI", 10, "bold"))
        style.configure("Treeview", font=("Segoe UI", 9), rowheight=25)
        style.map("Treeview", background=[("selected", "#3498db")])
        
        self.tree = ttk.Treeview(
            table_frame,
            columns=("Product", "Current Stock", "Predicted Demand", "Restock Qty"),
            show="headings",
            height=15,
            selectmode="extended"
        )
        
        # Configure columns
        self.tree.heading("Product", text="Product", anchor=tk.CENTER, command=lambda: self.sort_treeview("Product", False))
        self.tree.heading("Current Stock", text="Current Stock", anchor=tk.CENTER, command=lambda: self.sort_treeview("Current Stock", False))
        self.tree.heading("Predicted Demand", text="Predicted Demand (7 days)", anchor=tk.CENTER, command=lambda: self.sort_treeview("Predicted Demand", False))
        self.tree.heading("Restock Qty", text="Restock Qty", anchor=tk.CENTER, command=lambda: self.sort_treeview("Restock Qty", False))
        
        self.tree.column("Product", width=250, anchor=tk.W)
        self.tree.column("Current Stock", width=150, anchor=tk.CENTER)
        self.tree.column("Predicted Demand", width=200, anchor=tk.CENTER)
        self.tree.column("Restock Qty", width=150, anchor=tk.CENTER)
        
        # Add scrollbar
        scroll_y = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scroll_y.set)
        scroll_y.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree.pack(fill=tk.BOTH, expand=True)
        
        # Add striped row colors
        self.tree.tag_configure('oddrow', background="#ffffff")
        self.tree.tag_configure('evenrow', background="#f9f9f9")
        
        # Status bar
        self.status_bar = tk.Label(
            self.tab1,
            text=f"Showing {len(aggregated_predictions)} products requiring attention",
            bd=1,
            relief=tk.SUNKEN,
            anchor=tk.W,
            font=("Segoe UI", 9),
            bg="#dfe6e9",
            fg="#2d3436"
        )
        self.status_bar.pack(fill=tk.X, pady=(10, 0))
        
    def build_trends_tab(self):
        # Main frame for graphs
        graph_frame = tk.Frame(self.tab2, bg="#f5f6fa")
        graph_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Create notebook for graph tabs
        graph_notebook = ttk.Notebook(graph_frame)
        graph_notebook.pack(fill=tk.BOTH, expand=True)
        
        # 14-day top products tab
        trend_14_top_frame = tk.Frame(graph_notebook, bg="#f5f6fa")
        graph_notebook.add(trend_14_top_frame, text="14-Day (Top Products)")
        self.plot_14_day_top_trend(trend_14_top_frame)
        
        # 14-day all products tab
        trend_14_all_frame = tk.Frame(graph_notebook, bg="#f5f6fa")
        graph_notebook.add(trend_14_all_frame, text="14-Day (All Products)")
        self.plot_14_day_all_trend(trend_14_all_frame)
        
        # 30-day top products tab
        trend_30_top_frame = tk.Frame(graph_notebook, bg="#f5f6fa")
        graph_notebook.add(trend_30_top_frame, text="30-Day (Top Products)")
        self.plot_30_day_top_trend(trend_30_top_frame)
        
        # 30-day all products tab
        trend_30_all_frame = tk.Frame(graph_notebook, bg="#f5f6fa")
        graph_notebook.add(trend_30_all_frame, text="30-Day (All Products)")
        self.plot_30_day_all_trend(trend_30_all_frame)
        
    def build_insights_tab(self):
        # Insights frame
        insights_frame = tk.Frame(self.tab3, bg="#f5f6fa")
        insights_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
    
        # Calculate key metrics
        total_restock = sum(val[1] for val in aggregated_predictions.values() if isinstance(val[1], (int, float)))
        products_need_restock = len([val for val in aggregated_predictions.values() if val[1] > 0])
    
        # Find the highest demand products
        max_demand = 0
        highest_demand_products = []
    
        for product, (predicted_demand, _) in aggregated_predictions.items():
            if predicted_demand > max_demand:
                max_demand = predicted_demand
                highest_demand_products = [product]
            elif predicted_demand == max_demand:
                highest_demand_products.append(product)
    
        # Create metric cards
        metrics = [
            ("Products Requiring Restock", products_need_restock, "#e74c3c"),
            ("Total Restock Quantity", total_restock, "#3498db"),
            ("Highest Demand Product", ', '.join(highest_demand_products) + f"\n({max_demand} units)", "#2ecc71")
        ]
    
        for i, (title, value, color) in enumerate(metrics):
            card = tk.Frame(
                insights_frame,
                bg="white",
                bd=0,
                highlightbackground="#bdc3c7",
                highlightthickness=1,
                relief=tk.RAISED
            )
            card.grid(row=0, column=i, padx=10, pady=10, sticky="nsew")
            insights_frame.grid_columnconfigure(i, weight=1)
        
            tk.Label(
                card,
                text=title,
                font=("Segoe UI", 10, "bold"),
                bg="white",
                fg="#7f8c8d"
            ).pack(pady=(10, 5))
        
            tk.Label(
                card,
                text=str(value),
                font=("Segoe UI", 18, "bold"),
                bg="white",
                fg=color
            ).pack(pady=(0, 10))
    
        # Add summary text
        summary_frame = tk.Frame(insights_frame, bg="white", bd=0, highlightbackground="#bdc3c7", highlightthickness=1)
        summary_frame.grid(row=1, column=0, columnspan=3, padx=10, pady=10, sticky="nsew")
    
        summary_text = (
            f"Based on the last 14 days of sales data and forecasting for the next 7 days:\n\n"
            f"- {products_need_restock} products require restocking to meet predicted demand\n"
            f"- Total restocking quantity needed: {total_restock} units\n"
            f"- The product(s) with highest predicted demand: {', '.join(highest_demand_products)} with {max_demand} units needed"
        )
    
        tk.Label(
            summary_frame,
            text=summary_text,
            font=("Segoe UI", 10),
            bg="white",
            fg="#2d3436",
            justify=tk.LEFT,
            wraplength=800
        ).pack(padx=20, pady=20, anchor=tk.W)
        
    def plot_14_day_top_trend(self, parent_frame):
        fig = Figure(figsize=(8, 5), dpi=100)
        ax = fig.add_subplot(111)
        
        days = [(today - timedelta(days=i)).strftime("%d-%b") for i in range(13, -1, -1)]
        
        products_to_plot = [p for p in sales_data.keys() if p in aggregated_predictions]
        top_products = sorted(
            products_to_plot,
            key=lambda x: sum(qty for _, qty, _ in sales_data[x][-14:]),
            reverse=True
        )[:5]  # Show top 5 products
        
        colors = plt.cm.tab10.colors
        self.lines_14_top = []  # Store line objects for hover functionality
        
        for i, product in enumerate(top_products):
            data = sales_data[product]
            # Create aggregated sales dictionary
            sales_dict = {}
            for date, qty_sold, _ in data:
                date_str = date.strftime("%Y-%m-%d")
                if date_str in sales_dict:
                    sales_dict[date_str] += qty_sold
                else:
                    sales_dict[date_str] = qty_sold
            
            past_sales = [sales_dict.get(day, 0) for day in last_14_days]
            line, = ax.plot(days, past_sales[-14:], 
                           marker="o", 
                           linestyle="-", 
                           label=product,
                           color=colors[i],
                           linewidth=2,
                           markersize=6)
            self.lines_14_top.append(line)
        
        ax.set_title("Top 5 Products - 14-Day Sales Trend", fontsize=12, pad=20)
        ax.set_xlabel("Date", fontsize=10)
        ax.set_ylabel("Units Sold", fontsize=10)
        legend = ax.legend(loc="upper left", bbox_to_anchor=(1, 1), fontsize=9)
        ax.grid(True, linestyle="--", alpha=0.4)
        ax.tick_params(axis="x", rotation=45)
        ax.set_facecolor("#f9f9f9")
        fig.tight_layout()
        
        # Add hover functionality
        def on_hover(event):
            if event.inaxes == ax:
                for line in self.lines_14_top:
                    if line.contains(event)[0]:
                        line.set_linewidth(4)
                        line.set_alpha(1)
                        fig.canvas.draw_idle()
                        return
                for line in self.lines_14_top:
                    line.set_linewidth(2)
                    line.set_alpha(0.8)
                fig.canvas.draw_idle()
        
        def on_leave(event):
            for line in self.lines_14_top:
                line.set_linewidth(2)
                line.set_alpha(0.8)
            fig.canvas.draw_idle()
        
        fig.canvas.mpl_connect('motion_notify_event', on_hover)
        fig.canvas.mpl_connect('axes_leave_event', on_leave)
        
        canvas = FigureCanvasTkAgg(fig, master=parent_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
    def plot_14_day_all_trend(self, parent_frame):
        fig = Figure(figsize=(8, 5), dpi=100)
        ax = fig.add_subplot(111)
        
        days = [(today - timedelta(days=i)).strftime("%d-%b") for i in range(13, -1, -1)]
        
        products_to_plot = [p for p in sales_data.keys() if p in aggregated_predictions]
        colors = plt.cm.tab20.colors
        self.lines_14_all = []  # Store line objects for hover functionality
        
        for i, product in enumerate(products_to_plot):
            data = sales_data[product]
            # Create aggregated sales dictionary
            sales_dict = {}
            for date, qty_sold, _ in data:
                date_str = date.strftime("%Y-%m-%d")
                if date_str in sales_dict:
                    sales_dict[date_str] += qty_sold
                else:
                    sales_dict[date_str] = qty_sold
            
            past_sales = [sales_dict.get(day, 0) for day in last_14_days]
            line, = ax.plot(days, past_sales[-14:], 
                           marker="o", 
                           linestyle="-", 
                           label=product,
                           color=colors[i % len(colors)],
                           linewidth=1.5,
                           markersize=4,
                           alpha=0.7)
            self.lines_14_all.append(line)
        
        ax.set_title("All Products - 14-Day Sales Trend", fontsize=12, pad=20)
        ax.set_xlabel("Date", fontsize=10)
        ax.set_ylabel("Units Sold", fontsize=10)
        legend = ax.legend(loc="upper left", bbox_to_anchor=(1, 1), fontsize=8)
        ax.grid(True, linestyle="--", alpha=0.4)
        ax.tick_params(axis="x", rotation=45)
        ax.set_facecolor("#f9f9f9")
        fig.tight_layout()
        
        # Add hover functionality
        def on_hover(event):
            if event.inaxes == ax:
                for line in self.lines_14_all:
                    if line.contains(event)[0]:
                        line.set_linewidth(3)
                        line.set_alpha(1)
                        fig.canvas.draw_idle()
                        return
                for line in self.lines_14_all:
                    line.set_linewidth(1.5)
                    line.set_alpha(0.7)
                fig.canvas.draw_idle()
        
        def on_leave(event):
            for line in self.lines_14_all:
                line.set_linewidth(1.5)
                line.set_alpha(0.7)
            fig.canvas.draw_idle()
        
        fig.canvas.mpl_connect('motion_notify_event', on_hover)
        fig.canvas.mpl_connect('axes_leave_event', on_leave)
        
        canvas = FigureCanvasTkAgg(fig, master=parent_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
    def plot_30_day_top_trend(self, parent_frame):
        fig = Figure(figsize=(8, 5), dpi=100)
        ax = fig.add_subplot(111)
        
        last_30_days = [(today - timedelta(days=i)).strftime("%d-%b") for i in range(29, -1, -1)]
        products_to_plot = [p for p in sales_data.keys() if p in aggregated_predictions]
        
        top_products = sorted(
            products_to_plot,
            key=lambda x: sum(qty for _, qty, _ in sales_data[x][-30:]),
            reverse=True
        )[:5]  # Show top 5 products
        
        colors = plt.cm.tab10.colors
        self.lines_30_top = []  # Store line objects for hover functionality
        
        for i, product in enumerate(top_products):
            data = sales_data[product]
            # Create aggregated sales dictionary
            sales_dict = {}
            for date, qty_sold, _ in data:
                date_str = date.strftime("%Y-%m-%d")
                if date_str in sales_dict:
                    sales_dict[date_str] += qty_sold
                else:
                    sales_dict[date_str] = qty_sold
            
            past_sales_30 = [
                sales_dict.get((today - timedelta(days=i)).strftime("%Y-%m-%d"), 0)
                for i in range(29, -1, -1)
            ]
            line, = ax.plot(last_30_days, past_sales_30, 
                           marker="o", 
                           linestyle="-", 
                           label=product,
                           color=colors[i],
                           linewidth=2,
                           markersize=5,
                           alpha=0.9)
            self.lines_30_top.append(line)
        
        ax.set_title("Top 5 Products - 30-Day Sales Trend", fontsize=12, pad=20)
        ax.set_xlabel("Date", fontsize=10)
        ax.set_ylabel("Units Sold", fontsize=10)
        legend = ax.legend(loc="upper left", bbox_to_anchor=(1, 1), fontsize=9)
        ax.grid(True, linestyle="--", alpha=0.4)
        ax.tick_params(axis="x", rotation=45)
        ax.set_facecolor("#f9f9f9")
        fig.tight_layout()
        
        # Add hover functionality
        def on_hover(event):
            if event.inaxes == ax:
                for line in self.lines_30_top:
                    if line.contains(event)[0]:
                        line.set_linewidth(3)
                        line.set_alpha(1)
                        fig.canvas.draw_idle()
                        return
                for line in self.lines_30_top:
                    line.set_linewidth(2)
                    line.set_alpha(0.9)
                fig.canvas.draw_idle()
        
        def on_leave(event):
            for line in self.lines_30_top:
                line.set_linewidth(2)
                line.set_alpha(0.9)
            fig.canvas.draw_idle()
        
        fig.canvas.mpl_connect('motion_notify_event', on_hover)
        fig.canvas.mpl_connect('axes_leave_event', on_leave)
        
        canvas = FigureCanvasTkAgg(fig, master=parent_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
    def plot_30_day_all_trend(self, parent_frame):
        fig = Figure(figsize=(8, 5), dpi=100)
        ax = fig.add_subplot(111)
        
        last_30_days = [(today - timedelta(days=i)).strftime("%d-%b") for i in range(29, -1, -1)]
        products_to_plot = [p for p in sales_data.keys() if p in aggregated_predictions]
        
        colors = plt.cm.tab20.colors
        self.lines_30_all = []  # Store line objects for hover functionality
        
        for i, product in enumerate(products_to_plot):
            data = sales_data[product]
            # Create aggregated sales dictionary
            sales_dict = {}
            for date, qty_sold, _ in data:
                date_str = date.strftime("%Y-%m-%d")
                if date_str in sales_dict:
                    sales_dict[date_str] += qty_sold
                else:
                    sales_dict[date_str] = qty_sold
            
            past_sales_30 = [
                sales_dict.get((today - timedelta(days=i)).strftime("%Y-%m-%d"), 0)
                for i in range(29, -1, -1)
            ]
            line, = ax.plot(last_30_days, past_sales_30, 
                           marker="o", 
                           linestyle="-", 
                           label=product,
                           color=colors[i % len(colors)],
                           linewidth=1,
                           markersize=3,
                           alpha=0.6)
            self.lines_30_all.append(line)
        
        ax.set_title("All Products - 30-Day Sales Trend", fontsize=12, pad=20)
        ax.set_xlabel("Date", fontsize=10)
        ax.set_ylabel("Units Sold", fontsize=10)
        legend = ax.legend(loc="upper left", bbox_to_anchor=(1, 1), fontsize=8)
        ax.grid(True, linestyle="--", alpha=0.4)
        ax.tick_params(axis="x", rotation=45)
        ax.set_facecolor("#f9f9f9")
        fig.tight_layout()
        
        # Add hover functionality
        def on_hover(event):
            if event.inaxes == ax:
                for line in self.lines_30_all:
                    if line.contains(event)[0]:
                        line.set_linewidth(2)
                        line.set_alpha(1)
                        fig.canvas.draw_idle()
                        return
                for line in self.lines_30_all:
                    line.set_linewidth(1)
                    line.set_alpha(0.6)
                fig.canvas.draw_idle()
        
        def on_leave(event):
            for line in self.lines_30_all:
                line.set_linewidth(1)
                line.set_alpha(0.6)
            fig.canvas.draw_idle()
        
        fig.canvas.mpl_connect('motion_notify_event', on_hover)
        fig.canvas.mpl_connect('axes_leave_event', on_leave)
        
        canvas = FigureCanvasTkAgg(fig, master=parent_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
    def load_data(self):
        # Clear existing data
        for row in self.tree.get_children():
            self.tree.delete(row)
        
        # Get fresh current stock data
        current_stocks = fetch_current_stocks()
        
        # Insert data into treeview
        for i, (product, values) in enumerate(aggregated_predictions.items()):
            tags = ('evenrow',) if i % 2 == 0 else ('oddrow',)
            
            current_stock = current_stocks.get(product, 0)
            predicted_demand = values[0]
            restock_qty = max(0, predicted_demand - current_stock) if predicted_demand > current_stock else "-"
            
            self.tree.insert(
                "",
                tk.END,
                values=(
                    product,
                    current_stock,
                    round(predicted_demand),
                    restock_qty
                ),
                tags=tags
            )
        
        # Update status bar
        self.status_bar.config(text=f"Showing {len(aggregated_predictions)} products requiring attention | Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    def refresh_data(self):
        """Refresh all data from database"""
        global sales_data, aggregated_predictions, today, last_14_days
        
        try:
            # Reconnect to database in case connection was lost
            db.reconnect()
            
            # Fetch fresh data
            sales_data = fetch_sales_data()
            aggregated_predictions = calculate_predictions(sales_data)
            today = datetime.today().date()
            last_14_days = [(today - timedelta(days=i)).strftime("%Y-%m-%d") for i in range(14, -1, -1)]
            
            # Reload the table with fresh data
            self.load_data()
            
            # Update the graphs
            self.update_graphs()
            
            # Update insights tab
            self.update_insights_tab()
            
            # Show confirmation
            self.status_bar.config(text="Data refreshed successfully")
            self.root.after(3000, lambda: self.status_bar.config(
                text=f"Showing {len(aggregated_predictions)} products requiring attention | Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
            ))
        except Exception as e:
            messagebox.showerror("Refresh Error", f"Error refreshing data: {str(e)}")
            self.status_bar.config(text="Error refreshing data")
    
    def update_graphs(self):
        """Update the graphs with fresh data"""
        # Destroy existing graph frames
        for widget in self.tab2.winfo_children():
            widget.destroy()
        
        # Rebuild the graphs tab
        self.build_trends_tab()
    
    def update_insights_tab(self):
        """Update the insights tab with fresh data"""
        # Destroy existing insights tab widgets
        for widget in self.tab3.winfo_children():
            widget.destroy()
        
        # Rebuild the insights tab
        self.build_insights_tab()
    
    def sort_treeview(self, col, reverse):
        # Get all values from the treeview
        l = [(self.tree.set(k, col), k) for k in self.tree.get_children('')]
        
        # Handle numeric columns properly
        if col != "Product":
            l.sort(key=lambda t: float(t[0]) if t[0].replace('-', '').isdigit() else 0, reverse=reverse)
        else:
            l.sort(reverse=reverse)
        
        # Rearrange items in sorted positions
        for index, (val, k) in enumerate(l):
            self.tree.move(k, '', index)
        
        # Reverse sort next time
        self.tree.heading(col, command=lambda: self.sort_treeview(col, not reverse))
        
        # Reapply row colors
        for i, child in enumerate(self.tree.get_children()):
            self.tree.item(child, tags=('evenrow',) if i % 2 == 0 else ('oddrow',))
    
    def clear_filter(self):
        """Clear the filter and show all data"""
        self.filter_var.set("")  # Clear the filter text
    
        # First, delete all current items in the treeview
        for item in self.tree.get_children():
            self.tree.delete(item)
    
        # Then reload all the original data
        self.load_data()
    
        # Show confirmation message in status bar for 3 seconds
        original_text = self.status_bar.cget("text")
        self.status_bar.config(text="Filter cleared - showing all products")
        self.root.after(3000, lambda: self.status_bar.config(text=original_text))

    def filter_table(self, event=None):
        filter_text = self.filter_var.get().lower()
    
        # First, show all items
        for child in self.tree.get_children():
            self.tree.reattach(child, '', 'end')
    
        # If there's filter text, hide non-matching items
        if filter_text:
            for child in self.tree.get_children():
                product = self.tree.item(child)['values'][0].lower()
                if filter_text not in product:
                    self.tree.detach(child)
    
    def export_to_csv(self):
        try:
            import csv
            from datetime import datetime
            
            filename = f"restock_recommendations_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
            
            with open(filename, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(["Product", "Current Stock", "Predicted Demand (7 days)", "Restock Quantity"])
                
                for child in self.tree.get_children():
                    row = self.tree.item(child)['values']
                    writer.writerow(row)
            
            messagebox.showinfo(
                "Export Successful",
                f"Data exported successfully to {filename}",
                parent=self.root
            )
        except Exception as e:
            messagebox.showerror(
                "Export Error",
                f"An error occurred while exporting:\n{str(e)}",
                parent=self.root
            )

if __name__ == "__main__":
    root = tk.Tk()
    
    # Set theme (requires ttkthemes package - install with pip install ttkthemes)
    try:
        from ttkthemes import ThemedStyle
        style = ThemedStyle(root)
        style.set_theme("arc")
    except ImportError:
        pass
    
    app = ModernSalesAnalysisApp(root)
    root.mainloop()