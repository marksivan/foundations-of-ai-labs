import random

from connectfour import play_move
from connectfour import check_win_conditions


def get_valid_moves(board):
    """
    Returns list of playable columns.
    A column is playable if its top cell is empty.
    """

    valid_moves = []

    for col in range(7):

        if board[col] == 0:
            valid_moves.append(col)

    return valid_moves


def evaluate_window(window, player):
    """
    Scores a group of 4 cells.
    """

    opponent = 2 if player == 1 else 1

    score = 0

    player_count = window.count(player)
    opponent_count = window.count(opponent)
    empty_count = window.count(0)

    # strong patterns
    if player_count == 4:
        score += 100

    elif player_count == 3 and empty_count == 1:
        score += 10

    elif player_count == 2 and empty_count == 2:
        score += 3

    # defensive penalty
    if opponent_count == 3 and empty_count == 1:
        score -= 8

    return score


def simple_eval_fn(board, player):
    """
    Heuristic evaluation function.
    """

    opponent = 2 if player == 1 else 1

    score = 0

    # center column preference
    center_indices = [3, 10, 17, 24, 31, 38]

    for idx in center_indices:

        if board[idx] == player:
            score += 4

        elif board[idx] == opponent:
            score -= 4

    # horizontal windows
    for row in range(6):

        start = row * 7

        for col in range(4):

            window = [
                board[start + col + i]
                for i in range(4)
            ]

            score += evaluate_window(window, player)

    # vertical windows
    for col in range(7):

        for row in range(3):

            window = [
                board[(row + i) * 7 + col]
                for i in range(4)
            ]

            score += evaluate_window(window, player)

    # positive diagonals
    for row in range(3):

        for col in range(4):

            window = [
                board[(row + i) * 7 + (col + i)]
                for i in range(4)
            ]

            score += evaluate_window(window, player)

    # negative diagonals
    for row in range(3, 6):

        for col in range(4):

            window = [
                board[(row - i) * 7 + (col + i)]
                for i in range(4)
            ]

            score += evaluate_window(window, player)

    return score


def minimax(board,
            eval_fn,
            whose_turn,
            who_am_i,
            depth):
    """
    Standard minimax search.
    """

    winner = check_win_conditions(board)

    # terminal states
    if winner != 0:

        if winner == who_am_i:
            return (float("inf"), [])

        else:
            return (float("-inf"), [])

    valid_moves = get_valid_moves(board)

    # tie
    if len(valid_moves) == 0:
        return (0, [])

    # depth cutoff
    if depth == 0:
        return (eval_fn(board, who_am_i), [])

    move_values = []

    for move in valid_moves:

        new_board = board.copy()

        play_move(new_board,
                  whose_turn,
                  move)

        value, _ = minimax(
            new_board,
            eval_fn,
            3 - whose_turn,
            who_am_i,
            depth - 1
        )

        move_values.append((move, value))

    # maximizing player
    if whose_turn == who_am_i:

        best_value = max(v for _, v in move_values)

    else:

        best_value = min(v for _, v in move_values)

    best_moves = [
        move
        for move, value in move_values
        if value == best_value
    ]

    return (best_value, best_moves)


def initialize_my_player_fn(depth=3):
    """
    Returns a minimax player function.
    """

    def my_player(board, player):

        _, best_moves = minimax(
            board,
            simple_eval_fn,
            player,
            player,
            depth
        )

        return random.choice(best_moves)

    return my_player