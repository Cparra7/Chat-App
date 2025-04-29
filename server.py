#server.py

import socket
import threading
import sys
import os
import time

MAX_CLIENTS = 10  # Maximum number of clients or terminals allowed open to join room
clients = {}  # Dictionary to store username to socket mapping
logs_dir = "logs"  # Directory to store client logs
lock = threading.Lock()  # Thread lock to handle shared data access

# Create logs directory if it doesn't exist
if not os.path.exists(logs_dir):
    os.makedirs(logs_dir)

# Log messages to the user's file  - ONLY TO SPECIFIC USER - FIXED - Now saves entire history of user
def log_message(username, message):
    with open(f"{logs_dir}/{username}.txt", "a") as f:
        f.write(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] {message}\n")

# Send a message to all registered users except the sender - Need to Fix to send messages that are longer than a word - FIXED - Tested and it works for sentecnes,etc
def broadcast(sender, message):
    for user, conn in clients.items():
        if user != sender:
            try:
                conn.sendall(f"{sender}: {message}\n".encode())
            except:
                continue

#  - used for system message
def notify_all(message):
    for conn in clients.values():
        try:
            conn.sendall(f"{message}\n".encode())
        except:
            continue

# Sends direct messagee from sender to recipient - Message is logged as well
def private_message(sender, recipient, message):
    if recipient in clients:
        try:
            clients[recipient].sendall(f"{sender}: {message}\n".encode())
            log_message(sender, f"Message sent to {recipient} - \"{message}\"")
            log_message(recipient, f"Message received from {sender} - \"{message}\"")
        except:
            pass
    else:
        clients[sender].sendall(b"Unknown Recipient\n")

#  Only sed user can see their personal text log 
def send_log(username, conn):
    log_path = f"{logs_dir}/{username}.txt"
    if os.path.exists(log_path):
        with open(log_path, "r") as f:
            conn.sendall(f.read().encode())
    else:
        conn.sendall(b"No log available.\n")

# Handle a new client connection
def handle_client(conn, addr):
    username = None
    try:
        while True:
            data = conn.recv(1024).decode().strip()
            if not data:
                break

            parts = data.split(" ", 2)
            command = parts[0]

#When a user first joins - they must enter valid username (username that is not taken)

            if command == "JOIN":
                if username:
                    conn.sendall(b"Already registered.\n")
                elif len(parts) < 2:
                    conn.sendall(b"JOIN command requires a username.\n")
                else:
                    with lock:
                        if len(clients) >= MAX_CLIENTS: #10 users max
                            conn.sendall(b"Too Many Users\n")
                            conn.close()
                            return
                        username = parts[1]
                        clients[username] = conn
                        conn.sendall(f"{username} joined!Connected to server!\n".encode())
                        log_message(username, "User joined the chat")
                        notify_all(f"{username} joined the chatroom")
            elif command == "LIST": #shows list of those in server
                if username:
                    conn.sendall(",".join(clients.keys()).encode() + b"\n")
                else:
                    conn.sendall(b"Unregistered User. Use JOIN <username>\n")
            elif command == "MESG":
                if username:
                    if len(parts) < 3:
                        conn.sendall(b"Usage: MESG <username> <message>\n")
                    else:
                        recipient, message = parts[1], parts[2]
                        private_message(username, recipient, message)
                else:
                    conn.sendall(b"Unregistered User. Use JOIN <username>\n")
            elif command == "BCST":
                if username:
                    if len(parts) < 2:
                        conn.sendall(b"Usage: BCST <message>\n")
                    else:
                        message = parts[1] if len(parts) == 2 else parts[1] + ' ' + parts[2] if len(parts) == 3 else ''
                        broadcast(username, message)
                        log_message(username, f"Broadcasted: {message}")
                else:
                    conn.sendall(b"Unregistered User. Use JOIN <username>\n")
            elif command == "QUIT": #essentially same as (ctrl + c)
                break
            elif command == "LOG":
                if username:
                    send_log(username, conn)
                else:
                    conn.sendall(b"Unregistered User. Use JOIN <username>\n")
            else:
                conn.sendall(b"Unknown Message\n")
    finally:
        conn.close()
        if username:
            with lock:
                del clients[username]
            print(f"{username} left the chat")
            notify_all(f"{username} left the chatroom")

# command Line args validation
if len(sys.argv) != 2:
    print("usage: python3 server.py <svr_port>")
    sys.exit(1)

# Set up server socket
host = ""
port = int(sys.argv[1])

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((host, port))
server_socket.listen()
print("The Chat Server Started")

# Main loop to accept client connections
while True:
    conn, addr = server_socket.accept()
    print(f"Connected with {addr}")
    threading.Thread(target=handle_client, args=(conn, addr), daemon=True).start()
