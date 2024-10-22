import socket
import threading

# Server configuration
SERVER_IP = 'localhost'  # Replace with the public IP if running on another machine
PORT = 5000

# Function to receive messages from the server
def receive_messages(client_socket):
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            if not message:
                break
            print(message)
        except:
            print("[ERROR] Connection lost.")
            break

def start_client():
    # Create a TCP socket for the client
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((SERVER_IP, PORT))

    # Receive the prompt to enter username
    username_prompt = client_socket.recv(1024).decode('utf-8')
    print(username_prompt)
    username = input("Username: ")
    client_socket.send(username.encode('utf-8'))

    print(f"[CONNECTED] Connected to the server as {username}.")

    # Start a thread to receive messages from the server
    receive_thread = threading.Thread(target=receive_messages, args=(client_socket,))
    receive_thread.start()

    while True:
        # Send messages to the server
        message = input(f"{username}: ")
        if message.lower() == "exit":
            break
        client_socket.send(message.encode('utf-8'))

    client_socket.close()
    print("[DISCONNECTED] Disconnected from the server.")

if __name__ == "__main__":
    start_client()