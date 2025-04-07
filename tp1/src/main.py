"""
This script allows you to play or train a Tic Tac Toe game using different players.
You can play against a bot, a Monte Carlo model, or another human player.
It also allows you to train a Monte Carlo model using reinforcement learning.

Usage:
    main.py play --games=<number_of_games> [--bot] [--monte_carlo=<model_file>] [--human]
    main.py train --episodes=<number_of_episodes>

Options:
    -h --help                       Show this screen.
    --bot                           Play against a bot.
    --episodes=<number_of_episodes> Number of episodes to train the Monte Carlo model.
    --games=<number_of_games>       Number of games to play.
    --human                         Play against another human player.
    --monte_carlo=<model_file>      Play against a trained Monte Carlo model.
"""

import pickle
from datetime import datetime

from docopt import docopt
from tqdm import tqdm

from game.board import Board
from game.monte_carlo import MonteCarloEsControl
from game.players import BotPlayer, UserPlayer
from game.tic_tac_toe import TicTacToe


def play(args: dict):
    """
    Play the Tic Tac Toe game with the specified players.

    Args:
        args (dict): Command line arguments.
    """
    player_1 = UserPlayer()
    if args['--bot']:
        player_2 = BotPlayer()
    elif args['--monte_carlo']:
        with open(args['--monte_carlo'], 'rb') as file:
            # noinspection PyTypeChecker
            monte_carlo_player = pickle.load(file)
        player_2 = monte_carlo_player
    elif args['--human']:
        player_2 = UserPlayer()
    else:
        raise RuntimeError('Invalid run mode')
    for _ in range(int(args['--games'])):
        board = Board()
        game = TicTacToe(player_1, player_2, board)
        game.start()


def train(args: dict):
    """
    Train the Monte Carlo RL model using the specified training parameters.

    Args:
        args (dict): Command line arguments.
    """
    monte_carlo_player = MonteCarloEsControl()
    monte_carlo_player.set_train(True)
    bot_player = BotPlayer()
    for _ in tqdm(range(int(args['--episodes']))):
        try:
            game = TicTacToe(bot_player, monte_carlo_player)
            game.random_board()
            game.start()
        except RuntimeWarning:
            pass
    monte_carlo_player.set_train(False)
    with open('monte_carlo-' + datetime.now().strftime('%Y_%m_%d-%H_%M_%S') + '.pkl', 'wb') as file:
        # noinspection PyTypeChecker
        pickle.dump(monte_carlo_player, file)


def main():
    """
    Main function to parse command line arguments and start the game.
    """
    args = docopt(__doc__)
    if args['play']:
        play(args)
    elif args['train']:
        train(args)
    else:
        print("Invalid command. Use --help for usage information.")


if __name__ == "__main__":
    main()
