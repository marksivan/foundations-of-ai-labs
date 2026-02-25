from ttutil import print_board


def check_win_conditions(board):
    raise NotImplementedError("Fill this in!")


def play_game(player1_fn, player2_fn):
    raise NotImplementedError("Fill this in!")


def report_game(game):
    winner = check_win_conditions(game[-1])
    if winner == 0:
        print("\ntie!")
    else:
        print(f"\nplayer {winner} won!")
    for board in game:
        print_board(board)
        print("")
    return winner


def play_tournament(num_rounds, player1_fn, player2_fn):
    record = [0, 0, 0]  # ties, player1 wins, player2 wins
    for _ in range(num_rounds):
        game = play_game(player1_fn, player2_fn)
        winner = check_win_conditions(game[-1])
        record[winner] += 1
        game = play_game(player2_fn, player1_fn)
        winner = check_win_conditions(game[-1])
        if winner == 1:
            winner = 2
        elif winner == 2:
            winner = 1
        record[winner] += 1
    print(f"P1-P2-T: {record[1]}-{record[2]}-{record[0]}")


def compile_playbook():
    raise NotImplementedError("Fill this in!")
