"""
Chunked List of Milestones to do
1. Create build plan
2. Create the board and print it with mines showing
3. Compute the cells neighbors that are mines
4. Create the player's board view that only shows revealed tiles
5. Read a move and check if the tile is mine or not
6. Win and loss detection
7. Flood fill creation
8. Create flag-mode
END OF MVP
"""

import random

# 1. Settings and Data Types

ROWS = 9
COLUMNS = 9
MINE_COUNT = 10

# A cell is a set of coordinates (row, col)
Cell = tuple[int, int]

class Game():
    pass


class Move():
    pass


# 2. Game Logic

def all_cells() -> list[Cell]:
    return [(row, col) for row in range(ROWS) for col in range(COLUMNS)]


def is_on_board(cell: Cell) -> bool:
    row, col = cell
    return 0 <= row < ROWS and 0 <= col < COLUMNS


def neighbors(cell: Cell) -> list[Cell]:
    row, col = cell
    results = []
    for dr in (-1, 0 , 1):
        for dc in (-1, 0, 1):
            if (dr, dc) != (0, 0):
                n = (row + dr, col + dc)
                if is_on_board(n):
                    results.append(n)
    return results


def count_adjacent_mines(cell: Cell) -> int:
    return sum(1 for n in neighbors(cell) if n in mines)


def new_game() -> Game:
    pass


def reveal() -> Game:
    pass


def toggle_flag() -> Game:
    pass


def apply_move() -> Game:
    pass


def is_lost() -> bool:
    pass


def is_won() -> bool:
    pass


# 3. Player Input

# Defines possible allowed inputs
ACTIONS = {"r": "reveal", "reveal": "reveal", "f": "flag", "flag": "flag"}


def parse_move() -> Move | str:
    pass


def check_move() -> str | None:
    pass


def read_move() -> Move | str:
    pass


# 4. Creating the board

# ANSI escape codes for color in terminal
RESET = "\033[0m"
BOLD = "\033[1m"
DIM = "\033[2m"
RED = "\033[31m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
BLUE = "\033[34m"
MAGENTA = "\033[35m"
CYAN = "\033[36m"
WHITE_ON_RED = "\033[97;41m"
CLEAR_SCREEN = "\033[2J\033[H"

NUMBER_COLORS = {1: BLUE, 2: GREEN, 3: RED, 4: MAGENTA, 5: YELLOW, 6: CYAN, 7: BOLD, 8: DIM}


def paint() -> str:
    pass


def cell_symbol() -> str:
    pass


def render_row() -> str:
    pass


def render_board() -> str:
    pass

def render_screen() -> str:
    pass


# 5. Game Loop

def play() -> None:
    pass


def main() -> None:
    pass


if __name__ == "__main__":
    main()