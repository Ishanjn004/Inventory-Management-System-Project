from tkinter import *
from PIL import Image,ImageTk
from tkinter import ttk,messagebox


class BillClass:
    def __init__(self,root):
        self.root=root
        self.root.geometry("2560x980+0+0")
        self.root.title("Inventory Management System")
        self.root.config(bg="white")

        #=========================Title=========================
        self.icon_title=PhotoImage(file="images/logo1.png")
        title=Label(self.root,text="Inventory Management System",image=self.icon_title,compound=LEFT,font=("times new roman",40,"bold"),bg="#1b2631",fg="white",anchor="w",padx=20).place(x=0,y=0,relwidth=1,height=70)

        #=========================Button_Logout=========================
        btn_logout=Button(self.root,text="Logout",font=("times new roman",15,"bold"),bg="yellow",cursor="hand2").place(x=1500,y=10,width=150,height=50)

        #=========================Clock=========================
        self.lbl_clock=Label(self.root,text="Welcome to Inventory Management System\t\t Date: DD-MM-YYYY\t\t Time: HH:MM:SS",font=("times new roman",15),bg="#2c3e50",fg="white")
        self.lbl_clock.place(x=0,y=70,relwidth=1,height=30)

        #====Product Frame=======================================
        self.var_search=StringVar()
        ProductFrame1=Frame(self.root,bd=4,relief=RIDGE,bg="white")
        ProductFrame1.place(x=6,y=110,width=570,height=800)

        pTitle=Label(ProductFrame1,text="All Products",font=("goudy old style",20,"bold"),bg="#1c2833",fg="white").pack(side=TOP,fill=X)

        ProductFrame2=Frame(ProductFrame1,bd=2,relief=RIDGE,bg="white")
        ProductFrame2.place(x=2,y=42,width=558,height=110)

        lbl_search=Label(ProductFrame2,text="Search Product | By Name ",font=("times new roman",18,"bold"),bg="white",fg="#196f3d").place(x=2,y=5)

        lbl_search=Label(ProductFrame2,text="Product Name",font=("times new roman",18,"bold"),bg="white").place(x=20,y=55)
        txt_search=Entry(ProductFrame2,textvariable=self.var_search,font=("times new roman",18),bg="#d6eaf8").place(x=180,y=60,width=200,height=25)
        btn_search=Button(ProductFrame2,text="Search",font=("goudy old style",15),bg="#212f3c",fg="white",cursor="hand2").place(x=400,y=57,width=100,height=28)
        btn_show_all=Button(ProductFrame2,text="Show All",font=("goudy old style",15),bg="#641e16",fg="white",cursor="hand2").place(x=400,y=20,width=100,height=28)

        ProductFrame3=Frame(ProductFrame1,bd=3,relief=RIDGE)
        ProductFrame3.place(x=2,y=160,width=558,height=600)

        scrolly=Scrollbar(ProductFrame3,orient=VERTICAL)
        scrollx=Scrollbar(ProductFrame3,orient=HORIZONTAL)
        
        self.product_Table=ttk.Treeview(ProductFrame3,columns=("pid","name","price","qty","status"),yscrollcommand=scrolly.set,xscrollcommand=scrollx.set)
        scrollx.pack(side=BOTTOM,fill=X)
        scrolly.pack(side=RIGHT,fill=Y)
        scrollx.config(command=self.product_Table.xview)
        scrolly.config(command=self.product_Table.yview)
        self.product_Table.heading("pid",text="PID")
        self.product_Table.heading("name",text="Name")
        self.product_Table.heading("price",text="Price")
        self.product_Table.heading("qty",text="Quantity")
        self.product_Table.heading("status",text="Status")
        self.product_Table["show"]="headings"
        self.product_Table.column("pid",width=90)
        self.product_Table.column("name",width=100)
        self.product_Table.column("price",width=100)
        self.product_Table.column("qty",width=100)
        self.product_Table.column("status",width=100)
        
        self.product_Table.pack(fill=BOTH,expand=1)
        # self.product_Table.bind("<ButtonRelease-1>",self.get_data)
        lbl_note=Label(ProductFrame1,text="        Note: 'Enter 0 Quantity to remove product from the Cart'",font=("goudy old style",15),anchor='w',bg="white",fg="#cb4335").pack(side=BOTTOM,fill=X)
        


if __name__=="__main__":
    root=Tk()
    obj=BillClass(root)
    root.mainloop()