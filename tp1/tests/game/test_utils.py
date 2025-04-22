import pytest

from src.game.board import Board
from src.game.utils import board_to_index, pos_to_xy, xy_to_pos


@pytest.fixture
def board():
    return Board()


def test_board_to_index(board):
    # Given
    board.grid = [
        ['X', 'O', 'X'],
        ['O', 'X', 'O'],
        ['X', ' ', 'X']
    ]
    # When
    result = board_to_index(board)
    # Then
    assert result == "XOXOXOX X"


def test_pos_to_xy():
    # Given
    pos = 5
    # When
    x, y = pos_to_xy(pos)
    # Then
    assert (x, y) == (2, 1)


def test_xy_to_pos():
    # Given
    x, y = 2, 1
    # When
    pos = xy_to_pos(x, y)
    # Then
    assert pos == 5
