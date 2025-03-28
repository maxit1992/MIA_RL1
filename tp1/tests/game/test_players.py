import pytest

from src.game.board import Board
from src.game.players import UserPlayer, BotPlayer


@pytest.fixture
def board():
    return Board()


@pytest.fixture
def user_player():
    return UserPlayer()


@pytest.fixture
def bot_player():
    return BotPlayer()


def test_user_player_start_prints_message(capsys, user_player):
    # When
    user_player.start()
    # Then
    captured = capsys.readouterr()
    assert captured.out != ""


def test_user_player_turn_valid_input(monkeypatch, user_player, board):
    # Given
    monkeypatch.setattr('builtins.input', lambda _: "0")
    # When
    x, y = user_player.turn(board)
    # Then
    assert (x, y) == (0, 0)


def test_user_player_invalid_position_prints_message(capsys, user_player):
    # When
    user_player.invalid_position()
    # Then
    captured = capsys.readouterr()
    assert captured.out != ""


def test_user_player_win_prints_message(capsys, user_player):
    # When
    user_player.win()
    # Then
    captured = capsys.readouterr()
    assert captured.out != ""


def test_user_player_loose_prints_message(capsys, user_player):
    # When
    user_player.loose()
    # Then
    captured = capsys.readouterr()
    assert captured.out != ""


def test_user_player_draw_prints_message(capsys, user_player):
    # When
    user_player.draw()
    # Then
    captured = capsys.readouterr()
    assert captured.out != ""


def test_bot_player_start_prints_message(capsys, bot_player):
    # When
    bot_player.start()
    # Then
    captured = capsys.readouterr()
    assert captured.out != ""


def test_bot_player_turn_valid_input(bot_player, board):
    # When
    x, y = bot_player.turn(board)
    # Then
    assert (x, y) in board.get_empty_spots()


def test_bot_invalid_position_raise_error(bot_player):
    # When
    with pytest.raises(ValueError) as exc:
        bot_player.invalid_position()
    # Then
    assert str(exc.value) != ""


def test_bot_player_win_prints_message(capsys, bot_player):
    # When
    bot_player.win()
    # Then
    captured = capsys.readouterr()
    assert captured.out != ""


def test_bot_player_loose_prints_message(capsys, bot_player):
    # When
    bot_player.loose()
    # Then
    captured = capsys.readouterr()
    assert captured.out != ""


def test_bot_player_draw_prints_message(capsys, bot_player):
    # When
    bot_player.draw()
    # Then
    captured = capsys.readouterr()
    assert captured.out != ""
