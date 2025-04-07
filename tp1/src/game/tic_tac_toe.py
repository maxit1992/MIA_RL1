import random

from .board import Board
from .players import Player


class TicTacToe:
    """
    Tic Tac Toe game class.
    """

    SYMBOL_PLAYER1 = "X"
    SYMBOL_PLAYER2 = "O"

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
        print("New Game")
        player2_turn = random.choice([False, True])
        if player2_turn:
            self.player2.start()
        else:
            self.player1.start()
        while not (self.board.is_full()):
            if player2_turn:
                pos_x, pos_y = self.player_play(self.player2)
                self.board.place_symbol(self.SYMBOL_PLAYER2, pos_x, pos_y)
                self.board.print()
                if self.board.is_winner(self.SYMBOL_PLAYER2):
                    self.player2.win()
                    self.player1.loose()
                    return
            else:
                pos_x, pos_y = self.player_play(self.player1)
                self.board.place_symbol(self.SYMBOL_PLAYER1, pos_x, pos_y)
                self.board.print()
                if self.board.is_winner(self.SYMBOL_PLAYER1):
                    self.player1.win()
                    self.player2.loose()
                    return
            player2_turn = not player2_turn
        self.player1.draw()
        self.player2.draw()

    def player_play(self, player: Player):
        """
        Handle the player's turn. Get the player's move and check the validity.
        """
        pos_x, pos_y = -1, -1
        empty_spots = self.board.get_empty_spots()
        while (pos_x, pos_y) not in empty_spots:
            pos_x, pos_y = player.turn(self.board)
            if (pos_x, pos_y) not in empty_spots:
                player.invalid_position()
        return pos_x, pos_y

    def random_board(self):
        """
        Generates a random board state for Tic Tac Toe.
        """
        player2_turn = random.choice([True, False])
        while True:
            self.board = Board()
            for _ in range(0, random.randrange(0, 9)):
                empty_spots = self.board.get_empty_spots()
                pos_x, pos_y = empty_spots.pop(random.randrange(len(empty_spots)))
                symbol = self.SYMBOL_PLAYER2 if player2_turn else self.SYMBOL_PLAYER1
                self.board.place_symbol(symbol, pos_x, pos_y)
                player2_turn = not player2_turn
            if not self.board.is_winner(self.SYMBOL_PLAYER2) and not self.board.is_winner(self.SYMBOL_PLAYER1):
                break
