# CMD Interface - Server version
def cmd_disconnect(clients, client):
    client.close()
    clients.remove(client)
    print("Client deconnecte")

def cmd_getState(client, game):
    client.send(game.getState())

def cmd_getScore(client, game):
    client.send(game.getScore())

def cmd_place(client, game, data):
    client.send(game.place(client, data))