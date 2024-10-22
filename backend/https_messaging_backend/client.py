import requests
import time

# Path to the self-signed certificate
CERT_PATH = 'cert.pem'  # Replace with the correct path to your cert.pem file

def send_message(sender, recipient, message):
    url = 'https://localhost:5000/send_message'
    data = {
        'sender': sender,
        'recipient': recipient,
        'message': message
    }
    try:
        response = requests.post(url, json=data, verify=False)
        print(f"Sent message from {sender} to {recipient}: {response.json()['message']}")
    except requests.exceptions.SSLError as e:
        print(f"SSL Error: {e}")
    except Exception as e:
        print(f"Error sending message: {e}")

def get_messages(recipient):
    url = f'https://localhost:5000/get_messages/{recipient}'
    try:
        response = requests.get(url, verify=False)#need to verify certificate in production
        messages = response.json()['messages']
        if messages:
            print(f"Messages for {recipient}: {messages}")
        else:
            print(f"No new messages for {recipient}.")
    except requests.exceptions.SSLError as e:
        print(f"SSL Error: {e}")
    except Exception as e:
        print(f"Error retrieving messages: {e}")

if __name__ == '__main__':
    print("Messaging Client")
    while True:
        action = input("Do you want to (s)end a message or (g)et messages? (s/g): ").strip().lower()
        if action == 's':
            sender = input("Enter your name (sender): ")
            recipient = input("Enter the recipient name: ")
            message = input("Enter the message: ")
            send_message(sender, recipient, message)
        elif action == 'g':
            recipient = input("Enter your name to retrieve your messages: ")
            get_messages(recipient)
        else:
            print("Invalid option. Please type 's' to send or 'g' to get messages.")