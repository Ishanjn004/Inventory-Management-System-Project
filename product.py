from tkinter import *
from PIL import Image,ImageTk
from tkinter import ttk,messagebox
import mysql.connector
import pandas as pd
from tkinter import filedialog

class productClass:
    def __init__(self,root):
        self.root=root
        self.root.geometry("1290x700+380+150")
        self.root.title("Inventory Management System")
        self.root.config(bg="white")
        self.root.focus_force()

        #----------- variables -------------
        self.var_cat=StringVar()
        self.cat_list=[]
        self.sup_list=[]
        self.fetch_cat_sup()
        self.var_pid=StringVar()
        self.var_sup=StringVar()
        self.var_name=StringVar()
        self.var_price=StringVar()
        self.var_qty=StringVar()
        self.var_status=StringVar()
        self.var_searchby=StringVar()
        self.var_searchtxt=StringVar()

        product_Frame=Frame(self.root,bd=2,relief=RIDGE,bg="white")
        product_Frame.place(x=10,y=10,width=560,height=650)

        #------------ title --------------
        title=Label(product_Frame,text="Manage Product Details",font=("goudy old style",24,"bold"),bg="#784212",fg="white",height=2).pack(side=TOP,fill=X)

        lbl_category=Label(product_Frame,text="Category",font=("goudy old style",18),bg="white").place(x=30,y=100)
        lbl_supplier=Label(product_Frame,text="Supplier",font=("goudy old style",18),bg="white").place(x=30,y=150)
        lbl_product_name=Label(product_Frame,text="Name",font=("goudy old style",18),bg="white").place(x=30,y=200)
        lbl_price=Label(product_Frame,text="Price",font=("goudy old style",18),bg="white").place(x=30,y=250)
        lbl_qty=Label(product_Frame,text="Quantity",font=("goudy old style",18),bg="white").place(x=30,y=300)
        lbl_status=Label(product_Frame,text="Status",font=("goudy old style",18),bg="white").place(x=30,y=350)

        cmb_cat=ttk.Combobox(product_Frame,textvariable=self.var_cat,values=self.cat_list,state='readonly',justify=CENTER,font=("goudy old style",15))
        cmb_cat.place(x=150,y=100,width=200)
        cmb_cat.current(0)

        cmb_sup=ttk.Combobox(product_Frame,textvariable=self.var_sup,values=self.sup_list,state='readonly',justify=CENTER,font=("goudy old style",15))
        cmb_sup.place(x=150,y=150,width=200)
        cmb_sup.current(0)

        txt_name=Entry(product_Frame,textvariable=self.var_name,font=("goudy old style",15),bg="lightyellow").place(x=150,y=200,width=200)
        txt_price=Entry(product_Frame,textvariable=self.var_price,font=("goudy old style",15),bg="lightyellow").place(x=150,y=250,width=200)
        txt_qty=Entry(product_Frame,textvariable=self.var_qty,font=("goudy old style",15),bg="lightyellow").place(x=150,y=300,width=200)

        cmb_status=ttk.Combobox(product_Frame,textvariable=self.var_status,values=("Active","Inactive"),state='readonly',justify=CENTER,font=("goudy old style",15))
        cmb_status.place(x=150,y=350,width=200)
        cmb_status.current(0)

        #-------------- buttons -----------------
        btn_add=Button(product_Frame,text="Save",command=self.add,font=("goudy old style",15),bg="#2196f3",fg="white",cursor="hand2").place(x=10,y=400,width=100,height=40)
        btn_update=Button(product_Frame,text="Update",command=self.update,font=("goudy old style",15),bg="#4caf50",fg="white",cursor="hand2").place(x=120,y=400,width=100,height=40)
        btn_delete=Button(product_Frame,text="Delete",command=self.delete,font=("goudy old style",15),bg="#f44336",fg="white",cursor="hand2").place(x=230,y=400,width=100,height=40)
        btn_exp=Button(product_Frame,text="Export",command=self.export_excel,font=("goudy old style",15),bg="#1a5276",fg="white",cursor="hand2").place(x=340,y=400,width=100,height=40)
        btn_exp=Button(product_Frame,text="Import",command=self.import_excel,font=("goudy old style",15),bg="#935116",fg="white",cursor="hand2").place(x=450,y=400,width=100,height=40)
        btn_low_stck=Button(product_Frame,text="Low Stock",command=self.show_low_stock,font=("goudy old style",15),bg="#c0392b",fg="white",cursor="hand2").place(x=10,y=450,width=120,height=40)
        btn_out_of_stck=Button(product_Frame,text="Out of Stock",command=self.show_out_of_stock,font=("goudy old style",15),bg="#515a5a",fg="white",cursor="hand2").place(x=140,y=450,width=140,height=40)
        btn_stck_anal=Button(product_Frame,text="Stock Analysis",command=self.stock_analysis,font=("goudy old style",15),bg="#5b2c6f",fg="white",cursor="hand2").place(x=290,y=450,width=150,height=40)
        btn_clear=Button(product_Frame,text="Clear",command=self.clear,font=("goudy old style",15),bg="#607d8b",fg="white",cursor="hand2").place(x=450,y=450,width=100,height=40)

        #---------- Search Frame -------------
        SearchFrame=LabelFrame(self.root,text="Search Product",font=("goudy old style",12,"bold"),bd=2,relief=RIDGE,bg="white")
        SearchFrame.place(x=580,y=10,width=600,height=80)

        #------------ options ----------------
        cmb_search=ttk.Combobox(SearchFrame,textvariable=self.var_searchby,values=("Select","Category","Supplier","Name"),state='readonly',justify=CENTER,font=("goudy old style",15))
        cmb_search.place(x=10,y=10,width=180)
        cmb_search.current(0)

        txt_search=Entry(SearchFrame,textvariable=self.var_searchtxt,font=("goudy old style",15),bg="lightyellow").place(x=200,y=10)
        btn_search=Button(SearchFrame,text="Search",command=self.search,font=("goudy old style",15),bg="#4caf50",fg="white",cursor="hand2").place(x=410,y=9,width=150,height=30)

        #------------ product details -------------
        product_frame=Frame(self.root,bd=3,relief=RIDGE)
        product_frame.place(x=580,y=100,width=690,height=560)

        scrolly=Scrollbar(product_frame,orient=VERTICAL)
        scrollx=Scrollbar(product_frame,orient=HORIZONTAL)
        
        self.ProductTable=ttk.Treeview(product_frame,columns=("pid","Category","Supplier","name","price","qty","status"),yscrollcommand=scrolly.set,xscrollcommand=scrollx.set)
        scrollx.pack(side=BOTTOM,fill=X)
        scrolly.pack(side=RIGHT,fill=Y)
        scrollx.config(command=self.ProductTable.xview)
        scrolly.config(command=self.ProductTable.yview)
        self.ProductTable.heading("pid",text="P ID")
        self.ProductTable.heading("Category",text="Category")
        self.ProductTable.heading("Supplier",text="Suppler")
        self.ProductTable.heading("name",text="Name")
        self.ProductTable.heading("price",text="Price")
        self.ProductTable.heading("qty",text="Quantity")
        self.ProductTable.heading("status",text="Status")
        self.ProductTable["show"]="headings"
        self.ProductTable.column("pid",width=80)
        self.ProductTable.column("Category",width=100)
        self.ProductTable.column("Supplier",width=100)
        self.ProductTable.column("name",width=100)
        self.ProductTable.column("price",width=100)
        self.ProductTable.column("qty",width=100)
        self.ProductTable.column("status",width=100)
        
        self.ProductTable.pack(fill=BOTH,expand=1)
        self.ProductTable.bind("<ButtonRelease-1>",self.get_data)
        self.show()
        self.fetch_cat_sup()
#-----------------------------------------------------------------------------------------------------
    def fetch_cat_sup(self):
        self.cat_list.append("Empty")
        self.sup_list.append("Empty")

        try:
            connection = mysql.connector.connect(
                host="localhost",
                user="root",
                password="ishan",
                database="IMS"
            )
            if connection.is_connected():
                cursor = connection.cursor()
                cursor.execute("select name from category")
                cat=cursor.fetchall()
                if len(cat)>0:
                    del self.cat_list[:]
                    self.cat_list.append("Select")
                    for i in cat:
                        self.cat_list.append(i[0])
                cursor.execute("select name from supplier")
                sup=cursor.fetchall()
                if len(sup)>0:
                    del self.sup_list[:]
                    self.sup_list.append("Select")
                    for i in sup:
                        self.sup_list.append(i[0])
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to : {str(ex)}")

    def add(self):
        try:
            connection = mysql.connector.connect(
                host="localhost",
                user="root",
                password="ishan",
                database="IMS"
            )
            if connection.is_connected():
                cursor = connection.cursor()
                if self.var_cat.get()=="Select" or self.var_cat.get()=="Empty" or self.var_sup.get()=="Select" or self.var_sup.get()=="Empty" or self.var_name.get()=="" or self.var_price.get()=="" or self.var_qty.get()=="": 
                    messagebox.showerror("Error","All fields are required",parent=self.root)
                else:
                    cursor.execute("select * from product where name=%s",(self.var_name.get(),))
                    row=cursor.fetchone()
                    if row!=None:
                        messagebox.showerror("Error","Product already exists",parent=self.root)
                    else:
                        cursor.execute("insert into product (Category,Supplier,name,price,qty,status) values(%s,%s,%s,%s,%s,%s)",(
                            self.var_cat.get(),
                            self.var_sup.get(),
                            self.var_name.get(),
                            self.var_price.get(),
                            self.var_qty.get(),
                            self.var_status.get(),
                        ))
                        connection.commit()
                        messagebox.showinfo("Success","Product added successfully",parent=self.root)
                        self.clear()
                        self.show()
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to: {str(ex)}")

    def show(self):
        try:
            connection = mysql.connector.connect(
                host="localhost",
                user="root",
                password="ishan",
                database="IMS"
            )
            if connection.is_connected():
                cursor = connection.cursor()
                cursor.execute("select * from product")
                rows=cursor.fetchall()
                self.ProductTable.delete(*self.ProductTable.get_children())
                for row in rows:
                    self.ProductTable.insert('',END,values=row)
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to: {str(ex)}")

    def get_data(self,ev):
        f=self.ProductTable.focus()
        content=(self.ProductTable.item(f))
        row=content['values']
        self.var_pid.set(row[0])
        self.var_cat.set(row[1])
        self.var_sup.set(row[2])
        self.var_name.set(row[3])
        self.var_price.set(row[4])
        self.var_qty.set(row[5])
        self.var_status.set(row[6])

    def update(self):
        try:
            connection = mysql.connector.connect(
                host="localhost",
                user="root",
                password="ishan",
                database="IMS"
            )
            if connection.is_connected():
                cursor = connection.cursor()
                if self.var_pid.get()=="": 
                    messagebox.showerror("Error","Please select Product ID from list!!!",parent=self.root)
                else:
                    cursor.execute("select * from product where pid=%s",(self.var_pid.get(),))
                    row=cursor.fetchone()
                    if row==None:
                        messagebox.showerror("Error","Invalid Product ID",parent=self.root)
                    else:
                        cursor.execute("update product set Category=%s,Supplier=%s,name=%s,price=%s,qty=%s,status=%s where pid=%s",(
                            self.var_cat.get(),
                            self.var_sup.get(),
                            self.var_name.get(),
                            self.var_price.get(),
                            self.var_qty.get(),
                            self.var_status.get(),
                            self.var_pid.get(),
                        ))
                        connection.commit()
                        messagebox.showinfo("Success","Product updated successfully",parent=self.root)
                        self.clear()
                        self.show()
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to: {str(ex)}")

    def delete(self):
        try:
            connection = mysql.connector.connect(
                host="localhost",
                user="root",
                password="ishan",
                database="IMS"
            )
            if connection.is_connected():
                cursor = connection.cursor()
                if self.var_pid.get()=="": 
                    messagebox.showerror("Error","Select Product from the list!!!",parent=self.root)
                else:
                    cursor.execute("select * from product where pid=%s",(self.var_pid.get(),))
                    row=cursor.fetchone()
                    if row==None:
                        messagebox.showerror("Error","Invalid Product ID",parent=self.root)
                    else:
                        op=messagebox.askyesno("Confirm","Do you really want to delete?",parent=self.root)
                        if op==True:
                            cursor.execute("delete from product where pid=%s",(self.var_pid.get(),))
                            connection.commit()
                            messagebox.showinfo("Success","Product deleted successfully",parent=self.root)
                            self.show()
                            self.clear()
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to: {str(ex)}")

    def clear(self):
        self.var_cat.set("Select")
        self.var_sup.set("Select")
        self.var_name.set("")
        self.var_price.set("")
        self.var_qty.set("")
        self.var_status.set("Active")
        self.var_pid.set("")
        self.var_searchby.set("Select")
        self.var_searchtxt.set("")
        self.show()

    
    def search(self):
        try:
            connection = mysql.connector.connect(
                host="localhost",
                user="root",
                password="ishan",
                database="IMS"
            )
            if connection.is_connected():
                cursor = connection.cursor()
                if self.var_searchby.get()=="Select":
                    messagebox.showerror("Error","Select Search By option",parent=self.root)
                elif self.var_searchtxt.get()=="":
                    messagebox.showerror("Error","Search input should be required",parent=self.root)
                else:
                    cursor.execute("select * from product where "+self.var_searchby.get()+" LIKE '%"+self.var_searchtxt.get()+"%'")
                    rows=cursor.fetchall()
                    if len(rows)!=0:
                        self.ProductTable.delete(*self.ProductTable.get_children())
                        for row in rows:
                            self.ProductTable.insert('',END,values=row)
                    else:
                        messagebox.showerror("Error","No record found!!!",parent=self.root)
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to : {str(ex)}")

    def export_excel(self):
        try:
            connection = mysql.connector.connect(
                host="localhost",
                user="root",
                password="ishan",
                database="IMS"
            )
            if connection.is_connected():
                cursor = connection.cursor()
                cursor.execute("SELECT * FROM product")
                rows = cursor.fetchall()

                if not rows:
                    messagebox.showinfo("Info", "No data to export", parent=self.root)
                    return

                # Creating DataFrame
                df = pd.DataFrame(rows, columns=["Product ID", "Category", "Supplier", "Name", "Price", "Quantity", "Status"])

                # Ask file location
                file_path = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel files", "*.xlsx")])
                if file_path:
                    df.to_excel(file_path, index=False, engine='openpyxl')
                    messagebox.showinfo("Success", f"Data exported successfully to {file_path}", parent=self.root)
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)

    def import_excel(self):
        try:
            # Ask for Excel file to import
            file_path = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx")])
            if file_path == "":
                return  # If user cancels the file dialog

            df = pd.read_excel(file_path)

            required_columns = {"Category", "Supplier", "Name", "Price", "Quantity", "Status"}
            if not required_columns.issubset(set(df.columns)):
                messagebox.showerror("Error", f"Excel file must contain columns: {required_columns}", parent=self.root)
                return

            connection = mysql.connector.connect(
                host="localhost",
                user="root",
                password="ishan",
                database="IMS"
            )
            if connection.is_connected():
                cursor = connection.cursor()
                inserted = 0
                for _, row in df.iterrows():
                    # Check if product name already exists
                    cursor.execute("SELECT * FROM product WHERE name=%s", (row["Name"],))
                    exists = cursor.fetchone()
                    if not exists:
                        cursor.execute(
                            "INSERT INTO product (Category, Supplier, name, price, qty, status) VALUES (%s, %s, %s, %s, %s, %s)",
                            (
                                row["Category"],
                                row["Supplier"],
                                row["Name"],
                                row["Price"],
                                row["Quantity"],
                                row["Status"]
                            )
                        )
                        inserted += 1

                connection.commit()
                messagebox.showinfo("Success", f"{inserted} products imported successfully!", parent=self.root)
                self.show()
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)

    def stock_analysis(self):
        try:
            connection = mysql.connector.connect(
                host="localhost",
                user="root",
                password="ishan",
                database="IMS"
            )
            if connection.is_connected():
                cursor = connection.cursor()
                cursor.execute("SELECT * FROM product")
                rows = cursor.fetchall()

                if not rows:
                    messagebox.showinfo("Info", "No product data found", parent=self.root)
                    return

                total_items = len(rows)
                low_stock = [row for row in rows if int(row[5]) <= 5]
                out_of_stock = [row for row in rows if int(row[5]) == 0]
                total_value = sum(float(row[4]) * int(row[5]) for row in rows)

                # Category-wise count
                cursor.execute("SELECT Category, COUNT(*) FROM product GROUP BY Category")
                category_data = cursor.fetchall()

                # Create a popup
                analysis_win = Toplevel(self.root)
                analysis_win.title("Stock Analysis Report")
                analysis_win.geometry("500x500+500+200")
                analysis_win.config(bg="white")

                title = Label(analysis_win, text="📦 Stock Analysis", font=("goudy old style", 20, "bold"), bg="white", fg="#333")
                title.pack(pady=10)

                Label(analysis_win, text=f"🧾 Total Products: {total_items}", font=("goudy old style", 16), bg="white").pack(anchor="w", padx=20, pady=5)
                Label(analysis_win, text=f"📉 Out of Stock: {len(out_of_stock)}", font=("goudy old style", 16), fg="red", bg="white").pack(anchor="w", padx=20, pady=5)
                Label(analysis_win, text=f"⚠️ Low Stock (<=5): {len(low_stock)}", font=("goudy old style", 16), fg="orange", bg="white").pack(anchor="w", padx=20, pady=5)
                Label(analysis_win, text=f"💰 Total Inventory Value: ₹{total_value:.2f}", font=("goudy old style", 16), fg="green", bg="white").pack(anchor="w", padx=20, pady=5)

                Label(analysis_win, text="📊 Category-wise Distribution:", font=("goudy old style", 16, "bold"), bg="white").pack(anchor="w", padx=20, pady=10)
                for cat, count in category_data:
                    Label(analysis_win, text=f" - {cat}: {count} item(s)", font=("goudy old style", 15), bg="white").pack(anchor="w", padx=40)

        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)

    def show_out_of_stock(self):
        try:
            connection = mysql.connector.connect(
                host="localhost",
                user="root",
                password="ishan",
                database="IMS"
            )
            if connection.is_connected():
                cursor = connection.cursor()
                cursor.execute("SELECT * FROM product WHERE qty = 0")
                rows = cursor.fetchall()
                self.ProductTable.delete(*self.ProductTable.get_children())
                for row in rows:
                    self.ProductTable.insert('', END, values=row, tags=('low_stock',))
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}")


    def show_low_stock(self):
        try:
            connection = mysql.connector.connect(
                host="localhost",
                user="root",
                password="ishan",
                database="IMS"
            )
            if connection.is_connected():
                cursor = connection.cursor()
                cursor.execute("SELECT * FROM product WHERE qty <= 5")
                rows = cursor.fetchall()
                self.ProductTable.delete(*self.ProductTable.get_children())
                for row in rows:
                    self.ProductTable.insert('', END, values=row, tags=('low_stock',))
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}")



if __name__=="__main__":
    root=Tk()
    obj=productClass(root)
    root.mainloop()