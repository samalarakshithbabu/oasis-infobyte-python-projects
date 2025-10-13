import tkinter as tk
from tkinter import ttk, messagebox
import random
import string
import pyperclip

class SecurePasswordForge:
    def __init__(self, master_window):
        self.master = master_window
        self.master.title("🔐 Secure Password Forge")
        self.master.geometry("550x650")
        self.master.resizable(False, False)
        self.master.configure(bg='#f0f0f0')
        
        self.initialize_interface()
        
    def initialize_interface(self):
        container = ttk.Frame(self.master, padding="25")
        container.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        header_label = ttk.Label(container, text="🛡️ Secure Password Forge", 
                               font=("Segoe UI", 18, "bold"))
        header_label.grid(row=0, column=0, columnspan=2, pady=(0, 25))
        
        length_frame = ttk.LabelFrame(container, text="📏 Length Configuration", padding="15")
        length_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=10)
        
        ttk.Label(length_frame, text="Password Length:").grid(row=0, column=0, sticky=tk.W, pady=8)
        self.length_control = tk.StringVar(value="16")
        length_spinner = ttk.Spinbox(length_frame, from_=6, to=64, width=12, 
                                   textvariable=self.length_control)
        length_spinner.grid(row=0, column=1, sticky=tk.W, pady=8)
        
        char_frame = ttk.LabelFrame(container, text="🔤 Character Selection", padding="15")
        char_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=10)
        
        self.use_lowercase = tk.BooleanVar(value=True)
        self.use_uppercase = tk.BooleanVar(value=True)
        self.use_digits = tk.BooleanVar(value=True)
        self.use_symbols = tk.BooleanVar(value=True)
        
        ttk.Checkbutton(char_frame, text="🔤 Lowercase letters (a-z)", 
                       variable=self.use_lowercase).grid(row=0, column=0, sticky=tk.W, pady=3)
        ttk.Checkbutton(char_frame, text="🔠 Uppercase letters (A-Z)", 
                       variable=self.use_uppercase).grid(row=1, column=0, sticky=tk.W, pady=3)
        ttk.Checkbutton(char_frame, text="🔢 Numeric digits (0-9)", 
                       variable=self.use_digits).grid(row=2, column=0, sticky=tk.W, pady=3)
        ttk.Checkbutton(char_frame, text="🔣 Special symbols (!@#$...)", 
                       variable=self.use_symbols).grid(row=3, column=0, sticky=tk.W, pady=3)
        
        security_frame = ttk.LabelFrame(container, text="🛡️ Security Options", padding="15")
        security_frame.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=10)
        
        self.enforce_strength = tk.BooleanVar(value=True)
        ttk.Checkbutton(security_frame, text="✅ Enforce strong password requirements", 
                       variable=self.enforce_strength).grid(row=0, column=0, sticky=tk.W, pady=5)
        
        self.avoid_ambiguous = tk.BooleanVar(value=True)
        ttk.Checkbutton(security_frame, text="🚫 Avoid ambiguous characters (0,O,1,l,I)", 
                       variable=self.avoid_ambiguous).grid(row=1, column=0, sticky=tk.W, pady=5)
        
        exclusion_frame = ttk.LabelFrame(container, text="❌ Character Exclusion", padding="15")
        exclusion_frame.grid(row=4, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=10)
        
        ttk.Label(exclusion_frame, text="Exclude these characters:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.excluded_chars = tk.StringVar()
        exclusion_entry = ttk.Entry(exclusion_frame, textvariable=self.excluded_chars, width=35)
        exclusion_entry.grid(row=0, column=1, sticky=tk.W, padx=(10, 0), pady=5)
        
        generate_button = ttk.Button(container, text="🎲 Generate Secure Password", 
                                   command=self.create_password)
        generate_button.grid(row=5, column=0, columnspan=2, pady=25)
        
        output_frame = ttk.LabelFrame(container, text="📋 Generated Password", padding="15")
        output_frame.grid(row=6, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=10)
        
        self.password_output = tk.StringVar()
        password_display = ttk.Entry(output_frame, textvariable=self.password_output, 
                                   width=55, font=("Consolas", 11), state="readonly")
        password_display.grid(row=0, column=0, columnspan=2, pady=8)
        
        copy_button = ttk.Button(output_frame, text="📋 Copy Password", 
                               command=self.copy_to_clipboard)
        copy_button.grid(row=1, column=0, pady=8, padx=(0, 10))
        
        strength_button = ttk.Button(output_frame, text="🔍 Analyze Strength", 
                                   command=self.analyze_strength)
        strength_button.grid(row=1, column=1, pady=8)
        
        self.strength_display = tk.StringVar()
        strength_indicator = ttk.Label(output_frame, textvariable=self.strength_display, 
                                     font=("Segoe UI", 10, "bold"))
        strength_indicator.grid(row=2, column=0, columnspan=2, pady=8)
        
    def build_character_pool(self):
        pool = ""
        if self.use_lowercase.get():
            pool += string.ascii_lowercase
        if self.use_uppercase.get():
            pool += string.ascii_uppercase
        if self.use_digits.get():
            pool += string.digits
        if self.use_symbols.get():
            pool += "!@#$%^&*()_+-=[]{}|;:,.<>?"
        
        if self.avoid_ambiguous.get():
            ambiguous = "0O1lI"
            pool = ''.join(char for char in pool if char not in ambiguous)
        
        excluded = self.excluded_chars.get()
        if excluded:
            pool = ''.join(char for char in pool if char not in excluded)
        
        return pool
    
    def validate_security_requirements(self, password):
        if len(password) < 8:
            return False, "Password must contain at least 8 characters"
        
        requirements = []
        if self.use_lowercase.get() and not any(c.islower() for c in password):
            requirements.append("lowercase letter")
        if self.use_uppercase.get() and not any(c.isupper() for c in password):
            requirements.append("uppercase letter")
        if self.use_digits.get() and not any(c.isdigit() for c in password):
            requirements.append("numeric digit")
        if self.use_symbols.get() and not any(c in "!@#$%^&*()_+-=[]{}|;:,.<>?" for c in password):
            requirements.append("special symbol")
        
        if requirements:
            return False, f"Password must include: {', '.join(requirements)}"
        
        return True, "Password meets security requirements"
    
    def create_password(self):
        try:
            pwd_length = int(self.length_control.get())
            if pwd_length < 6 or pwd_length > 64:
                messagebox.showerror("Invalid Length", "Password length must be between 6 and 64 characters")
                return
            
            char_pool = self.build_character_pool()
            if not char_pool:
                messagebox.showerror("No Characters", "Please select at least one character type")
                return
            
            if self.enforce_strength.get() and pwd_length >= 8:
                password_chars = []
                available_types = []
                
                if self.use_lowercase.get():
                    available_types.append([c for c in string.ascii_lowercase if c in char_pool])
                if self.use_uppercase.get():
                    available_types.append([c for c in string.ascii_uppercase if c in char_pool])
                if self.use_digits.get():
                    available_types.append([c for c in string.digits if c in char_pool])
                if self.use_symbols.get():
                    available_types.append([c for c in "!@#$%^&*()_+-=[]{}|;:,.<>?" if c in char_pool])
                
                for char_type in available_types:
                    if char_type:
                        password_chars.append(random.choice(char_type))
                
                remaining_length = pwd_length - len(password_chars)
                password_chars.extend(random.choice(char_pool) for _ in range(remaining_length))
                
                random.shuffle(password_chars)
                generated_password = ''.join(password_chars)
            else:
                generated_password = ''.join(random.choice(char_pool) for _ in range(pwd_length))
            
            self.password_output.set(generated_password)
            self.analyze_strength()
            
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a valid password length")
        except Exception as error:
            messagebox.showerror("Generation Error", f"An error occurred: {str(error)}")
    
    def copy_to_clipboard(self):
        password = self.password_output.get()
        if password:
            try:
                pyperclip.copy(password)
                messagebox.showinfo("Success", "🎉 Password copied to clipboard!")
            except Exception:
                self.master.clipboard_clear()
                self.master.clipboard_append(password)
                messagebox.showinfo("Success", "🎉 Password copied to clipboard!")
        else:
            messagebox.showwarning("No Password", "⚠️ Generate a password first")
    
    def analyze_strength(self):
        password = self.password_output.get()
        if not password:
            return
        
        strength_score = 0
        feedback_items = []
        
        if len(password) >= 16:
            strength_score += 3
        elif len(password) >= 12:
            strength_score += 2
        elif len(password) >= 8:
            strength_score += 1
        else:
            feedback_items.append("Increase length to 8+ characters")
        
        if any(c.islower() for c in password):
            strength_score += 1
        else:
            feedback_items.append("Add lowercase letters")
            
        if any(c.isupper() for c in password):
            strength_score += 1
        else:
            feedback_items.append("Add uppercase letters")
            
        if any(c.isdigit() for c in password):
            strength_score += 1
        else:
            feedback_items.append("Add numeric digits")
            
        if any(c in "!@#$%^&*()_+-=[]{}|;:,.<>?" for c in password):
            strength_score += 1
        else:
            feedback_items.append("Add special symbols")
        
        if strength_score >= 6:
            strength_level = "🟢 Excellent"
        elif strength_score >= 4:
            strength_level = "🟡 Good"
        elif strength_score >= 2:
            strength_level = "🟠 Fair"
        else:
            strength_level = "🔴 Weak"
        
        self.strength_display.set(f"Strength: {strength_level}")

def launch_application():
    root_window = tk.Tk()
    application = SecurePasswordForge(root_window)
    root_window.mainloop()

if __name__ == "__main__":
    launch_application()