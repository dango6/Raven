import socket
import threading

# Server configuration
HOST = '0.0.0.0'  # Listen on all available interfaces
PORT = 5000       # Port to bind the server

# Store connected clients and their usernames
clients = {}
usernames = {}

# Function to handle incoming client connections
def handle_client(client_socket, client_address):
    print(f"[NEW CONNECTION] {client_address} connected.")

    # Request a username from the client
    client_socket.send("Enter your username: ".encode('utf-8'))
    username = client_socket.recv(1024).decode('utf-8')

    # Store the client's username
    clients[client_socket] = username
    usernames[username] = client_socket

    print(f"[USERNAME] {username} has joined.")

    # Notify all clients that a new user has joined
    broadcast(f"{username} has joined the chat.", client_socket)

    # Communication loop
    while True:
        try:
            # Receive message from client
            message = client_socket.recv(1024).decode('utf-8')
            if not message:
                break

            # Check if the message is a private message
            if message.startswith("/msg"):
                parts = message.split(" ", 2)
                if len(parts) == 3:
                    recipient_username = parts[1]
                    private_message = parts[2]

                    # Send the private message to the specified recipient
                    if recipient_username in usernames:
                        recipient_socket = usernames[recipient_username]
                        recipient_socket.send(f"[PRIVATE] {username}: {private_message}".encode('utf-8'))
                    else:
                        client_socket.send(f"[ERROR] User {recipient_username} not found.".encode('utf-8'))
                else:
                    client_socket.send("[ERROR] Invalid format. Use /msg <username> <message>".encode('utf-8'))
            else:
                # Broadcast the message to all other clients
                broadcast(f"{username}: {message}", client_socket)

        except ConnectionResetError:
            break

    # Remove client from list and notify others of disconnection
    client_socket.close()
    del clients[client_socket]
    del usernames[username]
    broadcast(f"{username} has left the chat.", client_socket)
    print(f"[DISCONNECTED] {client_address} disconnected.")

# Function to broadcast messages to all connected clients
def broadcast(message, sender_socket):
    for client in clients:
        if client != sender_socket:
            try:
                client.send(message.encode('utf-8'))
            except:
                client.close()
                del clients[client]

def start_server():
    # Create a TCP socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))
    server_socket.listen()
    print(f"[LISTENING] Server is listening on {HOST}:{PORT}")

    while True:
        # Accept new client connections
        client_socket, client_address = server_socket.accept()

        # Start a new thread for each connected client
        client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
        client_thread.start()

        print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")

if __name__ == "__main__":
    print("[STARTING] Server is starting...")
    start_server()