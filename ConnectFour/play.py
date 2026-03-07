from connectfour import check_win_conditions
from connectfour import play_move
from connectfour import print_board
from players import random_player_fn
import sys
import time
from tqdm import tqdm


def play_game(player1_fn, player2_fn, min_delay=0.2, visualize=True):
    def clear_screen():
        # Clear screen and move cursor to (0,0)
        sys.stdout.write("\033[2J\033[H")
        sys.stdout.flush()

    num_rows, num_cols = 6, 7
    board = [0 for _ in range(num_rows * num_cols)]
    moves_made = 0
    current_player = 1
    while check_win_conditions(board) == 0 and moves_made < 42:
        if visualize:
            clear_screen()
            print_board(board)
            print(f"\nplayer {current_player} is thinking...")
        player_fn = player1_fn if current_player == 1 else player2_fn
        start = time.time()
        col = player_fn(board, current_player)
        if visualize:
            elapsed = time.time() - start
            if elapsed < min_delay:
                time.sleep(min_delay - elapsed)
        play_move(board, current_player, col)
        current_player = 2 if current_player == 1 else 1
        moves_made += 1
    winner = check_win_conditions(board)
    if visualize:
        clear_screen()
        print_board(board)
        if winner == 0:
            print("\ntie!")
        else:
            print(f"\nwinner is player {winner}!")
    return winner


def play_tournament(player1_fn, player2_fn, num_rounds):
    p1_wins, p2_wins, ties = 0, 0, 0
    for _ in tqdm(range(num_rounds)):
        winner = play_game(player1_fn, player2_fn, visualize=False)
        if winner == 0:
            ties += 1
        elif winner == 1:
            p1_wins += 1
        elif winner == 2:
            p2_wins += 1
        winner = play_game(player2_fn, player1_fn, visualize=False)
        if winner == 0:
            ties += 1
        elif winner == 1:
            p2_wins += 1
        elif winner == 2:
            p1_wins += 1
    print(f"P1-P2-T: {p1_wins}-{p2_wins}-{ties}")


if __name__ == "__main__":
    play_game(random_player_fn, random_player_fn)
