import threading
import socket

host = '127.0.0.1'  # locahost
port = 5555

# creating a server via using socket
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# server combines with host and port
server.bind((host, port))
server.listen()

# clients and nicknames list
clients = []
nicknames = []


# distributes the message to all clients
def broadcast(message):
    for client in clients:
        client.send(message)


# this receives messages and call broadcast func
def handle(client):
    while True:
        try:
            message = client.recv(1024)
            broadcast(message)
        except:
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknames[index]
            broadcast(f'{nickname} left the chat!'.encode('ascii'))
            nicknames.remove(nickname)
            break


# this handles all connectivity between each client
def receive():
    while True:
        client, adress = server.accept()
        print(f"Connected with {str(adress)}")

        client.send('NICK'.encode('ascii'))
        nickname = client.recv(1024).decode('ascii')
        nicknames.append(nickname)
        clients.append(client)

        print(f'Nickname of the client is {nickname}!')
        broadcast(f'{nickname} joined the chat!'.encode('ascii'))
        client.send('Connected to the server!'.encode('ascii'))

        thread = threading.Thread(target=handle, args=(client,))
        thread.start()


# the main part !!!
# starts the server
print("Server is listening...")
receive()
