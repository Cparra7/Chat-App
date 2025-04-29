# Chat-App
A Python-based client-server chat application built using Linux stream sockets. This project features a simple text-based messaging service that allows multiple clients to connect to a central server and communicate in real-time, demonstrating core socket programming techniques and real-time data exchange over TCP.


#Features
Register up to 10 clients simultaneously

Real-time private (MESG) and broadcast (BCST) messaging

View active users with the LIST command

Session logs with timestamped chat history (LOG)

Graceful disconnects using the QUIT command

Built-in command validation and structured server responses


#Supported Commands
JOIN <username>	Register the client using a unique alphanumeric username
LIST	Get a list of all currently connected (registered) clients
MESG <username> <message>	Send a private message to a specific registered user
BCST <message>	Broadcast a message to all registered users (excluding self)
LOG	Retrieve the chat log for the current user session
QUIT	Exit the chat and unregister the user


#Server Setup
Open a terminal and navigate to your project folder

Run the server with a valid port number:
EX: "python3 server.py <port>"

#Client Setup
Open another terminal (can be on same or different machine)

Run the client and pass the server hostname and port:
EX: python3 client.py <hostname> <port>

Upon connection, immediately enter:
JOIN <username>
