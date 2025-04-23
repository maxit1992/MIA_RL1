import random

import matplotlib.pyplot as plt

from .board import Board
from .players import Player
from .utils import pos_to_xy, xy_to_pos, board_to_index


class QLearning(Player):
    """
    Q-Learning player for Tic Tac Toe.
    This player uses Q-Learning methods to learn and improve its strategy over time.
    """

    def __init__(self):
        """
        Initializes the Q-Learning player.
        """
        self.alpha = 0.1
        self.epsilon = 0.2
        self.gamma = 0.9
        self.train = False
        self.q_values = {}
        self.last_state = None
        self.last_action = None
        self.n_steps = 0
        self.episode_reward = 0
        self.train_results = []
        self.train_rewards = []

    def new_game(self):
        """
        Prints a message indicating q-learning is participating in a new game.
        If the mode is training, it initializes the episode steps and rewards.
        :return:
        """
        print("Q-Learning participates in a new game")
        if self.train:
            self.n_steps = 0
            self.episode_reward = 0
            self.last_state = None
            self.last_action = None

    def start(self):
        """
        Prints a message indicating q-learning starts the game.
        """
        print("Q-Learning starts")

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
        index = board_to_index(board)
        if not self.train:
            next_step = max(self.q_values[index], key=self.q_values[index].get)
        else:
            if index not in self.q_values:
                # Check if Q-values are initialized for the current state
                self.q_values[index] = {i: 0 for i in range(9)}
            if self.n_steps >= 20:
                # Check if we are over the limit of turns
                self.train_results.append('I')
                reward = -50
                self.episode_reward += reward
                self._update_q_values(self.last_state, self.last_action, reward, 0)
                self.train_rewards.append(self.episode_reward)
                raise RuntimeWarning("No more moves left")
            elif self.n_steps > 0:
                # Update last step rewards
                reward = -0.1
                self.episode_reward += reward
                actual_max_q_value = max(self.q_values[index].values())
                self._update_q_values(self.last_state, self.last_action, reward, actual_max_q_value)

            # Choose the next step
            if random.random() < self.epsilon:
                # Explore: choose a random action
                empty_spot = board.get_empty_spots()
                next_step_x, next_step_y = empty_spot.pop(random.randrange(len(empty_spot)))
                next_step = xy_to_pos(next_step_x, next_step_y)
            else:
                # Exploit: choose the best action based on Q-values
                next_step = max(self.q_values[index], key=self.q_values[index].get)
            self.last_state = index
            self.last_action = next_step
            self.n_steps += 1

        return pos_to_xy(next_step)

    def invalid_position(self):
        """
        Prints a message indicating q-learning has chosen an invalid position.
        """
        print("Q-Learning choose an invalid position")

    def win(self):
        """
        Prints a message indicating q-learning has won.
        Updates the rewards and Q-values if in training mode.
        """
        print("Q-Learning Wins")
        if self.train:
            reward = 10
            self.episode_reward += reward
            self._update_q_values(self.last_state, self.last_action, reward, 0)
            self.train_rewards.append(self.episode_reward)
            self.train_results.append('W')

    def loose(self):
        """
        Prints a message indicating q-learning has lost.
        Updates the rewards and Q-values if in training mode.
        """
        print("Q-Learning Loose")
        if self.train:
            reward = -10
            self.episode_reward += reward
            self._update_q_values(self.last_state, self.last_action, reward, 0)
            self.train_rewards.append(self.episode_reward)
            self.train_results.append('L')

    def draw(self):
        """
        Prints a message indicating q-learning has drawn.
        Updates the rewards and Q-values if in training mode.
        """
        print("Q-Learning Draw")
        if self.train:
            reward = -2
            self.episode_reward += reward
            self._update_q_values(self.last_state, self.last_action, reward, 0)
            self.train_rewards.append(self.episode_reward)
            self.train_results.append('D')

    def set_train(self, train: bool):
        """
        Set the training mode for q-learning.
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
        Plot a moving average (over n episodes) of the rewards.

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

    def _update_q_values(self, last_state: str, last_action: int, reward: float, max_q_value: float):
        self.q_values[last_state][last_action] = (
                self.q_values[last_state][last_action] +
                self.alpha * (reward + self.gamma * max_q_value - self.q_values[last_state][last_action]))
