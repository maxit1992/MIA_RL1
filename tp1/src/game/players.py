import random
from abc import ABC, abstractmethod

from .board import Board
from .utils import pos_to_xy


class Player(ABC):
    """
    An abstract base class to represent a player in the Tic Tac Toe game.
    """

    @abstractmethod
    def new_game(self):
        """
        Method called whenever a new game start.
        """

    @abstractmethod
    def start(self):
        """
        Method called whenever the player will make the first movement of the game.
        """

    @abstractmethod
    def turn(self, board: Board) -> (int, int):
        """
        Method called to handle the player's turn and return the position to place the symbol.

        Parameters
        ----------
        board : Board
            The current state of the game board.

        Returns
        -------
        tuple
            The (x, y) coordinates of the new symbol position.
        """

    @abstractmethod
    def invalid_position(self):
        """
        Method called whenever the player turn returned an invalid position.
        """

    @abstractmethod
    def win(self):
        """
        Method called whenever the player wins.
        """

    @abstractmethod
    def loose(self):
        """
        Method called whenever player looses.
        """

    @abstractmethod
    def draw(self):
        """
        Method called whenever the player draws.
        """


class UserPlayer(Player):
    """
    A class to represent a human player in the Tic Tac Toe game.
    """

    def new_game(self):
        """
        Prints a message indicating the user starts a new game.
        """
        print("User participates in a new game")

    def start(self):
        """
        Prints a message indicating the user starts the game.
        """
        print("User starts")

    def turn(self, board: Board) -> (int, int):
        """
        Prompts the user to pick a position on the board and returns the coordinates.

        Parameters
        ----------
        board : Board
            The current state of the game board.

        Returns
        -------
        tuple
            The (x, y) coordinates of the chosen position.
        """
        place = int(input("Pick a position:"))
        return pos_to_xy(place)

    def invalid_position(self):
        """
        Prints a message indicating the user has chosen an invalid position.
        """
        print("Invalid position")

    def win(self):
        """
        Prints a message indicating the user has won.
        """
        print("User won")

    def loose(self):
        """
        Prints a message indicating the user has lost.
        """
        print("User loose")

    def draw(self):
        """
        Prints a message indicating the game is a draw.
        """
        print("User Draw")


class BotPlayer(Player):
    """
    A class to represent a bot player in the Tic Tac Toe game.
    """

    def new_game(self):
        """
        Prints a message indicating the random bot starts a new game.
        """
        print("Bot participates in a new game")

    def start(self):
        """
        Prints a message indicating the bot starts the game.
        """
        print("Bot starts")

    def turn(self, board: Board) -> (int, int):
        """
        Randomly selects an empty spot on the board and returns the coordinates.

        Parameters
        ----------
        board : Board
            The current state of the game board.

        Returns
        -------
        tuple
            The (x, y) coordinates of the chosen position.
        """
        empty_spot = board.get_empty_spots()
        pos_x, pos_y = empty_spot.pop(random.randrange(len(empty_spot)))
        return pos_x, pos_y

    def invalid_position(self):
        """
        Bot shouldn't choose an invalid position, so this method raise an exception.
        """
        raise ValueError("Bot choose an invalid position")

    def win(self):
        """
        Prints a message indicating the bot has won.
        """
        print("Bot won")

    def loose(self):
        """
        Prints a message indicating the bot has lost.
        """
        print("Bot loose")

    def draw(self):
        """
        Prints a message indicating the game is a draw.
        """
        print("Bot Draw")
