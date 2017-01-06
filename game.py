import socket
from grid import *
from cmdServ import *
from tools import *


# Game class
class game:
    # Grids
    grids = [grid(), grid(), grid()]

    # Players and spectators
    players = dict()
    spectators = []
    currentPlayer = None
    gameReady = False

    # Scores
    scores = dict()

    # Game management
    # init Game
    def __init__(self):
        self.grid = grid()
        self.players = dict()
        self.scores = dict()
        self.currentPlayer = J1
        for i in [J1, J2]:
            self.players[i] = None
            self.scores[i] = None

    # addPlayer method : adds a player to the game
    def addPlayer(self, client):
        # Assigning to player 1 if available
        if self.players[J1] is None:
            self.players[J1] = client
            self.scores[J1] = 0
        # Assigning to player 2 if available
        elif self.players[J2] is None:
            self.players[J2] = client
            self.scores[J2] = 0
        # Assigning to spectators otherwise
        else:
            self.spectators.append(client)
        # No player spots available
        if not self.gameReady and self.players[J1] is not None and self.players[J2] is not None:
            self.gameReady = True

    # removeClient : removes a client (player or spectator) from the game
    def removeClient(self, client):
        # Checking in players
        for player in [J1, J2]:
            if self.players[player] == client:
                self.players[player] = None
        # Checking in spectators
        for spectator in self.spectators:
            if spectator == client:
                self.spectators.remove(client)

    # Players actions and getters
    # place method : places a token on a cell
    def place(self, player, cell):
        cell = int(cell)
        # Checking if the player is the current one
        if self.players[self.currentPlayer] == player:
            # Checking if cell is empty
            if self.grid.isEmpty(cell):
                # Updating player grid
                self.grids[self.currentPlayer].cells[cell] = self.currentPlayer
                # Updating public grid
                self.grids[0].play(self.currentPlayer, cell)
                # Sending new grid state
                cmd_sendstate(self.players[self.currentPlayer], self)
                # Changing turn
                self.currentPlayer = self.currentPlayer % 2 + 1
            # Cell not empty
            else:
                # Updating player grid
                self.grids[self.currentPlayer].cells[cell] = self.grids[0].cells[cell]
                # Sending new grid state
                cmd_sendstate(self.players[self.currentPlayer], self)
            # Telling the current player he has to play
            cmd_yourturn(self.players[self.currentPlayer])
        # Wrong player
        else:
            sendError(player, "Ce n'est pas votre tour.\n")

    # startGame method :
    def startGame(self):
        print("---- GAME STARTING ----")
        self.sendPlayers("START\n")

    # endGame method :
    def endGame(self):
        print("---- GAME ENDING ----")
        winner = self.grid.gameOver()
        if winner > 0:
            # Incrementing score and sending them with end token
            self.scores[winner] += 1
            self.sendAll("END " + winner + "\n")
            self.sendAll(self.getScore())
            return True
        else:
            return False

    # isPlayer method : checks if the specified client is a player
    def isPlayer(self, client):
        # Player 1
        if self.players[J1] == client:
            return J1
        # Player 2
        elif self.players[J2] == client:
            return J2
        # Spectator
        else:
            return 0

    # sendAll method : sends msg to all clients (players and spectators)
    def sendAll(self, msg):
        self.sendPlayers(msg)
        self.sendSpectators(msg)

    # sendPlayers method : sends msg to players
    def sendPlayers(self, msg):
        for player in [J1, J2]:
            self.players[player].send(msg)

    # sendSpectators method : sends msg to spectators
    def sendSpectators(self, msg):
        for spectator in self.spectators:
            spectator.send(msg)

    # sendScores method : sends scores to everyone
    def sendScores(self):
        self.sendPlayers(self.getScore())
        self.sendSpectators(self.getScore())

    # getScore method : returns scores as a string
    def getScore(self):
        return self.scores[J1] + " " + self.scores[J2]

    # getState method : returns grid state as a string
    def getState(self, client):
        # State J1 grid
        if self.isPlayer(client) == J1:
            return self.grids[J1].toString()
        # State J2 grid
        elif self.isPlayer(client) == J2:
            return self.grids[J2].toString()
        # State public grid
        else:
            return self.grids[0].toString()
