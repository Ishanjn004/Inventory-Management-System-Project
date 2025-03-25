from tkinter import *
from PIL import ImageTk
from tkinter import messagebox
import mysql.connector
import os
import email_pass
import smtplib
import time

class Login_System:
    def __init__(self,root):
        self.root=root
        self.root.title("Login System")
        self.root.geometry("1400x880+150+55")
        self.root.config(bg="#fafafa")
        # self.center_window(1400, 880)

        self.otp=''

        #images===============================
        self.phone_image=ImageTk.PhotoImage(file="images/phone.png")
        self.lbl_Phone_img=Label(self.root,image=self.phone_image,bd=0).place(x=250,y=120)

        #Login Frame===========================
        login_frame=Frame(self.root,bd=2,relief=RIDGE,bg="white")
        login_frame.place(x=700,y=150,width=350,height=460)

        title=Label(login_frame,text="Login System",font=("Elephant",30,"bold"),bg="white").place(x=0,y=30,relwidth=1)

        lbl_usr=Label(login_frame,text="User ID",font=("Andalus",15),bg="white",fg="#767171").place(x=50,y=100)
        self.userid=StringVar()
        self.password=StringVar()
        txt_userid=Entry(login_frame,textvariable=self.userid,font=("times new roman",15),bg="#ECECEC").place(x=50,y=140,width=250)

        lbl_pass=Label(login_frame,text="Password",font=("Andalus",15),bg="white",fg="#767171").place(x=50,y=200)
        txt_pass=Entry(login_frame,textvariable=self.password,show="*",font=("times new roman",15),bg="#ECECEC").place(x=50,y=240,width=250)

        btn_login=Button(login_frame,command=self.login,text="Log In",font=("Arial Rounded MT Bold",15),bg="#212f3d",fg="white",activebackground="#212f3d",activeforeground="white",cursor="hand2").place(x=50,y=300,width=250,height=35)

        hr=Label(login_frame,bg="#d5d8dc").place(x=50,y=370,width=250,height=2)
        or_=Label(login_frame,text="OR",bg="white",fg="#d5d8dc",font=("times new roman",15,"bold")).place(x=151,y=356)

        btn_forget=Button(login_frame,command=self.forget_window,text="Forget Password?",font=("times new roman",13),bg="white",fg="#21618c",bd=0,activebackground="white",activeforeground="#21618c").place(x=100,y=390)

        #=====Animation Images==============================
        self.im1=ImageTk.PhotoImage(file="images/im1.png")
        self.im2=ImageTk.PhotoImage(file="images/im2.png")
        self.im3=ImageTk.PhotoImage(file="images/im3.png")

        self.lbl_change_image=Label(self.root,bg="white")
        self.lbl_change_image.place(x=417,y=223,width=240,height=428)

        self.animate()
        # self.send_email('xyz')


    def animate(self):
        self.im=self.im1
        self.im1=self.im2
        self.im2=self.im3
        self.im3=self.im
        self.lbl_change_image.config(image=self.im)
        self.lbl_change_image.after(2000,self.animate)

    def login(self):
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="ishan",
            database="IMS"
        )
        try:
            if self.userid.get()=="" or self.password.get()=="":
                messagebox.showerror("Error","All fields are required",parent=self.root)
            else:
                cursor = connection.cursor()
                cursor.execute("Select utype from employee where eid=%s and pass=%s",(self.userid.get(),self.password.get()))
                user=cursor.fetchone()
                if user==None:
                    messagebox.showerror("Error","Invalid Username or Password",parent=self.root)
                else:
                    if user[0]=="Admin":
                        messagebox.showinfo("Success","Welcome",parent=self.root)
                        self.root.destroy()
                        os.system('python dashboard.py')
                    else:
                        messagebox.showinfo("Success","Welcome",parent=self.root)
                        self.root.destroy()
                        os.system('python billing.py')
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to: {str(ex)}")

    def forget_window(self):
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="ishan",
            database="IMS"
        )
        try:
            cursor = connection.cursor()
            if self.userid.get()=="":
                messagebox.showerror("Error","Please enter your User ID to reset your password",parent=self.root)
            else:
                cursor = connection.cursor()
                cursor.execute("Select email from employee where eid=%s",(self.userid.get(),))
                email=cursor.fetchone()
                if email==None:
                    messagebox.showerror("Error","Invalid Employee ID, Try Again!!!",parent=self.root)
                else:
                    self.var_otp=StringVar()
                    self.var_new_pass=StringVar()
                    self.var_confirm_pass=StringVar()
                    chk=self.send_email(email[0])
                    if chk!='s':
                        messagebox.showerror("Error","OTP not sent, Try Again!!!",parent=self.root)
                    else:
                        self.forget_win=Toplevel(self.root)
                        self.forget_win.title("Reset Password")
                        self.forget_win.geometry("550x350+600+300")
                        self.forget_win.config(bg="white")
                        self.forget_win.focus_force()

                        title=Label(self.forget_win,text="Reset Password",font=("goudy old style",20,"bold"),fg="#212f3c",bg="#d6eaf8").pack(side=TOP,fill=X)
                        lbl_reset=Label(self.forget_win,text="Enter OTP sent on Registered Email",font=("times new roman",15),bg="white",fg="#ec7063").place(x=20,y=60)
                        txt_reset=Entry(self.forget_win,textvariable=self.var_otp,font=("times new roman",15),show="*",bg="#fef5e7").place(x=20,y=100,width=250,height=30)
                        self.btn_reset=Button(self.forget_win,text="Submit",font=("times new roman",15),command=self.validate_otp,bg="#e8daef",fg="black",activebackground="#e8daef",activeforeground="black",cursor="hand2")
                        self.btn_reset.place(x=280,y=100,width=100,height=30)

                        new_pass=Label(self.forget_win,text="New Password",font=("times new roman",15),bg="white").place(x=20,y=160)
                        txt_new_pass=Entry(self.forget_win,textvariable=self.var_new_pass,font=("times new roman",15),show="*",bg="#fef5e7").place(x=20,y=190,   width=250,height=30)

                        conf_pass=Label(self.forget_win,text="Confirm Password",font=("times new roman",15),bg="white").place(x=20,y=225)
                        txt_conf_pass=Entry(self.forget_win,textvariable=self.var_confirm_pass,font=("times new roman",15),show="*",bg="#fef5e7").place(x=20,y=255,width=250,height=30)

                        self.btn_update=Button(self.forget_win,text="Update",state=DISABLED,font=("times new roman",15),command=self.update_pass,activebackground="#d4efdf",activeforeground="black",bg="#d4efdf",fg="black",cursor="hand2")
                        self.btn_update.place(x=220,y=300,width=100,height=30)

        except Exception as ex:
            messagebox.showerror("Error",f"Error due to: {str(ex)}")

    
    def update_pass(self):
        if self.var_new_pass.get()=="" or self.var_confirm_pass.get()=="":
            messagebox.showerror("Error","All fields are required",parent=self.forget_win)
        elif self.var_new_pass.get()!=self.var_confirm_pass.get():
            messagebox.showerror("Error","Password and Confirm Password should be same",parent=self.forget_win)
        else:
            connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="ishan",
            database="IMS"
        )
        try:
            cursor = connection.cursor()
            cursor.execute("update employee set pass=%s where eid=%s",(self.var_new_pass.get(),self.userid.get()))
            connection.commit()
            connection.close()
            messagebox.showinfo("Success","Password Updated Successfully",parent=self.forget_win)
            self.forget_win.destroy()

        except Exception as ex:
            messagebox.showerror("Error",f"Error due to: {str(ex)}")

    def validate_otp(self):
        if self.otp==int(self.var_otp.get()):
            self.btn_update.config(state=NORMAL)
            self.btn_reset.config(state=DISABLED)
        else:
            messagebox.showerror("Error","Invalid OTP, Try Again!!!",parent=self.forget_win)
    

    def send_email(self,to_):
        s=smtplib.SMTP('smtp.gmail.com',587)
        s.starttls()
        email_=email_pass.email_
        pass_=email_pass.pass_

        s.login(email_,pass_)

        self.otp=int(time.strftime("%H%S%M"))+int(time.strftime("%S"))
        
        subj='IMS - OTP for Password Reset'
        msg='Dear Sir/Madam,\n\nYour OTP for Password Reset is: '+str(self.otp)+'\n\nWith Regards,\nIMS Team'
        message='Subject: {}\n\n{}'.format(subj,msg)
        s.sendmail(email_,to_,message)
        chk=s.ehlo()
        if chk[0]==250:
            # messagebox.showinfo("Success","OTP Sent Successfully",parent=self.root)
            return 's'
        else:
            # messagebox.showerror("Error","OTP not sent, Try Again!!!",parent=self.root)
            return 'f'
        

root=Tk()
obj=Login_System(root)
root.mainloop()