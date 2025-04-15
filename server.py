import socket
import threading

SERVER_HOST = '0.0.0.0'
SERVER_PORT = 55555

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((SERVER_HOST, SERVER_PORT))
server.listen()
print(f'Server started on {SERVER_HOST}:{SERVER_PORT}')

client_list = []
nickname_list = []

def broadcast(message):
    for client in client_list:
        client.send(message)

def handle(csclient):
    while True:
        try:
            message = input.receive(1024)     
            broadcast(message)          

        except:
            index = client_list.index(csclient)
            client_list.remove(csclient)
            csclient.close()
            nickname = nickname_list[index]
            broadcast(f'{nickname} has left the chat!'.encode('utf-8'))
            nickname_list.remove(nickname)
            break

def receive():
    while True:
        crclient, address = server.accept()
        print(f'Connected with {str(address)}')

        crclient.send('NICK'.encode('utf-8'))
        nickname = crclient.receive(1024).decode('utf-8')
        nickname_list.append(nickname)
        client_list.append(crclient)

        print(f'The Nickname of the Client is {nickname}!')

        broadcast(f'{nickname} has joined the chat!'.encode('utf-8'))

        crclient.send('Connected to the server!'.encode('utf-8'))

        thread = threading.Thread(target=handle, args=(crclient,))
        thread.start()

receive()