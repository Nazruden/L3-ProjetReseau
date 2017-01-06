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
    if len(sys.argv) < 3:
        print 'Usage : python telnet.py hostname port'
        sys.exit()

    host = sys.argv[1]
    port = int(sys.argv[2])

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(2)

    # connect to remote host
    try:
        s.connect((host, port))
    except:
        print 'Unable to connect'
        sys.exit()

    print 'Connected to remote host. Start sending messages'
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
                    print '\nDisconnected from chat server'
                    sys.exit()
                else:
                    # print data
                    sys.stdout.write(data)
                    prompt()

            # user entered a message
            else:
                msg = sys.stdin.readline()
                s.send(msg)
                prompt()
    pass

main()