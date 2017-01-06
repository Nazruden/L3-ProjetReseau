#!/usr/bin/python3

from cmdServ import *
from game import *
from tools import *
import random
import select
import socket
import sys

# Main de base donne pour le morpion
# def main():
#     grids = [grid(), grid(), grid()]
#     current_player = J1
#     grids[J1].display()
#     while grids[0].gameOver() == -1:
#         if current_player == J1:
#             shot = -1
#             while shot <0 or shot >=NB_CELLS:
#                 shot = int(input ("quel case allez-vous jouer ?"))
#         else:
#             shot = random.randint(0,8)
#             while grids[current_player].cells[shot] != EMPTY:
#                 shot = random.randint(0,8)
#         if (grids[0].cells[shot] != EMPTY):
#             grids[current_player].cells[shot] = grids[0].cells[shot]
#         else:
#             grids[current_player].cells[shot] = current_player
#             grids[0].play(current_player, shot)
#             current_player = current_player%2+1
#         if current_player == J1:
#             grids[J1].display()
#     print("game over")
#     grids[0].display()
#     if grids[0].gameOver() == J1:
#         print("You win !")
#     else:
#         print("you loose !")
#
# main()
#

# Main serveur
def main():
    ## Vars
    # Communication
    clients = list()
    # Game
    gameInstance = game()

    # grids = [grid(), grid(), grid()]
    # current_player = J1
    # grids[J1].display()

    # creation du socket d'ecoute
    ear = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
    ear.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    ear.bind(('', 7777))
    ear.listen(1)
    print("Serveur lance")
    # Boucle d'attente de connexion
    print("Attente de connexion...")
    while True:
        tmp = list(clients)
        tmp.append(ear)
        changes = select.select(tmp, list(), list())[0]
        for client in changes:
            # Traitement du socket d'ecoute
            if client == ear:
                data = client.accept()
                print("Nouvelle connexion de " + str(data[1]))
                clients.append(data[0])

            # Sinon reception des donnees
            else:

                data = client.recv(1500)

                # Traitement deconnexion
                if len(data) == 0:  # Si la longueur recue est 0 c'est que l'user s'est deconnecte
                    cmd_disconnect(clients, client)

                # Analyse du paquet
                # CMD : PLACE
                if data.startswith("PLACE "):
                    cmd_place(formalizedata(data, "PLACE "))
                # CMD : GETSTATE
                elif data.startswith("GETSTATE"):
                    cmd_getstate(formalizedata(data, "GETSTATE"))
                # CMD : GETSCORE
                elif data.startswith("GETSCORE"):
                    cmd_getscore(formalizedata(data, "GETSCORE"))
                # CMD : DISCONNECT
                elif data.startswith("DISCONNECT"):
                    cmd_disconnect(clients, client)


    pass

main()
