from tkinter import *
from PIL import Image,ImageTk
from tkinter import ttk,messagebox
import mysql.connector

class categoryClass:
    def __init__(self,root):
        self.root=root
        self.root.geometry("1290x700+380+150")
        self.root.title("Inventory Management System")
        self.root.config(bg="white")
        self.root.focus_force()

        #------------ variables -------------
        self.var_cat_id=StringVar()
        self.var_name=StringVar()
        #--------------- title ---------------------
        lbl_title=Label(self.root,text="Manage Product Category",font=("goudy old style",30),bg="#6c3483",fg="white",bd=3,relief=RIDGE).pack(side=TOP,fill=X,padx=10,pady=20)
        
        lbl_mame=Label(self.root,text="Enter Category Name",font=("goudy old style",30),bg="white").place(x=50,y=100)
        txt_mame=Entry(self.root,textvariable=self.var_name,bg="lightyellow",font=("goudy old style",18)).place(x=50,y=170,width=300)

        btn_add=Button(self.root,text="ADD",command=self.add,font=("goudy old style",15),bg="#4caf50",fg="white",cursor="hand2").place(x=360,y=170,width=150,height=30)
        btn_delete=Button(self.root,text="Delete",command=self.delete,font=("goudy old style",15),bg="red",fg="white",cursor="hand2").place(x=520,y=170,width=150,height=30)

        #------------ category details -------------
        cat_frame=Frame(self.root,bd=3,relief=RIDGE)
        cat_frame.place(x=700,y=100,width=580,height=250)

        scrolly=Scrollbar(cat_frame,orient=VERTICAL)
        scrollx=Scrollbar(cat_frame,orient=HORIZONTAL)\
        
        self.CategoryTable=ttk.Treeview(cat_frame,columns=("cid","name"),yscrollcommand=scrolly.set,xscrollcommand=scrollx.set)
        scrollx.pack(side=BOTTOM,fill=X)
        scrolly.pack(side=RIGHT,fill=Y)
        scrollx.config(command=self.CategoryTable.xview)
        scrolly.config(command=self.CategoryTable.yview)
        self.CategoryTable.heading("cid",text="C ID")
        self.CategoryTable.heading("name",text="Name")
        self.CategoryTable["show"]="headings"
        self.CategoryTable.column("cid",width=90)
        self.CategoryTable.column("name",width=100)
        
        self.CategoryTable.pack(fill=BOTH,expand=1)
        self.CategoryTable.bind("<ButtonRelease-1>",self.get_data)
        self.show()

        #----------------- images ---------------------
        self.im1=Image.open("images/cat.jpg")
        self.im1=self.im1.resize((600,300))
        self.im1=ImageTk.PhotoImage(self.im1)
        self.lbl_im1=Label(self.root,image=self.im1,bd=2,relief=RAISED)
        self.lbl_im1.place(x=50,y=370)

        self.im2=Image.open("images/category.jpg")
        self.im2=self.im2.resize((600,300))
        self.im2=ImageTk.PhotoImage(self.im2)
        self.lbl_im2=Label(self.root,image=self.im2,bd=2,relief=RAISED)
        self.lbl_im2.place(x=660,y=370)
#----------------------------------------------------------------------------------
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
                if self.var_name.get()=="": 
                    messagebox.showerror("Error","Category name is required",parent=self.root)
                else:
                    cursor.execute("select * from category where name=%s",(self.var_name.get(),))
                    row=cursor.fetchone()
                    if row!=None:
                        messagebox.showerror("Error","Category already exists",parent=self.root)
                    else:
                        cursor.execute("insert into category(name) values(%s)",(
                            self.var_name.get(),
                        ))
                        connection.commit()
                        messagebox.showinfo("Success","Category added successfully",parent=self.root)
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
                cursor.execute("select * from category")
                rows=cursor.fetchall()
                self.CategoryTable.delete(*self.CategoryTable.get_children())
                for row in rows:
                    self.CategoryTable.insert('',END,values=row)
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to: {str(ex)}")

    
    def clear(self):
        self.var_name.set("")
        self.show()

    def get_data(self,ev):
        f=self.CategoryTable.focus()
        content=(self.CategoryTable.item(f))
        row=content['values']
        self.var_cat_id.set(row[0])
        self.var_name.set(row[1])
    
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
                if self.var_cat_id.get()=="": 
                    messagebox.showerror("Error","Category name is required",parent=self.root)
                else:
                    cursor.execute("select * from category where cid=%s",(self.var_cat_id.get(),))
                    row=cursor.fetchone()
                    if row==None:
                        messagebox.showerror("Error","Invalid Category Name",parent=self.root)
                    else:
                        op=messagebox.askyesno("Confirm","Do you really want to delete?",parent=self.root)
                        if op==True:
                            cursor.execute("delete from category where cid=%s",(self.var_cat_id.get(),))
                            connection.commit()
                            messagebox.showinfo("Success","Category deleted successfully",parent=self.root)
                            self.show()
                            self.clear()
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to: {str(ex)}")


if __name__=="__main__":
    root=Tk()
    obj=categoryClass(root)
    root.mainloop()