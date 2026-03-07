import random


def random_player_fn(board, player):
    num_cols = 7
    valid_moves = [i for i in range(num_cols) if board[i] == 0]
    if len(valid_moves) == 0:
        return None
    else:
        return random.choice(valid_moves)


def minimax(board, eval_fn, whose_turn, who_am_i, num_plys):
    raise NotImplementedError("fill this in!")


def initialize_my_player_fn(num_plys=4):
    raise NotImplementedError("fill this in!")
