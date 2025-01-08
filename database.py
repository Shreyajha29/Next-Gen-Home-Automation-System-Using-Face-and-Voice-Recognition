from tkinter import *
from PIL import Image, ImageTk
from tkinter import messagebox
import mysql.connector
from io import BytesIO

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
    root = Tk()
    app = RegisteredUsers(root)
    root.mainloop()
