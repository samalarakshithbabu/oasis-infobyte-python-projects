import tkinter as tk
from tkinter import ttk, messagebox
import socket
import json
import threading

class ChatClient:
    def __init__(self):
        self.socket = None
        self.username = None
        self.setup_gui()
    
    def setup_gui(self):
        self.root = tk.Tk()
        self.root.title("Chat Application")
        self.root.geometry("400x300")
        
        # Login Frame
        self.login_frame = ttk.Frame(self.root)
        self.login_frame.pack(expand=True, fill='both', padx=20, pady=20)
        
        ttk.Label(self.login_frame, text="Username:").pack(pady=5)
        self.username_entry = ttk.Entry(self.login_frame)
        self.username_entry.pack(pady=5)
        
        ttk.Label(self.login_frame, text="Password:").pack(pady=5)
        self.password_entry = ttk.Entry(self.login_frame, show="*")
        self.password_entry.pack(pady=5)
        
        button_frame = ttk.Frame(self.login_frame)
        button_frame.pack(pady=20)
        
        self.login_btn = ttk.Button(button_frame, text="Sign In", command=self.login)
        self.login_btn.pack(side='left', padx=5)
        
        self.register_btn = ttk.Button(button_frame, text="Create Account", command=self.register)
        self.register_btn.pack(side='left', padx=5)
        
        self.status_label = ttk.Label(self.login_frame, text="Enter credentials to continue")
        self.status_label.pack(pady=10)
        
        # Chat Frame (hidden initially)
        self.chat_frame = ttk.Frame(self.root)
        
        self.chat_text = tk.Text(self.chat_frame, state='disabled', height=15)
        self.chat_text.pack(fill='both', expand=True, padx=10, pady=5)
        
        self.message_entry = ttk.Entry(self.chat_frame)
        self.message_entry.pack(fill='x', padx=10, pady=5)
        self.message_entry.bind('<Return>', self.send_message)
        
        ttk.Button(self.chat_frame, text="Send", command=self.send_message).pack(pady=5)
    
    def connect_to_server(self):
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.connect(('127.0.0.1', 9999))
            return True
        except Exception as e:
            messagebox.showerror("Connection Error", f"Cannot connect to server.\nMake sure server is running.\nError: {e}")
            return False
    
    def login(self):
        self.status_label.config(text="Connecting...")
        self.login_btn.config(state='disabled')
        
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()
        
        if not username or not password:
            messagebox.showerror("Error", "Please enter both username and password")
            self.login_btn.config(state='normal')
            self.status_label.config(text="Enter credentials to continue")
            return
        
        if not self.connect_to_server():
            self.login_btn.config(state='normal')
            self.status_label.config(text="Connection failed")
            return
        
        try:
            msg = {'action': 'login', 'username': username, 'password': password}
            self.socket.send(json.dumps(msg).encode('utf-8'))
            
            response = self.socket.recv(1024).decode('utf-8')
            data = json.loads(response)
            
            if data['status'] == 'success':
                self.username = username
                self.show_chat()
                messagebox.showinfo("Success", "Login successful!")
            else:
                messagebox.showerror("Error", data['message'])
                self.socket.close()
                
        except Exception as e:
            messagebox.showerror("Error", f"Login failed: {e}")
            if self.socket:
                self.socket.close()
        
        self.login_btn.config(state='normal')
        self.status_label.config(text="Enter credentials to continue")
    
    def register(self):
        self.status_label.config(text="Creating account...")
        self.register_btn.config(state='disabled')
        
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()
        
        if not username or not password:
            messagebox.showerror("Error", "Please enter both username and password")
            self.register_btn.config(state='normal')
            self.status_label.config(text="Enter credentials to continue")
            return
        
        if not self.connect_to_server():
            self.register_btn.config(state='normal')
            self.status_label.config(text="Connection failed")
            return
        
        try:
            msg = {'action': 'register', 'username': username, 'password': password}
            self.socket.send(json.dumps(msg).encode('utf-8'))
            
            response = self.socket.recv(1024).decode('utf-8')
            data = json.loads(response)
            
            messagebox.showinfo("Result", data['message'])
            self.socket.close()
            
        except Exception as e:
            messagebox.showerror("Error", f"Registration failed: {e}")
            if self.socket:
                self.socket.close()
        
        self.register_btn.config(state='normal')
        self.status_label.config(text="Enter credentials to continue")
    
    def show_chat(self):
        self.login_frame.pack_forget()
        self.chat_frame.pack(expand=True, fill='both', padx=10, pady=10)
        self.root.title(f"Chat - {self.username}")
        
        self.chat_text.config(state='normal')
        self.chat_text.insert(tk.END, f"Welcome {self.username}! You are now connected.\n")
        self.chat_text.config(state='disabled')
    
    def send_message(self, event=None):
        message = self.message_entry.get().strip()
        if message and self.socket:
            self.chat_text.config(state='normal')
            self.chat_text.insert(tk.END, f"You: {message}\n")
            self.chat_text.config(state='disabled')
            self.chat_text.see(tk.END)
            self.message_entry.delete(0, tk.END)
    
    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    client = ChatClient()
    client.run()