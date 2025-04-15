import socket
import threading

SERVER_HOST = '0.0.0.0'
SERVER_PORT = 55555

srv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
srv.bind((SERVER_HOST, SERVER_PORT))
srv.listen()
print(f'Server started on {SERVER_HOST}:{SERVER_PORT}')

client_list = []
nickname_list = []

def broadcast(message):
    for client in client_list:
        client.send(message)

def handle(client):
    while True:
        try:
            message = input.recv(1024)     
            broadcast(message)          

        except:
            index = client_list.index(client)
            client_list.remove(client)
            client.close()
            nickname = nickname_list[index]
            broadcast(f'{nickname} has left the chat!'.encode('utf-8'))
            nickname_list.remove(nickname)
            break

def receive():
    while True:
        client, address = srv.accept()
        print(f'Connected on {str(address)}')

        client.send('NICK'.encode('utf-8'))
        nickname = client.recv(1024).decode('utf-8')

        nickname_list.append(nickname)
        client_list.append(client)

        print(f'The Nickname of the Client is {nickname}!')

        broadcast(f'{nickname} has joined the chat!'.encode('utf-8'))

        client.send('Connected to the server!'.encode('utf-8'))

        thread = threading.Thread(target=handle, args=(client,))
        thread.start()

receive()