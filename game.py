import socket
from grid import *

class game:
    # Grid
    grid = grid()
    # Players - tab of sockets
    players = []
    currentPlayer = None
    # Scores
    scores = []

    # init Game
    def __init__(self):
        self.grid = grid()
        self.players = []
        self.scores = []
        self.currentPlayer = J1
        for i in [J1, J2]:
            self.players[i] = None
            self.scores[i] = None

    # addPlayer method : adds a player to the game
    def addPlayer(self, client):
        # Assigning to player 1 if available
        if self.players[J1] is None:
            self.players[J1] = client
        # Assigning to player 2 if available
        elif self.players[J2] is None:
            self.players[J2] = client

    # Players actions and getters

    # place method : places a token on a cell
    def place(self, player, cell):
        # Checking if the player is the current one
        if self.players[self.currentPlayer] == player:
            # Checking if cell is empty
            if self.grid.isEmpty(cell):
                self.grid.play(self.currentPlayer, cell)
                # Changing turn
                if self.currentPlayer == J1:
                    self.currentPlayer = J2
                else:
                    self.currentPlayer = J1
            # Cell not empty
            else:
                return "Cette case n'est pas vide.\n"
        # Wrong player
        else:
            return "Ce n'est pas votre tour.\n"

    # getScore method : returns scores as a string
    def getScore(self):
        return self.scores[J1] + " " + self.scores[J2]

    # getState method : returns grid state as a string
    # TODO : Peut etre changer pour getGridState et différencier de getState ? a voir
    def getState(self):
        return self.grid.toString()



