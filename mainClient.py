#!/usr/bin/python3

from cmdClient import *
from grid import *
from tools import *
import select
import socket
import sys


def prompt():
    sys.stdout.write('<You> ')
    sys.stdout.flush()


# Main client
# TODO : modifier un peu, code choppe sur http://www.binarytides.com/code-chat-application-server-client-sockets-python/
# TODO 2 : Mettre dans un fichier a part - mainClient.py ? - et implementer les fonctions de traitement de retours de
# commandes appellees dans cmdClient.py
def main():
    if len(sys.argv) < 2:
        print('Usage : python3 mainClient.py hostname')
        sys.exit()

    host = '' #sys.argv[1]
    port = 7777
    s = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)

    # connect to remote host
    connect_to_server(s, host, port)
    prompt()

    while 1:
        socket_list = [sys.stdin, s]
        # Get the list sockets which are readable
        read_sockets, write_sockets, error_sockets = select.select(socket_list, [], [])

        for sock in read_sockets:
            # incoming message from remote server
            if sock == s:
                data = sock.recv(4096)
                if not data:
                    print('\nDisconnected from chat server')
                    sys.exit()
                else:
                    print(repr(data))
                    #if data

            # user entered a message
            else:
                msg = sys.stdin.readline()
                s.send(msg.encode())
                prompt()
    pass

main()