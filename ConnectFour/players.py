import random
from connectfour import play_move, check_win_conditions


def random_player_fn(board, player):
    num_cols = 7
    valid_moves = [i for i in range(num_cols) if board[i] == 0]
    if len(valid_moves) == 0:
        return None
    else:
        return random.choice(valid_moves)





def initialize_my_player_fn(num_plys=4):

    def my_player(board, whose_turn):
        val, moves = minimax(board, simple_eval_fn, whose_turn, whose_turn, num_plys)
        
        # choose randomly among equally good moves
        return random.choice(moves)

    return my_player


def get_valid_moves(board):
    """Return list of columns (0–6) that are not full."""
    valid = []
    for col in range(7):
        if board[col] == 0:  # top cell empty,so column playable
            valid.append(col)
    return valid


def copy_board(board):
    return board.copy()


def minimax(board, eval_fn, whose_turn, who_am_i, num_plys):
    winner = check_win_conditions(board)

    # TERMINAL
    if winner != 0:
        if winner == who_am_i:
            return (float('inf'), [])
        else:
            return (float('-inf'), [])

    # depth cutoff
    if num_plys <= 0:
        return (eval_fn(board, who_am_i), [])

    valid_moves = get_valid_moves(board)

    # tie
    if not valid_moves:
        return (0, [])

    move_vals = []

    # evaluate every move (no pruning)
    for move in valid_moves:
        new_board = board.copy()
        play_move(new_board, whose_turn, move)

        val, _ = minimax(
            new_board,
            eval_fn,
            3 - whose_turn,
            who_am_i,
            num_plys - 1
        )

        move_vals.append((move, val))

    #  max player
    if whose_turn == who_am_i:
        best_val = max(v for _, v in move_vals)
    else:
        best_val = min(v for _, v in move_vals)

    # filtering of optimal moves
    best_moves = [m for m, v in move_vals if v == best_val]

    return (best_val, best_moves)

def simple_eval_fn(board, player):
    opponent = 2 if player == 1 else 1

    score = 0

    # center column preference 
    center_indices = [3, 10, 17, 24, 31, 38]
    for i in center_indices:
        if board[i] == player:
            score += 3
        elif board[i] == opponent:
            score -= 3

    return score