#!/usr/bin/env python3

import sys
import os

def test_project():
    print("=" * 50)
    print("CHAT APPLICATION - PROJECT TEST")
    print("=" * 50)
    
    try:
        print("1. Testing imports...")
        import server
        import client_gui  
        import server_basic
        import client_basic
        print("   SUCCESS: All modules imported")
        
        print("\n2. Testing server creation...")
        from server import AdvancedMessageHub
        server_instance = AdvancedMessageHub()
        print("   SUCCESS: Advanced server created")
        
        print("\n3. Testing database setup...")
        server_instance.setup_database()
        print("   SUCCESS: Database initialized")
        
        print("\n4. Testing encryption...")
        test_data = b"Hello World"
        encrypted = server_instance.encryptor.encrypt(test_data)
        decrypted = server_instance.encryptor.decrypt(encrypted)
        assert decrypted == test_data
        print("   SUCCESS: Encryption working")
        
        print("\n5. Testing basic components...")
        from server_basic import SimpleMessageServer
        from client_basic import MessageClient
        basic_server = SimpleMessageServer()
        basic_client = MessageClient()
        print("   SUCCESS: Basic components created")
        
        print("\n" + "=" * 50)
        print("PROJECT TEST COMPLETED SUCCESSFULLY!")
        print("=" * 50)
        print("\nTo run the application:")
        print("1. python server.py          (Terminal 1)")
        print("2. python client_gui.py      (Terminal 2)")
        print("\nOr for basic version:")
        print("1. python server_basic.py    (Terminal 1)")  
        print("2. python client_basic.py    (Terminal 2)")
        
        return True
        
    except Exception as e:
        print(f"\nERROR: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_project()
    sys.exit(0 if success else 1)