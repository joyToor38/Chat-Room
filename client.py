import socket
import threading

HOST = '192.168.1.103'
PORT = 5500
nickname = input("\n\nEnter your name : ")

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST,PORT))

def write():
    while True:
        message = f'{nickname} : {input("")}'
        client.send(message.encode('utf-8'))
        

def receive():
    while True:
        try:
            message = client.recv(1024).decode('utf-8')
            if message == 'NICK':
                client.send(nickname.encode('utf-8'))
            else:
                print(message)
        except:
            client.close()
            break

receive_thread = threading.Thread(target=receive)
receive_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start()