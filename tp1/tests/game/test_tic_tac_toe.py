from unittest.mock import Mock

import pytest

from src.game.board import Board
from src.game.tic_tac_toe import TicTacToe


def create_mock_player():
    player = Mock()
    player.start = Mock()
    player.turn = Mock()
    player.invalid_position = Mock()
    player.win = Mock()
    player.loose = Mock()
    player.draw = Mock()
    return player


def create_game():
    mock_player1 = create_mock_player()
    mock_player2 = create_mock_player()
    return TicTacToe(mock_player1, mock_player2, Board()), mock_player1, mock_player2


def test_init_creates_game():
    # When
    game, _, _ = create_game()
    # Then
    assert isinstance(game, TicTacToe)
    assert isinstance(game.board, Board)
    assert isinstance(game.player1, Mock)
    assert isinstance(game.player2, Mock)


def test_start_seed_player1_call_player1_start():
    # Given
    game, mock_player1, mock_player2 = create_game()
    mock_player1.start.side_effect = Exception("Exit")
    game.SEED = 1
    # When
    with pytest.raises(Exception, match="Exit"):
        game.start()
    # Then
    mock_player1.start.assert_called_once()
    mock_player2.start.assert_not_called()


def test_start_seed_player2_call_player2_start():
    # Given
    game, mock_player1, mock_player2 = create_game()
    mock_player2.start.side_effect = Exception("Exit")
    game.SEED = 5
    # When
    with pytest.raises(Exception, match="Exit"):
        game.start()
    # Then
    mock_player2.start.assert_called_once()
    mock_player1.start.assert_not_called()


def test_start_after_player1_start_call_player1_turn():
    # Given
    game, mock_player1, mock_player2 = create_game()
    game.SEED = 1
    mock_player1.turn.side_effect = Exception("Exit")
    # When
    with pytest.raises(Exception, match="Exit"):
        game.start()
    # Then
    mock_player1.turn.assert_called_once()
    mock_player2.turn.assert_not_called()


def test_start_after_player2_start_call_player2_turn():
    # Given
    game, mock_player1, mock_player2 = create_game()
    game.SEED = 5
    mock_player2.turn.side_effect = Exception("Exit")
    # When
    with pytest.raises(Exception, match="Exit"):
        game.start()
    # Then
    mock_player2.turn.assert_called_once()
    mock_player1.turn.assert_not_called()


def test_start_after_player1_turn_call_player2_turn():
    # Given
    game, mock_player1, mock_player2 = create_game()
    game.SEED = 1
    mock_player1.turn.side_effect = lambda board: (0, 0)
    mock_player2.turn.side_effect = Exception("Exit")
    # When
    with pytest.raises(Exception, match="Exit"):
        game.start()
    # Then
    mock_player1.turn.assert_called_once()
    mock_player2.turn.assert_called_once()


def test_start_after_player_turn_valid_move_updates_board():
    # Given
    game, mock_player1, mock_player2 = create_game()
    game.SEED = 1
    mock_player1.turn.side_effect = lambda board: (0, 0)
    mock_player2.turn.side_effect = Exception("Exit")
    # When
    with pytest.raises(Exception, match="Exit"):
        game.start()
    # Then
    assert game.board.grid[0][0] == 'X'


def test_start_after_player_turn_invalid_move_calls_invalid_turn():
    # Given
    game, mock_player1, _ = create_game()
    game.SEED = 1
    mock_player1.turn.side_effect = lambda board: (5, 0)
    mock_player1.invalid_position.side_effect = Exception("Exit")
    # When
    with pytest.raises(Exception, match="Exit"):
        game.start()
    # Then
    mock_player1.invalid_position.assert_called_once()


def test_start_after_player_turn_invalid_move_does_not_update_board():
    # Given
    game, mock_player1, _ = create_game()
    game.SEED = 1
    mock_player1.turn.side_effect = lambda board: (5, 0)
    mock_player1.invalid_position.side_effect = Exception("Exit")
    # When
    with pytest.raises(Exception, match="Exit"):
        game.start()
    # Then
    assert len(game.board.get_empty_spots()) == 9


def test_start_after_player_turn_invalid_move_and_then_valid_move_update_board():
    # Given
    game, mock_player1, mock_player2 = create_game()
    game.SEED = 1
    mock_player1.turn.side_effect = [(5, 0), (1, 0)]
    mock_player2.turn.side_effect = Exception("Exit")
    # When
    with pytest.raises(Exception, match="Exit"):
        game.start()
    # Then
    assert game.board.grid[0][1] == 'X'


def test_start_player1_turn_win_call_player1_win_and_call_player2_loose():
    # Given
    game, mock_player1, mock_player2 = create_game()
    game.SEED = 1
    mock_player1.turn.side_effect = lambda board: (0, 0)
    game.board.place_symbol('X', 0, 1)
    game.board.place_symbol('X', 0, 2)
    # When
    game.start()
    # Then
    mock_player1.win.assert_called_once()
    mock_player2.loose.assert_called_once()


def test_start_player2_turn_win_call_player2_win_and_call_player1_loose():
    # Given
    game, mock_player1, mock_player2 = create_game()
    game.SEED = 1
    mock_player1.turn.side_effect = lambda board: (0, 0)
    mock_player2.turn.side_effect = lambda board: (1, 0)
    game.board.place_symbol('O', 1, 1)
    game.board.place_symbol('O', 1, 2)
    # When
    game.start()
    # Then
    mock_player2.win.assert_called_once()
    mock_player1.loose.assert_called_once()


def test_start_after_board_is_full_player1_draw_player2_draw():
    # Given
    game, mock_player1, mock_player2 = create_game()
    for y in range(3):
        for x in range(3):
            game.board.place_symbol('X' if (x + y) % 2 == 0 else 'O', x, y)
    # When
    game.start()
    # Then
    mock_player1.draw.assert_called_once()
    mock_player2.draw.assert_called_once()
