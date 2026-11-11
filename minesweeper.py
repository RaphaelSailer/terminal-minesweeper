"""
Chunked List of Milestones to do
1. Create build plan and function stubs ✅
2. Define cells, the game environment, and a move ✅
3. Compute the cells neighbors that are mines ✅
4. Create the screen with mine count, flags, and colors ✅
5. Randomize minds and create tests
6. Read a move and reveal a cell
7. Win and Loss
8. Flood Fill
END OF MVP
"""

import random
from functools import reduce
from typing import NamedTuple

# 1. Settings and Data Types

ROWS = 9
COLS = 9
MINE_COUNT = 10

# A cell is a set of coordinates (row, col)
Cell = tuple[int, int]

class Game(NamedTuple):
    # Immutable snapshot of the game

    mines: frozenset[Cell]
    revealed:frozenset[Cell] = frozenset()
    flagged: frozenset[Cell] = frozenset()
    exploded: Cell | None = None


class Move(NamedTuple):
    # One input from the player

    action: str  # "flag" or "reveal"
    cell: Cell


# 2. Game Logic

def all_cells() -> list[Cell]:
    # Returns a list of all coordinates in a ROWSxCOLS grid
    return [(row, col) for row in range(ROWS) for col in range(COLS)]


def is_on_board(cell: Cell) -> bool:
    row, col = cell
    return 0 <= row < ROWS and 0 <= col < COLS


def neighbors(cell: Cell) -> list[Cell]:
    """ 
        Finds all neighbors of the cell:
     - corner = 3, side = 5, others = 8
     - dr = move in row, dc = move in col
     - imagines the cell at (0, 0)
     - checks in each direction, includes diagonals, excludes itsels
     - adds the dr/dc to the actual row/col of the cell to find the 
       coords within the game grid
    """

    row, col = cell
    results = []
    
    for dr in (-1, 0 , 1):
        for dc in (-1, 0, 1):
            if (dr, dc) != (0, 0):
                n = (row + dr, col + dc)
                if is_on_board(n):
                    results.append(n)
    return results


def count_adjacent_mines(cell: Cell, mines: frozenset[Cell]) -> int:
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


def paint(text: str, *styles: str) -> str:
    return "".join(styles) + text + RESET


def cell_symbol(game: Game, cell: Cell, show_mines: bool) -> str:
    if cell == game.exploded: 
        return paint("*", BOLD, WHITE_ON_RED)
    if show_mines and cell in game.mines:
        return paint("*", BOLD, RED)
    if cell in game.flagged:
        return paint("F", BOLD, RED)
    if cell not in game.revealed:
        return paint("■", DIM)

    count = count_adjacent_mines(cell, game.mines)
    if count == 0:
        return " "
    else:
        return paint(str(count), BOLD, NUMBER_COLORS[count])

def render_row(game: Game, row: int, show_mines: bool) -> str:
    cells = "".join(f" {cell_symbol(game, (row, col), show_mines)} " for col in range(COLS))
    return f"{row + 1:>2} |{cells}|"

def render_board(game: Game, show_mines: bool = False) -> str:
    column_numbers = "    " + "".join(f"{col + 1:^3}" for col in range(COLS))
    top_border     = "   ┌" + "───" * COLS + "┐"
    bottom_border  = "   └" + "───" * COLS + "┘"
    rows = [render_row(game, row, show_mines) for row in range(ROWS)]
    return "\n".join([column_numbers, top_border, *rows, bottom_border])

def render_screen(game:Game, message:str, show_mines: bool = False) -> str:
    title = paint("  T E R M I N A L   M I N E S W E E P E R", BOLD)
    help_text = paint("  r row col = reveal    f row col = flag / unflag", DIM)
    return "\n".join([
        CLEAR_SCREEN + title,
        "", 
        render_board(game, show_mines), 
        "", 
        help_text, 
        "", 
        "  " + message
    ])

# 5. Game Loop

def play() -> None:
    pass


def main() -> None:
    pass



if __name__ == "__main__":
    main()