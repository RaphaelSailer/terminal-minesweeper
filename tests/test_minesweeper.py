from minesweeper import (
    Game,
    Move,
    Cell,
    MINE_COUNT,
    neighbors,
    is_on_board,
    count_adjacent_mines,
    new_game,
    toggle_flag,
)


def test_corner_has_three_neighbors():
    assert len(neighbors((0, 0))) == 3


def test_edge_has_five_neighbors():
    assert len(neighbors((0, 5))) == 5


def test_middle_has_eight_neighbors():
    assert len(neighbors((3, 7))) == 8


def test_cell_not_in_cells_neighbors_list():
    assert (5, 7) not in neighbors((5, 7))


def test_corners_are_on_board():
    assert is_on_board((0, 0))
    assert is_on_board((8, 8))


def test_off_board_are_not_on_board():
    assert is_on_board((-1, 0)) is False
    assert is_on_board((0, -1)) is False
    assert is_on_board((9, 0)) is False
    assert is_on_board((0, 9)) is False


def test_adjacent_mine_count():
    mines = frozenset([(1, 1), (1, 2), (2, 2), (3, 2), (3, 6)])
    assert count_adjacent_mines((2, 1), mines) == 4
    assert count_adjacent_mines((2, 3), mines) == 3
    assert count_adjacent_mines((1, 3), mines) == 2
    assert count_adjacent_mines((2, 7), mines) == 1
    assert count_adjacent_mines((8, 1), mines) == 0


def test_new_game():
    game = new_game()
    assert len(game.mines) == MINE_COUNT
    assert all(is_on_board(mine) for mine in game.mines)
    assert game.revealed == frozenset()
    assert game.flagged == frozenset()


def test_toggle_flag():
    game = Game(mines=frozenset({0, 0}))
    flagged_game = toggle_flag(game, (3, 4))
    assert (3, 4) in flagged_game.flagged
    assert flagged_game._replace(flagged=game.flagged) == game

