# CMD Interface - Client version

#Connection au serveur
def connect_to_server(socket, host, port):
    try:
        socket.connect((host, port))
    except:
        print('Unable to connect')
        sys.exit()
    print('Connected to remote host. Start sending messages')

# Gestion des retours de commandes
def cmd_getstate(grid=None):
    # TODO : traitement retour de getState -> mise a jour de la grille locale
    #client.send(b"GETSTATE")
    print("cmd_getstate")

def cmd_getscore(score):
    # TODO : traitement retour de getScore
    client.send(b"GETSCORE")

def cmd_play():
    print("play")