import random
from abc import ABC, abstractmethod

from .board import Board


class Player(ABC):
    """
    An abstract base class to represent a player in the Tic Tac Toe game.
    """

    @abstractmethod
    def start(self):
        """
        Method called whenever the player will make the first movement of the game.
        """
        pass

    @abstractmethod
    def turn(self, board: Board):
        """
        Method called to handle the player's turn.

        Parameters
        ----------
        board : Board
            The current state of the game board.
        """
        pass

    @abstractmethod
    def win(self):
        """
        Method called whenever the player wins.
        """
        pass

    @abstractmethod
    def loose(self):
        """
        Method called whenever player looses.
        """
        pass

    @abstractmethod
    def draw(self):
        """
        Method called whenever the player draws.
        """
        pass


class UserPlayer(Player):
    """
    A class to represent a human player in the Tic Tac Toe game.
    """

    def start(self):
        """
        Prints a message indicating the user starts the game.
        """
        print("User starts")

    def turn(self, board: Board):
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
        pos_x = -1
        pos_y = -1
        empty_slots = board.get_empty_spots()
        while (pos_x, pos_y) not in empty_slots:
            place = int(input("Pick a position:"))
            pos_x = place % 3
            pos_y = int(place / 3)
        return pos_x, pos_y

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

    def start(self):
        """
        Prints a message indicating the bot starts the game.
        """
        print("Bot starts")

    def turn(self, board: Board):
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
