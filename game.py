import socket
from grid import *
from tools import *

class game:
    # Grids
    grids = [grid(), grid(), grid()]
    # Players - tab of sockets
    players = []
    currentPlayer = None
    gameReady = False
    # Scores
    scores = []

    # Game management
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
        if self.players[J1] is not None and self.players[J2] is not None:
            self.gameReady = True

    # Players actions and getters
    # place method : places a token on a cell
    def place(self, player, cell):
        # Checking if the player is the current one
        if self.players[self.currentPlayer] == player:
            # Checking if cell is empty
            if self.grid.isEmpty(cell):
                self.grids[self.currentPlayer].cells[cell] = self.currentPlayer
                self.grids[0].play(self.currentPlayer, cell)
                # Changing turn
                self.currentPlayer = self.currentPlayer % 2 + 1
            # Cell not empty
            else:
                self.grids[self.currentPlayer].cells[cell] = self.grids[0].cells[cell]
        # Wrong player
        else:
            sendError(player, "Ce n'est pas votre tour.\n")

    # startGame method :
    def startGame(self):
        sendAll(self.players, "START\n")

    # endGame method :
    def endGame(self):
        winner = self.grid.gameOver()
        if winner > 0:
            sendAll(self.players, "END " + winner + "\n")
            return True
        else:
            return False

    def isPlayer(self, client):
        if self.players[J1] == client or self.players[J2] == client:
            return True
        else:
            return False

    # getScore method : returns scores as a string
    def getScore(self):
        return self.scores[J1] + " " + self.scores[J2]

    # getState method : returns grid state as a string
    def getState(self):
        return self.grid.toString()




