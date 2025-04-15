import random

import pytest

from src.game.board import Board
from src.game.monte_carlo import MonteCarloEsControl


@pytest.fixture
def board():
    return Board()


@pytest.fixture
def monte_carlo():
    return MonteCarloEsControl()


def test_start_resets_episode(monte_carlo):
    # Given
    monte_carlo.episode = 5
    monte_carlo.episode_steps = [(0, 0)]
    monte_carlo.episode_rewards = [1]
    # When
    monte_carlo.start()
    # Then
    assert monte_carlo.episode == 6
    assert monte_carlo.episode_steps == []
    assert monte_carlo.episode_rewards == []


def test_turn_play_returns_policy_position(monte_carlo, board):
    # Given
    board.place_symbol("X", 1, 0)
    monte_carlo.policy = {" X       ": 5}
    # When
    pos_x, pos_y = monte_carlo.turn(board)
    # Then
    assert (pos_x, pos_y) == (2, 1)


def test_turn_train_first_movement_returns_random(monte_carlo, board):
    # Given
    monte_carlo.set_train(True)
    random.seed(47)
    # When
    pos_x, pos_y = monte_carlo.turn(board)
    # Then
    assert (pos_x, pos_y) == (2, 1)


def test_turn_train_second_movement_returns_new_random_policy_position(monte_carlo, board):
    # Given
    monte_carlo.set_train(True)
    random.seed(47)
    monte_carlo.episode_steps = [("         ", 0)]
    board.place_symbol("X", 0, 0)
    # When
    pos_x, pos_y = monte_carlo.turn(board)
    # Then
    assert (pos_x, pos_y) == (0, 2)
    assert monte_carlo.policy == {"X        ": 6}


def test_turn_train_second_movement_returns_existing_policy_position(monte_carlo, board):
    # Given
    monte_carlo.set_train(True)
    random.seed(47)
    monte_carlo.episode_steps = [("         ", 0)]
    board.place_symbol("X", 0, 0)
    monte_carlo.policy = {"X        ": 8}
    # When
    pos_x, pos_y = monte_carlo.turn(board)
    # Then
    assert (pos_x, pos_y) == (2, 2)
    assert monte_carlo.episode_rewards == [-0.1]


def test_turn_train_second_movement_updates_reward(monte_carlo, board):
    # Given
    monte_carlo.set_train(True)
    random.seed(47)
    monte_carlo.episode_steps = [("         ", 0)]
    board.place_symbol("X", 0, 0)
    monte_carlo.policy = {"X        ": 8}
    # When
    monte_carlo.turn(board)
    # Then
    assert monte_carlo.episode_rewards == [-0.1]


def test_invalid_position_prints_message(capsys, monte_carlo):
    # When
    monte_carlo.invalid_position()
    # Then
    captured = capsys.readouterr()
    assert captured.out != ""


def test_win_train_prints_message_and_updates_q_values(capsys, monte_carlo):
    # Given
    monte_carlo.train = True
    monte_carlo.episode_steps = [("index", 0)]
    monte_carlo.episode_rewards = [1]
    # When
    monte_carlo.win()
    # Then
    captured = capsys.readouterr()
    assert captured.out != ""
    assert monte_carlo.q_values != {}


def test_loose_prints_message_and_updates_q_values(capsys, monte_carlo):
    # Given
    monte_carlo.train = True
    monte_carlo.episode_steps = [("index", 0)]
    monte_carlo.episode_rewards = [1]
    # When
    monte_carlo.loose()
    # Then
    captured = capsys.readouterr()
    assert captured.out != ""
    assert monte_carlo.q_values != {}


def test_draw_prints_message_and_updates_q_values(capsys, monte_carlo):
    # Given
    monte_carlo.train = True
    monte_carlo.episode_steps = [("index", 0)]
    monte_carlo.episode_rewards = [1]
    # When
    monte_carlo.draw()
    # Then
    captured = capsys.readouterr()
    assert captured.out != ""
    assert monte_carlo.q_values != {}


def test_turn_train_limit_movements_raise_warning_and_updates_q_values(monte_carlo, board):
    # Given
    monte_carlo.set_train(True)
    random.seed(47)
    monte_carlo.episode_steps = [("", 0) for _ in range(20)]
    monte_carlo.episode_rewards = [-0.1] * 19
    # When & Then
    with pytest.raises(RuntimeWarning):
        monte_carlo.turn(board)
    # Then
    assert monte_carlo.q_values != {}
    assert monte_carlo.policy != {}


def test_set_train_mode(monte_carlo):
    # When
    monte_carlo.set_train(True)
    # Then
    assert monte_carlo.train is True
    # When
    monte_carlo.set_train(False)
    # Then
    assert monte_carlo.train is False


def test_get_average_reward(monte_carlo):
    # Given
    monte_carlo.train_rewards = [1, 2, 3, 4, 5]
    # When
    avg_reward_all = monte_carlo.get_average_reward(episodes=5)
    avg_reward_partial = monte_carlo.get_average_reward(episodes=3)
    avg_reward_more_than_available = monte_carlo.get_average_reward(episodes=10)
    # Then
    assert avg_reward_all == 3.0
    assert avg_reward_partial == 4.0
    assert avg_reward_more_than_available == 3.0


def test_plot_rewards(monte_carlo, mocker):
    # Given
    monte_carlo.train_rewards = [1, 2, 3, 4, 5]
    mock_show = mocker.patch("matplotlib.pyplot.show")
    # When
    monte_carlo.plot_rewards(episodes=3)
    # Then
    mock_show.assert_called_once()


def test_get_success_rate(monte_carlo):
    # Given
    monte_carlo.train_results = ['W', 'L', 'W', 'D', 'W']
    # When
    success_rate_all = monte_carlo.get_success_rate(episodes=5)
    success_rate_partial = monte_carlo.get_success_rate(episodes=3)
    success_rate_more_than_available = monte_carlo.get_success_rate(episodes=10)
    # Then
    assert success_rate_all == 3 / 5
    assert success_rate_partial == 2 / 3
    assert success_rate_more_than_available == 3 / 5


def test_plot_success_rate(monte_carlo, mocker):
    # Given
    monte_carlo.train_results = ['W', 'L', 'W', 'D', 'W']
    mock_show = mocker.patch("matplotlib.pyplot.show")
    # When
    monte_carlo.plot_success_rate(episodes=3)
    # Then
    mock_show.assert_called_once()


def test_update_q_values_and_policy(monte_carlo):
    # Given
    monte_carlo.episode_steps = [("b1", 0), ("b2", 1), ("b3", 2)]
    monte_carlo.episode_rewards = [-0.1, -0.1, 10]
    monte_carlo.returns_sum = {("b1", 0): 2, ("b2", 1): -0.1, ("b3", 2): 5}
    monte_carlo.return_count = {("b1", 0): 1, ("b2", 1): 1, ("b3", 2): 1}
    monte_carlo.q_values = {"b1": {0: 2, 1: 5}, "b2": {1: -10}, "b3": {2: -10}}
    monte_carlo.policy = {"b1": 8, "b2": 8, "b3": 8}
    # When
    monte_carlo._update_q_values_and_policy()
    # Then
    assert monte_carlo.q_values == {"b1": {0: 4.955, 1: 5}, "b2": {1: 4.4}, "b3": {2: 7.5}}
    assert monte_carlo.policy == {"b1": 1, "b2": 1, "b3": 2}
