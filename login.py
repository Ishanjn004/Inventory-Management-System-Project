from tkinter import *
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import mysql.connector
import os
import email_pass
import smtplib
import time

class Login_System:
    def __init__(self, root):
        self.root = root
        self.root.title("Inventory Management System - Login")
        self.root.geometry("1400x880+150+55")
        self.root.config(bg="white")
        self.root.resizable(False, False)
        
        # Custom title bar
        self.title_bar = Frame(self.root, bg="#2f3640", height=50, relief=RAISED, bd=0)
        self.title_bar.pack(fill=X)
        
        self.title_label = Label(self.title_bar, text="INVENTORY MANAGEMENT SYSTEM", 
                               font=("Segoe UI", 14, "bold"), bg="#2f3640", fg="white")
        self.title_label.pack(side=LEFT, padx=20)
        
        self.close_btn = Button(self.title_bar, text="×", font=("Segoe UI", 16), 
                              bg="#2f3640", fg="white", bd=0, activebackground="#e84118",
                              command=self.root.quit)
        self.close_btn.pack(side=RIGHT, padx=10)
        
        self.otp = ''

        # Main content frame
        self.main_frame = Frame(self.root, bg="#f5f6fa")
        self.main_frame.pack(fill=BOTH, expand=True, padx=20, pady=20)

        # Left side with image and animation
        self.left_frame = Frame(self.main_frame, bg="white")
        self.left_frame.pack(side=LEFT, fill=BOTH, expand=True)

        # Phone image
        self.phone_image = Image.open("images/phone.png")
        self.phone_photo = ImageTk.PhotoImage(self.phone_image)

        # Create a label for the phone image
        self.lbl_phone_img = Label(self.left_frame, image=self.phone_photo, bd=0, bg="#f5f6fa")
        self.lbl_phone_img.image = self.phone_photo  # Keep a reference
        self.lbl_phone_img.pack(pady=50)

        # Get phone screen position (adjust these values based on your phone image)
        phone_x, phone_y = 165, 103  # Example coordinates, adjust as needed
        phone_width, phone_height = 240, 428  # Example dimensions, adjust as needed

        # Create a frame that will sit exactly on the phone screen
        self.phone_screen_frame = Frame(self.lbl_phone_img, bg='white', 
                               width=phone_width, height=phone_height)
        self.phone_screen_frame.place(x=phone_x, y=phone_y)

        # Animation images
        self.im1 = ImageTk.PhotoImage(file="images/im1.png")
        self.im2 = ImageTk.PhotoImage(file="images/im2.png")
        self.im3 = ImageTk.PhotoImage(file="images/im3.png")

        # Create animation label inside the phone screen frame
        self.lbl_change_image = Label(self.phone_screen_frame, bg="white")
        self.lbl_change_image.pack(fill=BOTH, expand=True)
        self.animate()

        # Right side with login form
        self.right_frame = Frame(self.main_frame, bg="#f5f6fa")
        self.right_frame.pack(side=RIGHT, fill=BOTH, expand=True)

        # Login Frame
        login_frame = Frame(self.right_frame, bd=0, relief=RIDGE, bg="white", 
                          highlightbackground="#dfe6e9", highlightthickness=1)
        login_frame.place(relx=0.5, rely=0.5, anchor=CENTER, width=400, height=500)

        # Title
        title = Label(login_frame, text="Login", font=("Segoe UI", 24, "bold"), 
                    bg="white", fg="#2f3640")
        title.pack(pady=40)

        # Username field
        lbl_usr = Label(login_frame, text="Employee ID", font=("Segoe UI", 11), 
                       bg="white", fg="#7f8c8d")
        lbl_usr.pack(pady=(0, 5), padx=50, anchor=W)

        self.userid = StringVar()
        self.entry_userid = ttk.Entry(login_frame, textvariable=self.userid, 
                                    font=("Segoe UI", 12))
        self.entry_userid.pack(fill=X, padx=50, pady=(0, 20), ipady=5)

        # Password field
        lbl_pass = Label(login_frame, text="Password", font=("Segoe UI", 11), 
                        bg="white", fg="#7f8c8d")
        lbl_pass.pack(pady=(0, 5), padx=50, anchor=W)

        self.password = StringVar()
        self.entry_pass = ttk.Entry(login_frame, textvariable=self.password, 
                                   show="*", font=("Segoe UI", 12))
        self.entry_pass.pack(fill=X, padx=50, pady=(0, 20), ipady=5)

        # Login button
        btn_login = Button(login_frame, command=self.login, text="LOGIN", 
                          font=("Segoe UI", 12, "bold"), bg="#3498db", fg="white",
                          activebackground="#2980b9", activeforeground="white",
                          bd=0, cursor="hand2", height=2)
        btn_login.pack(fill=X, padx=50, pady=(10, 20))

        # Separator
        separator = Frame(login_frame, bg="#dfe6e9", height=2)
        separator.pack(fill=X, padx=50, pady=10)

        # Forget password link
        btn_forget = Button(login_frame, command=self.forget_window, 
                          text="Forgot Password?", font=("Segoe UI", 10), 
                          bg="white", fg="#3498db", bd=0, 
                          activebackground="white", activeforeground="#2980b9",
                          cursor="hand2")
        btn_forget.pack(pady=10)

    def animate(self):
        self.im = self.im1
        self.im1 = self.im2
        self.im2 = self.im3
        self.im3 = self.im
        self.lbl_change_image.config(image=self.im)
        self.lbl_change_image.after(2000, self.animate)

    def login(self):
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="ishan",
            database="IMS"
        )
        try:
            if self.userid.get() == "" or self.password.get() == "":
                messagebox.showerror("Error", "All fields are required", parent=self.root)
            else:
                cursor = connection.cursor()
                cursor.execute("Select utype from employee where eid=%s and pass=%s", 
                             (self.userid.get(), self.password.get()))
                user = cursor.fetchone()
                if user == None:
                    messagebox.showerror("Error", "Invalid Username or Password", parent=self.root)
                else:
                    if user[0] == "Admin":
                        messagebox.showinfo("Success", "Welcome Admin", parent=self.root)
                        self.root.destroy()
                        os.system('python dashboard.py')
                    else:
                        messagebox.showinfo("Success", "Welcome Employee", parent=self.root)
                        self.root.destroy()
                        os.system('python billing.py')
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}")

    def forget_window(self):
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="ishan",
            database="IMS"
        )
        try:
            cursor = connection.cursor()
            if self.userid.get() == "":
                messagebox.showerror("Error", "Please enter your Employee ID to reset your password", 
                                    parent=self.root)
            else:
                cursor = connection.cursor()
                cursor.execute("Select email from employee where eid=%s", (self.userid.get(),))
                email = cursor.fetchone()
                if email == None:
                    messagebox.showerror("Error", "Invalid Employee ID, Try Again!!!", parent=self.root)
                else:
                    self.var_otp = StringVar()
                    self.var_new_pass = StringVar()
                    self.var_confirm_pass = StringVar()
                    
                    chk = self.send_email(email[0])
                    if chk != 's':
                        messagebox.showerror("Error", "OTP not sent, Try Again!!!", parent=self.root)
                    else:
                        self.forget_win = Toplevel(self.root)
                        self.forget_win.title("Reset Password")
                        self.forget_win.geometry("500x450+600+300")
                        self.forget_win.config(bg="white")
                        self.forget_win.focus_force()
                        self.forget_win.resizable(False, False)

                        # Title
                        title_frame = Frame(self.forget_win, bg="#3498db")
                        title_frame.pack(fill=X)
                        
                        title = Label(title_frame, text="Reset Password", 
                                     font=("Segoe UI", 14, "bold"), 
                                     fg="white", bg="#3498db")
                        title.pack(pady=15)

                        # Main content
                        content_frame = Frame(self.forget_win, bg="white")
                        content_frame.pack(fill=BOTH, expand=True, padx=30, pady=30)

                        # OTP Section
                        lbl_reset = Label(content_frame, 
                                        text="Enter OTP sent to your registered email", 
                                        font=("Segoe UI", 10), bg="white", fg="#7f8c8d")
                        lbl_reset.pack(pady=(10, 5), anchor=W)

                        otp_frame = Frame(content_frame, bg="white")
                        otp_frame.pack(fill=X, pady=(0, 20))

                        self.entry_otp = ttk.Entry(otp_frame, textvariable=self.var_otp, 
                                                  font=("Segoe UI", 12))
                        self.entry_otp.pack(side=LEFT, fill=X, expand=True, ipady=5)

                        self.btn_reset = Button(otp_frame, text="Verify", 
                                              font=("Segoe UI", 10, "bold"), 
                                              command=self.validate_otp,
                                              bg="#2ecc71", fg="white",
                                              activebackground="#27ae60", 
                                              activeforeground="white",
                                              bd=0, cursor="hand2")
                        self.btn_reset.pack(side=RIGHT, padx=(10, 0), ipadx=10, ipady=2)

                        # New Password Section
                        lbl_new_pass = Label(content_frame, text="New Password", 
                                           font=("Segoe UI", 10), bg="white", fg="#7f8c8d")
                        lbl_new_pass.pack(pady=(10, 5), anchor=W)

                        self.entry_new_pass = ttk.Entry(content_frame, 
                                                      textvariable=self.var_new_pass, 
                                                      show="*", font=("Segoe UI", 12))
                        self.entry_new_pass.pack(fill=X, pady=(0, 20), ipady=5)

                        # Confirm Password Section
                        lbl_confirm_pass = Label(content_frame, text="Confirm Password", 
                                               font=("Segoe UI", 10), bg="white", fg="#7f8c8d")
                        lbl_confirm_pass.pack(pady=(10, 5), anchor=W)

                        self.entry_confirm_pass = ttk.Entry(content_frame, 
                                                          textvariable=self.var_confirm_pass, 
                                                          show="*", font=("Segoe UI", 12))
                        self.entry_confirm_pass.pack(fill=X, pady=(0, 20), ipady=5)

                        # Update Button
                        self.btn_update = Button(content_frame, text="UPDATE PASSWORD", 
                                               state=DISABLED, font=("Segoe UI", 12, "bold"), 
                                               command=self.update_pass,
                                               bg="#95a5a6", fg="white",
                                               activebackground="#7f8c8d", 
                                               activeforeground="white",
                                               bd=0, cursor="hand2", height=2)
                        self.btn_update.pack(fill=X, pady=(10, 0))

        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}")

    def update_pass(self):
        if self.var_new_pass.get() == "" or self.var_confirm_pass.get() == "":
            messagebox.showerror("Error", "All fields are required", parent=self.forget_win)
        elif self.var_new_pass.get() != self.var_confirm_pass.get():
            messagebox.showerror("Error", "Password and Confirm Password should be same", 
                               parent=self.forget_win)
        else:
            connection = mysql.connector.connect(
                host="localhost",
                user="root",
                password="ishan",
                database="IMS"
            )
            try:
                cursor = connection.cursor()
                cursor.execute("update employee set pass=%s where eid=%s", 
                              (self.var_new_pass.get(), self.userid.get()))
                connection.commit()
                connection.close()
                messagebox.showinfo("Success", "Password Updated Successfully", 
                                   parent=self.forget_win)
                self.forget_win.destroy()
            except Exception as ex:
                messagebox.showerror("Error", f"Error due to: {str(ex)}")

    def validate_otp(self):
        if str(self.otp) == self.var_otp.get():
            self.btn_update.config(state=NORMAL, bg="#3498db", activebackground="#2980b9")
            self.btn_reset.config(state=DISABLED, bg="#95a5a6")
            messagebox.showinfo("Success", "OTP Verified Successfully", parent=self.forget_win)
        else:
            messagebox.showerror("Error", "Invalid OTP, Try Again!!!", parent=self.forget_win)

    def send_email(self, to_):
        s = smtplib.SMTP('smtp.gmail.com', 587)
        s.starttls()
        email_ = email_pass.email_
        pass_ = email_pass.pass_

        s.login(email_, pass_)

        self.otp = int(time.strftime("%H%S%M")) + int(time.strftime("%S"))
        
        subj = 'IMS - OTP for Password Reset'
        msg = f'''Dear User,

Your OTP for Password Reset is: {self.otp}

Note: This OTP is valid for a limited time only.

With Regards,
IMS Team'''
        message = 'Subject: {}\n\n{}'.format(subj, msg)
        s.sendmail(email_, to_, message)
        chk = s.ehlo()
        if chk[0] == 250:
            return 's'
        else:
            return 'f'

root = Tk()
obj = Login_System(root)
root.mainloop()