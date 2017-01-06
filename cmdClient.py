# CMD Interface - Client version
# Gestion des retours de commandes
def cmd_getstate(grid):
    # TODO : traitement retour de getState -> mise a jour de la grille locale
    client.send(b"GETSTATE")

def cmd_getscore(score):
    # TODO : traitement retour de getScore
    client.send(b"GETSCORE")