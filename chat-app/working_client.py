import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import socket
import threading
import json
from cryptography.fernet import Fernet

class SecureMessenger:
    def __init__(self):
        self.network_conn = None
        self.encryptor = None
        self.user_name = None
        self.build_interface()
        
    def build_interface(self):
        self.main_app = tk.Tk()
        self.main_app.title("Secure Communication Hub")
        self.main_app.geometry("850x650")
        
        self.auth_section = ttk.Frame(self.main_app)
        self.auth_section.pack(fill='both', expand=True)
        
        ttk.Label(self.auth_section, text="User ID:").pack(pady=12)
        self.user_field = ttk.Entry(self.auth_section, width=32)
        self.user_field.pack(pady=6)
        
        ttk.Label(self.auth_section, text="Access Code:").pack(pady=12)
        self.pass_field = ttk.Entry(self.auth_section, show="*", width=32)
        self.pass_field.pack(pady=6)
        
        ttk.Button(self.auth_section, text="Access", command=self.authenticate_user).pack(pady=12)
        ttk.Button(self.auth_section, text="New Account", command=self.create_user).pack(pady=6)
        
        self.comm_section = ttk.Frame(self.main_app)
        
        self.message_display = scrolledtext.ScrolledText(self.comm_section, height=22, state='disabled')
        self.message_display.pack(fill='both', expand=True, padx=12, pady=12)
        
        text_panel = ttk.Frame(self.comm_section)
        text_panel.pack(fill='x', padx=12, pady=6)
        
        self.text_field = ttk.Entry(text_panel)
        self.text_field.pack(side='left', fill='x', expand=True)
        self.text_field.bind('<Return>', self.transmit_text)
        
        ttk.Button(text_panel, text="Transmit", command=self.transmit_text).pack(side='right', padx=6)
        
        self.connection_info = ttk.Label(self.main_app, text="Disconnected")
        self.connection_info.pack(side='bottom', fill='x')
        
    def establish_connection(self):
        try:
            self.network_conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.network_conn.connect(('127.0.0.1', 9999))
            threading.Thread(target=self.listen_incoming, daemon=True).start()
            return True
        except Exception as e:
            messagebox.showerror("Connection Failed", f"Unable to reach server: {e}")
            return False
            
    def create_user(self):
        user_id = self.user_field.get().strip()
        access_code = self.pass_field.get().strip()
        
        if not user_id or not access_code:
            messagebox.showerror("Input Required", "Please provide user ID and access code")
            return
            
        if not self.establish_connection():
            return
            
        request = {'action': 'register', 'username': user_id, 'password': access_code}
        self.transmit_data(request)
        
    def authenticate_user(self):
        user_id = self.user_field.get().strip()
        access_code = self.pass_field.get().strip()
        
        if not user_id or not access_code:
            messagebox.showerror("Input Required", "Please provide user ID and access code")
            return
            
        if not self.establish_connection():
            return
            
        self.user_name = user_id
        request = {'action': 'login', 'username': user_id, 'password': access_code}
        self.transmit_data(request)
        
    def transmit_data(self, data):
        try:
            payload = json.dumps(data).encode('utf-8')
            if self.encryptor:
                payload = self.encryptor.encrypt(payload)
            self.network_conn.send(payload)
        except Exception as e:
            messagebox.showerror("Transmission Error", f"Data send failed: {e}")
            
    def listen_incoming(self):
        while True:
            try:
                incoming = self.network_conn.recv(1024)
                if not incoming:
                    break
                    
                try:
                    if self.encryptor:
                        decoded = self.encryptor.decrypt(incoming)
                        response = json.loads(decoded.decode('utf-8'))
                    else:
                        response = json.loads(incoming.decode('utf-8'))
                except:
                    response = json.loads(incoming.decode('utf-8'))
                    
                self.process_response(response)
            except Exception as e:
                print(f"Reception error: {e}")
                break
                
    def process_response(self, response):
        self.main_app.after(0, self._handle_response, response)
        
    def _handle_response(self, response):
        if response.get('status') == 'success':
            if 'key' in response:
                self.encryptor = Fernet(response['key'].encode())
                self.activate_communication()
            else:
                messagebox.showinfo("Success", response['message'])
        elif response.get('status') == 'error':
            messagebox.showerror("Error", response['message'])
        elif response.get('action') == 'new_message':
            self.show_text(f"[{response['timestamp']}] {response['username']}: {response['message']}")
            
    def activate_communication(self):
        self.auth_section.pack_forget()
        self.comm_section.pack(fill='both', expand=True)
        self.connection_info.config(text=f"Active as {self.user_name}")
        self.show_text("Communication established! Start messaging below.")
        
    def show_text(self, content):
        self.message_display.config(state='normal')
        self.message_display.insert(tk.END, content + "\n")
        self.message_display.config(state='disabled')
        self.message_display.see(tk.END)
        
    def transmit_text(self, event=None):
        content = self.text_field.get().strip()
        if content and self.user_name:
            request = {
                'action': 'send_message',
                'username': self.user_name,
                'message': content,
                'room': 'main'
            }
            self.transmit_data(request)
            self.text_field.delete(0, tk.END)
            
    def launch(self):
        self.main_app.mainloop()

if __name__ == "__main__":
    messenger = SecureMessenger()
    messenger.launch()