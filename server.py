import socket
import threading

HOST = socket.gethostbyname(socket.gethostname())
PORT = 5500
BUFFSIZ = 1024 #bytes
SERVER_ADDRESS = (HOST, PORT)

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(SERVER_ADDRESS)

clients = []  # stores clients sockets for communication 
nicknames = []

# listen for incoming connections
server_socket.listen()
print(f'server listening on {HOST}:{PORT}')

def broadcast(message):
    for client in clients:
        client.send(message)

def handle_client(communication_socket):
    while True:
        try :
            in_msg = communication_socket.recv(BUFFSIZ)
            broadcast(in_msg)
        except:
            index = clients.index(communication_socket)
            clients.remove(communication_socket)
            communication_socket.close()
            nickname = nicknames[index]
            broadcast(f'{nickname} has left the chat'.encode('utf-8'))
            nicknames.remove(nickname)
            break
    
def receive():
    while True:
        communication_socket, client_address = server_socket.accept()
        print('Accepted connection from {}:{}'.format(*client_address))

        communication_socket.send("NICK".encode('utf-8'))
        nickname = communication_socket.recv(BUFFSIZ).decode('utf-8')
        nicknames.append(nickname)
        clients.append(communication_socket)
        print(f'{client_address} is {nickname}')
        communication_socket.send('Connected to the server'.encode('utf-8'))
        broadcast(f'{nickname} has joined the chat'.encode('utf-8'))
        
        client_thread = threading.Thread(target=handle_client, args=(communication_socket,))
        client_thread.start()

receive()