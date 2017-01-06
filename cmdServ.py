from game import *
# CMD Interface - Server version
def cmd_disconnect(game, clients, client):
    # Closing connection and removing client from original clients list and game
    client.close()
    clients.remove(client)
    game.removeClient(client)
    print("Client deconnecte")


def cmd_sendstate(client, gameInstance):
    client.send(gameInstance.getState())


def cmd_sendscore(client, gameInstance):
    client.send(gameInstance.getScore())


def cmd_place(client, gameInstance, data):
    client.send(gameInstance.place(client, data))


def cmd_start(players):
    for player in players:
        player.send("START\n")

# CMD Yourturn : inform a player he has to play
def cmd_yourturn(player):
    player.send("YOURTURN")

# CMD End : send END to players with endstate, an int for :
#               - 1 : player 1 victory
#               - 2 : player 2 victory
def cmd_end(players, endstate):
    for player in players:
        player.send("END " + endstate)
