"""
Chunked List of Milestones to do
1. Create build plan and function stubs ✅
2. Define cells, the game environment, and a move ✅
3. Compute the cells neighbors that are mines ✅
4. Create the screen with mine count, flags, and colors ✅
5. Randomize mines and create tests ✅
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
    """Immutable snapshot of the game."""

    mines: frozenset[Cell]
    revealed: frozenset[Cell] = frozenset()
    flagged: frozenset[Cell] = frozenset()
    exploded: Cell | None = None


class Move(NamedTuple):
    """One input from the player."""

    action: str  # "flag" or "reveal"
    cell: Cell


# 2. Game Logic

def all_cells() -> list[Cell]:
    """Returns a list of all coordinates in a ROWSxCOLS grid."""
    return [(row, col) for row in range(ROWS) for col in range(COLS)]


def is_on_board(cell: Cell) -> bool:
    """Returns T/F if a given cell is on the ROWxCOL board"""
    row, col = cell
    return 0 <= row < ROWS and 0 <= col < COLS


def neighbors(cell: Cell) -> list[Cell]:
    """Returns all cells touching this one, includes diagonals.

    Only cells on board included: 
    corner = 3, side = 5, others = 8.
    """

    row, col = cell
    results = []

    # Try every offset (-1, 0, 1) in col/row direction
    for dr in (-1, 0 , 1):  # dr = move in row
        for dc in (-1, 0, 1):  # dc = move in col
            if (dr, dc) != (0, 0):  # Skips the cell itself
                # Adds the dr/dc to the actual row/col of the cell 
                # to find the actual coords within the board
                n = (row + dr, col + dc)
                if is_on_board(n):  # Drops cells past edge of the board
                    results.append(n)
    return results


def count_adjacent_mines(cell: Cell, mines: frozenset[Cell]) -> int:
    """Finds the # of adj. cells that are mines."""
    return sum(1 for n in neighbors(cell) if n in mines)


def new_game() -> Game:
    """Creates a new game with mines randomly assigned."""
    mines = random.sample(all_cells(), MINE_COUNT)
    return Game(mines=frozenset(mines))


def flood_fill(start: Cell, mines: frozenset[Cell], blocked: frozenset[Cell]) -> frozenset[Cell]:
    return frozenset({start}) # Todo for step 8


def reveal(game: Game, cell: Cell) -> Game:
    """Reveals a cell. If it is the mine, game over."""
    if cell in game.mines:
        return game._replace(exploded=cell)
    
    opened = flood_fill(cell, game.mines, blocked=game.flagged)
    return game._replace(revealed=game.revealed | opened)


def toggle_flag(game: Game, cell: Cell) -> Game:
    """Toggles the flag on a cell"""
    return game._replace(flagged=game.flagged ^ {cell})


def apply_move(game: Game, move: Move) -> Game:
    """Toggles a cell's flag, or reveals that cell"""
    if move.action == "flag":
        return toggle_flag(game, move.cell)
    return reveal(game, move.cell)


def is_lost() -> bool:
    pass


def is_won() -> bool:
    pass


# 3. Player Input

# Defines possible allowed inputs
ACTIONS = {"r": "reveal", "reveal": "reveal", "f": "flag", "flag": "flag"}


def parse_move(text: str) -> Move | str:
    """Turns the input text 'r 4 6' into a Move, or returns an error"""
    parts = text.split()

    if len(parts) != 3:
        return "Type a mode, a row and a column, for example: r 3 4"

    mode, row, col = parts
    if mode not in ACTIONS:
        return f"Unknown mode '{mode}'. Use 'r' to reveal or 'f' to flag."
    if not (row.isdecimal() and col.isdecimal()):
        return "Row and column must be whole numbers."

    cell = (int(row) - 1, int(col) - 1)  # Player counts from 1
    if not is_on_board(cell):
        return f"Row must be 1-{ROWS} and column must be 1-{COLS}."

    return Move(ACTIONS[mode], cell)


def check_move(game: Game, move: Move) -> str | None:
    """Return an error message if the move is not allowed right now."""
    if move.cell in game.revealed:
        return "That cell is already revealed."
    if move.action == "reveal" and move.cell in game.flagged:
        return "That cell is flagged. Unflag it first with: f row col"
    return None
    

def read_move(game: Game, text: str) -> Move | str:
    """Parses and validates the player's move. Returns move or error."""
    move = parse_move(text)
    if isinstance(move, str):
        return move
    return check_move(game, move) or move


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
    """Wraps the text in ANSI style and resets after."""
    return "".join(styles) + text + RESET


def cell_symbol(game: Game, cell: Cell, show_mines: bool) -> str:
    """Returns the colored cell symbol.

    Priority Order: exploded mine, mine if show_mines, flagged,
    hidden cell, adjacent mine count for revealed cell.
    """
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
    """Returns one row of the board, starting with the row's #."""
    cells = "".join(f" {cell_symbol(game, (row, col), show_mines)} " for col in range(COLS))
    return f"{row + 1:>2} |{cells}|"

def render_board(game: Game, show_mines: bool = False) -> str:
    """Returns the full board with column #s and border.
    
    show_mines = True; when game is over to show all mines."""
    column_numbers = "    " + "".join(f"{col + 1:^3}" for col in range(COLS))
    top_border     = "   ┌" + "───" * COLS + "┐"
    bottom_border  = "   └" + "───" * COLS + "┘"
    rows = [render_row(game, row, show_mines) for row in range(ROWS)]
    return "\n".join([column_numbers, top_border, *rows, bottom_border])

def render_screen(game: Game, message:str, show_mines: bool = False) -> str:
    """Returns the whole screen with title, board, help text, and message.
    
    Starts with ANSI code to clear screen and reset cursor.
    """
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
    """TEMPORARY."""
    game = new_game()
    message = "TESTING BOARD"

    while True:
        print(render_screen(game, message, show_mines=True))
        move = read_move(game, input("> "))
        if isinstance(move, str):
            message = paint(move, YELLOW)
        else:
            game = apply_move(game, move)
            message = ""


def main() -> None:
    play()



if __name__ == "__main__":
    main()