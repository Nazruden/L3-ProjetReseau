#!/usr/bin/python3

from cmdServ import *
from game import *
from tools import *
import random
import select
import socket
import sys


# Main serveur
def main():
    ## Vars
    # Communication
    clients = list()
    spectators = list()
    # Game
    gameInstance = game()

    # creation du socket d'ecoute
    ear = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    ear.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    ear.bind(('', 7777))
    ear.listen(3)
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
                # Ajout du client
                clients.append(data[0])
                # Ajout du client a la partie
                gameInstance.addPlayer(data[0])

            # Sinon reception des donnees
            else:

                data = client.recv(1500)

                # Traitement deconnexion
                if len(data) == 0:  # Si la longueur recue est 0 c'est que l'user s'est deconnecte
                    cmd_disconnect(gameInstance, clients, client)

                # Analyse du paquet
                # CMD : PLACE
                if data.startswith(b"PLACE "):
                    if gameInstance.gameReady:
                        gameInstance.place(client, formalizedata(data, "PLACE "))
                    else:
                        sendError(client, "Game hasn't started yet.\n")

                # CMD : JOIN
                elif data.startswith(b"JOIN"):
                    if not gameInstance.gameReady:
                        gameInstance.joinGame(client)

                # CMD : DISCONNECT
                elif data.startswith(b"DISCONNECT"):
                    cmd_disconnect(gameInstance, clients, client)


    pass

main()
