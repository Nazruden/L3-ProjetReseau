from game import *

# CMD Interface - Server version
def cmd_disconnect(clients, client):
    client.close()
    clients.remove(client)
    print("Client deconnecte")


def cmd_getstate(client, game):
    client.send(game.getState())


def cmd_getscore(client, game):
    client.send(game.getScore())


def cmd_place(client, game, data):
    client.send(game.place(client, data))


def cmd_start(players):
    for player in players:
        player.send("START\n")


# CMD End : send END to players with state, an in for :
#               - 1 : player 1 victory
#               - 2 : player 2 victory
def cmd_end(players, state):
    for player in players:
        player.send("END " + state)
