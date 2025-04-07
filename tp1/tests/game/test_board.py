import pytest

from src.game.board import Board


@pytest.fixture
def board():
    return Board()


def test_place_symbol_empty_spot_returns_true(board):
    # When
    result = board.place_symbol('X', 0, 0)
    # Then
    assert result == True
    assert board.grid[0][0] == 'X'


def test_place_symbol_occupied_spot_returns_false(board):
    # Given
    board.place_symbol('X', 0, 0)
    # When
    result = board.place_symbol('O', 0, 0)
    # Then
    assert result == False


def test_place_symbol_out_of_bounds_returns_false(board):
    # When
    result = board.place_symbol('X', 3, 3)
    # Then
    assert result == False


def test_get_empty_spots_empty_board_returns_all_spots(board):
    # When
    result = board.get_empty_spots()
    # Then
    assert len(result) == 9


def test_get_empty_spots_partially_filled_board_returns_remaining_spots(board):
    # Given
    board.place_symbol('X', 0, 0)
    # When
    result = board.get_empty_spots()
    # Then
    assert len(result) == 8
    assert (0, 0) not in board.get_empty_spots()


def test_is_winner_no_winner_returns_false(board):
    # When
    result = board.is_winner('X')
    # Then
    assert result == False


def test_is_winner_row_win_returns_true(board):
    # Given
    board.place_symbol('X', 0, 0)
    board.place_symbol('X', 1, 0)
    board.place_symbol('X', 2, 0)
    # When
    result = board.is_winner('X')
    # Then
    assert result == True


def test_is_winner_column_win_returns_true(board):
    # Given
    board.place_symbol('O', 0, 0)
    board.place_symbol('O', 0, 1)
    board.place_symbol('O', 0, 2)
    # When
    result = board.is_winner('O')
    # Then
    assert result == True


def test_is_winner_diagonal_win_returns_true(board):
    # Given
    board.place_symbol('X', 0, 0)
    board.place_symbol('X', 1, 1)
    board.place_symbol('X', 2, 2)
    # When
    result = board.is_winner('X')
    # Then
    assert result == True

def test_is_winner_inverse_diagonal_win_returns_true(board):
    # Given
    board.place_symbol('X', 0, 2)
    board.place_symbol('X', 1, 1)
    board.place_symbol('X', 2, 0)
    # When
    result = board.is_winner('X')
    # Then
    assert result == True

def test_is_full_empty_board_returns_false(board):
    # When
    result = board.is_full()
    # Then
    assert result == False


def test_is_full_full_board_returns_true(board):
    # Given
    for y in range(3):
        for x in range(3):
            board.place_symbol('X', x, y)
    # When
    result = board.is_full()
    # Then
    assert result == True


def test_print_output_prints_message(capsys, board):
    # When
    board.print()
    # Then
    captured = capsys.readouterr()
    assert captured.out != ""
