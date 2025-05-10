from tkinter import *
from PIL import Image,ImageTk
from tkinter import ttk,messagebox
import mysql.connector
import time
import os
import tempfile


class BillClass:
    def __init__(self,root):
        self.root=root
        self.root.geometry("2560x980+0+0")
        self.root.title("Inventory Management System")
        self.root.config(bg="white")
        self.cart_list=[]
        self.chk_print=0
        #=========================Title=========================
        self.icon_title=PhotoImage(file="images/logo1.png")
        title=Label(self.root,text="Inventory Management System",image=self.icon_title,compound=LEFT,font=("times new roman",40,"bold"),bg="#1b2631",fg="white",anchor="w",padx=20).place(x=0,y=0,relwidth=1,height=70)

        #=========================Button_Logout=========================
        btn_logout=Button(self.root,command=self.logout,text="Logout",font=("times new roman",15,"bold"),bg="yellow",cursor="hand2").place(x=1500,y=10,width=150,height=50)

        #=========================Clock=========================
        self.lbl_clock=Label(self.root,text="Welcome to Inventory Management System\t\t Date: DD-MM-YYYY\t\t Time: HH:MM:SS",font=("times new roman",15),bg="#2c3e50",fg="white")
        self.lbl_clock.place(x=0,y=70,relwidth=1,height=30)

        #------------ footer -----------------
        lbl_footer=Label(self.root,text="IMS-Inventory Management System\nFor any Technical Issues Contact: 8595791213",font=("times new roman",12,'bold'),bg="#4d636d",fg="white",height=2).pack(side=BOTTOM,fill=X)

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
        btn_search=Button(ProductFrame2,text="Search",font=("goudy old style",15),command=self.search,bg="#212f3c",fg="white",cursor="hand2").place(x=400,y=57,width=100,height=28)
        btn_show_all=Button(ProductFrame2,text="Show All",font=("goudy old style",15),command=self.show,bg="#641e16",fg="white",cursor="hand2").place(x=400,y=20,width=100,height=28)

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
        self.product_Table.bind("<ButtonRelease-1>",self.get_data)
        lbl_note=Label(ProductFrame1,text="        Note: 'Enter 0 Quantity to remove product from the Cart'",font=("goudy old style",15),anchor='w',bg="white",fg="#cb4335").pack(side=BOTTOM,fill=X)


       #Customer Frame===========================================
        self.var_cname=StringVar();
        self.var_contact=StringVar();
        CustomerFrame=Frame(self.root,bd=4,relief=RIDGE,bg="white")
        CustomerFrame.place(x=580,y=110,width=600,height=80)
        
        cTitle=Label(CustomerFrame,text="Customer Details",font=("goudy old style",15),bg="#b2babb").pack(side=TOP,fill=X)
        lbl_name=Label(CustomerFrame,text="Name",font=("times new roman",15),bg="white").place(x=5,y=35)
        txt_name=Entry(CustomerFrame,textvariable=self.var_cname,font=("times new roman",13),bg="#d6eaf8").place(x=80,y=38,width=180)

        lbl_contact=Label(CustomerFrame,text="Contact No.",font=("times new roman",15),bg="white").place(x=350,y=35)
        txt_contact=Entry(CustomerFrame,textvariable=self.var_contact,font=("times new roman",13),bg="#d6eaf8").place(x=450,y=38,width=140)

        Cal_Cart_Frame=Frame(self.root,bd=2,relief=RIDGE,bg="white")
        Cal_Cart_Frame.place(x=580,y=200,width=600,height=600)

        self.var_cal_input=StringVar()

        Cal_Frame=Frame(Cal_Cart_Frame,bd=10,relief=RIDGE,bg="white")
        Cal_Frame.place(x=5,y=40,width=340,height=490)

        txt_cal_input=Entry(Cal_Frame,textvariable=self.var_cal_input,font=('arial',15,'bold'),width=27,bd=12,relief=GROOVE,state="readonly",justify=RIGHT)
        txt_cal_input.grid(row=0,columnspan=4,sticky="nsew")

        for i in range(4):  
            Cal_Frame.columnconfigure(i, weight=1)

        btn_7=Button(Cal_Frame,text='7',font=('arial',18,'bold'),command=lambda:self.get_input(7),bd=5,width=4,pady=25,cursor='hand2').grid(row=1,column=0,sticky="nsew")
        btn_8=Button(Cal_Frame,text='8',font=('arial',18,'bold'),command=lambda:self.get_input(8),bd=5,width=4,pady=10,cursor='hand2').grid(row=1,column=1,sticky="nsew")
        btn_9=Button(Cal_Frame,text='9',font=('arial',18,'bold'),command=lambda:self.get_input(9),bd=5,width=4,pady=10,cursor='hand2').grid(row=1,column=2,sticky="nsew")
        btn_sum=Button(Cal_Frame,text='+',font=('arial',18,'bold'),command=lambda:self.get_input('+'),bd=5,width=4,pady=10,cursor='hand2').grid(row=1,column=3,sticky="nsew")

        btn_4=Button(Cal_Frame,text='4',font=('arial',18,'bold'),command=lambda:self.get_input(4),bd=5,width=4,pady=25,cursor='hand2').grid(row=2,column=0,sticky="nsew")
        btn_5=Button(Cal_Frame,text='5',font=('arial',18,'bold'),command=lambda:self.get_input(5),bd=5,width=4,pady=10,cursor='hand2').grid(row=2,column=1,sticky="nsew")
        btn_6=Button(Cal_Frame,text='6',font=('arial',18,'bold'),command=lambda:self.get_input(6),bd=5,width=4,pady=10,cursor='hand2').grid(row=2,column=2,sticky="nsew")
        btn_sub=Button(Cal_Frame,text='-',font=('arial',18,'bold'),command=lambda:self.get_input('-'),bd=5,width=4,pady=10,cursor='hand2').grid(row=2,column=3,sticky="nsew")

        btn_1=Button(Cal_Frame,text='1',font=('arial',18,'bold'),command=lambda:self.get_input(1),bd=5,width=4,pady=25,cursor='hand2').grid(row=3,column=0,sticky="nsew")
        btn_2=Button(Cal_Frame,text='2',font=('arial',18,'bold'),command=lambda:self.get_input(2),bd=5,width=4,pady=10,cursor='hand2').grid(row=3,column=1,sticky="nsew")
        btn_3=Button(Cal_Frame,text='3',font=('arial',18,'bold'),command=lambda:self.get_input(3),bd=5,width=4,pady=10,cursor='hand2').grid(row=3,column=2,sticky="nsew")
        btn_mul=Button(Cal_Frame,text='*',font=('arial',18,'bold'),command=lambda:self.get_input('*'),bd=5,width=4,pady=10,cursor='hand2').grid(row=3,column=3,sticky="nsew")

        btn_0=Button(Cal_Frame,text='0',font=('arial',18,'bold'),command=lambda:self.get_input(0),bd=5,width=4,pady=25,cursor='hand2').grid(row=4,column=0,sticky="nsew")
        btn_c=Button(Cal_Frame,text='c',font=('arial',18,'bold'),command=self.clear_cal,bd=5,width=4,pady=10,cursor='hand2').grid(row=4,column=1,sticky="nsew")
        btn_eq=Button(Cal_Frame,text='=',font=('arial',18,'bold'),command=self.perform_cal,bd=5,width=4,pady=10,cursor='hand2').grid(row=4,column=2,sticky="nsew")
        btn_div=Button(Cal_Frame,text='/',font=('arial',18,'bold'),command=lambda:self.get_input('/'),bd=5,width=4,pady=10,cursor='hand2').grid(row=4,column=3,sticky="nsew")



        cart_Frame=Frame(Cal_Cart_Frame,bd=3,relief=RIDGE)
        cart_Frame.place(x=350,y=8,width=245,height=578)

        self.cartTitle=Label(cart_Frame,text="Cart \t Total Product: 0",font=("goudy old style",15),bg="#b2babb")
        self.cartTitle.pack(side=TOP,fill=X)

        scrolly=Scrollbar(cart_Frame,orient=VERTICAL)
        scrollx=Scrollbar(cart_Frame,orient=HORIZONTAL)
        
        self.CartTable=ttk.Treeview(cart_Frame,columns=("pid","name","price","qty"),yscrollcommand=scrolly.set,xscrollcommand=scrollx.set)
        scrollx.pack(side=BOTTOM,fill=X)
        scrolly.pack(side=RIGHT,fill=Y)
        scrollx.config(command=self.CartTable.xview)
        scrolly.config(command=self.CartTable.yview)
        self.CartTable.heading("pid",text="PID")
        self.CartTable.heading("name",text="Name")
        self.CartTable.heading("price",text="Price")
        self.CartTable.heading("qty",text="Quantity")
        self.CartTable["show"]="headings"
        self.CartTable.column("pid",width=40)
        self.CartTable.column("name",width=100)
        self.CartTable.column("price",width=90)
        self.CartTable.column("qty",width=60)
        
        self.CartTable.pack(fill=BOTH,expand=1)
        self.CartTable.bind("<ButtonRelease-1>",self.get_data_cart)

        self.var_pid=StringVar()
        self.var_pname=StringVar()
        self.var_price=StringVar()
        self.var_qty=StringVar()
        self.var_stock=StringVar()


        Add_CartWidgetsFrame=Frame(self.root,bd=2,relief=RIDGE,bg="white")
        Add_CartWidgetsFrame.place(x=580,y=800,width=600,height=110)

        lbl_p_name=Label(Add_CartWidgetsFrame,text="Product Name",font=("times new roman",15),bg="white").place(x=5,y=5)
        txt_p_name=Entry(Add_CartWidgetsFrame,textvariable=self.var_pname,font=("times new roman",15),bg="#d6eaf8",state='readonly').place(x=5,y=35,width=190,height=22)

        lbl_p_price=Label(Add_CartWidgetsFrame,text="Price Per Qty",font=("times new roman",15),bg="white").place(x=230,y=5)
        txt_p_price=Entry(Add_CartWidgetsFrame,textvariable=self.var_price,font=("times new roman",15),bg="#d6eaf8",state='readonly').place(x=230,y=35,width=170,height=22)

        lbl_p_qty=Label(Add_CartWidgetsFrame,text="Quantity",font=("times new roman",15),bg="white").place(x=420,y=5)
        txt_p_qty=Entry(Add_CartWidgetsFrame,textvariable=self.var_qty,font=("times new roman",15),bg="#d6eaf8").place(x=420,y=35,width=150,height=22)


        self.lbl_inStock=Label(Add_CartWidgetsFrame,text="In Stock: ",font=("times new roman",15),bg="white")
        self.lbl_inStock.place(x=5,y=70)

        btn_clear_cart=Button(Add_CartWidgetsFrame,text="Clear",command=self.clear_cart,font=("times new roman",15,"bold"),bg="#ccd1d1",cursor="hand2").place(x=200,y=70,width=150,height=30)
        btn_add_cart=Button(Add_CartWidgetsFrame,text="ADD | Update Cart",font=("times new roman",15,"bold"),command=self.add_update_cart,bg="#eb984e",cursor="hand2").place(x=390,y=70,width=180,height=30)


        #====================Billing Area=================================
        billFrame=Frame(self.root,bd=2,relief=RIDGE,bg="white")
        billFrame.place(x=1185,y=110,width=520,height=650)
        BTitle=Label(billFrame,text="Customer Bill Area",font=("goudy old style",20,"bold"),bg="#1c2833",fg="white").pack(side=TOP,fill=X)
        scrolly=Scrollbar(billFrame,orient=VERTICAL)
        scrolly.pack(side=RIGHT,fill=Y)

        self.txt_bill_area=Text(billFrame,yscrollcommand=scrolly.set)
        self.txt_bill_area.pack(fill=BOTH,expand=1)
        scrolly.config(command=self.txt_bill_area.yview)

        #------------------- billing buttons -----------------------
        billMenuFrame=Frame(self.root,bd=2,relief=RIDGE,bg="white")
        billMenuFrame.place(x=1185,y=760,width=520,height=150)

        self.lbl_amnt=Label(billMenuFrame,text="Bill Amount\n0",font=("goudy old style",15,"bold"),bg="#3f51b5",fg="white")
        self.lbl_amnt.place(x=2,y=5,width=170,height=70)

        self.lbl_discount=Label(billMenuFrame,text="Discount\n5%",font=("goudy old style",15,"bold"),bg="#8bc34a",fg="white")
        self.lbl_discount.place(x=174,y=5,width=160,height=70)

        self.lbl_net_pay=Label(billMenuFrame,text="Net Pay\n0",font=("goudy old style",15,"bold"),bg="#607d8b",fg="white")
        self.lbl_net_pay.place(x=336,y=5,width=175,height=70)

        btn_print=Button(billMenuFrame,text="Print",command=self.print_bill,cursor="hand2",font=("goudy old style",15,"bold"),bg="#145a32",fg="white")
        btn_print.place(x=2,y=80,width=170,height=60)

        btn_clear_all=Button(billMenuFrame,text="Clear All",command=self.clear_all,cursor="hand2",font=("goudy old style",15,"bold"),bg="gray",fg="white")
        btn_clear_all.place(x=174,y=80,width=160,height=60)

        btn_generate=Button(billMenuFrame,text="Generate Bill",command=self.generate_bill,cursor="hand2",font=("goudy old style",15,"bold"),bg="#009688",fg="white")
        btn_generate.place(x=336,y=80,width=175,height=60)

        self.show()
        # self.bill_top()
        self.update_date_time()
        
        #=====================ALL FUNCTIONS================================
    def get_input(self,num):
        xnum=self.var_cal_input.get()+str(num)
        self.var_cal_input.set(xnum)

    def clear_cal(self):
        self.var_cal_input.set('')

    def perform_cal(self):
        result=self.var_cal_input.get()
        self.var_cal_input.set(eval(result))

    def show(self):
        try:
            # self.product_Table=ttk.Treeview(ProductFrame3,columns=("pid","name","price","qty","status"),yscrollcommand=scrolly.set,xscrollcommand=scrollx.set)
            connection = mysql.connector.connect(
                host="localhost",
                user="root",
                password="ishan",
                database="IMS"
            )
            if connection.is_connected():
                cursor = connection.cursor()
                cursor.execute("select pid,name,price,qty,status from product where status = 'Active'")
                rows=cursor.fetchall()
                self.product_Table.delete(*self.product_Table.get_children())
                for row in rows:
                    self.product_Table.insert('',END,values=row)
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to: {str(ex)}")

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
                if self.var_search.get()=="":
                    messagebox.showerror("Error","Search input should be required",parent=self.root)
                else:
                    cursor.execute("select pid,name,price,qty,status from product where name LIKE '%"+self.var_search.get()+"%' and status='Active'")
                    rows=cursor.fetchall()
                    if len(rows)!=0:
                        self.product_Table.delete(*self.product_Table.get_children())
                        for row in rows:
                            self.product_Table.insert('',END,values=row)
                    else:
                        messagebox.showerror("Error","No record found!!!",parent=self.root)
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to : {str(ex)}")

    def get_data(self,ev):
        f=self.product_Table.focus()
        content=(self.product_Table.item(f))
        row=content['values']
        self.var_pid.set(row[0])
        self.var_pname.set(row[1])
        self.var_price.set(row[2])
        self.lbl_inStock.config(text=f"In Stock: {str(row[3])}")
        self.var_stock.set(row[3])
        self.var_qty.set('1')

    def get_data_cart(self,ev):
        f=self.CartTable.focus()
        content=(self.CartTable.item(f))
        row=content['values']
        self.var_pid.set(row[0])
        self.var_pname.set(row[1])
        self.var_price.set(row[2])
        self.var_qty.set(row[3])
        self.lbl_inStock.config(text=f"In Stock: {str(row[4])}")
        self.var_stock.set(row[4])
        

    def add_update_cart(self):
        if self.var_pid.get()=='':
            messagebox.showerror('Error',"Please select Product from the list",parent=self.root)
        elif self.var_qty.get()=='':
            messagebox.showerror('Error',"Quantity is required",parent=self.root)
        elif int(self.var_qty.get())>int(self.var_stock.get()):
            messagebox.showerror('Error',"Invalid Quantity",parent=self.root)
        else:
            # price_cal=int(self.var_qty.get())*float(self.var_price.get())
            # price_cal=float(price_cal)
            price_cal=self.var_price.get()
            cart_data=[self.var_pid.get(),self.var_pname.get(),price_cal,self.var_qty.get(),self.var_stock.get()]
            
            # print(self.cart_list)
            # update cart
            present='no'
            index_=0
            for row in self.cart_list:
                if self.var_pid.get()==row[0]:
                    present='yes'
                    break
                index_+=1
            # print(present,index_)
            if present=='yes':
                op=messagebox.askyesno('Confirm',"Product already present\nDo you want to Update | Remove from the Cart List",parent=self.root)
                if op==True:
                    if self.var_qty.get()=="0":
                        self.cart_list.pop(index_)
                    else:
                        # self.cart_list[index_][2]=price_cal
                        self.cart_list[index_][3]=self.var_qty.get()
            else:
                self.cart_list.append(cart_data)
            self.show_cart()
            self.bill_updates()

    def bill_updates(self):
        self.bill_amnt=0
        self.net_pay=0
        self.discount=0
        for row in self.cart_list:
            self.bill_amnt=self.bill_amnt+(float(row[2])*int(row[3]))

        self.discount=(self.bill_amnt*5)/100
        self.net_pay=self.bill_amnt-self.discount
        self.lbl_amnt.config(text=f'Bill Amount\nRs. {str(self.bill_amnt)}')
        self.lbl_net_pay.config(text=f'Net Pay\nRs. {str(self.net_pay)}')
        self.cartTitle.config(text=f"Cart \t Total Prodact: {str(len(self.cart_list))}")

    def show_cart(self):
        try:
            self.CartTable.delete(*self.CartTable.get_children())
            for row in self.cart_list:
                self.CartTable.insert('',END,values=row)
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to: {str(ex)}")

    def generate_bill(self):
        if self.var_cname.get()=='' or self.var_contact.get()=='':
            messagebox.showerror("Error",f"Customers Details are required",parent=self.root)
            return
        elif len(self.cart_list)==0:
            messagebox.showerror("Error","Please Add product to the Cart!!!",parent=self.root)
            return
        else:
            #===========BILL TOP======================  
            self.bill_top()
            #===========BILL MIDDLE======================  
            self.bill_middle()
            #===========BILL BOTTOM======================  
            self.bill_bottom()

        fp=open(f'bills/{str(self.invoice)}.txt','w')
        fp.write(self.txt_bill_area.get('1.0',END))
        fp.close()
        messagebox.showinfo("Saved","Billed has been generated and saved in backend",parent=self.root)
        self.chk_print=1


    def bill_top(self):
        self.invoice=int(time.strftime('%H%M%S'))+int(time.strftime('%d%m%Y'))
        bill_top_temp=f'''
\t\t     Prabhu Dhyan - Inventory
\t\tPhone No. 991100**** , Delhi-110032
{str("="*61)}
 Customer Name: {self.var_cname.get()}
 Phone No.: {self.var_contact.get()}
 Bill No.: {str(self.invoice)}\t\t\t\t\tDate: {str(time.strftime("%d/%m/%Y"))}
{str("="*61)}
 Product Name\t\t\t     QTY\t\t\tPrice
{str("="*61)}
        '''
        self.txt_bill_area.delete('1.0',END)
        self.txt_bill_area.insert('1.0',bill_top_temp)

    def bill_bottom(self):
        bill_bottom_temp=f'''
{str("="*61)}
 Bill Amount\t\t\t\t\t\tRs.{self.bill_amnt}
 Discount\t\t\t\t\t\tRs.{self.discount}
 Net Pay\t\t\t\t\t\tRs.{self.net_pay}
{str("="*61)}
        '''
        self.txt_bill_area.insert(END,bill_bottom_temp)
    
    def bill_middle(self):
        try:
            connection = mysql.connector.connect(
                host="localhost",
                user="root",
                password="ishan",
                database="IMS"
            )
            for row in self.cart_list:
                
                pid=row[0]
                name=row[1]
                qty=int(row[4])-int(row[3])
                if int(row[3])==int(row[4]):
                    status="Inactive"
                if int(row[3])!=int(row[4]):
                    status="Active"
                price=float(row[2])*int(row[3])
                price=str(price)
                self.txt_bill_area.insert(END,"\n "+name+"\t\t\t     "+row[3]+"\t\t\tRs."+price)
                cursor = connection.cursor()
                cursor.execute('Update product set qty=%s,status=%s where pid=%s',(
                    qty,
                    status,
                    pid
                ))
                date = time.strftime("%Y-%m-%d")
                cursor.execute("insert into sales (name,date,qty_sold,current_stock) values(%s,%s,%s,%s)",(
                    name,
                    date,
                    row[3],
                    qty
                ))
            connection.commit()  # Commit all transactions
            cursor.close()  # Close cursor
            connection.close()  # Close connection
            self.show()
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to : {str(ex)}")

    def clear_cart(self):
        self.var_pid.set("")
        self.var_pname.set("")
        self.var_price.set("")
        self.var_qty.set("")
        self.lbl_inStock.config(text=f"In Stock")
        self.var_stock.set("")

    def clear_all(self):
        del self.cart_list[:]
        self.clear_cart()
        self.show()
        self.show_cart()
        self.var_cname.set("")
        self.var_contact.set("")
        self.chk_print=0
        self.txt_bill_area.delete('1.0',END)
        self.cartTitle.config(text=f"Cart \t Total Products: 0")
        self.var_search.set("")
        self.lbl_amnt.config(text="Bill Amount\n0")
        self.lbl_discount.config(text="Discount\n5%")
        self.lbl_net_pay.config(text="Net Pay\n0")

    def update_date_time(self):
        time_=time.strftime("%H:%M:%S")
        date_=time.strftime("%d-%m-%Y")
        self.lbl_clock.config(text=f"Welcome to Inventory Management System\t\t Date: {str(date_)}\t\t Time: {str(time_)}")
        self.lbl_clock.after(200,self.update_date_time)

    def print_bill(self):
        if self.chk_print==1:
            messagebox.showinfo("Print","Please wait while printing",parent=self.root)
            new_file=tempfile.mktemp('.txt')
            open(new_file,'w').write(self.txt_bill_area.get('1.0',END))
            os.startfile(new_file,'print')
        else:
            messagebox.showinfo("Print","Please generate bill to print the receipt",parent=self.root)

    def logout(self):
        self.root.destroy()
        os.system('python login.py')



if __name__=="__main__":
    root=Tk()
    obj=BillClass(root)
    root.mainloop()