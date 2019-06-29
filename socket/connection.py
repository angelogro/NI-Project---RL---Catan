import socket

HOST =  "localhost"
PORT = 8880

# create TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

sock.connect((HOST,PORT))
sock.send('hello '.encode())
while True:
    print(sock.recv(2000))

