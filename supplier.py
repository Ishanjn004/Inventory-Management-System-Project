from tkinter import*
from PIL import Image,ImageTk
from tkinter import ttk,messagebox
import mysql.connector

class supplierClass:
    def __init__(self,root):
        self.root=root
        self.root.geometry("1290x700+380+150")
        self.root.title("Inventory Management System | Nishant Gupta")
        self.root.config(bg="white")
        self.root.resizable(False,False)
        self.root.focus_force()

        #------------ all variables --------------
        self.var_searchby=StringVar()
        self.var_searchtxt=StringVar()
        self.var_sup_invoice=StringVar()
        self.var_name=StringVar()
        self.var_contact=StringVar()
        
        
        #---------- Search Frame -------------
        lbl_search=Label(self.root,text="Invoice No.",bg="white",font=("goudy old style",15))
        lbl_search.place(x=850,y=80)

        txt_search=Entry(self.root,textvariable=self.var_searchtxt,font=("goudy old style",15),bg="lightyellow").place(x=950,y=80,width=160)
        btn_search=Button(self.root,command=self.search,text="Search",font=("goudy old style",15),bg="#4caf50",fg="white",cursor="hand2").place(x=1130,y=79,width=100,height=28)

        #-------------- title ---------------
        title=Label(self.root,text="Supplier Details",font=("goudy old style",20,"bold"),bg="#0f4d7d",fg="white").place(x=50,y=10,width=1180,height=40)

        #-------------- content ---------------
        #---------- row 1 ----------------
        lbl_supplier_invoice=Label(self.root,text="Invoice No.",font=("goudy old style",15),bg="white").place(x=50,y=80)
        txt_supplier_invoice=Entry(self.root,textvariable=self.var_sup_invoice,font=("goudy old style",15),bg="lightyellow").place(x=180,y=80,width=180)
        
        #---------- row 2 ----------------
        lbl_name=Label(self.root,text="Name",font=("goudy old style",15),bg="white").place(x=50,y=120)
        txt_name=Entry(self.root,textvariable=self.var_name,font=("goudy old style",15),bg="lightyellow").place(x=180,y=120,width=180)
        
        #---------- row 3 ----------------
        lbl_contact=Label(self.root,text="Contact",font=("goudy old style",15),bg="white").place(x=50,y=160)
        txt_contact=Entry(self.root,textvariable=self.var_contact,font=("goudy old style",15),bg="lightyellow").place(x=180,y=160,width=180)
        
        #---------- row 4 ----------------
        lbl_desc=Label(self.root,text="Description",font=("goudy old style",15),bg="white").place(x=50,y=200)
        self.txt_desc=Text(self.root,font=("goudy old style",15),bg="lightyellow")
        self.txt_desc.place(x=180,y=200,width=470,height=120)
        
        #-------------- buttons -----------------
        btn_add=Button(self.root,text="Save",command=self.add,font=("goudy old style",15),bg="#2196f3",fg="white",cursor="hand2").place(x=180,y=370,width=110,height=35)
        btn_update=Button(self.root,text="Update",command=self.update,font=("goudy old style",15),bg="#4caf50",fg="white",cursor="hand2").place(x=300,y=370,width=110,height=35)
        btn_delete=Button(self.root,text="Delete",command=self.delete,font=("goudy old style",15),bg="#f44336",fg="white",cursor="hand2").place(x=420,y=370,width=110,height=35)
        btn_clear=Button(self.root,text="Clear",command=self.clear,font=("goudy old style",15),bg="#607d8b",fg="white",cursor="hand2").place(x=540,y=370,width=110,height=35)

        #------------ supplier details -------------
        sup_frame=Frame(self.root,bd=3,relief=RIDGE)
        sup_frame.place(x=800,y=120,width=430,height=500)

        scrolly=Scrollbar(sup_frame,orient=VERTICAL)
        scrollx=Scrollbar(sup_frame,orient=HORIZONTAL)\
        
        self.SupplierTable=ttk.Treeview(sup_frame,columns=("invoice","name","contact","description"),yscrollcommand=scrolly.set,xscrollcommand=scrollx.set)
        scrollx.pack(side=BOTTOM,fill=X)
        scrolly.pack(side=RIGHT,fill=Y)
        scrollx.config(command=self.SupplierTable.xview)
        scrolly.config(command=self.SupplierTable.yview)
        self.SupplierTable.heading("invoice",text="Invoice")
        self.SupplierTable.heading("name",text="Name")
        self.SupplierTable.heading("contact",text="Contact")
        self.SupplierTable.heading("description",text="Description")
        self.SupplierTable["show"]="headings"
        self.SupplierTable.column("invoice",width=90)
        self.SupplierTable.column("name",width=100)
        self.SupplierTable.column("contact",width=100)
        self.SupplierTable.column("description",width=100)
        
        self.SupplierTable.pack(fill=BOTH,expand=1)
        self.SupplierTable.bind("<ButtonRelease-1>",self.get_data)
        self.show()
#-----------------------------------------------------------------------------------------------------
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
                if self.var_sup_invoice.get()=="" or self.var_name.get()=="" or self.var_contact.get()=="": 
                    messagebox.showerror("Error","All fields are required",parent=self.root)
                else:
                    cursor.execute("select * from supplier where invoice=%s",(self.var_sup_invoice.get(),))
                    row=cursor.fetchone()
                    if row!=None:
                        messagebox.showerror("Error","Invoice No. already present, try different",parent=self.root)
                    else:
                        cursor.execute("insert into supplier (invoice,name,contact,description) values(%s,%s,%s,%s)",(
                            self.var_sup_invoice.get(),
                            self.var_name.get(),
                            self.var_contact.get(),
                            self.txt_desc.get('1.0',END)
                        ))
                        connection.commit()
                        messagebox.showinfo("Success","Employee added successfully",parent=self.root)
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
                cursor.execute("select * from supplier")
                rows=cursor.fetchall()
                self.SupplierTable.delete(*self.SupplierTable.get_children())
                for row in rows:
                    self.SupplierTable.insert('',END,values=row)
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to: {str(ex)}")

    def get_data(self,ev):
        f=self.SupplierTable.focus()
        content=(self.SupplierTable.item(f))
        row=content['values']
        self.var_sup_invoice.set(row[0])
        self.var_name.set(row[1])
        self.var_contact.set(row[2])
        self.txt_desc.delete('1.0',END)
        self.txt_desc.insert(END,row[3])

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
                if self.var_sup_invoice.get()=="" or self.var_name.get()=="" or self.var_contact.get()=="": 
                    messagebox.showerror("Error","All fields are required",parent=self.root)
                else:
                    cursor.execute("select * from supplier where invoice=%s",(self.var_sup_invoice.get(),))
                    row=cursor.fetchone()
                    if row==None:
                        messagebox.showerror("Error","Invalid Invoice No.",parent=self.root)
                    else:
                        cursor.execute("update supplier set name=%s,contact=%s,description=%s where invoice=%s",(
                            self.var_name.get(),
                            self.var_contact.get(),
                            self.txt_desc.get('1.0',END),
                            self.var_sup_invoice.get()
                        ))
                        connection.commit()
                        messagebox.showinfo("Success","Supplier updated successfully",parent=self.root)
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
                if self.var_sup_invoice.get()=="": 
                    messagebox.showerror("Error","Invoice No. is required",parent=self.root)
                else:
                    cursor.execute("select * from supplier where invoice=%s",(self.var_sup_invoice.get(),))
                    row=cursor.fetchone()
                    if row==None:
                        messagebox.showerror("Error","Invalid Invoice No.",parent=self.root)
                    else:
                        cursor.execute("delete from supplier where invoice=%s",(self.var_sup_invoice.get(),))
                        connection.commit()
                        messagebox.showinfo("Success","Supplier deleted successfully",parent=self.root)
                        self.clear()
                        self.show()
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to: {str(ex)}")

    def clear(self):
        self.var_sup_invoice.set("")
        self.var_name.set("")
        self.var_contact.set("")
        self.txt_desc.delete('1.0',END)
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
                if self.var_searchtxt.get()=="":
                    messagebox.showerror("Error","Invoice No. should be required",parent=self.root)
                else:
                    cursor.execute("select * from supplier where invoice=%s",(self.var_searchtxt.get(),))
                    row=cursor.fetchone()
                    if row!=None:
                        self.SupplierTable.delete(*self.SupplierTable.get_children())
                        self.SupplierTable.insert('',END,values=row)
                    else:
                        messagebox.showerror("Error","No record found!!!",parent=self.root)
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to: {str(ex)}")

if __name__=="__main__":
    root=Tk()
    obj=supplierClass(root)
    root.mainloop()