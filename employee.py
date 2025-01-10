from tkinter import *
from PIL import Image,ImageTk
from tkinter import ttk,messagebox
import mysql.connector

class employeeClass:
    def __init__(self,root):
        self.root=root
        self.root.geometry("1290x700+380+150")
        self.root.title("Inventory Management System")
        self.root.config(bg="white")
        self.root.focus_force()

        #=========================All Variables=========================
        self.var_searchby=StringVar()
        self.var_searchtxt=StringVar()
        self.var_emp_id=StringVar()
        self.var_gender=StringVar()
        self.var_contact=StringVar()
        self.var_name=StringVar()
        self.var_dob=StringVar()
        self.var_doj=StringVar()
        self.var_email=StringVar()
        self.var_pass=StringVar()
        self.var_utype=StringVar()
        self.var_salary=StringVar()

        #=========================Search Frame=========================
        SearchFrame=LabelFrame(self.root,text="Search Employee",font=("goudy old style",15,"bold"),bd=2,relief=RIDGE,bg="white")
        SearchFrame.place(x=250,y=20,width=800,height=70)

        #=========================Search Options=========================
        cmb_search=ttk.Combobox(SearchFrame,textvariable=self.var_searchby,values=("Select","Name","Contact","Email"),state="readonly",justify=CENTER,font=("goudy old style",15))
        cmb_search.place(x=10,y=10,width=180)
        cmb_search.current(0)

        txt_search=Entry(SearchFrame,textvariable=self.var_searchtxt,font=("goudy old style",15),bg="#fcf3cf").place(x=200,y=10,width=350)
        btn_search=Button(SearchFrame,text="Search",command=self.search,font=("goudy old style",15,"bold"),bg="#d35400",fg="white",cursor="hand2").place(x=600,y=9,width=150,height=30)

        #=========================Title=========================
        title=Label(self.root,text="Employee Details",font=("goudy old style",20,"bold"),bg="#0b5345",fg="white").place(x=50,y=100,width=1180)

        #=========================Content=========================
        #=========================Row 1=========================
        lbl_empid=Label(self.root,text="Employee ID",font=("goudy old style",20),bg="white").place(x=50,y=150)
        lbl_gender=Label(self.root,text="Gender",font=("goudy old style",20),bg="white").place(x=460,y=150)
        lbl_contact=Label(self.root,text="Contact Number",font=("goudy old style",20),bg="white").place(x=850,y=150)
        txt_empid=Entry(self.root,textvariable=self.var_emp_id,font=("goudy old style",20),bg="#fcf3cf").place(x=210,y=150,width=180)
        cmb_gender=ttk.Combobox(self.root,textvariable=self.var_gender,values=("Select","Male","Female","Other"),state="readonly",justify=CENTER,font=("goudy old style",15))
        cmb_gender.place(x=570,y=152,width=180)
        cmb_gender.current(0)
        txt_contact=Entry(self.root,textvariable=self.var_contact,font=("goudy old style",20),bg="#fcf3cf").place(x=1050,y=150,width=180)

        #=========================Row 2=========================
        lbl_name=Label(self.root,text="Emp Name",font=("goudy old style",20),bg="white").place(x=50,y=200)
        lbl_dob=Label(self.root,text="D.O.B",font=("goudy old style",20),bg="white").place(x=460,y=200)
        lbl_doj=Label(self.root,text="D.O.J",font=("goudy old style",20),bg="white").place(x=850,y=200)
        txt_name=Entry(self.root,textvariable=self.var_name,font=("goudy old style",20),bg="#fcf3cf").place(x=210,y=200,width=180)
        txt_dob=Entry(self.root,textvariable=self.var_dob,font=("goudy old style",20),bg="#fcf3cf").place(x=570,y=200,width=180)
        txt_doj=Entry(self.root,textvariable=self.var_doj,font=("goudy old style",20),bg="#fcf3cf").place(x=1050,y=200,width=180)

        #=========================Row 3=========================
        lbl_email=Label(self.root,text="Email",font=("goudy old style",20),bg="white").place(x=50,y=250)
        lbl_pass=Label(self.root,text="Password",font=("goudy old style",20),bg="white").place(x=460,y=250)
        lbl_utype=Label(self.root,text="User Type",font=("goudy old style",20),bg="white").place(x=850,y=250)
        txt_email=Entry(self.root,textvariable=self.var_email,font=("goudy old style",20),bg="#fcf3cf").place(x=210,y=250,width=180)
        txt_pass=Entry(self.root,textvariable=self.var_pass,font=("goudy old style",20),bg="#fcf3cf").place(x=570,y=250,width=180)
        cmb_utype=ttk.Combobox(self.root,textvariable=self.var_utype,values=("Select","Admin","Employee"),state="readonly",justify=CENTER,font=("goudy old style",15))
        cmb_utype.place(x=1050,y=250,width=180)
        cmb_utype.current(0)

        #=========================Row 4=========================
        lbl_address=Label(self.root,text="Address",font=("goudy old style",20),bg="white").place(x=50,y=300)
        lbl_salary=Label(self.root,text="Salary",font=("goudy old style",20),bg="white").place(x=670,y=300)
        self.txt_address=Text(self.root,font=("goudy old style",20),bg="#fcf3cf")
        self.txt_address.place(x=210,y=300,width=400,height=82)
        txt_salary=Entry(self.root,textvariable=self.var_salary,font=("goudy old style",20),bg="#fcf3cf").place(x=760,y=300,width=180)

        #=========================Buttons=========================
        btn_add=Button(self.root,text="Save",command=self.add,font=("goudy old style",15,"bold"),bg="#3498db",fg="white",cursor="hand2").place(x=674,y=350,width=120,height=30)
        btn_update=Button(self.root,text="Update",command=self.update,font=("goudy old style",15,"bold"),bg="#8e44ad",fg="white",cursor="hand2").place(x=804,y=350,width=120,height=30)
        btn_delete=Button(self.root,text="Delete",command=self.delete,font=("goudy old style",15,"bold"),bg="#d4ac0d",fg="white",cursor="hand2").place(x=934,y=350,width=120,height=30)
        btn_clear=Button(self.root,text="Clear",command=self.clear,font=("goudy old style",15,"bold"),bg="#616a6b",fg="white",cursor="hand2").place(x=1064,y=350,width=120,height=30)
        

        #=========================Employee Details=========================
        emp_frame=Frame(self.root,bd=3,relief=RIDGE)
        emp_frame.place(x=0,y=400,relwidth=1,height=298)

        scrolly=Scrollbar(emp_frame,orient=VERTICAL)
        scrollx=Scrollbar(emp_frame,orient=HORIZONTAL)

        self.employeeTable=ttk.Treeview(emp_frame,columns=("eid","name","email","gender","contact","dob","doj","pass","utype","address","salary"),yscrollcommand=scrolly.set,xscrollcommand=scrollx.set)
        scrollx.pack(side=BOTTOM,fill=X)
        scrolly.pack(side=RIGHT,fill=Y)
        scrollx.config(command=self.employeeTable.xview)
        scrolly.config(command=self.employeeTable.yview)

        self.employeeTable.heading("eid",text="Emp ID")
        self.employeeTable.heading("name",text="Name")
        self.employeeTable.heading("email",text="Email")
        self.employeeTable.heading("gender",text="Gender")
        self.employeeTable.heading("contact",text="Contact No.")
        self.employeeTable.heading("dob",text="D.O.B")
        self.employeeTable.heading("doj",text="D.O.J")
        self.employeeTable.heading("pass",text="Password")
        self.employeeTable.heading("utype",text="User Type")
        self.employeeTable.heading("address",text="Address")
        self.employeeTable.heading("salary",text="Salary")
        self.employeeTable["show"]="headings"
        self.employeeTable.column("eid",width=90)
        self.employeeTable.column("name",width=150)
        self.employeeTable.column("email",width=200)
        self.employeeTable.column("gender",width=100)
        self.employeeTable.column("contact",width=150)
        self.employeeTable.column("dob",width=100)
        self.employeeTable.column("doj",width=100)
        self.employeeTable.column("pass",width=100)
        self.employeeTable.column("utype",width=100)
        self.employeeTable.column("address",width=200)
        self.employeeTable.column("salary",width=100)
        self.employeeTable.pack(fill=BOTH,expand=1)
        self.employeeTable.bind("<ButtonRelease-1>",self.get_data)

        self.show()

#================================================================
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
                if self.var_emp_id.get()=="" or self.var_name.get()=="" or self.var_email.get()=="": 
                    messagebox.showerror("Error","All fields are required",parent=self.root)
                else:
                    cursor.execute("select * from employee where eid=%s",(self.var_emp_id.get(),))
                    row=cursor.fetchone()
                    if row!=None:
                        messagebox.showerror("Error","Employee ID already exists",parent=self.root)
                    else:
                        cursor.execute("insert into employee (eid,name,email,gender,contact,dob,doj,pass,utype,address,salary) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",(
                            self.var_emp_id.get(),
                            self.var_name.get(),
                            self.var_email.get(),
                            self.var_gender.get(),
                            self.var_contact.get(),
                            self.var_dob.get(),
                            self.var_doj.get(),
                            self.var_pass.get(),
                            self.var_utype.get(),
                            self.txt_address.get('1.0',END),
                            self.var_salary.get()
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
                cursor.execute("select * from employee")
                rows=cursor.fetchall()
                self.employeeTable.delete(*self.employeeTable.get_children())
                for row in rows:
                    self.employeeTable.insert('',END,values=row)
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to: {str(ex)}")
    
    def get_data(self,ev):
        r=self.employeeTable.focus()
        content=self.employeeTable.item(r)
        row=content["values"]
        self.var_emp_id.set(row[0])
        self.var_name.set(row[1])
        self.var_email.set(row[2])
        self.var_gender.set(row[3])
        self.var_contact.set(row[4])
        self.var_dob.set(row[5])
        self.var_doj.set(row[6])
        self.var_pass.set(row[7])
        self.var_utype.set(row[8])
        self.txt_address.delete('1.0',END)
        self.txt_address.insert(END,row[9])
        self.var_salary.set(row[10])
    
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
                if self.var_emp_id.get()=="" or self.var_name.get()=="" or self.var_email.get()=="": 
                    messagebox.showerror("Error","All fields are required",parent=self.root)
                else:
                    cursor.execute("select * from employee where eid=%s",(self.var_emp_id.get(),))
                    row=cursor.fetchone()
                    if row==None:
                        messagebox.showerror("Error","Invalid Employee ID",parent=self.root)
                    else:
                        cursor.execute("update employee set name=%s,email=%s,gender=%s,contact=%s,dob=%s,doj=%s,pass=%s,utype=%s,address=%s,salary=%s where eid=%s",(
                            self.var_name.get(),
                            self.var_email.get(),
                            self.var_gender.get(),
                            self.var_contact.get(),
                            self.var_dob.get(),
                            self.var_doj.get(),
                            self.var_pass.get(),
                            self.var_utype.get(),
                            self.txt_address.get('1.0',END),
                            self.var_salary.get(),
                            self.var_emp_id.get()
                        ))
                        connection.commit()
                        messagebox.showinfo("Success","Employee updated successfully",parent=self.root)
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
                if self.var_emp_id.get()=="" or self.var_name.get()=="" or self.var_email.get()=="": 
                    messagebox.showerror("Error","All fields are required",parent=self.root)
                else:
                    cursor.execute("select * from employee where eid=%s",(self.var_emp_id.get(),))
                    row=cursor.fetchone()
                    if row==None:
                        messagebox.showerror("Error","Invalid Employee ID",parent=self.root)
                    else:
                        op=messagebox.askyesno("Confirm","Do you really want to delete?",parent=self.root)
                        if op==True:
                            cursor.execute("delete from employee where eid=%s",(self.var_emp_id.get(),))
                            connection.commit()
                            messagebox.showinfo("Success","Employee deleted successfully",parent=self.root)
                            self.show()
                            self.clear()
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to: {str(ex)}")

    def clear(self):
        self.var_emp_id.set("")
        self.var_name.set("")
        self.var_email.set("")
        self.var_gender.set("Select")
        self.var_contact.set("")
        self.var_dob.set("")
        self.var_doj.set("")
        self.var_pass.set("")
        self.var_utype.set("Select")
        self.txt_address.delete('1.0',END)
        self.var_salary.set("")
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
                    cursor.execute("select * from employee where "+self.var_searchby.get()+" LIKE '%"+self.var_searchtxt.get()+"%'")
                    rows=cursor.fetchall()
                    if len(rows)!=0:
                        self.employeeTable.delete(*self.employeeTable.get_children())
                        for row in rows:
                            self.employeeTable.insert('',END,values=row)
                    else:
                        messagebox.showerror("Error","No record found!!!",parent=self.root)
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to : {str(ex)}")

if __name__=="__main__":
    root=Tk()
    obj=employeeClass(root)
    root.mainloop()