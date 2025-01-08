from tkinter import*
from tkinter import ttk
from PIL import Image, ImageTk 
from tkinter import messagebox, filedialog
import mysql.connector
from io import BytesIO
 
def main():
    win=Tk()
    app=Login_Window(win)
    win.mainloop()


class Login_Window:
    def __init__(self,root):
        self.root= root
        self.root.title("Login")
        self.root.geometry("1920x1080+0+0")
        self.bg=ImageTk.PhotoImage(file=r"C:\\Users\\DELL\\Desktop\\New folder\\Images\\wp2915522.png")
        lbl_bg=Label(self.root,image=self.bg)
        lbl_bg.place(x=0, y=0, relwidth=1,relheight=1)
        frame=Frame(self.root, bg="black")
        frame.place(x=500,y=170,width=440, height= 490)
        
        img1=Image.open(r"C:\\Users\\DELL\\Desktop\\New folder\\Images\\icon-symbol-or-website-admin-social-login-element-concept-3d-rendering-png.png")
        img1=img1.resize((100,100), Image.LANCZOS)
        self.photoimage1=ImageTk.PhotoImage(img1)
        lblimg1=Label(image=self.photoimage1,bg="black",borderwidth=0)
        lblimg1.place(x=660, y=178, width=100, height=100)
        
        
        get_str=Label(frame, text="Get Started", font=("times new roman",20,"bold"),fg="white", bg="black")
        get_str.place(x= 150,  y=100)
        
        #Label
        username=lbl=Label(frame, text="Username",font=("times new roman",16,"bold"),fg="white", bg="black")
        username.place(x=110, y=155)
        self.txtuser=ttk.Entry(frame,font=("times new roman",16,"bold"))
        self.txtuser.place(x=100, y=196,width=250)
        
        password=lbl=Label(frame, text="Password",font=("times new roman",16,"bold"),fg="white", bg="black")
        password.place(x=114, y=255)
        self.txtpass=ttk.Entry(frame,font=("times new roman",16,"bold"))
        self.txtpass.place(x=100, y=300,width=250)
        
        #icon images
        img2=Image.open(r"C:\\Users\\DELL\\Desktop\\New folder\\Images\\icon-symbol-or-website-admin-social-login-element-concept-3d-rendering-png.png")
        img2=img2.resize((28,28), Image.LANCZOS)
        self.photoimage2=ImageTk.PhotoImage(img2)
        lblimg2=Label(image=self.photoimage2,bg="black",borderwidth=0)
        lblimg2.place(x=575, y=320, width=28, height=28)
        
        img3=Image.open(r"C:\\Users\\DELL\\Desktop\\New folder\\Images\\images_2_-removebg-preview.png")
        img3=img3.resize((28,28), Image.LANCZOS)
        self.photoimage3=ImageTk.PhotoImage(img3)
        lblimg3=Label(image=self.photoimage3,bg="black",borderwidth=0)
        lblimg3.place(x=575, y=420, width=28, height=30)
        #login button
        loginbtn=Button(frame,command=self.login,text="Login",font=("times new roman",16,"bold"),bd=3, relief=RIDGE, fg="white", bg="red",activeforeground="white", activebackground="red")
        loginbtn.place(x=160, y=366, width= 120, height=35)
       
        #Register Button
        registerbtn=Button(frame, text="New User Register",command=self.register_window, font=("times new roman",12,"bold"),borderwidth=0, fg="white", bg="black",activeforeground="white", activebackground="black")
        registerbtn.place(x=140, y=420, width= 160)
        
        #forget passbtn
        registerbtn=Button(frame, text="Forget Password",command=self.forgot_password_window,font=("times new roman",12,"bold"),borderwidth=0, fg="white", bg="black",activeforeground="white", activebackground="black")
        registerbtn.place(x=140, y=440, width=160)
        
    def register_window(self):    
        self.new_window=Toplevel(self.root)
        self.app=Register(self.new_window)

    def login(self):
        if self.txtuser.get()==""or self.txtpass.get()=="":
            messagebox.showerror("Error","all field required")
        elif self.txtuser.get()=="shreyu" and self.txtpass.get()=="4433":
            messagebox.showinfo("Success","Welcome to our Home")
        else:
            conn=mysql.connector.connect(host="localhost",user="root",password="Shreya@14",database="mydata")
            my_cursor=conn.cursor()
            my_cursor.execute("select * from Register where email=%s and password=%s",(
                                                                                      self.txtuser.get(),
                                                                                      self.txtpass.get()
                                                                                      ))
            
            row= my_cursor.fetchone()
            # print(row)
            if row==None:
                messagebox.showerror("Error","Invalid Username & Password")
            else:
                open_main= messagebox.askyesno("YesNo","Access only admin")
                if open_main>0:
                    self.new_window=Toplevel(self.root)
                    self.app=RegisteredUsers(self.new_window)
                else:
                    if not open_main:
                        return
            conn.commit()
            conn.close()
#==============================================Reset Password===============================================
    def reset_pass(self):
        if self.txt_newpass.get() == "":
            messagebox.showerror("Error", "Please enter the new password",parent=self.root2)
        else:
            try:
                conn = mysql.connector.connect(host="localhost", user="root", password="Shreya@14", database="mydata")
                my_cursor = conn.cursor()

                query = "update register set password=%s where email=%s"
                value = (self.txt_newpass.get(), self.txtuser.get())
                my_cursor.execute(query, value)

                conn.commit()
                conn.close()
                messagebox.showinfo("Success", "Your password has been reset. Please log in using the new password.",parent=self.root2)
                if hasattr(self, 'root2'):
                    self.root2.destroy()  # Close the forgot password window
            except Exception as e:
                messagebox.showerror("Error", f"Something went wrong: {str(e)}")
                self.root2.destroy()

#==============================================Forgot Password===============================================
    def forgot_password_window(self):
        if self.txtuser.get()=="":
            messagebox.showerror("Error","Please enter valid Email address to reset password",parent=self.root2)
        else:
            conn=mysql.connector.connect(host="localhost",user="root",password="Shreya@14",database="mydata")
            my_cursor=conn.cursor()
            query= ("select * from register where email=%s")
            value= (self.txtuser.get(),)
            my_cursor.execute(query,value)
            row= my_cursor.fetchone()
            #print(row)

            if row==None:
                messagebox.showerror("My Error","Please enter valid user name",parent=self.root2)
            else:
                conn.close()
                self.root2=Toplevel()
                self.root2.title("Forgot Password")
                self.root2.geometry("340x350+610+170")

                l= Label(self.root2,text="Forgot Password",font=("times new roman",20,"bold"),fg="red", bg="white")
                l.place(x=0,y=10,relwidth=1)
                
                new_password=Label(self.root2,text="New Password",font=("times new roman",20,"bold"),bg="white",fg="black")
                new_password.place(x=30,y=120)
                self.txt_newpass=ttk.Entry(self.root2,font=("times new roman",20,"bold"))
                self.txt_newpass.place(x=30,y=150)

                btn=Button(self.root2,text="Reset",command=self.reset_pass,font=("times new roman",20,"bold"),bg="white",fg="green")
                btn.place(x=120,y=200)
           
class Register:
    def __init__(self,root):
        self.root=root
        self.root.title("Register")
        self.root.geometry("1150x800+0+0")
        #======================================Variables====================================
        self.var_fname=StringVar()
        self.var_lname=StringVar()
        self.var_contact=StringVar()
        self.var_email=StringVar()
        self.var_pass=StringVar()
        self.var_confpass=StringVar()
        self.var_image_path = StringVar()  # For storing the image path
        
        
        #bg image
        self.bg=ImageTk.PhotoImage(file=r"C:\\Users\\DELL\\Desktop\\New folder\\Images\\pexels-sebastians-731082.jpg")
        bg_lbl=Label(self.root,image=self.bg)
        bg_lbl.place(x=0, y=0,relwidth=1, relheight=1)
        
        #left image
        self.bg1=ImageTk.PhotoImage(file=r"C:\\Users\\DELL\\Desktop\\New folder\\Images\\download.jpg")
        left_lbl=Label(self.root,image=self.bg1)
        left_lbl.place(x=100, y=80,width=460, height=600)
        
        #main frame
        
        frame=Frame(self.root, bg="white")
        frame.place(x=550,y=80,width=650, height= 600)
        
        register_lbl=Label(frame, text="REGISTER HERE", font=("times new roman",30,"bold"),fg="darkgreen", bg="white")
        register_lbl.place(x=50,y=30)
        
        #===================================label and entry=============================================
        
        #----------------------row1
        fname=Label(frame, text= "First Name", font=("times new roman",18,"bold"), bg="white")
        fname.place(x=50, y=150)
        self.fname_entry=ttk.Entry(frame,textvariable=self.var_fname,font=("times new roman",15,"bold"))
        self.fname_entry.place(x=50,y=190, width=250)
        
        
        l_name=Label(frame, text= "Last Name", font=("times new roman",18,"bold"),fg="black", bg="white")
        l_name.place(x=370, y=150)
        self.txt_lname=ttk.Entry(frame,textvariable=self.var_lname, font=("times new roman",15))
        self.txt_lname.place(x=370,y=190, width=250)
        
        #-----------------------row 2
        
        contact=Label(frame,text="Contact Number",font=("times new roman",18,"bold"),fg="black", bg="white")
        contact.place(x=50,y=250)
        self.txt_contact=ttk.Entry(frame,textvariable=self.var_contact, font=("times new roman",15))
        self.txt_contact.place(x=50,y=290, width=250)
        
        email=Label(frame,text="Email",font=("times new roman",18,"bold"),fg="black", bg="white")
        email.place(x=370,y=250)
        self.txt_email=ttk.Entry(frame,textvariable=self.var_email, font=("times new roman",15))
        self.txt_email.place(x=370,y=290, width=250)
        
        #------------------------row 3
        
        pswd=Label(frame,text="Password",font=("times new roman",18,"bold"),fg="black", bg="white")
        pswd.place(x=50,y=350)
        self.txt_pswd=ttk.Entry(frame,textvariable=self.var_pass,font=("times new roman",15))
        self.txt_pswd.place(x=50,y=390, width=250)
        
        confirm_pswd=Label(frame,text=" Confirm Password",font=("times new roman",18,"bold"),fg="black", bg="white")
        confirm_pswd.place(x=370,y=350)
        self.txt_confirm_pswd=ttk.Entry(frame,textvariable=self.var_confpass, font=("times new roman",15))
        self.txt_confirm_pswd.place(x=370,y=390, width=250)

        # Image Upload
        self.image_label = Label(frame, text="No Image Selected", font=("times new roman", 12), bg="white", fg="gray")
        self.image_label.place(x=50, y=460)

        upload_btn = Button(frame, text="Upload Image", command=self.upload_image, font=("times new roman", 12, "bold"),
                            bg="blue", fg="white", cursor="hand2")
        upload_btn.place(x=370, y=460, width=150)

        #==============checkButton=====================================
        self.var_check=IntVar()
        checkbtn=Checkbutton(frame,variable=self.var_check, text="I Agree the terms and condition",font=("times new roman",18,"bold"),offvalue=0,onvalue=1)
        checkbtn.place(x=50, y=500)
        
       #================button=========================================
        img=Image.open(r"C:\\Users\\DELL\\Desktop\\New folder\\Images\\WhatsApp_Image_2024-10-21_at_19.22.10_6bcd74c0-removebg-preview.png")
        img=img.resize((200,50),Image.LANCZOS)
        self.photoimage=ImageTk.PhotoImage(img)
        
        b1=Button(frame,image=self.photoimage,command=self.register_data, borderwidth=0,cursor="hand2")
        b1.place(x=50,y=550, width=200)
        
        img1=Image.open(r"C:\\Users\\DELL\\Desktop\\New folder\\Images\\images-removebg-preview.png")
        img1=img1.resize((200,45),Image.LANCZOS)
        self.photoimage1=ImageTk.PhotoImage(img1)
        
        b1=Button(frame,image=self.photoimage1,command=self.return_login,borderwidth=0,cursor="hand2")
        b1.place(x=400,y=550, width=200)

    # Function to upload an image
    def upload_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.jpg *.png *.jpeg")])
        if file_path:
            self.var_image_path.set(file_path)
            self.image_label.config(text="Image Selected")
        else:
            self.image_label.config(text="No Image Selected")
                
#==============================================Function Declaration==================================================
    def register_data(self):
        if self.var_fname.get()=="" or self.var_email.get()=="" or self.var_contact.get() == "" or not self.var_image_path.get():
            messagebox.showerror("Error", "All field are required")
        elif self.var_pass.get()!= self.var_confpass.get():
            messagebox.showerror("Error", "Password & Confirm must be same!")
        elif self.var_check.get()==0:
            messagebox.showerror("Error", "Please agree our terms and conditions")
        else:
           try:
                conn = mysql.connector.connect(host="localhost", user="root", password="Shreya@14", database="mydata")
                my_cursor = conn.cursor()
                query = "SELECT * FROM register WHERE email=%s"
                value = (self.var_email.get(),)
                my_cursor.execute(query, value)
                row = my_cursor.fetchone()
                if row is not None:
                    messagebox.showerror("Error", "User already exists, please try another email")
                else:
                    with open(self.var_image_path.get(), 'rb') as img_file:
                        img_data = img_file.read()
                    my_cursor.execute(
                        "INSERT INTO register (fname, lname, contact, email, password, image) VALUES (%s, %s, %s, %s, %s, %s)",
                        (self.var_fname.get(), self.var_lname.get(), self.var_contact.get(),
                         self.var_email.get(), self.var_pass.get(), img_data))
                    conn.commit()
                    conn.close()
                    messagebox.showinfo("Success", "Registration Successful! Welcome to the Family.")
           except Exception as e:
                messagebox.showerror("Error", f"Something went wrong: {str(e)}")
    
    def return_login(self):
        self.root.destroy()


class RegisteredUsers:

    def __init__(self, root):
        self.root = root
        self.root.title("Display Registered Data")
        self.root.geometry("400x300")
        self.root.configure(bg="#f0f0f0")

        # Button to open the Registered Users window
        btn_display = Button(
            self.root, text="Show Registered Data", command=self.display_data,
            font=("times new roman", 16), bg="#007acc", fg="white",
            activebackground="#005c99", activeforeground="white"
        )
        btn_display.pack(pady=100)

    def fetch_data(self):
        try:
            conn = mysql.connector.connect(
                host="localhost", user="root", password="Shreya@14", database="mydata"
            )
            my_cursor = conn.cursor()
            my_cursor.execute("SELECT fname, lname, contact, email, image FROM register")
            rows = my_cursor.fetchall()
            conn.close()
            return rows
        except Exception as e:
            messagebox.showerror("Database Error", f"Error: {e}")
            return []

    def display_data(self):
        data = self.fetch_data()

        if not data:
            messagebox.showinfo("Info", "No data available in the database.")
            return

        # Create a new fullscreen window
        display_window = Toplevel()
        display_window.title("Registered Users")
        display_window.state("zoomed")  # Open in fullscreen

        # Title Label
        title_label = Label(display_window, text="Registered Users", font=("times new roman", 24, "bold"), bg="#ffffff", fg="#333333")
        title_label.pack(pady=20)

        # Scrollable frame for user entries
        canvas = Canvas(display_window, bg="#1a0a00", highlightthickness=0)
        scrollbar = Scrollbar(display_window, orient=VERTICAL, command=canvas.yview)
        scrollable_frame = Frame(canvas, bg="#1a0a00")

        # Bind the scroll region
        scrollable_frame.bind(
            "<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side=LEFT, fill=BOTH, expand=True)
        scrollbar.pack(side=RIGHT, fill=Y)

        # Create a frame for each user
        for row in data:
            user_frame = Frame(scrollable_frame, bg="#ffffff", bd=2, relief=SOLID)
            user_frame.pack(pady=10, padx=10, fill=X)

            # Center layout with text and image
            content_frame = Frame(user_frame, bg="#ffffff")
            content_frame.pack(padx=20, pady=20)

            # Image display
            if row[4]:
                try:
                    img_data = row[4]
                    img = Image.open(BytesIO(img_data))
                    img = img.resize((150, 150), Image.LANCZOS)
                    photo = ImageTk.PhotoImage(img)
                    image_label = Label(content_frame, image=photo, bg="#ffffff")
                    image_label.image = photo  # Keep a reference to prevent garbage collection
                    image_label.grid(row=0, column=0, rowspan=4, padx=20)
                except Exception as e:
                    Label(content_frame, text="Error loading image", font=("times new roman", 12, "italic"), bg="#ffffff", fg="red").grid(row=0, column=0, rowspan=4, padx=20)
            else:
                Label(content_frame, text="No Image", font=("times new roman", 12, "italic"), bg="#ffffff", fg="#555555").grid(row=0, column=0, rowspan=4, padx=20)

            # Text information
            Label(content_frame, text=f"First Name: {row[0]}", font=("times new roman", 14), bg="#ffffff", anchor="w").grid(row=0, column=1, sticky="w", padx=10, pady=5)
            Label(content_frame, text=f"Last Name: {row[1]}", font=("times new roman", 14), bg="#ffffff", anchor="w").grid(row=1, column=1, sticky="w", padx=10, pady=5)
            Label(content_frame, text=f"Contact: {row[2]}", font=("times new roman", 14), bg="#ffffff", anchor="w").grid(row=2, column=1, sticky="w", padx=10, pady=5)
            Label(content_frame, text=f"Email: {row[3]}", font=("times new roman", 14), bg="#ffffff", anchor="w").grid(row=3, column=1, sticky="w", padx=10, pady=5)
        
        
if __name__ == "__main__":
    main()