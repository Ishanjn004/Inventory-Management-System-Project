from tkinter import *
from PIL import Image,ImageTk
from tkinter import ttk,messagebox
import mysql.connector
import os

class salesClass:
    def __init__(self,root):
        self.root=root
        self.root.geometry("1290x700+380+150")
        self.root.title("Inventory Management System")
        self.root.config(bg="white")
        self.root.focus_force()

        self.bill_list=[]
        self.var_invoice=StringVar()

        lbl_title=Label(self.root,text="View Customer Bills",font=("goudy old style",30,"bold"),bg="#212f3d",fg="white",bd=3,relief=RIDGE).pack(side=TOP,fill=X,padx=10,pady=20)

        lbl_invoice=Label(self.root,text="Invoice No.",font=("times new roman",20,"bold"),bg="white").place(x=50,y=100)
        txt_invoice=Entry(self.root,textvariable=self.var_invoice,font=("times new roman",20,"bold"),bg="#d6eaf8").place(x=200,y=105,width=200,height=30)

        btn_search=Button(self.root,text="Search",command=self.search,font=("times new roman",18,"bold"),bg="#0b5345",fg="white",cursor="hand2").place(x=420,y=105,width=150,height=30)
        btn_clear=Button(self.root,text="Clear",command=self.clear,font=("times new roman",18,"bold"),bg="#424949",fg="white",cursor="hand2").place(x=580,y=105,width=150,height=30)

        sales_frame=Frame(self.root,bd=3,relief=RIDGE)
        sales_frame.place(x=50,y=150,width=300,height=500)

        scrolly=Scrollbar(sales_frame,orient=VERTICAL)

        self.Sales_List=Listbox(sales_frame,font=("goudy old style",16),bg="white",yscrollcommand=scrolly.set)
        scrolly.pack(side=RIGHT,fill=Y)
        scrolly.config(command=self.Sales_List.yview)
        self.Sales_List.pack(fill=BOTH,expand=1)
        self.Sales_List.bind("<ButtonRelease-1>",self.get_data)

        bill_frame=Frame(self.root,bd=3,relief=RIDGE)
        bill_frame.place(x=400,y=150,width=520,height=500)

        lbl_title2=Label(bill_frame,text="Customer Bill Area",font=("goudy old style",20,"bold"),bg="#273746",fg="white").pack(side=TOP,fill=X)

        scrolly2=Scrollbar(bill_frame,orient=VERTICAL)

        self.bill_area=Text(bill_frame,bg="#d6eaf8",yscrollcommand=scrolly2.set)
        scrolly2.pack(side=RIGHT,fill=Y)
        scrolly2.config(command=self.bill_area.yview)
        self.bill_area.pack(fill=BOTH,expand=1)

        self.bill_photo=Image.open("images/cat2.jpg")
        self.bill_photo=self.bill_photo.resize((300,400),Image.Resampling.LANCZOS)
        self.bill_photo=ImageTk.PhotoImage(self.bill_photo)

        lbl_image=Label(self.root,image=self.bill_photo,bd=0)
        lbl_image.place(x=940,y=180)

        self.show()

        #==========================================================================
    def show(self):
        del self.bill_list[:]
        self.Sales_List.delete(0,END)
        for i in os.listdir("bills"):
            if i.split(".")[-1]=="txt":
                self.Sales_List.insert(END,i)
                self.bill_list.append(i.split(".")[0])

    def get_data(self,ev):
        index_=self.Sales_List.curselection()
        file_name=self.Sales_List.get(index_)
        # print(file_name)
        self.bill_area.delete("1.0",END)
        fp=open(f"bills/{file_name}","r")
        for i in fp:
            self.bill_area.insert(END,i)

    def search(self):
        if self.var_invoice.get()=="":
            messagebox.showerror("Error","Invoice Number Required",parent=self.root)
        else:
            if self.var_invoice.get() in self.bill_list:
                fp=open(f"bills/{self.var_invoice.get()}.txt","r")
                self.bill_area.delete("1.0",END)
                for i in fp:
                    self.bill_area.insert(END,i)
                fp.close()
            else:
                messagebox.showerror("Error",f"No record found with Invoice No. {self.var_invoice.get()}",parent=self.root)

    def clear(self):
        self.show()
        self.bill_area.delete("1.0",END)


if __name__=="__main__":
    root=Tk()
    obj=salesClass(root)
    root.mainloop()