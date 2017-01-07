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
            self.startGame()


    def playerToSpectator(self, player):
        self.spectators.append(self.players[player])
        self.players[player] = None

    def spectatorToPlayer(self, spectator):
        self.spectators.remove(spectator)
        self.addPlayer(spectator)

    # removeClient : removes a client (player or spectator) from the game
    def removeClient(self, client):
        # Checking in players
        for player in [J1, J2]:
            if self.players[player] == client:
                self.players[player] = None
                # If game was running
                if self.gameReady:
                    self.gameReady = False
                    print("PAUSE - A PLAYER HAS LEFT")
                    self.sendAll("PAUSE - A PLAYER HAS LEFT\n")
        # Checking in spectators
        for spectator in self.spectators:
            if spectator == client:
                self.spectators.remove(client)

    # Players actions and getters
    # place method : places a token on a cell
    def place(self, player, cell):
        if cell is not "":
            cell = int(cell)
        if cell < 9 and cell >= 0:
            # Checking if the player is the current one
            if self.players[self.currentPlayer] == player:
                # Checking if cell is empty
                if self.grids[0].isEmpty(cell):
                    # Updating player grid
                    self.grids[self.currentPlayer].cells[cell] = self.currentPlayer
                    # Updating public grid
                    self.grids[0].play(self.currentPlayer, cell)
                    # Sending new grid state to current player and to spectators
                    self.players[self.currentPlayer].send(self.getState(self.players[self.currentPlayer]))
                    self.sendSpectators(self.getState(None))
                    # Checking end of game
                    if self.grids[0].gameOver() > 0:
                        self.endGame()
                    # Or going to next turn
                    else:
                        self.currentPlayer = self.currentPlayer % 2 + 1
                # Cell not empty
                else:
                    # Updating player grid
                    self.grids[self.currentPlayer].cells[cell] = self.grids[0].cells[cell]
                    # Sending new grid state to current player
                    self.players[self.currentPlayer].send(self.getState(self.players[self.currentPlayer]))
                # Telling the current player he has to play if game didn't end
                if self.gameReady:
                    self.sendTurn(self.players[self.currentPlayer])
            # Wrong player
            else:
                sendError(player, "Ce n'est pas votre tour.\n")
        # Illegal cell
        else:
            sendError(player, "Ceci n'est pas une case valide\n")
            self.sendTurn(self.players[self.currentPlayer])

    # startGame method :
    def startGame(self):
        # Print game beginning and sends START and TURN tokens
        print("---- GAME STARTING ----")
        self.sendPlayers("START\n")
        self.sendTurn(self.players[self.currentPlayer])

    # endGame method :
    def endGame(self):
        print("---- GAME ENDING ----")
        winner = self.grids[0].gameOver()
        if winner > 0:
            self.gameReady = False
            self.grids = [grid(), grid(), grid()]
            # Incrementing score and sending them with end token
            self.scores[winner] += 1
            self.sendAll("END " + str(winner) + "\n")
            self.sendAll(self.getScore())
            self.playerToSpectator(J1)
            self.playerToSpectator(J2)
            self.sendAll("---------------------\n"
                         "TYPE \"JOIN\" TO PLAY\n"
                         "---------------------\n")
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
            if self.players[player] is not None:
                self.players[player].send(msg)

    # sendSpectators method : sends msg to spectators
    def sendSpectators(self, msg):
        for spectator in self.spectators:
            spectator.send(msg)

    # sendScores method : sends scores to everyone
    def sendScores(self):
        self.sendPlayers(self.getScore())
        self.sendSpectators(self.getScore())

    # sendState method : sends appropriate state to specified client
    def sendState(self, client):
        client.send(self.getState())

    # sendTurn method : sends turn token to specified player
    def sendTurn(self, player):
        player.send("YOURTURN\n")

    # getScore method : returns scores as a string
    def getScore(self):
        prefix = "SCORE "
        return prefix + str(self.scores[J1]) + " " + str(self.scores[J2]) + "\n"

    # getState method : returns grid state as a string
    def getState(self, client):
        prefix = "STATE "
        # State J1 grid
        if self.isPlayer(client) == J1:
            return prefix + self.grids[J1].toString() + "\n"
        # State J2 grid
        elif self.isPlayer(client) == J2:
            return prefix + self.grids[J2].toString() + "\n"
        # State public grid
        else:
            return prefix + self.grids[0].toString() + "\n"

    # joinGame method : manage spectators joining when they ask

    def joinGame(self, client):
        self.spectatorToPlayer(client)
