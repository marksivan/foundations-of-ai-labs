import random


def random_player_fn(board):
    legal_moves = [i for i, val in enumerate(board) if val == 0]
    if len(legal_moves) == 0:
        return None
    else:
        return random.choice(legal_moves)


def create_optimal_player_fn(playbook):
    def player_fn(board):
        best_moves = playbook[tuple(board)]
        if len(best_moves) > 0:
            return random.choice(best_moves)
        else:
            return None

    return player_fn
