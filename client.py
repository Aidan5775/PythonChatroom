# client.py

import socket
import threading

# Ask the user for a nickname they want to be displayed for them
nickname = input("Enter a nickname to be displayed: ")

# Create a socket and connect to the server
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('127.0.0.1', 55555))  # IP must match the server's host and port

# receive function will handle incoming messages 
def receive():
    while True:
        try:
            message = client.receive(1024).decode('utf-8')
            # If the server requests a nickname, send it
            if message == 'NICK':
                client.send(nickname.encode('utf-8'))
            else:
                # Print all other messages from the server
                print(message)
        except:
            # In case of an error, like a shutdown, leave the server
            print("An error has occurred! Disconnecting you from the server.")
            client.close()
            break

# write function will handle sending messages
def write():
    while True:
        # Read an input from the user and send it
        message = f'{nickname}: {input("")}'
        client.send(message.encode('utf-8'))

# Start receiving and writing messages in separate threads so they can run simultaneously
receive_thread = threading.Thread(target=receive)
receive_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start()