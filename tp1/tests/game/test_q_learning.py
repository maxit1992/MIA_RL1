import random

import pytest

from src.game.board import Board
from src.game.q_learning import QLearning


@pytest.fixture
def board():
    return Board()


@pytest.fixture
def q_learning():
    return QLearning()


def test_start_player_start_prints_message(capsys, q_learning):
    # When
    q_learning.start()
    # Then
    captured = capsys.readouterr()
    assert captured.out != ""


def test_new_game_train_resets_episode(q_learning):
    # Given
    q_learning.set_train(True)
    q_learning.n_steps = 5
    q_learning.episode_reward = 10
    q_learning.last_state = "state"
    q_learning.last_action = 1
    # When
    q_learning.new_game()
    # Then
    assert q_learning.n_steps == 0
    assert q_learning.episode_reward == 0
    assert q_learning.last_state is None
    assert q_learning.last_action is None


def test_new_game_not_train_does_not_reset_episode(q_learning):
    # Given
    q_learning.set_train(False)
    q_learning.n_steps = 5
    q_learning.episode_reward = 10
    q_learning.last_state = "state"
    q_learning.last_action = 1
    # When
    q_learning.new_game()
    # Then
    assert q_learning.n_steps == 5
    assert q_learning.episode_reward == 10
    assert q_learning.last_state == "state"
    assert q_learning.last_action == 1


def test_new_game_prints_message(capsys, q_learning):
    # Given
    q_learning.set_train(False)
    # When
    q_learning.new_game()
    # Then
    captured = capsys.readouterr()
    assert captured.out != ""


def test_turn_play_returns_best_q_value_position(q_learning, board):
    # Given
    q_learning.set_train(False)
    board.place_symbol("X", 1, 0)
    q_learning.q_values = {" X       ": {5: 1.0, 6: 0.5}}
    # When
    pos_x, pos_y = q_learning.turn(board)
    # Then
    assert (pos_x, pos_y) == (2, 1)


def test_turn_train_explores_random_position(q_learning, board):
    # Given
    q_learning.set_train(True)
    random.seed(47)
    # When
    pos_x, pos_y = q_learning.turn(board)
    # Then
    assert (pos_x, pos_y) == (2, 1)


def test_turn_train_updates_q_values(q_learning, board):
    # Given
    q_learning.set_train(True)
    random.seed(47)
    q_learning.last_state = "state"
    q_learning.last_action = 0
    q_learning.q_values = {"state": {0: 0.5}}
    q_learning.episode_reward = 0
    board.place_symbol("X", 0, 0)
    # When
    q_learning.turn(board)
    # Then
    assert q_learning.q_values["state"][0] != 0.5


def test_invalid_position_prints_message(capsys, q_learning):
    # When
    q_learning.invalid_position()
    # Then
    captured = capsys.readouterr()
    assert captured.out != ""


def test_win_train_prints_message_and_updates_q_values(capsys, q_learning):
    # Given
    q_learning.set_train(True)
    q_learning.last_state = "state"
    q_learning.last_action = 0
    q_learning.q_values = {"state": {0: 0.5}}
    q_learning.episode_reward = 0
    # When
    q_learning.win()
    # Then
    captured = capsys.readouterr()
    assert captured.out != ""
    assert q_learning.q_values["state"][0] != 0.5


def test_loose_prints_message_and_updates_q_values(capsys, q_learning):
    # Given
    q_learning.set_train(True)
    q_learning.last_state = "state"
    q_learning.last_action = 0
    q_learning.q_values = {"state": {0: 0.5}}
    q_learning.episode_reward = 0
    # When
    q_learning.loose()
    # Then
    captured = capsys.readouterr()
    assert captured.out != ""
    assert q_learning.q_values["state"][0] != 0.5


def test_draw_prints_message_and_updates_q_values(capsys, q_learning):
    # Given
    q_learning.set_train(True)
    q_learning.last_state = "state"
    q_learning.last_action = 0
    q_learning.q_values = {"state": {0: 0.5}}
    q_learning.episode_reward = 0
    # When
    q_learning.draw()
    # Then
    captured = capsys.readouterr()
    assert captured.out != ""
    assert q_learning.q_values["state"][0] != 0.5


def test_turn_train_limit_movements_raise_warning_and_updates_q_values(q_learning, board):
    # Given
    q_learning.set_train(True)
    random.seed(47)
    q_learning.n_steps = 20
    q_learning.last_state = "state"
    q_learning.last_action = 0
    q_learning.q_values = {"state": {0: 0.5}}
    # When & Then
    with pytest.raises(RuntimeWarning):
        q_learning.turn(board)
    # Then
    assert q_learning.q_values["state"][0] != 0.5


def test_set_train_mode(q_learning):
    # When
    q_learning.set_train(True)
    # Then
    assert q_learning.train is True
    # When
    q_learning.set_train(False)
    # Then
    assert q_learning.train is False


def test_get_average_reward(q_learning):
    # Given
    q_learning.train_rewards = [1, 2, 3, 4, 5]
    # When
    avg_reward_all = q_learning.get_average_reward(episodes=5)
    avg_reward_partial = q_learning.get_average_reward(episodes=3)
    avg_reward_more_than_available = q_learning.get_average_reward(episodes=10)
    # Then
    assert avg_reward_all == 3.0
    assert avg_reward_partial == 4.0
    assert avg_reward_more_than_available == 3.0


def test_plot_rewards(q_learning, mocker):
    # Given
    q_learning.train_rewards = [1, 2, 3, 4, 5]
    mock_show = mocker.patch("matplotlib.pyplot.show")
    # When
    q_learning.plot_rewards(episodes=3)
    # Then
    mock_show.assert_called_once()


def test_get_success_rate(q_learning):
    # Given
    q_learning.train_results = ['W', 'L', 'W', 'D', 'W']
    # When
    success_rate_all = q_learning.get_success_rate(episodes=5)
    success_rate_partial = q_learning.get_success_rate(episodes=3)
    success_rate_more_than_available = q_learning.get_success_rate(episodes=10)
    # Then
    assert success_rate_all == 3 / 5
    assert success_rate_partial == 2 / 3
    assert success_rate_more_than_available == 3 / 5


def test_plot_success_rate(q_learning, mocker):
    # Given
    q_learning.train_results = ['W', 'L', 'W', 'D', 'W']
    q_learning.episode_reward = 0