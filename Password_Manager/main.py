import tkinter as tk
from tkinter import Label, Canvas, Entry, Button, PhotoImage, END, Toplevel
from tkinter import ttk
from pathlib import Path
from db import DbOperation

class PasswordManagerApp:
    def __init__(self, master, db):

        self.db = db
        self.master = master
        self.master.title("Password Manager")
        self.master.geometry("800x500")
        self.master.configure(bg="#FFFFFF")

        # Specify the path to the assets directory
        self.assets_path = Path(r"assets\frame0")

        self.create_widgets()

    def create_widgets(self):
        self.canvas = Canvas(
            self.master,
            bg="#FFFFFF",
            height=500,
            width=800,
            bd=0,
            highlightthickness=0,
            relief="ridge"
        )
        self.canvas.place(x=0, y=0)

        # Create password entry fields with larger text size
        self.entry_1 = self.create_entry(12.0, 174.0, 165.0, 33.0, "Website Name", "entry_1.png")
        self.entry_2 = self.create_entry(203.0, 174.0, 165.0, 33.0, "Username", "entry_2.png")
        self.entry_3 = self.create_entry(394.0, 174.0, 165.0, 33.0, "Password", "entry_3.png", is_password=True)
        self.entry_4 = self.create_entry(12.0, 109.0, 232.0, 29.0, "Website", "entry_4.png")
        self.entry_5 = self.create_entry(580.0, 440.0, 200.0, 29.0, "ID", "entry_1.png")

        # Create buttons
        self.create_button(255.0, 106.0, 207.0, 37.0, "Search_button", "button_1.png")
        self.create_button(588.0, 317.0, 207.0, 37.0, "Show_Button", "button_2.png")
        self.create_button(588.0, 266.0, 206.0, 37.0, "Copy_Button", "button_3.png")
        self.create_button(627.0, 209.0, 167.0, 40.0, "Delete_Button", "button_4.png")
        self.create_button(627.0, 161.0, 168.0, 37.0, "Update_Button", "button_5.png")
        self.create_button(627.0, 109.0, 168.0, 38.0, "Save_Button", "button_6.png")
        self.create_button(588.0, 365.0, 207.0, 37.0, "Clear_Button", "button_8.png")
        self.create_button(560.0, 174.0, 50.0, 33.0, "Show_Pass", "button_7.png")

        # Draw header
        self.canvas.create_rectangle(0.0, 0.0, 800.0, 85.0, fill="#92EFFD", outline="")
        self.canvas.create_text(211.0, 1, anchor="nw", text="Password Manager", fill="#000000", font=("Kodchasan ExtraLight", 32))

        self.tree_view()

        

    def create_entry(self, x, y, width, height, label_text, image_name, is_password=False, font_size=12):
        entry_image = PhotoImage(file=self.assets_path / image_name)
        entry_bg = self.canvas.create_image(x + width / 2, y + height / 2, image=entry_image)

        entry = Entry(
            self.master,
            bd=0,
            bg="#D9D9D9",
            fg="#000716",
            highlightthickness=0,
            show='*' if is_password else '',
            font=("Inter SemiBold", font_size)
        )
        entry.place(x=x, y=y, width=width, height=height)

        self.canvas.create_text(x, y - 15, anchor="nw", text=label_text, fill="#000000", font=("Inter SemiBold", 12))

        return entry

    def create_button(self, x, y, width, height, command, image_name):
        button_image = PhotoImage(file=self.assets_path / image_name)
        button = Button(
            self.master,
            image=button_image,
            borderwidth=0,
            highlightthickness=0,
            command=self.get_command_method(command),
            relief="flat"
        )
        button.image = button_image
        button.place(x=x, y=y, width=width, height=height)

    def get_command_method(self, command):
    # Define a mapping between command strings and corresponding methods
        methods_mapping = {
        "Save_Button": self.save_record,
        "Update_Button": self.update_record,
        "Delete_Button": self.delete_record,
        "Show_Button": self.show_record,
        "Copy_Button": self.copy_password,
        "Search_button": self.search,
        "Clear_Button": self.clear,
        "Show_Pass": self.show
        }
        # Return the method based on the command string
        return methods_mapping.get(command, lambda: print("Invalid command"))

    # Create Read Update Delete Functions

    def save_record(self):
        website = self.entry_1.get()
        username = self.entry_2.get()
        password = self.entry_3.get()

        data = {'website': website, 'username': username, 'password':password}
        self.db.create_record(data)

        self.show_record()

    def update_record(self):
        id = self.entry_5.get()
        website = self.entry_1.get()
        username = self.entry_2.get()
        password = self.entry_3.get()

        data = {'ID': id, 'website': website, 'username': username, 'password':password}
        self.db.update_record(data)

        self.show_record()

    def delete_record(self):
        id = self.entry_5.get()
        self.db.delete_record(id)

        self.show_record()

    def show_record(self):

        for item in self.records_tree.get_children():
            self.records_tree.delete(item)

        record_list = self.db.show_records()
        
        for i in record_list:
            self.records_tree.insert('',END, values=(i[0], i[3], i[4], i[5]))

    def item_selected(self, event):
        for selected_item in self.records_tree.selection():
            item = self.records_tree.item(selected_item)
            record = item['values']
            
        for entry_box, item in zip([self.entry_5, self.entry_1, self.entry_2, self.entry_3], record):
            entry_box.delete(0, END)
            entry_box.insert(0, item)

    def tree_view(self):
        column = ('ID', 'Website', 'Username', 'Password')
        self.records_tree = ttk.Treeview(self.master, columns=column, show="headings")
        self.records_tree.heading('Website', text='Website Name')
        self.records_tree.heading('Username', text='Username')

        self.records_tree.column('Website', width=150)
        self.records_tree.column('Username', width=200)

        self.records_tree['displaycolumns'] = ('Website', 'Username')

        self.records_tree.bind('<<TreeviewSelect>>', self.item_selected)  # Adjust accordingly

        self.records_tree.grid(padx=100, pady=250, columnspan=6)
        

    #Copy to Clipboard
    def copy_password(self):
        self.master.clipboard_clear()
        self.master.clipboard_append(self.entry_3.get())
        message = "Password Copied"
        title = "Copy"
        self.show_message(title, message)

        if self.entry_3.get == "":
            message = "Box is Empty"
            title = "Error"
            self.show_message(title, message)

    def show_message(self, title_box: str = None, message: str = None):
        TIME_TO_WAIT = 900
        root = Toplevel(self.master)
        background = 'blue'

        if title_box == "Error":
            background = 'red'

        root.geometry('200x30+600+200')
        root.title(title_box)

        Label(root, text=message, background=background, font=("Ariel", 15), fg='white').pack(padx=4, pady=2)

        try:
            root.after(TIME_TO_WAIT, root.destroy)
        except Exception as e:
            print("Error Occured", e)


    def search(self):

        website = self.entry_4.get()

        for item in self.records_tree.get_children():
            self.records_tree.delete(item)

        record_list = self.db.search(website)

        for i in record_list:
            self.records_tree.insert('',END, values=(i[0], i[3], i[4], i[5]))

    def clear(self):
        self.entry_1.delete(0, 'end')
        self.entry_2.delete(0, 'end')
        self.entry_3.delete(0, 'end')
        self.entry_4.delete(0, 'end')
        self.entry_5.delete(0, 'end')

    def show(self):
        current_show_state = self.entry_3.cget("show")
        if current_show_state == "":
            # Currently showing plain text, switch to masked mode (asterisks)
            self.entry_3.config(show="*")
        else:
            # Currently showing masked mode, switch to plain text
            self.entry_3.config(show="")

if __name__ == "__main__":

    #Creates Table if does not exists
    db_class = DbOperation()
    db_class.create_table()

    #App Window
    root = tk.Tk()
    app = PasswordManagerApp(root, db_class)
    root.resizable(False, False)
    root.mainloop()
