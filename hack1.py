import socket
import argparse
from itertools import product
from string import ascii_lowercase, digits


def main():
    with socket.socket() as client_sock:
        address = (args.ip_address, args.port)

        client_sock.connect(address)

        characters = "".join(ascii_lowercase + digits)

        length = 1
        while True:
            password_set = product(characters, repeat=length)
            send_receive(client_sock, password_set)
            length += 1


def send_receive(client, password_set):
    for password in password_set:
        client.send("".join(password).encode())

        response = client.recv(1024)

        response = response.decode()

        if response == "Connection success!":
            print("".join(password))
            exit(0)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('ip_address', type=str, help='IP address')
    parser.add_argument('port', type=int, help='port number')
    args = parser.parse_args()

    main()
