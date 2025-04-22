"""
This script allows you to play or train a Tic Tac Toe game using different players.
You can play against a bot, a Monte Carlo model, or another human player.
It also allows you to train a Monte Carlo or a Q-learning model using reinforcement learning.

Usage:
    main.py play --games=<number_of_games> [--bot] [--model-file=<model-file>] [--human]
    main.py train --model=<model-type> --episodes=<number_of_episodes>

Options:
    -h --help                       Show this screen.
    --bot                           Play against a bot.
    --episodes=<number_of_episodes> Number of episodes to train the Monte Carlo model.
    --games=<number_of_games>       Number of games to play.
    --human                         Play against another human player.
    --model-file=<model-file>       Play against a trained model.
    --model=<model_type>            The type of model to train. Valid options are: monte-carlo or q-learning.
"""

import os
import pickle
import sys
from contextlib import contextmanager
from datetime import datetime

from docopt import docopt
from tqdm import tqdm

from game.board import Board
from game.monte_carlo import MonteCarloEsControl
from game.players import BotPlayer, UserPlayer
from game.q_learning import QLearning
from game.tic_tac_toe import TicTacToe


@contextmanager
def suppress_stdout():
    """
    Context manager to suppress standard output.
    """
    with open(os.devnull, 'w') as devnull:
        old_stdout = sys.stdout
        sys.stdout = devnull
        try:
            yield
        finally:
            sys.stdout = old_stdout


def play(args: dict):
    """
    Play the Tic Tac Toe game with the specified players.

    Args:
        args (dict): Command line arguments.
    """
    player_1 = UserPlayer()
    if args['--bot']:
        player_2 = BotPlayer()
    elif args['--model-file']:
        with open(args['--model-file'], 'rb') as file:
            # noinspection PyTypeChecker
            model_player = pickle.load(file)
        player_2 = model_player
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
    if args['--model'] == 'monte-carlo':
        model_player = MonteCarloEsControl()
        random_start = True
    elif args['--model'] == 'q-learning':
        model_player = QLearning()
        random_start = False
    else:
        raise RuntimeError('Invalid model')
    model_player.set_train(True)
    bot_player = BotPlayer()
    total_episodes = int(args['--episodes'])
    update_episodes = int(total_episodes / 100)
    pbar = tqdm(range(total_episodes))
    for episode in pbar:
        try:
            with suppress_stdout():  # Suppress console output
                game = TicTacToe(bot_player, model_player, Board())
                if random_start:
                    game.random_board()
                game.start()
        except RuntimeWarning:
            pass
        if episode % update_episodes == 0:
            pbar.set_description(f"Episode {episode} |"
                                 f" Average reward: {model_player.get_average_reward(episodes=update_episodes)} |"
                                 f" Average success rate: {model_player.get_success_rate(episodes=update_episodes)}")
    model_player.set_train(False)
    # Plot the training results
    model_player.plot_rewards(episodes=100)
    model_player.plot_success_rate(episodes=100)
    with open('model-' + datetime.now().strftime('%Y_%m_%d-%H_%M_%S') + '.pkl', 'wb') as file:
        # noinspection PyTypeChecker
        pickle.dump(model_player, file)


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
