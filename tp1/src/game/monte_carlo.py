import random

import matplotlib.pyplot as plt

from .board import Board
from .players import Player


def _board_to_index(board: Board):
    index = ""
    for i in range(3):
        for j in range(3):
            index += board.grid[i][j]
    return index


def _pos_to_xy(pos: int):
    pos_x = pos % 3
    pos_y = int(pos / 3)
    return pos_x, pos_y


def _xy_to_pos(pos_x: int, pos_y: int):
    return pos_x + pos_y * 3


class MonteCarloEsControl(Player):
    """
    Monte Carlo Es Control player for Tic Tac Toe.
    This player uses Monte Carlo methods to learn and improve its strategy over time.
    """

    def __init__(self):
        """
        Initializes the Monte Carlo Es Control player.
        """
        self.q_values = {}
        self.policy = {}
        self.returns_sum = {}
        self.return_count = {}
        self.episode_steps = []
        self.episode_rewards = []
        self.train_results = []
        self.train_rewards = []
        self.episode = 0
        self.train = False

    def start(self):
        """
        Initializes the player for a new game.
        Resets the episode count and clears the steps and rewards.
        """
        # Reset the episode
        self.episode_steps = []
        self.episode_rewards = []
        self.episode += 1

    def turn(self, board: Board) -> (int, int):
        """
        Returns the next move for the player based on the current board state.
        If the player is in training mode, it explores the board and updates its policy.

        Parameters
        ----------
        board : Board
            The current state of the game board.
        Returns
        -------
        tuple
            The (x, y) coordinates of the chosen position.
        """
        index = _board_to_index(board)
        if not self.train:
            next_step = self.policy[index]
        else:
            # Check if we are over the limit of turns
            if len(self.episode_steps) >= 20:
                self.episode_rewards.append(-50)
                self.train_results.append('I')
                self._update_q_values_and_policy()
                raise RuntimeWarning("No more moves left")
            elif len(self.episode_steps) > 0:
                # Update rewards for the last step
                self.episode_rewards.append(-0.1)

            if len(self.episode_steps) == 0:
                # First movement is random to explore
                next_step = random.randint(0, 9)
            elif index not in self.policy:
                # If movement is not defined we define one
                empty_spot = board.get_empty_spots()
                next_step_x, next_step_y = empty_spot.pop(random.randrange(len(empty_spot)))
                next_step = _xy_to_pos(next_step_x, next_step_y)
                self.policy[index] = next_step
            else:
                next_step = self.policy[index]
            self.episode_steps.append((index, next_step))

        return _pos_to_xy(next_step)

    def invalid_position(self):
        """
        Prints a message indicating monte carlo has chosen an invalid position.
        """
        print("MonteCarlo choose an invalid position")

    def win(self):
        """
        Prints a message indicating monte carlo has won.
        Updates the rewards and Q-values if in training mode.
        """
        print("MonteCarlo Wins")
        if self.train:
            self.episode_rewards.append(10)
            self.train_results.append('W')
            self._update_q_values_and_policy()

    def loose(self):
        """
        Prints a message indicating monte carlo has lost.
        Updates the rewards and Q-values if in training mode.
        """
        print("MonteCarlo Loose")
        if self.train:
            self.episode_rewards.append(-10)
            self.train_results.append('L')
            self._update_q_values_and_policy()

    def draw(self):
        """
        Prints a message indicating monte carlo has drawn.
        Updates the rewards and Q-values if in training mode.
        """
        print("MonteCarlo Draw")
        if self.train:
            self.episode_rewards.append(-2)
            self.train_results.append('D')
            self._update_q_values_and_policy()

    def set_train(self, train: bool):
        """
        Set the training mode for monte carlo.
        """
        self.train = train

    def get_average_reward(self, episodes: int = 100) -> float:
        """
        Get the average reward over the last n episodes.

        Parameters
        ----------
        episodes : int
            The number of episodes to consider for the average.

        Returns
        -------
        float
            The average reward.
        """
        if len(self.train_rewards) < episodes:
            return sum(self.train_rewards) / len(self.train_rewards)
        else:
            return sum(self.train_rewards[-episodes:]) / episodes

    def plot_rewards(self, episodes: int = 100) -> None:
        """
        Plot episode rewards with a moving average over n episodes.

        Parameters
        ----------
        episodes : int
            The moving average window size.
        """
        moving_avg = [
            sum(self.train_rewards[max(0, i - episodes + 1):i + 1]) / min(i + 1, episodes)
            for i in range(len(self.train_rewards))
        ]
        plt.figure(figsize=(10, 5))
        plt.plot(self.train_rewards, label="Episode Rewards", alpha=0.6)
        plt.plot(moving_avg, label=f"Moving Average ({episodes} episodes)", color="red")
        plt.xlabel("Episodes")
        plt.ylabel("Reward")
        plt.title("Episode Rewards")
        plt.legend()
        plt.grid()
        plt.show()

    def plot_success_rate(self, episodes: int = 100) -> None:
        """
        Plot the success rate with a moving average over n episodes.

        Parameters
        ----------
        episodes : int
            The moving average window size.
        """
        moving_avg = [
            sum([1 for r in self.train_results[max(0, i - episodes + 1):i + 1] if r == 'W']) / min(i + 1, episodes)
            for i in range(len(self.train_results))
        ]
        plt.figure(figsize=(10, 5))
        plt.plot(moving_avg, label=f"Success Rate ({episodes} episodes)", color="green")
        plt.xlabel("Episodes")
        plt.ylabel("Success Rate")
        plt.title("Success Rate")
        plt.legend()
        plt.grid()
        plt.show()

    def get_success_rate(self, episodes: int = 100) -> float:
        """
        Get the success rate over the last n episodes.

        Parameters
        ----------
        episodes : int
            The number of episodes to consider for the success rate.

        Returns
        -------
        float
            The success rate.
        """
        if len(self.train_results) < episodes:
            return sum([1 for result in self.train_results if result == 'W']) / len(self.train_results)
        else:
            return sum([1 for result in self.train_results[-episodes:] if result == 'W']) / episodes

    def _update_q_values_and_policy(self):
        # Update the Q-values with the rewards of the episode
        cumulative_reward = 0
        while len(self.episode_steps) > 0:
            index, action = self.episode_steps.pop()
            cumulative_reward = self.episode_rewards.pop() + 0.9 * cumulative_reward
            if (index, action) not in self.episode_steps:
                if (index, action) not in self.returns_sum:
                    self.returns_sum[(index, action)] = 0
                    self.return_count[(index, action)] = 0
                self.returns_sum[(index, action)] += cumulative_reward
                self.return_count[(index, action)] += 1
                if index not in self.q_values:
                    self.q_values[index] = {}
                self.q_values[index][action] = self.returns_sum[(index, action)] / self.return_count[(index, action)]
        self.train_rewards.append(cumulative_reward)
        # Update the policy with the new best action
        for index in self.q_values.keys():
            best_action = max(self.q_values[index], key=self.q_values[index].get)
            self.policy[index] = best_action
