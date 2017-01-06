from tools import * 
# CMD Interface - Client version

def cmd_convert_data_to_grid(data):
    data = formalizedata(data ,"STATE ")
    cells = data.split(" ")
    grid = grid()
    grid.cells = cells
    return grid

#Connection au serveur
def connect_to_server(socket, host, port):
    try:
        socket.connect((host, port))
    except:
        print('Unable to connect')
        sys.exit()
    print('Connected to remote host. Start sending messages')

# Gestion des retours de commandes
def cmd_getstate(grid):
    # TODO : traitement retour de getState -> mise a jour de la grille locale
    print("cmd_getstate")
    grid.display()

def cmd_getscore(score):
    print("SCORE : " + score)

def cmd_play():
    place = -1
    while place > 8 or place < 0:
        place = input("Veuillez choisir une case a jouer comprise entre 0 et 8")
    return "PLACE " + place

    