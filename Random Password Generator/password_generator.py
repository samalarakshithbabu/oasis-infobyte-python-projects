import random
import string
import tkinter as tk
from tkinter import ttk, messagebox

class QuickPasswordMaker:
    def __init__(self):
        self.main_window = tk.Tk()
        self.main_window.title("⚡ Quick Password Maker")
        self.main_window.geometry("450x350")
        self.main_window.configure(bg='#e8f4fd')
        self.create_interface()
    
    def create_interface(self):
        container = ttk.Frame(self.main_window, padding="25")
        container.pack(fill=tk.BOTH, expand=True)
        
        title = ttk.Label(container, text="⚡ Quick Password Maker", font=("Arial", 14, "bold"))
        title.grid(row=0, column=0, columnspan=2, pady=(0, 20))
        
        ttk.Label(container, text="🔢 Password Length:").grid(row=1, column=0, sticky=tk.W, pady=8)
        self.pwd_length = tk.StringVar(value="14")
        length_spinner = ttk.Spinbox(container, from_=6, to=50, textvariable=self.pwd_length, width=12)
        length_spinner.grid(row=1, column=1, sticky=tk.W, pady=8)
        
        self.include_lower = tk.BooleanVar(value=True)
        self.include_upper = tk.BooleanVar(value=True)
        self.include_nums = tk.BooleanVar(value=True)
        self.include_specials = tk.BooleanVar(value=True)
        
        ttk.Checkbutton(container, text="🔤 Lowercase letters (a-z)", variable=self.include_lower).grid(row=2, column=0, columnspan=2, sticky=tk.W, pady=3)
        ttk.Checkbutton(container, text="🔠 Uppercase letters (A-Z)", variable=self.include_upper).grid(row=3, column=0, columnspan=2, sticky=tk.W, pady=3)
        ttk.Checkbutton(container, text="🔢 Numeric digits (0-9)", variable=self.include_nums).grid(row=4, column=0, columnspan=2, sticky=tk.W, pady=3)
        ttk.Checkbutton(container, text="🔣 Special characters (!@#$)", variable=self.include_specials).grid(row=5, column=0, columnspan=2, sticky=tk.W, pady=3)
        
        create_btn = ttk.Button(container, text="🎲 Create Password", command=self.build_password)
        create_btn.grid(row=6, column=0, columnspan=2, pady=25)
        
        self.result_password = tk.StringVar()
        pwd_display = ttk.Entry(container, textvariable=self.result_password, width=45, font=("Consolas", 11))
        pwd_display.grid(row=7, column=0, columnspan=2, pady=12)
        
        copy_btn = ttk.Button(container, text="📋 Copy to Clipboard", command=self.copy_result)
        copy_btn.grid(row=8, column=0, columnspan=2, pady=10)
    
    def build_password(self):
        try:
            pwd_len = int(self.pwd_length.get())
            character_set = ""
            
            if self.include_lower.get(): 
                character_set += string.ascii_lowercase
            if self.include_upper.get(): 
                character_set += string.ascii_uppercase
            if self.include_nums.get(): 
                character_set += string.digits
            if self.include_specials.get(): 
                character_set += "!@#$%^&*+=?<>"
            
            if not character_set:
                messagebox.showerror("❌ Error", "Please select at least one character type")
                return
            
            new_password = ''.join(random.choice(character_set) for _ in range(pwd_len))
            self.result_password.set(new_password)
            
        except ValueError:
            messagebox.showerror("❌ Error", "Please enter a valid length")
    
    def copy_result(self):
        current_password = self.result_password.get()
        if current_password:
            self.main_window.clipboard_clear()
            self.main_window.clipboard_append(current_password)
            messagebox.showinfo("✅ Success", "Password copied to clipboard!")
        else:
            messagebox.showwarning("⚠️ Warning", "No password to copy")
    
    def start_application(self):
        self.main_window.mainloop()

def launch_quick_maker():
    maker = QuickPasswordMaker()
    maker.start_application()

if __name__ == "__main__":
    launch_quick_maker()