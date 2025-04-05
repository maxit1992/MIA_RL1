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
    monte_carlo.steps = [(0, 0)]
    monte_carlo.rewards = [1]
    # When
    monte_carlo.start()
    # Then
    assert monte_carlo.episode == 6
    assert monte_carlo.steps == []
    assert monte_carlo.rewards == []


def test_turn_play_returns_policy_position(monte_carlo, board):
    # Given
    board.place_symbol("X", 1, 0)
    monte_carlo.policy = {" X       ": 5}
    # When
    pos_x, pos_y = monte_carlo.turn(board)
    # Then
    assert (pos_x, pos_y) == (2, 1)


def test_invalid_position_prints_message(capsys, monte_carlo):
    # When
    monte_carlo.invalid_position()
    # Then
    captured = capsys.readouterr()
    assert captured.out != ""


def test_win_train_prints_message_and_updates_q_values(capsys, monte_carlo):
    # Given
    monte_carlo.train = True
    monte_carlo.steps = [("index", 0)]
    monte_carlo.rewards = [1]
    # When
    monte_carlo.win()
    # Then
    captured = capsys.readouterr()
    assert captured.out != ""
    assert monte_carlo.q_values != {}


def test_loose_prints_message_and_updates_q_values(capsys, monte_carlo):
    # Given
    monte_carlo.train = True
    monte_carlo.steps = [("index", 0)]
    monte_carlo.rewards = [1]
    # When
    monte_carlo.loose()
    # Then
    captured = capsys.readouterr()
    assert captured.out != ""
    assert monte_carlo.q_values != {}


def test_draw_prints_message_and_updates_q_values(capsys, monte_carlo):
    # Given
    monte_carlo.train = True
    monte_carlo.steps = [("index", 0)]
    monte_carlo.rewards = [1]
    # When
    monte_carlo.draw()
    # Then
    captured = capsys.readouterr()
    assert captured.out != ""
    assert monte_carlo.q_values != {}


def test_set_train_mode(monte_carlo):
    # When
    monte_carlo.set_train(True)
    # Then
    assert monte_carlo.train is True
    # When
    monte_carlo.set_train(False)
    # Then
    assert monte_carlo.train is False
