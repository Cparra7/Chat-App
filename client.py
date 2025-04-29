#client.py 

#imports
import socket
import sys
import threading

# thread to listen for incoming messages from server
def receive_messages(sock):
    while True:
        try:
            message = sock.recv(1024).decode()
            if not message:
                break
            print(message, end='')
        except:
            break

# command line arguments
if len(sys.argv) != 3:
    print("Usage: python3 client.py <hostname> <port>")
    sys.exit(1)

host = sys.argv[1]
port = int(sys.argv[2])

# Connects to server
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((host, port))

# Start the receive thread to print incoming messages
threading.Thread(target=receive_messages, args=(sock,), daemon=True).start()

# Main loop to send user input to the server
while True:
    try:
        msg = input()
        sock.sendall((msg + "\n").encode())
        if msg.startswith("QUIT"):
            break
    except:
        break

# Close the socket connection
sock.close()
