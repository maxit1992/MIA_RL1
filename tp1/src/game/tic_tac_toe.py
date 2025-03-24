import random

from .board import Board
from .players import Player


class TicTacToe:
    """
    Tic Tac Toe game class.
    """

    SYMBOL_PLAYER1 = "X"
    SYMBOL_PLAYER2 = "O"
    SEED = None

    def __init__(self, player1: Player, player2: Player, board: Board = Board()):
        """
        Constructs all the necessary attributes for the Tic Tac Toe game.

        Parameters:
        -----------
        player1 : Player
            The first player.
        player2 : Player
            The second player.
        board : Board, optional
            The game board. A new default Board is created if not given.
        """
        self.board = board
        self.player1 = player1
        self.player2 = player2

    def start(self):
        """
        Starts a new game of Tic Tac Toe. Randomly selects which player starts first.
        Alternates turns between players until the board is full or a player wins.
        """
        if self.SEED:
            random.seed(self.SEED)
        print("New Game")
        player2_turn = random.randrange(0, 99, 1) >= 50
        if player2_turn:
            self.player2.start()
        else:
            self.player1.start()
        while not (self.board.is_full()):
            if player2_turn:
                pos_x, pos_y = self.player2.turn(self.board)
                self.board.place_symbol(self.SYMBOL_PLAYER2, pos_x, pos_y)
                self.board.print()
                if self.board.is_winner(self.SYMBOL_PLAYER2):
                    self.player2.win()
                    self.player1.loose()
                    return
            else:
                pos_x, pos_y = self.player1.turn(self.board)
                self.board.place_symbol(self.SYMBOL_PLAYER1, pos_x, pos_y)
                self.board.print()
                if self.board.is_winner(self.SYMBOL_PLAYER1):
                    self.player1.win()
                    self.player2.loose()
                    return
            player2_turn = not player2_turn
        self.player1.draw()
        self.player2.draw()
