#!/usr/bin/python3

from cmdClient import *
from grid import *
from tools import *
import select
import socket
import sys


def prompt():
    sys.stdout.flush()

def main():
    if len(sys.argv) < 2:
        print('Usage : python3 mainClient.py hostname')
        sys.exit()

    host = sys.argv[1]
    port = 7777
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Connect to remote host
    connect_to_server(s, host, port)

    while True:
        socket_list = [sys.stdin, s]
        # Get the list sockets which are readable
        read_sockets, write_sockets, error_sockets = select.select(socket_list, [], [])

        for sock in read_sockets:
            # incoming message from remote server
            if sock == s:
                data = sock.recv(1500)
                if not data:
                    print('\nDisconnected from server')
                    sys.exit()
                else:

                    # Analyse paquets serveur
                    cmds = split_data(data)
                    for cmd in cmds:
                        print(cmd)
                        # START
                        if cmd.startswith(b"START"):
                            cmdData = formalizedata(cmd, "START ")
                            print("GAME STARTS - You're player " + cmdData)

                        # STATE
                        if cmd.startswith(b"STATE"):
                            cmd_getstate(cmd_convert_data_to_grid(cmd))

                        # YOURTURN
                        if cmd.startswith(b"YOURTURN"):
                            print("IT IS YOUR TURN TO PLAY")
                            place = cmd_play()
                            s.send(place.encode())

                        # SCORE
                        if cmd.startswith(b"SCORE"):
                            cmdData = formalizedata(cmd, "SCORE ")
                            cmdData = cmdData.split(' ')
                            print("SCORE IS : PLAYER 1 - " + cmdData[0] + " | PLAYER 2 - " + cmdData[1])

                        # END
                        if cmd.startswith(b"END"):
                            cmdData = formalizedata(cmd, "END ")
                            print("GAME HAD ENDED - PLAYER " + cmdData + " WINS !")
            else:
                msg = sys.stdin.readline()
                s.send(msg)
    pass

main()
