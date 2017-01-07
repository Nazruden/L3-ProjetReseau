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

def main():
    if len(sys.argv) < 2:
        print('Usage : python3 mainClient.py hostname')
        sys.exit()

    host = sys.argv[1]
    port = 7777
    s = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)

    # connect to remote host
    connect_to_server(s, host, port)

    while 1:
        socket_list = [sys.stdin, s]
        # Get the list sockets which are readable
        read_sockets, write_sockets, error_sockets = select.select(socket_list, [], [])

        for sock in read_sockets:
            # incoming message from remote server
            if sock == s:
                data = sock.recv(1500)
                if not data:
                    print('\nDisconnected from chat server')
                    sys.exit()
                else:
                    # Analyse paquets serveur
                    cmds = split_data(data)
                    for cmd in cmds:
                        print(cmd)
                        #START
                        if cmd.startswith(b"START"):
                            data = formalizedata(data, "START")
                            print("GAME START")

                        #GETSATE
                        if cmd.startswith(b"STATE"):
                            cmd_getstate(cmd_convert_data_to_grid(cmd))

                        #YOURTURN
                        if cmd.startswith(b"YOURTURN"):
                            print("YOUR TURN")
                            place = cmd_play()
                            s.send(place.encode())
            elif sock == sys.stdin:
                s.send(sys.stdin.read(1500))
                        
            # user entered a message
            #else:
             #   msg = sys.stdin.readline()
              #  s.send(msg.encode())
    pass

main()