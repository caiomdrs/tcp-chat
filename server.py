import socket
import threading

host = '127.0.0.1'

port = 55555

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()

clients = []

nicknames = []

def broadcast(message):
    for client in clients:
        client.send(message)

def handle(client):
    while True:
        try:
            message = client.recv(1024)
            broadcast(message)
        except:
            index = clients.index(client)
            clients.remove()
            client.close()
            nickname = nicknames[index]
            broadcast(f"{nickname} left the Channel".encode('ascii'))
            nicknames.remove(nickname)
            break

def receive():
    while True:
        client, address = server.accept()
        print(f"Connected with {str(address)}")

        client.send('NICK'.encode('ascii'))
        nickname = client.recv(1024).decode('ascii')
        nicknames.append(nickname)
        clients.append(client)

        print(F"Connected as {nickname}!")
        broadcast(f"{nickname} joined the chat".encode('ascii'))
        client.send('Connected to the server'.encode('ascii'))

        thread = threading.Thread(target=handle, args=(clients,))
        thread.start()

print("Server is listening...")
receive()
