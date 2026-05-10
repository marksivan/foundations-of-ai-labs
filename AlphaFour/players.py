import random


def random_player_fn(board, player):

    valid_moves = []

    for col in range(7):

        if board[col] == 0:
            valid_moves.append(col)

    return random.choice(valid_moves)