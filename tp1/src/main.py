"""
This script initializes the Tic-Tac-Toe game with a human player and a bot player, and starts the game.
"""

from game.players import UserPlayer, BotPlayer
from game.tic_tac_toe import TicTacToe

if __name__ == "__main__":
    user_player = UserPlayer()
    bot_player = BotPlayer()
    game = TicTacToe(user_player, bot_player)
    game.start()
