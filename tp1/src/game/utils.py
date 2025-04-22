from .board import Board


def board_to_index(board: Board):
    index = ""
    for i in range(3):
        for j in range(3):
            index += board.grid[i][j]
    return index


def pos_to_xy(pos: int):
    pos_x = pos % 3
    pos_y = int(pos / 3)
    return pos_x, pos_y


def xy_to_pos(pos_x: int, pos_y: int):
    return pos_x + pos_y * 3
