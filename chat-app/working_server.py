import socket
import threading
import json
import sqlite3
from cryptography.fernet import Fernet
from datetime import datetime

class MessageHub:
    def __init__(self):
        self.active_users = {}
        self.security_key = Fernet.generate_key()
        self.encryptor = Fernet(self.security_key)
        self.initialize_storage()
        
    def initialize_storage(self):
        db_conn = sqlite3.connect('communication.db')
        db_cursor = db_conn.cursor()
        db_cursor.execute('''CREATE TABLE IF NOT EXISTS user_accounts 
                         (username TEXT PRIMARY KEY, password TEXT)''')
        db_cursor.execute('''CREATE TABLE IF NOT EXISTS chat_logs 
                         (id INTEGER PRIMARY KEY, username TEXT, message TEXT, timestamp TEXT)''')
        db_conn.commit()
        db_conn.close()
        
    def launch_hub(self):
        main_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        main_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        main_socket.bind(('127.0.0.1', 9999))
        main_socket.listen(8)
        print("Message hub operational on 127.0.0.1:9999")
        
        while True:
            try:
                user_conn, user_addr = main_socket.accept()
                print(f"User connected: {user_addr}")
                threading.Thread(target=self.manage_user, args=(user_conn, user_addr), daemon=True).start()
            except KeyboardInterrupt:
                break
                
        main_socket.close()
        
    def manage_user(self, user_conn, user_addr):
        verified = False
        user_id = None
        
        try:
            while True:
                incoming = user_conn.recv(1024)
                if not incoming:
                    break
                    
                try:
                    if verified:
                        decoded = self.encryptor.decrypt(incoming)
                        request = json.loads(decoded.decode('utf-8'))
                    else:
                        request = json.loads(incoming.decode('utf-8'))
                except:
                    request = json.loads(incoming.decode('utf-8'))
                    
                print(f"Processing from {user_addr}: {request}")
                
                if request['action'] == 'register':
                    result = self.create_account(request['username'], request['password'])
                    if result['status'] == 'success':
                        result['key'] = self.security_key.decode()
                        verified = True
                        user_id = request['username']
                        self.active_users[user_id] = user_conn
                        
                elif request['action'] == 'login':
                    result = self.verify_user(request['username'], request['password'])
                    if result['status'] == 'success':
                        result['key'] = self.security_key.decode()
                        verified = True
                        user_id = request['username']
                        self.active_users[user_id] = user_conn
                        
                elif request['action'] == 'send_message' and verified:
                    self.distribute_message(request['username'], request['message'])
                    result = {'status': 'success'}
                    
                else:
                    result = {'status': 'error', 'message': 'Invalid request'}
                    
                response_payload = json.dumps(result).encode('utf-8')
                if verified and request['action'] not in ['register', 'login']:
                    response_payload = self.encryptor.encrypt(response_payload)
                user_conn.send(response_payload)
                
        except Exception as e:
            print(f"User {user_addr} error: {e}")
        finally:
            if user_id and user_id in self.active_users:
                del self.active_users[user_id]
            user_conn.close()
            print(f"User {user_addr} disconnected")
            
    def create_account(self, username, password):
        db_conn = sqlite3.connect('communication.db')
        db_cursor = db_conn.cursor()
        try:
            db_cursor.execute("INSERT INTO user_accounts (username, password) VALUES (?, ?)", (username, password))
            db_conn.commit()
            return {'status': 'success', 'message': 'Account created successfully'}
        except sqlite3.IntegrityError:
            return {'status': 'error', 'message': 'User ID already taken'}
        finally:
            db_conn.close()
            
    def verify_user(self, username, password):
        db_conn = sqlite3.connect('communication.db')
        db_cursor = db_conn.cursor()
        db_cursor.execute("SELECT * FROM user_accounts WHERE username=? AND password=?", (username, password))
        account = db_cursor.fetchone()
        db_conn.close()
        
        if account:
            return {'status': 'success', 'message': 'Access granted'}
        else:
            return {'status': 'error', 'message': 'Authentication failed'}
            
    def distribute_message(self, sender, content):
        time_stamp = datetime.now().strftime("%H:%M:%S")
        
        db_conn = sqlite3.connect('communication.db')
        db_cursor = db_conn.cursor()
        db_cursor.execute("INSERT INTO chat_logs (username, message, timestamp) VALUES (?, ?, ?)",
                      (sender, content, time_stamp))
        db_conn.commit()
        db_conn.close()
        
        message_data = {
            'action': 'new_message',
            'username': sender,
            'message': content,
            'timestamp': time_stamp
        }
        
        print(f"Broadcasting message from {sender} to {len(self.active_users)} users")
        
        for user_id, connection in list(self.active_users.items()):
            try:
                encrypted_data = self.encryptor.encrypt(json.dumps(message_data).encode('utf-8'))
                connection.send(encrypted_data)
                print(f"Message sent to {user_id}")
            except Exception as e:
                print(f"Failed to send to {user_id}: {e}")
                del self.active_users[user_id]

if __name__ == "__main__":
    hub = MessageHub()
    hub.launch_hub()