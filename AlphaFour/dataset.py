import random
import pickle

from connectfour import play_move, check_win_conditions
from minimax import get_valid_moves
from minimax import minimax, simple_eval_fn



# board encoding
def encode_board(board, player):
    """
    Encode board from current player's perspective:
    1  = current player piece
    -1 = opponent piece
    0  = empty
    """

    return [
        0 if cell == 0 else
        1 if cell == player else
        -1
        for cell in board
    ]




# filter meaningful states
def is_useful_state(board):
    """
    Ignore extremely early-game positions.
    """

    filled = sum(1 for x in board if x != 0)
    return filled >= 6  # slightly stricter than before




# minimax label
def label_move(board, player, depth=2):
    """
    Uses minimax to label a position.
    Depth is intentionally LOW for speed.
    """

    _, best_moves = minimax(
        board.copy(),
        simple_eval_fn,
        player,
        player,
        depth
    )

    if not best_moves:
        return None

    return random.choice(best_moves)



# self-play generation 
def generate_dataset(num_games=200, depth=2):
    """
    Fast dataset generator (balanced + lightweight).
    """

    X, y = [], []

    for game_idx in range(num_games):

        if game_idx % 20 == 0:
            print(f"Generating game {game_idx}/{num_games}")

        board = [0] * 42
        player = 1

        move_count = 0

        while True:

            valid_moves = get_valid_moves(board)

            if not valid_moves:
                break

    

            if is_useful_state(board) and random.random() < 0.6:

                move = label_move(board, player, depth)

                if move is not None:

                    X.append(encode_board(board, player))
                    y.append(move)

           # play move
            if random.random() < 0.7:
                move = random.choice(valid_moves)
            else:
                move = label_move(board, player, depth)

                if move is None:
                    move = random.choice(valid_moves)

            play_move(board, player, move)

            move_count += 1

            winner = check_win_conditions(board)

            if winner != 0 or move_count > 42:
                break

            player = 3 - player

    return X, y



def save_dataset(X, y, filename="dataset.pkl"):
    with open(filename, "wb") as f:
        pickle.dump((X, y), f)


def load_dataset(filename="dataset.pkl"):
    with open(filename, "rb") as f:
        return pickle.load(f)



if __name__ == "__main__":

    print("generating dataset...")

    X, y = generate_dataset(num_games=200, depth=2)

    print("samples:", len(X))

    save_dataset(X, y)

    print("dataset saved - dataset.pkl")