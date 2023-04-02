import socket, threading

# HOST = socket.gethostbyname(socket.gethostname())
HOST = 'localhost'
PORT = 9090

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # INET means internet socket and sock stream means tcp socket
server_socket.bind((HOST, PORT))  #(HOST, PORT) in tuple form

server_socket.listen()
print(f'Listening on {HOST} : {PORT}')

clients = []  # stores all the client sockets for communication
nicknames = [] # stores nicknames of all the clients

def broadcast(message):
    for client in clients:
        client.send(message.encode('utf-8'))

def handle_client(client_socket):
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            broadcast(message)
        except:
            index = clients.index(client_socket)
            clients.remove(client_socket)
            broadcast(f'{nicknames[index]}' + ' ' + 'has left the chat\n')   # HAS LEFT THE CHAT
            print(nicknames[index] + 'has left the chat')
            # clients.remove(client_socket)
            nicknames.remove(nicknames[index])
            client_socket.close()
            # broadcast(f'{nicknames[index]} has left the chat')   # HAS LEFT THE CHAT
            # print(nicknames[index] + 'has left the chat')
            break   

def receive():
    while True:
        client_socket, client_address = server_socket.accept()  # client_address will contain a tuple consist of (HOST, PORT)
        print(f'{(client_address)} connected to the server')
        client_socket.send("NICK".encode('utf-8'))
        nickname = client_socket.recv(1024).decode('utf-8')
        nicknames.append(nickname)
        clients.append(client_socket)
        print(f'nickname of the {client_address} is "{nickname}"')

        broadcast(f'{nickname} has joined the chat\n')
        client_socket.send("You are connected to the server\n".encode('utf-8'))

        thread = threading.Thread(target=handle_client, args=(client_socket,)) # tuple needs to be passed in args
        thread.start()
        
receive()