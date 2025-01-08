from tkinter import*
from tkinter import ttk
from PIL import Image, ImageTk 
from tkinter import messagebox, filedialog
import mysql.connector
 
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
        
        b1=Button(frame,image=self.photoimage1,borderwidth=0,cursor="hand2")
        b1.place(x=400,y=550, width=200)

    # Function to upload an image
    def upload_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.jpg *.png *.jpeg")])
        if file_path:
            self.var_image_path.set(file_path)
            self.image_label.config(text="Image Selected")
        else:
            self.image_label.config(text="No Image Selected")
          
        
#==================================================Function Declaration====================================
        
        
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
           
               
       
        
if __name__=="__main__":
    root=Tk()
    app=Register(root)
    root.mainloop()