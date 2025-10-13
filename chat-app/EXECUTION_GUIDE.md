# Chat Application - Execution Guide

## Project Status: ✅ COMPLETE
Minimal chat application with beginner and advanced versions.

## Features
- Basic command-line chat
- Advanced GUI with authentication, rooms, file sharing, encryption

## Execute in VSCode

### Method 1: Manual Execution (Recommended)

**Basic Version:**
```bash
python server_basic.py    # Terminal 1
python client_basic.py    # Terminal 2
```

**Advanced Version:**
```bash
python server.py          # Terminal 1  
python client_gui.py      # Terminal 2
```

### Method 2: VSCode Debug Panel
Press F5 or use Run → Start Debugging

## Files
- `server_basic.py` - Basic server
- `client_basic.py` - Command-line client  
- `server.py` - Advanced server
- `client_gui.py` - GUI client
- `requirements.txt` - Dependencies

## Install
```bash
pip install -r requirements.txt
```

## Usage
**Basic:** Enter username, type messages, '/exit' to quit
**Advanced:** Register/login, select channel, send messages/files/emojis