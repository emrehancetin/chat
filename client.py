import socket
import threading

# input nickname
nickname = input("Choose a nickname: ")

# creating a client via using socket
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# client connection to localhost
client.connect(('127.0.0.1', 5555))


# this function receive the message from server!
def receive():
    while True:
        try:
            # The ascii() function returns a readable version of any object.
            message = client.recv(1024).decode('ascii')

            # if message == NICK then send nickname to server
            if message == 'NICK':
                client.send(nickname.encode('ascii'))
            # else just print terminal
            else:
                print(message)
        except:
            # this controls if there is error , it catch and close the client
            print("An error occurred!")
            client.close()
            break


# this method allows the application to constantly receive messages from the user.
def write():
    while True:
        message = f'{nickname}: {input("")}'
        client.send(message.encode('ascii'))


# beginning of receiving
receive_thread = threading.Thread(target=receive)
receive_thread.start()

# beginning of writing
write_thread = threading.Thread(target=write)
write_thread.start()
