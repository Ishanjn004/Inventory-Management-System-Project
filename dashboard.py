from tkinter import *
from PIL import Image,ImageTk
from employee import employeeClass
from supplier import supplierClass
from category import categoryClass
from product import productClass
from sales import salesClass
from sales_an import sales_analysis_Class
from sales_analysis import ModernSalesAnalysisApp
from return_supplier import purchase_ret_Class
import mysql.connector
from tkinter import ttk,messagebox
import os
import time

class IMS:
    def __init__(self,root):
        self.root=root
        self.root.geometry("2560x980+0+0")
        self.root.title("Inventory Management System")
        self.root.config(bg="white")

        #=========================Title=========================
        self.icon_title=PhotoImage(file="images/logo1.png")
        title=Label(self.root,text="Inventory Management System",image=self.icon_title,compound=LEFT,font=("times new roman",40,"bold"),bg="#1b2631",fg="white",anchor="w",padx=20).place(x=0,y=0,relwidth=1,height=70)

        #=========================Button_Logout=========================
        btn_logout=Button(self.root,text="Logout",command=self.logout,font=("times new roman",15,"bold"),bg="yellow",cursor="hand2").place(x=1500,y=10,width=150,height=50)

        #=========================Clock=========================
        self.lbl_clock=Label(self.root,text="Welcome to Inventory Management System\t\t Date: DD-MM-YYYY\t\t Time: HH:MM:SS",font=("times new roman",15),bg="#2c3e50",fg="white")
        self.lbl_clock.place(x=0,y=70,relwidth=1,height=30)

        #=========================Left Menu=========================
        self.MenuLogo=Image.open("images/menu_im.png")
        self.MenuLogo=self.MenuLogo.resize((200,300),Image.Resampling.LANCZOS)
        self.MenuLogo=ImageTk.PhotoImage(self.MenuLogo)
        LeftMenu=Frame(self.root,bd=2,relief=RIDGE,bg="white")
        LeftMenu.place(x=0,y=102,width=350,height=805) 
        self.icon_side=PhotoImage(file="images/side.png")  
        lbl_menu=Label(LeftMenu,image=self.MenuLogo)
        lbl_menu.pack(side=TOP,fill=X)

        lbl_menu=Label(LeftMenu,text="Menu",font=("times new roman",25,"bold"),bg="#0b5345",fg="#ecf0f1").pack(side=TOP,fill=X)
        btn_employee=Button(LeftMenu,text="Employee",command=self.employee,image=self.icon_side,compound=LEFT,padx=30,anchor="w",font=("times new roman",25,"bold"),bg="#f2f3f4",bd=3,cursor="hand2").pack(side=TOP,fill=X)
        btn_supplier=Button(LeftMenu,text="Supplier",command=self.supplier,image=self.icon_side,compound=LEFT,padx=30,anchor="w",font=("times new roman",25,"bold"),bg="#f2f3f4",bd=3,cursor="hand2").pack(side=TOP,fill=X)
        btn_category=Button(LeftMenu,text="Category",command=self.category,image=self.icon_side,compound=LEFT,padx=30,anchor="w",font=("times new roman",25,"bold"),bg="#f2f3f4",bd=3,cursor="hand2").pack(side=TOP,fill=X)
        btn_product=Button(LeftMenu,text="Product",command=self.product,image=self.icon_side,compound=LEFT,padx=30,anchor="w",font=("times new roman",25,"bold"),bg="#f2f3f4",bd=3,cursor="hand2").pack(side=TOP,fill=X)
        btn_sales=Button(LeftMenu,text="Sales",command=self.sales,image=self.icon_side,compound=LEFT,padx=30,anchor="w",font=("times new roman",25,"bold"),bg="#f2f3f4",bd=3,cursor="hand2").pack(side=TOP,fill=X)
        # btn_ret=Button(LeftMenu,text="Return Items",command=self.sales,image=self.icon_side,compound=LEFT,padx=30,anchor="w",font=("times new roman",25,"bold"),bg="#f2f3f4",bd=3,cursor="hand2").pack(side=TOP,fill=X)
        btn_purch_ret=Button(LeftMenu,text="Good Reciepts",command=self.purchase_ret,image=self.icon_side,compound=LEFT,padx=30,anchor="w",font=("times new roman",25,"bold"),bg="#f2f3f4",bd=3,cursor="hand2").pack(side=TOP,fill=X)
        btn_sales_anal=Button(LeftMenu,text="Sales Analysis",command=self.sales_analysis,image=self.icon_side,compound=LEFT,padx=30,anchor="w",font=("times new roman",25,"bold"),bg="#f2f3f4",bd=3,cursor="hand2").pack(side=TOP,fill=X)

        #=========================Content=========================
        self.lbl_employee=Label(self.root,text="Total Employees\n0",font=("goudy old style",28,"bold"),bg="#4a235a",fg="white",bd=5,relief=RIDGE)
        self.lbl_employee.place(x=500,y=150,width=400,height=200)

        self.lbl_supplier=Label(self.root,text="Total Suppliers\n0",font=("goudy old style",28,"bold"),bg="#641e16",fg="white",bd=5,relief=RIDGE)
        self.lbl_supplier.place(x=1050,y=150,width=400,height=200)

        self.lbl_category=Label(self.root,text="Total Cateories\n0",font=("goudy old style",28,"bold"),bg="#273746",fg="white",bd=5,relief=RIDGE)
        self.lbl_category.place(x=500,y=400,width=400,height=200)

        self.lbl_product=Label(self.root,text="Total Products\n0",font=("goudy old style",28,"bold"),bg="#4d5656",fg="white",bd=5,relief=RIDGE)
        self.lbl_product.place(x=1050,y=400,width=400,height=200)

        self.lbl_sales=Label(self.root,text="Total Sales\n0",font=("goudy old style",28,"bold"),bg="#1d8348",fg="white",bd=5,relief=RIDGE)
        self.lbl_sales.place(x=760,y=650,width=400,height=200)

        #=========================Footer=========================
        lbl_footer=Label(self.root,text="IMS - Inventory Mangaement System | Minor Project\nFor any Technical Issue Contact: 8595791213",font=("times new roman",12),bg="#2c3e50",fg="white").pack(side=BOTTOM,fill=X)

        self.update_content()

    #=========================Include other files=========================    
    def employee(self):
        self.new_win=Toplevel(self.root)
        self.new_obj=employeeClass(self.new_win)
    def supplier(self):
        self.new_win=Toplevel(self.root)
        self.new_obj=supplierClass(self.new_win)
    def category(self):
        self.new_win=Toplevel(self.root)
        self.new_obj=categoryClass(self.new_win)
    def product(self):
        self.new_win=Toplevel(self.root)
        self.new_obj=productClass(self.new_win)
    def sales(self):
        self.new_win=Toplevel(self.root)
        self.new_obj=salesClass(self.new_win)
    def purchase_ret(self):
        self.new_win=Toplevel(self.root)
        self.new_obj=purchase_ret_Class(self.new_win)
    # def sales_analysis(self):
    #     self.new_win=Toplevel(self.root)
    #     self.new_obj=sales_analysis_Class(self.new_win)
    def sales_analysis(self):
        self.new_win=Toplevel(self.root)
        self.new_obj=ModernSalesAnalysisApp(self.new_win)

    def update_content(self):
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="ishan",
            database="IMS"
        )
        try:
            cursor = connection.cursor()
            cursor.execute("Select * from product")
            product=cursor.fetchall()
            self.lbl_product.config(text=f"Total Products\n{str(len(product))}")

            cursor.execute("Select * from supplier")
            supplier=cursor.fetchall()
            self.lbl_supplier.config(text=f"Total Suppliers\n{str(len(supplier))}")

            cursor.execute("Select * from category")
            category=cursor.fetchall()
            self.lbl_category.config(text=f"Total Categories\n{str(len(category))}")

            cursor.execute("Select * from employee")
            emp=cursor.fetchall()
            self.lbl_employee.config(text=f"Total Employees\n{str(len(emp))}")

            bill=len(os.listdir("bills"))
            self.lbl_sales.config(text=f"Total Sales\n{str(bill)}")

            time_=time.strftime("%H:%M:%S")
            date_=time.strftime("%d-%m-%Y")
            self.lbl_clock.config(text=f"Welcome to Inventory Management System\t\t Date: {str(date_)}\t\t Time: {str(time_)}")
            self.lbl_clock.after(200,self.update_content)

        except Exception as ex:
            messagebox.showerror("Error",f"Error due to: {str(ex)}")

    def logout(self):
        self.root.destroy()
        os.system('python login.py')


if __name__=="__main__":
    root=Tk()
    obj=IMS(root)
    root.mainloop()
