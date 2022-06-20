import socket
from sys import argv

with socket.socket() as socket:
    address = argv[1]
    port = int(argv[2])
    message = argv[3].encode()

    sock = (address, port)

    socket.connect(sock)

    socket.send(message)
    recieve = socket.recv(1024).decode()
    print(recieve)